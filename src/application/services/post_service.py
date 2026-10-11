from src.application.dto.post_dto import CreatePostDTO, PostResponseDTO
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
