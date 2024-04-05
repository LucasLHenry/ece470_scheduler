import json, os
from typing import Union
from classes import *
from aux_functions import get_time, gen_time
import random, math

database_filename = "db.json"
database_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), database_filename)

def get_all_courses() -> list[Course]:
    """gets all courses from the database file. doesn't throw good errors currently

    Returns:
        list[Course]: all the courses it found in the database
    """
    courses_list: list[Course] = []
    with open(database_file) as f:
        db = json.load(f)
        courses_list_dict = db["courses"]
        for crs in courses_list_dict:
            courses_list.append(gen_course(crs))
    return courses_list

def list_all_courses(Print = False) -> list[str]:
    """lists the names of all possible courses in the database. 
    
    Args:
        Print (bool): Prints the names and number of sections to terminal if print is true
        
    Returns:
        list[str]: a list of the names of all the courses in the database
    """
    names_list = []
    with open(database_file) as f:
        db = json.load(f)
        for crs in db["courses"]:
            names_list.append(crs["course_name"])
    if Print:
        for crs in sorted(db["courses"], key=lambda x: x["course_name"]):
            plural = 's' if len(crs['sections']) != 1 else ''
            print(f"{crs['course_name']} with {len(crs['sections'])} section{plural}")
    return names_list

def find_course(course_str: str) -> Union[Course, bool]:
    """searches for a course with a specified name (ie MATH 100)
    if it can't find the course, returns False instead of the course object

    Args:
        course_str (str): input course name. not case sensitive, ignores spaces, everything else sensitive

    Returns:
        Union[Course, bool]: either the course (if it was found) or False, if it was not
    """
    with open(database_file) as f:
        db = json.load(f)
        courses_list = db["courses"]
        for crs in courses_list:
            if crs["course_name"].replace(" ", "") == course_str.upper().replace(" ", ""):                   
                return gen_course(crs)
        return False
    
def parse_priority(priority_str: str) -> Optional[int]:
    """parses a priority value into its corresponding integer

    Args:
        priority_str (str): the priority level as a string

    Returns:
        Optional[int]: _returns None if the parsing failed, and the integer if it didn't
    """
    try:
        priority_int = int(priority_str)
    except ValueError:
        return None
    if priority_int < 1 or priority_int > 3:
        return None
    return priority_int
    
def prompt_for_courses() -> tuple[list[Course], int]:
    """prompts the user to input a list of course names, then returns a list of the 
    corresponding courses and sections from the database. Course names must be in database
    
    Returns:
        tuple[list[Course], int]: all the courses it found in the database matching the prompt, 
        with priority fields filled, as well as number of desired courses.
    """
    print("Enter course names. Enter 'all' for all database courses. Press enter on a blank line when finished.")
    print("After each course entered, give the priority level for that course. 1 is top priority (required courses),")
    print("2 is medium priority (electives), and 3 is lowest priority (backup electives)")
    course_list = []
    while(True):
        inpt = input("Add course(s): ")
        if inpt.upper() == "ALL":
            course_list = get_all_courses()
            for course in course_list:
                course.priority = int(math.ceil(3*random.random()))
            break
        elif inpt:
            course = find_course(inpt)
            if course:
                # get priority level for course
                while True:
                    priority_str = input(f"priority for {course.name}: ")
                    priority_int = parse_priority(priority_str)
                    if priority_int is not None:
                        course.priority = priority_int
                        break
                    else:
                        print("priority int must be an integer between 1 and 3")
                course_list.append(course)
                print("Successfully added", course.name)
            else:
                print("Failed to find", inpt, "in database")
        else:
            break
    
    # get number of desired courses
    while True:
        num_courses_inpt = input("How many courses do you want: ")
        try:
            desired_num_courses = int(num_courses_inpt)
        except ValueError:
            print("number of classes must be an integer")
            continue
        if desired_num_courses < 1 or desired_num_courses > len(course_list):
            print("number of courses must be greater than 0 and less than or equal to the number of courses entered")
            continue
        break
    return course_list, desired_num_courses


def gen_course(course_dict: dict) -> Union[Course, bool]:
    """generates a course object from a json-parsed dictionary.
    interal use only, generally

    Args:
        course_dict (dict): dictionary with course info

    Returns:
        Union[Course, bool]: either the Course, or False if the dict was not parsable
    """
    try:
        sections_dict_list = course_dict["sections"]
    except KeyError:
        return False
    
    sections_list: list[Section] = []
    for sct in sections_dict_list:
        new_section = gen_section(sct, course_dict["course_name"])
        if new_section == False:
            return False
        sections_list.append(new_section)
    return Course(course_dict["course_name"], sections_list)
    
def gen_section(section_dict: dict, course_name: str) -> Union[Section, bool]:
    """generates a section object from a json-parsed dictionary.
    internal use only, generally

    Args:
        section_dict (dict): dictionary with section info
        course_name (str): name of course section is from

    Returns:
        Union[Section, bool]: Section object created or False if the dict couldn't be parsed
    """
    start_time: int = get_time(section_dict["start_time"])
    end_time: int = get_time(section_dict["end_time"])
    name = section_dict["section_name"]
    days = section_dict["days"]
    return Section(name, course_name, start_time, end_time, days)


def main():  # tests the functions
    print(get_all_courses())

if __name__ == "__main__":
    main()