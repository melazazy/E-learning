# E-Learning PlatForm
this platform for online courses

#### Video Demo:  https://www.youtube.com/watch?v=cOvKIFwn0oI
Note Slow Video to 0.25 x


## Table of Contents
0. [Distinctiveness and Complexity](#Distinctiveness)
1. [General Info](#general-info)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Technologies](#technologies)
5. [Files](#files)

### Distinctiveness and Complexity
***
 ## This App More Complexity Because:
-  have more Than 25 HTML File
-  have 15 relations SQLite  Django models
-  have more than 1000 lines of code in the Views.py file
-  have 9 Forms in forms.py File
-  have more Than 650 lines of code in 8 Javascript Files

## This App Distinctiveness Because:
- Teacher can add more types of files to the lectures of his course
- Teacher can Fully Manage all Materials in his Course by Edit these materials or even Delete It
- Student Can Communicate With All other students in general as a classmate
- Teachers Also can Communicate With All Course students in general as in school class
- Communicate in General to keep privacy for all students

### General Info
***
 philosophy of this platform is based on permanent communication between students and the teacher
## Student:
after the end of each unit or lecture, there are assignments for each student to solve so that he can move to the next unit or lecture
The teacher corrects the assignment and allows the student to move on to the next unit or lecture

## teacher:
Should follow the structure of the course as shown in the picture. Each course must be divided into lectures and each lecture into lessons. Each lecture contains questions that must be answered to allow the student to follow the lessons. It also contains an assignment that must be resolved to move to the next lecture.
Also, each lesson contains questions that must be answered to move to the next lesson. At the end of the course, there is a graduation project that the student must solve to obtain a graduation certificate

![Elearning Website blockframe2](https://user-images.githubusercontent.com/75970269/171384910-4fd811a2-8109-4b54-8992-2fd060660771.png)


### Requirements
***
- Django
	- > pip3 install django
- Django Restframework
	-  > pip install djangorestframework
- charset normalizer 2.0.12
	- > pip install charset-normalizer

### Installation
***
- **mkdir django_projectr:**
    -  cd django_project:
	- > `django-admin startproject django_project `
	- > ` django-admin startapp app_1 `

### Technologies
***
### Front-end :-
_Using Bootstrap, Javascript, and Some of My own CSS_

### Backend :-
- Python 3.10.1 / Django 4.0.3
- SQLite 3
- Javascript



### Files & directories
***
- capstone
	-   __ pycache__
	-   __ init__.py
	- settings.py
	- urls.py

- elearning
	-   __ pycache__
	- static
		- elearning
			- css
				- styles.css
				- lecture.css
			- js
				- addassigne.js
				- addlecture.js
				- addlesson.js
				- enroll.js
				- index.js
				- lecture.js
	- templates
		- elearning
			- index.html
			- manage.html
			- profile.html
			- course.html
			- lecturehtml

	-   __ init__.py
- media



######
Structure
note: there are some prepared files in the static and templates folder to make a simple view.

# 1)Teacher:-
	- register
	- login
	- Edit Profile
	- Add Courses
	- Add Leactures
	- Add Lessons
	- Add Questions
	- Add Assignments
	- Add Final Project
	- Grade Assignments
	- Grade Final Project
	- upload certifecate for students

# 2)Student:-
	- register
	- login
	- Edit Profile
	- Search for Course
	- Filter Courses in Category
	- Enroll in Courses
	- Watch lectures and lessons
	- Answer Questions and Assignments
	- Comment in Lecture
	- replay to studenta questionn and comments
	- Add reviews And rate Course
	- Do Final Project
	- can download graduated Certifcation and share it

# 3)Teacher Course managment:-
	- edit Lecture Details
	- delete Lecture
	- edit Lesson Details
	- delete Lesson
	- edit Assignment Details
	- delete Assignment
	- edit Questions Details
	- delete Questions
	- Review Assignment And Grade it
	- Review Final Projects And Grade it
	- create Special Certifecate For Each Student And upload it to Site



## what I used in this Web Application :-
### Django framework for python
### SQLite 3
###  bootstrap library
### HTML ,CSS,  javascript,

### Waiting to do
	improve Models and querys
	use React js in Project
	cancle more of  JSON  and use Routes
	add more CSS
	Improving visual perception


## Credits
_Mustafa Elazazy_
