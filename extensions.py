# extensions.py
# This module initializes shared Flask extensions to avoid circular imports.
from flask_sqlalchemy import SQLAlchemy

# 这里只创建一个空的 db 实例，稍后在 app.py 里初始化
db = SQLAlchemy()
