# RUN THIS FILE TO RUN THE PROGRAM
import courses_parser as parser
import scheduler_algo as scheduler

def main():
    print("running the program!")
    courses_list = parser.get_all_courses()
    print("all courses: \n", courses_list)
    schedule = scheduler.test()
    print("new schedule:")
    for i in schedule.sections:
        print(i)


if __name__ == "__main__":
    main()