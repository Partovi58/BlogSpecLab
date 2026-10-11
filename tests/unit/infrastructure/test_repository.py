from src.domain.models.post import Post
from src.infrastructure.persistence.post_repository import InMemoryPostRepository


def test_in_memory_repository():
    repo = InMemoryPostRepository()
    post1 = Post(title="Title 1", content="Content 1", author_id="author_1")
    post2 = Post(title="Title 2", content="Content 2", author_id="author_2")

    repo.save(post1)
    repo.save(post2)

    assert repo.get_by_id(post1.id) == post1

    # Only published posts returned
    assert len(repo.get_published_posts()) == 0

    post1.publish("author_1")
    repo.save(post1)

    published = repo.get_published_posts()
    assert len(published) == 1
    assert published[0].id == post1.id
