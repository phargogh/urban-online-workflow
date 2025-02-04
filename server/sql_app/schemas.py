"""Pydantic models which define more or less a "schema" (valid data shape)."""
#TODO: I suspect there are ways to condense the number of pydantic models.
# There are so many listed as a convenience for working with FastAPI and SQLA.
from datetime import datetime
from typing import Optional, Union, Literal

from pydantic import BaseModel


# Pydantic models declare the types using ":", the new type annotation
# syntax/type hints

class ScenarioBase(BaseModel):
    """Pydantic model base for Scenarios."""
    name: str
    description: Optional[str] = None


class ScenarioUpdate(BaseModel):
    """Pydantic model for updating Scenarios in the DB."""
    lulc_url_result: str
    lulc_stats: str


class Scenario(ScenarioBase):
    """Pydantic model used when reading data, when returning it from API."""
    scenario_id: int
    owner_id: str
    wkt: Union[str, None] = None
    lulc_url_result: Union[str, None] = None
    lulc_url_base: str
    lulc_stats: Union[str, None] = None


    class Config:
        orm_mode = True


class ScenarioResponse(BaseModel):
    """Pydantic model for the response after scenario creation."""
    scenario_id: int

    class Config:
        orm_mode = True


class Session(BaseModel):
    """Pydantic model used when reading data, when returning it from API."""
    id: int
    session_id: str
    last_active: datetime
    scenarios: list[Scenario] = []

    class Config:
        # Pydantic's 'orm_mode' will tell the Pydantic model to read the data
        # even if it is not a dict, but an ORM model (or any other arbitrary
        # object with attributes).
        # This way, instead of only trying to get the 'id' value from a dict
        # like: id = data["id"], it will also try to get it from an attr
        # like: id = data.id
        # With this, Pydantic model is compatible with ORMs, and you can
        # declare it in the 'response_model' argument in your path operations
        orm_mode = True


class SessionResponse(BaseModel):
    """Pydantic model for the response after session creation."""
    session_id: str

    class Config:
        orm_mode = True


class JobBase(BaseModel):
    """Pydantic model base for Jobs."""
    name: str
    description: Optional[str] = None
    status: Literal['success', 'failed', 'pending', 'running']


class Job(JobBase):
    """Pydantic model used when reading data, when returning it from API."""
    job_id: int
    owner_id: str

    class Config:
        orm_mode = True


class JobStatus(BaseModel):
    """Pydantic model used for returning status response of a job."""
    status: Literal['success', 'failed', 'pending', 'running']

    class Config:
        orm_mode = True


class JobResponse(BaseModel):
    """Pydantic model for the response after job creation."""
    job_id: int

    class Config:
        orm_mode = True


class PatternBase(BaseModel):
    """Pydantic model base for Patterns."""
    label: str
    wkt: str


class Pattern(PatternBase):
    """Pydantic model used when reading data, when returning it from API."""
    pattern_id: int
    owner_id: str

    class Config:
        orm_mode = True


class PatternResponse(BaseModel):
    """Pydantic model for the response after the pattern creation."""
    pattern_id: int
    label: str

    class Config:
        orm_mode = True


class ParcelStatsBase(BaseModel):
    """Pydantic model base for ParcelStats."""
    target_parcel_wkt: str


class ParcelStats(ParcelStatsBase):
    """Pydantic model used when reading data, when returning it from API."""
    stats_id: int
    job_id: int
    #owner_id: str

    class Config:
        orm_mode = True


class ParcelStatsRequest(BaseModel):
    """Pydantic model used in establishing the request to create stats."""
    session_id: str
    target_parcel_wkt: str


class ParcelStatsUpdate(BaseModel):
    """Pydantic model used for updating stats."""
    lulc_stats: str


class ParcelStatsResponse(BaseModel):
    """Pydantic model for the response after parcel stats creation request."""
    job_id: int
    #stats_id: int

    class Config:
        orm_mode = True

class WorkerResponse(BaseModel):
    """Pydantic model used for the jobsqueue request from the worker."""
    result: Union[str, dict]
    status: Literal['success', 'failed', 'pending', 'running']
    server_attrs: dict

    class Config:
        orm_mode = True


class Wallpaper(BaseModel):
    """Pydantic model for the wallpaper request."""
    scenario_id: int
    target_parcel_wkt: str
    pattern_id: int

    class Config:
        orm_mode = True


class ParcelFill(BaseModel):
    """Pydantic model for the parcel fill request."""
    scenario_id: int
    target_parcel_wkt: str
    lulc_class: int

    class Config:
        orm_mode = True

