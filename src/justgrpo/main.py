from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class autoregressiveVsdLLM(InteractiveScene, Scene2D):
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

        ## ar once

        model_ar = (
            Rectangle(width=4.5, height=1.5, color=RED_A, fill_opacity=0.5)
            .move_to(LO)
            .set_z_index(1)
        )
        modelt_ar = (
            Text("Transformer", font_size=24)
            .move_to(model_ar.get_center())
            .set_z_index(2)
        )
        self.playw(FadeIn(model_ar), Write(modelt_ar))

        ar_input = (
            Tensor(4, arrange=RIGHT, buff=0.2)
            .scale(0.7)
            .next_to(model_ar, DOWN, buff=0.35)
            .align(model_ar, LEFT, buff=0.1)
        )
        self.playw(FadeIn(ar_input))

        ar_output = (
            Tensor(4, arrange=RIGHT, buff=0.2)
            .scale(0.7)
            .next_to(model_ar, UP, buff=0.35)
            .align(model_ar, LEFT, buff=0.1)
        )
        self.playw(Transformr(ar_input.copy(), ar_output))

        ## ar loop

        out = ar_output[-1].copy()
        self.add(out)
        self.playw(FadeOut(ar_output), run_time=0.5)
        p1 = out.copy().set_opacity(0).next_to(model_ar, RIGHT).align_to(out, UP)
        p2 = out.copy().set_opacity(0).next_to(model_ar, RIGHT).align_to(ar_input, DOWN)
        p3 = out.copy().set_opacity(0).next_to(ar_input, RIGHT, buff=0.14)
        path = BrokenLine(
            out.get_center(), p1.get_center(), p2.get_center(), p3.get_center()
        )
        self.playw(MoveAlongPath(out, path), run_time=1.5)
        ar_input.add(out)
        ar_output = (
            Tensor(len(ar_input), arrange=RIGHT, buff=0.2)
            .scale(0.7)
            .next_to(model_ar, UP, buff=0.35)
            .align(model_ar, LEFT, buff=0.1)
        )
        self.play(Transformr(ar_input.copy(), ar_output), run_time=0.5)

        # loop

        for i in range(5):
            out = ar_output[-1].copy()
            self.add(out)
            self.play(FadeOut(ar_output), run_time=0.3)
            p1 = out.copy().set_opacity(0).next_to(model_ar, RIGHT).align_to(out, UP)
            p2 = (
                out.copy()
                .set_opacity(0)
                .next_to(model_ar, RIGHT)
                .align_to(ar_input, DOWN)
            )
            p3 = out.copy().set_opacity(0).next_to(ar_input, RIGHT, buff=0.14)
            path = BrokenLine(
                out.get_center(), p1.get_center(), p2.get_center(), p3.get_center()
            )
            self.play(MoveAlongPath(out, path), run_time=0.6)
            ar_input.add(out)
            ar_output = (
                Tensor(len(ar_input), arrange=RIGHT, buff=0.2)
                .scale(0.7)
                .next_to(model_ar, UP, buff=0.35)
                .align(model_ar, LEFT, buff=0.1)
            )
            self.play(Transformr(ar_input.copy(), ar_output), run_time=0.3)
        self.wait(2)

        ## dLLM once

        turns = [[6, 9], [4, 8], [5, 7]]

        model_dllm = (
            Rectangle(width=4.5, height=1.5, color=BLUE_A, fill_opacity=0.5)
            .move_to(RO)
            .set_z_index(1)
        )
        modelt_dllm = (
            Text("Transformer", font_size=24)
            .move_to(model_dllm.get_center())
            .set_z_index(2)
        )
        self.playw(FadeIn(model_dllm), Write(modelt_dllm))

        dllm_input = (
            Tensor(10, arrange=RIGHT, buff=0.2)
            .scale(0.7)
            .next_to(model_dllm, DOWN, buff=0.35)
            .align(model_dllm, LEFT, buff=0.1)
        )
        dllm_input[4:].set_fill(opacity=0)
        self.playw(FadeIn(dllm_input))

        dllm_output = (
            Tensor(10, arrange=RIGHT, buff=0.2)
            .scale(0.7)
            .next_to(model_dllm, UP, buff=0.35)
            .align(model_dllm, LEFT, buff=0.1)
        )
        self.playw(Transformr(dllm_input.copy(), dllm_output))

        ## dLLM loop

        out = VGroup(*[dllm_output[i] for i in turns[0]]).copy()
        self.add(out)
        self.playw(FadeOut(dllm_output), run_time=0.5)

        p1 = (
            out[0].copy().set_opacity(0).next_to(model_dllm, RIGHT).align_to(out[0], UP)
        )
        p2 = (
            out[0]
            .copy()
            .set_opacity(0)
            .next_to(model_dllm, RIGHT)
            .align_to(dllm_input[turns[0][0]], DOWN)
        )
        p31 = out[0].copy().set_opacity(0).move_to(dllm_input[turns[0][0]])
        p32 = out[0].copy().set_opacity(0).move_to(dllm_input[turns[0][1]])

        path1 = BrokenLine(
            out[0].get_center(), p1.get_center(), p2.get_center(), p31.get_center()
        )
        path2 = BrokenLine(
            out[1].get_center(), p1.get_center(), p2.get_center(), p32.get_center()
        )
        self.playwl(
            MoveAlongPath(out[1], path2),
            MoveAlongPath(out[0], path1),
            run_time=1.5,
            lag_ratio=0.5,
        )
        dllm_input[turns[0][0]].become(out[0])
        dllm_input[turns[0][1]].become(out[1])
        dllm_output = (
            Tensor(len(dllm_input), arrange=RIGHT, buff=0.2)
            .scale(0.7)
            .next_to(model_dllm, UP, buff=0.35)
            .align(model_dllm, LEFT, buff=0.1)
        )
        self.play(Transformr(dllm_input.copy(), dllm_output), run_time=0.5)

        # loop

        for i in range(1, 3):
            out = VGroup(*[dllm_output[j] for j in turns[i]]).copy()
            self.add(out)
            self.play(FadeOut(dllm_output), run_time=0.3)

            p1 = (
                out[0]
                .copy()
                .set_opacity(0)
                .next_to(model_dllm, RIGHT)
                .align_to(out[0], UP)
            )
            p2 = (
                out[0]
                .copy()
                .set_opacity(0)
                .next_to(model_dllm, RIGHT)
                .align_to(dllm_input[turns[i][0]], DOWN)
            )
            p31 = out[0].copy().set_opacity(0).move_to(dllm_input[turns[i][0]])
            p32 = out[0].copy().set_opacity(0).move_to(dllm_input[turns[i][1]])

            path1 = BrokenLine(
                out[0].get_center(), p1.get_center(), p2.get_center(), p31.get_center()
            )
            path2 = BrokenLine(
                out[1].get_center(), p1.get_center(), p2.get_center(), p32.get_center()
            )
            self.playwl(
                MoveAlongPath(out[1], path2),
                MoveAlongPath(out[0], path1),
                run_time=0.6,
                lag_ratio=0.5,
                wait=0,
            )
            dllm_input[turns[i][0]].become(out[0])
            dllm_input[turns[i][1]].become(out[1])
            dllm_output = (
                Tensor(len(dllm_input), arrange=RIGHT, buff=0.2)
                .scale(0.7)
                .next_to(model_dllm, UP, buff=0.35)
                .align(model_dllm, LEFT, buff=0.1)
            )
            if i == 2:
                break
            self.play(Transformr(dllm_input.copy(), dllm_output), run_time=0.3)


