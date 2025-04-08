from config.db_config import db_connect

def insert_dependency(cursor, source_id, target_id, dependency_type):
    sql = """
        INSERT INTO componentdependencies (source_component_id, target_component_id, dependency_type)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (source_id, target_id, dependency_type))

def get_latest_dependencies(limit=5):
    db, cursor = db_connect()
    if not db:
        return None, "Unable to connect to MySQL"

    try:
        cursor.execute("""
            SELECT d.source_component_id, d.target_component_id, d.dependency_type,
                   c1.component_name AS source_name,
                   c2.component_name AS target_name
            FROM componentdependencies d
            JOIN components c1 ON d.source_component_id = c1.component_id
            JOIN components c2 ON d.target_component_id = c2.component_id
            ORDER BY d.source_component_id DESC
            LIMIT %s;
        """, (limit,))
        results = cursor.fetchall()
        return results, None
    except Exception as e:
        return None, str(e)
    finally:
        cursor.close()
        db.close()