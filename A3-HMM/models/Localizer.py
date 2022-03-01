
#
# The Localizer binds the models together and controls the update cycle in its "update" method.
#

from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
import random

from models import StateModel, TransitionModel, ObservationModel, RobotSimAndFilter


class Localizer:
    def __init__(self, sm):

        self.__sm = sm

        self.__tm = TransitionModel(self.__sm)
        self.__om = ObservationModel(self.__sm)

        # change in initialise in case you want to start out with something else
        # initialise can also be called again, if the filtering is to be reinitialised without a change in size
        self.initialise()

    # retrieve the transition model that we are currently working with
    def get_transition_model(self) -> np.array:
        return self.__tm

    # retrieve the observation model that we are currently working with
    def get_observation_model(self) -> np.array:
        return self.__om

    # the current true pose (x, h, h) that should be kept in the local variable __trueState
    def get_current_true_pose(self) -> Tuple[int, int, int]:
        x, y, h = self.__sm.state_to_pose(self.__trueState)
        return x, y, h

    # the current probability distribution over all states
    def get_current_f_vector(self) -> np.array(float):
        return self.__probs

    # the current sensor reading (as position in the grid). "Nothing" is expressed as None
    def get_current_reading(self) -> Tuple[int, int]:
        ret = None
        if self.__sense is not None:
            ret = self.__sm.reading_to_position(self.__sense)
        return ret

    # get the currently most likely position, based on single most probable pose
    def most_likely_position(self) -> Tuple[int, int]:
        return self.__estimate

    ################################### Here you need to really fill in stuff! ##################################
    # if you want to start with something else, change the initialisation here!
    #
    # (re-)initialise for a new run without change of size
    def initialise(self):
        self.__trueState = random.randint(0, self.__sm.get_num_of_states() - 1)
        self.__sense = None
        self.__probs = np.ones(self.__sm.get_num_of_states()) / \
            (self.__sm.get_num_of_states())
        self.__estimate = self.__sm.state_to_position(np.argmax(self.__probs))

    # add your simulator and filter here, for example

        #self.__rs = RobotSimAndFilter.RobotSim( ...)
        #self.__HMM = RobotSimAndFilter.HMMFilter( ...)
    #
    #  Implement the update cycle:
    #  - robot moves one step, generates new state / pose
    #  - sensor produces one reading based on the true state / pose
    #  - filtering approach produces new probability distribution based on
    #  sensor reading, transition and sensor models
    #
    #  Add an evaluation in terms of Manhattan distance (average over time) and "hit rate"
    #  you can do that here or in the simulation method of the visualisation, using also the
    #  options of the dashboard to show errors...
    #
    #  Report back to the caller (viewer):
    #  Return
    #  - true if sensor reading was not "nothing", else false,
    #  - AND the three values for the (new) true pose (x, y, h),
    #  - AND the two values for the (current) sensor reading (if not "nothing")
    #  - AND the error made in this step
    #  - AND the new probability distribution
    #

    def next_state(self, true_state) -> int:
        limit = random.random()
        print(limit)
        for state in range(self.__tm.get_num_of_states()):
            if state != true_state:
                prob = self.__tm.get_T_ij(true_state, state)
                if limit < prob:
                    return state
                limit -= prob

        return true_state

    def sense(self, true_state) -> int:
        limit = random.random()
        for reading in range(self.__om.get_nr_of_readings() - 1):
            prob = self.__om.get_o_reading_state(reading, true_state)
            if limit < prob:
                return reading
            limit -= prob

        return None

    def forward_filter(self):
        self.__probs = self.__om.get_o_reading(
            self.__sense) @ self.__tm.get_T_transp() @ self.__probs
        alpha = 1 / np.sum(self.__probs)
        self.__probs *= alpha

    def estimate_pos(self) -> int:
        best_state = 0
        highest_prob = 0

        for state in range(self.__tm.get_num_of_states()):
            prob = self.__probs[state]
            if prob > highest_prob:
                highest_prob = prob
                best_state = state

        return best_state

    def update(self) -> Tuple[bool, int, int, int, int, int, int, int, int, np.array]:

        ret = False  # in case the sensor reading is "nothing" this is kept...
        self.__trueState = self.next_state(self.__trueState)
        tsX, tsY, tsH = self.__sm.state_to_pose(self.__trueState)

        self.__sense = self.sense(self.__trueState)

        srX = -1
        srY = -1
        if self.__sense != None:
            srX, srY = self.__sm.reading_to_position(self.__sense)
            ret = True

        self.forward_filter()

        self.__estimate = self.__sm.state_to_position(self.estimate_pos())

        eX, eY = self.__estimate

        # Manhattan error
        error = abs(eX - tsX) + abs(eY - tsY)

        # if you use the visualisation (dashboard), this return statement needs to be kept the same
        # or the visualisation needs to be adapted (your own risk!)
        return ret, tsX, tsY, tsH, srX, srY, eX, eY, error, self.__probs
