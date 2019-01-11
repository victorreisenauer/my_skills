"""create (not yet populate) the database for the my_skills app"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class SkillTable(Base):
    __tablename__ = 'skill_table'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_email = Column(String(100), nullable=False)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name'         : self.name,
            'id'           : self.id,
        }

class CourseTable(Base):
    __tablename__ = 'course_table'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    creator = Column(String(250))
    skill_id = Column(Integer, ForeignKey('skill_table.id'))
    skill = relationship(SkillTable)
    user_email = Column(String(100), nullable=False)

    @property
    def serialize(self):
        """return data in serializeable format"""
        return {
            'name'         : self.name,
            'description'  : self.description,
            'id'           : self.id,
            'price'        : self.price,
            'creator'      : self.creator,
        }

engine = create_engine('sqlite:///my_skills.db')
Base.metadata.create_all(engine)