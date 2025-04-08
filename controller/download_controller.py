import os
from flask import send_file, jsonify

def download_uml():
    output_png = os.path.join(os.getcwd(), "output.png")
    if os.path.exists(output_png):
        print(f"📥 Sending UML image: {output_png}")
        return send_file(output_png, as_attachment=True, mimetype="image/png")
    else:
        return jsonify({"error": "❌ UML image not found!"}), 404

def download_puml():
    output_puml = os.path.join(os.getcwd(), "output.puml")
    if os.path.exists(output_puml):
        print(f"📥 Sending PUML source: {output_puml}")
        return send_file(output_puml, as_attachment=True, mimetype="text/plain")
    else:
        return jsonify({"error": "❌ PUML file not found!"}), 404
