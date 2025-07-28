from dataclasses import dataclass


@dataclass
class PhotoUrlEntity:
    url: str
    
@dataclass
class PhotoEntity:
    filename: str
    content: bytes
    content_type: str
    
@dataclass
class PhotoUniqueNameEntity:
    name: str