---
title: "Proposal: Documentation-Driven Development (D3) - A New Pattern for the AI Era"
date: 2025-12-11
authors: [sampathm]
categories:
- "Documentation"
- "AI Development"
- "Google Cloud"
- "Development Patterns"
---

# Give Your AI a Brain: Context-Driven Development with Conductor for Gemini CLI
Stop coding in "YOLO Mode". Learn how to give Gemini CLI the full context of your project for better, more accurate results

**[Header Image Idea: A split screen. Left side: A messy desk with loose post-it notes labeled "YOLO Mode". Right side: A neat desk with a structured binder labeled "Conductor - CDD".]**

> "Failing to plan, is planning to fail."

Software development isn't just typing code. It’s planning, tracking, executing, testing, and iterating. For large corporate projects, we have heavyweights like Jira. But what about pet projects, POCs, or solo features? We are often stuck in the middle ground—Jira is overkill, but having zero structure leaves us vulnerable to scope creep and losing direction.

Enter the era of AI-assisted coding. If we humans need structure to stay focused, our AI tools need it even more. If you’re just firing random prompts at Gemini CLI, you are coding in "YOLO Mode." The AI has no memory of what you asked five minutes ago and no idea what the end goal is.

How do we bring structured planning to the "AI Way" of doing things?

### Introducing Conductor for Gemini CLI

Conductor is an open-source, optional extension for the Gemini CLI. It bridges the gap between unstructured prompting and full-blown project management tools.

You can think of Conductor as a lightweight project manager that lives directly inside your terminal and repository. It introduces **Context-Driven Development (CDD)** to the Gemini CLI experience.

