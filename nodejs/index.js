const UVicCourseScraper = require('@vikelabs/uvic-course-scraper').UVicCourseScraper;
// get all courses from the Kuali course catalog

async function get_all() {
    return await UVicCourseScraper.getAllCourses();
}

const allCourses = get_all();
var courseTitle = allCourses[0].title;
// get course details for course with pid 'ByS23Pp7E' (in this case thats ACAN 225)
// var courseDetails = await UVicCourseScraper.getCourseDetails('ByS23Pp7E');
// var courseDescription = courseDetails[0].description;
// var courseLectureHours = courseDetails[0].hoursCatalogText.lecture;
// // get course sections for CSC 111 in spring 2021
// var courseSections = await UVicCourseScraper.getCourseSections('202101', 'CSC', '111');
// var courseSectionCode = courseSections[0].sectionCode;
// // get seats for course section with CRN 10953 in spring 2021 (in this case thats ECE 260 - A01)
// var sectionSeats = await UVicCourseScraper.getSectionSeats('202101', '10953');
// var sectionTotalSeats = sectionSeats.seats.capacity;
