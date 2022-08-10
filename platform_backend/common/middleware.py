from django.http import HttpResponse


class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META["PATH_INFO"] == "/healthcheck/":
            return HttpResponse("ok")

        response = self.get_response(request)

        return response
