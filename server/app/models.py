# Standard Library imports

# Core Flask imports
from flask_login import UserMixin
from psycopg2 import Binary, Time

# Third-party imports
from sqlalchemy import (
    Integer,
    Column,
    Text,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

# App imports
from app import db_manager

# alias
Base = db_manager.base

class User(Base, UserMixin): # Inheriting from UserMixin for Flask-Login integration
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(Binary, nullable=False)

    tasks = relationship("Task", backref="user")
    calendar_events = relationship("CalendarEvent", backref="user")
    notes = relationship("Note", backref="user")


class TimeBlock(Base):
    __tablename__ = 'time_blocks'

    time_block_id = Column(String, primary_key=True)
    start_datetime = Column(DateTime, nullable=False)
    end_datetime = Column(DateTime, nullable=False)
    block_type = Column(String, nullable=False)

    tasks = relationship("Task", backref="time_block")
    calendar_events = relationship("CalendarEvent", backref="time_block")


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(String, primary_key=True)
    time_block_id = Column(String, ForeignKey('time_blocks.time_block_id'))
    title = Column(String, nullable=False)
    description = Column(Text)

    reminders = relationship("ReminderAssociation", backref="task")


class SchedulingMetadata(Base):
    __tablename__ = 'scheduling_metadata'

    metadata_id = Column(String, primary_key=True)
    parent_id = Column(String)
    start_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    importance_level = Column(String)
    deadline = Column(DateTime)


class CalendarEvent(Base):
    __tablename__ = 'calendar_events'

    calendar_event_id = Column(String, primary_key=True)
    time_block_id = Column(String, ForeignKey('time_blocks.time_block_id'))
    title = Column(String, nullable=False)
    description = Column(Text)

    reminders = relationship("ReminderAssociation", backref="calendar_event")


class Reminder(Base):
    __tablename__ = 'reminders'

    reminder_id = Column(String, primary_key=True)
    reminder_datetime = Column(DateTime, nullable=False)

    associations = relationship("ReminderAssociation", backref="reminder")


class ReminderAssociation(Base):
    __tablename__ = 'reminder_associations'

    association_id = Column(String, primary_key=True)
    reminder_id = Column(String, ForeignKey('reminders.reminder_id'))
    association_type = Column(String)
    object_id = Column(Integer)


class Note(Base):
    __tablename__ = 'notes'

    note_id = Column(String, primary_key=True)
    content = Column(Text)


class Routine(Base):
    __tablename__ = 'routines'

    routine_id = Column(String, primary_key=True)
    min_duration_minutes = Column(Integer, nullable=False)
    max_duration_minutes = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    optimal_time = Column(Time)

    scheduled_days = relationship("RoutineScheduledDay", backref="routine")
    timeframes = relationship("Timeframe", backref="routine")


class RoutineScheduledDay(Base):
    __tablename__ = 'routine_scheduled_days'

    scheduled_day_id = Column(Integer, primary_key=True)
    routine_id = Column(Integer, ForeignKey('routines.routine_id'))
    day_of_week = Column(String)


class Timeframe(Base):
    __tablename__ = 'timeframes'

    timeframe_id = Column(Integer, primary_key=True)
    routine_id = Column(Integer, ForeignKey('routines.routine_id'))
    start_time = Column(Time)
    end_time = Column(Time)
