from flask import Blueprint, request, current_app
from exts import db
from ..models import BookCategory
from utils.response_code import ResponseData, RET
from utils.qiniu_upload import upload_by_qiniu

bp = Blueprint('category', __name__, url_prefix='/category')


@bp.route('/list', methods=['GET'])
def category_list():
    cates = BookCategory.query.all()
    res = ResponseData(RET.OK)
    dicts = [cate.to_dict() for cate in cates]
    res.data = dicts
    return res.to_dict()


@bp.route('/add', methods=['POST'])
def category_add():
    result = ResponseData(RET.OK)
    cate_name = request.form.get('cate_name')
    if not cate_name:
        result.code = RET.NOPARAMS
        return result.to_dict()
    category = BookCategory.query.filter_by(cate_name=cate_name).first()
    if not category:
        category = BookCategory(cate_name=cate_name)
    else:
        result.data = category.to_dict()
        return result.to_dict()
    file = request.files.get('file')
    if not file:
        category.cate_icon = '/static/img/cate_cover.jpeg'
    else:
        try:
            key = upload_by_qiniu(file)
            category.cate_icon = key
        except Exception as e:
            current_app.logger.error(e)
            result.code = RET.THIRDPARTYERROR
            return result.to_dict()
    try:
        db.session.add(category)
        db.session.commit()
    except Exception as e:
        print(current_app.logger.error(e))
        result.code = RET.DBERR
        return result.to_dict()
    result.data = category.to_dict()
    return result.to_dict()


@bp.route('/delete/<int:id>', methods=['GET'])
def category_del(id):
    result = ResponseData(RET.OK)
    if not id:
        result.code = RET.NOPARAMS
        return result.to_dict()
    cate = BookCategory.query.get(id)
    db.session.delete(cate)
    db.session.commit()
    return result.to_dict()
