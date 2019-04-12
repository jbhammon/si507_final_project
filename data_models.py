from sqlalchemy import Table, Column, ForeignKey, Integer, String, Boolean # Added a bit here to create association tables...
from sqlalchemy.orm import relationship
from db import Base

## party_to_pokemon relationship table

class Pokemon(Base):
    pass

class Party(Base):
    pass
