import glob
import os
import time
from PIL import Image
from io import BytesIO
import base64
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
    image_name = upload_img['filename']
    today = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    new_name = today + image_name
    sava_to = 'static/face_upload/{}'.format(new_name)
    bytes_stream = BytesIO(upload_img["body"])
    roiimg = Image.open(bytes_stream)
    resized_image = roiimg.resize((50, 50), Image.ANTIALIAS)
    imgByteArr = BytesIO()
    resized_image.save(imgByteArr, format='PNG')
    imgByteArr = imgByteArr.getvalue()
    print("res:",imgByteArr)
    print(type(resized_image))
    with open(sava_to, 'wb') as fh:
        fh.write(imgByteArr)
    return sava_to

def save_upload_log(upload_logo):
    image_name = upload_logo['filename']
    today = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    new_name = today + image_name
    if not os.path.exists('static/movie_upload'):
        os.makedirs('static/movie_upload')
        os.chmod(int('static/movie_upload'),'rw')
    sava_to = 'static/movie_upload/{}'.format(new_name)
    with open(sava_to, 'wb') as fh:
        fh.write(upload_logo['body'])
    return sava_to

def save_upload_Plog(upload_logo):
    image_name = upload_logo['filename']
    today = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    new_name = today + image_name
    if not os.path.exists('static/pview_upload'):
        os.makedirs('static/pview_upload')
        os.chmod(int('static/pview_upload'),'rw')
    sava_to = 'static/P_movie_upload/{}'.format(new_name)
    with open(sava_to, 'wb') as fh:
        fh.write(upload_logo['body'])
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

from PIL import Image


def produceImage(file_in, width, height, file_out):
    image = Image.open(file_in)
    resized_image = image.resize((width, height), Image.ANTIALIAS)
    resized_image.save(file_out)


# if __name__ == '__main__':
#     file_in = '1寸.jpg'
#     width = 180
#     height = 240
#     file_out = '1.jpg'
#     produceImage(file_in, width, height, file_out)