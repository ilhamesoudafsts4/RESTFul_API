# Import necessary modules
from flask import Flask, request, jsonify, render_template  # Flask modules for web app and HTTP handling
from connexion import get_comments_from_db  # Custom function to fetch comments from the database
from sentiment import analyze_sentiment     # Custom function to analyze the sentiment of a comment
from datetime import datetime               # For parsing and formatting date and time

# Initialize the Flask application and specify the folder containing HTML templates
app = Flask(__name__, template_folder="templates")

# Define a route to handle GET requests for comments
@app.route("/comments", methods=["GET"])
def comments_endpoint():
    # Extract query parameters from the request URL
    subfeddit = request.args.get("subfeddit")  # Required: name of the subfeddit
    start_str = request.args.get("start")      # Optional: start date (ISO format)
    end_str = request.args.get("end")          # Optional: end date (ISO format)
    sort_by_polarity = request.args.get("sort_by_polarity", "false").lower() == "true"  # Optional: sort results by polarity

    # Return error if the required subfeddit parameter is missing
    if not subfeddit:
        return jsonify({"error": "Missing required parameter: subfeddit"}), 400

    # Try to parse the start and end dates, if provided
    try:
        start_date = datetime.fromisoformat(start_str) if start_str else None
        end_date = datetime.fromisoformat(end_str) if end_str else None
    except ValueError:
        return jsonify({"error": "Invalid date format. Use ISO 8601 (e.g., 2025-06-01T00:00:00)"}), 400

    # Fetch all comments for the given subfeddit from the database
    comments = get_comments_from_db(subfeddit)

    filtered = []  # Will store the filtered and processed comments

    # Loop through each comment
    for c in comments:
        created_at = c["created_at"]
        # If created_at is a UNIX timestamp (int), convert it to datetime
        if isinstance(created_at, int):
            created_at = datetime.fromtimestamp(created_at)

        # Apply date filtering if start or end dates are provided
        if (not start_date or created_at >= start_date) and (not end_date or created_at <= end_date):
            # Analyze the sentiment of the comment's text
            polarity, sentiment = analyze_sentiment(c["text"])
            # Add the formatted result to the filtered list
            filtered.append({
                "id": c["id"],
                "text": c["text"],
                "created_at": created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "polarity": polarity,
                "sentiment": sentiment
            })

    # If requested, sort the results by polarity in descending order
    if sort_by_polarity:
        filtered.sort(key=lambda x: x["polarity"], reverse=True)

    # Return the final filtered list as a JSON response
    return jsonify(filtered)

# Route for the homepage, renders the index.html template
@app.route("/")
def home():
    return render_template("index.html")

# Start the Flask development server
if __name__ == "__main__":
    app.run(debug=True)
