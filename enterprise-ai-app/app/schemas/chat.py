from pydantic import BaseModel, Field

class LoginRequest(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=3)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ChatRequest(BaseModel):
    question: str = Field(min_length=2, max_length=5000)
    conversation_id: str | None = None

class Source(BaseModel):
    id: str
    text: str
    score: float

class ChatResponse(BaseModel):
    answer: str
    sources: list[Source]
    conversation_id: str
