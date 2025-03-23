from sqlalchemy import Column, Integer, String
from app.db.base import Base

class ExampleModel(Base):
    __tablename__ = 'examples'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)

    def __repr__(self):
        return f"<ExampleModel(id={self.id}, name={self.name}, description={self.description})>"