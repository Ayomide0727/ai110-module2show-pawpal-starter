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

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
