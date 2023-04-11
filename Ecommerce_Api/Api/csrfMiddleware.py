from django.middleware.csrf import CsrfViewMiddleware
from django.http import HttpResponseForbidden

class csrfMiddleware(CsrfViewMiddleware):
    def process_exception(self, request, exception):
        if isinstance(exception, Forbidden):
            return HttpResponseForbidden('CSRF Token not provided or incorrect')
        else:
            return super().process_exception(request, exception)
