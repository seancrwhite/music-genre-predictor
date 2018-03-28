# # -*- coding: utf-8 -*-
# from __future__ import unicode_literals
#
# from django.shortcuts import render
# from uploader.models import UploadForm,Upload
# from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
# # Create your views here.
# def home(request):
# 	if request.method=="POST":
# 		img = UploadForm(request.POST, request.FILES)
# 		if img.is_valid():
# 			img.save()
# 			return HttpResponseRedirect(reverse('imageupload'))
# 	else:
# 		img=UploadForm()
# 	images=Upload.objects.all()
# 	return render(request,'home.html',{'form':img,'images':images})

# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from mysite.blog.models import Document
from mysite.blog.forms import DocumentForm


def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(
        request,
        'list.html',
        {'documents': documents, 'form': form}
    )