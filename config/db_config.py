import pymysql, os
from dotenv import load_dotenv

load_dotenv()  # 讀取本地 .env，部署時可以移除

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
    """ 建立 MySQL 連線 """
    try:
        print("🔹 嘗試使用 pymysql 連接 MySQL...")
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        print("✅ pymysql 連接 MySQL 成功！")
        return conn, cursor
    except pymysql.MySQLError as e:
        print(f"❌ pymysql 連接 MySQL 失敗: {e}")
        return None, None
