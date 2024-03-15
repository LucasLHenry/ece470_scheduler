#from classes import Course, Section, Schedule
#from classes import Schedule, Section, Course
from datetime import datetime, timedelta

def cost(Schedule) -> float:
    cost = check_overlap(Schedule)
    print(f"The total cost is {cost} hours.")
    return cost # easiest implementation is amount of overlapping time

# function to check for overlap between two time intervals
def calculate_overlap(interval1_start, interval1_end, interval2_start, interval2_end):
    latest_start = max(interval1_start, interval2_start)
    earliest_end = min(interval1_end, interval2_end)
    overlap = (earliest_end - latest_start).total_seconds() / 3600
    return max(0, overlap)

# function to convert time strings to datetime objects
def parse_time(time_str):
    return datetime.strptime(time_str, '%I:%M %p')
def check_overlap(schedule_list):

    # convert time strings in the schedule list to datetime objects
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