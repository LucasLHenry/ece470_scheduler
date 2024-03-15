# RUN THIS FILE TO RUN THE PROGRAM
import courses_parser as parser
from classes import Schedule, Section, Course
import operator

def sort_courses(courses_list) -> list[Course]:
    """sorts courses by number of available sections to make search tree more efficient. 
    
    Args:
        courses_list (list[Course]): list to be sorted

    Returns:
        list[Course]: sorted list
    """
    return sorted(courses_list, key=lambda Course: Course.num_sections)

def recur_schedule(courses_list: list[Course], curr_schedule: Schedule = Schedule(), curr_course_index: int = 0) -> tuple[Schedule, bool]:
    """recursively explores the solution space until it finds a solved schedule
    Args:
        courses_list (list[Course]): courses to be added to the schedule
        curr_schedule (Schedule): schedule that courses will be added to. Acts as the nodes of the tree
        curr_course_index (int): internal to recursion, used to keep track of how many courses have been added. Node counter in tree

    Returns:
        Schedule: successful schedule with added courses. Empty schedule if unsuccessful
        Bool: True if successful, False if unable to find a schedule that includes all courses
    """
    if curr_course_index == len(courses_list):
        return curr_schedule, True
    for sectn in courses_list[curr_course_index].sections:
        if curr_schedule.section_is_valid(sectn):
            curr_schedule.add(sectn)
            sched, check = recur_schedule(courses_list, curr_schedule, curr_course_index + 1)
            if check:
                return sched, True
            else:
                curr_schedule.remove(sectn)
    return curr_schedule, False

def build_schedule(courses_list) -> Schedule:
    """organizes course list and initializes recursive scheduler
    
    Args:
        courses_list (list[Course]): courses to be added to the schedule

    Returns:
        Schedule: successful schedule with added courses. Empty schedule if unsuccessful
        or
        Bool: False if unsuccessful
    """
    courses_list = sort_courses(courses_list)
    schedule, check = recur_schedule(courses_list)
    if check:
        return schedule
    print("impossible to include all classes in schedule")
    return False
    

def test():
    courses_list = parser.get_all_courses()
    schedule = build_schedule(courses_list)
    return schedule
    print("new schedule:")
    for i in schedule.sections:
        print(i)


if __name__ == "__main__":
    test()