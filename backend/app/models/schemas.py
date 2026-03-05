"""
Pydantic schemas for request validation and response serialisation.
Kept separate from database and routing logic.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, model_validator
from app.config import settings


# ── Request schemas ────────────────────────────────────────────────────────────

class RecordCreate(BaseModel):
    firstname: str
    lastname: str
    age: int
    sex: str
    health: str

    @field_validator("firstname", "lastname")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("must not be blank")
        return v

    @field_validator("age")
    @classmethod
    def age_in_range(cls, v: int) -> int:
        if not (settings.MIN_AGE <= v <= settings.MAX_AGE):
            raise ValueError(f"must be between {settings.MIN_AGE} and {settings.MAX_AGE}")
        return v

    @field_validator("sex")
    @classmethod
    def sex_valid(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in settings.VALID_SEX:
            raise ValueError(f"must be one of {sorted(settings.VALID_SEX)}")
        return v

    @field_validator("health")
    @classmethod
    def health_valid(cls, v: str) -> str:
        v = v.lower().strip()
        if v not in settings.VALID_HEALTH:
            raise ValueError(f"must be one of {sorted(settings.VALID_HEALTH)}")
        return v


class RecordUpdate(BaseModel):
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    health: Optional[str] = None

    @field_validator("firstname", "lastname")
    @classmethod
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("must not be blank")
        return v

    @field_validator("age")
    @classmethod
    def age_in_range(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (settings.MIN_AGE <= v <= settings.MAX_AGE):
            raise ValueError(f"must be between {settings.MIN_AGE} and {settings.MAX_AGE}")
        return v

    @field_validator("sex")
    @classmethod
    def sex_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.lower().strip()
            if v not in settings.VALID_SEX:
                raise ValueError(f"must be one of {sorted(settings.VALID_SEX)}")
        return v

    @field_validator("health")
    @classmethod
    def health_valid(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v = v.lower().strip()
            if v not in settings.VALID_HEALTH:
                raise ValueError(f"must be one of {sorted(settings.VALID_HEALTH)}")
        return v

    @model_validator(mode="after")
    def at_least_one_field(self) -> "RecordUpdate":
        if all(v is None for v in self.model_dump().values()):
            raise ValueError("at least one field must be provided")
        return self


# ── Response schema ────────────────────────────────────────────────────────────

class RecordResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    age: int
    sex: str
    health: str
    created_at: datetime

    model_config = {"from_attributes": True}
