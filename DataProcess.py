# -*- coding: utf-8 -*-
#Import Area
import csv
from datetime import datetime
import os

#Settings
firstGradeColumn = 9#3
studentEmailColumn = 1
userNameColumn = 2

testInputInform  = "Nhap id bai kiem tra: "
gradeFileNameFormat  = "Grade.csv"
resultFileNameFormat = "Result.csv"
staffName = ['cxnamis', 'nguyenhaitrieu100', 'vchitai']
notFilterValue = ['Not Attempted']
nullString = 'None'
maxTime = input("Nhap vao thoi gian toi da lam bai theo format (h:mm:ss): ")
reportNameCSV = 'FinalReport.csv'
reportNameHTML = 'FinalReport.html'
reportTemplateName = 'ReportTemplate.html'
timeFormat = '%Y-%m-%d %H:%M:%S+00:00'

userNameColumnResultFile = 0
endTimeResultFile = 6
startTimeResultFile = 5

resUserNameColumn = 1
resGradeColumn = 2
resTimeColumn = 3

top = 5

templateDelimiter = ['{{/Template}}','{{STT}}', '{{Username}}', '{{Result}}', '{{Time}}', '{{Content}}']

#Functions
def getTime(row):
    return datetime.strptime(row[:19] + row[26:], timeFormat)
     

#Input
testId = input(testInputInform)
testColumn = firstGradeColumn + testId
gradeFileName = gradeFileNameFormat;
resultFileName = resultFileNameFormat;
students = []

#Grade File Process
with open(gradeFileName,'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    iterStudent = iter(reader)
    next(iterStudent)
    for row in iterStudent:
        if (row[userNameColumn] in staffName):
            continue
        if not (row[testColumn] in notFilterValue ):
            students.append([row[studentEmailColumn], row[userNameColumn], row[testColumn]])

#Result File Process
with open(resultFileName,'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    iterStudent = iter(reader)
    next(iterStudent)
    for row in iterStudent:
        for student in students:
            if (row[userNameColumnResultFile] == student[0]):
                if not row[endTimeResultFile] == nullString:
                    student.append(str(getTime(row[endTimeResultFile])-getTime(row[startTimeResultFile])))
                else:
                    student.append(maxTime)
                break
for x in students:
    print x
#Sort
students_sorted_by_time = sorted(students, key=lambda tup: tup[resTimeColumn])
students_sorted_by_grade = sorted(students_sorted_by_time, key=lambda tup: tup[resGradeColumn], reverse=True)

with open(reportNameCSV, 'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for student in students_sorted_by_grade:
        writer.writerow([student[resUserNameColumn], int(float(student[resGradeColumn])*100), student[resTimeColumn]])

with open(reportTemplateName, 'r') as templateFile:
    with open(reportNameHTML, 'w') as htmlFile:
        template = templateFile.read().split(templateDelimiter[0])
        content = ''
        index = 0
        for student in students_sorted_by_grade:
            index += 1
            style = 0
            if top > 0:
                style=1
                top-=1
            else:
                style=2
            studentRow = template[style].replace(templateDelimiter[1],str(index))
            studentRow = studentRow.replace(templateDelimiter[2],student[resUserNameColumn])
            studentRow = studentRow.replace(templateDelimiter[3],str(int(float(student[resGradeColumn])*100)))
            studentRow = studentRow.replace(templateDelimiter[4],student[resTimeColumn])
            content += studentRow
        htmlFile.write(template[0].replace(templateDelimiter[5], content))


import webbrowser
webbrowser.open(reportNameHTML,new=2)
