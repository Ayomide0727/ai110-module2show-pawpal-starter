# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

Challenge 1: add a third algorithm beyond the basics. I had the agent propose options first and change nothing until I approved. I chose "next available slot" with an 8 PM day end, plus a UI control.

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

- `pawpal_system.py`: added `DAY_END_MINUTES` and `Scheduler.find_next_available_slot()`.
- `tests/test_pawpal.py`: added 5 tests (empty day, busy block, gap, `after`, 8 PM cutoff).
- `app.py`: added a "Find a free slot" section with a "Suggest a time" button.
- Ran pytest: 18 passing.

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

- One new test failed because the agent miscounted a gap (8:30–10:00 is exactly 90 min); the code was right, the test was fixed.
- The UI was only syntax-checked. I still need to run `streamlit run app.py` to confirm it.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | | |
| **Prompt** | | |
| **Response summary** | | |
| **What was useful** | | |
| **Problems noticed** | | |
| **Decision** | | |

**Which approach did you use in your final implementation and why?**

<!-- Your conclusion -->
