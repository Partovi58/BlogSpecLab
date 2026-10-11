from src.application.services.post_service import PostService
from src.infrastructure.persistence.post_repository import InMemoryPostRepository
from src.infrastructure.web.controllers.author_controller import AuthorController


def test_contract_put_author_edit_draft_success():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    controller = AuthorController(service)

    # First create
    headers = {"Authorization": "Bearer author_123"}
    create_body = {"title": "Initial Title", "content": "Initial Content"}
    _, create_res = controller.handle_create_post(headers, create_body)
    post_id = create_res["details"]["id"]

    # Now edit
    edit_body = {"title": "Updated Title", "content": "Updated Content"}
    status_code, response = controller.handle_edit_post(headers, post_id, edit_body)

    assert status_code == 200
    assert response["code"] == 200
    assert response["message"] == "Draft updated successfully"
    assert response["details"]["title"] == "Updated Title"
    assert response["details"]["content"] == "Updated Content"


def test_contract_put_author_edit_draft_unauthorized_user():
    repo = InMemoryPostRepository()
    service = PostService(repo)
    controller = AuthorController(service)

    # Author 1 creates
    headers1 = {"Authorization": "Bearer author_1"}
    _, create_res = controller.handle_create_post(
        headers1, {"title": "Initial", "content": "Initial"}
    )
    post_id = create_res["details"]["id"]

    # Author 2 attempts edit
    headers2 = {"Authorization": "Bearer author_2"}
    status_code, response = controller.handle_edit_post(
        headers2, post_id, {"title": "Hacked Title", "content": "Hacked Content"}
    )

    assert status_code == 401
    assert response["code"] == 401
    assert "Only the author can edit" in response["message"]
