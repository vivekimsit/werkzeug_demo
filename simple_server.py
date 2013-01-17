# -*- coding: utf-8 -*- 
import os
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import SharedDataMiddleware

from jinja2 import Environment, FileSystemLoader

HOST = 'localhost'
PORT = 5000
STATIC_FOLDER = 'static'
TEMPLATE_FOLDER = 'templates'
#def application(env, start_response):
#    response = Response("Hello World!", mimetype='text/plain')
#    return response(env, start_response)

class Blog(object):
    """
    A simple blog application class.
    """
    def __init__(self):
        self.url_map = Map([
            Rule('/', endpoint='home'),
            Rule('/about/', endpoint='about'),
            Rule('/projects', endpoint='projects'),
            Rule('/posts/<int:year>/<int:month>/<int:date>', endpoint='show_post')
            ])
        # Add support for the Templates.
        template_path = os.path.join(
                            os.path.dirname(__file__), 
                            TEMPLATE_FOLDER)
        self.jinja_env = Environment(loader=FileSystemLoader(template_path))

    def __call__(self, env, start_response):
        return self.application(env, start_response)

    def render_template(self, template_name, **context):
        templ = self.jinja_env.get_template(template_name)
        return Response(templ.render(context), mimetype='text/html')

    def view_home(self, req, args):
        return self.render_template('home.html')
        #return Response("You are in home :)")

    def view_about(self, req, args):
        return Response("You are in about :)")

    # The main application callable, it will be called on each request. 
    def application(self, env, start_response):
        request = Request(env)
        urls = self.url_map.bind_to_environ(env) # Returns the MapAdapter object.
        try:
            endpoint, args = urls.match()
        except HTTPException, e:
            return e(env, start_response)
        #start_response('200 OK', [('Content-Type', 'text/plain')])
        response = getattr(self, 'view_' + endpoint)(request, args)
        return response(env, start_response)
        #return ['Rule points to %r with arguments %r'%(endpoint, args)]

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = Blog()
    static_path = os.path.join(os.path.dirname(__file__), STATIC_FOLDER)
    # Apply a wrapper around the callable application.
    #app.application = SharedDataMiddleware(
    #                        app.application, 
    #                        {
    #                            '/static': static_path, 
    #                        })
    run_simple(
        HOST, PORT, app, use_debugger=True,
        use_reloader=True)
