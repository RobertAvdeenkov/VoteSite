from sqlalchemy import Column,String,Integer,ForeignKey,func,DateTime
from sqlalchemy.orm import DeclarativeBase,relationship

class Base(DeclarativeBase):pass

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    password=Column(String)
    answers=relationship('Answer', back_populates='user')

class Vote(Base):
    __tablename__='votes'
    id=Column(Integer,primary_key=True)
    title=Column(String)
    created_at=Column(DateTime, default=func.now())
    answers=relationship('Answer', back_populates='vote')
    typevar=relationship("TypeVar", back_populates='vote')

class Answer(Base):
    __tablename__='answers'
    id=Column(Integer,primary_key=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    vote_id=Column(Integer,ForeignKey('votes.id'))

    user=relationship('User', back_populates='answers')
    vote=relationship("Vote", back_populates='answers')

class TypeVar(Base):
    __tablename__='typevar'
    id=Column(Integer,primary_key=True)
    text=Column(String)
    count=Column(Integer, default=0)
    vote_id=Column(Integer,ForeignKey('votes.id'), nullable=False)
    vote=relationship("Vote", back_populates='typevar')