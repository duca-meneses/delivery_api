from pydantic import BaseModel, ConfigDict, EmailStr


class SignUpModelRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_staff: bool = False
    is_active: bool = False
    model_config = ConfigDict(from_atributes=True)


class SignUpModelResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    is_staff: bool = False
    is_active: bool = False
    model_config = ConfigDict(from_atributes=True)
