import pytest

from src.domain.exceptions.post_exceptions import (
    ImmutablePostException,
    InvalidPayloadException,
    UnauthorizedException,
)
from src.domain.models.post import Post, PostStatus


def test_post_creation_success():
    post = Post(title="Valid Title", content="Valid Content", author_id="author_123")
    assert post.title == "Valid Title"
    assert post.content == "Valid Content"
    assert post.author_id == "author_123"
    assert post.status == PostStatus.DRAFT
    assert post.published_at is None


def test_post_creation_empty_payload():
    with pytest.raises(InvalidPayloadException):
        Post(title="  ", content="Valid Content", author_id="author_123")

    with pytest.raises(InvalidPayloadException):
        Post(title="Valid Title", content="", author_id="author_123")


def test_post_creation_missing_author():
    with pytest.raises(UnauthorizedException):
        Post(title="Valid Title", content="Valid Content", author_id="  ")


def test_post_editing():
    post = Post(title="Old Title", content="Old Content", author_id="author_123")
    post.edit(new_title="New Title", new_content="New Content", requester_id="author_123")
    assert post.title == "New Title"
    assert post.content == "New Content"


def test_post_editing_unauthorized():
    post = Post(title="Old Title", content="Old Content", author_id="author_123")
    with pytest.raises(UnauthorizedException):
        post.edit(new_title="New Title", new_content="New Content", requester_id="hacker_456")


def test_post_publishing():
    post = Post(title="Title", content="Content", author_id="author_123")
    post.publish(requester_id="author_123")
    assert post.status == PostStatus.PUBLISHED
    assert post.published_at is not None

    # Editing published post fails
    with pytest.raises(ImmutablePostException):
        post.edit(new_title="Changed", new_content="Changed", requester_id="author_123")

    # Publishing already published post fails
    with pytest.raises(ImmutablePostException):
        post.publish(requester_id="author_123")
