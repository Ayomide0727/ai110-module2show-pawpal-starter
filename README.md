# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:


Today's Schedule
========================================
Daily plan for Biscuit (dog):
  08:00 — Morning walk (30 min) [priority: high]
  08:30 — Feeding (10 min) [priority: high]

Daily plan for Whiskers (cat):
  08:40 — Litter box cleaning (15 min) [priority: medium]


## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest

# Run with coverage:
python -m pytest --cov
```

The suite (`tests/test_pawpal.py`) covers:

- **Sorting** — `Scheduler.sort_by_time` orders tasks chronologically and pushes unscheduled tasks (`start_time=None`) to the end; `Scheduler.generate_plan` is checked end-to-end to confirm scheduled tasks come out in start-time order with the highest-priority task placed first.
- **Recurring tasks** — completing a `"daily"` task creates a new task due the next day, completing a `"weekly"` task creates one due a week later, a non-recurring task produces no follow-up, and a recurring task that was never attached to a `Pet` completes without crashing.
- **Conflict detection** — `Scheduler.check_conflicts` flags exact-duplicate start times, partial time overlaps, and overlaps across two different pets, while back-to-back (adjacent, non-overlapping) tasks and an empty schedule correctly produce no warnings.

Sample test output:

```
============================= test session starts =============================
collected 13 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  7%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 15%]
tests/test_pawpal.py::test_sort_by_time_orders_tasks_chronologically PASSED [ 23%]
tests/test_pawpal.py::test_sort_by_time_puts_unscheduled_tasks_last PASSED [ 30%]
tests/test_pawpal.py::test_generate_plan_schedules_tasks_in_chronological_start_time_order PASSED [ 38%]
tests/test_pawpal.py::test_mark_complete_on_daily_task_creates_task_for_next_day PASSED [ 46%]
tests/test_pawpal.py::test_mark_complete_on_weekly_task_creates_task_one_week_later PASSED [ 53%]
tests/test_pawpal.py::test_mark_complete_on_non_recurring_task_does_not_create_followup PASSED [ 61%]
tests/test_pawpal.py::test_mark_complete_on_recurring_task_without_pet_does_not_crash PASSED [ 69%]
tests/test_pawpal.py::test_check_conflicts_flags_overlapping_start_times PASSED [ 76%]
tests/test_pawpal.py::test_check_conflicts_flags_partial_overlap PASSED  [ 84%]
tests/test_pawpal.py::test_check_conflicts_allows_back_to_back_tasks PASSED [ 92%]
tests/test_pawpal.py::test_check_conflicts_returns_empty_when_no_tasks_scheduled PASSED [100%]

============================= 13 passed in 0.03s ==============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Priority + duration sorting | `Scheduler.generate_plan` | Sorts by priority first, then by shortest duration within a tier, so short tasks aren't starved by one long task of equal priority |
| Sort by start time | `Scheduler.sort_by_time` | Re-sorts `scheduled_tasks` by `start_time`; unscheduled tasks sort last |
| Budget filtering | `Scheduler.generate_plan` | Tasks that don't fit the remaining daily budget are routed to `skipped_tasks` with a reason |
| Task filtering | `Owner.filter_tasks` | Filters tasks across all pets by completion status and/or pet name |
| Conflict detection | `Scheduler.detect_conflicts` | Flags any two scheduled tasks whose time ranges overlap, same pet or different pets |
| Conflict warnings | `Scheduler.check_conflicts` | Lightweight, non-raising wrapper around `detect_conflicts`; returns human-readable warning strings instead of crashing |
| Recurring tasks | `Task.mark_complete` | Completing a `"daily"`/`"weekly"` task auto-creates the next occurrence, due one interval out via `timedelta` |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
