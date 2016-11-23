import base64
import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render


logger = logging.getLogger(__name__)


@login_required
def dummy(request):
    return render(request, 'ws-test.html')


def auth(request):
    if not request.user.is_authenticated():
        return HttpResponse('NOPE', status=401)
    response = HttpResponse('OK')
    response['Authorization'] = 'Basic %s' % base64.b64encode('bob:changeme')
    logger.info(response.get('Authorization'))
    return response


def log(request):
    logger.info(request.META)
    return HttpResponse('OK')
