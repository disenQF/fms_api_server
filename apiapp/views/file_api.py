#!/usr/bin/python3
# coding: utf-8
import hashlib
import uuid
from datetime import datetime

from flask import Blueprint
from flask import request, jsonify
from sqlalchemy import or_, and_, not_

from db import session
from apiapp.models import TFile

from common import code_, cache_, token_
from . import validate_json, validate_params
from common.serializor import to_json

blue = Blueprint('file_api', __name__)


@blue.route('/list/', methods=['GET'])
def get_code():
    user_id = cache_.get_user_id(request.args.get('token'))
    if user_id:
        try:
            ret = session.query(TFile).filter(TFile.user_id==user_id).all()
            return jsonify({
                'state': 0,
                'data': to_json(ret)
            })
        except:
            pass

    return jsonify({
        'state': 1,
        'msg': '没有数据'
    })

