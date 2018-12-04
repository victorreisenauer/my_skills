# missing docstring - please help me out here - what should I do here?

from flask import Flask, render_template
APP = Flask(__name__)


# -------------------FAKE DATABASE------------------------------
# fake skills
skill_data = {'name': 'Artificial Intelligence', 'id': '1'}
skills_data = [{'name': 'Artificial Intelligence', 'id': '1'}, {'name':'C++', 'id':'2'},{'name':'Electronics', 'id':'3'}]


# fake courses
course_data =  {'name':'AI in Python','description':'This is a great course','creator':'Udacity', 'id':'1'}
courses_data = [{'name':'AI in Python','description':'This is a great course','creator':'Udacity', 'id':'1'}, 
{'name':'Intro to Selfdriving Cars', 'description':'This is an amazing course', 'creator':'Udacity', 'id':'2'}, 
{'name':'Intro to Electronics','description':'this is a fun course', 'creator':'Coursera', 'id':'3'}]


# set up the routing for each page

@APP.route('/')
@APP.route('/home/')
def home_page():
    """routing for home page"""
    return render_template('home.html', skills_data=skills_data)


@APP.route('/<skill>/')
def show_skill(skill):
    """routing for the page of a specific skill"""
    return render_template('show_skill.html', skill=skill, course_data=course_data)


@APP.route('/<skill>/edit/')
def edit_skill(skill):
    """routing to edit a specific skill"""
    return render_template('edit_skill.html', skill=skill)


@APP.route('/<skill>/delete/')
def delete_skill(skill):
    """routing to delete a specific skill"""
    return render_template('delete_skill.html', skill=skill)


@APP.route('/skill/new/')
def new_skill():
    """routing to create a new category"""
    return render_template('new_skill.html')


@APP.route('/login/')
def login_page():
    """routing for the designated login page"""
    return render_template('login.html')


@APP.route('/<skill>/<course>')
def course_page(skill, course):
    """routing for a specific course in a skillset"""
    return render_template('course_page.html', skill=skill, course=course, courses_data=courses_data)


@APP.route('/<skill>/course/new/')
def new_course(skill):
    """routing for a new course in skillset"""
    return render_template('new_course.html', skill=skill, courses_data=courses_data)


@APP.route('/<skill>/<course>/edit/')
def edit_course(skill, course):
    """routing to edit a course in a skillset"""
    return render_template('edit_course.html', skill=skill, course=course, courses_data=courses_data)


@APP.route('/<skill>/<course>/delete/')
def delete_course(skill, course):
    """routing to delete an item in a category"""
    return render_template('delete_course.html', skill=skill, course=course, courses_data=courses_data)

@APP.route('/apis/')
def apis():
    """routing to a page that lists our apis"""
    return render_template('apis.html')










if __name__ == '__main__':
    APP.debug = True
    APP.run(host='0.0.0.0', port=5000)
