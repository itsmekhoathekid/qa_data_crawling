import os
from PIL import Image  # pip install pillow

output_dir = './PDFs'
source_dir = './Images'

for file in os.listdir(source_dir):
    if file.split('.')[-1] in ('png', 'jpg', 'jpeg'):
        image = Image.open(os.path.join(source_dir, file))
        image_converted = image.convert('RGB')
        image_converted.save(os.path.join(output_dir, '{0}.pdf'.format(file.split('.')[-2])))