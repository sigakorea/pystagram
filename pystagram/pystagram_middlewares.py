from django.conf import settings
from django.shortcuts import render
from blog.exceptions import HelloWorldError
from blog.models import Post


class PystagramMiddleware(object):
    def process_request(self, request):
        try:
            request.last_post = Post.objects.all()[1]
        except Post.DoesNotExist:
            request.last_post = None

    def process_exception(self, request, exc):
        if isinstance(exc, HelloWorldError):
            ctx = {
                'status': 599, 'error': 'hello world error'
            }
        else:
            ctx = {
                'status': 500, 'error': 'Something wrong'
            }

        _res = render(request, 'blog/error.html', ctx)
        _res.status_code = ctx['status']
        return _res
