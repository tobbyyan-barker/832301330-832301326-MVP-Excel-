# routes.py
from flask import Blueprint, render_template, request, redirect, url_for, send_file
from extensions import db
from models import Contact, ContactMethod
import pandas as pd
import io

# 创建蓝图对象
main_bp = Blueprint('main', __name__)

# --- 1. 首页列表 (查) ---
@main_bp.route('/')
def index():
    # 逻辑：收藏的排前面，同类中后创建的排前面
    contacts = Contact.query.order_by(Contact.is_favorite.desc(), Contact.id.desc()).all()
    return render_template('index.html', contacts=contacts)

# --- 2. 添加联系人 (增) ---
@main_bp.route('/add', methods=['POST'])
def add_contact():
    name = request.form.get('name')
    m_type = request.form.get('method_type')
    m_value = request.form.get('value')

    if name:
        # 第一步：创建联系人主体
        new_contact = Contact(name=name)
        db.session.add(new_contact)
        # 必须先提交一次 commit，数据库才会为 new_contact 生成 id
        db.session.commit()
        
        # 如果同时填写了联系方式
        if m_type and m_value:
            # 注意：这里用到了 contact_id 外键，关联到刚才创建的人
            new_method = ContactMethod(method_type=m_type, value=m_value, contact_id=new_contact.id)
            db.session.add(new_method)
            db.session.commit()
            
    return redirect(url_for('main.index'))

# --- 3. 为现有联系人添加方式 (一对多逻辑) ---
@main_bp.route('/add_method/<int:contact_id>', methods=['POST'])
def add_method(contact_id):
    m_type = request.form.get('method_type')
    m_value = request.form.get('value')
    if m_type and m_value:
        new_method = ContactMethod(method_type=m_type, value=m_value, contact_id=contact_id)
        db.session.add(new_method)
        db.session.commit()
    return redirect(url_for('main.index'))

# --- 4. 切换收藏状态 (改) ---
@main_bp.route('/toggle_favorite/<int:id>')
def toggle_favorite(id):
    contact = Contact.query.get_or_404(id)
    contact.is_favorite = not contact.is_favorite
    db.session.commit()
    return redirect(url_for('main.index'))

# --- 5. 删除联系人 (删) ---
@main_bp.route('/delete/<int:id>')
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect(url_for('main.index'))

# --- 6. 删除单个联系方式 ---
@main_bp.route('/delete_method/<int:id>')
def delete_method(id):
    method = ContactMethod.query.get_or_404(id)
    db.session.delete(method)
    db.session.commit()
    return redirect(url_for('main.index'))

# --- 7. 导出 Excel ---
@main_bp.route('/export')
def export_excel():
    contacts = Contact.query.all()
    data = []
    for c in contacts:
        # 将多个联系方式拼成字符串: "手机:123; 邮箱:abc"
        methods_str = "; ".join([f"{m.method_type}:{m.value}" for m in c.methods])
        data.append({
            "姓名": c.name,
            "是否收藏": "是" if c.is_favorite else "否",
            "联系方式": methods_str
        })
    # 使用 Pandas 创建 DataFrame
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)
    return send_file(output, download_name="contacts.xlsx", as_attachment=True)

# --- 8. 导入 Excel ---
@main_bp.route('/import', methods=['POST'])
def import_excel():
    file = request.files['file']
    if not file: return redirect(url_for('main.index'))

    try:
        df = pd.read_excel(file)
        for _, row in df.iterrows():
            if pd.isna(row.get('姓名')): continue
            
            # 创建联系人
            new_contact = Contact(name=str(row['姓名']))
            if str(row.get('是否收藏')).strip() in ['是', 'Yes', 'True', '1']:
                new_contact.is_favorite = True
            db.session.add(new_contact)
            db.session.commit()
            
            # 解析联系方式字符串
            raw_methods = row.get('联系方式')
            if not pd.isna(raw_methods):
                for item in str(raw_methods).split(';'):
                    if ':' in item:
                        t, v = item.split(':', 1)
                        db.session.add(ContactMethod(
                            method_type=t.strip(), value=v.strip(), contact_id=new_contact.id
                        ))
        db.session.commit()
    except Exception as e:
        print(f"Error importing: {e}")
        
    return redirect(url_for('main.index'))
