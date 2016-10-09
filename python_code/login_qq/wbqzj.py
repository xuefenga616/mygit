#coding:utf-8
import re

def qwb(text, start_str, end_str):
    cmp = re.compile(start_str+'(.*?)'+end_str,re.S)
    result = cmp.search(text)
    return result and result.group(1)

if __name__ == '__main__':
    text = '<span id="txtCity">深圳</span>'

    s1 = 'id="txtCity">'
    s2 = '</span>'
    print(qwb(text,s1,s2))
