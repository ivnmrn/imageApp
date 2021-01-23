from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS
import requests


def get_city_name(longitude, latitude):
    token = 'YOUR_TOKEN'
    url = f'https://api.mapbox.com/geocoding/v5/mapbox.places/{latitude},{longitude}.json?access_token={token}'
    response = requests.get(url)
    return response.json()['features'][0]['place_name']


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
        raw_coordinates = get_degrees(exif)
        coordinates = get_latitude_longitude(raw_coordinates)
        location = get_city_name(coordinates['latitude'], coordinates['longitude'])
        return dict(coordinates=coordinates, exif=exif)
    else:
        return dict(exif=exif)