from django.shortcuts import render

def index(request):
    return render(request, 'music/home.html')

def contact(request):
    return render(request, 'music/basic.html', {'content':['If you would like to contact me, please email me','hskinsley@gmail.com']})
