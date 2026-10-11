from src.application.services.post_service import PostService
from src.infrastructure.persistence.post_repository import InMemoryPostRepository
from src.infrastructure.web.controllers.author_controller import AuthorController


def test_contract_post_author_create_draft():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    controller = AuthorController(service)

    headers = {"Authorization": "Bearer author_123"}
    body = {"title": "Contract Title", "content": "Contract Content"}

    status_code, response = controller.handle_create_post(headers, body)

    assert status_code == 201
    assert response["code"] == 201
    assert response["message"] == "Draft created successfully"
    assert response["details"]["title"] == "Contract Title"
    assert response["details"]["status"] == "Draft"
    assert response["details"]["author_id"] == "author_123"


def test_contract_post_author_create_draft_unauthorized():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    controller = AuthorController(service)

    headers = {}
    body = {"title": "Title", "content": "Content"}

    status_code, response = controller.handle_create_post(headers, body)

    assert status_code == 401
    assert response["code"] == 401
    assert response["message"] == "Authentication token missing"
