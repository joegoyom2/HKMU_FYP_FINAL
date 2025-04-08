from config.db_config import db_connect

def insert_component(cursor, name, component_type, description):
    sql = """
        INSERT INTO components (component_name, component_type, description)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (name, component_type, description))
    return cursor.lastrowid


def get_latest_components(limit=5):
    db, cursor = db_connect()
    if not db:
        return None, "Unable to connect to MySQL"

    try:
        cursor.execute("""
            SELECT c.component_name, c.component_type, c.description, 
                   COALESCE(GROUP_CONCAT(m.method_name SEPARATOR ', '), '') AS methods
            FROM components c
            LEFT JOIN methods m ON c.component_id = m.component_id
            GROUP BY c.component_id
            ORDER BY c.component_id DESC
            LIMIT %s;
        """, (limit,))
        results = cursor.fetchall()
        return results, None
    except Exception as e:
        return None, str(e)
    finally:
        cursor.close()
        db.close()