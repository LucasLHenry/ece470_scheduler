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

def recur_schedule(courses_list: list[Course], num_courses_goal: int, sched_list: list[Schedule] = [], curr_schedule: Schedule = Schedule(), curr_course_index: int = 0) -> tuple[Schedule, bool]:
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
        return True, sched_list, curr_schedule, curr_course_index
    
    if curr_schedule.num_sections == num_courses_goal:
        sched_list.append(curr_schedule)
        return False, sched_list, curr_schedule, curr_course_index - 1
    
    curr_section_index = 0
    new_course_index = curr_course_index

    while curr_section_index < courses_list[curr_course_index].num_sections:
        sectn = courses_list[curr_course_index].sections[curr_section_index]
        if curr_schedule.section_is_valid(sectn):
            curr_schedule.add(sectn)
            no_more_courses, sched_list, curr_schedule, new_course_index = recur_schedule(courses_list, num_courses_goal, sched_list, curr_schedule, curr_course_index + 1)
            if no_more_courses:
                return True, sched_list, curr_schedule, curr_course_index
            else:
                curr_schedule.remove(sectn)
        if new_course_index == curr_course_index:
            curr_section_index += 1
        else:
            curr_course_index = new_course_index
            curr_section_index = 0

    sched_list.append(curr_schedule)
    return False, sched_list, curr_schedule, curr_course_index 

def build_schedule(courses_list: list[Course], num_courses_goal: int) -> Schedule:
    """organizes course list and initializes recursive scheduler
    
    Args:
        courses_list (list[Course]): courses to be added to the schedule
        num_courses_goal (int): number of courses desired by user

    Returns:
        Schedule: successful schedule with added courses. Empty schedule if unsuccessful
        or
        Bool: False if unsuccessful
    """
    courses_list = sort_courses(courses_list)
    no_more_courses, schedule_list, curr_schedule, curr_course_index = recur_schedule(courses_list, num_courses_goal)
    return schedule_list


def output(sched: Schedule):
    """Prints schedule found in a nice way for user to see

    Args:
        sched (Schedule): schedule object

    Returns:
        Printed schedule with courses in order of days and time from monday to friday
    """
    days = {"M": [], "T": [], "W": [], "R": [], "F": []}
    day_names = {
    "M": "MONDAY",
    "T": "TUESDAY",
    "W": "WEDNESDAY",
    "R": "THURSDAY",
    "F": "FRIDAY"
    }
    for course in sched.sections:
        for day in course.days:
            days[day].append(course)

    for day in days:
        if len(days[day]) == 0:
            print(f"{day_names[day]}: No Classes")
        else:
            print(f"{day_names[day]}:")
            sorted_courses = sorted(days[day], key=lambda cour: cour.start_time)
            for course in sorted_courses:
                print(f"\t{course}")


def test():
    courses_list = parser.get_all_courses()
    schedule = build_schedule(courses_list)
    return schedule
    print("new schedule:")
    for i in schedule.sections:
        print(i)


if __name__ == "__main__":
    test()