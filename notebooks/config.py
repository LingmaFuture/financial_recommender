# 数据库配置
MYSQL_CONFIG = {
    'user': 'root',  # 你的MySQL用户名
    'password': '20030926',  # 你的MySQL密码
    'host': 'localhost',
    'database': 'financial_recommender'
}

# SQLAlchemy配置字符串
SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}"

# 其他SQLAlchemy配置
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True  # 开启SQL语句日志 