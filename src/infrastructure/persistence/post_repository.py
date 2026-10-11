from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.models.post import Post, PostStatus


class PostRepository(ABC):
    @abstractmethod
    def save(self, post: Post) -> None:
        pass

    @abstractmethod
    def get_by_id(self, post_id: str) -> Optional[Post]:
        pass

    @abstractmethod
    def get_published_posts(self) -> List[Post]:
        pass


class InMemoryPostRepository(PostRepository):
    def __init__(self):
        self._posts: dict[str, Post] = {}

    def save(self, post: Post) -> None:
        self._posts[post.id] = post

    def get_by_id(self, post_id: str) -> Optional[Post]:
        return self._posts.get(post_id)

    def get_published_posts(self) -> List[Post]:
        published = [p for p in self._posts.values() if p.status == PostStatus.PUBLISHED]
        # Sort by published_at DESC (newest first)
        return sorted(published, key=lambda p: p.published_at or p.created_at, reverse=True)
