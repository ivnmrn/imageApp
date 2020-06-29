from django.shortcuts import render
from django.http import HttpResponseRedirect

from  .forms import Image
from .testss import cordenates

def upload_file(request):
    if request.method == 'POST':
        form = Image(request.POST, request.FILES)
        if form.is_valid():
            cordenates(request.FILES['file'])
            return HttpResponseRedirect('test/')
    else:
        form = Image()
    return render(request, 'upload.html', {'form': form})