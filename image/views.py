from django.shortcuts import render
from django.http import HttpResponseRedirect
from json import dumps 

from  .forms import Image
from .exif import handle_uploaded_image

def upload_file(request):
    if request.method == 'POST':
        form = Image(request.POST, request.FILES)
        if form.is_valid():
            result = handle_uploaded_image(request.FILES['file'])
            dataJSON = dumps(result)
            return render(request, 'map.html', {'data': dataJSON})
    else:
        form = Image()
    return render(request, 'upload.html', {'form': form})


