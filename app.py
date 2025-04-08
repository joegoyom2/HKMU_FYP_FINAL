from flask import Flask, render_template
from controller.upload_controller import handle_upload
from controller.uml_controller import generate_uml
from controller.results_controller import get_results
from controller.db_controller import reset_db, initialize_db
from controller.download_controller import download_uml, download_puml

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    return handle_upload()

@app.route("/generate_uml", methods=["GET"])
def handle_generate_uml():
    return generate_uml()

@app.route("/results", methods=["GET"])
def handle_results():
    return get_results()

@app.route("/reset_db", methods=["POST"])
def reset_database():
    return reset_db()

@app.route("/initialize_db", methods=["POST"])
def init_database():
    return initialize_db()

@app.route("/download_uml", methods=["GET"])
def download_uml_file():
    return download_uml()

@app.route("/download_puml", methods=["GET"])
def download_puml_file():
    return download_puml()

if __name__ == "__main__":
    app.run(debug=False)
