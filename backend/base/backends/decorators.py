from django.shortcuts import redirect
from functools import wraps

from .authenticate import ExpiredTokenAuthentication


def token_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.COOKIES.get('token')
        if token:
            try:
                temp = ExpiredTokenAuthentication().authenticate_credentials(token)
                request.user = temp[0]
                return view_func(request, *args, **kwargs)
            except:
                return redirect('login')
        else:
            return redirect('login')
    return wrapper
