# missing docstring - please help me out here - what should I do here?

from flask import Flask, render_template, request, redirect, url_for, flash
APP = Flask(__name__)

# imports to connect script to database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import SkillTable, Base, CourseTable

# connect script to my_skills.db database
engine = create_engine('sqlite:///my_skills.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# set up the routing for each page

@APP.route('/')
@APP.route('/home/')
def home_page():
    """routing for home page"""
    skill_lst = session.query(SkillTable).all()
    return render_template('home.html', skill_lst=skill_lst)


@APP.route('/<skill>/')
def show_skill(skill):
    """routing for the page of a specific skill"""
    first_letter = skill[0]
    skill = first_letter.upper() + skill[1:]
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    course_lst = session.query(CourseTable).filter_by(skill_id=skill_item.id).all()
    return render_template('show_skill.html', skill=skill, skill_item=skill_item, course_lst=course_lst)


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


@APP.route('/<skill>/<int:course>')
def course_page(skill, course):
    """routing for a specific course in a skillset"""
    first_letter = skill[0]
    skill = first_letter.upper() + skill[1:]
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    course_item = session.query(CourseTable).filter_by(id=course).one()
    return render_template('course_page.html', skill_item=skill_item, course_item=course_item)


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
