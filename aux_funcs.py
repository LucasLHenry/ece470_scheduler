from classes import Schedule, Course, Section

def overlap(s1: Section, s2: Section) -> bool:
    if s1.days != s2.days: return False
    if s1.start_time <= s2.start_time and s1.end_time > s2.start_time: return True
    if s2.start_time <= s1.start_time and s2.end_time > s1.start_time: return True
    return False