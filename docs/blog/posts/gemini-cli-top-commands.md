---
title: "Master Your Workflow: Top Gemini CLI Commands You Should Know"
description: "Master the Gemini CLI. Use AI commands in your terminal to code faster & boost productivity. Learn how."
date: 2025-10-13
authors:
  - msampathkumar
categories:
  - "AI"
  - "Development"
  - "CLI"
---

# Master Your Workflow: Top Gemini CLI Commands You Should Know

I've always been a terminal dweller. There's something uniquely satisfying about staying in the command line, but as my workflows grew, I found myself constantly context-switching—jumping to the browser to check docs, to a GUI for Git, and back. It was a focus killer.

That changed when I started integrating the Gemini CLI into my daily routine. Instead of leaving the terminal, I now have Google's AI models directly in my command line as a context-aware pair programmer. It's drastically streamlined my workflow, and I wanted to share the commands I find most useful.

## 🚀 Getting Started: The Essentials

Here are the foundational commands I use to get oriented in a new project.

*   **/init** 🎬: This is where your journey should begin. Running `/init` in your project directory allows Gemini to analyze your codebase and create a `GEMINI.md` file.

*   **/about** ℹ️: Curious about your setup? This command quickly displays your Gemini CLI version, the underlying model being used, and your current authentication method.

*   **/auth** 🔑: Security and access are paramount. The `/auth` command lets you configure how you authenticate with Google's AI services.

*   **/help & /docs** 📚: The `/help` command is your go-to for a quick overview. For more details, `/docs` opens the full documentation in your browser.

*   **/quit** 👋: When you're done for the day, simply use `/quit` to exit the Gemini CLI application.

## 🛠️ Core Workflow Commands

These are the commands you'll use day-to-day to interact with Gemini and your codebase.

*   **`!` (Shell Commands)** 🐚: This is one of the most powerful features. Press `SHIFT + 1` to enter "shell mode," allowing you to execute shell commands or describe them in natural language.

    <!-- TODO: Generate a GIF demonstrating natural language shell command, e.g., user types "list all ts files" and Gemini executes `find . -name "*.ts"` -->

*   **/tools** 🧰: Ever wonder what capabilities Gemini has? The `/tools` command lists all available tools Gemini can use to help you.

*   **/editor** ✍️: **Pro-Tip:** For complex, multi-line prompts, use `/editor` to set your preferred external editor (like Vim or VS Code), then use `Ctrl+X` to open it.

## 💬 Managing Your Conversations

A conversation with Gemini is a valuable asset. Here's how to manage it effectively.

*   **/chat (save, resume, list, delete, share)** 💾: The `/chat` command is a powerful tool for managing your session history. `save` a conversation, `resume` it later, or `share` it as a file.

    <!-- TODO: Generate a GIF demonstrating the /chat save and /chat resume workflow, showing a user saving a session and coming back to it later. -->

*   **/clear** 🧹: Need a fresh start? `/clear` will wipe the screen and your current conversation history.

*   **/compress** 🧠: When a conversation gets long, `/compress` intelligently summarizes the context to keep things focused.

## 🎨 Customization and Stats

Tailor the CLI to your liking and keep an eye on your usage.

*   **/theme** 🖌️: Customize your experience. The `/theme` command allows you to change the look and feel of the Gemini CLI.

*   **/stats** 📊: Curious about your usage? `/stats` provides statistics for your current session, including model and tool usage.

## ⌨️ Gemini CLI Keyboard Shortcuts You Should Know

To work even faster, it's worth learning a few essential keyboard shortcuts.

*   **`ESC`**: Cancel a long-running task or clear your input.
*   **`Ctrl+C`**: Quit the application (press twice).
*   **`Ctrl+X` / `Meta+Enter`**: Open your input in an external editor.
*   **`Enter`**: Send your query to Gemini.

## ✨ Common Use Cases to Try Today

Here are a few practical ideas to get you started:

*   **Quick Refactoring:** Use `@` to provide a file as context (e.g., `@src/utils.py`) and ask Gemini: "Refactor the `calculate_total` function in this file to be more readable."
*   **Commit Message Generation:** Run `!git diff --staged` and then ask Gemini: "Based on the diff, write a conventional commit message."
*   **Command-Line Coach:** Paste a complex shell command and ask: `tar -xzvf archive.tar.gz` "What do each of these flags do?"

```aiexclude
╭────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ >   tar -xzvf archive.tar.gz what does each flag do                                                                                             │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

✦ Of course. The command tar -xzvf archive.tar.gz is used to decompress and extract files from a gzipped tar archive.

  Here is a breakdown of what each flag does:

   * -x: eXtract. This tells tar to get files out of the archive.
   * -z: gZip. This tells tar to decompress the archive using gzip. This is necessary for files ending in .gz.
   * -v: Verbose. This makes tar list each file as it is being extracted, so you can see the progress.
   * -f: File. This flag must be followed by the name of the archive file you want to process (in this case, archive.tar.gz).

  You can think of the command as saying: "eXtract the gZipped contents Verbosely from the File named archive.tar.gz."
```

## Final Thoughts

Integrating these commands took a bit of muscle memory at first, but it's vastly improved how I work day-to-day. If you're also trying to maximize your terminal time, I definitely recommend giving some of these a shot. 

What does your terminal setup look like? I'm always looking for ways to optimize my workflow, so let me know if you have any favorite CLI tricks.
