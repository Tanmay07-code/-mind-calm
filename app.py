import streamlit as st
from typing import Dict, Any
from langgraph.graph import StateGraph, START, END

# ==========================================
# 1. STREAMLIT PAGE CONFIG & DARK THEME
# ==========================================
# We use custom CSS to enforce a calming, dark mental-wellness theme (Deep Slate & Teal)
st.set_page_config(page_title="MindCalm | Wellness Check-in", page_icon="🌱", layout="centered")

st.markdown("""
    <style>
    /* Main background and text colors */
    .stApp {
        background-color: #121820;
        color: #E0E6ED;
    }
    /* Titles and Headers */
    h1, h2, h3 {
        color: #81E6D9 !important; /* Soft Teal */
        font-family: 'Helvetica Neue', sans-serif;
    }
    /* Cards/Boxes for results */
    .result-box {
        background-color: #1A222F;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4FD1C5;
        margin-top: 20px;
    }
    /* Error styling */
    .error-box {
        background-color: #2D1A1A;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #E53E3E;
        color: #FED7D7;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. LANGGRAPH STATE DEFINITION
# ==========================================
# This dictionary represents the "memory" of our chatbot across nodes
class State(dict):
    sleep_score: int
    anxiety_score: int
    mood_score: int
    total_score: int
    stress_level: str
    coping_tips: list
    error_message: str
    is_valid: bool

# ==========================================
# 3. GRAPH NODES (The Logic)
# ==========================================

def validate_and_score_node(state: State) -> Dict[str, Any]:
    """Validates inputs and calculates the stress score."""
    try:
        # Fetch scores from state
        s_score = int(state.get("sleep_score", -1))
        a_score = int(state.get("anxiety_score", -1))
        m_score = int(state.get("mood_score", -1))
        
        # Rule-base check: Inputs must be between 1 and 5
        if not all(1 <= score <= 5 for score in [s_score, a_score, m_score]):
            return {
                "is_valid": False, 
                "error_message": "Please answer all questions before submitting."
            }
        
        # Calculate total (Lower score = higher stress in this formula)
        # e.g., 3 questions * max 5 points = 15 max points. 
        total = s_score + a_score + m_score
        return {"total_score": total, "is_valid": True, "error_message": ""}
        
    except (ValueError, TypeError):
        return {
            "is_valid": False, 
            "error_message": "Invalid values detected. Please use the options provided."
        }

def handle_error_node(state: State) -> Dict[str, Any]:
    """Graceful error node that logs the fault and prepares to halt safely."""
    return {"stress_level": "Error", "coping_tips": ["Please correct your inputs above to proceed."]}

def assess_stress_node(state: State) -> Dict[str, Any]:
    """Categorizes stress based on rule-based boundaries."""
    total = state["total_score"]
    
    # 3-6: High Stress | 7-11: Moderate Stress | 12-15: Low/No Stress
    if total <= 6:
        level = "High Stress"
    elif total <= 11:
        level = "Moderate Stress"
    else:
        level = "Low / Managed Stress"
        
    return {"stress_level": level}

def suggest_tips_node(state: State) -> Dict[str, Any]:
    """Rule-based coping mechanism mapping tips directly to stress levels."""
    level = state["stress_level"]
    
    tips_map = {
        "Low / Managed Stress": [
            "✨ Keep up the great routine! Your current balance is strong.",
            "🧘 Try a 5-minute gratitude journaling session tonight.",
            "🚶 Go for a light walk outside to maintain this positive energy."
        ],
        "Moderate Stress": [
            "⏸️ Take a 'tactical pause': Step away from screens for 15 minutes.",
            "🌬️ Try the 4-7-8 box breathing technique (Inhale 4s, Hold 7s, Exhale 8s).",
            "☕ Minimize caffeine intake for the rest of the day."
        ],
        "High Stress": [
            "🚨 Your system is in overdrive. It is time to prioritize dialling back.",
            "🛑 Halting task list: Postpone non-urgent tasks until tomorrow.",
            "📞 Reach out to a trusted friend, family member, or professional to talk it through.",
            "🌲 Strictly step away into a quiet environment and rest your eyes."
        ]
    }
    
    return {"coping_tips": tips_map.get(level, ["Take a few deep breaths and rest."])}

# ==========================================
# 4. CONDITIONAL ROUTING LOGIC
# ==========================================
def route_after_validation(state: State) -> str:
    """Determines whether to move to assessment or route to the error node."""
    if state.get("is_valid") == True:
        return "assess_stress"
    return "handle_error"

# ==========================================
# 5. BUILDING THE GRAPH FLOW
# ==========================================
builder = StateGraph(State)

# Add nodes to graph
builder.add_node("validate_and_score", validate_and_score_node)
builder.add_node("assess_stress", assess_stress_node)
builder.add_node("suggest_tips", suggest_tips_node)
builder.add_node("handle_error", handle_error_node)

# Set up flow control
builder.add_edge(START, "validate_and_score")

# Add conditional routing based on validation node output
builder.add_conditional_edges(
    "validate_and_score",
    route_after_validation,
    {
        "assess_stress": "assess_stress",
        "handle_error": "handle_error"
    }
)

# Connect remaining pipelines to termination
builder.add_edge("assess_stress", "suggest_tips")
builder.add_edge("suggest_tips", END)
builder.add_edge("handle_error", END)

# Compile graph
graph = builder.compile()

# ==========================================
# 6. STREAMLIT UI INTERFACE
# ==========================================
st.title("🌱 MindCalm Check-In")
st.subheader("SDG 3: Good Health & Well-being")
st.write("Take a brief moment to evaluate your current state. Your data is kept strictly local.")

st.write("---")

# User Questionnaire
st.write("### Rate your last 24 hours:")

sleep = st.selectbox(
    "1. How restfully did you sleep last night?",
    options=[0, 1, 2, 3, 4, 5],
    format_func=lambda x: "Select an option..." if x == 0 else [
        "1 - Barely slept / Tossing and turning",
        "2 - Interrupted, restless sleep",
        "3 - OK sleep, woke up slightly tired",
        "4 - Good, mostly uninterrupted sleep",
        "5 - Deep, completely restorative sleep"
    ][x-1]
)

anxiety = st.selectbox(
    "2. How calm and grounded have you felt today?",
    options=[0, 1, 2, 3, 4, 5],
    format_func=lambda x: "Select an option..." if x == 0 else [
        "1 - High anxiety / Constant racing thoughts",
        "2 - Noticeably tense or on edge",
        "3 - Mild, manageable background stress",
        "4 - Mostly calm and collected",
        "5 - Completely serene and centered"
    ][x-1]
)

mood = st.selectbox(
    "3. How would you rate your overall emotional mood?",
    options=[0, 1, 2, 3, 4, 5],
    format_func=lambda x: "Select an option..." if x == 0 else [
        "1 - Feeling completely overwhelmed or down",
        "2 - Low energy, irritable, or flat",
        "3 - Neutral / Doing alright",
        "4 - Good, positive, and optimistic",
        "5 - Excellent, joyful, and thriving"
    ][x-1]
)

# Execution Trigger
if st.button("Complete Check-In"):
    # Pack the user interface inputs into initial State dict
    inputs = {
        "sleep_score": sleep,
        "anxiety_score": anxiety,
        "mood_score": mood
    }
    
    # Run through the LangGraph workflow completely
    final_output = graph.invoke(inputs)
    
    # Render UI layout based on graph result
    if final_output.get("is_valid") == False:
        st.markdown(f"""
        <div class="error-box">
            <h4>⚠️ Attention</h4>
            <p>{final_output['error_message']}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display Results cleanly
        st.markdown(f"""
        <div class="result-box">
            <h3>Assessment Result: <b>{final_output['stress_level']}</b></h3>
            <p>System Score: <b>{final_output['total_score']}/15</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("### 🧘 Tailored Action Steps for You:")
        for tip in final_output['coping_tips']:
            st.write(tip)