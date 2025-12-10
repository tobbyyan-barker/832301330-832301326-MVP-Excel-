# app.py
import os
from flask import Flask
from extensions import db
from routes import main_bp

def create_app():
    # 1. 算出前端文件夹的路径 (假设 frontend 就在 app.py 旁边)
    # Get the absolute path of the current directory (where app.py is located)
    base_dir = os.path.abspath(os.path.dirname(__file__))
    # Set paths for frontend templates and static files
    # The frontend folder contains the HTML templates and static assets (CSS, JS, images)
    template_dir = os.path.join(base_dir, 'frontend', 'templates')
    static_dir = os.path.join(base_dir, 'frontend', 'static')

    # 2. 初始化 Flask，指定去哪里找 HTML
    # template_folder: Directory where Flask looks for HTML templates
    # static_folder: Directory for static files (CSS, JavaScript, images)
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

    # 3. 配置数据库
    # SQLite database file will be created in the project root directory
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'addressbook.db')
    # Disable modification tracking to save resources (not needed for this application)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Secret key for session management and security features
    app.config['SECRET_KEY'] = 'dev-key'

    # 4. 初始化数据库插件 (Extensions)
    # This connects SQLAlchemy to our Flask application
    db.init_app(app)

    # 5. 注册路由 (Routes)
    # Blueprints help organize the application into modular components
    app.register_blueprint(main_bp)

    # 6. 自动创建表结构 (如果表不存在)
    # This ensures all models are registered and tables are created if they don't exist
    with app.app_context():
        db.create_all()

    return app

# 启动代码
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
