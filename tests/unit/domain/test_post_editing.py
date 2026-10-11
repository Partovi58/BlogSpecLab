import pytest

from src.application.dto.post_dto import CreatePostDTO, EditPostDTO
from src.application.services.post_service import PostService
from src.domain.exceptions.post_exceptions import (
    InvalidPayloadException,
    PostNotFoundException,
    UnauthorizedException,
)
from src.infrastructure.persistence.post_repository import InMemoryPostRepository


def test_edit_draft_success():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    post_res = service.create_draft(
        CreatePostDTO(title="Old Title", content="Old Content"), author_id="author_1"
    )

    edit_dto = EditPostDTO(title="New Title", content="New Content")
    updated_res = service.edit_draft(
        post_id=post_res.id, dto=edit_dto, requester_id="author_1"
    )

    assert updated_res.title == "New Title"
    assert updated_res.content == "New Content"


def test_edit_draft_unauthorized():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    post_res = service.create_draft(
        CreatePostDTO(title="Old Title", content="Old Content"), author_id="author_1"
    )

    edit_dto = EditPostDTO(title="New Title", content="New Content")
    with pytest.raises(UnauthorizedException):
        service.edit_draft(
            post_id=post_res.id, dto=edit_dto, requester_id="author_2"
        )


def test_edit_draft_invalid_payload():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    post_res = service.create_draft(
        CreatePostDTO(title="Old Title", content="Old Content"), author_id="author_1"
    )

    with pytest.raises(InvalidPayloadException):
        service.edit_draft(
            post_id=post_res.id,
            dto=EditPostDTO(title="   ", content="Valid"),
            requester_id="author_1",
        )


def test_edit_draft_not_found():
    repo = InMemoryPostRepository()
    service = PostService(repo)

    with pytest.raises(PostNotFoundException):
        service.edit_draft(
            post_id="non_existent_id",
            dto=EditPostDTO(title="Title", content="Content"),
            requester_id="author_1",
        )
