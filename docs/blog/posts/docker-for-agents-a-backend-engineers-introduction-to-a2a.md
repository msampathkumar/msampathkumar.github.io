---
title: "Docker for Agents: A Backend Engineer’s Introduction to A2A"
description: "A2A Introduction Post  A2A is a lightweight wrapper — like Docker. Your app stays exactly as it is;..."
date: 2026-06-15
authors:
  - sampathm
categories:
  - backend
  - a2aprotocol
  - aiagentsinaction
canonical_url: "https://medium.com/google-cloud/a2a-protocol-blog-post-01-introduction-8294ca1d6a61"
---

> Originally published on
> [dev.to](https://dev.to/sampathm/docker-for-agents-a-backend-engineers-introduction-to-a2a-3h0p)
> /
> [Medium](https://medium.com/google-cloud/a2a-protocol-blog-post-01-introduction-8294ca1d6a61).

![A2A Introduction Post](https://cdn-images-1.medium.com/max/1024/0*jwY8iemtl1oBPKtE)
_A2A Introduction Post_

A2A is a lightweight wrapper — like Docker. Your app stays exactly as it is;
you add the wrapper, and it gains the ability to talk to any agent in the
world. In this posts, I share the three concepts you actually need to know.

### Introduction

You built an agent. It works. Now someone asks the obvious next question: _can
it talk to the agent another team built?_

Today, the answer is usually, “Only if we write a custom integration for each
one”. That’s the same trap **REST APIs** solved for web services — and it’s
exactly the trap **A2A (Agent-to-Agent protocol)** is built to get us out of.

Here’s the mental model I’d lead with, because every backend engineer already
owns it:

> **_A2A is a lightweight wrapper, like Docker._** _Your Agentic app lives
> exactly as it is. You wrap it with A2A, and it automatically gains the
> ability to be discovered by — and talk to — any agent in the world. You
> didn’t rewrite your app; you made it portable._

With Docker you wrap your app, and it runs anywhere. Similarly, wrap your agent
with A2A, it talks to any Agents across the world. In this post, I share the
three concepts you need to understand to make your agent interoperable.

This is **Part 1 of a series.** Later parts go deep on multi-tenancy (serving
many agents behind one host), a 60-second Quickstart, and more. Today we stay
at the intro: the smallest complete mental model you can hold in your head.

### What you’ll learn

1. **The Agent Card**  — how an agent advertises who it is and how to reach it
   (discovery).
1. **Tasks & messages**  — how a client asks your agent to do work.
1. **The EventQueue & status updates**  — why long-running work doesn’t block,
   and the weightlifting A2A does for you.

That’s it. Three concepts. Everything else (auth schemes, multi-tenancy,
extended cards) is a _later_ post — and you won’t need it to ship your first
interoperable agent.

#### The mental model, in one diagram

The wrapper sits between any A2A client and your unchanged app:

![A2A Intro — Mermaid Chart 1](https://cdn-images-1.medium.com/max/1024/1*T7nN-ec391OG7PQwaLUiVA.png)
_A2A Intro — Mermaid Chart 1_

And here’s the same interaction over time — discovery, then the task lifecycle:

![A2A Intro — Mermaid Chart 2](https://cdn-images-1.medium.com/max/1024/1*Bp4v-FnXDiSv8DbffcaOcg.png)
_A2A Intro — Mermaid Chart 2_

Now the three concepts.

### 1. The Agent Card — discovery

Before two agents can work together, one has to find the other and learn what
it can do. In A2A, every agent publishes an **Agent Card** : a small,
structured description served at a well-known URL. It says _who I am_, _what I
can do_ (skills), _where to reach me_ (interfaces/endpoints), and _what
features I support_ (e.g. streaming).

```python
# Conceptual (trimmed from the hello-world sample)
public_agent_card = AgentCard(
    name="Hello World Agent",
    description="Just a hello world agent",
    version="0.0.1",
    capabilities=AgentCapabilities(streaming=True),
    supported_interfaces=[
        AgentInterface(protocol_binding="JSONRPC", url="http://127.0.0.1:9999"),
    ],
    skills=[skill],  # Not the same Agent skills
)
```

A client fetches this card from an A2A instance endpoint, reads it, and knows
exactly how to talk to you — no out-of-band docs, no bespoke client. This is
the part that makes “any agent in the world” literally true.

**Tips:** Discovery is the front door — if you publish a good Agent Card,
everything else (including the routing tricks in the multi-tenancy post) falls
out of it.

### 2. Tasks & Messages — asking an agent to do work

Once a client has your card, it sends a **message** (think: the request — text,
and optionally files/structured parts). Your wrapper turns that into a **Task**
— the unit of work A2A tracks from start to finish.

```python
# Conceptual: the wrapper turns an incoming message into a Task
task = new_task_from_user_message(context.message)
await event_queue.enqueue_event(task)
```

A message is the “what I want.” A task is the “thing being worked on,” with a
lifecycle and an id the client can follow. Your app’s actual logic — the LLM
call, the database query, the tool use — runs unchanged underneath.

**Tip:** If you can think in request → unit-of-work → result, you already
understand tasks and messages.

### 3. The EventQueue & Status updates — A2A does the weightlifting

Here’s the concept that earns A2A its keep. Agents are slow — a real task can
take seconds or minutes. You don’t want to block, and you don’t want to
hand-roll streaming, polling, and reconnects for every client.

So you don’t. Your app just **posts events to an EventQueue**  — “working,”
“here’s a partial result,” “done” — and **A2A handles delivering them to the
client however and whenever the client prefers** (streaming now, or polling
later).

```python
# updater: Helper to update tasks
updater = TaskUpdater(event_queue, task_id=task.id, context_id=task.context_id)

await updater.update_status(
    TaskState.TASK_STATE_WORKING, message=new_text_message("Processing request...")
)

# my_agent.invoke: your app's logic
# (for simplicity, below code assume text input and output)
result = await my_agent.invoke(query)

await updater.add_artifact(parts=[new_text_part(text=result)])

await updater.update_status(
    TaskState.TASK_STATE_COMPLETED, message=new_text_message("Request is completed!")
)
```

Read that again from the app’s point of view: you posted three updates and an
artifact. You wrote **zero** networking code. That’s the weightlifting — A2A
manages client communication so your agents are truly interoperable and can
work across teams, services, and continents. You focus on your app and its
executions.

**Tip:** Any work that isn’t instantaneous (i.e. almost all real agent work).
Post updates as you go and let A2A meet each client where it is.

### The Complete Flow

These three aren’t separate features you choose between — they’re one flow.
Discovery (the card) tells a client how to send a message; the message becomes
a task; the task streams updates back through the EventQueue.

Get the Agent Card right and the rest composes naturally. When you later have
_many_ agents behind one host, the same card-driven discovery is what makes
routing tractable — which is exactly where Part 2 (multi-tenancy) picks up.

### Recap/ Key Takeaways

- **A2A is Docker for agents.** Wrap your app; it stays the same and gains
  interoperability. You don’t rewrite — you make portable.
- **Three concepts are the whole intro:** the **Agent Card** (discovery),
  **tasks & messages** (the request and the unit of work), and the
  **EventQueue** (async status updates).
- **A2A does the weightlifting.** You post status updates; A2A handles
  streaming/polling/reconnects so any client can keep up.
- **Discovery is the front door.** A good Agent Card makes “talk to any agent”
  literally true — and sets up everything that comes later in the series.

### Demo

**To get started with a simple hands-on-demo:**

1. A2A Server instance — Step

```shell
# To start an A2A instance
$ git clone https://github.com/a2aproject/a2a-samples.git
$ cd a2a-samples/samples/python/agents/helloworld
$ uv run .
```

2. Client instance in a new terminal

```shell
# To start an A2A instance
$ git clone https://github.com/a2aproject/a2a-samples.git
$ cd a2a-samples/samples/python/agents/helloworld
$ uv run test_client.py 
```

To learn more:

- Read the spec →
  [https://a2a-protocol.org/latest/](https://a2a-protocol.org/latest/)
- Star the project →
  [https://github.com/a2aproject/A2A](https://github.com/a2aproject/A2A)

**A question for you:** what’s the first agent you’d wrap in A2A — and which
_other_ team’s agent would you most want it to talk to? That second answer is
usually the one that proves the protocol’s worth.

______________________________________________________________________
