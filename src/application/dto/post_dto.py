from dataclasses import dataclass
from typing import Optional

from src.domain.exceptions.post_exceptions import InvalidPayloadException


@dataclass
class CreatePostDTO:
    title: str
    content: str

    def validate(self) -> None:
        if not self.title or not self.title.strip():
            raise InvalidPayloadException("Title cannot be empty or whitespace only")
        if not self.content or not self.content.strip():
            raise InvalidPayloadException("Content cannot be empty or whitespace only")


@dataclass
class EditPostDTO:
    title: str
    content: str

    def validate(self) -> None:
        if not self.title or not self.title.strip():
            raise InvalidPayloadException("Title cannot be empty or whitespace only")
        if not self.content or not self.content.strip():
            raise InvalidPayloadException("Content cannot be empty or whitespace only")


@dataclass
class PostResponseDTO:
    id: str
    title: str
    content: str
    status: str
    author_id: str
    created_at: str
    updated_at: str
    published_at: Optional[str] = None
