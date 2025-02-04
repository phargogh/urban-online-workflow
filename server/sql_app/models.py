""" Create SQLAlchemy models from the 'Base' class."""
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

# SQLAlchemy uses 'model' to refer to these classes and instances that
# interact with the database.
# Pydantic uses term 'model' to refer to data validation, conversion, and
# documentation classes and instances


class Job(Base):
    """SQLAlchemy model to track jobs."""
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    status = Column(String)
    # each job has an associated session owner
    owner_id = Column(String, ForeignKey("sessions.session_id"))

    owner = relationship("Session", back_populates="jobs")
    #jobs = relationship("ParcelStats", back_populates="jobs_id")


class Session(Base):
    """SQLAlchemy model for sessions."""
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    last_active = Column(DateTime(timezone=True), server_default=func.now())

    # 'relationship' a "magic" attribute that will contain the values from
    # other tables related to this one.
    # When accessing the attribute 'items' in a User, as in 'my_user.items',
    # it will have a list of Item SQLAlchemy models (from the 'items' table)
    # that have a foreign key pointing to this record in the 'users' table.

    # When you access 'User.[jobs|scenarios|patterns]', SQLA will actually
    # go and fetch the jobs from the db in the corresponding table and
    # populate them here.
    scenarios = relationship("Scenario", back_populates="owner")
    patterns = relationship("Pattern", back_populates="owner")
    jobs = relationship("Job", back_populates="owner")


class Scenario(Base):
    """SQLAlchemy model for scenarios."""
    __tablename__ = "scenarios"

    scenario_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    wkt = Column(String)
    lulc_url_result = Column(String)
    lulc_stats = Column(String)
    lulc_url_base = Column(String, default="NLCD_2016.tif")
    # each scenario has an associated session owner
    owner_id = Column(String, ForeignKey("sessions.session_id"))

    #parcel_stats = relationship("ParcelStats", back_populates="owner")
    owner = relationship("Session", back_populates="scenarios")


class Pattern(Base):
    """SQLAlchemy model for storing creating patterns."""
    __tablename__ = "patterns"

    pattern_id = Column(Integer, primary_key=True, index=True)
    label = Column(String, index=True)
    wkt = Column(String)
    # each pattern has an associated session owner
    owner_id = Column(String, ForeignKey("sessions.session_id"))

    owner = relationship("Session", back_populates="patterns")


class ParcelStats(Base):
    """SQLAlchemy model for storing lulc stats under parcels."""
    __tablename__ = "parcel_stats"

    stats_id = Column(Integer, primary_key=True, index=True)
    target_parcel_wkt = Column(String)
    lulc_stats = Column(String)
    #TODO: I'm not sure if parcel stats not associated with a scenario
    # should be related to another table...
    job_id = Column(Integer, ForeignKey("jobs.job_id"))

    #owner = relationship("Job", back_populates="parcel_stats")
