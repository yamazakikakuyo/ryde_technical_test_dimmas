from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class Location(BaseModel):
    type: str = Field(default="Point",json_schema_extra={"example": "Point"})
    coordinates: List[float] = Field(...,json_schema_extra={"example": [106.8456, -6.2088]})  # [longitude, latitude]

class UserBase(BaseModel):
    username: str = Field(...,json_schema_extra={"example": "john_doe"})
    name: str = Field(...,json_schema_extra={"example": "John Doe"})
    dob: date = Field(...,json_schema_extra={"example": "1990-01-01"})
    address: str = Field(...,json_schema_extra={"example": "1234 Main St"})
    description: str = Field(...,json_schema_extra={"example": "A sample user"})
    location: Location = Field(...,json_schema_extra={"example": {"type": "Point", "coordinates": [106.8456, -6.2088]}})

class UserCreate(UserBase):
    """Schema used when creating a new user."""
    pass

class UserUpdate(BaseModel):
    """Schema for updating an existing user."""
    username: str = Field(None,json_schema_extra={"example": "john_doe"})
    name: Optional[str] = Field(None,json_schema_extra={"example": "John Doe"})
    dob: Optional[date] = Field(None,json_schema_extra={"example": "1990-01-01"})
    address: Optional[str] = Field(None,json_schema_extra={"example": "1234 Updated St"})
    description: Optional[str] = Field(None,json_schema_extra={"example": "Updated desc"})
    followers: Optional[List[str]] = Field(default_factory=list,json_schema_extra={"example": ["1", "2", "3"]})
    following: Optional[List[str]] = Field(default_factory=list,json_schema_extra={"example": ["4", "5", "6"]})
    location: Optional[Location] = Field(None,json_schema_extra={"example": {"type": "Point", "coordinates": [106.8456, -6.2088]}})

class UserInDB(UserBase):
    id: str
    createdAt: str
    followers: List[str]
    following: List[str]
    
    model_config = {
        "from_attributes": True
    }
