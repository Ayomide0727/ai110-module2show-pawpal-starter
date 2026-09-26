"""
PawPal+ system classes.

Core implementation matching diagrams/uml.mmd.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import date, time, timedelta

# Priority ranking used for sorting; lower number = scheduled first.
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# The day is assumed to start at 8:00 AM when tasks begin being placed.
DAY_START_MINUTES = 8 * 60

# How far out the next occurrence of a recurring task is due.
RECURRENCE_INTERVALS = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}


def _minutes_to_time(total_minutes: int) -> time:
    """Convert minutes-since-midnight into a `time` object (wraps past 24h)."""
    hours, minutes = divmod(total_minutes % (24 * 60), 60)
    return time(hour=hours, minute=minutes)


def _time_to_minutes(t: time) -> int:
    """Convert a `time` object into minutes-since-midnight."""
    return t.hour * 60 + t.minute


@dataclass
class Task:
    """A single pet care task (walk, feeding, meds, grooming, enrichment, etc.)."""

    title: str
    duration_minutes: int
    priority: str  # "low" | "medium" | "high"
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    start_time: time | None = None
    reason: str = ""
    pet_name: str = ""
    pet_species: str = ""
    completed: bool = False
    recurrence: str | None = None  # None | "daily" | "weekly"
    due_date: date | None = None
    # Back-reference to the owning Pet, set by Pet.add_task(); lets a recurring
    # task re-enroll itself without callers having to remember to do so.
    _pet: Pet | None = field(default=None, repr=False, compare=False)

    def mark_complete(self) -> None:
        """Mark this task as completed. If it's a recurring ("daily"/"weekly") task
        attached to a pet, automatically create and enroll the next occurrence, due
        one interval (a day or a week) from today."""
        self.completed = True
        interval = RECURRENCE_INTERVALS.get(self.recurrence)
        if interval is not None and self._pet is not None:
            next_task = Task(
                title=self.title,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                recurrence=self.recurrence,
                due_date=date.today() + interval,
            )
            self._pet.add_task(next_task)


@dataclass
class Pet:
    """A pet and the care tasks associated with it."""

    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet, tagging it with the pet's name and species."""
        task.pet_name = self.name
        task.pet_species = self.species
        task._pet = self
        self.tasks.append(task)

    def edit_task(self, task_id: str, changes: dict) -> None:
        """Apply attribute changes to the task with the given id."""
        for task in self.tasks:
            if task.id == task_id:
                for key, value in changes.items():
                    setattr(task, key, value)
                return
        raise ValueError(f"No task with id {task_id!r} found on {self.name!r}")


@dataclass
class Owner:
    """The pet owner using the app."""

    name: str
    available_minutes_per_day: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Flatten tasks across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def filter_tasks(
        self, completed: bool | None = None, pet_name: str | None = None
    ) -> list[Task]:
        """Return tasks across all pets matching the given completion status and/or pet name."""
        tasks = self.get_all_tasks()
        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        if pet_name is not None:
            tasks = [task for task in tasks if task.pet_name == pet_name]
        return tasks


