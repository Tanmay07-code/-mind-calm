# 🌱 MindCalm

**MindCalm** is a lightweight, privacy-first single-page web application built to support **UN Sustainable Development Goal 3 (Good Health & Well-being)**. It provides individuals with an instant, anonymous mental wellness pulse-check by evaluating their daily sleep, anxiety, and mood.

The system processes data entirely in-memory with zero database tracking or account sign-ups. Using a deterministic state machine, it validates inputs, categorizes current stress levels, and instantly delivers tailored, actionable coping strategies through a calming, dark-themed user interface.

---

## ✨ Features

* 🔒 **Absolute Privacy:** Operates entirely in-memory with zero data logging or tracking.
* ⚡ **Zero Friction:** No signups, onboarding flows, or paywalls—get insights in under 60 seconds.
* 🤖 **Graph State Architecture:** Managed by a clean LangGraph pipeline featuring conditional validation and robust, built-in error handling.
* 🌙 **Calming Dark UI:** Customized with low-strain, desaturated slate and teal tones designed to soothe stressed eyes.

---

## 🛠️ Technology Stack

* **LangGraph:** Manages the state tracking machine, validation rules, and conditional routing logic.
* **Streamlit:** Powers the responsive front-end user forms and handles custom CSS injection.
* **Python Core:** Drives the underlying rule-based scoring math and in-memory processing.

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python installed on your system.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mindcalm.git
   cd mindcalm
   ```

2. Install the required open-source dependencies:
   ```bash
   pip install streamlit langgraph
   ```

### Running the Application

Launch the server locally by executing:

```bash
streamlit run app.py
```

The application will automatically spin up in your default web browser at `http://localhost:8501`.

---

## 🗺️ How the Logic Works (Graph Pipeline)

The engine guides your check-in through a strict, crash-proof pipeline:

1. **START** → Collects user drop-down scores.
2. **Validate & Score Node** → Checks if all fields are populated correctly.
   * **Valid Path:** Enters the Assessment Node to classify stress boundaries (High, Moderate, Managed).
   * **Invalid Path:** Routes to the Error Node to gracefully alert the user and safely halt.
3. **Suggest Tips Node** → Injects specific breathing, workload, or rest suggestions based on the final stress level.
4. **END** → Safely terminates the execution session.

---

## 🔮 Future Scope

* **Local NLP Journaling:** Integrating lightweight text-embedding models to analyze short, written thoughts.
* **Enterprise Hooks:** Building native messaging workflows to run quick check-ins inside Slack and Microsoft Teams.
* **Offline-First PWA:** Upgrading to a Progressive Web App for localized wellness checks without network access.
