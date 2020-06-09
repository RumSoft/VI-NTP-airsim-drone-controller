import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class Fuzzy:
    def __init__(self):
        self.control = self._init(0.01)

    def _init(self, precision):

        left = ctrl.Antecedent(np.arange(0, 1, precision), 'left')
        left["close"] = fuzz.trimf(left.universe, [-0.417, 0, 0.89815])
        left["far"] = fuzz.trimf(left.universe, [0.099206, 1, 1.42])

        right = ctrl.Antecedent(np.arange(0, 1, precision), "right")
        right["close"] = fuzz.trimf(right.universe, [-0.417, 0, 0.90608])
        right["far"] = fuzz.trimf(right.universe, [0.10714, 1, 1.42])

        mid = ctrl.Antecedent(np.arange(0, 1, precision), "mid")
        mid["close"] = fuzz.trapmf(mid.universe, [-1, 0.1, 0.3, 1])
        mid["far"] = fuzz.trimf(mid.universe, [0.1045, 1, 1.42])

        horizontal = ctrl.Consequent(np.arange(-1, 1, precision), "horizontal")
        horizontal["left"] = fuzz.trimf(
            horizontal.universe, [-1.833, -1, -0.1667])
        horizontal["mid"] = fuzz.trimf(
            horizontal.universe, [-0.8333, 0, 0.8333])
        horizontal["right"] = fuzz.trimf(
            horizontal.universe, [0.1667, 1, 1.833])

        vertical = ctrl.Consequent(np.arange(-1, 1, precision), "vertical")
        vertical["down"] = fuzz.trimf(
            vertical.universe, [-1.833, -1, -0.1667])
        vertical["mid"] = fuzz.trimf(vertical.universe, [-0.8333, 0, 0.8333])
        vertical["up"] = fuzz.trimf(vertical.universe, [0.1667, 1, 1.833])

        forward = ctrl.Consequent(np.arange(-1, 1, precision), "forward")
        forward["backward"] = fuzz.trimf(
            forward.universe, [-1.83, -1, -0.61662])
        forward["zero"] = fuzz.trimf(forward.universe, [-0.8333, 0, 0.8333])
        forward["forward"] = fuzz.trimf(
            forward.universe, [0.17206, 1.0054, 1.8384])

        regla1 = ctrl.Rule(antecedent=(mid["close"]), consequent=(
            vertical["up"], forward["zero"]))
        regla2 = ctrl.Rule(antecedent=(left["close"]), consequent=(
            horizontal["right"], forward["zero"]))
        regla3 = ctrl.Rule(antecedent=(right["close"]), consequent=(
            horizontal["left"], forward["zero"]))
        regla4 = ctrl.Rule(antecedent=(left["close"] & right["close"] & mid["close"]), consequent=(
            vertical["up"], forward["zero"]))
        regla5 = ctrl.Rule(antecedent=(left["far"] & right["far"] & mid["far"]), consequent=(
            horizontal["mid"], vertical["mid"], forward["forward"]))
        regla6 = ctrl.Rule(antecedent=(
            mid["far"]), consequent=(forward["forward"]))
        c_ctrl = ctrl.ControlSystem(
            [regla1, regla2, regla3, regla4, regla5, regla6])

        return ctrl.ControlSystemSimulation(c_ctrl)

    def _normalized(self, arr):
        return (arr-min(arr))/(max(arr)-min(arr))

    def calculate(self, l, m, r):
        self.control.input["left"] = l
        self.control.input["mid"] = m
        self.control.input["right"] = r
        try:
            self.control.compute()
            return self._normalized([self.control.output['horizontal'],
                                     self.control.output['forward'],
                                     self.control.output['vertical']])
        except ValueError as err:
            print("FUZZY ERROR: ", err)
            return [0, 0, 1]
