select count(file_id) cnt, concat(round(sum(file_size)/1024, 2),"K") as total_size
from t_file
where user_id=4
and file_type!=0
and date(create_time) BETWEEN  current_date-6 and current_date;


-- 查询所有文件和文件所属用户的手机号
SELECT f.*, u.phone
from t_file f
JOIN t_user u ON f.user_id = u.user_id
where f.file_type !=0