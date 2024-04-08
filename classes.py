from dataclasses import dataclass, field
from aux_functions import gen_time, get_time
from typing import Optional

@dataclass
class Section:
    """class containing information on a specific course section
    """
    section_name: str
    course_name: str
    start_time: int
    end_time: int
    days: str
    course_priority: Optional[int] = None
    
    @property
    def length(self) -> int:
        return self.end_time - self.start_time
    
    def does_overlap(self, s: 'Section') -> bool:  # forward reference to not freak out type checker
        """checks to see if two sections overlap (ie exist at the same day and time)

        Args:
            s (Section): section to check against

        Returns:
            bool: true if the sections overlap, false otherwise
        """
        all_days_diff = True
        for char1 in self.days:
            if -1 != s.days.find(char1): all_days_diff = False
        if not all_days_diff:
            if self.start_time <= s.start_time and self.end_time > s.start_time: return True
            if s.start_time <= self.start_time and s.end_time > self.start_time: return True
        return False
    
    def __str__(self):
        return f"{self.course_name} {self.section_name}: {gen_time(self.start_time)} to {gen_time(self.end_time)}"


@dataclass
class Course:
    """class containing information on a specific course. Includes list of sections
    """
    name: str
    sections: list[Section]
    priority: Optional[int] = None

    @property
    def num_sections(self) -> int:
        return len(self.sections)
    
    def set_priority(self, new_priority):
        self.priority = new_priority
        for section in self.sections:
            section.course_priority = new_priority

@dataclass
class Schedule:
    """class continaing information for a given schedule. Contains a list of sections,
    as well as methods to derive the cost of the schedule
    """
    sections: list[Section]

    def __init__(self):
        self.sections = []
    
    @property
    def num_sections(self) -> int:
        return len(self.sections)

    def add(self, sectn):
        self.sections.append(sectn)
    
    def remove(self, sectn):
        self.sections.remove(sectn)

    def course_in_schedule(self, course: Course) -> bool:
        """checks to see if a course already has a section in this schedule"""
        for section in self.sections:
            if section.course_name.upper() == course.name.upper():
                return True
        return False

    def section_is_valid(self, sectn: Section) -> bool:
        """checks to see if a section fits into this schedule without overlapping an existing section and without duplicate courses"""
        for scheduled_sectn in self.sections:
            if scheduled_sectn.does_overlap(sectn) or scheduled_sectn.course_name.upper() == sectn.course_name.upper():
                return False
        return True
    
    def cost(self, curr_section_to_be_added: Section, future_courses_to_be_added: list[Course]) -> float:
        """calculates the cost of adding a section to the current schedule. Can be given a list of courses to be added in the future to consider
        cost is calculated as priority (highest priority is zero cost, 2nd highest is 1 cost, etc) plus the normalized number of future sections 
        (sections that have yet to be added to the schedule) that this course will overlap with (0 means the course does not overlap with any 
        future sections, 1 means it will overlap with every future section)

        Args:
            curr_section_to_be_added (Section): the section that is being proposed to be added
            future_courses_to_be_added (list[Course]): the list of courses that are not currently in the schedule

        Returns:
            float: the cost of the schedule with the given section included in it
        """
        priority_cost = curr_section_to_be_added.course_priority - 1

        overlap_cost = 0
        future_courses_checked = 0
        for future_course in future_courses_to_be_added:
            for future_section in future_course.sections:
                if self.section_is_valid(future_section):
                    future_courses_checked += 1
                    if curr_section_to_be_added.does_overlap(future_section): overlap_cost += 1

        if future_courses_checked != 0: return priority_cost + overlap_cost/future_courses_checked
        return priority_cost
                    
                