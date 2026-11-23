from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ParticipanteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    nome: str = Field(min_length=1, examples=["Maria Silva"])
    email: EmailStr = Field(examples=["maria@email.com"])
    curso: str = Field(min_length=1, examples=["Engenharia de Software"])


class Participante(ParticipanteCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
