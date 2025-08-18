---
title: Adding a badge to your project
date: 2023-11-30
authors: [sampathm]
slug: adding-a-badge-to-your-project
description: >
  Share the love – you can now add a badge to your README, showing that your
  project is built with Material for MkDocs
categories:
  - General
---
## title: "Vibe Code? The What, Why, and How (And When to Hit the Brakes)" date: 2024-01-31

# Vibe Code? The What, Why, and How (And When to Hit the Brakes)

What is Vibe Coding? At its heart, vibe coding is about using AI to generate
code from a high-level intent or "vibe." Think of it less like a co-pilot and
more like an automated sidekick. You describe a function or a script, the AI
generates the code, and you run it. You're less focused on the syntax and more
on the desired outcome. It’s a workflow of describe-generate-run-refine.

This is a stark contrast to responsible AI-assisted development, where the
human developer remains firmly in the driver's seat, meticulously reviewing and
guiding every line of code. Vibe coding is fast, fluid, and often done with the
explicit goal of getting a quick result, sometimes with the intent to throw the
code away later.

When to Ride the Vibe 🏄 Not all projects are created equal. Vibe coding is a
superpower for the right task.

For Developers: Rapid Prototyping: Got a weekend idea for a simple web app or a
data script? Vibe code it. You can spin up a proof-of-concept in hours, not
days.

Automating Repetitive Tasks: Need a Python script to rename files or parse some
logs? A simple prompt like "write a Python function to read a CSV file" can
save you the boilerplate.

Learning a New Library: Want to see how a new library works? Ask an AI to
generate a simple example. It's like having a personalized, instant
documentation assistant.

When to Hit the Brakes 🛑 Just as a sports car is a bad choice for a family road
trip, vibe coding has its limits. This is where it gets critical for tech leads
and project managers.

For Tech Leads and Project Managers: Critical Systems: Never, ever vibe code
mission-critical or security-sensitive applications. The code generated might
have unknown flaws, and the cost of debugging or a security breach will far
outweigh the speed benefits.

Long-term Projects: If a project needs to be maintained for months or years, a
vibe-coded mess will become a nightmare. It will accumulate technical debt that
cripples the team and makes scaling impossible.

Ensuring Code Quality: Vibe-coded solutions often lack documentation,
modularity, and proper error handling. This can lead to an "entropy loop" where
every fix introduces more problems.

Common Vibe-Coding Mistakes (And How to Fix Them) The true danger isn't the
AI—it's the over-reliance on it. Here are some pitfalls to watch out for, with
actionable advice for everyone on the team.

1. The Security Trap 🔒 The Mistake: Blindly accepting AI-generated code that
   contains vulnerabilities. In one notable case, an AI assistant naively used
   eval() on user input, creating a critical arbitrary code execution
   vulnerability. Another common mistake is hardcoding API keys directly into a
   script.

   Fix: Developers, maintain a "human in the loop" mindset. Always review code
   for common security flaws like insecure input handling. Tech leads, mandate
   static analysis tools and code reviews for any AI-generated code, no matter
   how small.

1. The Technical Debt Vortex 🌪️ The Mistake: Treating a vibe-coded prototype as
   a production-ready solution. The code works, but it's a tangled mess that's
   impossible to debug or extend.

   Fix: Developers, refactor aggressively. If a prototype is promising, treat
   it as pseudo-code and rewrite it with proper structure. Project managers,
   plan for a "refactoring phase" in your sprints. The AI got you 80% there;
   now build the last, most crucial 20% responsibly.

1. The Skills Erosion 🧠 The Mistake: Over-relying on AI to the point where
   developers stop understanding the fundamentals. You lose the ability to
   debug complex issues because you never truly learned how the code works.

   Fix: Developers, use AI as a tool to explore, not a crutch to lean on.
   Always ask the AI why it made a certain choice. Tech leads, foster a culture
   of learning. Encourage pair programming and discussions on how to improve
   AI-generated code.
