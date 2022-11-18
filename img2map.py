from PIL import Image
import random

if __name__ == '__main__':
    # the color of the seperating line as aim of the clustering
    sep = 400
    # scale the sep to RGB color range
    N = 1
    im = Image.open(input('img:'))
    pix = im.load()
    s = ""
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            if sum(pix[x,y]) > sep*N:
                s += str(int(random.uniform(0, sep)))
            else:
                s += str(int(random.uniform(sep, 765/N)))
            s += ','
    print(s[:-1:])