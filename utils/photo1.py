import glob
import os
from PIL import Image
from data.user_module import User
from data.connect import session

def get_imgs(path):
    """
    获取对应目录的所有图片
    :param path:
    :return:
    """
    return glob.glob('{}/*.jpg'.format(path))

def sava_upload(upload_img):
    sava_to = 'static/face_upload/{}'.format(upload_img['filename'])
    with open(sava_to, 'wb') as fh:
        fh.write(upload_img['body'])
    return sava_to

def make_thumb(save_to):
    size = (200, 200)
    im = Image.open(save_to)
    im.thumbnail(size)
    name, ext = os.path.splitext(os.path.basename(save_to))
    im.save('static/upload/thumb/{}_{}x{}{}'.format(
        name, size[0], size[1], ext
    ))

# def add_post_for(username, image_url, thumb_url):
#     """
#     保存用户上传的图片信息
#     :param username:
#     :param image_url:
#     :param thumb_url:
#     :return:
#     """
#     user = session.query(User).filter(name = username).first()
#     # post =



