#
# tfairchild3  September 2015
#
# AgentBasic represents the class used for performing a series of basic, simple tests
# on the input images
#

import logging
import operator
from PIL import Image
from PIL import ImageStat
from PIL import ImageChops
from AgentImage import AgentImage
from AgentAttribute import Attribute

__author__ = 'tfairchild3'

# instantiate and object of type AgentImage
ai = AgentImage()
op_functions = {"+": operator.add,
       "-": operator.sub,
       "*": operator.mul,
       "/": operator.div}

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
        # this needs to be tightened up, it wont work if all the

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
    def are_equal(self, hasVerbal, p1, p2, threshold):

        img1 = ai.open_problem_image(p1.visualFilename)
        img2 = ai.open_problem_image(p2.visualFilename)

        if img1 == img2:
            rc = True
        else:
            rc = False

        # get the difference using the rms (root mean square)
        diff = ImageStat.Stat(ImageChops.difference(img1, img2)).rms
        #logging.debug("image difference in are_equal is %s", diff)
        if diff[0] < threshold:
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
    def find_image(self, problem, imgx, threshold=50.0):

        # init
        answer = -1
        diff_vals = []

        # loop through problem answers looking for the image that matches'
        figkeylist = problem.figures.keys()
        figkeylist.sort()
        for figkey in figkeylist:
            # if figure is a number then this is an answer we need to look at
            if figkey.isdigit():
                fname = problem.figures[figkey]
                tmpimg = ai.open_problem_image(fname.visualFilename)
                fff = Image.new('RGBA', imgx.size, (255,)*4)
                imgx = Image.composite(imgx, fff, imgx)
                # get the difference using the rms (root mean square)
                diff = ImageStat.Stat(ImageChops.difference(imgx, tmpimg)).rms
                diff_vals.append(diff[0])
                tmpimg.close()
        # get the min value in the array
        (val, idx) = min((v,i) for i,v in enumerate(diff_vals))
        if val < threshold:
            answer = idx+1

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
        figkeylist.sort()
        for figkey in figkeylist:
            # if figure is a number then this is an answer we need to look at
            if figkey.isdigit():
                # open
                tmpimgfname = problem.figures[figkey]
                tmpimg = ai.open_problem_image(tmpimgfname.visualFilename)
                if self.are_equal(hasVerbal, probX, tmpimgfname, threshold):
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
    # flip_rotate_subtract
    # incrementally flips and rotates imgA and compares to imgB, if a match is found then
    # flips and rotates imgC in the same way and looks for a match with our answers
    #
    # returns answer variable, if found, which is the figure number of our problem answers
    # TODO:  ABANDONED
    def flip_rotate_subtract(self, problem, imgA, imgB, imgC):
        answer = -1
        logging.debug("in flip_rotate_subtract")
        # flip and rotate imageA, subtract it from imgB and test if it equals imageC, if so, then do the same for imageC and look for answer
        for x in (Image.FLIP_TOP_BOTTOM, Image.FLIP_LEFT_RIGHT):
            #for y in xrange(0, 1):
                if answer == -1:
                    # not sure how to flip right to left, so instead I flip everything left to right
                    imgA = imgA.transpose(x)#.rotate(y)
                    imgB = imgB.transpose(x)#.rotate(y)
                    imgC = imgC.transpose(x)#.rotate(y)
                    #imgA.show()
                    #imgB.show()
                    #imgC.show()
                    imgx = imgA.transpose(x)#.rotate(y)
                    fff = Image.new('RGBA', imgx.size, (255,)*4)
                    imgx = Image.composite(imgx, fff, imgx)
                    rc, imgblend = self.subtract_test_3x3(imgB, imgx, imgC)
                    diff = ImageStat.Stat(ImageChops.difference(imgblend, imgC)).rms
                    if diff[0] < threshold: # my threshold to indicate they are equal
                        logging.debug("flip_rotate_subtract diff met threshold after flipping %s and rotating %s = %s", x, y, diff)
                        # flip C in the same way
                        #imgx = imgC.transpose(x).rotate(y)
                        #fff = Image.new('RGBA', imgx.size, (255,)*4)
                        #imgx = Image.composite(imgx, fff, imgx)
                        # look for this image in the answers
                        #answer = self.find_image(problem, imgx)
                        #if answer != -1:
                        break
                else:
                    break
        return rc, imgblend

    #
    # elim_image()
    # this function will check if image X is repeated in our problem set
    # if it is, then it could possibly be a correct answer BUT...
    # if it is not repeated, and it is in our answer list then it is likely NOT a correct answer ever
    # so remove it from our answerList
    #
    def elim_image(self, hasVerbal, problem, x):

        # if none of the pattern images match image x, then image x could likely never be an answer
        if problem.problemType == '2x2':
            if ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['A'], 50) and x!= 'A') or\
               ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['B'], 50) and x!= 'B') or\
               ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['C'], 50) and x!= 'C'):  #or\
                    #logging.debug("image %s appears more than once in our prob ", x)
                    return False
        elif problem.problemType == '3x3':
            if hasVerbal:
                threshold = 50
            else:
                threshold = 40

            if ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['A'], threshold) and x!= 'A') or\
               ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['B'], threshold) and x!= 'B') or\
               ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['C'], threshold) and x!= 'C') or\
               ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['D'], threshold) and x!= 'D') or\
               ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['E'], threshold) and x!= 'E') or\
               ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['F'], threshold) and x!= 'F') or\
               ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['G'], threshold) and x!= 'G') or\
               ( self.are_equal(hasVerbal, problem.figures[x], problem.figures['H'], threshold) and x!= 'H'):
                    logging.debug("image %s appears more than once in our prob ", x)
                    return False

        logging.debug("image %s only appears once in our problem", x)
        return True

    #
    # num_fills()
    # This function returns the number of fills that a problem figure has
    #
    def num_fills(self, p1):
        nfill = 0

         # loop through all figures in object p1 and create an Attribute object for each one
        for figkey in p1.objects.keys():
            a = Attribute(p1.objects[figkey].attributes) # ex: {'shape': 'square', 'size': 'very large', 'fill': 'yes'}
            if a.get_fill() == 'yes':
                nfill = nfill + 1

        return nfill

    #
    # num_nonfills()
    # This function returns the number of NONfills that a problem figure has
    #
    def num_nonfills(self, p1):
        nfill = 0

         # loop through all figures in object p1 and create an Attribute object for each one
        for figkey in p1.objects.keys():
            a = Attribute(p1.objects[figkey].attributes) # ex: {'shape': 'square', 'size': 'very large', 'fill': 'yes'}
            if a.get_fill() == 'no':
                nfill = nfill + 1

        return nfill


    #
    # find_fill_pattern()
    # This function loops through problem set looking for a pattern in the number of fills
    #
    def find_fill_pattern(self, problem):
        f1 = 0
        f2 = 0
        f3 = 0
        fA = 0
        row1_trend = 0
        row2_trend = 0
        row3_trend = 0
        fill_list = []
        #r_fill_list = []
        # loop through objects in prob
        keylist = problem.figures.keys()
        keylist.sort()
        for figkey in keylist:
            # if the figure number is not numeric then we want to examine it (ie, it is not an answer figure)
            if not figkey.isdigit():
                num_fills = 0
                for objlist in problem.figures[figkey].objects.keys():
                    attrlist = problem.figures[figkey].objects[objlist].attributes.keys()
                    for attrkey in attrlist:
                        if attrkey == 'fill' and problem.figures[figkey].objects[objlist].attributes[attrkey]=='yes':
                            num_fills = num_fills+1
                if figkey == 'A' or figkey == 'D' or figkey == 'G':
                    f1 = num_fills
                    if figkey == 'A':
                        fA = num_fills #save this so we can make an easy compare of fill_list and reverse(fill_list) below
                elif figkey == 'B' or figkey == 'E' or figkey == 'H':
                    f2 = num_fills
                elif figkey == 'C' or figkey == 'F':
                    f3 = num_fills

                #logging.debug("number of fills for %s is %d", figkey, num_fills)
                fill_list.append(num_fills)

                if figkey == 'C':
                    if f1<f2<f3:
                        row1_trend = '+'
                    elif f1>f2>f3:
                        row1_trend = '-'
                    elif f1==f2==f3:
                        row1_trend = '='
                    else:
                        row1_trend = '0'
                elif figkey == 'F':
                    if f1<f2<f3:
                        row2_trend = '+'
                    elif f1>f2>f3:
                        row2_trend = '-'
                    elif f1==f2==f3:
                        row2_trend = '='
                    else:
                        row2_trend = '0'
                elif figkey == 'H':
                    if f1<f2:
                        row3_trend = '+'
                    elif f1>f2:
                        row3_trend = '-'
                    elif f1==f2:
                        row3_trend = '='
                    else:
                        row3_trend = '0'

                if problem.problemType == '2x2' and figkey == 'C':
                    if f1 == f2 and f2 == f3:
                        return f3, '='
                    elif f1 != f2 and f2 != f3 and f3 == f1:
                        return f2, '='
                    elif f1 == f2 and f2 != f3:
                        return f3, '='
                elif problem.problemType == '3x3' and figkey == 'H':
                    fill_list.append(fA)

        if len(set(fill_list)) == 1 and set(fill_list).pop() == 0:
            #fill_list is all zeros... just return
            return 0,0
        else:
            r_fill_list = fill_list
            r_fill_list.reverse()
            if fill_list == r_fill_list:
                #logging.debug("found a pattern in the #fills... its same backwards: %s, %s", fill_list, r_fill_list)
                #if its the same backwards then the next fill number should equal the first
                return fill_list[0], '='
            else:
                #logging.debug("NO pattern in the #fills... its NOT the same backwards: %s, %s", fill_list, r_fill_list)
                return f3, row3_trend

    #
    # find_common_shapes2x2()
    # Find common shapes found in all the 2x2 objects
    # return a list of these common shapes
    #
    def find_common_shapes2x2(self, problem, pX):

        setlist = []
        #common_list = []
        # loop through objects in prob
        keylist = problem.figures.keys()
        keylist.sort()
        for figkey in keylist:
            # only look at problem figures (not the answers)
            if not figkey.isdigit() and figkey == pX:
                shapelist = []
                for objlist in problem.figures[figkey].objects.keys():
                    attrlist = problem.figures[figkey].objects[objlist].attributes.keys()
                    for attrkey in attrlist:
                        if attrkey == 'shape':
                            this_shape = problem.figures[figkey].objects[objlist].attributes[attrkey]
                            if this_shape not in shapelist:
                                shapelist.append(this_shape)
                #logging.debug("these are the shapes we found in %s: %s", figkey, shapelist)
                if shapelist not in setlist and len(shapelist) > 0:
                    setlist.append(shapelist)
        if len(setlist) > 0:
            return setlist[0]
        else:
            return []

    #
    # find_common_shapes()
    # Find common shapes found in all the 3x3 objects
    # return a list of these common shapes
    #
    def find_common_shapes(self, problem):

        setlist = []
        common_list = []
        # loop through objects in prob
        keylist = problem.figures.keys()
        keylist.sort()
        for figkey in keylist:
            # only look at problem figures (not the answers)
            if not figkey.isdigit():
                shapelist = []
                for objlist in problem.figures[figkey].objects.keys():
                    attrlist = problem.figures[figkey].objects[objlist].attributes.keys()
                    for attrkey in attrlist:
                        if attrkey == 'shape':
                            this_shape = problem.figures[figkey].objects[objlist].attributes[attrkey]
                            if this_shape not in shapelist:
                                shapelist.append(this_shape)
                #logging.debug("these are the shapes we found in %s: %s", figkey, shapelist)
                if shapelist not in setlist and len(shapelist) > 0:
                    setlist.append(shapelist)
        if len(setlist) > 0:
            return setlist[0]
        else:
            return []


    #
    # blend_images()
    # blends two images and returns the resulting image
    # NOT USED
    #
    def blend_images(self, img1, img2):
        return Image.blend(img1,img2,10)


    #
    # blend_test_3x3()
    # blends first 2 images together and see if it matches the 3rd
    #
    def blend_test_3x3(self, a, b, c):
            # test whether the rows are are just blended images of each other
            img1 = ai.make_transparent(a)
            img2 = ai.make_transparent(b)
            img1.paste(img2, (0,0), img2)
            img3 = img1
            if self.images_are_equal(c, img3, 40):
                return True, img3
            else:
                return False, img3


    #
    # subtract_test_3x3()
    # subtract img b from img a and see if it matches the img c
    #
    def subtract_test_3x3(self, a, b, c):
            # test whether the rows are are just subtracted images of each other
            img1 = ai.make_transparent(a)
            img2 = ai.make_transparent(b)
            img2 = ai.make_black_white(img2)
            img1.paste(img2, (0,0), img2)
            img3 = img1
            #img3.show()
            if self.images_are_equal(c, img3, 40):
                return True, img3
            else:
                return False, img3

    #
    # crop_and_test_3x3
    # crops the same section of 3 images and compare, if they are all equal return True
    #
    def crop_and_test_3x3(self,problem, a, b, c, section):

        #crop bottom section from images
        imgA = Image.open(problem.figures[a].visualFilename)
        #crop box is (left, top, right, bottom)
        w, h = imgA.size
        if section == 'top':
            crop_box = (0, 0, w, h/3)
        elif section == 'top-small':
            crop_box = (0, 0, w, h/4)
        elif section == 'middle':
            crop_box = (0, h/3, w, h/3*2)
        elif section == 'bottom':
            crop_box = (0,h/3*2, w, h)
        elif section == 'inner':
            crop_box = (h/4,w/3,w-w/3,h-h/4)
        elif section == 'r-2/3': #right 2/3 of the image
            crop_box = (w-(w/3*2)+25, 0, w-25, h)  # try to eliminate white space with the +/- 25 pixels
        elif section == 'l-2/3': #left 2/3 of the image
            crop_box = (0, 0, w-w/3, h)
        else: #section == 'bottom-third' default to bottom third, this seems to work well...
            crop_box = (0,h/3,w,h)

        cropA = imgA.crop(crop_box)
        #if section == 'r-2/3': cropA.show()
        imgB = Image.open(problem.figures[b].visualFilename)
        cropB = imgB.crop(crop_box)
        #if section == 'r-2/3': cropB.show()
        imgC = Image.open(problem.figures[c].visualFilename)
        cropC = imgC.crop(crop_box)

        if self.images_are_equal(cropA, cropB, 50):
            if self.images_are_equal(cropA, cropC, 50):
                return True, cropC

        return False, None

    #
    # flip_and_blend_3x3()
    # flips and blends the 3 images returns true if they are equal
    # NOT FINISHED
    # NOT IMPLEMENTED
    #
    def flip_and_blend_3x3(self, problem, a, b, c):
        imgA = Image.open(problem.figures[a].visualFilename)
        imgB = Image.open(problem.figures[b].visualFilename).transpose(Image.FLIP_LEFT_RIGHT)
        imgC = Image.open(problem.figures[c].visualFilename)
        imgblend = Image.blend(imgA,imgB,10)
        if self.images_are_equal(imgblend, imgC, 30):
            return True, imgblend

        return False, None

    #
    # crop_whitespace()
    # remove leading and trailing whitespace from the image
    #
    # reference:  This solution is common on the web, but I give this website credit because of the good explanation
    # http://question.ikende.com/question/2D31303733323637313936
    def crop_whitespace(self, img):
        bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
        diff = ImageChops.difference(img, bg)
        diff = ImageChops.add(diff, diff, 2.0, -100)
        bbox = diff.getbbox()
        return img.crop(bbox)

    #
    # do_2x2()
    # the main processing for 2x2 problems
    # this is new over project 1
    # I abandoned my project 1 logic because my Project 2 logic is much more effective
    #
    def do_2x2(self, problem, agtAns):
            answer = -1
            hasVerbal = problem.hasVerbal

            # equality test 1
            imgA = Image.open(problem.figures['A'].visualFilename)
            imgB = Image.open(problem.figures['B'].visualFilename)
            imgC = Image.open(problem.figures['C'].visualFilename)


            if (imgA == imgB and imgB == imgC) or imgA == imgC:
                logging.debug("passed equality test 1")
                answer = self.find_image_verbal(hasVerbal, problem,problem.figures['C'])

            if imgA == imgC:
                logging.debug("passed equality test 1")
                answer = self.find_image_verbal(hasVerbal, problem,problem.figures['B'])

            # equality test 2
            if answer == -1:
                if self.images_are_equal(imgA, imgB, 20) and\
                   self.images_are_equal(imgB, imgC, 20):
                    logging.debug("passed equality test 2")
                    answer = self.find_image_verbal(hasVerbal, problem,problem.figures['C'])
                elif self.images_are_equal(imgA, imgC, 20):
                    logging.debug("passed equality test 2")
                    answer = self.find_image_verbal(hasVerbal, problem,problem.figures['B'])

            #equality test 3
            if answer == -1:
                 if self.are_equal(hasVerbal, problem.figures['A'], problem.figures['B'], 80) and\
                   self.are_equal(hasVerbal, problem.figures['B'], problem.figures['C'], 80):
                        logging.debug("passed equality test 3")
                        answer = self.find_image_verbal(hasVerbal, problem,problem.figures['C'])


            # none of the more obvious tests passed so now its time to start eliminating answers with what we know
            if answer == -1:
                # test for same number of objects
                logging.debug("testing for same number of objects in all ")
                num_objsA = len(problem.figures['A'].objects.keys())
                num_objsB = len(problem.figures['B'].objects.keys())
                num_objsC = len(problem.figures['C'].objects.keys())

                if num_objsA == num_objsB and\
                   num_objsB == num_objsC:
                        # answer must have the same number of objects as G or H
                        logging.debug("answer must have %s objects", num_objsC)
                        # remove any answers that do not have the same # objects
                        agtAns.removeNumObj_not(num_objsC)

                # test for pattern in number of objects
                logging.debug("**** pattern in the number of objects test ******")
                found = 0
                for op in ('+','*','-'):
                    for x in range(0,5):
                        op_func = op_functions[op]
                        logging.debug("testing with x=%d, op=%s", x, op)
                        if not found and len(problem.figures['B'].objects.keys()) == op_func(len(problem.figures['A'].objects.keys()),x):
                            # answer must have x more number of objects as C
                            logging.debug("answer must have %s objects(%s, %s)", op_func(len(problem.figures['C'].objects.keys()),x), len(problem.figures['C'].objects.keys()), x)
                            # remove any answers that do not have the same # objects
                            found = 1
                            agtAns.removeNumObj_not(op_func(len(problem.figures['C'].objects.keys()),x))
                            break
                        if found:
                            break
                    if found:
                       break


                # test for pattern in number of fills
                logging.debug("**** pattern in the number of fills test ******")
                found = 0
                for op in ('+','*','-'):
                    for x in range(0,5):
                        op_func = op_functions[op]
                        logging.debug("testing with x=%d, op=%s and %s", x, op, op_func)
                        if not found and\
                           self.num_fills(problem.figures['B']) == op_func(self.num_fills(problem.figures['A']),x):
                                # answer must have x more number of fills as G and y more as H
                                num_fills = self.num_fills(problem.figures['C'])
                                logging.debug("answer must have %s fills", op_func(num_fills,x))
                                # remove any answers that do not have the same # objects
                                found = 1
                                nfills = op_func(num_fills,x)
                                agtAns.removeFillNum_not2(nfills, problem.problemType,op)
                                break
                        if found:
                            break
                    if found:
                        break


                # find objects common to all figures and remove answers that dont have it
                logging.debug("testing for figures common to all objects")
                shape_list = []
                shape_list = self.find_common_shapes2x2(problem,'C')
                logging.debug("shape_list = %s", shape_list)
                for shape in shape_list:
                    logging.debug("removing not %s's", shape)
                    agtAns.removeShapeObj_not(shape)

                # crop test
                logging.debug("*** crop test w/bottom-third ***")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'A','B','C', 'bottom-third')
                if rc == True:
                    #answer must have same cropped portion, eliminate those that do not
                    logging.debug("loop through answers, eliminating those without the cropped image")
                    agtAns.removeCropped_Not(problem, croppedImg, 'bottom-third')

                # crop test
                logging.debug("*** crop test w/bottom ***")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'A','B','C', 'bottom')
                if rc == True:
                    #answer must have same cropped portion, eliminate those that do not
                    logging.debug("loop through answers, eliminating those without the cropped image")
                    agtAns.removeCropped_Not(problem, croppedImg, 'bottom')

            # check our pool of answers, do we have one yet?
            if agtAns.get_num_answers() == 1:
               logging.debug("only 1 answer to pick from...")
               answer = agtAns.get_fig_num(0)

            # equality test 3 use a higher threshold
            if answer == -1:
                 if self.are_equal(hasVerbal, problem.figures['A'], problem.figures['B'], 50) and\
                   self.are_equal(hasVerbal, problem.figures['B'], problem.figures['C'], 50):
                        logging.debug("passed equality test 3")
                        answer = self.find_image_verbal(hasVerbal, problem,problem.figures['C'])

            # fall back on some of the P1 tests
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

            if answer == -1:
                # test for pattern in number of NONfills in outlying objects
                logging.debug("**** 2x2 incremental pattern in the number of NONfills in outlying objects test ******")
                found = 0
                nnfillsA = self.num_nonfills(problem.figures['A'])
                nnfillsB = self.num_nonfills(problem.figures['B'])
                nnfillsC = self.num_nonfills(problem.figures['C'])

                incremental_amt1 = nnfillsA - nnfillsB

                if incremental_amt1 < 0:  #means the number is increasing
                    num_nonfills = nnfillsC + abs(incremental_amt1)
                elif incremental_amt1 > 0: #means the number is decreasing
                    num_nonfills = nnfillsC - abs(incremental_amt1)
                else:
                    num_nonfills = nnfillsC

                agtAns.removeNonFillNum_not(num_nonfills, '=')

            # check our pool of answers, do we have one yet?
            if agtAns.get_num_answers() == 1:
               logging.debug("only 1 answer to pick from...")
               answer = agtAns.get_fig_num(0)

            logging.debug("returning for 2x2")

            return answer


    #
    # do_2x2_P1()
    # the main processing for 2x2 problems in Project 1
    # this is my old logic from project 1
    # abandoned because Project 2 logic is much more effective
    #
    def do_2x2_P1(self, problem, agtAns):
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

        # show the answers we have not eliminated so far
        # agtAns.show_prob_answer_list()

        #Project 1 logic abandoned
        #if problem.problemType == '2x2':
        #   answer = self.do_2x2_P1(problem,agtAns)

        if problem.problemType == '2x2':
            answer = self.do_2x2(problem,agtAns)
            if answer == -1 and agtAns.get_num_answers() == 1:
                logging.debug("only 1 2x2 answer to pick from...")
                answer = agtAns.get_fig_num(0)



        elif problem.problemType == '3x3':
            # equality test 1
            imgA = Image.open(problem.figures['A'].visualFilename)
            imgB = Image.open(problem.figures['B'].visualFilename)
            imgC = Image.open(problem.figures['C'].visualFilename)
            imgD = Image.open(problem.figures['D'].visualFilename)
            imgE = Image.open(problem.figures['E'].visualFilename)
            imgF = Image.open(problem.figures['F'].visualFilename)
            imgG = Image.open(problem.figures['G'].visualFilename)
            imgH = Image.open(problem.figures['H'].visualFilename)

            #************* test area *****************
            #imgA_bitmap = ai.get_bitmap(imgA)
            #print('\n'.join([''.join(['{:1}'.format(item) for item in row])
            #for row in imgA_bitmap]))

            #img = ai.make_transparent(imgG)
            #img2 = ai.make_transparent(imgH)
            #img.paste(img2, (0,0), img2)
            #img.show()

            #w1, h1 = imgA.size
            #new_img = Image.new('RGBA', (w1, h1), (255, 255, 255, 255))
            #new_img = ImageChops.blend(img, img2, .9)
            #new_img.show()
            #new_img.paste(imgA, (0,0))
            #new_img.show()
            #new_img.paste(imgB, (0,0))
            #new_img.show()
            #PIL.Image.merge(mode, bands)

            #************* end test area *****************

            logging.debug("****** equality test 1 *****")
            if imgA == imgB and imgB == imgC and imgD == imgE and imgE==imgF and imgG==imgH:
                logging.debug("passed equality test 1")
                answer = self.find_image_verbal(hasVerbal, problem,problem.figures['G'])

            # equality test 2
            if answer == -1:
                logging.debug("****** equality test 2 *****")
                if self.images_are_equal(imgA, imgB, 50) and\
                   self.images_are_equal(imgB, imgC, 50) and\
                   self.images_are_equal(imgD, imgE, 50) and\
                   self.images_are_equal(imgE, imgF, 50) and\
                   self.images_are_equal(imgG, imgH, 50):
                    logging.debug("passed equality test 2")
                    answer = self.find_image_verbal(hasVerbal, problem,problem.figures['G'])

            # equality test 2b check for equality in diagonals
            if answer == -1:
                logging.debug("****** equality test 2b *****")
                if self.images_are_equal(imgA, imgE, 50) and\
                   self.images_are_equal(imgB, imgF, 50) and\
                   self.images_are_equal(imgD, imgH, 50) :
                    logging.debug("passed equality test 2b")
                    if hasVerbal:
                        answer = self.find_image_verbal(hasVerbal, problem,problem.figures['E'])
                    else:
                        answer = self.find_image(problem, imgE, 50)

            if answer == -1:
                # try a blend test
                logging.debug("******* blend test *******")
                rc, imgblend = self.blend_test_3x3(imgA, imgB, imgC)
                if rc == True:
                    #imgblend.show()
                    rc, imgblend = self.blend_test_3x3(imgD, imgE, imgF)
                    if rc == True:
                        rc, imgblend = self.blend_test_3x3(imgG, imgH, imgH)
                        #imgblend.show()
                        answer  = self.find_image(problem, imgblend, 50)

            if answer == -1:
                # try a subtraction test
                logging.debug("******* subtraction test *******")
                rc, imgblend = self.subtract_test_3x3(imgA, imgB, imgC)
                #imgblend.show()
                if rc == True:
                    rc, imgblend = self.subtract_test_3x3(imgD, imgE, imgF)
                    if rc == True:
                        rc, imgblend = self.subtract_test_3x3(imgG, imgH, imgH)
                        answer  = self.find_image(problem, imgblend, 50)
                        logging.debug("found answer from subtract test: %s", answer)

            if answer == -1:
                logging.debug("******* blend and subtract test XOR *******")
                more_blending = False
                rc, imgblend1 = self.subtract_test_3x3(imgA, imgB, imgC)
                rc, imgblend2 = self.subtract_test_3x3(imgB, imgA, imgC)
                rc, imgblend3 = self.blend_test_3x3(imgblend1, imgblend2, imgC)
                if rc == False:
                    more_blending = True
                    # blend the two original images together, then subtract imgblend3 from above
                    rc, imgblend = self.blend_test_3x3(imgA, imgB, imgC)
                    rc, imgblend = self.subtract_test_3x3(imgblend, imgblend3, imgC)
                if rc == True:
                    rc, imgblend1 = self.subtract_test_3x3(imgD, imgE, imgF)
                    rc, imgblend2 = self.subtract_test_3x3(imgE, imgD, imgF)
                    rc, imgblend3 = self.blend_test_3x3(imgblend1, imgblend2, imgF)
                    if rc == False and more_blending == True:
                        # blend the two original images together, then subtract imgblend3 from above
                        rc, imgblend = self.blend_test_3x3(imgD, imgE, imgF)
                        rc, imgblend = self.subtract_test_3x3(imgblend, imgblend3, imgF)
                    if rc == True:
                        rc, imgblend1 = self.subtract_test_3x3(imgG, imgH, imgH)
                        rc, imgblend2 = self.subtract_test_3x3(imgH, imgG, imgH)
                        rc, imgblend3 = self.blend_test_3x3(imgblend1, imgblend2, imgH)
                        if rc == False and more_blending == True:
                            rc, imgblend = self.blend_test_3x3(imgG, imgH, imgH)
                            rc, imgblend = self.subtract_test_3x3(imgblend, imgblend3, imgH)
                            answer  = self.find_image(problem, imgblend, 50)
                        else:
                            answer  = self.find_image(problem, imgblend3, 50)
                        logging.debug("found answer from blend and subtract test: %s", answer)


            if answer == -1 and not hasVerbal:
                for x in (0, Image.FLIP_TOP_BOTTOM):
                    logging.debug("******* transpose and subtract test  *******")
                    # bg is background image - image with only the background color
                    bg = Image.new(imgA.mode, imgA.size, imgA.getpixel((0,0)))
                    cA = self.crop_whitespace(imgA)
                    cB = self.crop_whitespace(imgB.transpose(x))
                    cC = self.crop_whitespace(imgC)
                    # subtract cB from cA
                    rc, imgblend1 = self.subtract_test_3x3(cA, cB, cC)
                    # get imgBlend1 back to orig size
                    rc, imgblend1 = self.blend_test_3x3(bg, imgblend1, imgblend1)
                    # get cC back to orig size
                    rc, imgblend2 = self.blend_test_3x3(bg, cC, cC)
                    # compare
                    if self.images_are_equal(imgblend1, imgblend2, 75):
                        # crop D
                        bg = Image.new(imgD.mode, imgD.size, imgD.getpixel((0,0)))
                        cD = self.crop_whitespace(imgD)
                        cE = self.crop_whitespace(imgE.transpose(x))
                        cF = self.crop_whitespace(imgF)
                        # subtract
                        rc, imgblend1 = self.subtract_test_3x3(cD, cE, imgF)
                        # get imgBlend1 back to orig size
                        rc, imgblend1 = self.blend_test_3x3(bg, imgblend1, imgblend1)
                        # get cF back to orig size
                        rc, imgblend2 = self.blend_test_3x3(bg, cF, cF)
                        if self.images_are_equal(imgblend1, imgblend2, 75):
                            # crop G
                            cG = self.crop_whitespace(imgG)
                            cH = self.crop_whitespace(imgH.transpose(x))
                            # subtract
                            rc, imgblend1 = self.subtract_test_3x3(cG, cH, imgH)
                            # get imgBlend1 back to orig size
                            rc, imgblend1 = self.blend_test_3x3(bg, imgblend1, imgblend1)
                            answer  = self.find_image(problem, imgblend1, 75)


            # none of the more obvious tests passed so now its time to start eliminating answers with what we can figure out
            if answer == -1:
                if hasVerbal:
                        # test for same number of objects
                        logging.debug("***** same number of objects test ***** ")
                        num_objsA = len(problem.figures['A'].objects.keys())
                        num_objsB = len(problem.figures['B'].objects.keys())
                        num_objsC = len(problem.figures['C'].objects.keys())
                        num_objsD = len(problem.figures['D'].objects.keys())
                        num_objsE = len(problem.figures['E'].objects.keys())
                        num_objsF = len(problem.figures['F'].objects.keys())
                        num_objsG = len(problem.figures['G'].objects.keys())
                        num_objsH = len(problem.figures['H'].objects.keys())
                        if num_objsA == num_objsB and\
                           num_objsB == num_objsC and\
                           num_objsD == num_objsE and\
                           num_objsE == num_objsF and\
                           num_objsG == num_objsH:
                                # answer must have the same number of objects as G or H
                                logging.debug("answer must have %s objects", len(problem.figures['G'].objects.keys()))
                                # remove any answers that do not have the same # objects
                                agtAns.removeNumObj_not(len(problem.figures['G'].objects.keys()))

                        elif num_objsA == num_objsB and\
                               num_objsA == num_objsC and\
                               num_objsA == num_objsD and\
                               num_objsA == num_objsF and\
                               num_objsA == num_objsG and\
                               num_objsA == num_objsH:
                                    logging.debug("***** same # objects in outlying images *******")
                                    # answer must have the same number of objects as num_objs
                                    logging.debug("answer must have %s objects", num_objsA)
                                    # remove any answers that do not have the same # objects
                                    agtAns.removeNumObj_not(num_objsA)

                        elif num_objsC == num_objsF and\
                                num_objsF == num_objsG and\
                                num_objsG == num_objsH:
                                    logging.debug("****** same number of objects in right and bottom images test ******")
                                    # answer must have the same number of objects as num_objsC
                                    logging.debug("answer must have %s objects", num_objsC)
                                    # remove any answers that do not have the same # objects
                                    agtAns.removeNumObj_not(num_objsC)

                        # test for pattern in number of objects
                        logging.debug("**** 3x3 pattern in the number of objects test ******")
                        found = 0
                        for op in ('+','*','-'):
                            for x in range(0,5):
                                for y in range(0,5):
                                    op_func = op_functions[op]
                                    logging.debug("testing with x=%d y=%d, op=%s", x, y, op)
                                    if not found and\
                                       len(problem.figures['B'].objects.keys()) == op_func(len(problem.figures['A'].objects.keys()),x) and\
                                       len(problem.figures['C'].objects.keys()) == op_func(len(problem.figures['A'].objects.keys()),(x+y)) and\
                                       len(problem.figures['E'].objects.keys()) == op_func(len(problem.figures['D'].objects.keys()),x) and\
                                       len(problem.figures['F'].objects.keys()) == op_func(len(problem.figures['D'].objects.keys()),(x+y)) and\
                                       len(problem.figures['H'].objects.keys()) == op_func(len(problem.figures['G'].objects.keys()),x):
                                            # answer must have x more number of objects as G and y more as H
                                            logging.debug("answer must have %s objects", op_func(len(problem.figures['G'].objects.keys()),(x+y)))
                                            # remove any answers that do not have the same # objects
                                            found = 1
                                            agtAns.removeNumObj_not(op_func(len(problem.figures['G'].objects.keys()),x+y))
                                            break
                                    if found:
                                        break
                                if found:
                                    break
                            if found:
                                break

                        # test for pattern in number of objects in outlying objects
                        logging.debug("**** 3x3 pattern in the number of objects in outlying squares test ******")
                        found = 0
                        for op in ('+','*','-'):
                            for x in range(0,5):
                                for y in range(0,5):
                                    op_func = op_functions[op]
                                    logging.debug("testing with x=%d y=%d, op=%s", x, y, op)
                                    if not found and\
                                       len(problem.figures['F'].objects.keys()) == op_func(len(problem.figures['C'].objects.keys()),x) and\
                                       len(problem.figures['H'].objects.keys()) == op_func(len(problem.figures['G'].objects.keys()),x):
                                            # answer must have x more number of objects as G and y more as H
                                            logging.debug("answer must have %s objects", op_func(len(problem.figures['G'].objects.keys()),x))
                                            # remove any answers that do not have the same # objects
                                            found = 1
                                            agtAns.removeNumObj_not(op_func(len(problem.figures['G'].objects.keys()),x))
                                            break
                                    if found:
                                        break
                                if found:
                                    break
                            if found:
                                break

                        # test for pattern in number of fills
                        logging.debug("**** 3x3 pattern in the number of fills test ******")
                        found = 0
                        for op in ('+','*','-'):
                            for x in range(0,5):
                                for y in range(0,5):
                                    op_func = op_functions[op]
                                    logging.debug("testing with x=%d y=%d, op=%s", x, y, op)
                                    if not found and\
                                       self.num_fills(problem.figures['B']) == op_func(self.num_fills(problem.figures['A']),x) and\
                                       self.num_fills(problem.figures['C']) == op_func(self.num_fills(problem.figures['A']),(x+y)) and\
                                       self.num_fills(problem.figures['E']) == op_func(self.num_fills(problem.figures['D']),x) and\
                                       self.num_fills(problem.figures['F']) == op_func(self.num_fills(problem.figures['D']),(x+y)) and\
                                       self.num_fills(problem.figures['H']) == op_func(self.num_fills(problem.figures['G']),x):
                                            # answer must have x more number of fills as G and y more as H
                                            num_fills = self.num_fills(problem.figures['G'])
                                            logging.debug("answer must have %s fills", op_func(num_fills,x+y))
                                            # remove any answers that do not have the same # objects
                                            found = 1
                                            nfills = op_func(num_fills,x+y)
                                            agtAns.removeFillNum_not2(nfills, problem.problemType, op)
                                            break
                                    if found:
                                        break
                                if found:
                                    break
                            if found:
                                break

                        # test for pattern in number of fills in outlying objects
                        logging.debug("**** 3x3 pattern in the number of fills in outlying objects test ******")
                        found = 0
                        for op in ('+','*','-'):
                            for x in range(0,5):
                                for y in range(0,5):
                                    op_func = op_functions[op]
                                    logging.debug("testing with x=%d y=%d, op=%s", x, y, op)
                                    if not found and\
                                       self.num_fills(problem.figures['F']) == op_func(self.num_fills(problem.figures['C']),x) and\
                                       self.num_fills(problem.figures['H']) == op_func(self.num_fills(problem.figures['G']),x):
                                            # answer must have x more number of fills as G and y more as H
                                            num_fills = self.num_fills(problem.figures['G'])
                                            logging.debug("answer must have %s fills", op_func(num_fills,x))
                                            # remove any answers that do not have the same # objects
                                            found = 1
                                            nfills = op_func(num_fills,x)
                                            #agtAns.removeFillNum_not2(nfills, problem.problemType)
                                            agtAns.removeFillNum_not(nfills, op)
                                            break
                                    if found:
                                        break
                                if found:
                                    break
                            if found:
                                break
                else:
                    # use num of objects here
                    #logging.debug("skipping test because not hasVerbal")
                    pass

                agtAns.show_prob_answer_list()

                # test each image to see if it is matched anywhere else in the pattern
                # if it is not, then it could never be an answer so remove it if it is there
                logging.debug("***** image uniqueness test *******")
                for x in ('A','B','C','D','E','F','G','H'):
                    logging.debug("checking %s", x)
                    # if none of the images match image x, then image x is likely not an answer
                    if self.elim_image(hasVerbal, problem, x):
                        #logging.debug("removing %s", x)
                        agtAns.removeImage(problem.figures[x].visualFilename, 40)

                agtAns.show_prob_answer_list()

                if hasVerbal:
                    # find objects common to all figures and remove answers that dont have it
                    logging.debug("****** figures common to all objects test ******")
                    shape_list = []
                    shape_list = self.find_common_shapes(problem)
                    logging.debug("3x3 shape_list = %s", shape_list)
                    agtAns.removeShapeObj_not(shape_list)
                else:
                    #logging.debug("skipping test because not hasVerbal")
                    pass

                agtAns.show_prob_answer_list()

                # crop test
                logging.debug("****** crop test5b DIAGONALS (inner) *****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'B','F','F', 'inner')
                if rc == True:
                    rc, croppedImg = self.crop_and_test_3x3(problem, 'D','H','H', 'inner')
                    if rc == True:
                        rc, croppedImg = self.crop_and_test_3x3(problem, 'A','E','E', 'inner')
                        if rc == True:
                            #answer must have same cropped portion, eliminate those that do not
                            logging.debug("loop through answers, eliminating those without the cropped image G&H")
                            agtAns.removeCropped_Not(problem, croppedImg, 'inner')

                # crop test
                logging.debug("****** crop test1 (bottom-third)*****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'A','B','C', 'bottom-third')
                if rc == True:
                    rc, croppedImg = self.crop_and_test_3x3(problem, 'D','E','F', 'bottom-third')
                    if rc == True:
                        rc, croppedImg = self.crop_and_test_3x3(problem, 'G','H','H', 'bottom-third')
                        if rc == True:
                            #answer must have same cropped portion, eliminate those that do not
                            logging.debug("loop through answers, eliminating those without the cropped image G&H")
                            agtAns.removeCropped_Not(problem, croppedImg, 'bottom-third')

                # crop test
                #logging.debug("****** crop test1 (R-2/3)*****")
                #rc, croppedImg = self.crop_and_test_3x3(problem, 'A','B','C', 'r-2/3')
                #if rc == True:
                #    rc, croppedImg = self.crop_and_test_3x3(problem, 'D','E','F', 'r-2/3')
                #    if rc == True:
                #        rc, croppedImg = self.crop_and_test_3x3(problem, 'G','H','H', 'r-2/3')
                #        if rc == True:
                #            #answer must have same cropped portion, eliminate those that do not
                #            logging.debug("loop through answers, eliminating those without the cropped image G&H")
                #            agtAns.removeCropped_Not(problem, croppedImg, 'r-2/3')


                # crop test
                logging.debug("****** crop test1 (R-2/3)*****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'A','C','C', 'r-2/3')
                if rc == True:
                    rc, croppedImg = self.crop_and_test_3x3(problem, 'D','F','F', 'r-2/3')
                    if rc == True:
                        #answer must have same cropped portion, eliminate those that do not
                        logging.debug("loop through answers, eliminating those without the cropped image G&H")
                        agtAns.removeCropped_Not(problem, croppedImg, 'r-2/3')


                # crop test
                logging.debug("****** crop test1 (Left-2/3)*****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'A','B','C', 'l-2/3')
                if rc == True:
                    rc, croppedImg = self.crop_and_test_3x3(problem, 'D','E','F', 'l-2/3')
                    if rc == True:
                        rc, croppedImg = self.crop_and_test_3x3(problem, 'G','H','H', 'l-2/3')
                        if rc == True:
                            #answer must have same cropped portion, eliminate those that do not
                            logging.debug("loop through answers, eliminating those without the cropped image G&H")
                            agtAns.removeCropped_Not(problem, croppedImg, 'l-2/3')


                agtAns.show_prob_answer_list()

                # crop test
                logging.debug("****** crop test2 (bottom) *****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'A','B','C', 'bottom')
                if rc == True:
                    rc, croppedImg = self.crop_and_test_3x3(problem, 'D','E','F', 'bottom')
                    if rc == True:
                        rc, croppedImg = self.crop_and_test_3x3(problem, 'G','H','H', 'bottom')
                        if rc == True:
                            #answer must have same cropped portion, eliminate those that do not
                            logging.debug("loop through answers, eliminating those without the cropped image of G&H")
                            agtAns.removeCropped_Not(problem, croppedImg, 'bottom')

                agtAns.show_prob_answer_list()

                # crop test
                logging.debug("****** crop test3 (top) *****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'A','B','C', 'top')
                if rc == True:
                    rc, croppedImg = self.crop_and_test_3x3(problem, 'D','E','F', 'top')
                    if rc == True:
                        rc, croppedImg = self.crop_and_test_3x3(problem, 'G','H','H', 'top')
                        if rc == True:
                            #answer must have same cropped portion, eliminate those that do not
                            logging.debug("loop through answers, eliminating those without the cropped image of G&H")
                            agtAns.removeCropped_Not(problem, croppedImg, 'top')

                # crop test
                logging.debug("****** crop test1 (inner)*****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'A','B','C', 'inner')
                if rc == True:
                    rc, croppedImg = self.crop_and_test_3x3(problem, 'D','E','F', 'inner')
                    if rc == True:
                        rc, croppedImg = self.crop_and_test_3x3(problem, 'G','H','H', 'inner')
                        if rc == True:
                            #answer must have same cropped portion, eliminate those that do not
                            logging.debug("loop through answers, eliminating those without the cropped image G&H")
                            agtAns.removeCropped_Not(problem, croppedImg, 'inner')

                agtAns.show_prob_answer_list()

                # crop test
                logging.debug("****** crop test4 (top) *****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'C','F','F','top-small')
                if rc == True:
                    #answer must have same cropped portion, eliminate those that do not
                    logging.debug("loop through answers, eliminating those without the cropped image of C&F")
                    agtAns.removeCropped_Not(problem, croppedImg, 'top-small', 60)

              # crop test
                logging.debug("****** crop test4b (bottom) *****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'C','F','F','bottom')
                if rc == True:
                    #answer must have same cropped portion, eliminate those that do not
                    logging.debug("loop through answers, eliminating those without the cropped image of C&F")
                    agtAns.removeCropped_Not(problem, croppedImg, 'bottom')


                # crop test
                logging.debug("****** crop test5 DIAGONOLS (top) *****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'A','E','E','top')
                if rc == True:
                    #answer must have same cropped portion, eliminate those that do not
                    logging.debug("loop through answers, eliminating those without the cropped image of A&E")
                    agtAns.removeCropped_Not(problem, croppedImg, 'top')

                # crop test
                logging.debug("****** crop test5b DIAGONOLS (bottom) *****")
                rc, croppedImg = self.crop_and_test_3x3(problem, 'A','E','E','bottom')
                if rc == True:
                    #answer must have same cropped portion, eliminate those that do not
                    logging.debug("loop through answers, eliminating those without the cropped image of A&E")
                    agtAns.removeCropped_Not(problem, croppedImg, 'bottom')


            # do we have an answer yet?
            if agtAns.get_num_answers() == 1:
               logging.debug("only 1 answer to pick from...")
               answer = agtAns.get_fig_num(0)

            # equality test 2
            if answer == -1:
                logging.debug("****** equality test 3 *****")
                if self.images_are_equal(imgA, imgB, 50) and\
                   self.images_are_equal(imgB, imgC, 50) and\
                   self.images_are_equal(imgD, imgE, 50) and\
                   self.images_are_equal(imgE, imgF, 50) and\
                   self.images_are_equal(imgG, imgH, 50):
                    logging.debug("passed equality test 3")
                    answer = self.find_image_verbal(hasVerbal, problem,problem.figures['G'])

            # equality test 4
            if answer == -1:
                 logging.debug("****** equality test 4 *****")
                 if self.are_equal(hasVerbal, problem.figures['A'], problem.figures['B'], 50) and\
                   self.are_equal(hasVerbal, problem.figures['B'], problem.figures['C'], 50) and\
                   self.are_equal(hasVerbal, problem.figures['D'], problem.figures['E'], 50) and\
                   self.are_equal(hasVerbal, problem.figures['E'], problem.figures['F'], 50) and\
                   self.are_equal(hasVerbal, problem.figures['G'], problem.figures['H'], 50):
                        logging.debug("passed equality test 3")
                        answer = self.find_image_verbal(hasVerbal, problem,problem.figures['G'])

            if answer == -1:
                if hasVerbal:
                        # test for pattern in number of NONfills in outlying objects
                        logging.debug("**** 3x3 incremental pattern in the number of NONfills in outlying objects test ******")
                        found = 0
                        nnfillsC = self.num_nonfills(problem.figures['C'])
                        nnfillsF = self.num_nonfills(problem.figures['F'])
                        nnfillsG = self.num_nonfills(problem.figures['G'])
                        nnfillsH = self.num_nonfills(problem.figures['H'])
                        incremental_amt1 = nnfillsC - nnfillsF
                        incremental_amt2 = nnfillsG - nnfillsH
                        if incremental_amt1 == incremental_amt2 and\
                            nnfillsF == nnfillsH:  #we have a pattern
                                if incremental_amt1 < 0:  #means the number is increasing
                                    num_nonfills = nnfillsF + abs(incremental_amt1)
                                elif incremental_amt1 > 0: #means the number is decreasing
                                    num_nonfills = nnfillsF - abs(incremental_amt1)
                                else:
                                    num_nonfills = nnfillsF

                                agtAns.removeNonFillNum_not(num_nonfills, '=')
                else:
                   logging.debug("skipping test because not hasVerbal")


            if answer == -1:
                logging.debug("num answers left to pick from: %d", agtAns.get_num_answers())
                if agtAns.get_num_answers() == 1:
                   logging.debug("only 1 answer to pick from...")
                   answer = agtAns.get_fig_num(0)
            else:
                logging.debug("found answer")
            logging.debug("returning after 3x3 processing")


        return answer