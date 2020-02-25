#!/usr/bin/python3
# coding: utf-8

from db import db_conn


def query(sql, *args, **kwargs):
    with db_conn as cursor:
        cursor.execute(sql, args=(args if args else kwargs))
        if cursor.rowcount > 0:
            return cursor.fetchall()


if __name__ == '__main__':
    sql = """
        SELECT count(file_id) cnt, concat(round(sum(file_size)/1024, 2),"K") AS total_size
        FROM t_file
        WHERE user_id=%(user_id)s
        AND file_type!=%(file_type)s
        AND date(create_time) BETWEEN  current_date-6 AND current_date;
    """
    print(query(sql, user_id=6, file_type=0))

    sql2 = """
    SELECT f.*, u.phone
    from t_file f
    JOIN t_user u ON f.user_id = u.user_id
    where f.file_type = %s
    """

    print(query(sql2, 1))

