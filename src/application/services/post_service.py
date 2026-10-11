from src.application.dto.post_dto import CreatePostDTO, EditPostDTO, PostResponseDTO
from src.domain.exceptions.post_exceptions import PostNotFoundException
from src.domain.models.post import Post
from src.infrastructure.persistence.post_repository import PostRepository


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    def create_draft(self, dto: CreatePostDTO, author_id: str) -> PostResponseDTO:
        dto.validate()
        post = Post(title=dto.title, content=dto.content, author_id=author_id)
        self.repository.save(post)

        return PostResponseDTO(
            id=post.id,
            title=post.title,
            content=post.content,
            status=post.status.value,
            author_id=post.author_id,
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat(),
            published_at=post.published_at.isoformat() if post.published_at else None,
        )

    def edit_draft(self, post_id: str, dto: EditPostDTO, requester_id: str) -> PostResponseDTO:
        dto.validate()
        post = self.repository.get_by_id(post_id)
        if not post:
            raise PostNotFoundException("Post not found")

        post.edit(new_title=dto.title, new_content=dto.content, requester_id=requester_id)
        self.repository.save(post)

        return PostResponseDTO(
            id=post.id,
            title=post.title,
            content=post.content,
            status=post.status.value,
            author_id=post.author_id,
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat(),
            published_at=post.published_at.isoformat() if post.published_at else None,
        )

    def publish_post(self, post_id: str, requester_id: str) -> PostResponseDTO:
        post = self.repository.get_by_id(post_id)
        if not post:
            raise PostNotFoundException("Post not found")

        post.publish(requester_id=requester_id)
        self.repository.save(post)

        return PostResponseDTO(
            id=post.id,
            title=post.title,
            content=post.content,
            status=post.status.value,
            author_id=post.author_id,
            created_at=post.created_at.isoformat(),
            updated_at=post.updated_at.isoformat(),
            published_at=post.published_at.isoformat() if post.published_at else None,
        )
