from dataclasses import dataclass

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

@dataclass
class Schedule:
    
    sections: list[Section]

    @property
    def num_courses(self) -> int:
        return len(self.sections)
    
    def __init__(self):
        self.sections = []

    def add(self, sectn):
        self.sections.append(sectn)
    
    def remove(self, sectn):
        self.sections.remove(sectn)

    def section_is_valid(self, sectn) -> bool:
        """checks to see if a section fits into this schedule"""
        for scheduled_sectn in self.sections:
            if (sectn.days == scheduled_sectn.days) and ((sectn.start_time >= scheduled_sectn.start_time and sectn.start_time <= scheduled_sectn.end_time) or (sectn.end_time >= scheduled_sectn.start_time and sectn.end_time <= scheduled_sectn.end_time)):
                return False
        return True