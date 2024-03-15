# RUN THIS FILE TO RUN THE PROGRAM
import courses_parser as parser
import courses_scheduler as scheduler

def main():
    print("running the program!")
    print("all courses:")
    parser.list_all_courses(Print = True)
    courses_list = parser.prompt_for_courses()
    schedule = scheduler.build_schedule(courses_list)
    print("new schedule:")
    for i in schedule.sections:
        print(i)


if __name__ == "__main__":
    main()