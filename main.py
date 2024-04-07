# RUN THIS FILE TO RUN THE PROGRAM
import courses_parser as parser
import courses_scheduler as scheduler

def main():
    print("Welcome to the automated UVic course scheduler!")
    print("All courses:")
    parser.list_all_courses(Print = True)
    courses_list, desired_num_classes = parser.prompt_for_courses()
    schedule = scheduler.build_schedule(courses_list, desired_num_classes)
    if schedule == False:
        print("failed to find valid schedule")
    else:
        print("\n~~~~~~~~~~~~~~~~~~Output~~~~~~~~~~~~~~~~~~")
        print("\n   New schedule includes:")
        for sectn in schedule.sections:
            print(f"{sectn} {sectn.days }")
        print("\n   Weekly calendar:")
        parser.output_schedule(schedule)

if __name__ == "__main__":
    main()