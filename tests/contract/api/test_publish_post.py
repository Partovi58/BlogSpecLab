from src.application.services.post_service import PostService
from src.infrastructure.persistence.post_repository import InMemoryPostRepository
from src.infrastructure.web.controllers.author_controller import AuthorController


def test_contract_post_author_publish_draft_success():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    controller = AuthorController(service)

    # Create draft
    headers = {"Authorization": "Bearer author_123"}
    _, create_res = controller.handle_create_post(
        headers, {"title": "Title to Publish", "content": "Content to Publish"}
    )
    post_id = create_res["details"]["id"]

    # Publish draft
    status_code, response = controller.handle_publish_post(headers, post_id)

    assert status_code == 200
    assert response["code"] == 200
    assert response["message"] == "Post published successfully"
    assert response["details"]["status"] == "Published"
    assert response["details"]["published_at"] is not None


def test_contract_post_author_publish_unauthorized():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    controller = AuthorController(service)

    # Author 1 creates draft
    headers1 = {"Authorization": "Bearer author_1"}
    _, create_res = controller.handle_create_post(
        headers1, {"title": "Title", "content": "Content"}
    )
    post_id = create_res["details"]["id"]

    # Author 2 attempts publish
    headers2 = {"Authorization": "Bearer author_2"}
    status_code, response = controller.handle_publish_post(headers2, post_id)

    assert status_code == 401
    assert response["code"] == 401
    assert "Only the author can publish" in response["message"]
