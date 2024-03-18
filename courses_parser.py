import json, os
from typing import Union
from classes import *
from aux_functions import get_time, gen_time

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
        Print (bool): Prints the names to terminal if print is true
        
    Returns:
        list[str]: a list of the names of all the courses in the database
    """
    names_list = []
    with open(database_file) as f:
        db = json.load(f)
        for crs in db["courses"]:
            names_list.append(crs["course_name"])
    if Print:
        for crs in sorted(names_list):
            print(crs)
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
    
def prompt_for_courses() -> list[Course]:
    """prompts the user to input a list of course names, then returns a list of the 
    corresponding courses and sections from the database. Course names must be in database
    
    Returns:
        list[Course]: all the courses it found in the database matching the prompt
    """
    print("Enter course names, or a list of names separated by commas. Enter 'all' for all database courses. Press enter on a blank line when finished")
    course_list = []
    while(True):
        inpts = input("Add course(s): ")
        if inpts.upper() == "ALL":
            return get_all_courses()
        elif inpts:
            for inpt in inpts.split(","):
                course = find_course(inpt)
                if course:
                    course_list.append(course)
                    print("Successfully added", course.name)
                else:
                    print("Failed to find", inpt, "in database")
        else:
            break
    return course_list


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