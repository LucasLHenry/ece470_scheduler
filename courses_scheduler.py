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