from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Biscuit", species="dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high"))

    assert len(pet.tasks) == 1


# --- Sorting correctness -----------------------------------------------------


def test_sort_by_time_orders_tasks_chronologically():
    scheduler = Scheduler()
    scheduler.scheduled_tasks = [
        Task(title="Evening walk", duration_minutes=20, priority="low", start_time=time(18, 0)),
        Task(title="Breakfast", duration_minutes=10, priority="high", start_time=time(8, 0)),
        Task(title="Lunch", duration_minutes=15, priority="medium", start_time=time(12, 30)),
    ]

    scheduler.sort_by_time()

    assert [t.title for t in scheduler.scheduled_tasks] == [
        "Breakfast",
        "Lunch",
        "Evening walk",
    ]


def test_sort_by_time_puts_unscheduled_tasks_last():
    scheduler = Scheduler()
    scheduled = Task(title="Feeding", duration_minutes=10, priority="high", start_time=time(9, 0))
    unscheduled = Task(title="Grooming", duration_minutes=45, priority="low", start_time=None)
    scheduler.scheduled_tasks = [unscheduled, scheduled]

    scheduler.sort_by_time()

    assert [t.title for t in scheduler.scheduled_tasks] == ["Feeding", "Grooming"]


def test_generate_plan_schedules_tasks_in_chronological_start_time_order():
    owner = Owner(name="Jamie", available_minutes_per_day=90)
    pet = Pet(name="Biscuit", species="dog")
    owner.add_pet(pet)
    pet.add_task(Task(title="Walk", duration_minutes=30, priority="low"))
    pet.add_task(Task(title="Meds", duration_minutes=5, priority="high"))
    pet.add_task(Task(title="Play", duration_minutes=20, priority="medium"))

    scheduler = Scheduler()
    scheduler.generate_plan(owner)

    start_times = [t.start_time for t in scheduler.scheduled_tasks]
    assert start_times == sorted(start_times)
    # Highest priority (Meds) should be placed first in the day.
    assert scheduler.scheduled_tasks[0].title == "Meds"


# --- Recurrence logic ---------------------------------------------------------


def test_mark_complete_on_daily_task_creates_task_for_next_day():
    pet = Pet(name="Biscuit", species="dog")
    daily_task = Task(
        title="Give medicine",
        duration_minutes=5,
        priority="high",
        recurrence="daily",
        due_date=date.today(),
    )
    pet.add_task(daily_task)

    daily_task.mark_complete()

    assert len(pet.tasks) == 2
    new_task = pet.tasks[-1]
    assert new_task is not daily_task
    assert new_task.completed is False
    assert new_task.recurrence == "daily"
    assert new_task.due_date == date.today() + timedelta(days=1)
    assert new_task.title == daily_task.title
    assert new_task.pet_name == "Biscuit"


def test_mark_complete_on_weekly_task_creates_task_one_week_later():
    pet = Pet(name="Whiskers", species="cat")
    weekly_task = Task(
        title="Grooming",
        duration_minutes=30,
        priority="medium",
        recurrence="weekly",
        due_date=date.today(),
    )
    pet.add_task(weekly_task)

    weekly_task.mark_complete()

    new_task = pet.tasks[-1]
    assert new_task.due_date == date.today() + timedelta(weeks=1)


def test_mark_complete_on_non_recurring_task_does_not_create_followup():
    pet = Pet(name="Biscuit", species="dog")
    one_off = Task(title="Vet visit", duration_minutes=60, priority="high")
    pet.add_task(one_off)

    one_off.mark_complete()

    assert len(pet.tasks) == 1


def test_mark_complete_on_recurring_task_without_pet_does_not_crash():
    # A recurring task built directly, never enrolled via Pet.add_task.
    orphan_task = Task(
        title="Feeding", duration_minutes=10, priority="high", recurrence="daily"
    )

    orphan_task.mark_complete()

    assert orphan_task.completed is True  # no exception, no follow-up created


# --- Conflict detection --------------------------------------------------------


def test_check_conflicts_flags_overlapping_start_times():
    pet_a = Pet(name="Biscuit", species="dog")
    pet_b = Pet(name="Whiskers", species="cat")
    task_a = Task(title="Walk", duration_minutes=30, priority="high", start_time=time(9, 0))
    task_b = Task(title="Feeding", duration_minutes=20, priority="medium", start_time=time(9, 0))
    pet_a.add_task(task_a)
    pet_b.add_task(task_b)

    scheduler = Scheduler()
    scheduler.scheduled_tasks = [task_a, task_b]

    warnings = scheduler.check_conflicts()

    assert len(warnings) == 1
    assert "Biscuit: Walk" in warnings[0]
    assert "Whiskers: Feeding" in warnings[0]


def test_check_conflicts_flags_partial_overlap():
    task_a = Task(title="Walk", duration_minutes=30, priority="high", start_time=time(9, 0))
    task_b = Task(title="Training", duration_minutes=15, priority="low", start_time=time(9, 15))
    scheduler = Scheduler()
    scheduler.scheduled_tasks = [task_a, task_b]

    warnings = scheduler.check_conflicts()

    assert len(warnings) == 1


def test_check_conflicts_allows_back_to_back_tasks():
    task_a = Task(title="Walk", duration_minutes=30, priority="high", start_time=time(9, 0))
    task_b = Task(title="Feeding", duration_minutes=15, priority="medium", start_time=time(9, 30))
    scheduler = Scheduler()
    scheduler.scheduled_tasks = [task_a, task_b]

    warnings = scheduler.check_conflicts()

    assert warnings == []


def test_check_conflicts_returns_empty_when_no_tasks_scheduled():
    scheduler = Scheduler()
    scheduler.scheduled_tasks = []

    assert scheduler.check_conflicts() == []
