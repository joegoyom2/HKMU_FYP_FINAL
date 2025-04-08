import pymysql

config = {
    'host': '127.0.0.1',   # **確保使用 127.0.0.1 而不是 localhost**
    'user': 'root',
    'password': '24295151qQ!',  # **請確保密碼正確**
    'database': 'cd_insight',
    'port': 3307,         # **確保使用正確的 MySQL 連接埠**
    'cursorclass': pymysql.cursors.DictCursor,  # **回傳 dict 格式**
    'autocommit': True
}

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
