---
title: "What’s New in A2A: v1.0, a Python DX Glow-Up, and a Fresh New Look"
description: "A2A Documentations &amp; New Updates.  🎉 A2A reached v1.0 — a production-ready, open standard for..."
date: 2026-07-02
authors:
  - sampathm
categories:
  - agenticai
  - agents
  - a2aprotocol
  - a2a
canonical_url: "https://medium.com/google-cloud/whats-new-in-a2a-protocol-v1-release-b36dc6b4febd"
---

> Originally published on
> [dev.to](https://dev.to/sampathm/whats-new-in-a2a-v10-a-python-dx-glow-up-and-a-fresh-new-look-1hek)
> /
> [Medium](https://medium.com/google-cloud/whats-new-in-a2a-protocol-v1-release-b36dc6b4febd).

![](https://cdn-images-1.medium.com/max/1024/1*zB1cWExaMgqAMYapEInu4w.png) _A2A
Documentations & New Updates._

🎉 A2A reached v1.0 — a production-ready, open standard for agents to talk to
each other. It was created by Google but now it’s maintained under the **Linux
Foundation** by a Technical Steering Committee(TSC) spanning eight companies
(AWS, Cisco, Google, IBM Research, Microsoft, Salesforce, SAP, and ServiceNow).

I have been attending these TSC meetings and met Google’s Software Engineers
who are working on A2A. Based on what I saw and understood, this v1.0 is really
big news and we are planning more cool and exiting things 😀. For today let us
focus on what’s new under the hood in A2A’s v1.0, a Python (
[📦 a2a-python](https://github.com/a2aproject/a2a-python) SDK)
developer-experience glow-up worth getting excited about, and a fresh new look
on the surface to match. ✨

### What’s new in v1.0

v1.0 is about making A2A protocol **stable, standardized, and
enterprise-grade**  — and building it so the A2A SDKs can keep evolving
_without breaking everyone_ down the line. The changes group into four themes:
1️⃣ protocol maturity, 2️⃣ stronger type safety, 3️⃣ a better developer
experience, and 4️⃣ enterprise-ready features.

Here’s what’s worth your attention.

→ **Enterprise-ready security and identity.** Agent Cards can now be
cryptographically signed and verified (JWS, per RFC 7515, with JSON
Canonicalization per RFC 8785), so you can trust that an agent is who it claims
to be. OAuth 2.0 support was modernized too: the Device Code flow (RFC 8628) is
in for CLI, IoT, and headless agents, PKCE is supported, and the insecure
implicit and password flows are gone.

→ **Multi-tenancy, built in.** A native tenant field means a single endpoint
can serve multiple agents or tenants — no more bolting it on yourself.

→ **Listing that scales.** A new ListTasks operation adds filtering and
cursor-based pagination, so task listing holds up as your agents get busy.

→ **Consistent behavior across every transport.** Errors are now standardized
on google.rpc.Status / ErrorInfo, so you get the same error shape whether
you're on JSON-RPC, gRPC, or HTTP+JSON. And version negotiation via the
A2A-Version header — with the protocol version declared _per interface_ — means
a single agent can support multiple protocol versions at once. That's the
mechanism that makes graceful, backward-compatible upgrades possible.

→ **A cleaner data model.** The big one: text, file, and data are unified into
a single Part type — no more separate TextPart / FilePart / DataPart, and no
kind discriminator to carry around. Enum values are standardized to
SCREAMING_SNAKE_CASE for ProtoJSON compliance, timestamps are ISO-8601 with
milliseconds, and tasks now carry createdAt / lastModified. IDs are simple
UUIDs (no compound tasks/{id}), and the /v1 HTTP path prefix is gone.

**Straight talk:** yes, several of these are breaking changes. v1.0 is a
genuine version bump, not a coat of paint. The payoff is a protocol that’s
stable, standardized, and designed so that _future_ versions won’t keep
breaking your integrations.

Want more details? Three links cover it: the
[What’s new in v1.0](https://a2a-protocol.org/latest/whats-new-v1/) guide (five
minutes to find out if anything affects you), the
[full specification](https://a2a-protocol.org/latest/specification/) for the
canonical reference, and — if you’re on Python — the
[v1.0 migration guide](https://github.com/a2aproject/a2a-python/blob/main/docs/migrations/v1_0/README.md).
Stuck on something? The community hangs out in
[GitHub Discussions](https://github.com/a2aproject/A2A/discussions) — a good
place to ask.

### Provably interoperable — the Integration Test Kit

The whole promise of A2A is that agents built by different teams, in different
languages, actually interoperate — and the **A2A Integration Test Kit (ITK)**
is how that gets _proven_ rather than asserted. If you ship across SDKs or
languages, the
[public ITK dashboard](https://a2aproject.github.io/a2a-itk/dashboard) shows
you which combinations are known-good — a daily snapshot of nightly cross-SDK
runs (not a live or real-time view). For the full story on how it works, the
[ITK dashboard deep-dive](https://dev.to/sampathm/breaking-down-agent-silos-the-a2a-integration-test-kit-dashboard-is-here-4m60)
covers it.

![](https://cdn-images-1.medium.com/max/1024/0*fyG15BKvFPR7rpBO.png)
_https://a2aproject.github.io/a2a-itk/dashboard/_

### The Python DX glow-up

Here’s the part I’m genuinely excited about. v1.0 didn’t just tighten the
protocol — it gave the Python SDK a real developer-experience glow-up, and most
of it lives in one new module: **a2a.helpers**.

Instead of hunting through scattered a2a.utils.\* imports, you get a single
consolidated import with friendly factory functions for the things you do all
day: building messages, parts, tasks, and artifacts (new_text_message,
new_task, new_text_artifact, …); creating the status and artifact **update
events** you enqueue while streaming (new_text_status_update_event,
new_text_artifact_update_event, plus data/raw/url variants); and pulling
content back out (get_message_text, get_text_parts, get_stream_response_text).
One import, far less boilerplate.

The before/after says it best — and spinning up a client got the same
treatment, with create_client() (from a2a.client) collapsing the old
ClientFactory dance into a single await:

```python
##############################################################
# Before — v0.3: wrapper types by hand, and a client factory
##############################################################
message = Message(role=Role.user, parts=[Part(TextPart(text="hi"))])

factory = ClientFactory()
client = factory.create_client(url)

##############################################################
# After - v1.0: one helper each
##############################################################
from a2a.helpers import new_text_message
from a2a.client import create_client

message = new_text_message("hi", role=Role.ROLE_USER)
client = await create_client(url)
```

That’s the flavor of the whole release: fewer wrapper types, fewer lines, less
to remember. **Upgrading an existing agent?** The
[v1.0 migration guide](https://github.com/a2aproject/a2a-python/blob/main/docs/migrations/v1_0/README.md)
walks you through it — and you can run a v1.0 server with v0.3 compatibility
enabled, so you don’t have to migrate every client at once.

### A fresh look to match

A milestone like this deserves a face — so the parts you see first got
attention too.

**A friendlier home.** [a2a-protocol.org](https://a2a-protocol.org/) has a
redesigned home page and navigation, reorganized around one question: _what do
you want to do next?_ Less overwhelming, easier to find your starting
point — whether that’s a five-minute “what is A2A?”, the full spec, or the
hands-on Python tutorial.

[**# New Homepage**](https://a2a-protocol.org/latest/)\
At the top of the home page, we’ve added _Get started_ and _Read the spec_
buttons, allowing you to instantly jump straight to the resources you need
based on your immediate goals.

![](https://cdn-images-1.medium.com/max/1024/1*IF8Z6Rxmh0rxExesN99dFw.png) _A2A
Home Page — https://a2a-protocol.org/latest/_

[**# Restructured Navigation**](https://github.com/a2aproject/A2A/blob/main/mkdocs.yml#L20)\
We’ve reorganized our previous layout into highly focused, grouped sections,
making it effortless to pinpoint your specific topic of interest and dive right
into development.

![](https://cdn-images-1.medium.com/max/1024/1*NiFeCGWHqkXE62WlB9UqAw.png)
_A2A — restructured navigation_

[**# New A2A logo**](https://a2a-protocol.org/latest/assets/a2a_logo/color/SVG/a2a_color.svg)\
A cleaner, more consistent mark across the docs, the repo, and everywhere A2A
shows up.

![](https://cdn-images-1.medium.com/max/1024/0*8zOfs1t1-z8hdOtq.png) _A2A New
Logo_

[**# Lastly, our new A2A Mascot**](https://github.com/a2aproject/A2A/blob/main/docs/assets/a2a_logo/mascot/PNG/a2a_ada.png)

A2A now has one: a friendly orange-and-cream, a puppy — sitting, tongue out,
wearing a collar with an “A2A” dog tag. It’s the warmth a spec and a governance
doc can’t quite carry on their own: approachable, a little playful, and
(fittingly for an interoperability protocol) happy to make friends with anyone.

The protocol is grown-up and production-ready; the project should still feel
like somewhere you’d want to hang out and contribute.

![](https://cdn-images-1.medium.com/max/1024/1*t0kgsULhkHiOqmm9OVn3mQ.png) _A2A
Mascot_

### Coming next

One more thing worth flagging: the next post digs into **A2A multi-tenancy**
— how the native tenant model dramatically simplifies building multi-agent
applications, letting a single deployment serve many agents and tenants
cleanly. If you’re building anything beyond a single agent, it’ll be worth your
time. More soon.

### What to do next

- **To see what changed,** check
  [_What’s new in v1.0_](https://a2a-protocol.org/latest/whats-new-v1/)
  guide — five minutes to find out if anything affects you.
- **Need to upgrade your Python A2A Agent?** Start with the
  [migration guide](https://github.com/a2aproject/a2a-python/blob/main/docs/migrations/v1_0/README.md) — and
  remember you can run a v1.0 server with v0.3 compatibility while you
  transition.
- **To check inter-op for A2A app,** start with
  [ITK compatibility dashboard](https://a2aproject.github.io/a2a-itk/dashboard).

> **Community Request:** We are actively looking to grow our A2A community and
> expand our A2A blog content. If you have ideas, feedback, or unique insights,
> your suggestions are incredibly welcome!

______________________________________________________________________
