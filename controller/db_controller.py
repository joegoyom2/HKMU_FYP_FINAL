from flask import jsonify
from config.db_config import db_connect

def reset_db():
    db, cursor = db_connect()
    if not db:
        return jsonify({"error": "Unable to connect to MySQL"}), 500

    try:
        cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cursor.execute("DROP TABLE IF EXISTS variableparametermapping;")
        cursor.execute("DROP TABLE IF EXISTS methodparameters;")
        cursor.execute("DROP TABLE IF EXISTS methods;")
        cursor.execute("DROP TABLE IF EXISTS componentdependencies;")
        cursor.execute("DROP TABLE IF EXISTS components;")
        cursor.execute("SET FOREIGN_KEY_CHECKS=1;")

        db.commit()
        return jsonify({"message": "✅ Database reset successfully!"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"❌ Reset failed: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()


def initialize_db():
    db, cursor = db_connect()
    if not db:
        return jsonify({"error": "Unable to connect to MySQL"}), 500

    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS components (
            component_id INT AUTO_INCREMENT PRIMARY KEY,
            component_name VARCHAR(255) NOT NULL,
            component_type ENUM('class', 'function', 'module', 'external_library') NOT NULL,
            description TEXT
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS methods (
            method_id INT AUTO_INCREMENT PRIMARY KEY,
            component_id INT NOT NULL,
            method_name VARCHAR(255) NOT NULL,
            FOREIGN KEY (component_id) REFERENCES components(component_id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS methodparameters (
            parameter_id INT AUTO_INCREMENT PRIMARY KEY,
            method_id INT NOT NULL,
            parameter_name VARCHAR(255) NOT NULL,
            parameter_type VARCHAR(255),
            FOREIGN KEY (method_id) REFERENCES methods(method_id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS variableparametermapping (
            mapping_id INT AUTO_INCREMENT PRIMARY KEY,
            parameter_id INT NOT NULL,
            variable_name VARCHAR(255) NOT NULL,
            FOREIGN KEY (parameter_id) REFERENCES methodparameters(parameter_id) ON DELETE CASCADE
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS componentdependencies (
            source_component_id INT NOT NULL,
            target_component_id INT NOT NULL,
            dependency_type ENUM('uses', 'calls', 'imports', 'extends') NOT NULL,
            PRIMARY KEY (source_component_id, target_component_id),
            FOREIGN KEY (source_component_id) REFERENCES components(component_id) ON DELETE CASCADE,
            FOREIGN KEY (target_component_id) REFERENCES components(component_id) ON DELETE CASCADE
        );
        """)

        db.commit()
        return jsonify({"message": "✅ All tables initialized successfully!"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": f"❌ Initialization failed: {str(e)}"}), 500

    finally:
        cursor.close()
        db.close()
