# missing docstring - please help me out here - how do I do this?

from flask import Flask
APP = Flask(__name__)


# set up the routing for each page

@APP.route('/')
@APP.route('/home/')
def home_page():
    """routing for home page"""
    return "This is the home page"


@APP.route('/<skill>/')
def all_category(skill):
    """routing for the page of a specific skill"""
    return "This is the page to learn {}".format(skill)


@APP.route('/<skill>/edit/')
def edit_category(skill):
    """routing to edit a specific skill"""
    return "This is the editing page of the skill {}".format(skill)


@APP.route('/<skill>/delete/')
def delete_category(skill):
    """routing to delete a specific skill"""
    return "This is the deleting page of {}".format(skill)


@APP.route('/skill/new/')
def new_category():
    """routing to create a new category"""
    return "here you can add a new skill to learn"


@APP.route('/login/')
def login_page():
    """routing for the designated login page"""
    return "This is the login page"


@APP.route('/<skill>/<course>')
def item_page(skill, course):
    """routing for the courses in a skillset"""
    return "This is the description page of the {1} course to learn {0}".format(skill, course)


@APP.route('/<skill>/course/new/')
def new_item(skill):
    """routing for a new course in skillset"""
    return "Add a new course to learn {}".format(skill)


@APP.route('/<skill>/<course>/edit/')
def edit_item(skill, course):
    """routing to edit a course in a skillset"""
    return "This is the edit page of {1}s {0} course".format(skill, course)


@APP.route('/<skill>/<course>/delete/')
def delete_item(skill, course):
    """routing to delete an item in a category"""
    return "This is the delete page of {1}s {0} course".format(skill, course)










if __name__ == '__main__':
    APP.debug = True
    APP.run(host='0.0.0.0', port=5000)