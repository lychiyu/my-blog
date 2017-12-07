# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import traceback
from django.http import HttpResponse, JsonResponse


class EnhanceMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get('HTTP_X_FORWARDED_FOR'):
            request.ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
        else:
            request.ip = request.META['REMOTE_ADDR']

        response = self.get_response(request)
        if type(response) in [str]:
            response = HttpResponse(response)
        elif type(response) in [dict, list]:
            response = JsonResponse(response)
        if response.status_code == 500:
            # TODO: 发邮件通知管理员
            traceback.print_exc()
        return response
