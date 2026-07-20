from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class autoregressiveVsdLLM2(InteractiveScene, Scene2D):
    def construct(self):
        ## intro
        line = DashedLine(UP * 5, DOWN * 5, color=GREY_D)
        LO = LEFT * 7.11111111 / 2
        RO = RIGHT * 7.11111111 / 2
        ar_title = (
            Text("Autoregressive", font_size=28).set_color(RED_B).move_to(LO + UP * 2.5)
        )
        dllm_title = Text("dLLM", font_size=28).set_color(BLUE_B).move_to(RO + UP * 2.5)
        self.addw(line, ar_title, dllm_title)

        ## ar model
        model_ar = (
            Rectangle(width=4.5, height=1.5, color=RED_A, fill_opacity=0.5)
            .move_to(LO)
            .shift(DOWN * 1.25)
            .set_z_index(1)
        )
        modelt_ar = (
            Text("Transformer", font_size=24)
            .move_to(model_ar.get_center())
            .set_z_index(2)
        )

        self.playw(FadeIn(model_ar), Write(modelt_ar))

        def token(text: str, color=YELLOW_A):
            t = Text(text, font_size=22).set_color(color)
            sr = SurroundingRectangle(t, buff=0.1).set_color(color)
            return VGroup(t, sr)

        ## ar output

        t1 = (
            Text("...", font_size=24)
            .next_to(model_ar, UP, buff=0.5)
            .align_to(model_ar, LEFT)
            .shift(LEFT * 0.5)
        )
        t2 = token("A인").next_to(t1, RIGHT, buff=0.2)
        t3 = token("것").next_to(t2, RIGHT, buff=0.2)
        t4 = token("같습니다").next_to(t3, RIGHT, buff=0.2)
        t5a = token("하지만", color=PURE_RED).next_to(t4, RIGHT, buff=0.2)
        t5b = token("그리고", color=PURE_RED).next_to(t5a, UP, buff=0.1)
        t5c = token("그래서", color=PURE_RED).next_to(t5b, UP, buff=0.1)
        t6a = token("B가").next_to(t5a, RIGHT, buff=0.2)
        t6b = token("확신합니다").next_to(t5b, RIGHT, buff=0.2)
        t6c = token("한번").next_to(t5c, RIGHT, buff=0.2)

        self.play(FadeIn(t1), run_time=0.5)
        self.play(FadeIn(t2, shift=t2.get_center() - model_ar.get_center(), scale=2))
        self.play(
            FadeIn(t3, shift=t2.get_center() - model_ar.get_center(), scale=2),
            run_time=0.5,
        )
        self.playw(
            FadeIn(t4, shift=t2.get_center() - model_ar.get_center(), scale=2),
            run_time=0.5,
        )

        ## ar output exploration

        self.playwl(
            FadeIn(t5c, shift=t5c.get_center() - t4.get_center(), scale=2),
            FadeIn(t5b, shift=t5b.get_center() - t4.get_center(), scale=2),
            FadeIn(t5a, shift=t5a.get_center() - t4.get_center(), scale=2),
            lag_ratio=0.5,
        )

        self.play(FadeIn(t6c, shift=RIGHT * 0.5), run_time=0.5)
        self.play(FadeIn(t6b, shift=RIGHT * 0.5), run_time=0.5)
        self.playw(FadeIn(t6a, shift=RIGHT * 0.5), run_time=0.5)

        ## dLLM model

        model_dllm = (
            Rectangle(width=4.5, height=1.5, color=BLUE_A, fill_opacity=0.5)
            .move_to(RO)
            .shift(DOWN * 1.25)
            .set_z_index(1)
        )
        modelt_dllm = (
            Text("Transformer", font_size=24)
            .move_to(model_dllm.get_center())
            .set_z_index(2)
        )

        self.playw(FadeIn(model_dllm), Write(modelt_dllm), run_time=0.5)

        ## dLLM output

        t1 = (
            Text("...", font_size=24)
            .next_to(model_dllm, UP, buff=0.5)
            .align_to(model_dllm, LEFT)
            .shift(LEFT * 0.5)
        )

        t2 = token("A인").next_to(t1, RIGHT, buff=0.2)
        t3 = token("것").next_to(t2, RIGHT, buff=0.2)
        t4 = token("같습니다").next_to(t3, RIGHT, buff=0.2)
        t5 = token("하지만", color=PURE_RED).next_to(t4, RIGHT, buff=0.2)
        t6 = token("B가").next_to(t5, RIGHT, buff=0.2)
        t7 = token("맞습니다").next_to(t6, RIGHT, buff=0.2)

        random_order = [t1, t7, t3, t6, t2, t4, t5]

        self.playwl(
            *[
                FadeIn(
                    t,
                    shift=t.get_center() - model_dllm.get_center(),
                    scale=2,
                )
                for t in random_order[:-1]
            ],
            lag_ratio=0.5,
        )
        t5[0].set_opacity(0)
        self.playw(
            FadeIn(
                random_order[-1],
                shift=random_order[-1].get_center() - model_dllm.get_center(),
                scale=2,
            ),
            run_time=0.5,
        )

        self.playw(t5[0].animate.set_opacity(1))

