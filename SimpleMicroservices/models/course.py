from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, StringConstraints
from decimal import Decimal

# Course code constraints (e.g., COMS4111, MATH1101, etc.)
CourseCodeType = Annotated[
    str, 
    StringConstraints(
        pattern=r"^[A-Z]{3,5}\d{4}[A-Z]?$",
        min_length=7,
        max_length=9
    )
]

# Semester constraints
SemesterType = Annotated[
    str,
    StringConstraints(pattern=r"^(Fall|Spring|Summer)$")
]

# Department code constraints (e.g., COMS, MATH, PHYS, etc.)
DepartmentCodeType = Annotated[
    str,
    StringConstraints(
        pattern=r"^[A-Z]{3,5}$",
        min_length=3,
        max_length=5
    )
]


class CourseBase(BaseModel):
    course_code: CourseCodeType = Field(
        ...,
        description="Standardized course code (e.g., COMS4111, MATH1101).",
        json_schema_extra={"example": "COMS4111"},
    )
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Course title.",
        json_schema_extra={"example": "Introduction to Databases"},
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Detailed course description and objectives.",
        json_schema_extra={
            "example": "Fundamentals of database design and implementation. Topics include relational model, SQL, normalization, and transaction management."
        },
    )
    credits: Decimal = Field(
        ...,
        ge=0,
        le=10,
        decimal_places=1,
        description="Number of academic credits (0.0-10.0).",
        json_schema_extra={"example": 3.0},
    )
    semester: SemesterType = Field(
        ...,
        description="Semester when the course is offered (Fall, Spring, Summer).",
        json_schema_extra={"example": "Fall"},
    )
    year: int = Field(
        ...,
        ge=2020,
        le=2040,
        description="Academic year when the course is offered.",
        json_schema_extra={"example": 2025},
    )
    department_code: DepartmentCodeType = Field(
        ...,
        description="Department code offering this course (e.g., COMS, MATH).",
        json_schema_extra={"example": "COMS"},
    )
    instructor_id: Optional[UUID] = Field(
        None,
        description="ID of the instructor (Person) teaching this course.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    max_enrollment: Optional[int] = Field(
        None,
        ge=1,
        le=1000,
        description="Maximum number of students that can enroll.",
        json_schema_extra={"example": 120},
    )
    prerequisites: List[CourseCodeType] = Field(
        default_factory=list,
        description="List of prerequisite course codes.",
        json_schema_extra={"example": ["COMS1004", "COMS3134"]},
    )
    location: Optional[str] = Field(
        None,
        max_length=100,
        description="Classroom or building location.",
        json_schema_extra={"example": "Mudd 233"},
    )
    meeting_times: Optional[str] = Field(
        None,
        max_length=200,
        description="Class meeting schedule (days and times).",
        json_schema_extra={"example": "MW 2:40PM-3:55PM"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "course_code": "COMS4111",
                    "title": "Introduction to Databases",
                    "description": "Fundamentals of database design and implementation.",
                    "credits": 3.0,
                    "semester": "Fall",
                    "year": 2025,
                    "department_code": "COMS",
                    "instructor_id": "99999999-9999-4999-8999-999999999999",
                    "max_enrollment": 120,
                    "prerequisites": ["COMS1004", "COMS3134"],
                    "location": "Mudd 233",
                    "meeting_times": "MW 2:40PM-3:55PM",
                }
            ]
        }
    }


class CourseCreate(CourseBase):
    """Creation payload for a Course."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "course_code": "COMS4115",
                    "title": "Programming Languages and Translators",
                    "description": "Modern programming language concepts and implementation techniques.",
                    "credits": 3.0,
                    "semester": "Spring",
                    "year": 2025,
                    "department_code": "COMS",
                    "instructor_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                    "max_enrollment": 80,
                    "prerequisites": ["COMS3157", "COMS3203"],
                    "location": "Mudd 644",
                    "meeting_times": "TR 11:40AM-12:55PM",
                }
            ]
        }
    }


class CourseUpdate(BaseModel):
    """Partial update for a Course; supply only fields to change."""
    course_code: Optional[CourseCodeType] = Field(
        None,
        description="Standardized course code.",
        json_schema_extra={"example": "COMS4111W"},
    )
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Course title.",
        json_schema_extra={"example": "Advanced Database Systems"},
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Course description.",
        json_schema_extra={"example": "Updated course description with new topics."},
    )
    credits: Optional[Decimal] = Field(
        None,
        ge=0,
        le=10,
        decimal_places=1,
        description="Number of academic credits.",
        json_schema_extra={"example": 4.0},
    )
    semester: Optional[SemesterType] = Field(
        None,
        description="Semester when offered.",
        json_schema_extra={"example": "Spring"},
    )
    year: Optional[int] = Field(
        None,
        ge=2020,
        le=2040,
        description="Academic year.",
        json_schema_extra={"example": 2026},
    )
    department_code: Optional[DepartmentCodeType] = Field(
        None,
        description="Department code.",
        json_schema_extra={"example": "COMS"},
    )
    instructor_id: Optional[UUID] = Field(
        None,
        description="ID of the instructor.",
        json_schema_extra={"example": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"},
    )
    max_enrollment: Optional[int] = Field(
        None,
        ge=1,
        le=1000,
        description="Maximum enrollment.",
        json_schema_extra={"example": 150},
    )
    prerequisites: Optional[List[CourseCodeType]] = Field(
        None,
        description="Replace the entire list of prerequisites.",
        json_schema_extra={"example": ["COMS1004", "COMS3134", "COMS3203"]},
    )
    location: Optional[str] = Field(
        None,
        max_length=100,
        description="Classroom location.",
        json_schema_extra={"example": "Hamilton 517"},
    )
    meeting_times: Optional[str] = Field(
        None,
        max_length=200,
        description="Class meeting schedule.",
        json_schema_extra={"example": "TR 10:10AM-11:25AM"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"title": "Advanced Database Systems"},
                {"max_enrollment": 150},
                {"location": "Hamilton 517", "meeting_times": "TR 10:10AM-11:25AM"},
                {"prerequisites": ["COMS1004", "COMS3134", "COMS3203"]},
            ]
        }
    }


class CourseRead(CourseBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Course ID.",
        json_schema_extra={"example": "77777777-7777-4777-8777-777777777777"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )
    current_enrollment: int = Field(
        default=0,
        ge=0,
        description="Current number of enrolled students.",
        json_schema_extra={"example": 85},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "77777777-7777-4777-8777-777777777777",
                    "course_code": "COMS4111",
                    "title": "Introduction to Databases",
                    "description": "Fundamentals of database design and implementation.",
                    "credits": 3.0,
                    "semester": "Fall",
                    "year": 2025,
                    "department_code": "COMS",
                    "instructor_id": "99999999-9999-4999-8999-999999999999",
                    "max_enrollment": 120,
                    "prerequisites": ["COMS1004", "COMS3134"],
                    "location": "Mudd 233",
                    "meeting_times": "MW 2:40PM-3:55PM",
                    "current_enrollment": 85,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }