from django.shortcuts import render


def show_main_page(request):
    return render(request, 'example.html')