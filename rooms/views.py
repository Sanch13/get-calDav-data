from django.shortcuts import render

from rest_framework import views
from rest_framework.permissions import AllowAny


class TheFirstConferenceView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request=request,
                      template_name="rooms/index_old.html")