class paperIdea(InteractiveScene, Scene2D):
    def construct(self):

        ## dLLM model

        model_dllm = (
            Rectangle(width=4.5, height=1.5, color=BLUE_A, fill_opacity=0.5)
            .move_to(ORIGIN)
            .shift(DOWN * 1.25)
            .set_z_index(1)
        )
        modelt_dllm = (
            Text("Transformer", font_size=24)
            .move_to(model_dllm.get_center())
            .set_z_index(2)
        )

        self.playw(FadeIn(model_dllm), FadeIn(modelt_dllm), run_time=0.5)

        ## dLLM output
        def token(text: str, color=YELLOW_A):
            t = Text(text, font_size=22).set_color(color)
            sr = SurroundingRectangle(t, buff=0.1).set_color(color)
            return VGroup(t, sr)

        t1 = (
            Text("...", font_size=24)
            .next_to(model_dllm, UP, buff=0.75)
            .align_to(model_dllm, LEFT)
            .shift(LEFT * 0.5)
        )
        t2 = token("A인").next_to(t1, RIGHT, buff=0.2)
        t3 = token("것").next_to(t2, RIGHT, buff=0.2)
        t4 = token("같습니다").next_to(t3, RIGHT, buff=0.2)
        t5 = token("하지만").next_to(t4, RIGHT, buff=0.2)
        t6 = token("B가").next_to(t5, RIGHT, buff=0.2)
        t7 = token("맞습니다").next_to(t6, RIGHT, buff=0.2)
        t8 = Text("...", font_size=24).next_to(t7, RIGHT, buff=0.2)

        ar_order = [t1, t2, t3, t4, t5, t6, t7, t8]

        self.playwl(
            *[
                FadeIn(
                    t,
                    shift=t.get_center() - model_dllm.get_center(),
                    scale=2,
                )
                for t in ar_order
            ],
            lag_ratio=0.5,
        )

        self.wait(2)

        ## train, inference

        line = DashedLine(UP * 5, DOWN * 5, color=GREY_D)
        LO = LEFT * 7.11111111 / 2
        RO = RIGHT * 7.11111111 / 2

        train_title = (
            Text("Training", font_size=28).set_color(RED_B).move_to(LO + UP * 2.5)
        )

        inference_title = (
            Text("Inference", font_size=28).set_color(BLUE_B).move_to(RO + UP * 2.5)
        )
        lefts = VGroup(model_dllm, modelt_dllm, *ar_order)
        self.playwl(FadeIn(line), FadeIn(train_title), FadeIn(inference_title), lefts.animate.shift(LEFT * 4))

        ## inference

        model_inf = VGroup(model_dllm, modelt_dllm).copy()

        self.playw(model_inf.animate.move_to(RO).shift(DOWN * 1.25))

        ## inference output

        t1 = (
            Text("...", font_size=24)
            .next_to(model_inf, UP, buff=0.75)
            .align_to(model_inf, LEFT)
            .shift(LEFT)
        )
        t2 = token("답은").next_to(t1, RIGHT, buff=0.2)
        t3 = token("A").next_to(t2, RIGHT, buff=0.2)
        t4 = token("같습니다").next_to(t3, RIGHT, buff=0.2)
        t5 = token("하지만").next_to(t4, RIGHT, buff=0.2)
        t6 = token("바로").next_to(t5, RIGHT, buff=0.2)
        t7 = token("B입니다").next_to(t6, RIGHT, buff=0.2)
        t8 = Text("...", font_size=24).next_to(t7, RIGHT, buff=0.2)

        dllm_order = [t1, t6, t2, t4, t3, t7, t5, t8]

        self.playwl(
            *[
                FadeIn(
                    t,
                    shift=t.get_center() - model_inf.get_center(),
                    scale=2,
                )
                for t in dllm_order
            ],
            lag_ratio=0.5,
        )

        ## indicate training

        self.playw(*[Indicate(item, scale_factor=1.1) for item in lefts])

