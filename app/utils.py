#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re

class Utils:
    def filter_tags(self,htmlstr):
        # 先过滤CDATA
        re_cdata = re.compile('//<![CDATA[[^>]*//]]>', re.I)  # 匹配CDATA
        re_script = re.compile('<s*script[^>]*>[^<]*<s*/s*scripts*>', re.I)  # Script
        re_style = re.compile('<s*style[^>]*>[^<]*<s*/s*styles*>', re.I)  # style
        re_br = re.compile('<brs*?/?>')  # 处理换行
        re_h = re.compile('</?w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_cdata.sub('', htmlstr)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('n+')
        s = blank_line.sub('n', s)
        s = self.replaceCharEntity(s)  # 替换实体
        return s

    def replaceCharEntity(self,htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }

        re_charEntity = re.compile(r'&#?(?P<name>w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # entity全称，如>
            key = sz.group('name')  # 去除&;后entity,如>为gt
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

    def repalce(self,s, re_exp, repl_string):
        return re_exp.sub(repl_string, s)

    def subStr(self,s, length):
        return s.decode('utf8')[0:length].encode('utf8')

    def reImg(self,html):
        reg = r'https://[^\s]*?\.jpg'
        imgre = re.compile(reg)  # 转换成一个正则对象
        imglist = imgre.findall(html)  # 表示在整个网页过滤出所有图片的地址，放在imgList中
        return imglist
