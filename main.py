from flask import Flask, render_template, request

app = Flask(__name__)

STATUS_FILE = "status.txt"


def get_status():
    try:
        with open(STATUS_FILE, "r") as f:
            return f.read().strip()
    except:
        return "OFF"


def save_status(status):
    with open(STATUS_FILE, "w") as f:
        f.write(status)


@app.route("/")
def index():

    status = request.args.get("status")

    if status in ["on", "off"]:
        save_status(status.upper())

    current_status = get_status()

    return render_template(
        "index.html",
        status=current_status
    )


if __name__ == "__main__":
    app.run(debug=True)