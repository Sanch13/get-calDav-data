from django.shortcuts import render

from rest_framework import views
from rest_framework.permissions import AllowAny


class TheFirstConferenceView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        print("USUAL REQUEST")
        return render(request=request,
                      template_name="rooms/first.html")


class TheThirdConferenceView(views.APIView):
    def get(self, request):
        print("USUAL REQUEST")

        return render(request=request,
                      template_name="rooms/third.html")
