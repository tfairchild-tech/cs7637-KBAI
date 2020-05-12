#
# tfairchild3  September 2015
#
# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.

from AgentSemanticNet import SemanticNet
from AgentBasic import AgentBasic
from AgentImage import AgentImage
from AgentAnswer import AgentAnswer

import logging

# instantiate and object of type AgentImage
ai = AgentImage()

class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        pass
        # logging.basicConfig(filename='myagent.log', level=logging.INFO)
        logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', level=logging.INFO)
        logging.info("  Starting Agent")

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

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an integer representing its
    # answer to the question: "1", "2", "3", "4", "5", or "6". These integers
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName() (as Strings).
    #
    # In addition to returning your answer at the end of the method, your Agent
    # may also call problem.checkAnswer(int givenAnswer). The parameter
    # passed to checkAnswer should be your Agent's current guess for the
    # problem; checkAnswer will return the correct answer to the problem. This
    # allows your Agent to check its answer. Note, however, that after your
    # agent has called checkAnswer, it will *not* be able to change its answer.
    # checkAnswer is used to allow your Agent to learn from its incorrect
    # answers; however, your Agent cannot change the answer to a question it
    # has already answered.
    #
    # If your Agent calls checkAnswer during execution of Solve, the answer it
    # returns will be ignored; otherwise, the answer returned at the end of
    # Solve will be taken as your Agent's answer to this problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.

    def Solve(self, problem):

        logging.info("  =============== Problem = %s ===============", problem.name)

        guess = -1

        # agtAns is a list of the answers available to the agent, initialized from the numeric figure numbers in the problem
        # AgentBasic will pop from this list when it is obvious that the answer object cannot be correct
        # get the list of answer choices
        agtAns = AgentAnswer(problem)

        # apply the simple tests first
        guess  = AgentBasic().solve(problem, agtAns)

        # if answer is not found then apply the semantic network logic
        if guess == -1:
            sm = SemanticNet()
            guess = sm.solve(problem)

        # show the answers we have not eliminated so far
        #agtAns.show_prob_answer_list()
        #test the elimination
        #agtAns.eliminate_answer(0)
        #agtAns.show_prob_answer_list()

        if guess != -1:
            answer = problem.checkAnswer(guess)
            logging.info("  guess = %s, correct answer: %s %s", guess, answer, " << CORRECT" if answer == int(guess) else " >> WRONG")
        else:
            logging.info("  << SKIPPED >>")

        return guess
