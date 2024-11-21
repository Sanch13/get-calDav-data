from django.shortcuts import render


def first_room(request):
    return render(request=request,
                  template_name="rooms/first.html")


def third_room(request):
    return render(request=request,
                  template_name="rooms/third.html")
