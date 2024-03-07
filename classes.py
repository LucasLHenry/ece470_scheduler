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

@dataclass
class Schedule:
    sections: list[Section]
    
    @property
    def num_courses(self) -> int:
        return len(self.sections)