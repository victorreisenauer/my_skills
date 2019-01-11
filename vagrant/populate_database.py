"""populate the my_skills database created in database_setup.py"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import SkillTable, Base, CourseTable

engine = create_engine('sqlite:///my_skills.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Courses for Learning Python
skill1 = SkillTable(name="Python", user_email="victorreisenauer99@gmail.com")

session.add(skill1)
session.commit()


course1 = CourseTable(name="The Python Mega Course", description="This is a great course!", \
					  price="29.99", creator="Udemy", skill=skill1,                         \
					  user_email="victorreisenauer99@gmail.com")

session.add(course1)
session.commit()


course2 = CourseTable(name="Learn Python 3", description="This is an amazing course!",  \
	                  price="0.00",														\
					  creator="Codecademy", skill=skill1, user_email="victorreisenauer99@gmail.com")

session.add(course2)
session.commit()

course3 = CourseTable(name="Introduction to Programming with Python",  \
					  description="This is a perfect course!",         \
					  price="0.00", creator="Microsoft", skill=skill1, \
					  user_email="victorreisenauer99@gmail.com")

session.add(course3)
session.commit()


# Courses for Learning Artificial Intelligence
skill2 = SkillTable(name="Artificial Intelligence", user_email="victorreisenauer99@gmail.com")

session.add(skill2)
session.commit()


course1 = CourseTable(name="Machine Learning", description="This is a well structured course!", \
					  price="0.00", creator="Coursera", skill=skill2, \
					  user_email="victorreisenauer99@gmail.com")

session.add(course1)
session.commit()


course2 = CourseTable(name="Intro to AI", description="This is an amazing course!", price="0.00", \
					  creator="Microsoft", skill=skill2, user_email="victorreisenauer99@gmail.com")

session.add(course2)
session.commit()

course3 = CourseTable(name="AI with Python", description="This is a wonderful course!", \
					  price="599.00", creator="Udacity", skill=skill2, 					\
					  user_email="victorreisenauer99@gmail.com")

session.add(course3)
session.commit()


# Courses for Learning C++
skill3 = SkillTable(name="C++", user_email="victorreisenauer99@gmail.com")

session.add(skill3)
session.commit()


course1 = CourseTable(name="Intro to C++", description="This is a google course!", price="0.00", \
					  creator="Google", skill=skill3, user_email="victorreisenauer99@gmail.com")

session.add(course1)
session.commit()


course2 = CourseTable(name="Introduction to Programming in C", 									\
					  description="This is an great course!", price="0.00", creator="Coursera", \
					  skill=skill3, user_email="victorreisenauer99@gmail.com")

session.add(course2)
session.commit()

course3 = CourseTable(name="C++ Tutorial for Complete Beginners", \
					  description="This is a really good course!", price="0.00", creator="Udemy",\
					  skill=skill3, user_email="victorreisenauer99@gmail.com")

session.add(course3)
session.commit()

print("added all skills!")
