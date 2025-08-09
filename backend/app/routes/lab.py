from flask import Blueprint, request, jsonify, g
from app import db
from app.models import Lab, EditRecord, Member, ResearchGroup
from app.auth import admin_required
from app.utils.validators import validate_email, validate_string_length
from app.utils.helpers import success_response, error_response
from app.utils.file_handler import save_file, delete_file

bp = Blueprint('lab', __name__)

@bp.route('/lab', methods=['GET'])
def get_lab():
    lab = Lab.query.filter_by(enable=1).first()
    
    if not lab:
        # 返回默認實驗室信息
        default_lab = {
            'lab_id': None,
            'lab_logo_path': None,
            'carousel_img_1': None,
            'carousel_img_2': None,
            'carousel_img_3': None,
            'carousel_img_4': None,
            'lab_zh': '實驗室',
            'lab_en': 'Laboratory',
            'lab_desc_zh': '請在管理後台設置實驗室信息',
            'lab_desc_en': 'Please set lab information in admin panel',
            'lab_address_zh': '',
            'lab_address_en': '',
            'lab_email': '',
            'lab_phone': '',
            'enable': 1
        }
        return jsonify(success_response(default_lab))
    
    return jsonify(success_response(lab.to_dict()))

@bp.route('/lab', methods=['PUT', 'POST'])
@admin_required
def update_lab():
    lab = Lab.query.filter_by(enable=1).first()
    is_create = lab is None
    
    if is_create:
        lab = Lab(enable=1)
    
    try:
        # 處理文件上傳
        old_logo_path = lab.lab_logo_path
        if 'lab_logo' in request.files:
            file = request.files['lab_logo']
            if file and file.filename:
                # 保存新logo
                new_logo_path = save_file(file, 'lab_logo', max_size=5*1024*1024)
                lab.lab_logo_path = new_logo_path
                
                # 刪除舊logo
                if old_logo_path and old_logo_path != new_logo_path:
                    delete_file(old_logo_path)
        
        # 處理輪播圖片上傳和清除
        carousel_fields = ['carousel_img_1', 'carousel_img_2', 'carousel_img_3', 'carousel_img_4']
        for carousel_field in carousel_fields:
            old_carousel_path = getattr(lab, carousel_field)
            
            # 檢查是否要清除圖片
            clear_param = f'clear_{carousel_field}'
            if clear_param in request.form and request.form[clear_param].lower() == 'true':
                setattr(lab, carousel_field, None)
                if old_carousel_path:
                    delete_file(old_carousel_path)
            # 檢查是否有新圖片上傳
            elif carousel_field in request.files:
                file = request.files[carousel_field]
                if file and file.filename:
                    # 保存新輪播圖片
                    new_carousel_path = save_file(file, carousel_field, max_size=5*1024*1024)
                    setattr(lab, carousel_field, new_carousel_path)
                    
                    # 刪除舊圖片
                    if old_carousel_path and old_carousel_path != new_carousel_path:
                        delete_file(old_carousel_path)
        
        # 更新文本字段
        text_fields = [
            'lab_zh', 'lab_en', 'lab_desc_zh', 'lab_desc_en',
            'lab_address_zh', 'lab_address_en', 'lab_email', 'lab_phone'
        ]
        
        update_data = {}
        for field in text_fields:
            if field in request.form:
                value = request.form[field].strip()
                
                # 特殊校驗
                if field == 'lab_email' and value:
                    if not validate_email(value):
                        return jsonify(error_response(2000, '郵箱格式不正確')), 400
                
                if field.startswith('lab_desc'):
                    if not validate_string_length(value, 1000):
                        return jsonify(error_response(2000, f'{field} 長度不能超過1000字符')), 400
                else:
                    if not validate_string_length(value, 500):
                        return jsonify(error_response(2000, f'{field} 長度不能超過500字符')), 400
                
                setattr(lab, field, value)
                update_data[field] = value
        
        if is_create:
            db.session.add(lab)
        
        db.session.flush()
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='CREATE' if is_create else 'UPDATE',
            edit_module=1,  # 實驗室模組
        )
        record.set_content(update_data)
        db.session.add(record)
        
        db.session.commit()
        
        message = '實驗室信息創建成功' if is_create else '實驗室信息更新成功'
        return jsonify(success_response(lab.to_dict(), message))
        
    except ValueError as e:
        db.session.rollback()
        return jsonify(error_response(2000, str(e))), 400
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'操作失敗: {str(e)}')), 500

@bp.route('/lab', methods=['DELETE'])
@admin_required
def delete_lab():
    """刪除實驗室信息（軟刪除）"""
    lab = Lab.query.filter_by(enable=1).first()
    
    if not lab:
        return jsonify(error_response(4000, '實驗室信息不存在')), 404
    
    # 檢查是否有有效的課題組
    active_groups = ResearchGroup.query.filter_by(
        lab_id=lab.lab_id,
        enable=1
    ).count()
    
    if active_groups > 0:
        return jsonify(error_response(4000, '該實驗室下仍有有效課題組，無法刪除')), 409
    
    # 檢查是否有有效的成員
    active_members = Member.query.filter_by(
        lab_id=lab.lab_id,
        enable=1
    ).count()
    
    if active_members > 0:
        return jsonify(error_response(4000, '該實驗室下仍有有效成員，無法刪除')), 409
    
    try:
        # 刪除關聯的文件
        if lab.lab_logo_path:
            delete_file(lab.lab_logo_path)
        
        carousel_fields = ['carousel_img_1', 'carousel_img_2', 'carousel_img_3', 'carousel_img_4']
        for carousel_field in carousel_fields:
            carousel_path = getattr(lab, carousel_field)
            if carousel_path:
                delete_file(carousel_path)
        
        # 軟刪除
        lab.enable = 0
        
        # 記錄操作
        record = EditRecord(
            admin_id=g.current_admin.admin_id,
            edit_type='DELETE',
            edit_module=0,  # 實驗室模組
        )
        record.set_content({'deleted_lab_id': lab.lab_id})
        db.session.add(record)
        
        db.session.commit()
        
        return jsonify(success_response(None, '實驗室信息刪除成功'))
        
    except Exception as e:
        db.session.rollback()
        return jsonify(error_response(5000, f'刪除失敗: {str(e)}')), 500