class passAtK(InteractiveScene, Scene2D):
    def construct(self):

        def get_checkmark():
            checkmark = Text("✓", font_size=24).set_color(GREEN_B)
            return checkmark

        def get_cross():
            cross = Text(X_STRING, font_size=24, font="Sans Not-Rotated 24").set_color(
                RED_B
            )
            return cross

        ## model

        model = Rectangle(
            width=4.5, height=1.5, color=BLUE_A, fill_opacity=0.5
        ).set_z_index(1)
        modelt = (
            Text("Transformer", font_size=24).move_to(model.get_center()).set_z_index(2)
        )

        answer1 = Words("The answer is ABC...", font_size=24)
        answer1.words[3:].set_color(random_color())
        answer2 = Words("The answer is blahblah...", font_size=24)
        answer2.words[3:].set_color(random_color())
        answer3 = Words("The answer is 42, because ...", font_size=24)
        answer3.words[3:].set_color(PURE_GREEN)
        answer4 = Words("The answer is very difficult to ...", font_size=24)
        answer4.words[3:].set_color(random_color())

        answers = (
            VGroup(answer1, answer2, answer3, answer4)
            .arrange(UP, aligned_edge=LEFT, buff=0.15)
            .next_to(model, UP, buff=0.35)
        )
        self.playw(FadeIn(model), Write(modelt))

        self.playw(
            FadeIn(answer4, shift=answer4.get_center() - model.get_center(), scale=2)
        )
        self.play(
            FadeIn(answer3, shift=answer3.get_center() - model.get_center(), scale=2),
            run_time=0.5,
        )
        self.play(
            FadeIn(answer2, shift=answer2.get_center() - model.get_center(), scale=2),
            run_time=0.5,
        )
        self.playw(
            FadeIn(answer1, shift=answer1.get_center() - model.get_center(), scale=2),
            run_time=0.5,
        )

        ## xxcx
        e1 = get_cross().next_to(answer1, RIGHT, buff=0.1)
        e2 = get_cross().next_to(answer2, RIGHT, buff=0.1)
        e3 = get_checkmark().next_to(answer3, RIGHT, buff=0.1)
        e4 = get_cross().next_to(answer4, RIGHT, buff=0.1)

        es = VGroup(e1, e2, e3, e4)
        self.playw(FadeIn(es))

        ## camera

        self.playw(
            self.cf.animate.reorient(
                0, 62, 0, (np.float32(0.27), np.float32(0.81), np.float32(1.57)), 9.13
            ),
            answers.animate.rotate(62 * DEGREES, axis=RIGHT).shift(UP * 1.3),
            es.animate.rotate(62 * DEGREES, axis=RIGHT).shift(UP * 1.3),
            run_time=2,
        )

        ## answers2, answers3, ...

        answers2 = (
            VGroup(
                Words("I don't know, ...", font_size=24),
                Words("The answer is 16, because ...", font_size=24),
                Words("The answer is ...", font_size=24),
                Words("Interesting questions...", font_size=24),
            )
            .arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            .next_to(answers, LEFT, buff=1)
            .rotate(62 * DEGREES, axis=RIGHT)
        )
        for a2 in answers2:
            a2.words[3:].set_color(random_color())
        e21 = (
            get_cross()
            .next_to(answers2[0], RIGHT, buff=0.1)
            .rotate(62 * DEGREES, axis=RIGHT)
        )
        e22 = (
            get_cross()
            .next_to(answers2[1], RIGHT, buff=0.1)
            .rotate(62 * DEGREES, axis=RIGHT)
        )
        e23 = (
            get_cross()
            .next_to(answers2[2], RIGHT, buff=0.1)
            .rotate(62 * DEGREES, axis=RIGHT)
        )
        e24 = (
            get_cross()
            .next_to(answers2[3], RIGHT, buff=0.1)
            .rotate(62 * DEGREES, axis=RIGHT)
        )
        es2 = VGroup(e21, e22, e23, e24)

        answers3 = (
            VGroup(
                Words("The answer is 42, because ...", font_size=24),
                Words("The answer is ...", font_size=24),
                Words("I don't know, ...", font_size=24),
                Words("Interesting questions...", font_size=24),
            )
            .arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            .next_to(answers, RIGHT, buff=1)
            .rotate(62 * DEGREES, axis=RIGHT)
        )
        for a3 in answers3:
            a3.words[3:].set_color(random_color())
        answers3[0].words[3:].set_color(PURE_GREEN)
        e31 = (
            get_checkmark()
            .next_to(answers3[0], RIGHT, buff=0.1)
            .rotate(62 * DEGREES, axis=RIGHT)
        )
        e32 = (
            get_cross()
            .next_to(answers3[1], RIGHT, buff=0.1)
            .rotate(62 * DEGREES, axis=RIGHT)
        )
        e33 = (
            get_cross()
            .next_to(answers3[2], RIGHT, buff=0.1)
            .rotate(62 * DEGREES, axis=RIGHT)
        )
        e34 = (
            get_cross()
            .next_to(answers3[3], RIGHT, buff=0.1)
            .rotate(62 * DEGREES, axis=RIGHT)
        )
        es3 = VGroup(e31, e32, e33, e34)

        self.playw(FadeIn(answers2), FadeIn(answers3), FadeIn(es2), FadeIn(es3))

        c1 = (
            SurroundingRectangle(
                VGroup(answers, es).copy().rotate(-62 * DEGREES, axis=RIGHT), buff=0.3
            )
            .rotate(62 * DEGREES, axis=RIGHT)
            .set_stroke(PURE_GREEN)
        )
        c2 = (
            SurroundingRectangle(
                VGroup(answers2, es2).copy().rotate(-62 * DEGREES, axis=RIGHT), buff=0.3
            )
            .rotate(62 * DEGREES, axis=RIGHT)
            .set_stroke(PURE_RED)
        )
        c3 = (
            SurroundingRectangle(
                VGroup(answers3, es3).copy().rotate(-62 * DEGREES, axis=RIGHT), buff=0.3
            )
            .rotate(62 * DEGREES, axis=RIGHT)
            .set_stroke(PURE_GREEN)
        )

        self.playw(FadeIn(c1), FadeIn(c2), FadeIn(c3))

        ## pass@k

        text = (
            Text("Pass@k = 2/3 = 0.6667", font_size=32)
            .rotate(62 * DEGREES, axis=RIGHT)
            .set_color(GREEN_A)
            .next_to(c1, UP + OUT, buff=0.5)
        )
        self.playw(FadeIn(text))


