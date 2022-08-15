from platform_backend.common.api.mixins import APIErrorsMixin, PublicAPIView
from rest_framework.views import APIView

class GetAvailableUserPromoAPIView(APIErrorsMixin, APIView):
    def get(self, request):
        