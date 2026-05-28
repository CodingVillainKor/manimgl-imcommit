from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)

# 0과 1 사이의 무작위 숫자를 계속 더할 때, 그 합이 1을 넘기기 위해 필요한 숫자의 개수는 평균 몇 개일까요?


class intro(InteractiveScene, Scene2D):
    """
    ## Scene1: 직접 확인해보기
    1. uniform에서 숫자를 샘플링
    2. 합이 1을 넘을 때까지 샘플링
    3. 합이 1을 넘으면 멈추고 한 에피소드 추가
    4. 한 에피소드당 샘플링된 수 하나씩 쌓임
    5. 이 평균을 계속 계산해서 결과 근사
    """
    def construct(self):
        self.embed()
        
        ## intro
        nump = RaenimPlane(x_range=[-0.5, 1.5], y_range=[-0.5, 1.5], width=6, height=2)
        nump.y_axis.set_opacity(0)

        uniform_plot = nump.get_graph(lambda x: 1, x_range=[0, 1], color=RED).set_fill(opacity=0.3)
        self.playw(FadeIn(nump), FadeIn(uniform_plot))