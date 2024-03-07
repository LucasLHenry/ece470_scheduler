import json
from typing import Union

from classes import Section, Course

database_file = "db.json"

def get_all_courses() -> list[Course]:
    """gets all courses from the database file. doesn't throw good errors currently

    Returns:
        list[Course]: all the courses it found in the database
    """
    courses_list: list[Course] = []
    with open(database_file) as f:
        db = json.loads(f)
        courses_list = db["classes"]
        for crs in courses_list:
            courses_list.append(gen_course(crs))

def find_course(course_str: str) -> Union[Course, bool]:
    """searches for a course with a specified name (ie MATH 100)
    if it can't find the course, returns False instead of the course object

    Args:
        course_str (str): input course name. not case sensitive, everything else sensitive

    Returns:
        Union[Course, bool]: either the course (if it was found) or False, if it was not
    """
    with open(database_file) as f:
        db = json.loads(f)
        courses_list = db["classes"]
        for crs in courses_list:
            if crs["course_name"] == course_str.upper():
                return gen_course(crs)
        return False

def gen_course(course_dict: dict) -> Course:
    """generates a course object from a json-parsed dictionary.
    interal use only, generally

    Args:
        course_dict (dict): dictionary with course info

    Returns:
        Course: course object generated from dictionary
    """
    sections_dict_list = course_dict["sections"]
    sections_list: list[Section] = []
    for sct in sections_dict_list:
        sections_list.append(gen_section(sct, course_dict["course_name"]))
    return Course(course_dict["course_name"], sections_list)
    
def gen_section(section_dict: dict, course_name: str) -> Section:
    """generates a section object from a json-parsed dictionary.
    internal use only, generally

    Args:
        section_dict (dict): dictionary with section info
        course_name (str): name of course section is from

    Returns:
        Section: Section object created
    """
    start_time: int = get_time(section_dict["start_time"])
    end_time: int = get_time(section_dict["end_time"])
    name = section_dict["section_name"]
    days = section_dict["days"]
    return Section(name, course_name, start_time, end_time, days)
    
def get_time(time_str: str) -> int:
    """generates a time number from a time string, in the format
    'hh:mm(AM/PM)'. The number is the number of minutes since the start of the day.
    This format makes it easy to calculate length and make comparisons for overlap

    Args:
        time_str (str): string representing the time, ie 9:30AM

    Returns:
        int: number of minutes since the start of the day
    """
    hours, minutes_and_AM_PM = time_str.split(':')
    minutes = minutes_and_AM_PM[:2]
    out_val = int(hours)
    if minutes_and_AM_PM[-2:].upper() == "PM" and out_val != 12:
        out_val += 12
    out_val *= 60
    out_val += int(minutes)
    return out_val

def gen_time(time_val: int) -> str:
    """generates a time string from a time number (opposite of get_time). See
    get_time docstring for more info

    Args:
        time_val (int): number of minutes since the start of the day

    Returns:
        str: time in 'hh:mm(AM/PM)' format
    """
    minutes = time_val % 60
    hours_24 = int((time_val - minutes) / 60)
    PM = True if hours_24 >= 12 else False
    PM_str = "PM" if PM else "AM"
    hours = hours_24 if hours_24 <= 12 else hours_24 - 12
    return f"{hours}:{minutes:02d}{PM_str}"


def main():  # tests the functions
    assert "9:20AM" == gen_time(560)
    assert "12:30PM" == gen_time(750)
    assert "4:50AM" == gen_time(290)
    assert "5:19PM" == gen_time(1039)
    assert 560 == get_time("9:20AM")
    assert 750 == get_time("12:30PM")
    assert 290 == get_time("4:50AM")
    assert 1039 == get_time("5:19PM")

if __name__ == "__main__":
    main()