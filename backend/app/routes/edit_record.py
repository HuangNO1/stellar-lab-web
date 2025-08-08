from flask import Blueprint, request, jsonify
from app.models import EditRecord
from app.auth import admin_required, super_admin_required
from app.utils.helpers import get_pagination_params, paginate_query, success_response, error_response
from app.utils.validators import validate_date

bp = Blueprint('edit_record', __name__)

@bp.route('/edit-records', methods=['GET'])
@admin_required
def get_edit_records():
    page, per_page = get_pagination_params()
    
    query = EditRecord.query
    
    # 按管理員篩選
    admin_id = request.args.get('admin_id', type=int)
    if admin_id:
        query = query.filter(EditRecord.admin_id == admin_id)
    
    # 按模組篩選
    edit_module = request.args.get('edit_module', type=int)
    if edit_module is not None:
        query = query.filter(EditRecord.edit_module == edit_module)
    
    # 按操作類型篩選
    edit_type = request.args.get('edit_type')
    if edit_type:
        query = query.filter(EditRecord.edit_type == edit_type.upper())
    
    # 按日期範圍篩選
    start_date = request.args.get('start_date')
    if start_date:
        valid, date_obj = validate_date(start_date)
        if valid and date_obj:
            query = query.filter(EditRecord.edit_date >= date_obj)
    
    end_date = request.args.get('end_date')
    if end_date:
        valid, date_obj = validate_date(end_date)
        if valid and date_obj:
            from datetime import datetime, timedelta
            # 包含當天結束時間
            end_datetime = datetime.combine(date_obj, datetime.max.time())
            query = query.filter(EditRecord.edit_date <= end_datetime)
    
    # 按時間倒序排序
    query = query.order_by(EditRecord.edit_date.desc())
    
    result = paginate_query(query, page, per_page)
    return jsonify(success_response(result))

@bp.route('/edit-records/<int:edit_id>', methods=['GET'])
@admin_required
def get_edit_record(edit_id):
    record = EditRecord.query.get_or_404(edit_id)
    return jsonify(success_response(record.to_dict()))