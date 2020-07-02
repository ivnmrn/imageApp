from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS

def get_decimal_from_dms(dms, ref):

    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0

    if ref in ['S', 'W']:
        degrees = -degrees
        minutes = -minutes
        seconds = -seconds

    return round(degrees + minutes + seconds, 5)

def get_latitude_longitude(geotags):
    lat = get_decimal_from_dms(geotags['GPSLatitude'], geotags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geotags['GPSLongitude'], geotags['GPSLongitudeRef'])

    return lon, lat

def get_degrees(exif):

    geo = {}
    for key, val in exif['GPSInfo'].items():
        if GPSTAGS[key][:4] == 'GPSL':
            geo[GPSTAGS[key]] = val
    return geo

def handle_uploaded_image(image):

    img = Image.open(image)
    exif = {}

    try:
        for key, value in img._getexif().items():
            if key in ExifTags.TAGS and key != 37500:
                exif[ExifTags.TAGS[key]] = value
        # print(exif)
        if 'GPSInfo' in exif:
            cordenates = get_degrees(exif)
            location = get_latitude_longitude(cordenates)
            print(location)
        else:
            print('dep')
            # get_exif(exif)
    except AttributeError:
        raise ValueError









# def get_exif(exif):

#     expected_values = ['Make', 'Model', 'Software', 'DateTimeOriginal', 'ColorSpace']

#     for key, val in exif.items():
#         if key in expected_values:
#             print(key, val)