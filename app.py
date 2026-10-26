import streamlit as st

st.set_page_config(
    page_title="OptiMind AI",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 OptiMind AI")
st.subheader("AI-Based Study & Task Optimizer (DAA Project)")

st.write(
    "Plan smarter, prioritize subjects, and optimize your study hours using "
    "dynamic programming (0/1 Knapsack)."
)

st.divider()

# Initialize session state for tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = [
        {"name": "Revise DAA Algorithms", "hours": 3, "priority": 90},
        {"name": "Cloud Security Lab", "hours": 2, "priority": 75},
        {"name": "Database Assignment", "hours": 1, "priority": 50}
    ]

# Sidebar inputs
st.sidebar.header("⚙️ Configuration & Inputs")
available_hours = st.sidebar.slider("Total Study Hours Available", 1, 24, 5)

st.sidebar.subheader("➕ Add New Task")
with st.sidebar.form("task_form", clear_on_submit=True):
    new_name = st.text_input("Task / Subject Name")
    new_hours = st.number_input("Estimated Hours", min_value=1, max_value=12, value=2)
    new_priority = st.slider("Priority Value (1-100)", 1, 100, 70)
    
    submitted = st.form_submit_button("Add Task")
    if submitted and new_name:
        st.session_state.tasks.append({
            "name": new_name,
            "hours": int(new_hours),
            "priority": int(new_priority)
        })
        st.rerun()

# Main UI
col1, col2 = st.columns(2)

with col1:
    st.header("📚 Current Task Pool")
    for task in st.session_state.tasks:
        st.markdown(f"- **{task['name']}** (⏱️ {task['hours']} hrs | ⭐ Priority: {task['priority']})")

with col2:
    st.header("⚡ DAA 0/1 Knapsack Optimizer")
    st.write(f"Optimizing for a time budget of **{available_hours} hours**.")

    def solve_knapsack(tasks, W):
        n = len(tasks)
        if n == 0 or W == 0:
            return 0, []
        dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]
        for i in range(1, n + 1):
            wt = tasks[i-1]["hours"]
            val = tasks[i-1]["priority"]
            for w in range(1, W + 1):
                if wt <= w:
                    dp[i][w] = max(val + dp[i-1][w - wt], dp[i-1][w])
                else:
                    dp[i][w] = dp[i-1][w]
        w = W
        selected = []
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i-1][w]:
                selected.append(i-1)
                w -= tasks[i-1]["hours"]
        return dp[n][W], selected

    max_val, selected_idx = solve_knapsack(st.session_state.tasks, available_hours)
    st.metric(label="Maximum Priority Score Achieved", value=max_val)
    
    st.subheader("✅ Recommended Study Plan")
    total_time = 0
    for idx in selected_idx:
        t = st.session_state.tasks[idx]
        total_time += t["hours"]
        st.success(f"**{t['name']}** ({t['hours']} hrs, Priority {t['priority']})")
    st.info(f"Total Time Utilized: **{total_time} / {available_hours} hours**")
    