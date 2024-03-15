# RUN THIS FILE TO RUN THE PROGRAM
import courses_parser as parser
from classes import *
import operator

def sort_courses(courses_list) -> list[Course]:
    """sorts courses by number of available sections to make search tree more efficient. Returns sorted list"""
    return sorted(courses_list, key=lambda Course: Course.num_sections)

def build_schedule(courses_list, curr_course_index = 0, curr_schedule = Schedule()) -> tuple[Schedule, bool]:
    """recursively explores the solution space until it finds a solved schedule"""
    if curr_course_index == len(courses_list):
        return curr_schedule, True
    for sectn in courses_list[curr_course_index].sections:
        if curr_schedule.section_is_valid(sectn):
            curr_schedule.add(sectn)
            sched, check = build_schedule(courses_list, curr_course_index + 1, curr_schedule)
            if check:
                return sched, True
            else:
                curr_schedule.remove(sectn)
    return curr_schedule, False
    

def test():
    courses_list = parser.get_all_courses()
    sort_courses(courses_list)
    schedule, check = build_schedule(courses_list)
    return schedule


if __name__ == "__main__":
    test()