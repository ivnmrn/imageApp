from PIL import Image, ExifTags

def handle_uploaded_file(filepath):
    img = Image.open(filepath)
    exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
    print(exif)
