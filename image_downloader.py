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
    parser.add_argument("--excel_file", "-f", type=str, default="./superstars/test.xlsx",
                        help='Excel文件路径')
    parser.add_argument("--column_name", "-c", type=str, default="姓名",
                        help='指定列名')
    # 需下载多张图恢复此注释
    # parser.add_argument("--max-number", "-n", type=int, default=1,
    #                     help="下载的图片数")
    parser.add_argument("--output", "-o", type=str, default="./images",
                        help="输出文件路径")
    args = parser.parse_args(args=argv)

    # 验证 max-number 不会超过 10000
    # if args.max_number > 10000:
    #     print("Max number should not exceed 10000.")
    #     return

    # 读取 Excel 文件
    df = pd.read_excel(args.excel_file)

    # 添加一个新的列来存储下载的图片数
    df["下载图片数"] = 0

    # 遍历关键词列
    for index, row in df.iterrows():
        keyword = row[args.column_name]

        crawled_urls = crawler.crawl_image_urls(keyword, max_number=1,
                                                proxy_type=None, proxy=None)

        # 需下载多张图片时，恢复此注释
        # file_addr = os.path.join(args.output, utils.gen_valid_dir_name_for_keywords(keyword))

        # 单张使用此路径
        file_addr = args.output

        os.makedirs(file_addr, exist_ok=True)

        downloaded_count = downloader.download_images(image_urls=crawled_urls, dst_dir=file_addr.replace("\\", "/"),
                                                      concurrency=50, timeout=10,
                                                      proxy_type=None, proxy=None,
                                                      file_prefix=keyword)

        # 更新下载的图片数到 DataFrame
        df.at[index, "下载图片数"] = downloaded_count

        print(f"Finished processing keyword: {keyword}")
        print(f"Successfully downloaded {downloaded_count} images.")

    # 将更新后的 DataFrame 写回到 Excel 文件
    df.to_excel(args.excel_file, index=False)
    print(f"Excel file updated: {args.excel_file}")

    print("All done.")


if __name__ == '__main__':
    main(sys.argv[1:])

# python image_downloader.py -f ./superstars/test.xlsx -c 姓名 -n 1 -o ./images