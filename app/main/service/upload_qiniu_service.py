from app.main import qiniu_store
import random, string
import os

def random_name(num=7):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(num))

def save_new_image(file, sfx):
    key = random_name() + "." + sfx
    ret, info = qiniu_store.save(file, key)
    if(info.status_code == 200):
        # 上传到 qiniu 成功后，就删掉本地临时文件
        # 先检查本地是否存在该文件，防止报错
        if os.path.exists(file):
            os.remove(file)
        return {
            "status": "success",
            "message": "file upload success",
            "data": ret
        }
    else:
        return {
            "status": "fail",
            "message": str(ret) + str(info)
        }

def get_image(key):
    return {
            "status": "success",
            "data": qiniu_store.url(key)
        } 

def get_config():
    return {
        "status":"success",
        "data": {
            'qiniu_bucket_domain': qiniu_store.url('')
        }
    }

def delete_image(key):
    ret, info = qiniu_store.delete(key)
    if(info.status_code == 200):
        return {
            "status": "success",
            "message": "file delte success"
        }
    elif(info.status_code == 612):
        return {
            "status": "fail",
            "message": "file key is not exit"
        }