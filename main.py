# RUN THIS FILE TO RUN THE PROGRAM
import courses_parser as parser
import courses_scheduler as scheduler
import algo.cost_function as cost

def main():
    print("Welcome to the automated UVic course scheduler!")
    print("all courses:")
    parser.list_all_courses(Print = True)
    courses_list, desired_num_classes = parser.prompt_for_courses()
    schedule = scheduler.build_schedule(courses_list, desired_num_classes)
    print("new schedule:")
    print(f"number of possible schedules: {len(schedule)}")
    print(schedule)
    for i in schedule[0].sections:
        print(i)
    # overlap = cost.total_cost(schedule) #testing cost function
    # print(f"\nthe total overlap cost is: {overlap}")
    print("SCHEDULE")

    # scheduler.output(schedule)


if __name__ == "__main__":
    main()