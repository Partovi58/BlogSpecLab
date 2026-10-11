import pytest

from src.application.dto.post_dto import CreatePostDTO, EditPostDTO
from src.application.services.post_service import PostService
from src.domain.exceptions.post_exceptions import (
    ImmutablePostException,
    UnauthorizedException,
)
from src.domain.models.post import PostStatus
from src.infrastructure.persistence.post_repository import InMemoryPostRepository


def test_publish_post_success():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    post_res = service.create_draft(
        CreatePostDTO(title="Draft Title", content="Draft Content"), author_id="author_1"
    )

    published_res = service.publish_post(post_id=post_res.id, requester_id="author_1")

    assert published_res.status == PostStatus.PUBLISHED.value
    assert published_res.published_at is not None


def test_publish_post_unauthorized():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    post_res = service.create_draft(
        CreatePostDTO(title="Draft Title", content="Draft Content"), author_id="author_1"
    )

    with pytest.raises(UnauthorizedException):
        service.publish_post(post_id=post_res.id, requester_id="author_2")


def test_published_post_immutability():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    post_res = service.create_draft(
        CreatePostDTO(title="Draft Title", content="Draft Content"), author_id="author_1"
    )
    service.publish_post(post_id=post_res.id, requester_id="author_1")

    # Attempt to edit published post fails
    with pytest.raises(ImmutablePostException):
        service.edit_draft(
            post_id=post_res.id,
            dto=EditPostDTO(title="New Title", content="New Content"),
            requester_id="author_1",
        )

    # Attempt to publish already published post fails
    with pytest.raises(ImmutablePostException):
        service.publish_post(post_id=post_res.id, requester_id="author_1")
