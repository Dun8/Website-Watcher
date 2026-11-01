from pydantic import BaseModel, Field, HttpUrl


class WebsiteCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    url: HttpUrl
    css_selector: str | None = Field(default=None, description="Необязательный CSS-селектор. Если не указан, проверяется вся страница.")
    check_interval_minutes: int = Field(default=60, ge=5)


class WebsiteUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    check_interval_minutes: int | None = Field(default=None, ge=5)
    is_active: bool | None = None
    css_selector: str | None = Field(default=None, description="Необязательный CSS-селектор. Если не указан, проверяется вся страница.")