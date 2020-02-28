#!/bin/bash

if [ -d fms_api_server ]; then
   cd fms_api_server
   git pull
else
   git clone https://github.com/disenQF/fms_api_server.git
   ## fms_api_server
   cd fms_api_server
fi

if [ ! -d /root/venvs/fms_api_server ]; then 
   echo "正在创建环境"     
   virtualenv /root/venvs/fms_api_server -p python3	
   pip install gunicorn oss2  -i https://mirrors.aliyun.com/pypi/simple
fi

source /root/venvs/fms_api_server/bin/activate

echo "正在更新安装依赖包"
pip install -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple

gunicorn server:app -b 0.0.0.0:$1 -w 2 $2 

