#!/usr/bin/python3
# coding: utf-8

from sqlalchemy.orm.state import InstanceState

from db import Base


def to_json(obj):
    if isinstance(obj, list):
        # 查询的结果是多个模型类的实例
        datas = []
        for instance in obj:
            obj_dict = instance._sa_instance_state.dict
            print('---obj_dict--', obj_dict)
            datas.append(_obj_to_json(obj_dict))

        return datas

    # 单个模型类的实例
    return _obj_to_json(obj._sa_instance_state.dict)


def _obj_to_json(obj: dict):
    # 模块的私有函数，不对外使用
    ret = obj.copy()
    for k, v in obj.items():

        if isinstance(v, InstanceState):
            del ret[k]

        if isinstance(v, Base):  # apiapp.models.TUser
            ret[k] = _obj_to_json(v._sa_instance_state.dict)

    return ret
