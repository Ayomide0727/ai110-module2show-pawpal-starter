"""
PawPal+ system classes.

Core implementation matching diagrams/uml.mmd.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import time

# Priority ranking used for sorting; lower number = scheduled first.
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# The day is assumed to start at 8:00 AM when tasks begin being placed.
DAY_START_MINUTES = 8 * 60


def _minutes_to_time(total_minutes: int) -> time:
    """Convert minutes-since-midnight into a `time` object (wraps past 24h)."""
    hours, minutes = divmod(total_minutes % (24 * 60), 60)
    return time(hour=hours, minute=minutes)


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

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


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


@dataclass
class Scheduler:
    """Builds a daily plan for a pet's tasks given an owner's constraints."""

    scheduled_tasks: list[Task] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)

    def generate_plan(self, owner: Owner) -> None:
        """Sort the owner's tasks by priority and schedule as many as fit in the day's budget."""
        self.scheduled_tasks = []
        self.skipped_tasks = []

        sorted_tasks = sorted(
            owner.get_all_tasks(),
            key=lambda t: PRIORITY_ORDER.get(t.priority, len(PRIORITY_ORDER)),
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

        return "\n".join(lines).rstrip()
