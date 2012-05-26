from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def hello(request):
    return HttpResponse('hello, libauth')

