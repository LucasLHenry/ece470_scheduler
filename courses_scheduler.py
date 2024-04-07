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

<<<<<<< HEAD
=======
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
    if curr_schedule.num_sections == num_courses_goal: return Schedule # if assignment is complete, return assignment
    next_courses = get_next_courses(curr_schedule, course_list)
    if next_courses is None: return Schedule # no more classes to pick from, but not at desired number. Return possibility with most courses
    sorted_sections = get_sorted_sections(next_courses, curr_schedule)# this is where cost function gets applied to all potential additions, returned as a cost-sorted list of sections to add
    for section in sorted_sections:
        curr_schedule.add(section)
        result: Optional[Schedule] = backtracking_search(curr_schedule, course_list, num_courses_goal)
        if result is not None: return result
        curr_schedule.remove(section)
    return None

>>>>>>> origin/algo_attempt
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
<<<<<<< HEAD
    

def course_in_schedule(schedule: Schedule, course: Course) -> bool:
    """checks whether or not a course is already in a schedule

    Args:
        schedule (Schedule): the schedule
        course (Course): the course

    Returns:
        bool: True if a section from the course is in the schedule, False otherwise
    """
    for section in schedule.sections:
        if section.course_name.upper() == course.name.upper():
            return True
    return False

def get_next_courses(schedule: Schedule, course_list: list[Course]) -> Optional[list[Course]]:
    """gets the next valid courses to expand. Uses priority, so generates a list of courses with
    the highest priority among courses in the list

    Args:
        schedule (Schedule): schedule used to make sure courses aren't already in schedule
        course_list (list[Course]): list of courses to check from

    Returns:
        Optional[list[Course]]: list of courses with highest priority, or None if there were none that aren't already in the schedule
    """
    highest_priority = 3
    courses = []
    for course in course_list:
        if not course_in_schedule(schedule, course):
            if course.priority == highest_priority: courses.append(course) # add to current list
            elif course.priority < highest_priority:  # need to restart list
                highest_priority = course.priority
                courses = [course]
    if len(courses) != 0: return courses
    return None

def get_sorted_sections(course_list: list[Course], schedule: Schedule) -> list[Section]:
    """from a list of courses (assuming all have same priority), returns a list of sections in order
    of cost

    Args:
        course_list (list[Course]): courses to generate sections from
        schedule (Schedule): schedule to calcuate cost with

    Returns:
        list[Section]: list of sections belonging to course_list, in order from lowest to highest cost
    """
    # all courses in this course list have the same priority, so the only thing that matters is the cost function
    sections: list[Section] = []
    costs: list[int] = []
    for course in course_list:
        for section in course.sections:
            sections.append(section)
            # calc cost of schedule with
            schedule.add(section)
            costs.append(-schedule.cost()) # do negative to sort from min to max
            schedule.remove(section)
    sorted_sections = [sec for _, sec in sorted(zip(costs, sections), key=lambda c_sec: c_sec[0])]
    return sorted_sections
            

def backtracking_search(curr_schedule: Schedule, course_list: list[Course], num_desired_courses: int) -> Optional[Schedule]:
    """standard CSP backtracking search, but with the addition that it does assignments according to a cost function.
    Recursive, so this is called to expand one branch of the tree.

    Args:
        curr_schedule (Schedule): current schedule
        course_list (list[Course]): list of courses to pick from, static
        num_desired_courses (int): number of courses desired by user, also static

    Returns:
        Optional[Schedule]: the schedule if it found a solution, None if it couldn't find anything valid
    """
    # if assignment is complete, return assignment
    if curr_schedule.num_sections == num_desired_courses: return Schedule
    next_courses = get_next_courses(curr_schedule, course_list)
    # no more classes to pick from, but not at desired number. User error, decide to interpret as success
    if next_courses is None: return Schedule 
    
    # this is where cost function gets applied
    sorted_sections = get_sorted_sections(next_courses, curr_schedule)
    
    for section in sorted_sections:
        curr_schedule.add(section)
        result: Optional[Schedule] = backtracking_search(curr_schedule, course_list, num_desired_courses)
        if result is not None: return result
        curr_schedule.remove(section)
    return None
    
    

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


=======
>>>>>>> origin/algo_attempt

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