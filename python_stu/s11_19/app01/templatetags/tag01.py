#coding:utf-8
__author__ = 'xuefeng'
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def my_simple_time(v1,v2,v3):
    return  v1 + v2 + v3

@register.simple_tag
def my_input(id,arg):
    result = "<input type='text' id='%s' class='%s' />" %(id,arg,)
    return mark_safe(result)

@register.simple_tag
def errors_msg(error_list):
    if error_list:
        return error_list[0]
    return ''