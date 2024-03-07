import json
from typing import Union

from classes import Section, Course

database_file = "db.json"

def get_all_courses() -> list[Course]:
    courses_list: list[Course] = []
    with open(database_file) as f:
        db = json.loads(f)
        courses_list = db["classes"]
        for crs in courses_list:
            courses_list.append(gen_course(crs))

def find_course(course_str: str) -> Union[Course, bool]:
    with open(database_file) as f:
        db = json.loads(f)
        courses_list = db["classes"]
        for crs in courses_list:
            if crs["course_name"] == course_str.upper():
                return gen_course(crs)
        return False

def gen_course(course_dict: dict) -> Course:
    sections_dict_list = course_dict["sections"]
    sections_list: list[Section] = []
    for sct in sections_dict_list:
        sections_list.append(gen_section(sct, course_dict["course_name"]))
    return Course(course_dict["course_name"], sections_list)
    
def gen_section(section_dict: dict, course_name: str) -> Section:
    start_time: int = get_time(section_dict["start_time"])
    end_time: int = get_time(section_dict["end_time"])
    name = section_dict["section_name"]
    days = section_dict["days"]
    return Section(name, course_name, start_time, end_time, days)
    
def get_time(time_str: str) -> int:
    hours, minutes_and_AM_PM = time_str.split(':')
    minutes = minutes_and_AM_PM[:2]
    out_val = int(hours)
    if minutes_and_AM_PM[-2:].upper() == "PM" and out_val != 12:
        out_val += 12
    out_val *= 60
    out_val += int(minutes)
    return out_val

def gen_time(time_val: int) -> str:
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