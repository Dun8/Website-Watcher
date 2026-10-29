from pydantic import BaseModel, Field, HttpUrl

class WebsiteCreate(BaseModel):
    name: str = Field(min_length= 1, max_length=120)
    url: HttpUrl
    css_selector: str | None = None
    check_interval_minutes: int | None = Field(default=60, ge=5)