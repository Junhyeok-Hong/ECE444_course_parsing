# Script & Resources to parse undergraduate courses in the University of Toronto

@ Junhyeok Hong\
Data last updated 10/15/2022

## Data can be found in data directory

### Sources are from:

https://calendar.utoronto.ca/
https://artsci.calendar.utoronto.ca/print/view/pdf/course_search/print_page/debug
https://engineering.calendar.utoronto.ca/print/view/pdf/search_courses/print_page/debug
https://daniels.calendar.utoronto.ca/print/view/pdf/search_courses/print_page/debug
https://kpe.calendar.utoronto.ca/print/view/pdf/search_courses/print_page/debug
https://music.calendar.utoronto.ca/print/view/pdf/search_courses/print_page/debug
https://pharmacy.calendar.utoronto.ca/print/view/pdf/search_courses/print_page/debug

## Source Code can found in src directory

Note that some of the sources have minor syntatical differences; thus, require small modifications to the parsing script

## To Run

Simply navigate to the src directory and run the parsing script\
Reads html file and generates an output csv file in the output directory\

Generated output csv has columns:\
{Course Code, Course Name, Credit Value, Details, Prerequisites, Corequisite, Exclusion, Recommended Preparation}

## NOTES:

In Prerequisites, Corequisite, Exclusion, Recommended Preparation, there may be 'or equivalent' or 'Complicated'.\
'or equivalent' is intuitive\
'Complicated' is just a simplification of more specific information such as: 'Contact the instructor'
# ECE444_course_parsing
