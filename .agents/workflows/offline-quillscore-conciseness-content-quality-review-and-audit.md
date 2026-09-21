# Offline Quillscore Conciseness & Content Quality Review Workflow

## Purpose
Audit and improve documentation in this repo using `quillscore` and `be-concise` standards.

## When to Run
- Reviewing draft posts in `docs/writing/` or `docs/scion-cookbook/`.
- User asks for a content quality review.
- Pre-merge checks before publishing.

---

## Step 1: Pre-Flight Check
Ensure `quillscore` is available in `$PATH` (reference: [msampathkumar/quillscore](https://github.com/msampathkumar/quillscore)):
```bash
quillscore --version
```
If not installed:
```bash
pip install git+https://github.com/msampathkumar/quillscore.git
```

---

## Step 2: Baseline Quality Audit
Run `quillscore` in offline mode on the target document:
```bash
quillscore <path/to/document.md>
```

Record baseline metrics:
- **Total findings**: count of errors (E), warnings (W), and infos (I).
- **Readability grade**: target is Grade A (0 warnings).
- **Slop count**: AI cliches and buzzwords.
- **Structure findings**: broken links or relative schemes.

---

## Step 3: Apply Conciseness & Structural Refinements
Follow the `be-concise` rules:

1. **Split High-Grade Sentences**:
   - Break any sentence with reading grade > 14 into 2–3 short, active sentences.
   - Lead with subject and verb.
   - Cut introductory filler.

2. **Eliminate Zombie Nouns & Passive Voice**:
   - Use active voice.
   - Use direct verbs instead of nominalizations.

3. **Convert Walls of Text to Tables or Bullet Lists**:
   - Turn complex setup steps or configuration keys into tables.
   - Keep table cells short.

4. **Convert ASCII Art to Native Mermaid Charts**:
   - Replace ASCII box diagrams with `mermaid` fenced blocks (`graph TD`).
   - Use subgraphs for layered stacks.
   - Quote node labels containing symbols.

5. **Remove Wordy Phrasing**:
   - Replace wordy phrases with direct words.
   - Cut marketing cliches and buzzwords.

---

## Step 4: Verification & Quality Gate
Re-run `quillscore` on the modified file:
```bash
quillscore <path/to/document.md>
```

**Quality Gate Criteria**:
- Errors: **0**
- Warnings: **0**
- Readability Scorecard: **Grade A**

---

## Step 5: Document Results
Record before/after results in `review.md` or the corresponding review tracker:
- Baseline vs. final finding counts
- Summary of sections edited
- Verified readability grade
