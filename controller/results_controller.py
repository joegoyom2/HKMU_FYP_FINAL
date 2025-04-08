
from flask import jsonify
from model.component_model import get_latest_components
from model.dependency_model import get_latest_dependencies

def get_results():
    components, err1 = get_latest_components()
    dependencies, err2 = get_latest_dependencies()

    if err1:
        return jsonify({"error": f"❌ Component query failed: {err1}"}), 500
    if err2:
        return jsonify({"error": f"❌ Dependency query failed: {err2}"}), 500

    return jsonify({
        "components": components,
        "dependencies": dependencies
    }), 200
