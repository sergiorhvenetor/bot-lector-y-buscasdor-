from pydantic import BaseModel
from typing import List, Union, Literal

class TextContent(BaseModel):
    type: Literal["text"]
    text: str

class ImageUrlContent(BaseModel):
    type: Literal["image_url"]
    image_url: str

class FileContent(BaseModel):
    type: Literal["file"]
    data: str  # Assuming file data is base64 encoded string
    mime_type: str

class UserChatMessage(BaseModel):
    content: List[Union[TextContent, FileContent, ImageUrlContent]]
