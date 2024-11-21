# 人像抓取器

在Bing浏览器中抓取指定人名的人像图。

#### 获取人名表格

运行以下命令生成人名表格：

```
python gen_excel.py -o ./superstars -f test.xlsx
```

参数解释：

-o <文件保存路径> 选填，不填默认保存到`./superstars`

-f <文件名称> 选填，不填默认为`test.xlsx`

如需更改人名请更改`gen_excel.py`文件中的`name`列表。

#### 获取人像图片

运行以下命令抓取人像图片：

```
python image_downloader.py -f ./superstars/test.xlsx -c 姓名 -n 10 -o ./images
```

参数解释：

-f <Excel文件路径> 选填，不填默认为`./superstars/test.xlsx`

-c <保存人名的列名> 选填，不填默认为`姓名`

-n <下载的图片数> 选填，不填默认为`10`，单人最大下载图片数为`10000`张。

-o <输出文件路径> 选填，不填默认为`./images`。

#### 输出结果

默认输出为：

人名表格储存在`./superstars/test.xlsx`，格式为：

| 姓名 | 下载图片数 |
| ---- | ---------- |

下载的照片以人名作为文件夹名称，分别储存在`./images/<人名>/`。

如需更改储存路径只需在命令中指定参数。

**注意：关闭代理后再使用人像抓取器。**

