from typing import Any, Dict, Tuple

from src.application.dto.post_dto import CreatePostDTO, EditPostDTO
from src.application.services.post_service import PostService
from src.domain.exceptions.post_exceptions import (
    ImmutablePostException,
    InvalidPayloadException,
    PostNotFoundException,
    UnauthorizedException,
)
from src.infrastructure.web.middlewares.auth_middleware import extract_auth_context


class AuthorController:
    def __init__(self, service: PostService):
        self.service = service

    def handle_create_post(
        self, headers: Dict[str, Any], body: Dict[str, Any]
    ) -> Tuple[int, Dict[str, Any]]:
        try:
            auth_context = extract_auth_context(headers)
            dto = CreatePostDTO(
                title=body.get("title", ""),
                content=body.get("content", ""),
            )
            response_dto = self.service.create_draft(dto, author_id=auth_context.user_id)
            return 201, {
                "code": 201,
                "message": "Draft created successfully",
                "details": {
                    "id": response_dto.id,
                    "title": response_dto.title,
                    "content": response_dto.content,
                    "status": response_dto.status,
                    "author_id": response_dto.author_id,
                    "created_at": response_dto.created_at,
                    "updated_at": response_dto.updated_at,
                    "published_at": response_dto.published_at,
                },
            }
        except UnauthorizedException as e:
            return 401, {"code": 401, "message": str(e), "details": None}
        except InvalidPayloadException as e:
            return 400, {"code": 400, "message": str(e), "details": None}
        except ImmutablePostException as e:
            return 409, {"code": 409, "message": str(e), "details": None}
        except PostNotFoundException as e:
            return 404, {"code": 404, "message": str(e), "details": None}
        except Exception as e:
            return 500, {
                "code": 500,
                "message": f"Internal server error: {str(e)}",
                "details": None,
            }

    def handle_edit_post(
        self, headers: Dict[str, Any], post_id: str, body: Dict[str, Any]
    ) -> Tuple[int, Dict[str, Any]]:
        try:
            auth_context = extract_auth_context(headers)
            dto = EditPostDTO(
                title=body.get("title", ""),
                content=body.get("content", ""),
            )
            response_dto = self.service.edit_draft(
                post_id=post_id, dto=dto, requester_id=auth_context.user_id
            )
            return 200, {
                "code": 200,
                "message": "Draft updated successfully",
                "details": {
                    "id": response_dto.id,
                    "title": response_dto.title,
                    "content": response_dto.content,
                    "status": response_dto.status,
                    "author_id": response_dto.author_id,
                    "created_at": response_dto.created_at,
                    "updated_at": response_dto.updated_at,
                    "published_at": response_dto.published_at,
                },
            }
        except UnauthorizedException as e:
            return 401, {"code": 401, "message": str(e), "details": None}
        except InvalidPayloadException as e:
            return 400, {"code": 400, "message": str(e), "details": None}
        except ImmutablePostException as e:
            return 409, {"code": 409, "message": str(e), "details": None}
        except PostNotFoundException as e:
            return 404, {"code": 404, "message": str(e), "details": None}
        except Exception as e:
            return 500, {
                "code": 500,
                "message": f"Internal server error: {str(e)}",
                "details": None,
            }

    def handle_publish_post(
        self, headers: Dict[str, Any], post_id: str
    ) -> Tuple[int, Dict[str, Any]]:
        try:
            auth_context = extract_auth_context(headers)
            response_dto = self.service.publish_post(
                post_id=post_id, requester_id=auth_context.user_id
            )
            return 200, {
                "code": 200,
                "message": "Post published successfully",
                "details": {
                    "id": response_dto.id,
                    "title": response_dto.title,
                    "content": response_dto.content,
                    "status": response_dto.status,
                    "author_id": response_dto.author_id,
                    "created_at": response_dto.created_at,
                    "updated_at": response_dto.updated_at,
                    "published_at": response_dto.published_at,
                },
            }
        except UnauthorizedException as e:
            return 401, {"code": 401, "message": str(e), "details": None}
        except InvalidPayloadException as e:
            return 400, {"code": 400, "message": str(e), "details": None}
        except ImmutablePostException as e:
            return 409, {"code": 409, "message": str(e), "details": None}
        except PostNotFoundException as e:
            return 404, {"code": 404, "message": str(e), "details": None}
        except Exception as e:
            return 500, {
                "code": 500,
                "message": f"Internal server error: {str(e)}",
                "details": None,
            }
