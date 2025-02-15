from sqlalchemy.orm import Session

from microservice_template.config.db_config import Base, get_db


def create(data: Base, db: Session) -> Base:
    db.add(data)
    db.commit()
    db.refresh(data)
    return data







"""def db_create_recipe(recipe_data: CreateRecipe, user_id: int, test_db: Session):
    new_recipe = Recipe(
        **recipe_data.model_dump(exclude={"ingredients"}), created_by=user_id
    )
    test_db.add(new_recipe)
    test_db.commit()
    test_db.refresh(new_recipe)
    return new_recipe"""