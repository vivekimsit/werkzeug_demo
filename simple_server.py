# -*- coding: utf-8 -*- 
from werkzeug.wrappers import Response

def application(env, start_response):
    response = Response("Hello World!", mimetype='text/plain')
    return response(env, start_response)

#from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
#
#url_map = Map([
#        Rule('/', endpoint='blog/archive'),
#        Rule('/<int:year>/', endpoint='blog/archive'),
#        Rule('/<int:year>/<int:month>/<slug>', endpoint='blog/show_post'),
#        Rule('/feeds/<feed_name>.rss', endpoint='blog/show_feed')
#        ])
#
#def application(env, start_res):
#    urls = url_map.bind_to_environ(env) # Returns the MapAdapter object.
#    try:
#        endpoint, args = urls.match()
#    except HTTPException, e:
#        return e(env, start_res)
#    start_res = ('200 OK', [('Content-Type', 'text/plain')])
#    return ['Rule points to %r with arguments %r'%(endpoint, args)]

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    run_simple(
        'localhost', 5000, application, use_debugger=True,
        use_reloader=True)


