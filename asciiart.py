from PIL import Image
import random
import argparse

# Require a file with regular expressions in it passed as a paramater
parser = argparse.ArgumentParser()
parser.add_argument('file', help='file input')
parser.add_argument('--keep-image','-i', help='write image of ascii out', action=('store_true'))
parser.add_argument('--nearest-neighbor','-nn', help='scale the image down', action=('store_true'))
args = parser.parse_args()

value = ['@','W','M', '&', '$', '?', '!', ',', '.', '`', ' ']

def asciiFromFloat(f):
        return value[int(f*10.)]

art = open('test.txt','w')
im = Image.open(args.file)
if args.keep_image:
    im_out = Image.new('L',im.size)
size = im.size
for j in range(0,size[1]):
    for i in range(0,size[0]):
        pix = im.getpixel((i,j))
        if args.keep_image:
            im_out.putpixel((i,j),(pix[0] + pix[1] + pix[2])/3)
        art.write(asciiFromFloat(round(((pix[0] + pix[1] + pix[2])//3)/256.0, 1)))
    art.write('\n')

art.close()
if args.keep_image:
    im_out.save('out.png')
