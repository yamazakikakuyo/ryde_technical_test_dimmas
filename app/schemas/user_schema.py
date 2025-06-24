from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

class Location(BaseModel):
    type: str = Field(default="Point", example="Point")
    coordinates: List[float] = Field(..., example=[106.8456, -6.2088])  # [longitude, latitude]

class UserBase(BaseModel):
    name: str = Field(..., example="John Doe")
    dob: date = Field(..., example="1990-01-01")
    address: str = Field(..., example="1234 Main St")
    description: str = Field(..., example="A sample user")
    followers: List[str] = Field(default_factory=list, example=["1", "2", "3"])
    following: List[str] = Field(default_factory=list, example=["4", "5", "6"])
    location: Location = Field(..., example={"type": "Point", "coordinates": [106.8456, -6.2088]})

class UserCreate(UserBase):
    """Schema used when creating a new user."""
    pass

class UserUpdate(BaseModel):
    """Schema for updating an existing user."""
    name: Optional[str] = Field(None, example="John Doe")
    dob: Optional[date] = Field(None, example="1990-01-01")
    address: Optional[str] = Field(None, example="1234 Updated St")
    description: Optional[str] = Field(None, example="Updated desc")
    followers: Optional[List[str]] = Field(default_factory=list, example=["1", "2", "3"])
    following: Optional[List[str]] = Field(default_factory=list, example=["4", "5", "6"])
    location: Optional[Location] = Field(None, example={"type": "Point", "coordinates": [106.8456, -6.2088]})

class UserInDB(UserBase):
    id: str
    createdAt: str

    class Config:
        orm_mode = True
