# coding:utf-8
from flask import jsonify


class RET:
    OK = "0"
    DBERR = "4001"
    NODATA = "4002"
    DATAEXIST = "4003"
    NOPARAMS = "4004"
    PARAMERROR = "4005"
    DUPLICATEDATA = "4006"
    TOKENERROR = "4100"
    THIRDPARTYERROR = "4200"
    UNKOWNERR = "4501"


error_map = {
    RET.OK: u"请求成功",
    RET.DBERR: u"数据库操作错误",
    RET.NODATA: u"无数据",
    RET.DATAEXIST: u"数据已存在",
    RET.NOPARAMS: u"缺少必要参数",
    RET.DUPLICATEDATA: u"重复数据",
    RET.PARAMERROR: u"参数有误",
    RET.TOKENERROR: u"token过期",
    RET.THIRDPARTYERROR: u"第三方库报错",
    RET.UNKOWNERR: u"未知错误",
}


class PageModel(object):
    def __init__(self, total_page, total_num, items, page_num):
        self.total_page = total_page
        self.total_num = total_num
        self.items = items
        self.page_num = page_num

    def keys(self):
        return 'total_page', 'total_num', 'items', 'page_num'

    def __getitem__(self, item):
        return getattr(self, item)


class ResponseData(object):
    def __init__(self, code, data=None):
        self.code = code
        self.data = data

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, value):
        self._code = int(value)
        if not error_map[value]:
            self.message = '未知错误'
        self.message = error_map[value]

    def to_dict(self):
        return jsonify({'code': self._code, 'message': self.message, 'data': self.data})