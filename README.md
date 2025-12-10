# 📘 软工结对作业：极限编程通讯录 (XP Address Book)

> "Simple Design, Rapid Feedback" - 基于极限编程 (Extreme Programming) 理念开发的 Web 通讯录。

## 👥 团队成员与分工 (Team & Division of Labor)

**项目贡献度分配：50% / 50%**

| 角色 | 学号 | 姓名 | 主要职责 (Responsibilities) |
| :--- | :--- | :--- | :--- |
| **后端/架构** | 832301330 | 颜一顺 | 1. 搭建 Flask + SQLAlchemy 后端框架<br>2. 编写核心路由逻辑 (增删改查、收藏)<br>3. 实现 Excel 导入导出功能 (Pandas)<br>4. Git 版本控制与分支管理 |
| **前端/测试** | 832301326 | 曾渝 | 1. 设计前端页面 (HTML/CSS) 与交互逻辑<br>2. 准备测试数据 (Excel) 并进行验收测试<br>3. 编写项目文档与博客 (PSP表格、截图)<br>4. 协助进行 UI 美化与用户体验优化 |

---

## 🚀 项目功能 (Key Features)

本项目已完成作业要求的所有核心功能：

- [x] **基础功能**：完整的联系人增、删、改、查 (CRUD)。
- [x] **多联系方式 (1-to-N)**：支持一个联系人关联多个电话、邮箱或微信号。
- [x] **收藏/书签 (Favorites)**：支持将重要联系人“加星/收藏”，收藏后自动置顶并高亮显示。
- [x] **数据迁移**：支持导出通讯录为 Excel (.xlsx) 文件，以及从 Excel 批量导入数据。

---

## 🛠️ 技术栈 (Tech Stack)

* **Backend**: Python 3, Flask
* **Database**: SQLite, SQLAlchemy (ORM)
* **Frontend**: HTML5, CSS3, Jinja2 Templates
* **Data Processing**: Pandas, OpenPyXL
* **Tools**: Git, VS Code

---

## 💻 如何运行 (How to Run)

如果你将代码下载到了本地，请按以下步骤运行：

1.  **创建虚拟环境**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    # .\venv\Scripts\activate  # Windows
    ```

2.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

3.  **运行项目**
    ```bash
    python app.py
    ```

4.  **访问页面**
    打开浏览器访问：`http://127.0.0.1:5000`
