'''
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import urllib.request as req
'''

import pandas

import bs4
import json

import random

def makecontexthtml(url):
    request = req.Request(url, headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"})
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    context = bs4.BeautifulSoup(data,"html.parser")
    return context

def makecontextjson(url):
    request = req.Request(url, headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"})
    with req.urlopen(request) as response:
        data =  response.read().decode("utf-8")
    context = json.loads(data)
    return context

def combine(a,b):
    course = []
    for i in range (100):
        if (i == len(a)):
            break
        course.append(a[i])
        if (i == len(b)):
            break
        course.append(b[i])
    return course

def makelist(context):
    course1 = context.find_all('tr',class_="row-a")
    course2 = context.find_all('tr',class_="row-b")
    courses = combine(course1,course2)
    for i in range (len(courses)):
        courses[i] = courses[i].find_all('td')
        for j in range (len(courses[i])):
            #print(courses[i][j])
            courses[i][j] = courses[i][j].string
            if (courses[i][j] != None):
                courses[i][j] = courses[i][j].replace('\u3000','').replace(' ','')
    return courses

def qualified2(course):
    if (course.loc['decided'].find('*') != -1):
        return True
    temp = random.randint(1,int(course.loc['people']))
    if (temp <= int(course.loc['max']) - int(course.loc['already'])):
        return True
    return False

def repeated2(course,final):
    return False

def qualified(course):
    if (course[0].find('*') != -1):
        return True
    temp = random.randint(1,int(course[10]))
    if (temp <= int(course[8]) - int(course[9])):
        return True
    return False

def repeated(course,success):
    chinese = []
    number = []
    for word in ['一','二','三','四','五']:
        if (course[7].find(word) != -1):
            chinese.append(word)
    for word in ['0','1','2','3','4','5','6','7','8','9']:
        if (course[7].find(word) != -1):
            number.append(word)
    for i in range (len(success)):
        if (course[2] == success[i][2]):
            return True
        for word1 in chinese:
            for word2 in number:
                if (success[i][7].find(word1) != -1) and (success[i][7].find(word2) != -1):
                    return True
    return False
    
if __name__ == '__main__':
    myfile = open('lesson.txt')
    data = myfile.read()
    context = bs4.BeautifulSoup(data,"html.parser")
    courses = makelist(context)
    success = []
    success2 = []
    for i in range (len(courses)):
        if (qualified(courses[i]) == True):
            if(repeated(courses[i],success) == False):
                courses[i].append('選上')
                success.append(courses[i])
            else:
                courses[i].append('選上，但已錄取更高志願課程')
                success2.append(courses[i])
        else:
            courses[i].append('未選上')
    credit = 0
    print("以下是你選上的課：")
    for i in range (len(success)):
        print(success[i])
        credit += int(success[i][6])
    print('學分數：',credit)

    '''
    print("以下是你選上，但錄取更高志願的課：")
    for i in range (len(success2)):
        print(success2[i])
    '''


    '''
    attribute = ['decided','num','name','teacher','id','class','credit',
                 'time','max','already','people','ap','order']
    newcourses = pandas.DataFrame({},index = attribute)
    for i in range (len(courses)):
        newcourses[i] = courses[i]
    #print(newcourses)
    #print(newcourses[0])
    #print(newcourses.iloc[2])
    #print(newcourses.loc['name'])

    success = pandas.DataFrame({}, index = attribute)
    for i in range (newcourses.shape[1]):
        if (qualified2(newcourses[i]) == True) and (repeated2(newcourses[i],success) == False):
            success[i] = newcourses[i]
    print(success)
    '''
