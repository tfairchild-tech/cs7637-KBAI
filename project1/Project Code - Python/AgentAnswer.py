#
# tfairchild3  September 2015
#
# AgentAnswer represents the class used for answer related functions
# the object creates a list of the answers from the given problem
#

from PIL import Image
from PIL import ImageStat
from PIL import ImageChops
from AgentImage import AgentImage
from AgentAttribute import Attribute
from AgentBasic import AgentBasic

import logging
import os

__author__ = 'tfairchild3'

# instantiate and object of type AgentImage
ai = AgentImage()
# global value of threshold used for hash comparisons
threshold = 50.0

class AgentAnswer:

    def __init__(self, problem):

        # get all the problems answers into a list
        self.answerlist = []
        keylist = problem.figures.keys()
        keylist.sort()
        for figkey in keylist:
            # if the figure number is numeric then this is an answer figure
            if figkey.isdigit():
                #logging.debug("initializing figure %s, hasVerbal=%s, type=%s", figkey, problem.hasVerbal, problem.problemType)
                self.answerlist.append(problem.figures[figkey])

    #
    # prt_debug_info
    # used for debugging
    #
    def prt_debug_info(self, problem):
        # loop through objects in prob
        figkeylist = problem.objects.keys()
        figkeylist.sort()
        logging.debug(" ***** (%s) object  has %d figures (%s):", problem.visualFilename, len(figkeylist), figkeylist)
        for figkey in figkeylist:
            logging.debug("\t\tfigure: %s", figkey)
            # loop through attributes of each object
            attrlist = problem.objects[figkey].attributes.keys()
            for attrkey in attrlist:
                logging.debug("\t\t\t%s: %s", attrkey, problem.objects[figkey].attributes[attrkey])
        return

    #
    # show_prob_answer_list
    # shows each answer image to the console
    #
    def show_prob_answer_list(self):
        logging.debug("there are %d answers left...", len(self.answerlist))
        for i in range(0,len(self.answerlist)):
            if self.answerlist[i].visualFilename != '':
                logging.debug(" %s. answerlist fname: %s", i, self.answerlist[i].visualFilename)
                #self.prt_debug_info(self.answerlist[i])


        return

    # find_img(img)
    # loop through answerlist and eliminate_answer for the one matching the image provided
    #
    def removeImage(self, fname, threshold):
        img_to_remove = []
        diff_vals = []
        imgx = Image.open(fname)
        for i in range(0,len(self.answerlist)):
            found = 0
            # open
            fname = self.answerlist[i].visualFilename
            tmpimg = ai.open_problem_image(fname)
            fff = Image.new('RGBA', imgx.size, (255,)*4)
            imgx = Image.composite(imgx, fff, imgx)
            # get the difference using the rms (root mean square)
            diff = ImageStat.Stat(ImageChops.difference(imgx, tmpimg)).rms
            #logging.debug("diff from imagechops is %s", diff)
            diff_vals.append(diff[0])
            #if diff[0] < threshold:
            #    tmpimg.close()
            #    logging.debug("found image in our answerlist: %s...", i)
            #    found = 1
            #    break
            #else:
            #    tmpimg.close()
            tmpimg.close()

        #logging.debug("diff_vals=%s",diff_vals)
        (val, idx) = min((v,i) for i,v in enumerate(diff_vals))
        logging.debug("min diff_vals index=%s, val=%s", idx, val )
        if diff_vals[idx] < threshold:
            img_to_remove.append(idx)
        else:
            logging.debug("image not found in our answerlist...")
        #if found:
        #    img_to_remove.append(i)
        #else:
        #    logging.debug("image not found in our answerlist...")

        for x in sorted(img_to_remove,reverse=True):
            logging.debug("removing index %s from our answerlist", x)
            self.eliminate_answer(x)


    # removeCropped_Not(img)
    # loop through answerlist and eliminate_answer for whichever image doesn't match the image provided
    #
    def removeCropped_Not(self, problem, imgx, section, threshold=50):
        pop_index = []
        diff_list_tie = []
        logging.debug("in removeCropped_Not... num answers to search: %d", len(self.answerlist))
        for i in range(0,len(self.answerlist)):
            logging.debug("looking at answerlist #%d", i)
            # open the answer image
            fname = self.answerlist[i].visualFilename
            tmpimg = ai.open_problem_image(fname)
            #crop it
            w, h = tmpimg.size
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
            else: #bottom-third, default, this seems to work well...
                crop_box = (0,h/3,w,h)
            tmpimg = tmpimg.crop(crop_box)

            #make an rgb composite
            fff = Image.new('RGBA', imgx.size, (255,)*4)
            imgx = Image.composite(imgx, fff, imgx)
            # get the difference using the rms (root mean square)
            diff = ImageStat.Stat(ImageChops.difference(imgx, tmpimg)).rms
            logging.debug("answer %s diff = %s, threshold=%s", i, diff, threshold)
            if diff[0] < threshold:
                diff_list_tie.append(diff[0])
                logging.debug("found a match, keeping %d", i)
                tmpimg.close()
            else:
                logging.debug("no match, adding %d for removal", i)
                tmpimg.close()
                pop_index.append(i)

        if len(diff_list_tie) > 1:
            m = min(diff_list_tie)
            keep = [i for i, j in enumerate(diff_list_tie) if j == m]
            for x in range(0, len(diff_list_tie)):
                if x != keep[0]:
                    logging.debug("tiebreaker:  adding %s for removal", x)
                    # there can only be 1 winner when it is tied like this
                    if x not in pop_index:
                            pop_index.append(x)

        for x in sorted(pop_index,reverse=True):
            logging.debug("removing image %s", x)
            self.eliminate_answer(x)





    # removeNumObj_not(keepObjNum)
    # loop through answerlist and eliminate_answer for those without the same number of objects as keepObjNum
    #
    def removeNumObj_not(self, keepObjNum):
        pop_index = []
        for i in range(0,len(self.answerlist)):
            logging.debug("looking at %s, #objs=%s", i, len(self.answerlist[i].objects.keys()))
            if len(self.answerlist[i].objects.keys()) != keepObjNum:
                logging.debug("adding index %s", i)
                pop_index.append(i)

        for x in sorted(pop_index,reverse=True):
            logging.debug("removing %s", x)
            self.eliminate_answer(x)



    # NOT USED
    # removeCommonObj(problem)
    def findCommonObj(self,p1,p2,p3):
        # loop through each object in problem
        found = 1
        for p1f in p1.objects.keys():
            attrlist = p1.objects[p1f].attributes.keys()
            for p1a in attrlist:
                p1.objects[p1f].attributes[p1a]

        # if it appears in every object then the answer must have it too
        # if it doesn't then remove the answer

        # ABANDONED...
        return

    # removeNumObj_not(keepObjNum)
    # loop through answerlist and eliminate_answer for those without the same number of objects as keepObjNum
    #
    def removeShapeObj_notBAK(self, keepObjShape):
        pop_index = []
        #logging.debug("in removeShapeObj_not... we have %s in our answerlist", len(self.answerlist))
        for i in range(0,len(self.answerlist)):
            added = 0
            if added == 0:
                #logging.debug("looking at %s, #objs=%s", i, len(self.answerlist[i].objects.keys()))
                for figkey in self.answerlist[i].objects.keys():
                    #logging.debug("looking for %s in %s", keepObjShape, figkey)
                    attrlist = self.answerlist[i].objects[figkey].attributes.keys()
                    for attrkey in attrlist:
                        #logging.debug("this is the answer %s info \t\t\t%s: %s", figkey, attrkey, self.answerlist[i].objects[figkey].attributes[attrkey])
                        if attrkey == 'shape' and self.answerlist[i].objects[figkey].attributes[attrkey] != keepObjShape:
                            logging.debug("going to remove %s answer with shape %s", i, self.answerlist[i].objects[figkey].attributes[attrkey])
                            if i not in pop_index:
                                pop_index.append(i)
                            added = 1
                            #break
                        elif attrkey == 'shape' and self.answerlist[i].objects[figkey].attributes[attrkey] == keepObjShape:
                            logging.debug("check to see if we added figure to remove list, if so take it off of the list")
                            if i in pop_index:
                                pop_index.pop(i)
                            #break
            else:
                break

        for x in sorted(pop_index,reverse=True):
            logging.debug("removing %s", x)
            self.eliminate_answer(x)

    # removeNumObj_not(keepObjNum)
    # loop through answerlist and eliminate_answer for those without the same number of objects as keepObjNum
    #
    def removeShapeObj_not(self, keepObjShape):
        # init the lists that will contain object stuff
        pop_index = []

        logging.debug("in removeShapeObj_not... we have %s in our answerlist... need to remove all without %s", len(self.answerlist), keepObjShape)
        for i in range(0,len(self.answerlist)):
                shape_list = []
                #logging.debug("looking at %s, #objs=%s", i, len(self.answerlist[i].objects.keys()))
                # loop through all figures in object p1 and create an Attribute object for each one
                for figkey in self.answerlist[i].objects.keys():
                    s = Attribute(self.answerlist[i].objects[figkey].attributes).get_shape()
                    if s not in shape_list:
                        shape_list.append(s) # ex: {'shape': 'square', 'size': 'very large', 'fill': 'yes'}

                logging.debug("shapes for this answer are: %s", shape_list)
                # if elements in shape_list do not contain all elements in keepObjShape then add it to the pop list
                S1 = set(keepObjShape)
                S2 = set(shape_list)

                if [item in keepObjShape for item in shape_list]:
                    if item not in keepObjShape:
                        logging.debug("-->%s",item)
                        pop_index.append(i)

                if any([item in keepObjShape for item in shape_list]) == False:
                    if i not in pop_index:
                        pop_index.append(i)

        for x in sorted(pop_index,reverse=True):
            logging.debug("removing %s", x)
            self.eliminate_answer(x)




    def removeFillNum_not2(self, nfill, probtype, op):
        pop_index = []
        logging.debug("in removeFillNum_not2(%s)... we have %s in our answerlist", nfill, len(self.answerlist))
        for i in range(0,len(self.answerlist)):
                num_fills = 0

                f = 0
                for figkey in self.answerlist[i].objects.keys():
                    #logging.debug("looking for fill in %s", figkey)
                    attrlist = self.answerlist[i].objects[figkey].attributes.keys()
                    for attrkey in attrlist:
                        #logging.debug("this is the answer %s info \t\t\t%s: %s", figkey, attrkey, self.answerlist[i].objects[figkey].attributes[attrkey])
                        if attrkey == 'fill' and self.answerlist[i].objects[figkey].attributes[attrkey] == 'yes':
                            f = f + 1

                if probtype == '2x2':
                    if not f >= nfill:
                        logging.debug("number of fills found = %s adding %s to pop_index",f, i)
                        pop_index.append(i)
                else:
                    #if not f >= nfill-1:
                    #    logging.debug("number of fills found = %s adding %s to pop_index",f, i)
                    #    pop_index.append(i)
                    #
                    if op == '+' or op == '*':
                        # increasing trend so num_fills must be greater than num, pop everything else
                        if nfill < f:
                            logging.debug("(+)... adding %s to pop_index", i)
                            pop_index.append(i)
                    elif op == '-':
                        # decreasing trend so must be less than num, pop everything else
                        if nfill > f:
                            logging.debug("(-)... adding %s to pop_index", i)
                            pop_index.append(i)
                    else:
                        # stable trend so must be equal to num, pop everything else
                        if nfill != f:
                            logging.debug("(=)... number of fills found = %s", num_fills)
                            logging.debug("(=)... adding %s to pop_index", i)
                            pop_index.append(i)

        if len(pop_index) > 0:
            for x in sorted(pop_index,reverse=True):
                logging.debug("removing %s", x)
                self.eliminate_answer(x)








    # removeFillNum_not(num, operator)
    # loop through answerlist and eliminate_answer for those without the same number of objects as keepObjNum
    #
    def removeFillNum_not(self, num, op):
        pop_index = []
        logging.debug("in removeFillNum_not(%s,%s)... we have %s in our answerlist", num, op, len(self.answerlist))

        for i in range(0,len(self.answerlist)):
                num_fills = 0
                logging.debug("looking at %s, #objs=%s", i, len(self.answerlist[i].objects.keys()))
                for figkey in self.answerlist[i].objects.keys():

                    attrlist = self.answerlist[i].objects[figkey].attributes.keys()
                    for attrkey in attrlist:
                        #logging.debug("this is the answer %s info \t\t\t%s: %s", figkey, attrkey, self.answerlist[i].objects[figkey].attributes[attrkey])
                        if attrkey == 'fill' and self.answerlist[i].objects[figkey].attributes[attrkey] == 'yes':
                            num_fills = num_fills + 1

                if op == '+':
                    # increasing trend so num_fills must be greater than num, pop everything else
                    if num_fills < num:
                        logging.debug("(+)... adding %s to pop_index", i)
                        pop_index.append(i)
                elif op == '-':
                    # decreasing trend so must be less than num, pop everything else
                    if num_fills > num:
                        logging.debug("(-)... adding %s to pop_index", i)
                        pop_index.append(i)
                else:
                    # stable trend so must be equal to num, pop everything else
                    if num_fills != num:
                        logging.debug("(=)... number of fills found = %s", num_fills)
                        logging.debug("(=)... adding %s to pop_index", i)
                        pop_index.append(i)

        if len(pop_index) > 0:
            for x in sorted(pop_index,reverse=True):
                logging.debug("removing %s", x)
                self.eliminate_answer(x)

    # removeNonFillNum_not(num, operator)
    # loop through answerlist and eliminate_answer for those without the same number of objects as keepObjNum
    #
    def removeNonFillNum_not(self, num, op):
        pop_index = []
        logging.debug("in removeNonFillNum_not(%s,%s)... we have %s in our answerlist", num, op, len(self.answerlist))

        for i in range(0,len(self.answerlist)):
                num_nonfills = 0
                logging.debug("looking at %s, #objs=%s", i, len(self.answerlist[i].objects.keys()))
                for figkey in self.answerlist[i].objects.keys():
                    #logging.debug("looking for fill in %s", figkey)
                    attrlist = self.answerlist[i].objects[figkey].attributes.keys()
                    for attrkey in attrlist:
                        #logging.debug("this is the answer %s info \t\t\t%s: %s", figkey, attrkey, self.answerlist[i].objects[figkey].attributes[attrkey])
                        if attrkey == 'fill' and self.answerlist[i].objects[figkey].attributes[attrkey] == 'no':
                            num_nonfills = num_nonfills + 1

                if op == '+':
                    # increasing trend so num_fills must be greater than num, pop everything else
                    if num_nonfills < num:
                        logging.debug("(+)... adding %s to pop_index", i)
                        pop_index.append(i)
                elif op == '-':
                    # decreasing trend so must be less than num, pop everything else
                    if num_nonfills > num:
                        logging.debug("(-)... adding %s to pop_index", i)
                        pop_index.append(i)
                else:
                    # stable trend so must be equal to num, pop everything else
                    if num_nonfills != num:
                        logging.debug("(=)... number of NONfills found = %s", num_nonfills)
                        logging.debug("(=)... adding %s to pop_index", i)
                        pop_index.append(i)

        if len(pop_index) > 0:
            for x in sorted(pop_index,reverse=True):
                logging.debug("removing %s", x)
                self.eliminate_answer(x)



    # eliminate_answer
    # eliminates an answer from our list
    #
    def eliminate_answer(self,idx):
        if len(self.answerlist) > 1:
            self.answerlist.pop(idx)

    # get_num_answers
    #
    # returns the number of answer objects we have left, ie, we have not eliminated
    def get_num_answers(self):
        return len(self.answerlist)

    def get_fig_num(self,idx):
        root, ext = os.path.splitext(self.answerlist[idx].visualFilename)
        head, tail = os.path.split(self.answerlist[idx].visualFilename)
        head, tail = os.path.splitext(tail)
        return head