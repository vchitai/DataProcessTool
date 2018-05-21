# -*- coding: utf-8 -*-
import json
import re
import os
clear = lambda: os.system('cls')

usrname = input("Nhap username: ")
password = input("Nhap password: ")
rootUrl = 'http://khanviet.org/courses/course-v1:HCMUS+Python_Beginner+2018_T3/discussion/forum/'
dataFile = 'data.txt'
reportTemplateName = 'forumReportTemplate.txt'
finalReportName = "finalForumReport.html"

clear()
print ("Dia chi forum: " + rootUrl)
print ("File luu data: " + dataFile)
command = "phantomjs forumCrawler.js " + usrname + " " + password + " " + rootUrl + " " + dataFile
os.system(command)

inputFile = open(dataFile, "r")
outputFile = open(finalReportName, "w")

inputFileContent = inputFile.read()
rawData = json.loads(inputFileContent)
data = []
for x in rawData:
    data.append(x.values())
for x in data:
    if ('hour' in x[1]):
        x[1] = '1 day ago'
    if (x[1] == 'a day ago'):
        x[1] = '1 day ago'
    if (x[1] == 'about a month ago'):
        x[1] = '30 day ago'
    x[1] = re.search(r'\d+', x[1]).group()
        

res = []
res2 = []

for x in data:
    if (x[0] not in res):
        res.append(x[0])
        if (int(x[1]) <= 7):
            res2.append(1)
        else:
            res2.append(0)
    else:
        if (int(x[1]) < 7):
            res2[res.index(x[0])]+=1

with open(reportTemplateName, 'r') as templateFile:
    template = templateFile.read().split('{{/Template}}')
    content = ""
    for i in xrange(0, len(res)):
        if (res2[i]>0):
            c = template[1].replace("{{Username}}", res[i])
            c = c.replace("{{Comments}}", str(res2[i]))
            content += c
    outputFile.write(template[0].replace("{{Content}}", content))
outputFile.close()

import webbrowser
webbrowser.open(finalReportName,new=2)
