import pymysql, os

if os.getenv("RENDER") != "true":
    from dotenv import load_dotenv
    load_dotenv()

config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME'),
    'port': int(os.getenv('DB_PORT', 3307)),
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}

connection = pymysql.connect(**config)

def db_connect():
    """ Establishing a MySQL connection """
    try:
        print("🔹 Try connecting to MySQL using pymysql...")
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        print("✅ pymysql connects to MySQL successfully！")
        return conn, cursor
    except pymysql.MySQLError as e:
        print(f"❌ pymysql fails to connect to MySQL: {e}")
        return None, None
