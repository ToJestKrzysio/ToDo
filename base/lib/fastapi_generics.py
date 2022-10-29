from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str


class HTTPExceptionResponseModel(BaseModel):
    detail: str

    class Config:
        schema_extra = {
            "example": {"detail": "HTTPException raised."},
        }
