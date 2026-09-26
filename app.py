import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner & Pet")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input(
    "Available minutes per day", min_value=1, max_value=1440, value=60
)
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_minutes_per_day=int(available_minutes))
    st.session_state.pet = Pet(name=pet_name, species=species)
    st.session_state.owner.add_pet(st.session_state.pet)

owner: Owner = st.session_state.owner
pet: Pet = st.session_state.pet

# Keep the persisted Owner/Pet in sync with the latest widget values.
owner.name = owner_name
owner.available_minutes_per_day = int(available_minutes)
pet.name = pet_name
pet.species = species

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed directly into the Scheduler below.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add task"):
    pet.add_task(Task(title=task_title, duration_minutes=int(duration), priority=priority))

if pet.tasks:
    st.write("Current tasks:")
    st.table(
        [
            {"title": t.title, "duration_minutes": t.duration_minutes, "priority": t.priority}
            for t in pet.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    scheduler.generate_plan(owner)
    st.code(scheduler.explain())
