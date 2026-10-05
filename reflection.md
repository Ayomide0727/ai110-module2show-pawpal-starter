# PawPal+ Project Reflection

## 1. System Design

**Core Actions**
- Add a pet
- See today's tasks
- edit tasks

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

- **Owner** — represents the pet owner using the app. Holds the owner's name, the list of `Pet` objects they own, and how many minutes per day they have available for pet care. Its responsibility is just to hold owner-level info and let pets be added (`add_pet`).
- **Pet** — represents a single pet and the tasks tied to it (name, species, and a list of `Task` objects). Responsible for managing that list — adding new tasks and editing existing ones (`add_task`, `edit_task`).
- **Task** — represents one pet care activity (title, duration in minutes, priority, and once scheduled, a start time and a reason explaining why it was placed there). It's a simple data holder with no behavior of its own — all the decision-making happens elsewhere.
- **Scheduler** — the engine that takes a `Pet` and `Owner` and produces a daily plan. It holds the resulting `scheduled_tasks` and `skipped_tasks`, generates the plan (`generate_plan`), and explains the reasoning behind it (`explain`).

I kept the design to four classes on purpose: `Owner` and `Pet` model who/what the plan is for, `Task` models the unit of work being scheduled, and `Scheduler` is the one class responsible for the actual scheduling logic and its justification. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

 Yes. `Task` was missing a unique `id`, so `edit_task` had no reliable way to find a specific task (matching by title would break with duplicate names).

**Change:** Added `id: str` to `Task`, auto-generated with `uuid.uuid4().hex`.

**Why:** `edit_task` needs a stable key that doesn't depend on task content, since content is exactly what it changes.
---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

The scheduler always fills the day's budget strictly in priority order (high, then medium, then low), rather than searching for the combination of tasks that fits the most total tasks or minutes into the day. A single large high-priority task can "starve" several smaller low-priority tasks that would otherwise have fit.

This is reasonable because priority is meant to reflect real urgency (e.g., meds vs. optional playtime) — a pet owner would rather see the important task guaranteed a slot than have the scheduler silently reorder for efficiency. The one place efficiency does matter, sorting by duration as a tiebreaker within the same priority tier, is still respected, so short same-priority tasks aren't starved by a long one.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI alot for refactoring and debugging also for when i am trying to understand an implementation some of the propmts i used are "how can i improve this app" or " help me implement core features"

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

I known that AI can complicate simple task so most time i make sure to tell it to only implement what i ask for with no external features

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?

  Sorting (`sort_by_time` orders scheduled tasks chronologically and pushes unscheduled ones last), recurring tasks (completing a daily/weekly task creates the correct follow-up, a non-recurring task doesn't, and a recurring task with no pet attached doesn't crash), and conflict detection (exact-duplicate start times, partial overlaps, overlaps across two different pets, and confirming back-to-back tasks and an empty schedule produce no false warnings).

- Why were these tests important?

  These are the behaviors most likely to silently produce a wrong plan instead of an obvious crash — if sorting or conflict detection had an off-by-one error, the app would still run and show a schedule, just a wrong one, so I needed tests that would catch that instead of relying on eyeballing the output.

**b. Confidence**

- How confident are you that your scheduler works correctly?

  Fairly confident for the paths I tested (13 passing tests covering sorting, recurrence, and conflicts) and for the manual walkthrough in `main.py`, but less confident about combinations I haven't exercised together, like recurrence interacting with a skipped (not scheduled) task.

- What edge cases would you test next if you had more time?

  Two tasks tied on both priority and duration, a task whose scheduled time wraps past midnight, editing a task's time after the plan was already generated, and an owner with zero available minutes.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
  
  Working with the AI to improve the secheduler and also debugging at each steps to ensure it is working well

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve the general ui of the app to make it more easy to use

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
 
 Working with AI can be overwhelming and you have to make sure you are in control of the implemation it is making 
