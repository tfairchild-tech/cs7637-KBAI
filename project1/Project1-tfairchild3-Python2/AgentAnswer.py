#
# tfairchild3  September 2015
#
# AgentAnswer represents the class used for answer related functions
# the object creates a list of the answers from the given problem
#

from AgentImage import AgentImage

__author__ = 'tfairchild3'

class AgentAnswer:

    def __init__(self, problem):

        # get all the problems answers into a list
        self.answerlist = []
        keylist = problem.figures.keys()
        keylist.sort()
        for figkey in keylist:
            # if the figure number is numeric then this is an answer figure
            if figkey.isdigit():
                self.answerlist.append(problem.figures[figkey])


    #
    # show_prob_answer_list
    # shows each answer image to the console
    #
    def show_prob_answer_list(self):
        for i in range(0,len(self.answerlist)):
            if self.answerlist[i].visualFilename != '':
                ii = AgentImage.open_problem_image(self.answerlist[i].visualFilename)
                ii.show()
        return
