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

### UI features

The Streamlit app (`app.py`) lets a user:

- Enter owner info (name, available minutes per day) and pet info (name, species)
- Add tasks to the active pet with a title, duration, and priority (low/medium/high)
- View the current task list in a table before scheduling
- Generate a daily schedule with one click
- See the resulting plan broken out into a scheduled-tasks table, a skipped-tasks section (with the reason each was skipped), and a conflict-check section that reports overlapping tasks or confirms the plan is clear
- Expand a "Full explanation" section for the same plain-text summary `Scheduler.explain()` produces

### Example workflow

1. Add a pet (e.g., "Biscuit," a dog) under Owner & Pet.
2. Add a task ("Morning walk," 30 min, high priority), then add a couple more tasks with varying durations and priorities.
3. Click **Generate schedule**.
4. View today's schedule — tasks appear sorted by start time, with any tasks that didn't fit the daily budget listed separately.
5. Check the conflict-check section — if two tasks were assigned overlapping times, each overlap is called out individually; otherwise a confirmation message shows the plan is conflict-free.

### Key Scheduler behaviors shown

- **Priority + duration sorting** — `generate_plan` schedules high-priority tasks first, breaking ties by shorter duration.
- **Sorting by time** — `sort_by_time` re-orders the plan chronologically for display, regardless of the order tasks were scheduled in.
- **Budget filtering** — tasks that don't fit the owner's remaining daily minutes are routed to `skipped_tasks` with a reason instead of silently dropped.
- **Conflict warnings** — `check_conflicts` detects overlapping start times (even across different pets) and returns a human-readable warning for each one instead of raising an error.
- **Recurrence** — completing a daily/weekly task (via `mark_complete`) automatically enrolls its next occurrence.

### Sample CLI output (`python main.py`)

```
Today's Schedule
========================================
Daily plan for Biscuit (dog):
  08:00 — Feeding (10 min) [priority: high]
  08:10 — Morning walk (30 min) [priority: high]
  08:55 — Evening brush (5 min) [priority: low]

Daily plan for Whiskers (cat):
  08:40 — Litter box cleaning (15 min) [priority: medium]

Skipped:
  Whiskers — Play session: Skipped: needs 10 min but only 0 min remain in the day's budget.

Sorted by start time (after shuffling)
========================================
  08:00 — Biscuit: Feeding
  08:10 — Biscuit: Morning walk
  08:40 — Whiskers: Litter box cleaning
  08:55 — Biscuit: Evening brush

Completed tasks
========================================
  Biscuit: Feeding
  Whiskers: Litter box cleaning

Incomplete tasks for Biscuit
========================================
  Biscuit: Morning walk
  Biscuit: Evening brush

Forcing a same-time conflict (Biscuit's Feeding vs Whiskers' Litter box cleaning)
========================================
  Warning: 'Biscuit: Feeding' (08:00) overlaps with 'Whiskers: Litter box cleaning' (08:00).
  Warning: 'Whiskers: Litter box cleaning' (08:00) overlaps with 'Biscuit: Morning walk' (08:10).

Plan after the conflict (see the Conflicts section)
========================================
Daily plan for Biscuit (dog):
  08:00 — Feeding (10 min) [priority: high]
  08:10 — Morning walk (30 min) [priority: high]
  08:55 — Evening brush (5 min) [priority: low]

Daily plan for Whiskers (cat):
  08:00 — Litter box cleaning (15 min) [priority: medium]

Skipped:
  Whiskers — Play session: Skipped: needs 10 min but only 0 min remain in the day's budget.

Conflicts:
  Warning: 'Biscuit: Feeding' (08:00) overlaps with 'Whiskers: Litter box cleaning' (08:00).
  Warning: 'Whiskers: Litter box cleaning' (08:00) overlaps with 'Biscuit: Morning walk' (08:10).
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->