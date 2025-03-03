from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base  # Make sure to define a Base for your ORM

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    full_name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)


class ReferenceRange(Base):
    __tablename__ = 'reference_ranges'

    id = Column(Integer, primary_key=True)
    test_name = Column(String(255), nullable=False)
    min_value = Column(Float)
    max_value = Column(Float)
    units = Column(String(50))
    department_id = Column(Integer, ForeignKey('departments.id'), nullable=False)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=True)
    study_id = Column(Integer, ForeignKey('studies.id'), nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    department = relationship('Department')
    source = relationship('Source', back_populates='reference_ranges')
    study = relationship('Study', back_populates='reference_ranges')
    user = relationship('User')


class Source(Base):
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255))
    source_type = Column(String(100), nullable=False)

    reference_ranges = relationship('ReferenceRange', back_populates='source')


class Study(Base):
    __tablename__ = 'studies'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    authors = Column(String(500))
    publication_date = Column(DateTime)  # Use DateTime here instead of Date

    reference_ranges = relationship('ReferenceRange', back_populates='study')
