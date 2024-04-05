from dataclasses import dataclass, field
from aux_functions import gen_time
from typing import Optional

@dataclass
class Section:
    section_name: str
    course_name: str
    start_time: int
    end_time: int
    days: str
    
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
        """checks to see if a section fits into this schedule without duplicate courses"""
        for scheduled_sectn in self.sections:
            if self.overlap(scheduled_sectn, sectn) or scheduled_sectn.course_name == sectn.course_name:
                return False
        return True
       
    def overlap(self, s1: Section, s2: Section) -> bool:
        all_days_diff = True
        for char1 in s1.days:
            if -1 != s2.days.find(char1): all_days_diff = False
        if not all_days_diff:
            if s1.start_time <= s2.start_time and s1.end_time > s2.start_time: return True
            if s2.start_time <= s1.start_time and s2.end_time > s1.start_time: return True
        return False