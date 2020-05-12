#
# tfairchild3  September 2015
#
# AgentImage represents the class used for performing common functions
# on the input images
#

from PIL import Image
import logging

__author__ = 'tfairchild'


class AgentImage:
    def __init__(self):
        pass

    #
    # open_problem_image
    # opens file
    # returns file handle
    #
    def open_problem_image(self,fname):
        return Image.open(fname)

    #
    # print_image
    # prints the image to the console
    def print_image(self, img):
        img.show()
        return

    #
    # flip_image
    # flips the image
    #
    # returns the flipped image
    #
    def flip_image(self, img):
        i = Image.open(img).transpose(Image.FLIP_LEFT_RIGHT)
        return i

    #
    # pixel_compare
    # does a pixel by pixel comparison in 2 images
    #
    def pixel_compare(self, img1, img2):
        img1Loaded = img1.load()
        img2Loaded = img2.load()
        #loop through each pixel
        for i in range(0, img1.size[0]):
            for j in range(0, img1.size[1]):
                    thisPixel1 = img1Loaded[i,j]
                    thisPixel2 = img2Loaded[i,j]

                    # i dont know what to do here
                    if thisPixel1 != thisPixel2:
                        print thisPixel1, thisPixel2

                    #if thisPixel1[3] == 255:
                    #    setColor(thisPixel1,'black')
                    #else:
                    #    if thisPixel1[3] == 0:
                    #        img1Loaded.setColor(thisPixel1,'white')

                    #self.print_image(img1Loaded)

        return

    #
    # get_hash
    # returns the hash value of an image
    #
    def get_hash(self,img):
        # resize to remove detail and high frequencies
        image = img.resize((12, 12), Image.ANTIALIAS)
        # convert to grayscale - this reduces # colors
        image = image.convert('L')
        # compute the mean value of the 64 colors basically find the avg pixel value
        pixels = list(image.getdata())
        avg = sum(pixels) / len(pixels)
        # compute the hash by putting the 64 bits into a 64-bit integer
        bits = ''.join(map(lambda pixel: '1' if pixel < avg else '0', pixels))
        hash = int(bits, 2).__format__('016x').upper()
        return hash

    #
    # mean_squared_error
    # returns the MSE of an image
    #
    def mean_squared_error(self, img):
        err = sum((float(img) - float(img)) ** 2)
        err /= float(img.shape[0] * img.shape[1])

        return err

    #
    # get_bitmap
    # returns a 2x2 matrix of the image with 0=background, 1=foreground
    #
    def get_bitmap(self, img):

        pixdata = img.load()

        # get size of image, define matrix to be same size
        img_bitmap = [[x for x in range(img.size[0])] for y in range(img.size[1])]

        for x in xrange(img.size[0]):
            for y in xrange(img.size[1]):
                if pixdata[x,y][0] != 255:
                    img_bitmap[x][y] = 1
                else:
                    img_bitmap[x][y] = 0

        return img_bitmap

    # make the white pixels transparent
    # we need this for combinging images with the paste operation
    def make_transparent(self, img):
        img = img.convert("RGBA")
        pixdata = img.load()
        for x in xrange(img.size[0]):
            for y in xrange(img.size[1]):
                if pixdata[x, y] == (255, 255, 255, 255):
                    pixdata[x, y] = (255, 255, 255, 0)
        return img

    # make the white pixels transparent
    # we need this for combinging images with the paste operation
    def make_black_white(self, img):
        img = img.convert("RGBA")
        pixdata = img.load()
        for x in xrange(img.size[0]):
            for y in xrange(img.size[1]):
                #logging.debug("pixdata[x,y]=%s", pixdata[x,y])
                if pixdata[x, y] != (255, 255, 255, 0):
                    pixdata[x, y] = (255, 255, 255, 255)
        return img