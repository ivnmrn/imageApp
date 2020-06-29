from PIL import Image, ExifTags
from PIL.ExifTags import TAGS, GPSTAGS

def cordenates(filepath):
    img = Image.open(filepath)
    exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
    print(exif)
    # for (idx, tag) in TAGS.items():
    #     if tag == 'GPSInfo':
    #         for (key, val) in GPSTAGS.items():
    #             if key in exif[idx]:
    #                 print(val)