* **Website:** [Google Developers Blog Introduction](https://developers.googleblog.com/conductor-introducing-context-driven-development-for-gemini-cli/)
* **Repo:** [GitHub (Apache-2.0 License)](https://github.com/gemini-cli-extensions/conductor)

### The "Why": Context is King

Why should you care about another tool? Because context is what separates a generic code snippet from a perfectly integrated feature.

Conductor adds a strict protocol used to specify, plan, and implement software features. By maintaining files in your repository that define the product guidelines, tech stack, and current feature specifications, Conductor ensures that every prompt you send to Gemini is automatically enriched with the bigger picture.

It stops the AI from guessing your tech stack and forces it to adhere to your agreed-upon plan.

### The "How": A Practical Walkthrough

Let's look at how Conductor actually works on a local machine.

#### Step 1: Installation

Installing Conductor is as simple as adding any other Gemini extension.

```bash
gemini extensions install https://github.com/gemini-cli-extensions/conductor

```

#### Step 2: Initialization (Giving the AI Context)

Just like you `git init` a repo, you need to initialize Conductor in your project root.

**(Recommended Screenshot/GIF: Run this command and show the output indicating files were created)**

```bash
# Start a Gemini session
gemini

# Inside the session run:
conductor init
```

As you do this, Gemini CLI works to fulfill the requirements and creates a new folder named `conductor/` populated with guideline files.

**(Recommended Screenshot: Show your iTerm file tree showing this structure)**

```
conductor/
├── product-guidelines.md  <-- How we build things here
├── product.md             <-- What this product is
├── tech-stack.md          <-- The tools we use (React, Python, etc.)
└── tracks/                <-- Where active work lives

```

These files are accessible by both you and Gemini. You should fill out `tech-stack.md` and `product.md` first. This is the baseline context Gemini will now use for *everything* in this project.

#### Step 3: The Workflow (Tracks, Specs, and Plans)

Conductor organizes work into "Tracks" (like a feature branch or a Jira ticket).

**1. Create a Track**
Let's say we want to add a chatbot feature.

**(Recommended Screenshot: The output of creating a track)**

```bash
# Setup conductor
# Note: Conductor will create a folder structure for you.
/conductor:setup

# Create a new track.
# Example: To create blog post on Quantum Physics
# Note: Conductor will ask a few follow-up questions to create a plan and an implementation track
/conductor:newTrack create blog post on Quantum Physics

# Check all open tracks for this project.
/conductor:status

# To start work on all open tracks for this project.
/conductor:implement
```

This creates a new folder structure under `conductor/tracks/chatbot_feature` containing a `spec` file.

**2. Define the Spec**
You (the human) edit the `spec` file in that folder to define *what* you want. You don't say *how* to code it, just define the requirements.

**3. Generate the Plan**
This is where the magic happens. You ask Conductor to look at your spec, your tech stack, and your product guidelines, and generate a step-by-step implementation plan.

**(Recommended Video Clip: Record the terminal as Gemini generates the plan. It's satisfying to watch it list the steps.)**

```bash
# Inside gemini session, ensuring you have the track selected
conductor plans generate

```

Gemini will generate a detailed `plan.md` file listing numbered tasks required to build your spec.

**4. Execute the Tasks**
Now, instead of randomly prompting, you tell Conductor to execute a specific step from the plan it just created.

```bash
# Inside gemini session
conductor tasks execute 1

```

Gemini now has the ultimate context: It knows the overall product goal, the specific feature spec, the exact step in the plan it needs to do, and the tech stack rules. It will write the code, and then update the plan to mark task #1 as complete.

### Conclusion

If you enjoy working with Gemini CLI, Conductor sharpens its focus significantly. It turns an AI coding assistant into an AI development partner that understands the "definition of done."

Stop YOLO prompting. Give your AI some context.

---

---

## Part 2: The YouTube Video Script

**Video Concept:** A fast-paced, "over-the-shoulder" look at using Conductor. The tone should be enthusiastic and practical.
**Estimated Duration:** 3-5 minutes.

| Time | Visual Idea | Script (Voiceover/Host) |
| --- | --- | --- |
| **0:00** | **Face to camera (or engaging terminal intro screen).** Text overlay: "AI Coding: YOLO Mode vs. God Mode" | Are you just throwing random prompts at your terminal hoping for working code? That’s coding in YOLO mode. Your AI has no memory and no context. Today, we’re fixing that. |
| **0:20** | **Screen share: Google Blog Post about Conductor.** Highlight "Context-Driven Development". | Google recently introduced "Conductor" for the Gemini CLI. It introduces "Context-Driven Development." |
| **0:35** | **Graphic:** Simple diagram showing: YOU -> (Prompts) -> GEMINI -> (Random Code?). Then change it to: YOU + CONDUCTOR FILES -> (Rich Context) -> GEMINI -> (Structured Features). | Think of Conductor as a lightweight project manager that lives right inside your repo. It forces you to define *what* you want before the AI starts guessing *how* to write it. |
| **0:55** | **Screen Share: iTerm on Macbook.** Show an empty project folder. Run the install command. | Let’s look at it in action on my local machine. Installing it is just a standard Gemini extension command. |
| **1:10** | **Screen Share: Terminal.** Run `gemini start` then `conductor init`. **Crucial: Zoom in on the file tree updating on the left.** | Once we start Gemini, we run `conductor init`. Watch the file tree on the left. Boom. |
| **1:25** | **Screen Share: Briefly open the generated markdown files in VS Code or Vim.** Point out `tech-stack.md`. | It created a `conductor` folder. This is the AI's brain for your project. You define your `tech-stack` here once, and Gemini never has to guess again. |
| **1:45** | **Screen Share: Terminal.** Run `conductor tracks create new-landing-page`. Show the new folders created. | Work happens in "Tracks". Let's create a track for a new landing page. Conductor sets up the structure for us. |
| **2:05** | **Screen Share: Briefly show the `spec` file.** Then back to terminal. Run `conductor plans generate`. **Let the recording run while Gemini types out the plan.** | I’ve put my requirements into the spec file. Now, I’ll ask Conductor to generate the plan. Look at that—it’s reading my spec, my tech stack, and creating a step-by-step checklist. |
| **2:35** | **Screen Share: Show the generated `plan.md`.** Point to task #1. Back to terminal: run `conductor tasks execute 1`. | We have a plan. Now we just execute. "Conductor, do task one." |
| **2:55** | **Screen Share: Show Gemini generating the actual code files for task 1.** | Because it has all that context, it knows exactly which files to create and what stack to use, without me having to re-explain it in the prompt. |
| **3:15** | **Face to camera.** | Conductor turns Gemini CLI from a smart autocomplete into an actual junior developer that understands your project's plan. The links to install it are in the description below. Stop YOLO coding, and give your AI some brainpower. |