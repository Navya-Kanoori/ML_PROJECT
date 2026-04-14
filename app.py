from flask import Flask, render_template, request, send_file
import os
from model import detect_anomalies

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    if file.filename == "":
        return "No file uploaded"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    df, anomalies, normal, total = detect_anomalies(filepath)

    anomaly_count = len(anomalies)
    normal_count = len(normal)

    anomalies.to_csv("anomaly_report.csv", index=False)

    table = anomalies.head(20).to_html(classes="table table-striped", index=False)

    return render_template("dashboard.html",
                           total=total,
                           normal=normal_count,
                           anomalies=anomaly_count,
                           table=table)


@app.route('/download')
def download():
    return send_file("anomaly_report.csv", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)