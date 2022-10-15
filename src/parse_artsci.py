################################################################################
##### Script to parse artsci courses in the University of Toronto          #####
##### @ Junhyeok Hong                                                      #####
##### Data last updated 10/15/2022                                         #####
################################################################################
##### Course data retrived are as following:                               #####
##### - Course Code                                                        #####
##### - Course Name                                                        #####
##### - Credit Value                                                       #####
##### - Details                                                            #####
##### - Prerequisite                                                       #####
##### - Corequisite                                                        #####
##### - Exclusion                                                          #####
##### - Recommended Preparation                                            #####
################################################################################
##### Generated CSV has columns:                                           #####
##### {Course Code, Course Name, Credit Value, Details,                    #####
#####   Prerequisites, Corequisite, Exclusion, Recommended Preparation}    #####
################################################################################

import re
import csv
import sys

header = ['Course Code', 'Course Name', 'Credit Value', 'Details',
          'Prerequisites', 'Corequisites', 'Exclusion', 'Recommended Preparation']

f = open('../data/artsci.html', 'r')
lines = f.readlines()

with open('../output/artsci.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for index, line in enumerate(lines):

        course_data = []

        if '<div class="no-break views-row"><div class="views-field views-field-title"><span class="field-content"><br /><h3>' in line:

            # Parse 1 - Course Code
            parse_line1 = line.split(
                '<div class="no-break views-row"><div class="views-field views-field-title"><span class="field-content"><br /><h3>')[1]
            course_code = parse_line1[:8]
            course_data.append(course_code)
            # print(course_code)

            # Parse 2 - Course Name
            parse_line2 = parse_line1.split(course_code + ' - ')[1]
            course_name = parse_line2.split('</h3>')[0]
            if ('&amp;' in course_name):
                course_name = course_name.replace('&amp;', "&")
            course_data.append(course_name)
            # print(course_name)

            course_data.append('')

            i = index+1

            details = ''
            prerequisites = []
            corequisites = []
            exclusions = []
            recommended_preparations = []

            while ('<div class="no-break views-row"><div class="views-field views-field-title"><span class="field-content"><br /><h3>' not in lines[i]):
                if 'class="views-field views-field-body"' in lines[i]:
                    parse_line = lines[i].split(
                        '<div class="views-field views-field-body"><div class="field-content">')[1]
                    details = parse_line.split('</div></div>')[0]
                    details = re.sub(r'<.+?>', '', details)
                    if ('&amp;' in details):
                        details = details.replace('&amp;', "&")

               # Parse 5 Prerequisite (May not exist)
                if 'class="views-label views-label-field-prerequisite"' in lines[i]:
                    parse_line5 = lines[i].split(
                        'class="views-label views-label-field-prerequisite"')[1]

                    if 'class="views-field views-field-field-corequisite"' in parse_line5:
                        parse_line5_1 = parse_line5.split(
                            'class="views-field views-field-field-corequisite"')[0]
                    elif 'class="views-label views-label-field-exclusion"' in parse_line5:
                        parse_line5_1 = parse_line5.split(
                            'class="views-label views-label-field-exclusion"')[0]
                    elif 'class="views-field views-field-field-recommended-preparation"' in parse_line5:
                        parse_line5_1 = parse_line5.split(
                            'class="views-field views-field-field-recommended-preparation"')[0]
                    elif 'class="views-label views-label-field-total-au-value"' in parse_line5:
                        parse_line5_1 = parse_line5.split(
                            'class="views-label views-label-field-total-au-value"')[0]
                    elif 'class="views-field views-field-field-program-tags"' in parse_line5:
                        parse_line5_1 = parse_line5.split(
                            'class="views-field views-field-field-program-tags"')[0]
                    else:
                        parse_line5_1 = parse_line5.split(
                            '</a></div></li></ul></div></div></div></div>')[0]

                    parse_line5_2 = parse_line5_1.split('</a></span>')[0]
                    prerequisites = parse_line5_2.split('</a>')
                    for index, prerequisite in enumerate(prerequisites):
                        prerequisites[index] = prerequisite[-8:]
                        if ('<' in prerequisites[index]) or ('\n' in prerequisites[index]):
                            prerequisites[index] = 'Complicated'
                    if ('equivalent' in parse_line5_1):
                        prerequisites[-1] = 'or equivalent'

                # Parse 6 Corequisite (May not exist)
                if 'class="views-label views-label-field-corequisite"' in lines[i]:
                    parse_line6 = lines[i].split(
                        'class="views-label views-label-field-corequisite"')[1]

                    if 'class="views-label views-label-field-exclusion"' in parse_line6:
                        parse_line6_1 = parse_line6.split(
                            'class="views-label views-label-field-exclusion"')[0]
                    elif 'class="views-field views-field-field-recommended-preparation"' in parse_line6:
                        parse_line6_1 = parse_line6.split(
                            'class="views-field views-field-field-recommended-preparation"')[0]
                    elif 'class="views-label views-label-field-total-au-value"' in parse_line6:
                        parse_line6_1 = parse_line6.split(
                            'class="views-label views-label-field-total-au-value"')[0]
                    elif 'class="views-field views-field-field-program-tags"' in parse_line6:
                        parse_line6_1 = parse_line6.split(
                            'class="views-field views-field-field-program-tags"')[0]
                    else:
                        parse_line6_1 = parse_line6.split(
                            '</a></div></li></ul></div></div></div></div>')[0]

                    parse_line6_2 = parse_line6_1.split('</a></span>')[0]
                    corequisites = parse_line6_2.split('</a>')
                    for index, corequisite in enumerate(corequisites):
                        corequisites[index] = corequisite[-8:]
                        if ('<' in corequisites[index]):
                            corequisites[index] = 'Complicated'
                    if ('equivalent' in parse_line6_1):
                        corequisites[-1] = 'or equivalent'

                # Parse 7 Exclusion (May not exist)
                if 'class="views-label views-label-field-exclusion"' in lines[i]:
                    parse_line7 = lines[i].split(
                        'class="views-label views-label-field-exclusion"')[1]

                    if 'class="views-field views-field-field-recommended-preparation"' in parse_line7:
                        parse_line7_1 = parse_line7.split(
                            'class="views-field views-field-field-recommended-preparation"')[0]
                    elif 'class="views-label views-label-field-total-au-value"' in parse_line7:
                        parse_line7_1 = parse_line7.split(
                            'class="views-label views-label-field-total-au-value"')[0]
                    elif 'class="views-field views-field-field-program-tags"' in parse_line7:
                        parse_line7_1 = parse_line7.split(
                            'class="views-field views-field-field-program-tags"')[0]
                    else:
                        parse_line7_1 = parse_line7.split(
                            '</a></div></li></ul></div></div></div></div>')[0]

                    parse_line7_2 = parse_line7_1.split('</a></span>')[0]
                    exclusions = parse_line7_2.split('</a>')
                    for index, exclusion in enumerate(exclusions):
                        exclusions[index] = exclusion[-8:]
                        if ('<' in exclusions[index]):
                            exclusions[index] = 'Complicated'
                    if ('equivalent' in parse_line7_1):
                        exclusions[-1] = 'or equivalent'

                # Parse 8 Recommended Preparation (May not exist)
                if 'class="views-label views-label-field-recommended-preparation"' in lines[i]:
                    parse_line8 = lines[i].split(
                        'class="views-label views-label-field-recommended-preparation"')[1]

                    if 'class="views-label views-label-field-total-au-value"' in parse_line5:
                        parse_line8_1 = parse_line8.split(
                            'class="views-label views-label-field-total-au-value"')[0]
                    elif 'class="views-field views-field-field-program-tags"' in parse_line5:
                        parse_line8_1 = parse_line8.split(
                            'class="views-field views-field-field-program-tags"')[0]
                    else:
                        parse_line8_1 = parse_line8.split(
                            '</a></div></li></ul></div></div></div></div>')[0]

                    parse_line8_2 = parse_line8_1.split('</a></span>')[0]
                    recommended_preparations = parse_line8_2.split('</a>')
                    for index, recommended_preparation in enumerate(recommended_preparations):
                        recommended_preparations[index] = recommended_preparation[-8:]
                        if ('<' in recommended_preparations[index]):
                            recommended_preparations[index] = 'Complicated'
                    if ('equivalent' in parse_line8_1):
                        recommended_preparations[-1] = 'or equivalent'

                i += 1
                if (i >= len(lines)):
                    course_data.append('We will read and write a variety of texts focused on effecting social change. Students will be encouraged to engage with different theories of social change and an array of writing genres, ranging from journalism to critical theory to fiction. Ultimately, students will focus on one or several key social issues that they wish to write about for their final project.')
                    course_data.append(['Complicated'])
                    course_data.append([])
                    course_data.append(['INI414H1'])
                    course_data.append([])
                    writer.writerow(course_data)
                    sys.exit()

            course_data.append(details)
            course_data.append(prerequisites)
            course_data.append(corequisites)
            course_data.append(exclusions)
            course_data.append(recommended_preparations)
            writer.writerow(course_data)
