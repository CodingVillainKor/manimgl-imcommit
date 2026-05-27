from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        model = Rectangle(
            width=4,
            height=2,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2,
        ).set_z_index(1)
        modelt = Text("Text to Image", font_size=32).set_z_index(1.5)

        model = VGroup(model, modelt).set_z_index(1)
        self.playw(FadeIn(model))
        text_input = (
            Text(
                '"한강 위를 걷는 닭, 월리를 찾아서 그림체로"',
                font="Noto Sans KR",
                font_size=24,
            )
            .next_to(model, DOWN, buff=0.3)
            .set_color(GREEN)
        )
        self.playw(FadeIn(text_input))
        self.playw(FadeOut(text_input, shift=UP, scale=0.5))
        gemini = ImageMobject("gemini.png").scale(0.75).next_to(model, UP, buff=0.5)
        self.playwl(
            FadeIn(gemini, shift=UP * 3, scale=3),
            self.cf.animate.shift(UP).scale(1.2),
            lag_ratio=0.3,
        )

        ## p_theta(x|c)
        eq = (
            Tex(
                "X \\sim p_\\theta(x|c)",
            )
            .scale(1.5)
            .next_to(model, RIGHT, buff=0.3)
        )
        self.playwl(
            FadeIn(eq, shift=RIGHT),
            FadeOut(gemini),
            self.cf.animate.move_to(VGroup(model, eq)).scale(1 / 1.2),
            lag_ratio=0.3,
        )
        # scale up eq
        self.play(FadeOut(model))
        self.playw(eq.animate.scale(2), self.cf.animate.move_to(eq))

        ## highlight
        surrounding_theta = SurroundingRectangle(
            eq[3], color=RED, buff=0.05, stroke_width=3
        )
        surrounding_x = SurroundingRectangle(
            eq[5], color=RED, buff=0.05, stroke_width=3
        )
        surrounding_c = SurroundingRectangle(
            eq[7], color=RED, buff=0.05, stroke_width=3
        )
        self.playw(
            FadeIn(surrounding_theta), FadeIn(surrounding_x), FadeIn(surrounding_c)
        )

        ## question
        question_theta = Text("???").set_color(RED)
        question_x = Text("???").set_color(RED)
        question_c = Text("???").set_color(RED)

        question_vgroup = (
            VGroup(question_theta, question_x, question_c)
            .arrange(RIGHT, buff=1.5)
            .next_to(VGroup(surrounding_theta, surrounding_x, surrounding_c), DOWN, buff=1.5)
        )
        question_x.shift(DOWN * 0.75)
        arrow_theta = Arrow(question_theta.get_top(), surrounding_theta.get_bottom(), buff=0.1).set_color(RED)
        arrow_x = Arrow(question_x.get_top(), surrounding_x.get_bottom(), buff=0.1).set_color(RED)
        arrow_c = Arrow(question_c.get_top(), surrounding_c.get_bottom(), buff=0.1).set_color(RED)
        
        self.play(FadeIn(question_theta), FadeIn(arrow_theta))
        self.play(FadeIn(question_x), FadeIn(arrow_x), self.cf.animate.move_to(VGroup(eq, question_vgroup)).scale(1.2))
        self.playw(FadeIn(question_c), FadeIn(arrow_c))

        self.embed()
        ## theta, x, c
        theta_text = Text("Model Parameters", font_size=36).set_color(GREEN).move_to(question_theta).align_to(question_theta, RIGHT)
        x_text = Text("Random Variables", font_size=36).set_color(GREEN).move_to(question_x)
        c_text = Text("Model Inputs", font_size=36).set_color(GREEN).move_to(question_c).align_to(question_c, LEFT)

        self.playw(
            FadeTransform(question_theta, theta_text),
            FadeTransform(question_x, x_text),
            FadeTransform(question_c, c_text),
            arrow_theta.animate.set_color(GREEN),
            arrow_x.animate.set_color(GREEN),
            arrow_c.animate.set_color(GREEN),
            surrounding_theta.animate.set_color(GREEN),
            surrounding_x.animate.set_color(GREEN),
            surrounding_c.animate.set_color(GREEN),
        )
