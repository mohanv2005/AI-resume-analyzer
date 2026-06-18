from pydantic import BaseModel
from typing import Optional

class UploadResponse(BaseModel):
    filename: str           
    file_size: int          
    content_type: str       
    message: str            
    saved_path: str        


class ErrorResponse(BaseModel):
    error: str              
    detail: str             

class ExtractResponse(BaseModel):
    filename: str
    page_count: int
    word_count: int
    line_count: int
    char_count: int
    extracted_text: str         # The full cleaned text
    message: str