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

# imports to add login functionality
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "my_skills App"


# set up the routing for each page

@APP.route('/')
def home_page():
    """routing for home page"""
    skill_lst = session.query(SkillTable).all()
    return render_template('home.html', skill_lst=skill_lst, login_session=login_session)


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
        if 'username' not in login_session:
            return redirect('/login/')
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
        if 'username' not in login_session:
            return redirect('/login/')
        for x in course_lst:
            session.delete(x)
        session.delete(skill_item)
        session.commit()
        return redirect(url_for('home_page'))
    return render_template('delete_skill.html', skill=skill, skill_item=skill_item)


@APP.route('/skill/new/', methods=['GET', 'POST'])
def new_skill():
    """routing to create a new category"""
    if 'username' not in login_session:
        return redirect('/login/')
    if request.method == 'POST':
        add_skill = SkillTable(name=request.form['name'])
        add_skill = SkillTable(user_email=login_session['email'])
        session.add(add_skill)
        session.commit()
        return redirect(url_for('home_page'))
    return render_template('new_skill.html')

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
    if 'username' not in login_session:
        return redirect('/login/')
    if request.method == 'POST':
        iterator = 1
        switch = True
        while switch:   # loop is used to always assign the lowest possible id to database entry
            try:        # there should not be unused id's in the database
                session.query(CourseTable).filter_by(id=iterator).one()
                iterator += 1
            except Exception:
                switch = False
        add_course = CourseTable(name=request.form['name'], description=request.form['description'],\
                                 price=request.form['price'], creator=request.form['creator'],\
                                 skill_id=skill_item.id, id=iterator, user_email=login_session['email'])
        session.add(add_course)
        session.commit()
        return redirect(url_for('show_skill', skill=skill))
    return render_template('new_course.html', skill=skill)


@APP.route('/<skill>/<int:course>/edit/', methods=['GET', 'POST'])
def edit_course(skill, course):
    """routing to edit a course in a skillset"""
    skill_item = session.query(SkillTable).filter_by(name=skill).one()
    course_item = session.query(CourseTable).filter_by(id=course).one()
    if 'username' not in login_session:
        return redirect('/login/')
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
    if 'username' not in login_session:
        return redirect('/login/')
    if request.method == 'POST':
        session.delete(course_item)
        session.commit()
        return redirect(url_for('show_skill', skill=skill, course=course))
    return render_template('delete_course.html', skill=skill, course=course, skill_item=skill_item, course_item=course_item)

@APP.route('/apis/')
def apis():
    """routing to a page that lists our apis"""
    return render_template('apis.html')

@APP.route('/apis/skills/JSON')
def skills_api():
    """API endpoint for all skills in database"""
    skill_lst = session.query(SkillTable).all()
    return jsonify(SkillItems=[i.serialize for i in skill_lst])


@APP.route('/apis/courses/JSON')
def courses_api():
    """API endpoint for all courses"""
    course_lst = session.query(CourseTable).all()
    return jsonify(CourseItems=[i.serialize for i in course_lst])





@APP.route('/login/')
def show_login():
    """routing for the designated login page"""
    # Create anti-forgery state token
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)\
        for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@APP.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1].decode())
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # check if user is already connected
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


@APP.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s'), access_token
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response



@APP.route('/del_database/', methods=['GET'])
def delete_database():
    """routing to delete a specific skill"""
    skill_lst = session.query(SkillTable).all()
    course_lst = session.query(CourseTable).all()
    for x in skill_lst:
        session.delete(x)
    session.commit()
    for x in course_lst:
        session.delete(x)
    session.commit()
    return redirect(url_for('home_page'))







if __name__ == '__main__':
    APP.debug = True
    APP.run(host='0.0.0.0', port=5000)
