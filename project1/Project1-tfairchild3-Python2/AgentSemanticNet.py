#
# tfairchild3  September 2015
#
# AgentSemanticNet represents the class used for performing semantic network operations on the images
# using the verbal representations
#

import logging
from AgentImage import AgentImage
from AgentAttribute import Attribute


__author__ = 'tfairchild3'


# instantiate and object of type AgentImage
ai=AgentImage()

# used for mapping the figure letter index to a number index
figIndexList = dict()

class SemanticNet:

    def __init__(self):
        logging.info('  Starting AgentSemanticNet')


    #
    # prt_debug_info
    # used for debugging
    #
    def prt_debug_info(self, title, problem):
        # loop through objects in prob
        figkeylist = problem.objects.keys()
        logging.debug(" ***** (%s) object %s has %d figures (%s):", problem.visualFilename, title, len(figkeylist), figkeylist)
        for figkey in figkeylist:
            logging.debug("\t\tfigure: %s", figkey)
            # loop through attributes of each object
            attrlist = problem.objects[figkey].attributes.keys()
            for attrkey in attrlist:
                logging.debug("\t\t\t%s: %s", attrkey, problem.objects[figkey].attributes[attrkey])
        return

    #
    # find_semantic_net_answer
    # loops through each answer in the problem set looking for a match with the new attribute we build
    # using semantic networking methods
    #
    def find_semantic_net_answer(self, problem, guessVerbal):

        answer = -1

        logging.debug(" guess verbal attributes:")
        for x in range(0,len(guessVerbal)):
            logging.debug(" *** %s: %s", x, guessVerbal[x].get_attribute_dict())

        # loop through problem answers looking for the image that matches
        figkeylist = problem.figures.keys()
        for figkey in sorted(figkeylist):
            if answer == -1:
                # if figure is a number then this is an answer we need to look at
                if figkey.isdigit():
                    count = 0
                    attr_list1 = []
                    objkeylist = problem.figures[figkey].objects.keys()
                    #logging.debug("figure key=%s",figkey)
                    for objkey in objkeylist:
                        count = count + 1
                        #logging.debug("\t\t\tfigure %s, %s: %s... %s", figkey, objkeylist, objkey, problem.figures[figkey].objects[objkey].attributes.keys())
                        # loop through attributes of each object
                        a = Attribute(problem.figures[figkey].objects[objkey].attributes)
                        attr_list1.append(a)
                        figIndexList[objkey]=count
                        #logging.debug("just appended %s", a.get_attribute_dict())
                        #attrlist = problem.figures[figkey].objects[objkey].attributes.keys()
                        #for attrkey in attrlist:
                        #    logging.debug("\t\t\t attrkey=%s, value= %s", attrkey, problem.figures[figkey].objects[objkey].attributes[attrkey])#.attributes[attrkey])

                    #logging.debug("about to remap_index_vals for attr_list1 (figure %s)", figkey)
                    #attr_list1 = self.remap_index_vals(attr_list1)

                    logging.debug(" problem figure #%s attributes:", figkey)
                    for x in range(0,len(attr_list1)):
                        logging.debug(" *** %s: %s", x, attr_list1[x].get_attribute_dict())

                    diff = Attribute([]).get_diffs(attr_list1, guessVerbal)
                    #for x in range(0,len(diff)):
                    #    logging.debug("diff: %s, %s", x, diff[x].get_attributes())
                    if len(diff) == 0:
                        answer = figkey
                        break

            else:
                break

        return answer

    #
    # remap_index_vals
    # maps letter indices to number indices
    #
    def remap_index_vals(self,aList):

        inside_vals = []

        #in order to get accurate comparisons we have to update the references to the figure numbers using figIndexList
        for attr in aList:
            inside_vals = attr.get_inside()

            if inside_vals != 'None':
                #    for index, elem in enumerate(inside_vals):
                #        logging.debug("index=%s, elem=%s, inside=%s", index, elem, str(inside_vals))
                #        inside_vals[index] = map[elem]
                #    inside_vals = str(inside_vals).strip('[]')
                #    attr.set_inside(inside_vals)
                for key in sorted(figIndexList.keys()):
                    inside_vals = inside_vals.replace(key,str(figIndexList[key]))

                attr.set_inside(inside_vals)

        return aList

    #
    # AB_Cx
    # compares A to B and builds a new attribute for C to x
    #
    def AB_Cx(self, p1, p2, p3):

        attr_list1 = []
        attr_list2 = []
        attr_list3 = []
        attrNew_list = []

        logging.debug(" in AB_Cx")
        self.prt_debug_info("A", p1)
        self.prt_debug_info("B", p2)
        self.prt_debug_info("C", p3)

        # create a new empty attribute set
        attrNew = Attribute([])

        #loop through all figures of each object and create an Attribute object for each one
        count = 0
        numFigsA = len(p1.objects.keys())
        for figkey in p1.objects.keys():
            count = count +1
            a = Attribute(p1.objects[figkey].attributes)# ex: {'shape': 'square', 'size': 'very large', 'fill': 'yes'}
            a.set_figure_index(figkey, count)
            figIndexList[figkey]=count
            attr_list1.append(a)
            #figmapA[figkey] = count

        count = 0
        numFigsB = len(p2.objects.keys())
        for figkey in p2.objects.keys():
            count = count +1
            a = Attribute(p2.objects[figkey].attributes)# ex: {'shape': 'square', 'size': 'very large', 'fill': 'yes'}
            a.set_figure_index(figkey, count)
            figIndexList[figkey]=count
            attr_list2.append(a)
            #figmapB[figkey] = count

        count = 0
        numFigsC = len(p3.objects.keys())
        for figkey in p3.objects.keys():
            count = count +1
            a = Attribute(p3.objects[figkey].attributes)# ex: {'shape': 'square', 'size': 'very large', 'fill': 'yes'}
            a.set_figure_index(figkey, count)
            figIndexList[figkey]=count
            attr_list3.append(a)
            #figmapA[figkey] = count


        # remap_index_vals not used
        #logging.debug(" figIndexList=%s", numFigsA, numFigsB, numFigsC,figIndexList)
        #attr_list1 = self.remap_index_vals(attr_list1)
        #attr_list2 = self.remap_index_vals(attr_list2)
        #attr_list3 = self.remap_index_vals(attr_list3)


        # comparisons not used
        #inA_notB = Attribute([]).get_diffs(attr_list1, attr_list2)
        #for attr in inA_notB:
        #    logging.debug(" elements inA_notB: %s", attr.get_attributes())
        #inB_notA = Attribute([]).get_diffs(attr_list2, attr_list1)
        #for attr in inB_notA:
        #    logging.debug(" elements inB_notA: %s", attr.get_attributes())
        #inAB = Attribute([]).get_sames(attr_list1, attr_list2)
        #for attr in inAB:
        #    logging.debug(" elements in both: %s", attr.get_attributes())

        # TODO: possible semantic net algorithm
        # not used
        #
        # first pass, eliminate/pop all figures that match - we use this below
        # (try to create or add to a figure to figure mapping)
        # which will hopefully give us a process of elimination type advantage
        # next... for each answer available to us
                # if only 1 answer left in list, then this could be our guess
                # else...
                # inC_notD =
                # inD_notC =
                # inCD =
                # if len(inA_notB) != len(inC_notD) eliminate/pop this answer and break
                # if len(inB_notA) != len(inD_notC) eliminate/pop this answer and break
                # if len(inAB) != len(inCD) eliminate/pop this answer and break
                # eliminate/pop (or save?) the figures in CD that match and concentrate on the differences
                # (try to create a figure to figure mapping)


        #foreach figure in A and each figure in B
        #compare the attributes, going in order for now
        while len(attr_list1)>0 or len(attr_list2)>0 or len(attr_list3)>0:
            if len(attr_list1)>0:
                fig1 = attr_list1.pop()
            else:
                fig1 = []

            if len(attr_list2)>0:
                fig2 = attr_list2.pop()
            else:
                fig2 = []

            if len(attr_list3)>0:
                fig3 = attr_list3.pop()
            else:
                fig3 = []

            attrNew = Attribute([])

            # comparing fig1 and fig2...
            if fig1 and fig2:
                # shape
                if fig1.get_shape() == fig2.get_shape():
                    attrNew.set_shape(fig3.get_attribute_dict().get('shape'))
                else:
                    attrNew.set_shape(fig2.get_shape())

                # size
                if fig1.get_size() == fig2.get_size():
                    attrNew.set_size(fig3.get_attribute_dict().get('size'))
                else:
                    attrNew.set_size(fig2.get_size())

                # fill
                if fig1.get_fill() == fig2.get_fill():
                    attrNew.set_fill(fig3.get_attribute_dict().get('fill'))
                else:
                    attrNew.set_fill(fig2.get_fill())

                # angle
                if fig1.get_angle() == fig2.get_angle():
                    attrNew.set_angle(fig3.get_attribute_dict().get('angle'))
                else:
                    attrNew.set_angle(fig2.getAngle())

                #inside
                #if fig1.get_inside() == fig2.get_inside():
                #    attrNew.set_inside(fig3.get_attribute_dict().get('inside'))
                #else:
                #    attrNew.set_inside(fig2.get_inside())
                attrNew.set_inside('None')

                # width
                if fig1.get_width() == fig2.get_width():
                    attrNew.set_width(fig3.get_attribute_dict().get('width'))
                else:
                    attrNew.set_width(fig2.get_width())

                # length
                if fig1.get_length() == fig2.get_length():
                    attrNew.set_length(fig3.get_attribute_dict().get('length'))
                else:
                    attrNew.set_length(fig2.get_length())

                # left-of
                # need to call it left-of here instead of leftOf as in the attribute class
                # because we are comparing it to the left-of property in the answers
                if fig1.get_left_of() == fig2.get_left_of():
                    attrNew.set_left_of(fig3.get_attribute_dict().get('left-of'))
                else:
                    attrNew.set_left_of(fig2.get_left_of())

                # above
                if fig1.get_above() == fig2.get_above():
                    attrNew.set_above(fig3.get_attribute_dict().get('above'))
                else:
                    attrNew.set_above(fig2.gt_above())

            elif fig3:
                attrNew.set_shape(fig3.get_attribute_dict().get('shape'))
                attrNew.set_size(fig3.get_attribute_dict().get('size'))
                attrNew.set_fill(fig3.get_attribute_dict().get('fill'))
                attrNew.set_angle(fig3.get_attribute_dict().get('angle'))
                attrNew.set_inside(fig3.get_attribute_dict().get('inside'))
                attrNew.set_width(fig3.get_attribute_dict().get('width'))
                attrNew.set_length(fig3.get_attribute_dict().get('length'))

            if attrNew.get_shape() != None:
                attrNew_list.append(attrNew)

        # attrNew_list = self.remap_index_vals(attrNew_list)

        return attrNew_list


    # print debug info
    # do_debug
    def do_debug(self,problem):
        logging.debug(" %s, problem type=%s, hasVisual=%s", problem.name, problem.problemType, problem.hasVerbal)
        logging.debug(" keylist %s", problem.figures.keys())


    #
    # solve using semantic network method
    #
    def solve(self,problem):
        answer = -1
        guessVerbal = []
        if problem.hasVerbal == 'False':
            logging.debug("hasVerbal is False, returning from SemanticNet")
            return -1

        self.do_debug(problem)

        if problem.problemType == '2x2':
            guessVerbal = self.AB_Cx(problem.figures['A'], problem.figures['B'], problem.figures['C'])
            if len(guessVerbal):
                answer = self.find_semantic_net_answer(problem, guessVerbal)

        return answer
