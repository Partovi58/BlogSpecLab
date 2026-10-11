import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from src.domain.exceptions.post_exceptions import (
    ImmutablePostException,
    InvalidPayloadException,
    UnauthorizedException,
)


class PostStatus(str, Enum):
    DRAFT = "Draft"
    PUBLISHED = "Published"


class Post:
    def __init__(
        self,
        title: str,
        content: str,
        author_id: str,
        post_id: Optional[str] = None,
        status: PostStatus = PostStatus.DRAFT,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        published_at: Optional[datetime] = None,
    ):
        self._validate_payload(title, content)
        if not author_id or not author_id.strip():
            raise UnauthorizedException("Author ID is required")

        now = datetime.now(timezone.utc)
        self.id = post_id or str(uuid.uuid4())
        self.title = title.strip()
        self.content = content.strip()
        self.author_id = author_id.strip()
        self.status = status
        self.created_at = created_at or now
        self.updated_at = updated_at or now
        self.published_at = published_at

    @staticmethod
    def _validate_payload(title: str, content: str) -> None:
        if not title or not title.strip():
            raise InvalidPayloadException("Title cannot be empty or whitespace only")
        if not content or not content.strip():
            raise InvalidPayloadException("Content cannot be empty or whitespace only")

    def edit(self, new_title: str, new_content: str, requester_id: str) -> None:
        if self.status == PostStatus.PUBLISHED:
            raise ImmutablePostException("Published posts cannot be edited")
        if requester_id != self.author_id:
            raise UnauthorizedException("Only the author can edit this draft")

        self._validate_payload(new_title, new_content)
        self.title = new_title.strip()
        self.content = new_content.strip()
        self.updated_at = datetime.now(timezone.utc)

    def publish(self, requester_id: str) -> None:
        if self.status == PostStatus.PUBLISHED:
            raise ImmutablePostException("Post is already published")
        if requester_id != self.author_id:
            raise UnauthorizedException("Only the author can publish this draft")

        now = datetime.now(timezone.utc)
        self.status = PostStatus.PUBLISHED
        self.updated_at = now
        self.published_at = now
