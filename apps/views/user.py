from flask import Blueprint, current_app, request, g
from utils.jwt_utils import generate_jwt
from ..models import db, Book, User
from utils.authorization import LoginRequired
from utils.response_code import RET, ResponseData, PageModel
from utils.qiniu_upload import upload_by_qiniu
from werkzeug.security import check_password_hash

bp = Blueprint('user_router', __name__, url_prefix='/user')


@bp.route('/register', methods=['POST'])
def register():
    image_data = request.files.get("file")
    result = ResponseData(RET.OK)
    if not image_data:
        result.code = RET.NOPARAMS
        return result.to_dict()
    location = request.form.get('location')
    if not location:
        location = '北京市/北京市/东城区'
    ls = location.split('/')
    if len(ls) != 3:
        result.code = RET.PARAMERROR
        return result.to_dict()
    token = upload_by_qiniu(image_data)
    if not token:
        result.code = RET.THIRDPARTYERROR
        return result.to_dict()
    try:
        user = User({
            'userName': request.form.get('userName'),
            'password': request.form.get('password'),
            'gender': request.form.get('gender'),
            'province': ls[0],
            'city': ls[1],
            'district': ls[2],
            'avatarUrl': token
        })
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        result.code = RET.DBERR
        return result.to_dict()
    result.data = user.to_dict()
    result.data['token'] = generate_jwt({'user_id': user.id})
    return result.to_dict()


@bp.route('/login', methods=['POST'])
def login():
    result = ResponseData(RET.OK)
    userName = request.form.get('userName')
    password = request.form.get('password')
    if not all([userName, password]):
        result.code = RET.NOPARAMS
        return result.to_dict()
    try:
        user = User.query.filter_by(userName=userName).first()
        if not user:
            result.code = RET.NODATA
            return result.to_dict()
        if not check_password_hash(user.password_hash, password):
            result.code = RET.NODATA
            return result.to_dict()
        result.data = user.to_dict()
        result.data['token'] = generate_jwt({'user_id': user.id})
    except Exception as e:
        current_app.logger.error(e)
        result.code = RET.NODATA
        return result.to_dict()
    return result.to_dict()


@bp.route('/addMyBook', methods=['POST'])
@LoginRequired
def addMyBook():
    result = ResponseData(RET.OK)
    book_id = request.form.get('book_id')
    user_id = g.user_id
    if not all([book_id, user_id]):
        result.code = RET.NOPARAMS
        return result.to_dict()
    try:
        book = Book.query.get(book_id)
        if not book:
            result.code = RET.NODATA
            return result.to_dict()
        user = User.query.get(user_id)
        if not user:
            result.code = RET.NODATA
            return result.to_dict()
        book.collect_count += 1
        user.book_shelf.append(book)
        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)
        result.code = RET.DBERR
    return result.to_dict()


@bp.route('/mybook', methods=['GET'])
@LoginRequired
def getMyBookShelf():
    result = ResponseData(RET.OK)
    user_id = g.user_id
    keyword = request.args.get('keyword')
    if not user_id:
        result.code = RET.NOPARAMS
        return result.to_dict()
    try:
        user = User.query.get(user_id)
        if not user:
            result.code = RET.NODATA
            return result.to_dict()
        books = user.book_shelf
        if keyword:
            for book in books[:]:
                if not keyword in book.book_name:
                    books.remove(book)
        books = [dict(book) for book in books]
        result.data = books
    except Exception as e:
        current_app.logger.error(e)
        result.code = RET.DBERR
    return result.to_dict()
