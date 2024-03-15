from dataclasses import dataclass
from aux_funcs import overlap

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


@dataclass
class Course:
    name: str
    sections: list[Section]

    @property
    def num_sections(self) -> int:
        return len(self.sections)


class Schedule:
    def __init__(self):
        self.sections = []
        
    @property
    def num_courses(self) -> int:
        return len(self.sections)

    def add(self, sectn):
        self.sections.append(sectn)
    
    def remove(self, sectn):
        self.sections.remove(sectn)

    def section_is_valid(self, sectn) -> bool:
        """checks to see if a section fits into this schedule"""
        for scheduled_sectn in self.sections:
            if overlap(scheduled_sectn, sectn):
                return False
        return True