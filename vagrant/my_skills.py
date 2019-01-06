# missing docstring - please help me out here - what should I do here?

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
APP = Flask(__name__)
APP.secret_key = "VerySecretKey"

# imports to connect script to database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import SkillTable, Base, CourseTable

# connect script to my_skills.db database
engine = create_engine('sqlite:///my_skills.db', connect_args={'check_same_thread': False})
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
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    course_lst = session.query(CourseTable).filter_by(skill_id=skill_item.id).all()
    return render_template('show_skill.html', skill=skill, skill_item=skill_item, course_lst=course_lst)


@APP.route('/<skill>/edit/', methods=['GET', 'POST'])
def edit_skill(skill):
    """routing to edit a specific skill"""
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    if request.method == 'POST':
        if request.form['name']:
            skill_item.name = request.form['name']
        session.add(skill_item)
        session.commit()
        return redirect(url_for('home_page'))
    return render_template('edit_skill.html', skill=skill, skill_item=skill_item)


@APP.route('/<skill>/delete/', methods=['GET', 'POST'])
def delete_skill(skill):
    """routing to delete a specific skill"""
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    course_lst = session.query(CourseTable).filter_by(skill_id=skill_item.id).all()
    if request.method == 'POST':
        for x in course_lst:
            session.delete(x)
        session.delete(skill_item)
        session.commit()
        return redirect(url_for('home_page'))
    return render_template('delete_skill.html', skill=skill, skill_item=skill_item)


@APP.route('/skill/new/', methods=['GET', 'POST'])
def new_skill():
    """routing to create a new category"""
    if request.method == 'POST':
        add_skill = SkillTable(name=request.form['name'])
        session.add(add_skill)
        session.commit()
        return redirect(url_for('home_page'))
    return render_template('new_skill.html')


@APP.route('/login/')
def login_page():
    """routing for the designated login page"""
    return render_template('login.html')


@APP.route('/<skill>/<int:course>')
def course_page(skill, course):
    """routing for a specific course in a skillset"""
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    course_item = session.query(CourseTable).filter_by(id=course).one()
    return render_template('course_page.html', skill=skill, skill_item=skill_item, course_item=course_item)


@APP.route('/<skill>/course/new/', methods=['GET', 'POST'])
def new_course(skill):
    """routing for a new course in skillset"""
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    if request.method == 'POST':
        add_course = CourseTable(name=request.form['name'], description=request.form['description'],\
                                 price=request.form['price'], creator=request.form['creator'],\
                                 skill_id=skill_item.id)
        session.add(add_course)
        session.commit()
        return redirect(url_for('show_skill', skill=skill))
    return render_template('new_course.html', skill=skill)


@APP.route('/<skill>/<int:course>/edit/', methods=['GET', 'POST'])
def edit_course(skill, course):
    """routing to edit a course in a skillset"""
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    course_item = session.query(CourseTable).filter_by(id=course).one()
    if request.method == 'POST':
        if request.form['name']:
            course_item.name = request.form['name']
        if request.form['description']:
            course_item.description = request.form['description']
        if request.form['price']:
            course_item.price = request.form['price']
        if request.form['creator']:
            course_item.creator = request.form['creator']
        session.add(course_item)
        session.commit()
        return redirect(url_for('show_skill', skill=skill))
    return render_template('edit_course.html', skill=skill, course=course, skill_item=skill_item, course_item=course_item)


@APP.route('/<skill>/<course>/delete/', methods=['GET', 'POST'])
def delete_course(skill, course):
    """routing to delete an item in a category"""
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    course_item = session.query(CourseTable).filter_by(id=course).one()
    if request.method == 'POST':
        session.delete(course_item)
        session.commit()
        return redirect(url_for('show_skill', skill=skill, course=course))
    return render_template('delete_course.html', skill=skill, course=course, skill_item=skill_item, course_item=course_item)

@APP.route('/apis/')
def apis():
    """routing to a page that lists our apis"""
    return render_template('apis.html')


@APP.route('/api/<skill>/JSON')
def course_api(skill):
    """API endpoint for the courses of a specific skill"""
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    items = session.query(CourseTable).filter_by(skill_id=skill_item.id).all()
    return jsonify(CourseItems=[i.serialize for i in items])










if __name__ == '__main__':
    APP.debug = True
    APP.run(host='0.0.0.0', port=5000)
