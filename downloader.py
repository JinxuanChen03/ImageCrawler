from __future__ import print_function

import shutil
import imghdr
import os
import concurrent.futures
import requests
import socket
from PIL import Image

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Proxy-Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
    # 'Connection': 'close',
}


def convert_to_jpg(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    for filename in os.listdir(src_dir):
        if filename.lower().endswith(('.png', '.jpeg', '.bmp', '.webp')):
            src_path = os.path.join(src_dir, filename).replace("\\", "/")
            file_base, _ = os.path.splitext(filename)  # 分离文件名和扩展名
            dst_path = os.path.join(dst_dir, file_base + '.jpg').replace("\\", "/")

            try:
                image = Image.open(src_path)
                # 如果图片包含透明通道，则转换为RGB
                if image.mode in ('RGBA', 'LA'):
                    image = image.convert('RGB')
                image.save(dst_path, 'JPEG')
                # print(f"Converted {src_path} to {dst_path}")
                os.remove(src_path)
                # print(f"Deleted original image: {src_path}")
            except Exception as e:
                print(f"Error converting {src_path}: {e}")

def download_image(image_url, dst_dir, file_name, timeout=20, proxy_type=None, proxy=None):
    proxies = None
    if proxy_type is not None:
        proxies = {
            "http": proxy_type + "://" + proxy,
            "https": proxy_type + "://" + proxy
        }

    response = None
    file_path = os.path.join(dst_dir, file_name).replace("\\", "/")
    try_times = 0
    while True:
        try:
            try_times += 1
            response = requests.get(
                image_url, headers=headers, timeout=timeout, proxies=proxies)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            response.close()
            file_type = imghdr.what(file_path)
            # if file_type is not None:
            if file_type in ["jpg", "jpeg", "png", "bmp", "webp"]:
                new_file_name = "{}.{}".format(file_name, file_type)
                new_file_path = os.path.join(dst_dir, new_file_name).replace("\\", "/")
                shutil.move(file_path, new_file_path)
                print("## OK:  {}  {}".format(new_file_name, image_url))
                convert_to_jpg(dst_dir,dst_dir)
                return True
            else:
                os.remove(file_path)
                print("## Err: TYPE({})  {}".format(file_type, image_url))
            break
        except Exception as e:
            if try_times < 3:
                continue
            if response:
                response.close()
            print("## Fail:  {}  {}".format(image_url, e.args))
            break
    return False


def download_images(image_urls, dst_dir, file_prefix="img", concurrency=50, timeout=20, proxy_type=None, proxy=None):
    """
    Download image according to given urls and automatically rename them in order.
    :param timeout:
    :param proxy:
    :param proxy_type:
    :param image_urls: list of image urls
    :param dst_dir: output the downloaded images to dst_dir
    :param file_prefix: if set to "img", files will be in format "img_xxx.jpg"
    :param concurrency: number of requests process simultaneously
    :return: none
    """

    socket.setdefaulttimeout(timeout)

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        future_list = list()
        count = 0
        success_count = 0
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for image_url in image_urls:
            # 多张图恢复此注释
            # file_name = file_prefix + "_" + "%04d" % count

            #单张图使用此路径
            file_name = file_prefix

            future_list.append(executor.submit(
                download_image, image_url, dst_dir, file_name, timeout, proxy_type, proxy))
            count += 1

        for future in concurrent.futures.as_completed(future_list):
            if future.result():  # 如果下载成功，增加计数器
                success_count += 1

        concurrent.futures.wait(future_list, timeout=180)

        return success_count
