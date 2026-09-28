from pydantic import BaseModel, Field, field_validator


class TaskCreate(BaseModel):
    """Модель для создания задачи."""

    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description=(
            "Название задачи (от 3 до 100 символов). "
            "Не может состоять только из пробелов."
        ),
    )
    description: str | None = Field(
        default=None,
        description="Подробное описание задачи (необязательно, по умолчанию — None)",
    )
    priority: int = Field(
        ...,
        ge=1,
        le=5,
        description="Приоритет задачи от 1 (низкий) до 5 (высокий)",
    )

    @field_validator("title")
    @classmethod
    def title_not_blank(cls, v: str) -> str:
        """title не может состоять только из пробелов."""
        if not v.strip():
            raise ValueError("title must not be blank or whitespace-only")
        return v


class TaskResponse(BaseModel):
    """Модель ответа с данными задачи."""

    id: int = Field(description="Уникальный идентификатор задачи")
    title: str = Field(description="Название задачи")
    description: str | None = Field(
        default=None, description="Подробное описание задачи"
    )
    priority: int = Field(description="Приоритет задачи от 1 до 5")

    model_config = {"from_attributes": True}
