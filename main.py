from flask import Flask, request
import os

app = Flask(__name__)

STATUS_FILE = os.path.join(os.path.dirname(__file__), "status.txt")


def get_history():
    if not os.path.exists(STATUS_FILE):
        return []

    with open(STATUS_FILE, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def save_status(status):
    history = get_history()

    number = len(history) + 1
    history.append(f"{number} {status}")

    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(history))


@app.route("/")
def index():

    status = request.args.get("status")

    if status in ["on", "off"]:
        save_status(status.upper())

    history = get_history()

    # 🔥 ТОЛЬКО ON/OFF в главном блоке
    if history:
        current = history[-1].split()[1]
    else:
        current = "OFF"

    # цвет
    color = "#00c853" if current == "ON" else "#d50000"

    history_html = "<br>".join(history) if history else "NO DATA"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Status Panel</title>

        <style>
            body {{
                background:#0f1117;
                color:white;
                font-family:Arial;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
            }}

            .box {{
                background:#181c25;
                padding:30px;
                border-radius:20px;
                width:380px;
                text-align:center;
            }}

            .status {{
                font-size:50px;
                font-weight:bold;
                margin:20px;
                color:{color};
            }}

            button {{
                width:110px;
                padding:10px;
                margin:5px;
                border:none;
                cursor:pointer;
                color:white;
                border-radius:10px;
                font-size:16px;
            }}

            .on {{ background:#00c853; }}
            .off {{ background:#d50000; }}

            .log {{
                margin-top:20px;
                font-size:14px;
                text-align:left;
                max-height:200px;
                overflow:auto;
                background:#111;
                padding:10px;
                border-radius:10px;
            }}

            .info {{
                font-size:13px;
                opacity:0.7;
                margin-top:10px;
            }}
        </style>
    </head>

    <body>

        <div class="box">

            <h2>STATUS PANEL</h2>

            <div class="status">{current}</div>

            <a href="/?status=on">
                <button class="on">ON</button>
            </a>

            <a href="/?status=off">
                <button class="off">OFF</button>
            </a>

            <div class="info">
                Управление через кнопки или URL:<br>
                <b>/?status=on</b> / <b>/?status=off</b>
            </div>

            <div class="log">
                {history_html}
            </div>

        </div>

    </body>
    </html>
    """


if __name__ == "__main__":
    print("SERVER STARTED: http://127.0.0.1:5000")
    app.run(debug=True)