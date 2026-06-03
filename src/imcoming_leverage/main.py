from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):
        self.embed()

        ## intro
        money = SVGMobject("money.svg").scale(0.5)
        self.playw(FadeIn(money))