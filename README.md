# 人像抓取器

在Bing浏览器中抓取指定人名的人像图。

#### 获取人名表格

运行以下命令获取人名表格。

```console
python gen_excel.py -o ./superstars -f test.xlsx
```

参数解释：

-o <文件保存路径> 选填，不填默认保存到`./superstars`

-f <文件名称> 必填。

如需更改人名请更改`gen_excel.py`文件中的`name`列表。



表格格式默认为

| 姓名 | 图片数 |
| ---- | ------ |

#### 获取人像图片

运行以下命令获取人像图片

```
python image_downloader.py -f ./superstars/test.xlsx -c 姓名 -n 10 -o ./images
```

参数解释：

-f <Excel文件路径> 必填。

-c <保存人名的列名> 选填，默认为`姓名`

-n <下载的图片数> 选填，默认为`10`，单人最大下载图片数为`10000`张。
-o <输出文件路径> 选填，默认为`./images`。

