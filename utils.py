# -*- coding: utf-8 -*-
# author: Yabin Zheng
# Email: sczhengyabin@hotmail.com

import chromedriver_autoinstaller

def gen_valid_dir_name_for_keywords(keywords):
    keep = ["-", "_", "."]
    keywords = keywords.replace(" ", "_").replace(":", "-")
    return "".join(c for c in keywords if c.isalnum() or c in keep).rstrip()
