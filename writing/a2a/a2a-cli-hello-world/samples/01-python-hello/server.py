"""Minimal A2A v1.0 Hello World server in Python."""

import os
import uvicorn
from starlette.applications import Starlette

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
from a2a.types import AgentCapabilities, AgentCard, AgentInterface, AgentSkill
from a2a.types.a2a_pb2 import TaskState

HOST = os.environ.get("A2A_HOST", "127.0.0.1")
PORT = int(os.environ.get("A2A_PORT", "9001"))
BASE_URL = os.environ.get("A2A_BASE_URL", f"http://{HOST}:{PORT}")


class HelloPythonExecutor(AgentExecutor):
    """Handles incoming A2A messages and replies with a greeting artifact."""

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
            message=new_text_message("Processing greeting in Python..."),
        )

        user_text = get_message_text(context.message) or "World"
        reply = f'Hello from Python A2A Agent! You said: "{user_text}"'

        await updater.add_artifact(
            parts=[new_text_part(text=reply, media_type="text/plain")]
        )
        await updater.update_status(
            state=TaskState.TASK_STATE_COMPLETED,
            message=new_text_message("Greeting complete."),
        )

    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        updater = TaskUpdater(
            event_queue=event_queue,
            task_id=context.task_id or "",
            context_id=context.context_id or "",
        )
        await updater.cancel()


def build_agent_card() -> AgentCard:
    return AgentCard(
        name="Python Hello World Agent",
        description="Minimal A2A v1.0 Hello World agent built with a2a-sdk in Python.",
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
                id="hello-python",
                name="Python Greeting",
                description="Echoes a greeting from the Python A2A server.",
                input_modes=["text/plain"],
                output_modes=["text/plain"],
                tags=["hello", "python", "a2a"],
                examples=["Hello from A2A CLI!"],
            )
        ],
    )


def build_app() -> Starlette:
    card = build_agent_card()
    handler = DefaultRequestHandler(
        agent_executor=HelloPythonExecutor(),
        task_store=InMemoryTaskStore(),
        agent_card=card,
    )
    routes = [
        *create_agent_card_routes(card),
        *create_jsonrpc_routes(handler, rpc_url="/"),
    ]
    return Starlette(routes=routes)


if __name__ == "__main__":
    print(f"Python Hello World A2A server listening on {BASE_URL}")
    uvicorn.run(build_app(), host=HOST, port=PORT, log_level="warning")
