from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class equation(InteractiveScene, Scene2D):
    def construct(self):
        self.embed()

        ## Scene 2
        """
        ## Scene 2
        **핵심: 수식과 코드를 자세히 보자**
        1. Diffusion 수식
        2. Sampling하는 과정
        3. 코드도 같은지 확인
        """

class actually(InteractiveScene, Scene2D):
    def construct(self):
        self.embed()

        ## 
        """
        ## Scene 3
        **핵심: 실제의 모습, 그리고 Diffusion vs Flow matching 차이**
        1. 실제의 모습
        2. Diffusion: 목적지를 예측
        3. Flow matching: 목적지 방향을 예측
        """


class paperFigure(InteractiveScene, Scene2D):
    def construct(self):
        self.embed()

        """
        **핵심: Flow matching 논문에서의 비교 figure**
        1. 약간 돌아가는 궤적을 그리는 diffusion
        2. 직선 궤적을 따라가는 flow matching
        3. 정말 그럴까?
        """
        ## Scene 1
        cfm_fig = ImageMobject("cfm_fig.png").scale(0.75)
        self.playw(FadeIn(cfm_fig))
        
        nump_diff = RaenimPlane()
        nump_cfm = RaenimPlane()

        VGroup(nump_diff, nump_cfm).arrange(RIGHT, buff=1.5)

        start_diff_arr = np.array([1.5, 1.5, 0])
        start_cfm_arr = np.array([1.5, 1.5, 0])
        end_diff_arr = np.array([-1.5, -1.5, 0])
        end_cfm_arr = np.array([-1.5, -1.5, 0])
        
        start_diff_dot = Dot(start_diff_arr, color=RED)
        start_cfm_dot = Dot(start_cfm_arr, color=RED)
        end_diff_dot = Dot(end_diff_arr, color=GREEN)
        end_cfm_dot = Dot(end_cfm_arr, color=GREEN)
        


        # diffusion_fig = ImageMobject("diffusion_paper.png").scale(0.75)
        # self.playw(FadeIn(diffusion_fig))