@dataclass
class Scheduler:
    """Builds a daily plan for a pet's tasks given an owner's constraints."""

    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)
    conflict_warnings: list[str] = field(default_factory=list)

    def generate_plan(self, owner: Owner) -> None:
        """Sort the owner's tasks by priority (ties broken by shorter duration first) and
        schedule as many as fit in the day's budget."""
        self.scheduled_tasks = []
        self.skipped_tasks = []

        sorted_tasks = sorted(
            owner.get_all_tasks(),
            key=lambda t: (
                PRIORITY_ORDER.get(t.priority, len(PRIORITY_ORDER)),
                t.duration_minutes,
            ),
        )

        remaining_minutes = owner.available_minutes_per_day
        cursor_minutes = DAY_START_MINUTES

        for task in sorted_tasks:
            if task.duration_minutes <= remaining_minutes:
                task.start_time = _minutes_to_time(cursor_minutes)
                task.reason = (
                    f"Scheduled ({task.priority} priority) with "
                    f"{remaining_minutes} min remaining in the day's budget."
                )
                self.scheduled_tasks.append(task)
                cursor_minutes += task.duration_minutes
                remaining_minutes -= task.duration_minutes
            else:
                task.start_time = None
                task.reason = (
                    f"Skipped: needs {task.duration_minutes} min but only "
                    f"{remaining_minutes} min remain in the day's budget."
                )
                self.skipped_tasks.append(task)

        self.conflict_warnings = self.check_conflicts()

    def sort_by_time(self) -> None:
        """Sort scheduled tasks in place by start time (unscheduled tasks sort last)."""
        self.scheduled_tasks.sort(
            key=lambda t: t.start_time if t.start_time is not None else time.max
        )

    def detect_conflicts(self) -> list[tuple[Task, Task]]:
        """Return pairs of scheduled tasks whose time ranges overlap, whether they
        belong to the same pet or different pets — an owner can't be in two places
        (or doing two tasks) at once regardless of which pet each task is for."""
        conflicts: list[tuple[Task, Task]] = []
        timed_tasks = sorted(
            (t for t in self.scheduled_tasks if t.start_time is not None),
            key=lambda t: _time_to_minutes(t.start_time),
        )

        for i, task_a in enumerate(timed_tasks):
            a_start = _time_to_minutes(task_a.start_time)
            a_end = a_start + task_a.duration_minutes
            for task_b in timed_tasks[i + 1 :]:
                b_start = _time_to_minutes(task_b.start_time)
                if b_start >= a_end:
                    break  # sorted by start time, so no later task can overlap either
                conflicts.append((task_a, task_b))

        return conflicts

    def check_conflicts(self) -> list[str]:
        """Lightweight conflict check: never raises. Returns a human-readable warning
        string for each overlapping pair of scheduled tasks, or an empty list if the
        plan is clean or something goes wrong while checking."""
        try:
            conflicts = self.detect_conflicts()
        except Exception as exc:  # a bad conflict check should never crash the app
            return [f"Warning: could not check for scheduling conflicts ({exc})."]

        warnings: list[str] = []
        for task_a, task_b in conflicts:
            label_a = f"{task_a.pet_name}: {task_a.title}" if task_a.pet_name else task_a.title
            label_b = f"{task_b.pet_name}: {task_b.title}" if task_b.pet_name else task_b.title
            warnings.append(
                f"Warning: '{label_a}' ({task_a.start_time.strftime('%H:%M')}) overlaps "
                f"with '{label_b}' ({task_b.start_time.strftime('%H:%M')})."
            )
        return warnings

    def explain(self) -> str:
        """Return a human-readable summary of the most recent plan."""
        if not self.scheduled_tasks and not self.skipped_tasks:
            return "No plan has been generated yet."

        lines: list[str] = []
        groups: dict[tuple[str, str], list[Task]] = {}
        for task in self.scheduled_tasks:
            groups.setdefault((task.pet_name, task.pet_species), []).append(task)

        for (pet_name, species), tasks in groups.items():
            label = f"{pet_name} ({species})" if species else pet_name
            lines.append(f"Daily plan for {label}:")
            for task in tasks:
                time_str = task.start_time.strftime("%H:%M") if task.start_time else "??:??"
                lines.append(
                    f"  {time_str} — {task.title} ({task.duration_minutes} min) "
                    f"[priority: {task.priority}]"
                )
            lines.append("")

        if self.skipped_tasks:
            lines.append("Skipped:")
            for task in self.skipped_tasks:
                pet_label = f"{task.pet_name} — " if task.pet_name else ""
                lines.append(f"  {pet_label}{task.title}: {task.reason}")
            lines.append("")

        if self.conflict_warnings:
            lines.append("Conflicts:")
            for warning in self.conflict_warnings:
                lines.append(f"  {warning}")

        return "\n".join(lines).rstrip()
