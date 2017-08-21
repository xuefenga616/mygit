#coding:utf-8
__author__ = 'xuefeng'
from django import template
register = template.Library()

@register.simple_tag
def build_comment_tree(comment_list):
    #print "comment_list:",comment_list

    comment_dic = {}
    for comment_obj in comment_list:
        if comment_obj.parent_comment is None:  #顶级评论
            comment_dic[comment_obj] = {}
            #{A:
            # {A2:{
            #   A3-1:{},
            #   A3-2:{}
            #     }
            #  }
            #}
        else:
            tree_search(comment_dic,comment_obj)

    # 开始拼接html str
    html = "<div class='comment-box'>"
    margin_left = 0     #缩进值默认等于0,下面每层加缩进
    for k,v in comment_dic.items():
        print k,v
        html += "<div class='comment-node'>" + k.comment + "</div>"
        html += generate_comment_html(v,margin_left+20)     #下级评论树
    html += "</div>"
    return html


def tree_search(d_dic,comment_obj):
    for k,v_dic in d_dic.items():
        if k == comment_obj.parent_comment: #find parent
            d_dic[k][comment_obj] = {}
            return
        else:   #going deeper...
            tree_search(d_dic[k],comment_obj)

def generate_comment_html(sub_comment_dic,margin_left_val):
    html = ""
    for k,v_dic in sub_comment_dic.items():
        html += "<div style='margin-left: %spx' class='comment-node'>" %margin_left_val + k.comment + "</div>"
        if v_dic:
            html += generate_comment_html(v_dic,margin_left_val+20)    #下面还有则递归找
    return html









