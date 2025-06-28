from flask import Flask, request, render_template
from ice_breaker import ice_break_with_sequential

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    profile_url = None
    tool_used = None
    query = None
    headline = None

    if request.method == "POST":
        query = request.form.get("name")  # Matches input field name in HTML

        if query:
            summary, profile_url, tool_used, _, headline = ice_break_with_sequential(query)

    return render_template(
        "index.html",
        summary=summary,
        url=profile_url,
        tool=tool_used,
        query=query,
        headline=headline.replace('\n', '<br>')
    )

if __name__ == "__main__":
    app.run(debug=True)
