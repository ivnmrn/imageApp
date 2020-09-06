from django.shortcuts import render
from json import dumps

from .forms import Image
from .exif import handle_uploaded_image


def upload_file(request):
    if request.method == 'POST':
        form = Image(request.POST, request.FILES)
        if form.is_valid():
            result = handle_uploaded_image(request.FILES['file'])
            if 'location' in result:
                data_json = dumps(result['location'])
                return render(request, 'map.html', {'coordinates': data_json,
                                                    'exif': result['exif']
                                                    })
            else:
                return render(request, 'map_no_coordinates.html')
    else:
        form = Image()
    return render(request, 'upload.html', {'form': form})
