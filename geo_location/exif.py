from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS


def get_decimal_from_dms(dms, ref):
    degrees = dms[0][0] / dms[0][1]
    minutes = dms[1][0] / dms[1][1] / 60.0
    seconds = dms[2][0] / dms[2][1] / 3600.0
    if ref in ['S', 'W']:
        degrees *= -1
        minutes *= -1
        seconds *= -1
    return round(degrees + minutes + seconds, 5)


def get_latitude_longitude(geo_tags):
    lat = get_decimal_from_dms(geo_tags['GPSLatitude'], geo_tags['GPSLatitudeRef'])
    lon = get_decimal_from_dms(geo_tags['GPSLongitude'], geo_tags['GPSLongitudeRef'])
    return dict(latitude=lat, longitude=lon)


def get_degrees(exif):
    geo = {}
    for key, val in exif['GPSInfo'].items():
        if GPSTAGS[key][:4] == 'GPSL':
            geo[GPSTAGS[key]] = val
    return geo


def handle_uploaded_image(image):
    img = Image.open(image)
    exif = {}
    if img._getexif():
        for key, value in img._getexif().items():
            if key in ExifTags.TAGS and key != 37500:
                exif[ExifTags.TAGS[key]] = value

    if 'GPSInfo' in exif and exif['GPSInfo'][2] != ((0, 0), (0, 0), (0, 0)):
        coordinates = get_degrees(exif)
        location = get_latitude_longitude(coordinates)
        result = dict(location=location, exif=exif)
        return result
    else:
        result = dict(exif=exif)
        return result