class pathARvsdLLM(InteractiveScene, Scene2D):
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

        ## dLLM model

        model_dllm = (
            Rectangle(width=4.5, height=1.5, color=BLUE_A, fill_opacity=0.5)
            .move_to(RO)
            .shift(DOWN)
            .set_z_index(1)
        )
        modelt_dllm = (
            Text("Transformer", font_size=24)
            .move_to(model_dllm.get_center())
            .set_z_index(2)
        )

        orders_dllm_list = ["<0>", "<1>", "<2>", "<3>", "<4>", "<5>", "<6>", "<7>"]
        orders_dllm = (
            VGroup(
                *[
                    Text(o, font_size=20, font=MONO_FONT).set_color(GREY_A)
                    for o in orders_dllm_list
                ]
            )
            .arrange(RIGHT, buff=0.2)
            .next_to(model_dllm, UP, buff=0.5)
        )
        self.playw(
            FadeIn(orders_dllm), FadeIn(model_dllm), Write(modelt_dllm), run_time=0.5
        )

        dllm_order = [5, 2, 6, 1, 3, 4, 0, 7]

        ## path dot

        path_dot_dllm = (
            Dot(radius=0.05)
            .set_color(BLUE)
            .move_to(orders_dllm[5].get_center())
            .shift(DOWN)
        )
        self.play(FadeIn(path_dot_dllm))
        for i in range(len(dllm_order)):
            if i == 0:
                self.play(
                    path_dot_dllm.animate.move_to(
                        orders_dllm[dllm_order[i]].get_center()
                    ),
                    run_time=0.5,
                )
            else:
                path = BrokenLine(
                    orders_dllm[dllm_order[i - 1]].get_center(),
                    VGroup(
                        orders_dllm[dllm_order[i]], orders_dllm[dllm_order[i - 1]]
                    ).get_center()
                    + UP * 0.5,
                    orders_dllm[dllm_order[i]].get_center(),
                    smooth=True,
                )
                self.play(MoveAlongPath(path_dot_dllm, path), run_time=0.5)
        self.wait(2)

        ## ar model

        model_ar = (
            Rectangle(width=4.5, height=1.5, color=RED_A, fill_opacity=0.5)
            .move_to(LO)
            .shift(DOWN)
            .set_z_index(1)
        )
        modelt_ar = (
            Text("Transformer", font_size=24)
            .move_to(model_ar.get_center())
            .set_z_index(2)
        )

        orders_list = ["<0>", "<1>", "<2>", "<3>", "<4>", "<5>", "<6>", "<7>"]
        orders = (
            VGroup(
                *[
                    Text(o, font_size=20, font=MONO_FONT).set_color(GREY_A)
                    for o in orders_list
                ]
            )
            .arrange(RIGHT, buff=0.2)
            .next_to(model_ar, UP, buff=0.5)
        )
        self.playw(FadeIn(orders), FadeIn(model_ar), Write(modelt_ar), run_time=0.5)

        ## path dot ar

        path_dot = (
            Dot(radius=0.05).set_color(RED).move_to(orders[0].get_center()).shift(DOWN)
        )
        self.play(FadeIn(path_dot))
        for i in range(len(orders)):
            self.play(path_dot.animate.move_to(orders[i].get_center()), run_time=0.5)
        self.wait(2)

        ## dLLM sampling the ar order by chance

        ar_order = list(range(len(orders_dllm)))

        self.play(FadeOut(path_dot_dllm), run_time=0.5)
        path_dot_dllm_ar = (
            Dot(radius=0.05)
            .set_color(BLUE)
            .move_to(orders_dllm[0].get_center())
            .shift(DOWN)
        )
        self.play(FadeIn(path_dot_dllm_ar))
        for i in range(len(ar_order)):
            if i == 0:
                self.play(
                    path_dot_dllm_ar.animate.move_to(
                        orders_dllm[ar_order[i]].get_center()
                    ),
                    run_time=0.5,
                )
            else:
                path = BrokenLine(
                    orders_dllm[ar_order[i - 1]].get_center(),
                    VGroup(
                        orders_dllm[ar_order[i]], orders_dllm[ar_order[i - 1]]
                    ).get_center()
                    + UP * 0.5,
                    orders_dllm[ar_order[i]].get_center(),
                    smooth=True,
                )
                self.play(MoveAlongPath(path_dot_dllm_ar, path), run_time=0.5)
        self.wait(2)


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
        self.play(
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

class pathKPotential(InteractiveScene, Scene2D):
    def construct(self):
        ## model

        model = (
            Rectangle(width=4.5, height=1.5, color=BLUE_A, fill_opacity=0.5)
            .move_to(ORIGIN)
            .set_z_index(1)
        )
        modelt = (
            Text("Transformer", font_size=24).move_to(model.get_center()).set_z_index(2)
        )

        self.addw(model, modelt)

        ## answers

        answer1 = Words("The answer is ABC...", font_size=24)
        answer1.words[3:].set_color(random_color())
        answer2 = Words("The answer is blahblah...", font_size=24)
        answer2.words[3:].set_color(random_color())
        answer3 = Words("The answer is 42, because ...", font_size=24)
        answer3.words[3:].set_color(PURE_GREEN)
        answer4 = Words("The answer is very difficult to ...", font_size=24)
        answer4.words[3:].set_color(random_color())

        answers = (
            VGroup(answer1, answer2, answer3, answer4)
            .arrange(UP, aligned_edge=LEFT, buff=0.15)
            .next_to(model, UP, buff=0.35)
        )

        self.play(FadeIn(answer1, shift=answer1.get_center() - model.get_center(), scale=2))
        self.play(FadeIn(answer2, shift=answer2.get_center() - model.get_center(), scale=2), run_time=0.5)
        self.play(FadeIn(answer3, shift=answer3.get_center() - model.get_center(), scale=2), run_time=0.5)
        self.playw(FadeIn(answer4, shift=answer4.get_center() - model.get_center(), scale=2), run_time=0.5)

        ## xxcx

        def get_checkmark():
            checkmark = Text("✓", font_size=24).set_color(GREEN_B)
            return checkmark
        
        def get_cross():
            cross = Text(X_STRING, font_size=24, font="Sans Not-Rotated 24").set_color(RED_B)
            return cross

        e1 = get_cross().next_to(answer1, RIGHT, buff=0.1)
        e2 = get_cross().next_to(answer2, RIGHT, buff=0.1)
        e3 = get_checkmark().next_to(answer3, RIGHT, buff=0.1)
        e4 = get_cross().next_to(answer4, RIGHT, buff=0.1)

        es = VGroup(e1, e2, e3, e4)

        self.playw(FadeIn(es), *[t.animate.set_opacity(0.3) for t in [answers[0], answers[1], answers[3]]])

class GRPO(InteractiveScene, Scene2D):
    def construct(self):
        ## model

        model = (
            Rectangle(width=4.5, height=1.5, color=BLUE_A, fill_opacity=0.5)
            .move_to(ORIGIN)
            .set_z_index(1)
        )
        modelt = (
            Text("Transformer", font_size=24).move_to(model.get_center()).set_z_index(2)
        )

        self.addw(model, modelt)

        ## question

        q = Words("What is the answer of 3 × 4?", font_size=24).next_to(model, DOWN, buff=0.35)

        self.playwl(*[FadeIn(w) for w in q.words], lag_ratio=0.3)

        ## answers

        answer1 = Words("The answer is 8.", font_size=24).set_color(RED)
        answer2 = Words("I don't know.", font_size=24).set_color(RED)
        answer3 = Words("The answer is 12.", font_size=24).set_color(GREEN)
        answer4 = Words("The answer is 16.", font_size=24).set_color(RED)

        answers = (
            VGroup(answer1, answer2, answer3, answer4)
            .arrange(UP, aligned_edge=LEFT, buff=0.15)
            .next_to(model, UP, buff=0.35)
        )

        self.play(FadeIn(answer1, shift=answer1.get_center() - model.get_center(), scale=2))
        self.play(FadeIn(answer2, shift=answer2.get_center() - model.get_center(), scale=2), run_time=0.5)
        self.play(FadeIn(answer3, shift=answer3.get_center() - model.get_center(), scale=2), run_time=0.5)
        self.playw(FadeIn(answer4, shift=answer4.get_center() - model.get_center(), scale=2), run_time=0.5)

        ## + if correct, - if wrong, xxcx

        e1 = Text("-", font_size=30).set_color(RED).next_to(answer1, RIGHT, buff=0.1)
        e2 = Text("-", font_size=30).set_color(RED).next_to(answer2, RIGHT, buff=0.1)
        e3 = Text("+", font_size=30).set_color(GREEN).next_to(answer3, RIGHT, buff=0.1)
        e4 = Text("-", font_size=30).set_color(RED).next_to(answer4, RIGHT, buff=0.1)

        es = VGroup(e1, e2, e3, e4)

        self.playw(FadeIn(es))

        ## train

        t1 = VGroup(answer1, e1)
        t2 = VGroup(answer2, e2)
        t3 = VGroup(answer3, e3)
        t4 = VGroup(answer4, e4)

        self.playwl(FadeOut(t1, shift=model.get_center()-t1.get_center(), scale=2), Indicate(model, color=RED), lag_ratio=0.5)
        self.playwl(FadeOut(t2, shift=model.get_center()-t2.get_center(), scale=2), Indicate(model, color=RED), lag_ratio=0.5, wait=0)
        self.playwl(FadeOut(t3, shift=model.get_center()-t3.get_center(), scale=2), Indicate(model, color=GREEN), lag_ratio=0.5, wait=0)
        self.playwl(FadeOut(t4, shift=model.get_center()-t4.get_center(), scale=2), Indicate(model, color=RED), lag_ratio=0.5)


        self.playw(FadeIn(VGroup(t1, t2, t3, t4)))

        self.embed()
        ## indicate answer

        self.playw(Circumscribe(t3, color=GREEN), *[t.animate.set_opacity(0.3) for t in [t1, t2, t4]])

class GRPOfail(InteractiveScene, Scene2D):
    def construct(self):
        ## model

        model = (
            Rectangle(width=4.5, height=1.5, color=BLUE_A, fill_opacity=0.5)
            .move_to(ORIGIN)
            .set_z_index(1)
        )
        modelt = (
            Text("Transformer", font_size=24).move_to(model.get_center()).set_z_index(2)
        )

        ## question

        q = Words("What is the answer of 3 × 4?", font_size=24).next_to(model, DOWN, buff=0.35)

        self.addw(q, model, modelt)

        ## answers

        answer1 = Words("The answer is 8.", font_size=24).set_color(RED)
        answer2 = Words("I don't know.", font_size=24).set_color(RED)
        answer3 = Words("The answer is 15.", font_size=24).set_color(RED)
        answer4 = Words("The answer is 16.", font_size=24).set_color(RED)

        answers = (
            VGroup(answer1, answer2, answer3, answer4)
            .arrange(UP, aligned_edge=LEFT, buff=0.15)
            .next_to(model, UP, buff=0.35)
        )

        self.play(FadeIn(answer1, shift=answer1.get_center() - model.get_center(), scale=2), run_time=0.5)
        self.play(FadeIn(answer2, shift=answer2.get_center() - model.get_center(), scale=2), run_time=0.5)
        self.play(FadeIn(answer3, shift=answer3.get_center() - model.get_center(), scale=2), run_time=0.5)
        self.playw(FadeIn(answer4, shift=answer4.get_center() - model.get_center(), scale=2), run_time=0.5)

        sr = SurroundingRectangle(answers, buff=0.1).set_color(RED)

        self.playw(FadeIn(sr))