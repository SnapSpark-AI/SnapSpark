imagename = file.filename
img = PIL.Image.open(imagename)
exif = {
    PIL.ExifTags.TAGS[k]: v
    for k, v in img._getexif().items
    if k in PIL.ExifTags.TAGS
}
    
north = exif['GPSinfo'][2]
east = exif['GPSinfo'][4]
    
latitude = (((north[0]*60)+north[1]*60)+north[2])/60/60
longitude = (((east[0]*60)+east[1]*60)+east[2])/60/60

file_location = subprocess.run(['pwd'], capture_output=True, text=True)
file_location = file_location.stdout