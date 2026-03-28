import re

from pydantic import BaseModel, Field, field_validator


KEBAB_CASE_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
DATE_VERSION_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class VersionedRef(BaseModel):
    id: str
    version: str

    @field_validator("id")
    @classmethod
    def validate_kebab_case(cls, value: str) -> str:
        if not KEBAB_CASE_PATTERN.fullmatch(value):
            raise ValueError("id must use kebab-case")
        return value

    @field_validator("version")
    @classmethod
    def validate_date_version(cls, value: str) -> str:
        if not DATE_VERSION_PATTERN.fullmatch(value):
            raise ValueError("version must use YYYY-MM-DD")
        return value


class ModelTarget(BaseModel):
    model_provider: str
    model_name: str
    model_version: str


class SamplingProfile(BaseModel):
    profile_id: str
    temperature: float = 0.8
    top_p: float = 0.95
    max_tokens: int = Field(default=512, ge=1)
