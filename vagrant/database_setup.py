import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class SkillTable(Base):
    __tablename__ = 'skill_table'
   
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
 
class CourseTable(Base):
    __tablename__ = 'course_table'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    creator = Column(String(250))
    skill_id = Column(Integer,ForeignKey('skill_table.id'))
    skill = relationship(SkillTable) 
 

engine = create_engine('sqlite:///my_skills.db')
Base.metadata.create_all(engine)