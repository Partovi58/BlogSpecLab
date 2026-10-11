import pytest

from src.application.dto.post_dto import CreatePostDTO
from src.application.services.post_service import PostService
from src.domain.exceptions.post_exceptions import InvalidPayloadException, UnauthorizedException
from src.domain.models.post import PostStatus
from src.infrastructure.persistence.post_repository import InMemoryPostRepository


def test_create_draft_success():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    dto = CreatePostDTO(title="My First Post", content="This is the post content.")

    response = service.create_draft(dto, author_id="author_1")

    assert response.title == "My First Post"
    assert response.content == "This is the post content."
    assert response.status == PostStatus.DRAFT.value
    assert response.author_id == "author_1"
    assert response.id is not None


def test_create_draft_whitespace_rejection():
    repo = InMemoryPostRepository()
    service = PostService(repo)

    with pytest.raises(InvalidPayloadException):
        service.create_draft(CreatePostDTO(title="  ", content="Content"), author_id="author_1")

    with pytest.raises(InvalidPayloadException):
        service.create_draft(CreatePostDTO(title="Title", content="   \n "), author_id="author_1")


def test_create_draft_unauthenticated_rejection():
    repo = InMemoryPostRepository()
    service = PostService(repo)

    with pytest.raises(UnauthorizedException):
        service.create_draft(CreatePostDTO(title="Title", content="Content"), author_id=" ")
