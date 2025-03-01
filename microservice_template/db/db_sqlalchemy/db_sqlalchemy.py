from sqlalchemy import Sequence, select
from sqlalchemy.orm import Session

from microservice_template.config.db_config import Base, get_db


def create(data: Base, db: Session) -> Base:
    db.add(data)
    db.commit()
    db.refresh(data)
    return data


def get_all(model: Base, db: Session) -> Sequence[Base]:
    found_data =  db.scalars(select(model)).all()
    return found_data

def get_one(model: Base, primary_key: int, db: Session) -> Base| None:
    found_one = db.get(model, primary_key)
    return found_one

def update(updated_data: Base, primary_key: int, model: Base, db: Session) -> Base:
    found_one = get_one(model, primary_key, db)
    for key, value in model:
        setattr(found_one, key, value)
    db.commit()
    return found_one


"""def db_get_all_recipies(db: Session) -> list[ReturnRecipe]:
    found_recipies = db.scalars(select(Recipe)).all()
    return_recipies = [
        ReturnRecipe(
            **recipe.to_dict(),
            ingredients=[ingredient.to_dict() for ingredient in recipe.ingredients],
        )
        for recipe in found_recipies
    ]

    return return_recipies"""