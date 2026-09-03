from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## ln box and vector sequence

        ln_box = Rectangle(width=8, height=4, color=WHITE)
        ln_text = Words("Layer Normalization", font_size=24).align(ln_box, UL, buff=0.1)
        ln = VGroup(ln_box, ln_text).shift(UP * 1)

        vecs = (
            VGroup(*[randn(5, 1).scale(0.4) for _ in range(5)])
            .arrange(RIGHT, buff=0.5)
            .next_to(ln, DOWN)
        )
        vec_vals = [vecs[i].val for i in range(len(vecs))]
        for vec in vecs:
            vec[2].become(Text("...", font_size=24).move_to(vec[2]))
        vecs.add(Text("...", font_size=24).next_to(vecs, RIGHT, buff=0.5))

        self.play(FadeIn(ln), FadeIn(vecs))
        self.play(FlashUnder(ln_text.words[0]))
        self.playw(FlashUnder(ln_text.words[1]), wait=4)
        self.playwl(vecs.animate.shift(UP * 2), FadeOut(ln, scale=3), lag_ratio=0.7)

        ## normalize
        means = [np.mean(vec_vals[i]) for i in range(len(vec_vals))]
        stds = [np.std(vec_vals[i]) for i in range(len(vec_vals))]
        normalized_vec_vals = [
            (vec_vals[i] - means[i]) / stds[i] for i in range(len(vec_vals))
        ]
        norm_vecs = VGroup(
            *[
                DecimalMatrix(normalized_vec_vals[i]).scale(0.4).move_to(vecs[i])
                for i in range(len(normalized_vec_vals))
            ]
        )

        lines = VGroup(
            *[
                DashedLine(
                    vecs[i].get_top(), vecs[i].get_bottom(), color=GREEN, stroke_width=6
                )
                for i in range(len(vecs) - 1)
            ]
        )

        self.play(*[Create(lines[i]) for i in range(len(lines))], run_time=0.5)

        ## mu and sigma
        mu = VGroup(
            *[
                Tex(r"\mu = %.2f" % means[i], font_size=32).next_to(vecs[i], DOWN)
                for i in range(len(means))
            ]
        ).set_color(GREEN)
        sigma = VGroup(
            *[
                Tex(r"\sigma = %.2f" % stds[i], font_size=32).next_to(vecs[i], DOWN)
                for i in range(len(stds))
            ]
        ).set_color(GREEN)
        musigs = VGroup(
            *[
                VGroup(mu[i], sigma[i]).arrange(DOWN, buff=0.1).next_to(vecs[i], UP)
                for i in range(len(means))
            ]
        )

        self.play(FadeIn(mu, shift=UP), FadeIn(sigma, shift=UP))

        self.playw(
            Transform(vecs[:-1], norm_vecs),
            *[FadeOut(line, scale=1.5) for line in lines],
            *[FadeOut(musig, scale=0.5, shift=DOWN) for musig in musigs],
        )

        ## learnable parameter affine
        gamma = Tex(r"\cdot \gamma", font_size=32)
        beta = Tex(r"+ \beta", font_size=32)
        gb_box = SurroundingRectangle(
            VGroup(gamma, beta).arrange(RIGHT), color=RED_B, buff=0.2
        )
        gb = VGroup(gb_box, gamma, beta).next_to(vecs[:-1], UP, buff=0.5)
        lines = VGroup(
            *[
                DashedLine(gb_box, vecs[i].get_top(), color=RED_B)
                for i in range(len(vecs) - 1)
            ]
        )

        self.play(*[Create(line) for line in lines], FadeIn(gb))


class stableLearning(InteractiveScene, Scene2D):
    def construct(self):
        ## 5 layers

        def get_layer(i):
            layer_box = Rectangle(width=1.5, height=4, color=WHITE)
            if i == 3:
                i = "..."
            layer_text = Words(f"Layer {i}", font_size=24).align(
                layer_box, UL, buff=0.1
            )
            return VGroup(layer_box, layer_text)

        layers = (
            VGroup(*[get_layer(i) for i in range(1, 6)])
            .arrange(RIGHT, buff=0.5)
            .shift(UP * 0.5)
        )
        lines = VGroup(
            *[
                Line(layers[i].get_right(), layers[i + 1].get_left(), color=WHITE)
                for i in range(len(layers) - 1)
            ]
        )

        self.playwl(FadeIn(layers), Create(lines), lag_ratio=0.7)

        ## gradients be equally distributed
        gradients = VGroup(
            *[
                Tex(r"\nabla W_{", f"{i}", "}", font_size=32)
                .set_color(RED_B)
                .move_to(layers[i - 1])
                .scale(random.random() * 0.5 - 0.25 + 1)
                for i in range(1, 6)
            ]
        )
        self.playw(FadeIn(gradients), wait=3)

        ## not good if gradients are not equally distributed
        gradients2 = VGroup(
            *[
                Tex(r"\nabla W_{", f"{i}", "}", font_size=32)
                .set_color(PURE_RED)
                .move_to(layers[i - 1])
                .scale(random.random() * 1.8 - 0.9 + 1)
                for i in range(1, 6)
            ]
        )
        self.playw(Transform(gradients, gradients2))


