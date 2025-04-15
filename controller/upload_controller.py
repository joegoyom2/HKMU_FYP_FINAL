import os
from flask import request, jsonify
from werkzeug.utils import secure_filename
from config.config import UPLOAD_FILE, VALID_COMPONENT_TYPES, VALID_DEPENDENCY_TYPES
from config.db_config import db_connect
from service.ai_code_analysis import ai_code_analysis
from model.component_model import insert_component
from model.dependency_model import insert_dependency

def handle_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    file_path = os.path.join(UPLOAD_FILE, secure_filename(file.filename))
    file.save(file_path)
    print(f"✅ File {file.filename} saved to {file_path}")

    with open("latest_uploaded_path.txt", "w", encoding="utf-8") as f:
        f.write(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        code_content = f.read()

    print("🔍 Submit code for AI analysis...")
    analysis_result = ai_code_analysis(code_content)

    if "error" in analysis_result:
        print(f"❌ AI analysis failed: {analysis_result['error']}")
        return jsonify({"error": analysis_result["error"]}), 500

    print("✅ AI analysis completed, ready to be stored in MySQL...")
    db, cursor = db_connect()
    if not db:
        return jsonify({"error": "Unable to connect to MySQL"}), 500

    try:
        component_ids = {}
        for comp in analysis_result["components"]:
            name = comp["component_name"]
            ctype = comp["component_type"]
            description = comp["description"]
            if ctype not in VALID_COMPONENT_TYPES:
                ctype = "external_library"
            cid = insert_component(cursor, name, ctype, description)
            component_ids[name] = cid

        for dep in analysis_result["dependencies"]:
            src = dep["source_component"]
            tgt = dep["target_component"]
            dtype = dep["dependency_type"]
            if dtype not in VALID_DEPENDENCY_TYPES:
                dtype = "uses"

            src_id = component_ids.get(src)
            tgt_id = component_ids.get(tgt)

            if tgt_id is None:
                cid = insert_component(cursor, tgt, "external_library", f"Auto-generated external component for {tgt}")
                tgt_id = cid
                component_ids[tgt] = tgt_id

            if src_id and tgt_id:
                insert_dependency(cursor, src_id, tgt_id, dtype)

        db.commit()
        print("✅ MySQL storage successful!")
        return jsonify({
            "message": f"✅ File {file.filename} uploaded, analyzed, and stored successfully!"
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Database Error: {e}"}), 500

    finally:
        cursor.close()
        db.close()