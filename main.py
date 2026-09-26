"""
Quick manual demo for PawPal+.

Creates an owner with two pets, gives each pet a few tasks, and prints the
scheduler's plan for each pet to the terminal.
"""

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Jordan", available_minutes_per_day=60)

    biscuit = Pet(name="Biscuit", species="dog")
    whiskers = Pet(name="Whiskers", species="cat")
    owner.add_pet(biscuit)
    owner.add_pet(whiskers)

    biscuit.add_task(Task(title="Morning walk", duration_minutes=30, priority="high"))
    biscuit.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))
    whiskers.add_task(Task(title="Litter box cleaning", duration_minutes=15, priority="medium"))

    print("Today's Schedule")
    print("=" * 40)

    scheduler = Scheduler()
    scheduler.generate_plan(owner)
    print(scheduler.explain())


if __name__ == "__main__":
    main()
