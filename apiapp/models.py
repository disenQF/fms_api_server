# coding: utf-8
from sqlalchemy import Column, DateTime, Float, ForeignKey, Index, Integer, MetaData, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue
from db import Base, metadata


class TBlockSetting(Base):
    __tablename__ = 't_block_setting'

    block_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('t_user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    block_size = Column(Integer)
    last_time = Column(DateTime)
    note = Column(Text)

    user = relationship('TUser', primaryjoin='TBlockSetting.user_id == TUser.user_id', backref='t_block_settings')



class TFile(Base):
    __tablename__ = 't_file'

    file_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('t_user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    file_type = Column(Integer, server_default=FetchedValue())
    file_name = Column(String(50))
    create_time = Column(DateTime)
    last_time = Column(DateTime)
    file_size = Column(Float, server_default=FetchedValue())
    parent_file_id = Column(Integer, server_default=FetchedValue())
    note = Column(Text)
    file_path = Column(String(200))

    # lazy = 'select' 表示查看属性时，才会执行selet查询语句, 如果是immediate 表示同当前所在的模型数据一起查询出来。
    user = relationship('TUser', primaryjoin='TFile.user_id == TUser.user_id', backref='t_files', lazy='select')



t_t_groom = Table(
    't_groom', metadata,
    Column('groom_id', Integer),
    Column('user_id', Integer),
    Column('friend_id', Integer)
)



class THistory(Base):
    __tablename__ = 't_history'

    history_id = Column(Integer, primary_key=True)
    message_id = Column(ForeignKey('t_message.message_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    user_id = Column(ForeignKey('t_user.user_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    see_time = Column(DateTime)
    see_cnt = Column(Integer)

    message = relationship('TMessage', primaryjoin='THistory.message_id == TMessage.message_id', backref='t_histories')
    user = relationship('TUser', primaryjoin='THistory.user_id == TUser.user_id', backref='t_histories')



class TImageLink(Base):
    __tablename__ = 't_image_links'

    link_id = Column(Integer, primary_key=True)
    water_id = Column(ForeignKey('t_water.water_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    file_id = Column(ForeignKey('t_file.file_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    token = Column(String(50))
    expires = Column(Integer)
    create_time = Column(String(10))

    file = relationship('TFile', primaryjoin='TImageLink.file_id == TFile.file_id', backref='t_image_links')
    water = relationship('TWater', primaryjoin='TImageLink.water_id == TWater.water_id', backref='t_image_links')



class TMessage(Base):
    __tablename__ = 't_message'

    message_id = Column(Integer, primary_key=True)
    title = Column(String(50))
    content = Column(Text)
    create_time = Column(DateTime)
    link_url = Column(String(100))
    note = Column(Text)
    state = Column(Integer, server_default=FetchedValue())



class TShare(Base):
    __tablename__ = 't_share'

    share_id = Column(Integer, primary_key=True)
    file_id = Column(ForeignKey('t_file.file_id', ondelete='RESTRICT', onupdate='RESTRICT'), index=True)
    friend_id = Column(Integer)
    expires = Column(Integer)

    file = relationship('TFile', primaryjoin='TShare.file_id == TFile.file_id', backref='t_shares')



class TUser(Base):
    __tablename__ = 't_user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    auth_string = Column(String(50))
    mail = Column(String(50))
    phone = Column(String(50))
    head = Column(String(50))
    label = Column(String(200))
    create_time = Column(DateTime)
    note = Column(Text)



class TWater(Base):
    __tablename__ = 't_water'

    water_id = Column(Integer, primary_key=True)
    water_text = Column(String(50))
    water_pos = Column(Integer)
    font_size = Column(Integer)
    font_name = Column(String(20))
    note = Column(Text)
