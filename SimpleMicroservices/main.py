from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID
from decimal import Decimal

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.organization import OrganizationCreate, OrganizationRead, OrganizationUpdate
from models.course import CourseCreate, CourseRead, CourseUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
organizations: Dict[UUID, OrganizationRead] = {}
courses: Dict[UUID, CourseRead] = {}

app = FastAPI(
    title="Person/Address/Organization/Course API",
    description="Demo FastAPI app using Pydantic v2 models for Person, Address, Organization, and Course management",
    version="0.2.0",
)

# -----------------------------------------------------------------------------
# Health endpoints
# -----------------------------------------------------------------------------

def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())

    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]

    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------

@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())

    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]

    # nested address filtering
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]

    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# -----------------------------------------------------------------------------
# Organization endpoints
# -----------------------------------------------------------------------------

@app.post("/organizations", response_model=OrganizationRead, status_code=201)
def create_organization(organization: OrganizationCreate):
    organization_read = OrganizationRead(**organization.model_dump())
    organizations[organization_read.id] = organization_read
    return organization_read

@app.get("/organizations", response_model=List[OrganizationRead])
def list_organizations(
    name: Optional[str] = Query(None, description="Filter by organization name"),
    org_type: Optional[str] = Query(None, description="Filter by organization type"),
    founded_year: Optional[int] = Query(None, description="Filter by founding year"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
    contact_person_id: Optional[UUID] = Query(None, description="Filter by contact person ID"),
):
    results = list(organizations.values())

    if name is not None:
        results = [o for o in results if name.lower() in o.name.lower()]
    if org_type is not None:
        results = [o for o in results if o.org_type == org_type]
    if founded_year is not None:
        results = [o for o in results if o.founded_year == founded_year]
    if contact_person_id is not None:
        results = [o for o in results if o.contact_person_id == contact_person_id]

    # nested address filtering
    if city is not None:
        results = [o for o in results if any(addr.city == city for addr in o.addresses)]
    if country is not None:
        results = [o for o in results if any(addr.country == country for addr in o.addresses)]

    return results

@app.get("/organizations/{organization_id}", response_model=OrganizationRead)
def get_organization(organization_id: UUID):
    if organization_id not in organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organizations[organization_id]

@app.patch("/organizations/{organization_id}", response_model=OrganizationRead)
def update_organization(organization_id: UUID, update: OrganizationUpdate):
    if organization_id not in organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    stored = organizations[organization_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    organizations[organization_id] = OrganizationRead(**stored)
    return organizations[organization_id]

# -----------------------------------------------------------------------------
# Course endpoints
# -----------------------------------------------------------------------------

@app.post("/courses", response_model=CourseRead, status_code=201)
def create_course(course: CourseCreate):
    # Check if course code already exists for the same semester/year
    existing = [c for c in courses.values() 
                if c.course_code == course.course_code 
                and c.semester == course.semester 
                and c.year == course.year]
    if existing:
        raise HTTPException(
            status_code=400, 
            detail=f"Course {course.course_code} already exists for {course.semester} {course.year}"
        )
    
    course_read = CourseRead(**course.model_dump())
    courses[course_read.id] = course_read
    return course_read

@app.get("/courses", response_model=List[CourseRead])
def list_courses(
    course_code: Optional[str] = Query(None, description="Filter by course code"),
    title: Optional[str] = Query(None, description="Filter by course title (partial match)"),
    department_code: Optional[str] = Query(None, description="Filter by department code"),
    semester: Optional[str] = Query(None, description="Filter by semester"),
    year: Optional[int] = Query(None, description="Filter by year"),
    instructor_id: Optional[UUID] = Query(None, description="Filter by instructor ID"),
    credits: Optional[Decimal] = Query(None, description="Filter by credit value"),
    min_credits: Optional[Decimal] = Query(None, description="Filter by minimum credits"),
    max_credits: Optional[Decimal] = Query(None, description="Filter by maximum credits"),
):
    results = list(courses.values())

    if course_code is not None:
        results = [c for c in results if c.course_code == course_code]
    if title is not None:
        results = [c for c in results if title.lower() in c.title.lower()]
    if department_code is not None:
        results = [c for c in results if c.department_code == department_code]
    if semester is not None:
        results = [c for c in results if c.semester == semester]
    if year is not None:
        results = [c for c in results if c.year == year]
    if instructor_id is not None:
        results = [c for c in results if c.instructor_id == instructor_id]
    if credits is not None:
        results = [c for c in results if c.credits == credits]
    if min_credits is not None:
        results = [c for c in results if c.credits >= min_credits]
    if max_credits is not None:
        results = [c for c in results if c.credits <= max_credits]

    return results

@app.get("/courses/{course_id}", response_model=CourseRead)
def get_course(course_id: UUID):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses[course_id]

@app.patch("/courses/{course_id}", response_model=CourseRead)
def update_course(course_id: UUID, update: CourseUpdate):
    if course_id not in courses:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # If updating course_code, semester, or year, check for conflicts
    if any(field in update.model_dump(exclude_unset=True) 
           for field in ['course_code', 'semester', 'year']):
        current_course = courses[course_id]
        new_code = update.course_code or current_course.course_code
        new_semester = update.semester or current_course.semester
        new_year = update.year or current_course.year
        
        existing = [c for c in courses.values() 
                    if c.id != course_id
                    and c.course_code == new_code 
                    and c.semester == new_semester 
                    and c.year == new_year]
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Course {new_code} already exists for {new_semester} {new_year}"
            )
    
    stored = courses[course_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    courses[course_id] = CourseRead(**stored)
    return courses[course_id]

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Welcome to the Person/Address/Organization/Course API", 
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "persons": "/persons",
            "addresses": "/addresses", 
            "organizations": "/organizations",
            "courses": "/courses"
        }
    }

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)