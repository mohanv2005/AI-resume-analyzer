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