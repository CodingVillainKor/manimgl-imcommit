from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class equation(InteractiveScene, Scene2D):
    def construct(self):

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
        """
        **핵심: Flow matching 논문에서의 비교 figure**
        1. 약간 돌아가는 궤적을 그리는 diffusion
        2. 직선 궤적을 따라가는 flow matching
        3. 정말 그럴까?
        """
        ## Scene 1
        cfm_fig = ImageMobject("cfm_fig.png").scale(0.75)
        self.playw(FadeIn(cfm_fig))

        ## FadeOut cfm_fig

        nump_diff = RaenimPlane()
        nump_diff.x_axis.set_opacity(0.75)
        nump_diff.y_axis.set_opacity(0.75)
        nump_cfm = RaenimPlane()
        nump_cfm.x_axis.set_opacity(0.75)
        nump_cfm.y_axis.set_opacity(0.75)

        VGroup(nump_diff, nump_cfm).arrange(RIGHT, buff=0.75)

        start_diff_arr = np.array([1.5, 1.5])
        start_cfm_arr = np.array([1.5, 1.5])
        end_diff_arr = np.array([-1.5, -1.5])
        end_cfm_arr = np.array([-1.5, -1.5])

        start_diff_dot = Dot(nump_diff.c2p(*start_diff_arr), radius=0.05).set_color(RED)
        start_cfm_dot = Dot(nump_cfm.c2p(*start_cfm_arr), radius=0.05).set_color(RED)
        end_diff_dot = Dot(nump_diff.c2p(*end_diff_arr), radius=0.05).set_color(GREEN)
        end_cfm_dot = Dot(nump_cfm.c2p(*end_cfm_arr), radius=0.05).set_color(GREEN)

        self.play(FadeOut(cfm_fig), FadeIn(nump_diff), FadeIn(nump_cfm), run_time=0.5)
        diffusion_text = (
            Text("Diffusion", font_size=24, font="Noto Sans KR")
            .next_to(nump_diff, UP)
            .set_color(GREY_A)
        )
        start_diff_text = (
            Text("start", font_size=18, font="Noto Sans KR")
            .next_to(start_diff_dot, DOWN, buff=0.1)
            .set_color(RED)
        )
        end_diff_text = (
            Text("end", font_size=18, font="Noto Sans KR")
            .next_to(end_diff_dot, DOWN, buff=0.1)
            .set_color(GREEN)
        )
        self.playw(
            FadeIn(start_diff_dot),
            FadeIn(end_diff_dot),
            FadeIn(diffusion_text),
            FadeIn(start_diff_text),
            FadeIn(end_diff_text),
        )

        self.embed()
        ## Diffusion 궤적
        diff1_arr = np.array([0.3, 2.25])
        path = (
            BrokenLine(
                start_diff_dot.get_center(),
                nump_diff.c2p(*diff1_arr),
                end_diff_dot.get_center(),
                smooth=True,
            )
            .set_color_by_gradient(RED, GREEN)
            .set_stroke(width=2)
        )
        t_dot = Dot(path.point_from_proportion(0), radius=0.07).set_color(RED)
        value = ValueTracker(0)
        T = 1000
        t_text = (
            Text(f"t = {int(T-T*value.get_value())}", font_size=18, font="Noto Sans KR")
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(RED)
        )
        self.add(t_dot, t_text)
        t_dot.add_updater(
            lambda m: m.move_to(
                path.point_from_proportion(value.get_value() ** 0.001)
            ).set_color(interpolate_color(RED, GREEN, value.get_value()))
        )
        t_text.add_updater(
            lambda m: m.become(
                Text(
                    f"t = {int(T-T*value.get_value())}",
                    font_size=18,
                    font="Noto Sans KR",
                )
                .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
                .set_color(t_dot.get_color())
            )
        )
        self.playw(value.animate.set_value(1), ShowCreation(path), run_time=3)

        # diffusion_fig = ImageMobject("diffusion_paper.png").scale(0.75)
        # self.playw(FadeIn(diffusion_fig))
