from dataclasses import dataclass, field
from aux_functions import gen_time, get_time
from typing import Optional

@dataclass
class Section:
    section_name: str
    course_name: str
    start_time: int
    end_time: int
    days: str
    course_priority: Optional[int] = None
    
    @property
    def length(self) -> int:
        return self.end_time - self.start_time
    
    def __str__(self):
        return f"{self.course_name} section {self.section_name}: {self.days} {gen_time(self.start_time)} to {gen_time(self.end_time)}"


@dataclass
class Course:
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

    def section_is_valid(self, sectn: Section) -> bool:
        """checks to see if a section fits into this schedule without overlapping an existing section and without duplicate courses"""
        for scheduled_sectn in self.sections:
            if self.does_overlap(scheduled_sectn, sectn) or scheduled_sectn.course_name.upper() == sectn.course_name.upper():
                return False
        return True
       
    def does_overlap(self, s1: Section, s2: Section) -> bool:
        """checks to see if two sections overlap (ie exist at the same day and time)"""
        all_days_diff = True
        for char1 in s1.days:
            if -1 != s2.days.find(char1): all_days_diff = False
        if not all_days_diff:
            if s1.start_time <= s2.start_time and s1.end_time > s2.start_time: return True
            if s2.start_time <= s1.start_time and s2.end_time > s1.start_time: return True
        return False
    
    def cost(self, future_courses_to_be_added, curr_section_to_be_added) -> float:
        """cost is calculated as priority (highest priority is zero cost, 2nd highest is 1 cost, etc) plus the normalized number of future sections (sections that have yet to be added to the schedule) that this course will overlap with (0 means the course does not overlap with any future sections, 1 means it will overlap with every future section)"""
        cost = curr_section_to_be_added.course_priority - 1
        return cost
    # def cost(self, future_courses_to_be_added, curr_section_to_be_added) -> int:
    #     # optimize for not too early, not too late
        
    #     # make the margins tight so that more schedules will have nonzero cost
    #     nice_start_time = get_time("11:00AM")
    #     nice_end_time = get_time("1:00PM")
        
    #     start_time_offsets: dict[str, int] = {"M": 0, "T": 0, "W": 0, "R": 0, "F": 0}
    #     end_time_offsets  : dict[str, int] = {"M": 0, "T": 0, "W": 0, "R": 0, "F": 0}
    #     for section in self.sections:
    #         start_diff = nice_start_time - section.start_time
    #         end_diff = section.end_time - nice_end_time
    #         for day in section.days:
    #             if start_diff > start_time_offsets[day]: start_time_offsets[day] = start_diff
    #             if end_diff > end_time_offsets[day]: end_time_offsets[day] = end_diff
    #     return sum(start_time_offsets.values()) + sum(end_time_offsets.values())
                    
                