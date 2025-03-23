from app.db.models.example_model import ExampleModel
from app.schemas.example_schema import ExampleSchema
from sqlalchemy.orm import Session
from fastapi import HTTPException

class ExampleService:
    def __init__(self, db: Session):
        self.db = db

    def create_example(self, example_data: ExampleSchema) -> ExampleModel:
        db_example = ExampleModel(**example_data.dict())
        self.db.add(db_example)
        self.db.commit()
        self.db.refresh(db_example)
        return db_example

    def get_example(self, example_id: int) -> ExampleModel:
        db_example = self.db.query(ExampleModel).filter(ExampleModel.id == example_id).first()
        if db_example is None:
            raise HTTPException(status_code=404, detail="Example not found")
        return db_example

    def update_example(self, example_id: int, example_data: ExampleSchema) -> ExampleModel:
        db_example = self.get_example(example_id)
        for key, value in example_data.dict().items():
            setattr(db_example, key, value)
        self.db.commit()
        return db_example

    def delete_example(self, example_id: int) -> None:
        db_example = self.get_example(example_id)
        self.db.delete(db_example)
        self.db.commit()