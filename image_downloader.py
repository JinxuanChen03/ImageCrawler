from __future__ import print_function

import argparse
import sys

import crawler
import downloader
import utils
import pandas as pd
import os

def main(argv):
    parser = argparse.ArgumentParser(description="Image Downloader")
    parser.add_argument("--excel_file", "-f", type=str,
                        help='Excel文件路径')
    parser.add_argument("--column_name", "-c", type=str, default="姓名",
                        help='指定列名')
    parser.add_argument("--max-number", "-n", type=int, default=10,
                        help="下载的图片数")
    parser.add_argument("--output", "-o", type=str, default="./images",
                        help="输出文件路径")
    args = parser.parse_args(args=argv)

    # 验证 max-number 不会超过 10000
    if args.max_number > 10000:
        print("Max number should not exceed 10000.")
        return

    # 读取 Excel 文件
    df = pd.read_excel(args.excel_file)

    # 遍历关键词列
    for keyword in df[args.column_name]:
        crawled_urls = crawler.crawl_image_urls(keyword, max_number=args.max_number,
                                                proxy_type=None, proxy=None)

        file_addr = os.path.join(args.output, utils.gen_valid_dir_name_for_keywords(keyword))
        os.makedirs(file_addr, exist_ok=True)

        downloader.download_images(image_urls=crawled_urls, dst_dir=file_addr,
                                   concurrency=50, timeout=10,
                                   proxy_type=None, proxy=None,
                                   file_prefix="Bing")

        print(f"Finished processing keyword: {keyword}")

    print("All done.")


if __name__ == '__main__':
    main(sys.argv[1:])

# python image_downloader.py -f ./superstars/female.xlsx -c 姓名 -n 10 -o ./images