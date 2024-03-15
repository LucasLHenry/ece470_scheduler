#from classes import Course, Section, Schedule
#from classes import Schedule, Section, Course
from datetime import datetime, timedelta

def cost(Schedule) -> float:

    cost = check_overlap(Schedule)
    print(f"The total cost is {cost} hours.")
    return cost # easiest implementation is amount of overlapping time


def calculate_overlap(interval1_start, interval1_end, interval2_start, interval2_end):
    """
    Calculates the overlap in hours between two time intervals.

    Args:
        interval1_start (datetime): start time of the first interval.
        interval1_end (datetime): end time of the first interval.
        interval2_start (datetime): start time of the second interval.
        interval2_end (datetime): end time of the second interval.

    Returns:
        float: Overlap in hours between the two intervals.
    """
    latest_start = max(interval1_start, interval2_start)
    earliest_end = min(interval1_end, interval2_end)
    overlap = (earliest_end - latest_start).total_seconds() / 3600
    return max(0, overlap)


def parse_time(time_str):
    """
    Parses a time string into a datetime object.

    Args:
        time_str (str): time string

    Returns:
        datetime: parsed datetime object.
    """
    return datetime.strptime(time_str, '%I:%M %p')

def check_overlap(schedule_list):
    """
    Calculates the total overlap in hours between schedules.

    Args:
        schedule_list (list[Schedule]): list of schedules representing schedules.
            should contain keys 'start_time', 'end_time', and 'days'.
            'start_time' and 'end_time' should be in the format '%I:%M %p'.
            'days' should be a string representing days of the week 'MTWRF'.

    Returns:
        float: total overlap in hours.
    """

    for schedule in schedule_list:
        schedule['start_time'] = parse_time(schedule['start_time'])
        schedule['end_time'] = parse_time(schedule['end_time'])

    overlap_hours = {}

    # check for overlaps
    for i in range(len(schedule_list)):
        for j in range(i + 1, len(schedule_list)):
            schedule1 = schedule_list[i]
            schedule2 = schedule_list[j]

            # check for overlap for each day of the week
            for day in schedule1['days']:
                if day in schedule2['days']:
                    overlap = calculate_overlap(schedule1['start_time'], schedule1['end_time'],
                                                schedule2['start_time'], schedule2['end_time'])
                    overlap_hours[day] = overlap_hours.get(day, 0) + overlap

    total_overlap = sum(overlap_hours.values())
    return total_overlap


def main():  # tests the functions
    # test case:
    Schedules = [
        {'start_time': '8:00 AM', 'end_time': '10:00 AM', 'days': 'MF'},
        {'start_time': '8:00 AM', 'end_time': '3:00 PM', 'days': 'MTF'},
        {'start_time': '7:00 AM', 'end_time': '4:00 PM', 'days': 'MWF'},
    ]
    cost(Schedules)

if __name__ == "__main__":
    main()