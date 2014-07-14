#!/usr/bin/env python2
from tornado.web import Application, RequestHandler, authenticated
from tornado.ioloop import IOLoop
import os;

import tornado
import tornado.auth
import tornado.web

import json
import logging


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("name")

class LoginHandler(BaseHandler):
    def get(self):
        self.render('templates/login')

    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("name")
        self.clear_cookie("id")
        self.redirect('/')

class TopHandler(BaseHandler):
    def get(self):
#         logging.debug('top page get')
        self.render("templates/index")


class MypageHandler(BaseHandler):
    @authenticated
    def get(self):
        tmps = {}
        todo_data = database.get_todo_divide_data(self.get_secure_cookie('id'))
        tmps['get_rdata'] = todo_data['nonull']
        tmps['get_nrdata'] = todo_data['null']
#        tmps['get_data'] = database.find_todo_data(self.get_secure_cookie("id"))
        tmps['delete_data'] = database.delete_todo_data
        tmps['context'] = True
#         logging.debug('mypage get')
        self.render("templates/mypage",
                **tmps)


    @authenticated
    def post(self):
        del_task= self.get_argument('del' ,None)
        #if push delete button
        if del_task:
#             print('delete')
#             print(del_task)
            database.delete_todo_data(self.get_secure_cookie('id'),
                                      del_task)
        #if push submit button
        else:
            classifide = self.get_argument('classifide', None)
            context = self.get_argument('context', None)
            rimit = self.get_argument('rimit', None)
#             print(classifide)
#             print(context)
#             print(rimit)

            if context:
#                 print(context)
                database.insert_todo_data(
                        self.get_secure_cookie('id'),
                        classifide,
                        context,
                        rimit)
            else:
#                 print('none')
                pass
#         logging.debug('mypage post')
        self.redirect('/mypage')

#twitter authenticated
class TwitterAuthHandler(BaseHandler, tornado.auth.TwitterMixin):
#    _OAUTH_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
#    _OAUTH_VERSION = '1.0'
#    _OAUTH_NO_CALLBACKS = False

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect()

    @DBManager.decorate_with_line
    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter auth failed")

#        data = tornado.escape.json_encode(user)
#        data = json.load(user)
        #debug
#        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        #user is dictionary
#        self.set_secure_cookie("user", user["username"])
#         print(user['access_token']['user_id'])
        logging.debug('User: ' + user['access_token']['user_id'])
        data = database.find_user_data(int(user['access_token']['user_id']))
        if not len(data):
#             print('not found')
            tmp = user['access_token']
            database.insert_user_data(tmp['user_id'],
                                      tmp['screen_name'],
                                      tmp['key'],
                                      tmp['secret'])

            #TODO: add question abour 'do you want to register?'
            self.set_secure_cookie('name', tmp['screen_name'])
            self.set_secure_cookie('id', tmp['user_id'])

        else:
#             print('found')
            self.set_secure_cookie('name', data['name'])
            self.set_secure_cookie('id', str(data['id']))

        self.redirect('/')




    def _oauth_consumer_token(self):
        consumer_token = {'key' : 'zN2WcTWHHmTsXIchruaeRw',
                          'secret' : '2AB4lHdkWY8SnvfTCfpwo5NHXSCbAW0jUT3lRQoM'
                          }
        return consumer_token




if __name__ == '__main__':
    database = DBManager.DBManager()

    settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "cookie_secret":'8dfjh4=fkaldsf824jkf-2klfdjafjkaer8',
            "login_url": "/"
            }

    logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s [%(levelname)s] %(message)s'
                )


    app = Application([
        (r'/', TopHandler),
        (r'/mypage', MypageHandler),
        (r'/logout', LogoutHandler),
        (r'/twAuth', TwitterAuthHandler)
        ], **settings)

    logging.debug('start application')

    app.listen(8000)
#     context = DaemonContext(
#            working_directory = '/',
#            umask = 0o002
#            pidfile = PIDLockFile('task_backend.pid')
#             )

    t = tornado.ioloop.IOLoop.instance()
    t.start() 
    
