from pydantic import BaseModel, Field
from typing import List

class RecipeStep(BaseModel):
    """Ein einzelner Schritt in einem Rezept."""
    step_number: int
    description: str = ""
    duration: int = 0

class Course(BaseModel):
    """Ein Gang in einem Menü"""
    id: str = ""
    llm_name: str = ""
    recipe_api_name: str = ""
    steps: List[RecipeStep] = []
    link: str = ""


class Menu(BaseModel):
    courses: List[Course] = []



   
