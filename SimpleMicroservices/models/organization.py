from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, StringConstraints

from .address import AddressBase

# Organization type constraints
OrgTypeType = Annotated[
    str, 
    StringConstraints(
        pattern=r"^(university|company|nonprofit|government|startup|research)$"
    )
]


class OrganizationBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Organization name.",
        json_schema_extra={"example": "Columbia University"},
    )
    org_type: OrgTypeType = Field(
        ...,
        description="Type of organization (university, company, nonprofit, government, startup, research).",
        json_schema_extra={"example": "university"},
    )
    website: Optional[HttpUrl] = Field(
        None,
        description="Organization's official website URL.",
        json_schema_extra={"example": "https://www.columbia.edu"},
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Brief description of the organization.",
        json_schema_extra={
            "example": "Ivy League research university in New York City, founded in 1754."
        },
    )
    contact_person_id: Optional[UUID] = Field(
        None,
        description="ID of the primary contact person for this organization.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    employee_count: Optional[int] = Field(
        None,
        ge=0,
        description="Approximate number of employees/members.",
        json_schema_extra={"example": 15000},
    )
    founded_year: Optional[int] = Field(
        None,
        ge=1000,
        le=2030,
        description="Year the organization was founded.",
        json_schema_extra={"example": 1754},
    )
    
    # Embed addresses (organizations can have multiple locations)
    addresses: List[AddressBase] = Field(
        default_factory=list,
        description="Physical addresses/locations of this organization.",
        json_schema_extra={
            "example": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "street": "116th St & Broadway",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10027",
                    "country": "USA",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Columbia University",
                    "org_type": "university",
                    "website": "https://www.columbia.edu",
                    "description": "Ivy League research university in New York City.",
                    "contact_person_id": "99999999-9999-4999-8999-999999999999",
                    "employee_count": 15000,
                    "founded_year": 1754,
                    "addresses": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "street": "116th St & Broadway",
                            "city": "New York", 
                            "state": "NY",
                            "postal_code": "10027",
                            "country": "USA",
                        }
                    ],
                }
            ]
        }
    }


class OrganizationCreate(OrganizationBase):
    """Creation payload for an Organization."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Google LLC",
                    "org_type": "company",
                    "website": "https://www.google.com",
                    "description": "Multinational technology company specializing in Internet-related services.",
                    "contact_person_id": None,
                    "employee_count": 150000,
                    "founded_year": 1998,
                    "addresses": [
                        {
                            "id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
                            "street": "1600 Amphitheatre Parkway",
                            "city": "Mountain View",
                            "state": "CA", 
                            "postal_code": "94043",
                            "country": "USA",
                        }
                    ],
                }
            ]
        }
    }


class OrganizationUpdate(BaseModel):
    """Partial update for an Organization; supply only fields to change."""
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Organization name.",
        json_schema_extra={"example": "Columbia University in the City of New York"},
    )
    org_type: Optional[OrgTypeType] = Field(
        None,
        description="Type of organization.",
        json_schema_extra={"example": "university"},
    )
    website: Optional[HttpUrl] = Field(
        None,
        description="Organization's official website URL.",
        json_schema_extra={"example": "https://www.columbia.edu"},
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Brief description of the organization.",
        json_schema_extra={"example": "Updated description of the organization."},
    )
    contact_person_id: Optional[UUID] = Field(
        None,
        description="ID of the primary contact person.",
        json_schema_extra={"example": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"},
    )
    employee_count: Optional[int] = Field(
        None,
        ge=0,
        description="Approximate number of employees/members.",
        json_schema_extra={"example": 16000},
    )
    founded_year: Optional[int] = Field(
        None,
        ge=1000,
        le=2030,
        description="Year the organization was founded.",
        json_schema_extra={"example": 1754},
    )
    addresses: Optional[List[AddressBase]] = Field(
        None,
        description="Replace the entire set of addresses with this list.",
        json_schema_extra={
            "example": [
                {
                    "id": "cccccccc-cccc-4ccc-8ccc-cccccccccccc",
                    "street": "535 W 116th St",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10027",
                    "country": "USA",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"name": "Columbia University in the City of New York"},
                {"employee_count": 16000},
                {"description": "Premier Ivy League research institution."},
            ]
        }
    }


class OrganizationRead(OrganizationBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Organization ID.",
        json_schema_extra={"example": "88888888-8888-4888-8888-888888888888"},
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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "88888888-8888-4888-8888-888888888888",
                    "name": "Columbia University",
                    "org_type": "university",
                    "website": "https://www.columbia.edu",
                    "description": "Ivy League research university in New York City.",
                    "contact_person_id": "99999999-9999-4999-8999-999999999999",
                    "employee_count": 15000,
                    "founded_year": 1754,
                    "addresses": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "street": "116th St & Broadway",
                            "city": "New York",
                            "state": "NY", 
                            "postal_code": "10027",
                            "country": "USA",
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }