import os
import json
import traceback
import subprocess
from flask import request, jsonify, send_file
from config.config import PLANTUML_JAR_PATH
from config.db_config import db_connect
from service.ai_class_diagram import class_diagram_from_code
from service.ai_code_analysis import call_plantuml_ai

# ✅ 從文字檔讀取最新上傳檔案路徑
def read_uploaded_path():
    try:
        with open("latest_uploaded_path.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None

def generate_uml():
    uml_type = request.args.get("type", "sequence")

    db, cursor = db_connect()
    if not db:
        return jsonify({"error": "❌ Unable to connect to MySQL"}), 500

    try:
        if uml_type == "sequence":
            # 🔹 從資料庫取得 components 和 dependencies
            cursor.execute("SELECT component_name, component_type FROM components")
            components = [{"name": row["component_name"], "type": row["component_type"]} for row in cursor.fetchall()]
            if not components:
                return jsonify({"error": "❌ No components found"}), 500

            cursor.execute("""
                SELECT c1.component_name AS source_component, 
                       c2.component_name AS target_component, 
                       d.dependency_type
                FROM componentdependencies d
                JOIN components c1 ON d.source_component_id = c1.component_id
                JOIN components c2 ON d.target_component_id = c2.component_id
            """)
            dependencies = [{"source": row["source_component"], "target": row["target_component"], "type": row["dependency_type"]}
                            for row in cursor.fetchall()]
            if not dependencies:
                return jsonify({"error": "❌ Dependencies not found"}), 500

            uml_data = {"components": components, "dependencies": dependencies}
            print("🔍 JSON sent to AI:\n", json.dumps(uml_data, indent=2))

            prompt = f"""
            Generate a well-formatted PlantUML sequence diagram.
            - Do NOT repeat participants.
            - Show only necessary interactions.
            - Direction must match dependency type.

            JSON:
            {json.dumps(uml_data, indent=2)}
            """

            plantuml_code = call_plantuml_ai(prompt)

        elif uml_type == "class":
            file_path = read_uploaded_path()
            if not file_path or not os.path.exists(file_path):
                return jsonify({"error": "❌ No uploaded file found for class diagram"}), 400

            print(f"🔍 Analyze uploaded file: {file_path}")
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()

            class_data = class_diagram_from_code(code)
            if "error" in class_data:
                return jsonify({"error": class_data["error"]}), 500

            # ✅ 根據 class_data 組成 PlantUML 語法
            plantuml_lines = ["@startuml"]
            for cls in class_data.get("classes", []):
                plantuml_lines.append(f"class {cls['class_name']} {{")
                for attr in cls.get("attributes", []):
                    plantuml_lines.append(f"  - {attr['name']} : {attr['type']}")
                for method in cls.get("methods", []):
                    visibility = "+" if method['visibility'] == "public" else "-"
                    plantuml_lines.append(f"  {visibility} {method['name']}() : {method['return_type']}")
                plantuml_lines.append("}")
            plantuml_lines.append("@enduml")
            plantuml_code = "\n".join(plantuml_lines)
            print("🧠 Cleaned PlantUML code:\n", plantuml_code)
        elif uml_type == "use case":
            cursor.execute("SELECT component_name, component_type FROM components")
            components = [{"name": row["component_name"], "type": row["component_type"]} for row in cursor.fetchall()]
            if not components:
                return jsonify({"error": "❌ No components found"}), 500

            cursor.execute("""
                SELECT c1.component_name AS source_component, 
                       c2.component_name AS target_component, 
                       d.dependency_type
                FROM componentdependencies d
                JOIN components c1 ON d.source_component_id = c1.component_id
                JOIN components c2 ON d.target_component_id = c2.component_id
            """)
            dependencies = [{"source": row["source_component"], "target": row["target_component"], "type": row["dependency_type"]}
                            for row in cursor.fetchall()]
            if not dependencies:
                return jsonify({"error": "❌ Dependencies not found"}), 500

            uml_data = {"components": components, "dependencies": dependencies}
            print("🔍 JSON sent to AI for use case:\n", json.dumps(uml_data, indent=2))

            prompt = f"""
            Please generate a use case diagram in PlantUML format based on the following metadata.
            - Assume actors such as 'User' or 'Admin' if needed.
            - Group related use cases together.
            - Use actor --> (use case) syntax.

            JSON:
            {json.dumps(uml_data, indent=2)}
            """

            plantuml_code = call_plantuml_ai(prompt)
            if "@startuml" in plantuml_code and "@enduml" in plantuml_code:
                between = plantuml_code.split("@startuml")[1].split("@enduml")[0].strip()
                if not between:
                    return jsonify({"error": "❌ AI returns an empty use case diagram. Please check the prompt or regenerate it."}), 400

        else:
            return jsonify({"error": f"Unknown UML type: {uml_type}"}), 400

        # 🔧 儲存 PUML 並執行 JAR 產圖
        output_puml = os.path.join(os.getcwd(), "output.puml")
        output_png = os.path.join(os.getcwd(), "output.png")

        with open(output_puml, "w", encoding="utf-8") as f:
            f.write(plantuml_code)
        print(f"✅ PlantUML saved: {output_puml}")

        if os.path.exists(PLANTUML_JAR_PATH):
            subprocess.run(["java", "-jar", PLANTUML_JAR_PATH, output_puml], check=True)
        else:
            return jsonify({"error": f"❌ PlantUML JAR not found at {PLANTUML_JAR_PATH}"}), 500

        if os.path.exists(output_png):
            print(f"✅ UML image generated: {output_png}")
            return send_file(output_png, mimetype="image/png")
        else:
            return jsonify({"error": "❌ output.png not found"}), 500

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "traceback": traceback.format_exc()}), 500

    finally:
        cursor.close()
        db.close()
