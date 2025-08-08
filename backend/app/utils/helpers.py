from flask import request

def get_pagination_params():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    
    return page, per_page

def paginate_query(query, page, per_page):
    items = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return {
        'items': [item.to_dict() for item in items.items],
        'total': items.total,
        'pages': items.pages,
        'page': page,
        'per_page': per_page,
        'has_prev': items.has_prev,
        'has_next': items.has_next
    }

def success_response(data=None, message='OK'):
    return {
        'code': 0,
        'message': message,
        'data': data
    }

def error_response(code, message, data=None):
    return {
        'code': code,
        'message': message,
        'data': data
    }