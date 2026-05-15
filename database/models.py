from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    papers = relationship("Paper", back_populates="owner")

class Paper(Base):
    __tablename__ = "papers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    subtitle = Column(String, nullable=True)
    genre = Column(String)
    tone = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="papers")
    sections = relationship("Section", back_populates="paper", cascade="all, delete-orphan")

class Section(Base):
    __tablename__ = "sections"
    
    id = Column(Integer, primary_key=True, index=True)
    paper_id = Column(Integer, ForeignKey("papers.id"))
    section_number = Column(Integer)
    section_title = Column(String)
    content = Column(Text)
    summary = Column(Text)
    
    paper = relationship("Paper", back_populates="sections")
