from pydantic import BaseModel


class InfoBase(BaseModel):
    title: str
    description: str | None = None


class InfoCreate(InfoBase):
    pass


class Info(InfoBase):
    index: int
    info_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Info] = []

    class Config:
        orm_mode = True