class ffnGradient(InteractiveScene, Scene2D):
    def construct(self):

        ## mid line
        mid_line = DashedLine(UP * 7, DOWN * 7, color=GREY_D, stroke_width=2)
        self.addw(mid_line)
        OL = LEFT * 7.11111111 / 2
        OR = RIGHT * 7.11111111 / 2


        ## ffn box
        def get_ffn():
            ffn_box = Rectangle(width=3.5, height=1.5, color=GREY_C)
            ffn_text = (
                Words("FFN", font_size=24)
                .align(ffn_box, UL, buff=0.1)
                .set_color(GREY_B)
            )
            return VGroup(ffn_box, ffn_text)

        ffn_preln = get_ffn().move_to(OL)
        ffn_postln = get_ffn().move_to(OR)
        pre_line_preln = Line(
            ffn_preln.get_bottom() + DOWN * 0.2,
            ffn_preln.get_bottom(),
            stroke_width=2,
            color=GREY_C,
        )
        dot3_preln = (
            Text("...", font_size=20)
            .rotate(PI / 2)
            .next_to(pre_line_preln, DOWN, buff=0.05)
            .set_color(GREY_C)
        )
        pre_line_postln = Line(
            ffn_postln.get_bottom() + DOWN * 0.2,
            ffn_postln.get_bottom(),
            stroke_width=2,
            color=GREY_C,
        )
        dot3_postln = (
            Text("...", font_size=20)
            .rotate(PI / 2)
            .next_to(pre_line_postln, DOWN, buff=0.05)
            .set_color(GREY_C)
        )
        pre_lines_preln = VGroup(pre_line_preln, dot3_preln)
        pre_lines_postln = VGroup(pre_line_postln, dot3_postln)

        self.playw(
            FadeIn(ffn_preln),
            FadeIn(ffn_postln),
            FadeIn(pre_lines_preln),
            FadeIn(pre_lines_postln),
            wait=2,
        )

        ## gradients
        dLdo_preln = (
            Tex(r"\frac{\partial L}{\partial o}", font_size=32)
            .set_color(RED_B)
            .next_to(ffn_preln, UP, buff=0.2)
        )
        dLdo_postln = (
            Tex(r"\frac{\partial L}{\partial o}", font_size=32)
            .set_color(RED_B)
            .next_to(ffn_postln, UP, buff=0.2)
        )
        self.playw(
            FadeIn(dLdo_preln, shift=DOWN),
            FadeIn(dLdo_postln, shift=DOWN),
            run_time=1.5,
            rate_func=linear,
        )

        ## chain rule
        chain_rule = Tex(
            r"\frac{\partial L}{\partial W_{\text{ffn}}}",
            "=",
            r"\frac{\partial L}{\partial o}",
            r"\cdot",
            r"\frac{\partial o}{\partial W}",
            font_size=32,
        ).add_background_rectangle(BLACK, buff=0.1).shift(UP*2.5)
        self.playw(FadeIn(chain_rule))

        ## gradient1: dLdo
        self.play(Circumscribe(chain_rule[10:15]), chain_rule[10:15].animate.set_color(RED_B))

        ## gradient2: dodW
        self.play(Circumscribe(chain_rule[16:]), chain_rule[16:].animate.set_color(GREEN))

        x_preln = Tex(r"x_{\text{ffn}}", font_size=32).set_color(GREEN).move_to(ffn_preln)
        x_postln = Tex(r"x_{\text{ffn}}", font_size=32).set_color(GREEN).move_to(ffn_postln)
        self.playw(
            FadeIn(x_preln, shift=UP*0.5),
            FadeIn(x_postln, shift=UP*0.5),
            rate_func=linear,
        )

        ## key point: dLdo
        self.playw(
            Circumscribe(dLdo_preln, color=RED_B),
            Circumscribe(dLdo_postln, color=RED_B),
            run_time=1.5,
            wait=3
        )

        self.embed()
        ## dLdo from LayerNorm: Big O notation O(1/||x||_2)
        dLdo_ln_preln = (   
            Tex("=", r"O(\frac{1}{\Vert x\Vert_2})", font_size=32)
            .set_color(RED_B)
            .next_to(dLdo_preln, RIGHT, buff=0.2)
        )
        dLdo_ln_postln = (
            Tex("=", r"O(\frac{1}{\Vert x\Vert_2})", font_size=32)
            .set_color(RED_B)
            .next_to(dLdo_postln, RIGHT, buff=0.2)
        )
        self.playw(
            FadeIn(dLdo_ln_preln, shift=RIGHT*0.3),
            FadeIn(dLdo_ln_postln, shift=RIGHT*0.3),
        )