class ideaDeepDive(InteractiveScene, Scene2D):
    def construct(self):
        ## dLLM model

        model_dllm = (
            Rectangle(width=5.5, height=1.75, color=BLUE_A, fill_opacity=0.7)
            .move_to(ORIGIN)
            .shift(DOWN * 1.25)
            .set_z_index(1)
        )
        modelt_dllm = (
            Text("Transformer", font_size=24)
            .move_to(model_dllm.get_center())
            .set_z_index(2)
        )

        infer_title = (
            Text("Inference", font_size=28).set_color(RED_B).shift(UP * 2.5)
        )
        self.addw(model_dllm, modelt_dllm, infer_title)


        ## latent in the model

        t1 = (
            Text("...", font_size=24)
            .next_to(model_dllm, UP, buff=0.75)
            .align_to(model_dllm, LEFT)
        )
        t2 = Text("A인", font_size=22).set_color(YELLOW_A).next_to(t1, RIGHT, buff=0.2)
        t3 = Text("것", font_size=22).set_color(YELLOW_A).next_to(t2, RIGHT, buff=0.2)
        t4 = Text("같습니다", font_size=22).set_color(YELLOW_A).next_to(t3, RIGHT, buff=0.2)
        t5 = Text("하지만", font_size=22).set_color(YELLOW_A).next_to(t4, RIGHT, buff=0.2)
        t6 = Text("B가", font_size=22).set_color(YELLOW_A).next_to(t5, RIGHT, buff=0.2)
        t7 = Text("맞습니다", font_size=22).set_color(YELLOW_A).next_to(t6, RIGHT, buff=0.2)
        t8 = Text("...", font_size=24).next_to(t7, RIGHT, buff=0.2)

        latent = Tensor(8, arrange=RIGHT, buff=0.25).move_to(model_dllm.get_center() + UP * 0.5).set_z_index(0)

        dllm_order = [[t1], [t3, t7], [t2, t6], [t4, t5], [t8]]
        self.add(model_dllm)
        self.add(latent)
        self.playw(FadeIn(latent))
        dependencies = VGroup()
        for i, ts in enumerate(dllm_order):
            self.play(*[FadeIn(t, shift=t.get_center() - model_dllm.get_center(), scale=2) for t in ts], run_time=0.5)
            lines = VGroup(*[VGroup(*[DashedLine(latent[j].get_top(), t.get_bottom(), color=GREY_C) for j in range(8)]) for t in ts])
            dependencies.add(lines)
            if i == 0:
                self.playw(FadeIn(lines))
            else:
                self.play(FadeIn(lines), run_time=0.5)

        self.wait(2)

        ## train, inference
        rights = VGroup(latent, model_dllm, modelt_dllm, t1, t2, t3, t4, t5, t6, t7, t8, dependencies)

        line = DashedLine(UP * 5, DOWN * 5, color=GREY_D)
        LO = LEFT * 7.11111111 / 2
        RO = RIGHT * 7.11111111 / 2

        self.playw(rights.animate.shift(RIGHT * 3.5), infer_title.animate.move_to(RO + UP * 2.5), FadeIn(line))

        self.embed()
        ## training

        model_train = (
            Rectangle(width=5.5, height=1.75, color=BLUE_A, fill_opacity=0.7)
            .move_to(LO + DOWN * 1.25)
            .set_z_index(1)
        )
        modelt_train = (
            Text("Transformer", font_size=24)
            .move_to(model_train.get_center())
            .set_z_index(2)
        )

        train_title = (
            Text("Training", font_size=28).set_color(RED_B).move_to(LO + UP * 2.5)
        )
        latent_ar = Tensor(8, arrange=RIGHT, buff=0.25).move_to(model_train.get_center() + UP * 0.5).set_z_index(0)
        self.playw(FadeIn(model_train), FadeIn(modelt_train), FadeIn(latent_ar), FadeIn(train_title))

        l1 = Text("...", font_size=24).next_to(model_train, UP, buff=0.75).align_to(model_train, LEFT)
        l2 = Text("A인", font_size=22).set_color(YELLOW_A).next_to(l1, RIGHT, buff=0.2)
        l3 = Text("것", font_size=22).set_color(YELLOW_A).next_to(l2, RIGHT, buff=0.2)
        l4 = Text("같습니다", font_size=22).set_color(YELLOW_A).next_to(l3, RIGHT, buff=0.2)
        l5 = Text("하지만", font_size=22).set_color(YELLOW_A).next_to(l4, RIGHT, buff=0.2)
        l6 = Text("B가", font_size=22).set_color(YELLOW_A).next_to(l5, RIGHT, buff=0.2)
        l7 = Text("맞습니다", font_size=22).set_color(YELLOW_A).next_to(l6, RIGHT, buff=0.2)
        l8 = Text("...", font_size=24).next_to(l7, RIGHT, buff=0.2)

        ar_order = [l1, l2, l3, l4, l5, l6, l7, l8]

        dependencies_ar = VGroup()

        for i, t in enumerate(ar_order):
            # self.play(FadeIn(t, shift=t.get_center() - model_train.get_center(), scale=2), run_time=0.5)
            self.play(Transformr(latent_ar.copy(), t), run_time=0.5)
            lines = VGroup(*[DashedLine(latent_ar[j].get_top(), t.get_bottom(), color=GREY_C) for j in range(8)])
            dependencies_ar.add(lines)
            self.play(FadeIn(lines), run_time=0.5)
        self.wait()
