# Smart Task Planner: AI-Driven Project Decomposition

## 1. Project Overview

The Smart Task Planner is a full-stack application designed to **automate project decomposition** by leveraging advanced Large Language Model (LLM) reasoning.

The system's core function is to take a high-level, natural language goal (e.g., "Launch a product in 2 weeks") and generate a structured, actionable project plan that includes estimated timelines and logical task dependencies.

## 2. Technical Architecture & Design

The solution is implemented using a clean, two-tier architecture:

### A. Backend API (Flask & Python)
* **Purpose:** Implemented a robust Backend API using the Flask framework to host the core logic.
* **Endpoint:** Exposes a single `POST /api/plan` endpoint, accepting the user's goal via JSON input.
* **Security:** Utilizes `python-dotenv` to securely manage the LLM API key via environment variables, ensuring credentials are never exposed in the source code.

### B. LLM Reasoning Service
* **Technology:** Integrated the application with the **Google Gemini API** (`llm.py`) for project decomposition.
* **Evaluation Focus:** The LLM's primary role is to provide strong **timeline logic**, enforce **task completeness**, and establish accurate **dependencies**—all key evaluation criteria.

## 3. Critical Solution: Structured Output

A key technical challenge was ensuring the LLM's natural language output was consistently and reliably parsed. This was solved using dedicated prompt engineering:

* The LLM is prompted to assume the persona of an **"expert project manager."**
* The prompt explicitly mandates a **strict JSON output format**. This guarantees the frontend receives reliable data containing all required keys:
    * `task` (string)
    * `duration_days` (integer)
    * `deadline_days` (integer, cumulative timeline)
    * `dependencies` (list of prerequisite tasks)

## 4. Setup and Local Execution

### Prerequisites
* Python 3.8+
* A valid **Google Gemini API Key**.

### Step 1: Installation
Navigate to the project directory and install the required dependencies:
```bash
pip install -r requirements.txt
