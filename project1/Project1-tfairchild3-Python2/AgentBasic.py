#
# tfairchild3  September 2015
#
# AgentBasic represents the class used for performing a series of basic, simple tests
# on the input images
#

import logging
from PIL import Image
from PIL import ImageStat
from PIL import ImageChops
from AgentImage import AgentImage
from AgentAttribute import Attribute

__author__ = 'tfairchild3'

# instantiate and object of type AgentImage
ai = AgentImage()

# global value of threshold used for hash comparisons
threshold = 50.0

class AgentBasic:

    def __init__(self):
        logging.info('  Starting AgentBasic')


    #
    # check_textual
    # compare the attributes in each object
    #
    # returns True if equal, otherwise returns False
    #
    def check_textual(self, p1, p2):

        # init the lists that will contain each objects figures attributes
        attr_list1 = []
        attr_list2 = []

        # loop through all figures in object p1 and create an Attribute object for each one
        for figkey in p1.objects.keys():
            a = Attribute(p1.objects[figkey].attributes) # ex: {'shape': 'square', 'size': 'very large', 'fill': 'yes'}
            attr_list1.append(a) # ex: {'shape': 'square', 'size': 'very large', 'fill': 'yes'}

        # loop through all figures in object p2 and create an Attribute object for each one
        for figkey in p2.objects.keys():
            a = Attribute(p2.objects[figkey].attributes) # ex: {'shape': 'square', 'size': 'very large', 'fill': 'yes'}
            attr_list2.append(a)

        # get the difference between the two lists
        diff = Attribute([]).get_diffs(attr_list1, attr_list2)

        # if the length of the difference is zero then they are equal
        if len(diff) == 0 and len(attr_list1) > 0 and len(attr_list2) > 0:
            return True
        else:
            return False

    #
    # are_equal
    # compares 2 images to see if they are equal
    # first compares if they are not equal visually
    # then calls subroutine which compares the images using their verbal representations
    #
    # returns True if equal, otherwise returns False
    #
    def are_equal(self, hasVerbal, p1, p2):

        img1 = ai.open_problem_image(p1.visualFilename)
        img2 = ai.open_problem_image(p2.visualFilename)

        if img1 == img2:
            rc = True
        else:
            rc = False

        img1.close()
        img2.close()

        # if images are not equal, then check the textual representation to verify our findings
        if rc is False and hasVerbal and len(p1.objects.keys()) == len(p2.objects.keys()):
            rc = self.check_textual(p1, p2)

        return rc
    #
    # are_equal_verbal
    # compares 2 images to see if they are equal using their verbal representations
    #
    # returns True if equal, otherwise returns False
    #
    def are_equal_verbal(self, p1, p2):

        rc = False

        if len(p1.objects.keys()) == len(p2.objects.keys()):
            rc = self.check_textual(p1, p2)

        return rc

    #
    # find_image
    # loops through the problem answer images looking for a match comparing image to image
    #
    # returns the figure key if a match is found
    #
    def find_image(self, problem, imgx):

        # init
        answer = -1

        # loop through problem answers looking for the image that matches'
        figkeylist = problem.figures.keys()
        for figkey in figkeylist:
            # if figure is a number then this is an answer we need to look at
            if figkey.isdigit():
                #logging.debug(" checking if %s is our answer...", figkey)
                # open
                fname = problem.figures[figkey]
                tmpimg = ai.open_problem_image(fname.visualFilename)
                fff = Image.new('RGBA', imgx.size, (255,)*4)
                imgx = Image.composite(imgx, fff, imgx)
                # get the difference using the rms (root mean square)
                diff = ImageStat.Stat(ImageChops.difference(imgx, tmpimg)).rms
                if diff[0] < threshold:
                    tmpimg.close()
                    answer = figkey
                    break
                else:
                    tmpimg.close()

        return answer

    #
    # find_image_verbal
    # loops through the problem answer images looking for a match comparing visual representations
    #
    def find_image_verbal(self, hasVerbal, problem, probX):
        # init
        answer = -1

        # loop through problem answers looking for the image that matches'
        figkeylist = problem.figures.keys()
        for figkey in figkeylist:
            # if figure is a number then this is an answer we need to look at
            if figkey.isdigit():
                # open
                tmpimgfname = problem.figures[figkey]
                tmpimg = ai.open_problem_image(tmpimgfname.visualFilename)
                if self.are_equal(hasVerbal, probX, tmpimgfname):
                    tmpimg.close()
                    answer = figkey
                    break
                else:
                    tmpimg.close()

        return answer

    #
    # find_image_list
    # loops through the global "answer list" set of images instead of the problem set of images
    # looking for a match comparing visual representations
    # NOT USED AT THIS TIME
    #
    def find_image_list(self, answerlist, img):
        # init
        answer = -1

        # loop through problem answers looking for the image that matches'
        for i in range(0,len(answerlist)):
            fname = answerlist[i].visualFilename
            tmpimg = ai.open_problem_image(fname)
            if img == tmpimg:
                tmpimg.close()
                answer = i
                break
            else:
                tmpimg.close()

        return answer

    #
    # images_are_equal
    # does a direct comparison of images
    #
    # returns True if equal, otherwise False
    def images_are_equal(self, imga, imgb, thrhold):
        fff = Image.new('RGBA', imga.size, (255,)*4)
        imga = Image.composite(imga, fff, imga)
        diff = ImageStat.Stat(ImageChops.difference(imga, imgb)).rms
        if diff[0] < thrhold:
           return True
        else:
            return False


    #
    # do_rotate
    # incrementally rotates imgA and compares to imgB, if a match is found then
    # rotates imgC in the same way and looks for a match with our answers
    #
    # returns answer variable, if found, which is the figure number of our problem answers
    #
    def do_rotate(self, problem, imgA, imgB, imgC):
        answer = -1
        for y in xrange(0, 360):
            if answer == -1:
                #logging.debug("rotating %d", y)
                imgx = imgA.rotate(y)
                fff = Image.new('RGBA', imgx.size, (255,)*4)
                imgx = Image.composite(imgx, fff, imgx)
                diff = ImageStat.Stat(ImageChops.difference(imgx, imgC)).rms
                if diff[0] < threshold: # my threshold to indicate they are equal
                    # so now flip B and look for this image in the answers
                    #logging.debug(" diff met threshold after rotating %s = %s", y, diff)
                    imgx = imgB.rotate(y)
                    fff = Image.new('RGBA', imgx.size, (255,)*4)
                    imgx = Image.composite(imgx, fff, imgx)
                    answer = self.find_image(problem, imgx)
                    if answer != -1:
                        break
            else:
                break

        return answer

    #
    # flip_and_rotate
    # incrementally flips and rotates imgA and compares to imgB, if a match is found then
    # flips and rotates imgC in the same way and looks for a match with our answers
    #
    # returns answer variable, if found, which is the figure number of our problem answers
    #
    def flip_and_rotate(self, problem, imgA, imgB, imgC):
        answer = -1
        # flip and rotate imageA and test if it equals imageB, if so, then do the same for imageC and look for answer
        for x in (Image.FLIP_TOP_BOTTOM, Image.FLIP_LEFT_RIGHT):
            for y in xrange(0, 360):
                if answer == -1:
                    imgx = imgA.transpose(x).rotate(y)
                    fff = Image.new('RGBA', imgx.size, (255,)*4)
                    imgx = Image.composite(imgx, fff, imgx)
                    diff = ImageStat.Stat(ImageChops.difference(imgx, imgB)).rms
                    if diff[0] < threshold: # my threshold to indicate they are equal
                        #logging.debug(" diff met threshold after flipping %s and rotating %s = %s", x, y, diff)
                        # flip C in the same way
                        imgx = imgC.transpose(x).rotate(y)
                        fff = Image.new('RGBA', imgx.size, (255,)*4)
                        imgx = Image.composite(imgx, fff, imgx)
                        # look for this image in the answers
                        answer = self.find_image(problem, imgx)
                        if answer != -1:
                            break
                else:
                    break

        return answer

    #
    # solve
    # main processing routine of AgentBasic
    #
    # returns answer variable
    #
    def solve(self,problem,agtAns):
        answer = -1
        hasVerbal = problem.hasVerbal

        if problem.problemType == '2x2':
            imgA = Image.open(problem.figures['A'].visualFilename)
            hash_imgA = ai.get_hash(imgA)
            imgB = Image.open(problem.figures['B'].visualFilename)
            hash_imgB = ai.get_hash(imgB)
            imgC = Image.open(problem.figures['C'].visualFilename)
            hash_imgC = ai.get_hash(imgC)

            # test for A = B
            # first compare hashes
            if hash_imgA == hash_imgB:

                answer  = self.find_image(problem, imgC)

            # maybe they are equal verbally
            elif problem.hasVerbal and self.are_equal_verbal(problem.figures['A'], problem.figures['B']):

                answer  = self.find_image(problem, imgC)

            else:

                # maintain the global agent answer list, making it smaller whenever possible
                # if A != B != C then the answer cannot be either A, B or C
                pos=int(self.find_image_list(agtAns.answerlist,imgA))
                if pos != -1:
                    agtAns.answerlist.pop(pos)
                pos=int(self.find_image_list(agtAns.answerlist,imgB))
                if pos != -1:
                    agtAns.answerlist.pop(pos)
                pos = int(self.find_image_list(agtAns.answerlist,imgC))
                if pos != -1:
                    agtAns.answerlist.pop(pos)

            # test for A = C
            if answer == -1:
                if hash_imgA == hash_imgC:
                    answer  = self.find_image(problem, imgB)
                elif problem.hasVerbal and self.are_equal_verbal(problem.figures['A'], problem.figures['C']):
                    answer  = self.find_image(problem, imgB)

            if answer == -1:
                # flip and rotate imageA and test if it equals imageB, if so, then do the same for imageC and look for answer
                answer = self.flip_and_rotate(problem, imgA, imgB, imgC)

            if answer == -1:
                # flip and rotate imageA and test if it equals imageC, if so, then do the same for imageB and look for answer
                answer = self.flip_and_rotate(problem, imgA, imgC, imgB)

            if answer == -1:
                # just rotate imageA and test if it equals imageC, if so, then do the same for imageB and look for answer
                answer = self.do_rotate(problem, imgA, imgB, imgC)

            if answer == -1:
                # just rotate imageA and test if it equals imageC, if so, then do the same for imageB and look for answer
                answer = self.do_rotate(problem, imgA, imgC, imgB)

        elif problem.problemType == '3x3':
            # test for equality
            if self.are_equal(hasVerbal, problem.figures['A'], problem.figures['B']) and\
               self.are_equal(hasVerbal, problem.figures['D'], problem.figures['F']):
                answer = self.find_image_verbal(hasVerbal, problem,problem.figures['G'])

        return answer