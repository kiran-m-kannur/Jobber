import os

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "123456789"

# Configure upload folder
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/upload_pdf", methods=["POST"])
def upload_pdf():
    if "pdf_file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["pdf_file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Store the filename in session
        session["uploaded_pdf"] = filename

        return redirect(url_for("job_form"))

    return jsonify({"error": "Invalid file type"}), 400


@app.route("/job_form")
def job_form():
    if "uploaded_pdf" not in session:
        return redirect(url_for("landing"))
    return render_template("index.html", pdf_name=session.get("uploaded_pdf"))


@app.route("/submit", methods=["POST"])
def submit():
    data = request.json

    # Process the received data
    processed_data = {
        "received_data": {
            "about_job": data.get("about_job"),
            "about_company": data.get("about_company"),
            "job_description": data.get("job_description"),
            "uploaded_pdf": session.get("uploaded_pdf", "No PDF uploaded"),
        },
        "status": "success",
        "message": "Data received successfully",
    }

    return jsonify(processed_data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
