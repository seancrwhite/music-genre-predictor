import os
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.conf import settings
from django.views.generic.edit import FormView
# from music.forms import ProfileForm
# from music.models import Profile
# from django.http import JsonResponse
# from django.views.decorators.http import require_POST
#
#
def index(request):
    return render(request, 'music/home.html')

def contact(request):
    return render(request, 'music/basic.html', {'content':[]})
