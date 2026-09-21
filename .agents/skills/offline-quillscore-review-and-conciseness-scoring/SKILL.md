---
name: offline-quillscore-review-and-conciseness-scoring
description: Audit, grade, and improve technical documentation, blog posts, and markdown guides using the offline quillscore CLI and be-concise principles.
---

# Offline Quillscore Review & Conciseness Scoring Skill

## Overview
This skill grades technical documentation using the offline `quillscore` tool. It ensures Grade A readability, zero warnings, and clean formatting.

## Prerequisites
Ensure the `quillscore` CLI is installed and available in `$PATH` (source: [msampathkumar/quillscore](https://github.com/msampathkumar/quillscore)):
```bash
quillscore --version
```

## Audit Procedure

1. **Deterministic Run**:
   ```bash
   quillscore <file.md>
   ```

2. **Evaluate Severity Categories**:
   - **Readability**: Flesch-Kincaid reading grade. Sentences with grade > 14 need splitting and simpler words.
   - **Slop**: Flagged buzzwords and cliches. Remove or replace them with plain words.
   - **Structure**: Verify relative and cross-document markdown links.

3. **Apply `be-concise` Rules**:
   - Prefer active voice over passive voice.
   - Replace zombie nouns with direct verbs (for example, `analyze` instead of `conduct analysis`).
   - Cut introductory filler.
   - Break long paragraphs into structured tables or concise bullet lists.
   - Replace ASCII architecture boxes with MkDocs-compatible `mermaid` charts (`graph TD`).

4. **Verify Quality Gate**:
   Run `quillscore <file.md>` again. Target:
   - 0 errors
   - 0 warnings
   - Readability Grade: **A**

5. **Report Generation**:
   Summarize before/after metrics in `review.md`.
