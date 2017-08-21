#coding:utf-8
__author__ = 'Administrator'
import helper

if __name__ == '__main__':
    try:
        n = '1'
        n = int(n)
        ret = helper.f1()
        if ret:
            print 'success'
        else:
            #print u"失败"
            raise Exception('false')    #出错时，主动触发异常
    except Exception,e:
        print u"出现错误！"
        print e
    finally:
        # 断开连接，释放资源（数据库、redis等）
        pass

