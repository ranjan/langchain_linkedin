from flask import Flask, request, render_template
from ice_breaker import ice_break_with

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = None
    profile_url = None
    tool_used = None

    if request.method == "POST":
        #query = request.form.get("query")
        query = request.form.get("name")  # fix field name

        if query:
            summary, profile_url, tool_used = ice_break_with(query)

    return render_template("index.html", summary=summary, url=profile_url, tool=tool_used)

if __name__ == "__main__":
    app.run(debug=True)
