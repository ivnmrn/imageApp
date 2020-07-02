from django.shortcuts import render
from django.http import HttpResponseRedirect

from  .forms import Image
from .exif import handle_uploaded_image

def upload_file(request):
    if request.method == 'POST':
        form = Image(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_image(request.FILES['file'])
            return render(request, 'map.html', {})
    else:
        form = Image()
    return render(request, 'upload.html', {'form': form})


