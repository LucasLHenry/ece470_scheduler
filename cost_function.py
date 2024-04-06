from classes import Course, Section, Schedule


def total_cost(sch: Schedule) -> int:
    """total number of overlap in minutes of a schedule is calculated. Days are considered

    Args:
        sch (Schedule): schedule object

    Returns:
        int: total overlap in minutes
    """
    total_overlap_minutes = 0
    for i, course1 in enumerate(sch.sections):
        for course2 in sch.sections[i+1:]:
            section1 = course1
            section2 = course2
            common_days = set(section1.days).intersection(section2.days)

            for day in common_days:
                start1 = section1.start_time
                end1 = section1.end_time
                start2 = section2.start_time
                end2 = section2.end_time

                overlap_minutes = calculate_overlap(start1, end1, start2, end2)
                total_overlap_minutes += overlap_minutes

    return total_overlap_minutes  # easiest implementation is amount of overlapping time


def calculate_overlap(start1, end1, start2, end2):
    """calculates amount of overlap

    Args:
        start1 (int): start time for first section
        end1 (int): end time for first section
        start2 (int): start time for second section
        end2 (int): end time for second section


    Returns:
        int: amount of overlap
    """
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    overlap = max(0, earliest_end - latest_start)

    return overlap