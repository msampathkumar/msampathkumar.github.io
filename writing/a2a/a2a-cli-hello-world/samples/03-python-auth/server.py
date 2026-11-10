"""A2A v1.0 Hello World server in Python with API key Bearer token verification."""

import hmac
import os
import uvicorn
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from a2a.helpers import (
    get_message_text,
    new_task_from_user_message,
    new_text_message,
    new_text_part,
)
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.routes import create_agent_card_routes, create_jsonrpc_routes
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentInterface,
    AgentSkill,
    HTTPAuthSecurityScheme,
    SecurityScheme,
)
from a2a.types.a2a_pb2 import TaskState
from a2a.utils.constants import AGENT_CARD_WELL_KNOWN_PATH

HOST = os.environ.get("A2A_HOST", "127.0.0.1")
PORT = int(os.environ.get("A2A_PORT", "9003"))
BASE_URL = os.environ.get("A2A_BASE_URL", f"http://{HOST}:{PORT}")
EXPECTED_API_KEY = os.environ.get("A2A_API_KEY", "a2a-demo-secret-key")


class ApiKeyAuthMiddleware(BaseHTTPMiddleware):
    """Allows public Agent Card discovery and requires a valid Bearer API key on RPC calls."""

    async def dispatch(self, request: Request, call_next):
        if request.url.path == AGENT_CARD_WELL_KNOWN_PATH:
            return await call_next(request)

        auth_header = request.headers.get("authorization", "")
        scheme, _, token = auth_header.partition(" ")
        if scheme.lower() != "bearer" or not hmac.compare_digest(
            token.strip(), EXPECTED_API_KEY
        ):
            return JSONResponse(
                {
                    "error": {
                        "code": 401,
                        "status": "UNAUTHENTICATED",
                        "message": "Missing or invalid Bearer API key token.",
                    }
                },
                status_code=401,
                headers={"WWW-Authenticate": "Bearer"},
            )
        return await call_next(request)


class SecuredPythonExecutor(AgentExecutor):
    """Replies after the middleware has verified the caller's API key."""

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        task = context.current_task
        if not task:
            task = new_task_from_user_message(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(
            event_queue=event_queue, task_id=task.id, context_id=task.context_id
        )
        await updater.update_status(
            state=TaskState.TASK_STATE_WORKING,
            message=new_text_message("Verified API key; processing in Python..."),
        )

        user_text = get_message_text(context.message) or "World"
        reply = (
            f"Hello from Secured Python A2A Agent! "
            f'API key verified. You said: "{user_text}"'
        )

        await updater.add_artifact(
            parts=[new_text_part(text=reply, media_type="text/plain")]
        )
        await updater.update_status(
            state=TaskState.TASK_STATE_COMPLETED,
            message=new_text_message("Secured greeting complete."),
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        updater = TaskUpdater(
            event_queue=event_queue,
            task_id=context.task_id or "",
            context_id=context.context_id or "",
        )
        await updater.cancel()


def build_agent_card() -> AgentCard:
    card = AgentCard(
        name="Secured Python Hello World Agent",
        description="Python A2A v1.0 agent protected by Bearer API key verification.",
        version="1.0.0",
        default_input_modes=["text/plain"],
        default_output_modes=["text/plain"],
        capabilities=AgentCapabilities(streaming=True),
        supported_interfaces=[
            AgentInterface(
                protocol_binding="JSONRPC",
                url=BASE_URL,
                protocol_version="1.0",
            )
        ],
        skills=[
            AgentSkill(
                id="hello-python-auth",
                name="Authenticated Python Greeting",
                description="Replies with a greeting when a valid Bearer API key is supplied.",
                input_modes=["text/plain"],
                output_modes=["text/plain"],
                tags=["hello", "python", "auth", "a2a"],
                examples=["Hello with an API key!"],
            )
        ],
    )
    card.security_schemes["bearer_api_key"].CopyFrom(
        SecurityScheme(
            http_auth_security_scheme=HTTPAuthSecurityScheme(
                scheme="Bearer",
                bearer_format="APIKey",
                description="Pass the API key via `a2a send --auth 'Bearer <API_KEY>'`",
            )
        )
    )
    return card


def build_app() -> Starlette:
    card = build_agent_card()
    handler = DefaultRequestHandler(
        agent_executor=SecuredPythonExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=card,
    )
    routes = [
        *create_agent_card_routes(card),
        *create_jsonrpc_routes(handler, rpc_url="/"),
    ]
    return Starlette(
        routes=routes,
        middleware=[Middleware(ApiKeyAuthMiddleware)],
    )


if __name__ == "__main__":
    print(f"Secured Python A2A server listening on {BASE_URL}")
    uvicorn.run(build_app(), host=HOST, port=PORT, log_level="warning")
