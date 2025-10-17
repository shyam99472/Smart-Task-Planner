from flask import Flask, request, jsonify
from flask_cors import CORS
from llm import generate_task_plan

app = Flask(__name__)
# IMPORTANT: CORS is needed so the 'index.html' file can send requests to this API.
CORS(app)

@app.route('/api/plan', methods=['POST'])
def plan_task():
    """
    Receives the user's goal via POST request, calls the LLM service, and returns the plan.
    """
    try:
        # 1. Get the JSON data from the request body
        data = request.get_json()
        goal = data.get('goal', '').strip()
    except:
        return jsonify({"error": "Invalid JSON in request body."}), 400

    if not goal:
        return jsonify({"error": "No goal provided in the request."}), 400

    # 2. Call the LLM service to get the task breakdown
    task_plan = generate_task_plan(goal)

    # 3. Handle errors or return the final plan
    if "error" in task_plan:
        # If there's an error from LLM, return it with a 500 status
        return jsonify(task_plan), 500
    else:
        # Success! Return the structured plan
        return jsonify(task_plan), 200

if __name__ == '__main__':
    # Run the server on the default port
    # You will run this file in your terminal: `python app.py`
    app.run(debug=True)