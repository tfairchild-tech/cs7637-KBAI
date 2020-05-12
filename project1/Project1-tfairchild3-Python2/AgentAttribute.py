#
# tfairchild3  September 2015
#
# Attribute represents the container class for an attribute and defines
# tests and functions on one or more attribute objects
#

__author__ = 'tfairchild3'

class Attribute:

    def __init__(self, dictionary):

        # instantiates a new object
        # example of attribute keys: {'shape','size','fill','inside','width','length','angle','left-of','above'}

        if len(dictionary):

            try:
                setattr(dictionary, 'left-of', 'leftof')
            except:
                pass

            try:
                self.shape = dictionary.get('shape', 'None')
            except KeyError:
                pass

            try:
                self.size = dictionary.get('size', 'None')
            except KeyError:
                pass

            try:
                self.fill = dictionary.get('fill', 'None')
            except KeyError:
                pass

            try:
            # TODO: not sure of how to process the inside attribute yet, so for now just return None
            # TODO: this will allow comparisons to happen regardless of inside value
            #    i = dictionary.get('inside','None')
            #    if i != 'None':
            #        i_list = [x.strip() for x in i.split(',')]
            #        self.inside = len(i_list)
            #    else:
                    self.inside = 'None'
            except KeyError:
                pass

            try:
                self.width = dictionary.get('width',999)
            except KeyError:
                pass

            try:
                self.length = dictionary.get('length',999)
            except KeyError:
                pass

            try:
                self.angle = dictionary.get('angle',999)
            except KeyError:
                pass

            try:
                self.leftof = dictionary.get('leftof',999)
            except KeyError:
                pass

            try:
                self.above = dictionary.get('above',999)
            except KeyError:
                pass


    # set_figure_index
    # this sub returns the number index of the object after it's been mapped from the letter to the corresponding number
    # for example, if figure index = a and it's the first figure in the set then number would be 1, b = 2, c = 3, etc.
    # another example, if figure index = f and its the first figure in the set then number would be 1, g=2, h=3, etc.
    # TODO: not used at this time
    def set_figure_index(self, letter, num):
        self.figureIndex = {letter:num}

    # set_shape
    def set_shape(self, s):
        self.shape = s
        return

    # set_size
    def set_size(self, sz):
        self.size = sz

    # set_fill
    def set_fill(self, f):
        self.fill = f

    # set_inside
    def set_inside(self, i):
        #if i != 'None':
        #    i_list = [x.strip() for x in i.split(',')]
        #    #i_str = ','.join(sorted(i_list))
        #    # can't figure out a good algorithm here so set inside value = len(i) instead of the actual i val
        #    self.inside = str(len(i_list))
        #else:
            self.inside = 'None'

    # set_angle
    def set_angle(self, a):
        self.angle = a

    # set_above
    def set_above(self, a):
        self.above = a

    # set_width
    def set_width(self, w):
        self.width = w

    # set_length
    def set_length(self,l):
        self.length = l

    # set_left_of
    def set_left_of(self,l):
        self.leftof = l

    # get_figure_index
    def get_figure_index(self):
        return self.figureIndex

    # get_shape
    def get_shape(self):
        try:
            return self.shape
        except:
            return 'None'

    # get_size
    def get_size(self):
        try:
            return self.size
        except:
            return 999

    # get_fill
    def get_fill(self):
        try:
            return self.fill
        except:
            return 999

    # get_inside
    def get_inside(self):
        try:
            return str(self.inside)
        except:
            return 999

    # get_left_of
    def get_left_of(self):
        try:
            return self.leftof
        except:
            return 999

    # get_above
    def get_above(self):
        try:
            return self.above
        except:
            return 999

    # get_angle
    def get_angle(self):
        try:
            return self.angle
        except:
            return 999

    # get_width
    def get_width(self):
        try:
            return self.width
        except:
            return 999

    # get_length
    def get_length(self):
        try:
            return self.length
        except:
            return 999

    # get_attributes_str
    def get_attributes_str(self):
        return "%s,%s,%s,%s,%s,%s,%s" % (self.shape,self.size,self.angle,self.fill,self.inside,self.width,self.length)

    # get_attributes
    def get_attributes(self):
        return self.shape,self.size,self.angle,self.fill,self.inside,self.width,self.length

    # get_attribute_dict
    # returns a dictionary object of this attribute
    def get_attribute_dict(self):
        thisDict = {}
        try:
            thisDict['shape'] = self.get_shape()
        except:
            AttributeError

        try:
            thisDict['size'] = self.get_size()
        except:
            AttributeError

        try:
            thisDict['fill'] = self.get_fill()
        except:
            AttributeError

        try:
            thisDict['inside'] = self.get_inside()
        except:
            AttributeError

        try:
            thisDict['width'] = self.get_width()
        except:
            AttributeError

        try:
            thisDict['length'] = self.get_length()
        except:
            AttributeError

        try:
            thisDict['angle'] = self.get_angle()
        except:
            AttributeError

        try:
            thisDict['left-of'] = self.get_left_of()
        except:
            AttributeError

        try:
            thisDict['above'] = self.get_above()
        except:
            AttributeError

        return thisDict

    # the_same
    # tests if two attribute objects are the same
    def the_same(self, attrA,attrB):
        if attrA.get_shape() == attrB.get_shape() and\
            attrA.get_size() == attrB.get_size() and\
            attrA.get_fill() == attrB.get_fill() and\
            attrA.get_left_of() == attrB.get_left_of() and\
            attrA.get_width() == attrB.get_width() and\
            attrA.get_length() == attrB.get_length() and\
            attrA.get_inside() == attrB.get_inside() and\
            attrA.get_angle() == attrB.get_angle() and\
            attrA.get_above() == attrB.get_above():
            return True
        else:
            return False

    # get_diffs
    # compare the attribute sets returning a set with only the figures that are different
    def get_diffs(self, list1, list2):

        list_return = list(list1)

        # loop through each list, comparing attributes...
        if len(list1) == len(list2):
            for attrA in list1:
                for attrB in list2:
                    if self.the_same(attrA,attrB) == True:
                        list_return.remove(attrA)
                        break
        else:
            # they can't be equal so just return list_return which is the value of list1
            pass

        return list_return

    # get_sames
    # compare the attribute sets returning a set with only the figures that are different
    def get_sames(self, list1, list2):

        list_return = list(list1)

        # loop through each list, comparing attributes...
        for attrA in list1:
            for attrB in list2:
                if self.the_same(attrA,attrB) == True:
                    list_return.append(attrA)
                    break

        return list_return

    # compare_item
    def compare_item(self,itemA,itemB):
        if itemA == itemB:
            return 'unchanged'
        else:
            return itemB

    # upd_fig_references
    def upd_fig_references(self,figList):
        return