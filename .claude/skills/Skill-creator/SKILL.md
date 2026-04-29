---
name: skill-creator
description: Create new skills, modify and improve existing skills, and measure skill performance. Use when users want to create a skill from scratch, edit, or optimize an existing skill, run evals to test a skill, benchmark skill performance with variance analysis, or optimize a skill's description for better triggering accuracy.
---

# Skill Creator

A skill for creating new skills and iteratively improving them.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Help the user evaluate the results both qualitatively and quantitatively
  - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them). Then explain them to the user (or if they already existed, explain the ones that already exist)
  - Use the `eval-viewer/generate_review.py` script to show the user the results for them to look at, and also let them look at the quantitative metrics
- Rewrite the skill based on feedback from the user's evaluation of the results (and also if there are any glaring flaws that become apparent from the quantitative benchmarks)
- Repeat until you're satisfied
- Expand the test set and try again at larger scale

Your job when using this skill is to figure out where the user is in this process and then jump in and help them progress through these stages.

## Communicating with the user

Pay attention to context cues to understand how to phrase your communication. In the default case:
- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. Should we set up test cases to verify the skill works?

### Write the SKILL.md

Components:
- **name**: Skill identifier
- **description**: When to trigger, what it does. Make descriptions a little "pushy" — include both what the skill does AND specific contexts. Counter Claude's tendency to undertrigger.
- **the rest of the skill**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

1. **Metadata** (name + description) — Always in context (~100 words)
2. **SKILL.md body** — In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** — As needed (unlimited)

#### Writing Patterns

- Use imperative form in instructions
- Explain the **why** behind everything — today's LLMs are smart enough to apply reasoning
- Try to make the skill general, not super-narrow to specific examples
- If you find yourself writing ALWAYS/NEVER in all caps, reframe and explain the reasoning instead

---

## Running and evaluating test cases

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Organize by iteration (`iteration-1/`, `iteration-2/`, etc.).

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents simultaneously — one with the skill, one without.

### Step 2: While runs are in progress, draft assertions

Draft quantitative assertions for each test case. Good assertions are objectively verifiable with descriptive names.

Save to `evals/evals.json`:
```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for full schema.

### Step 3: Grade, aggregate, and launch the viewer

```bash
python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
```

**GENERATE THE EVAL VIEWER *BEFORE* evaluating inputs yourself:**
```bash
nohup python <skill-creator-path>/eval-viewer/generate_review.py \
  <workspace>/iteration-N \
  --skill-name "my-skill" \
  --benchmark <workspace>/iteration-N/benchmark.json \
  > /dev/null 2>&1 &
```

For iteration 2+, add `--previous-workspace <workspace>/iteration-<N-1>`.

In headless environments, use `--static <output_path>` instead.

---

## Improving the skill

### How to think about improvements

1. **Generalize from the feedback** — skills must work across millions of uses, not just your test cases
2. **Keep the prompt lean** — remove things not pulling their weight
3. **Explain the why** — LLMs are smart; give them reasoning, not rigid rules
4. **Bundle repeated work** — if all test cases independently wrote the same helper script, bundle it

---

## Description Optimization

After creating or improving a skill, offer to optimize the description for better triggering accuracy.

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

---

## Package and Present

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

---

## Reference files

- `agents/grader.md` — How to evaluate assertions against outputs
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another
- `references/schemas.md` — JSON structures for evals.json, grading.json, etc.
