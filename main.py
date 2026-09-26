"""
Quick manual demo for PawPal+.

Creates an owner with two pets, gives each pet a few tasks (added out of
order to make the scheduler's sorting and filtering visible), then prints:
  - the scheduler's plan for each pet
  - the scheduled tasks re-sorted by start time (after being shuffled)
  - tasks filtered by completion status and/or pet name
  - a forced same-time conflict between two pets' tasks, and the warning
    the Scheduler prints for it instead of crashing
"""

import random
from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan", available_minutes_per_day=60)

    biscuit = Pet(name="Biscuit", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    # Tasks added out of priority/duration order on purpose.
    biscuit.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    whiskers.add_task(Task(title="Litter box cleaning", duration_minutes=15, priority="medium"))
    biscuit.add_task(Task(title="Morning walk", duration_minutes=30, priority="high"))
    whiskers.add_task(Task(title="Play session", duration_minutes=10, priority="low"))
    biscuit.add_task(Task(title="Evening brush", duration_minutes=5, priority="low"))

    print("Today's Schedule")
    print("=" * 40)

    scheduler = Scheduler()
    scheduler.generate_plan(owner)
    print(scheduler.explain())

    print()
    print("Sorted by start time (after shuffling)")
    print("=" * 40)
    random.shuffle(scheduler.scheduled_tasks)
    scheduler.sort_by_time()
    for task in scheduler.scheduled_tasks:
        time_str = task.start_time.strftime("%H:%M") if task.start_time else "??:??"
        print(f"  {time_str} — {task.pet_name}: {task.title}")

    # Mark a couple of tasks complete to exercise filter_tasks().
    biscuit.tasks[0].mark_complete()
    whiskers.tasks[0].mark_complete()

    print()
    print("Completed tasks")
    print("=" * 40)
    for task in owner.filter_tasks(completed=True):
        print(f"  {task.pet_name}: {task.title}")

    print()
    print("Incomplete tasks for Biscuit")
    print("=" * 40)
    for task in owner.filter_tasks(completed=False, pet_name="Biscuit"):
        print(f"  {task.pet_name}: {task.title}")

    # Force two different pets' tasks onto the same start time, simulating a
    # manual edit, to verify the Scheduler detects it and warns instead of crashing.
    print()
    print("Forcing a same-time conflict (Biscuit's Feeding vs Whiskers' Litter box cleaning)")
    print("=" * 40)
    biscuit.edit_task(biscuit.tasks[0].id, {"start_time": time(8, 0)})
    whiskers.edit_task(whiskers.tasks[0].id, {"start_time": time(8, 0)})
    scheduler.conflict_warnings = scheduler.check_conflicts()
    if scheduler.conflict_warnings:
        for warning in scheduler.conflict_warnings:
            print(f"  {warning}")
    else:
        print("  No conflicts detected.")

    print()
    print("Plan after the conflict (see the Conflicts section)")
    print("=" * 40)
    print(scheduler.explain())


if __name__ == "__main__":
    main()
