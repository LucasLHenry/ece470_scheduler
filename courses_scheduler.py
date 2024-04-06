# RUN THIS FILE TO RUN THE PROGRAM
import courses_parser as parser
from classes import Schedule, Section, Course
from typing import Optional

def get_next_courses(schedule: Schedule, course_list: list[Course]) -> Optional[list[Course]]:
    """finds courses that have not yet been added to the schedule
    
    Args:
        schedule (Schedule): current schedule
        courses_list (list[Course]): courses requested by user to be added to the schedule

    Returns:
        list[Course]: list of courses that the user has requested but are not yet in the schedule
        or
        None: None if there are no user requested courses not in the schedule remaining
    """
    courses = []
    for course in course_list:
        if not schedule.course_in_schedule(course):
            courses.append(course)
    if len(courses) != 0: return courses
    return None

def get_sorted_sections(course_list: list[Course], schedule: Schedule) -> list[Section]:
    """from the list of courses that have yet to be added, sorts the valid sections of each course by cost
    Args:
        schedule (Schedule): current schedule
        course_list (list[Course]): list of courses intended to be added to the schedule

    Returns:
        list[Section]: list of sections to be added, sorted from least cost to highest cost
    """
    sections: list[Section] = []
    costs: list[int] = []
    for course in course_list:
        for section in course.sections:
            if schedule.section_is_valid(section):
                sections.append(section)
                costs.append(schedule.cost(section, course_list)) #cost is calculated here
    sorted_sections = [sec for _, sec in sorted(zip(costs, sections), key=lambda c_sec: c_sec[0])]
    return sorted_sections

def backtracking_search(curr_schedule: Schedule, course_list: list[Course], num_courses_goal: int) -> Optional[Schedule]:
    """recursive backtracking scheduler. Explores the solution space until the goal number of courses in the schedule is found, or it runs out of courses to add.
    The current schedule represents the current node, each child node has one added section.
    Uses cost function to inform search, checks lowest cost possibilities first. -> least-cost search.
    As long as the cost function is working correctly, this should find the optimal solution without any backtracking
    
    Args:
        curr_schedule (Schedule): current schedule
        course_list (list[Course]): list of courses intended to be added to the schedule
        num_courses_goal (int): goal number of courses in the schedule as determined by user

    Returns:
        Schedule: successful schedule with as many courses as possible towards the goal number of courses
        or
        Bool: None if unsuccessful
    """
    # if assignment is complete, return assignment
    if curr_schedule.num_sections == num_courses_goal: return Schedule
    next_courses = get_next_courses(curr_schedule, course_list)
    # no more classes to pick from, but not at desired number. Return possibility with most courses
    if next_courses is None: return Schedule 
    
    # this is where cost function gets applied to all potential additions
    sorted_sections = get_sorted_sections(next_courses, curr_schedule)
    
    for section in sorted_sections:
        curr_schedule.add(section)
        result: Optional[Schedule] = backtracking_search(curr_schedule, course_list, num_courses_goal)
        if result is not None: return result
        curr_schedule.remove(section)
    return None

def build_schedule(courses_list: list[Course], num_courses_goal: int) -> Schedule:
    """initializes recursive scheduler
    
    Args:
        courses_list (list[Course]): courses requested by user to be added to the schedule
        num_courses_goal (int): goal number of courses in the schedule as determined by user

    Returns:
        Schedule: successful schedule with added courses
        or
        Bool: False if unsuccessful
    """
    schedule = Schedule()
    result = backtracking_search(schedule, courses_list, num_courses_goal)
    if result is None: return False
    return schedule

def test():
    """used to debug scheduler"""
    courses_list = parser.get_all_courses()
    for course in courses_list:
        course.set_priority(1)
    schedule = build_schedule(courses_list, len(courses_list))
    print("new schedule:")
    for i in schedule.sections:
        print(i)


if __name__ == "__main__":
    test()