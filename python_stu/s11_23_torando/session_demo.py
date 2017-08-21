#coding:utf-8
__author__ = 'xuefeng'

from hashlib import sha1
import os, time

session_container = {}
create_session_id = lambda: sha1('%s%s' % (os.urandom(16), time.time())).hexdigest()
class Session(object):

    session_id = "__sessionId__"

    def __init__(self, request):
        session_value = request.get_cookie(Session.session_id)
        if not session_value:
            self._id = create_session_id()
        else:
            self._id = session_value
        request.set_cookie(Session.session_id, self._id)

    def __getitem__(self, key):     #类似字典操作 Session[key]，外部调用时自动触发
        ret = None
        try:
            ret = session_container[self._id][key]
        except Exception as e:
            pass

        return ret

    def __setitem__(self, key, value):  #类似字典操作 Session[key] = value
        if session_container.has_key(self._id):
            session_container[self._id][key] = value
        else:
            session_container[self._id] = {key: value}

    def __delitem__(self, key):     #类似字典操作 del Session[key]
        del session_container[self._id][key]
