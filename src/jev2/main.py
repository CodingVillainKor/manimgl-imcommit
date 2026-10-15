from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        noul_text = Text("noul", font_size=24)
        noul_box = Rectangle(width=2, height=1)
        noul = VGroup(noul_text, noul_box).set_color(ORANGE)
        score_text = Text("score", font_size=24)
        score_box = Rectangle(width=2, height=1)
        score = VGroup(score_text, score_box).set_color(GREEN)
        VGroup(noul, score).arrange(RIGHT, buff=0.5)
        self.play(FadeIn(noul))
        self.playw(FadeIn(score))

        ## choice

        choice_text = Text("choice", font_size=24)
        choice_box = Rectangle(width=5.5, height=3)
        choice_text.align(choice_box, UR, buff=0.1)
        choice = VGroup(choice_text, choice_box).set_color(BLUE)
        self.playw(FadeIn(choice))

        ## types

        self.play(
            choice_box.animate.set_stroke(opacity=0.3),
            choice_text.animate.set_opacity(0.3),
            run_time=0.75,
        )
        self.playw(
            RWiggle(noul, amp=0.3, speed=2),
            RWiggle(score, amp=0.3, speed=2),
            run_time=3,
        )


class noul(InteractiveScene, Scene2D):
    def construct(self):

        ## last state of intro
        noul_text = Text("noul", font_size=24)
        noul_box = Rectangle(width=2, height=1)
        noul = VGroup(noul_text, noul_box).set_color(ORANGE)
        score_text = Text("score", font_size=24)
        score_box = Rectangle(width=2, height=1)
        score = VGroup(score_text, score_box).set_color(GREEN)
        VGroup(noul, score).arrange(RIGHT, buff=0.5)
        self.add(noul, score)

        ## choice
        choice_text = Text("choice", font_size=24)
        choice_box = Rectangle(width=5.5, height=3)
        choice_text.align(choice_box, UR, buff=0.1)
        choice = VGroup(choice_text, choice_box).set_color(BLUE)
        choice_box.set_stroke(opacity=0.3)
        choice_text.set_opacity(0.3)
        self.addw(choice)

        ## fadeout choice and score
        self.play(FadeOut(choice), FadeOut(score), run_time=0.75)
        nt = noul.generate_target()
        nt[1].stretch_to_fit_width(5 * 1.77777).stretch_to_fit_height(5).set_stroke(
            width=1.5, opacity=0.7
        )
        nt.move_to(ORIGIN).shift(UP * 0.5)
        self.playw(MoveToTarget(noul))

        ## circumscribe nt[0]
        self.playw(Circumscribe(nt[0]))

        ## Bernoulli
        bernoulli_text = (
            Text("Bernoulli", font_size=24).set_color(GREY_D).shift(UP * 0.5)
        )
        b37 = bernoulli_text[3:7].set_color(ORANGE)
        bernoulli_text.shift(noul[0].get_center() - b37.get_center())
        self.playw(FadeIn(bernoulli_text))

        ## yest, not
        yes_t = Text("yes", font_size=24).set_color(GREEN)
        no_t = Text("no", font_size=24).set_color(RED)
        yesno = (
            VGroup(yes_t, no_t)
            .arrange(RIGHT, buff=0.5)
            .next_to(bernoulli_text, DOWN, buff=0.5)
        )
        self.play(FadeIn(yes_t, shift=yes_t.get_center() - b37.get_center()))
        self.playw(FadeIn(no_t, shift=no_t.get_center() - b37.get_center()))

        ## choice: much bigger than camera frame
        choice_text = Text("choice", font_size=24)
        choice_box = Rectangle(width=30.5, height=15)
        choice_text.align(choice_box, UR, buff=8).shift(UR + UP * 3)
        choice = VGroup(choice_text, choice_box).set_color(BLUE)
        choice_box.set_stroke(opacity=0.3)
        choice_text.set_opacity(1).rotate(66 * DEGREES, axis=RIGHT)
        self.add(choice)
        self.cf.save_state()
        self.play(
            FadeOut(yesno),
            self.cf.animate.reorient(
                0, 66, 0, (np.float32(2.25), np.float32(1.42), np.float32(0.79)), 11.01
            ),
        )

        ## multi choices
        m1 = Text("choice 1: ...", font_size=24).set_color(BLUE)
        m2 = Text("choice 2: ...", font_size=24).set_color(BLUE)
        m3 = Text("choice 3: ...", font_size=24).set_color(BLUE)
        ms = (
            VGroup(m1, m2, m3)
            .arrange(DOWN, buff=0.5)
            .next_to(noul_box, RIGHT, buff=0.5)
        )
        self.play(FadeIn(ms))
        self.playw(ms.animate.rotate(66 * DEGREES, axis=RIGHT))

        ## restore camera frame
        self.play(self.cf.animate.restore(), FadeOut(ms), FadeOut(bernoulli_text))

        ## true or false choices
        tf1 = Text("True", font_size=24).set_color(GREEN)
        tf2 = Text("False", font_size=24).set_color(RED)
        tf_choices = (
            VGroup(tf1, tf2)
            .arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            .next_to(noul_text, RIGHT, buff=0.75)
        )
        self.play(FadeIn(tf_choices))
        line_true = DashedLine(noul_text.get_right(), tf1.get_left(), buff=0.1)
        line_false = DashedLine(noul_text.get_right(), tf2.get_left(), buff=0.1)
        self.playw(Create(line_true), Create(line_false), run_time=0.75)


class noulResponse(InteractiveScene, Scene2D):
    def construct(self):
        ## choice request and response

        nl = NumberLine(x_range=(-0.1, 1.1, 2), unit_size=6, include_ticks=False)
        tick_buff = 0.1
        tick0 = Line(nl.n2p(0) + UP * tick_buff, nl.n2p(0) - UP * tick_buff)
        tick1 = Line(nl.n2p(1) + UP * tick_buff, nl.n2p(1) - UP * tick_buff)
        tick_half = Line(
            nl.n2p(0.5) + UP * tick_buff, nl.n2p(0.5) - UP * tick_buff
        ).set_color(GREY_C)
        t0 = Text("0", font_size=24, font=MONO_FONT).next_to(tick0, DOWN, buff=0.1)
        t_half = (
            Text("0.5", font_size=24, font=MONO_FONT)
            .next_to(tick_half, DOWN, buff=0.1)
            .set_color(GREY_C)
        )
        t1 = Text("1", font_size=24, font=MONO_FONT).next_to(tick1, DOWN, buff=0.1)
        self.add(nl, tick0, tick_half, tick1, t0, t_half, t1)

        ## def get noul
        def get_noul(value):
            dot = Dot(nl.n2p(value), radius=0.08).set_color(
                interpolate_color(RED_C, BLUE_C, value)
            )
            arrow = Arrow(
                dot.get_top() + UP * 0.7, dot.get_top(), buff=0.07, thickness=2
            )
            text = (
                Text(f"noul: {value:.2f}", font_size=20)
                .next_to(arrow, UP, buff=0.1)
                .set_color(interpolate_color(RED_C, BLUE_C, value))
            )
            return VGroup(dot, arrow, text)

        val = ValueTracker(0.53)
        noul = get_noul(val.get_value())
        self.addw(noul)

        noul.add_updater(lambda m: m.become(get_noul(val.get_value())))
        self.playw(val.animate.set_value(0.03), run_time=1.5)
        self.playw(val.animate.set_value(0.98), run_time=1.5)

        noul.clear_updaters()

        ## state and questions
        state_text = Words("state: ㅋㅋ 개꿀ㄹ", font_size=24).set_color(GREEN_B)
        state_text.words[1:].set_color(WHITE)
        question_text = Words(
            "instructions: state는 지금 긍정적인 상태인가요?", font_size=24
        ).set_color(YELLOW_B)
        question_text.words[1:].set_color(WHITE)
        sq = (
            VGroup(state_text, question_text)
            .arrange(DOWN, aligned_edge=LEFT)
            .shift(UP * 2.25)
        )
        self.playw(FadeIn(sq, shift=RIGHT))

        q2_text = Words("instructions: state는 문의 중인가요?", font_size=24).set_color(
            YELLOW_B
        )
        q2_text.words[1:].set_color(WHITE).move_to(
            question_text.words[1:].get_center()
        ).align_to(question_text.words[1:], LEFT)
        noul.add_updater(lambda m: m.become(get_noul(val.get_value())))
        self.play(Transformr(question_text.words[1:], q2_text.words[1:]))
        self.play(Circumscribe(q2_text.words[1:]))
        self.playw(val.animate.set_value(0.08), run_time=1.5)

        ## q3
        q3_text = Words(
            "instructions: state는 불만을 토로하고 있나요?", font_size=24
        ).set_color(YELLOW_B)
        q3_text.words[1:].set_color(WHITE).move_to(
            question_text.words[1:].get_center()
        ).align_to(question_text.words[1:], LEFT)
        self.play(Transformr(q2_text.words[1:], q3_text.words[1:]))
        self.play(Circumscribe(q3_text.words[1:]))
        self.playw(val.animate.set_value(0.32), run_time=1.5)


class whatisScore(InteractiveScene, Scene2D):
    def construct(self):

        ## last state of intro
        noul_text = Text("noul", font_size=24)
        noul_box = Rectangle(width=2, height=1)
        noul = VGroup(noul_text, noul_box).set_color(ORANGE)
        score_text = Text("score", font_size=24)
        score_box = Rectangle(width=2, height=1)
        score = VGroup(score_text, score_box).set_color(GREEN)
        VGroup(noul, score).arrange(RIGHT, buff=0.5)
        self.add(noul, score)

        ## choice
        choice_text = Text("choice", font_size=24)
        choice_box = Rectangle(width=5.5, height=3)
        choice_text.align(choice_box, UR, buff=0.1)
        choice = VGroup(choice_text, choice_box).set_color(BLUE)
        choice_box.set_stroke(opacity=0.3)
        choice_text.set_opacity(0.3)
        self.addw(choice)

        ## fadeout noul
        self.playw(FadeOut(noul))

        ## choice text: opacity 1 and box to be circle and become choice_box
        self.play(
            choice_text.animate.set_opacity(1),
            choice_box.animate.become(Circle(radius=3).set_color(BLUE).shift(RIGHT)),
            run_time=0.75,
        )
        self.play(
            Transform(choice_box, score_box.copy()),
            FadeOut(
                choice_text, shift=score_text.get_center() - choice_text.get_center()
            ),
            run_time=0.75,
        )
        self.remove(choice_box)
        st = score.generate_target()
        st[1].stretch_to_fit_width(5 * 1.77777).stretch_to_fit_height(5).set_stroke(
            width=1.5, opacity=0.7
        ).move_to(ORIGIN)
        st[0].align(st[1], UR, buff=0.1)
        self.playw(MoveToTarget(score))

        ## nl
        nl = NumberLine(
            x_range=[-0.1, 3.1, 1], width=7, color=WHITE, include_ticks=False
        ).shift(DOWN * 0.7)
        ticks = VGroup(
            *[
                Line(nl.n2p(i) + UP * 0.07, nl.n2p(i) + DOWN * 0.07, color=WHITE)
                for i in [0, 1, 2, 3]
            ]
        )
        tick_texts = VGroup(
            *[
                Text(string, font_size=18).next_to(ticks[i], DOWN, buff=0.1)
                for i, string in enumerate(
                    ["중립", "약한 감정", "보통 감정", "강한 감정"]
                )
            ]
        ).set_color(GREY_A)
        tick_nums = VGroup(
            *[
                Text(str(i), font_size=18).next_to(tick_texts[i], DOWN, buff=0.1)
                for i in [0, 1, 2, 3]
            ]
        )
        self.play(
            FadeIn(nl), FadeIn(ticks), FadeIn(VGroup(tick_texts[0], tick_nums[0]))
        )
        self.playwl(
            *[FadeIn(VGroup(tick_texts[i], tick_nums[i])) for i in range(1, 4)],
            lag_ratio=0.5,
            wait=5,
        )

        ## 가중합
        texts = tick_texts.copy()
        texts.generate_target().arrange(DOWN, buff=0.3, aligned_edge=RIGHT).next_to(
            nl.n2p(0), UP, buff=0.75, aligned_edge=RIGHT
        )
        self.play(MoveToTarget(texts))

        logits = Group(
            ValueTracker(np.log(0.01)),
            ValueTracker(np.log(0.48)),
            ValueTracker(np.log(0.44)),
            ValueTracker(np.log(0.07)),
        )

        def get_probs() -> Group[DecimalNumber]:
            total = sum([tracker.get_value() for tracker in logits])
            # robust softmax
            max_logit = max([tracker.get_value() for tracker in logits])
            exp_values = [np.exp(tracker.get_value() - max_logit) for tracker in logits]
            total_exp = sum(exp_values)
            return VGroup(
                *[DecimalNumber(exp_val / total_exp) for exp_val in exp_values]
            )

        probs = get_probs()
        _h = 0.25
        _w = nl.n2p(1) - nl.n2p(0)
        _w = _w[0]

        def get_bars_upper() -> VGroup[Rectangle]:
            probs = get_probs()
            c1, c2, c3, c4 = YELLOW_B, GREEN_B, YELLOW_E, GREEN_E
            bar1 = (
                Rectangle(height=_h, width=probs[0].get_value() * _w, color=c1)
                .next_to(texts[0], RIGHT, buff=0.2)
                .set_stroke(width=1)
                .set_fill(opacity=1)
            )
            bar2 = (
                Rectangle(height=_h, width=probs[1].get_value() * _w, color=c2)
                .next_to(texts[1], RIGHT, buff=0.2)
                .set_stroke(width=1)
                .set_fill(opacity=1)
            )
            bar3 = (
                Rectangle(height=_h, width=probs[2].get_value() * _w, color=c3)
                .next_to(texts[2], RIGHT, buff=0.2)
                .set_stroke(width=1)
                .set_fill(opacity=1)
            )
            bar4 = (
                Rectangle(height=_h, width=probs[3].get_value() * _w, color=c4)
                .next_to(texts[3], RIGHT, buff=0.2)
                .set_stroke(width=1)
                .set_fill(opacity=1)
            )
            return VGroup(bar1, bar2, bar3, bar4)

        def get_bars_lower() -> VGroup[Rectangle]:
            probs = get_probs()
            c1, c2, c3, c4 = YELLOW_B, GREEN_B, YELLOW_E, GREEN_E
            bar1 = (
                Rectangle(height=_h, width=probs[0].get_value() * 0 * _w, color=c1)
                .set_stroke(width=1)
                .set_fill(opacity=1)
            )
            bar2 = (
                Rectangle(height=_h, width=probs[1].get_value() * 1 * _w, color=c2)
                .set_stroke(width=1)
                .set_fill(opacity=1)
            )
            bar3 = (
                Rectangle(height=_h, width=probs[2].get_value() * 2 * _w, color=c3)
                .set_stroke(width=1)
                .set_fill(opacity=1)
            )
            bar4 = (
                Rectangle(height=_h, width=probs[3].get_value() * 3 * _w, color=c4)
                .set_stroke(width=1)
                .set_fill(opacity=1)
            )
            return (
                VGroup(bar1, bar2, bar3, bar4)
                .arrange(RIGHT, buff=0)
                .next_to(nl.n2p(0), RIGHT, buff=0)
            )

        def get_lines1() -> VGroup[Line]:
            line1_l = DashedLine(
                start=bars_upper[1].get_corner(DL), end=bars_lower[1].get_corner(UL)
            ).set_color(GREEN_B)
            line1_r = DashedLine(
                start=bars_upper[1].get_corner(DR), end=bars_lower[1].get_corner(UR)
            ).set_color(GREEN_B)
            return VGroup(line1_l, line1_r)

        def get_lines2() -> VGroup[Line]:
            line1_l = DashedLine(
                start=bars_upper[2].get_corner(DL), end=bars_lower[2].get_corner(UL)
            ).set_color(YELLOW_E)
            line1_r = DashedLine(
                start=bars_upper[2].get_corner(DR), end=bars_lower[2].get_top()
            ).set_color(YELLOW_E)
            line2_l = DashedLine(
                start=bars_upper[2].get_corner(DL), end=bars_lower[2].get_top()
            ).set_color(YELLOW_E)
            line2_r = DashedLine(
                start=bars_upper[2].get_corner(DR), end=bars_lower[2].get_corner(UR)
            ).set_color(YELLOW_E)
            return VGroup(line1_l, line1_r, line2_l, line2_r)

        def get_lines3() -> VGroup[Line]:
            ul, ur = bars_lower[3].get_corner(UL), bars_lower[3].get_corner(UR)
            dl, dr = bars_upper[3].get_corner(DL), bars_upper[3].get_corner(DR)
            return VGroup(
                *[
                    DashedLine(start=start, end=interpolate(ul, ur, t))
                    for i in range(3)
                    for start, t in ((dl, i / 3), (dr, (i + 1) / 3))
                ]
            ).set_color(GREEN_E)

        bars_upper = get_bars_upper()
        bars_lower = get_bars_lower()
        lines1 = get_lines1()
        lines2 = get_lines2()
        lines3 = get_lines3()
        self.playw(
            FadeIn(bars_upper),
            FadeIn(bars_lower),
            FadeIn(lines1),
            FadeIn(lines2),
            FadeIn(lines3),
        )

        ## state: "내 API 키였네;;", instructions: "이 사람 감정이 지금 얼마나 격한가요?"
        state_text = Words('"state": "내 API 키였네;;"', font_size=20)
        state_text.words[0].set_color(YELLOW_B)
        instructions_text = Words(
            '"instructions": "이 사람 감정이 지금 얼마나 격한가요?"', font_size=20
        )
        instructions_text.words[0].set_color(GREEN_B)
        si = (
            VGroup(state_text, instructions_text)
            .arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            .align(score_box, UP)
            .shift(RIGHT)
        )
        self.playw(FadeIn(instructions_text))

        ## circumscribe tick_texts, nums
        self.play(Circumscribe(VGroup(tick_texts[0], tick_nums[0])))
        self.play(Circumscribe(VGroup(tick_texts[1], tick_nums[1])))
        self.playwl(
            Circumscribe(VGroup(tick_texts[2], tick_nums[2])),
            Circumscribe(VGroup(tick_texts[3], tick_nums[3])),
            lag_ratio=0.5,
        )

        ## nums: 0.01, 0.48, 0.44, 0.07
        def get_nums() -> VGroup:
            return VGroup(
                *[
                    DecimalNumber(n, font_size=24).next_to(bars_upper[i])
                    for i, n in enumerate([p.get_value() for p in get_probs()])
                ]
            )
        nums = get_nums()
        self.playw(FadeIn(nums))

        ## fade in state
        self.playw(FadeIn(state_text))

        self.playw(FlashUnder(state_text.words[1:]))

        ## def get_sum
        def get_sum() -> DecimalNumber:
            nums_sum = sum([p.get_value() * i for i, p in enumerate(get_probs())])
            nums_sum = np.floor(nums_sum * 100) / 100
            return DecimalNumber(nums_sum, font_size=24).next_to(bars_lower[-1], UR, buff=0.05)

        nums_sum = get_sum()
        self.playw(FadeIn(nums_sum))

        self.embed()
        ## animate via updating the sum as the bars change
        l1, l2, l3, l4 = logits
        bars_upper.add_updater(lambda m: m.become(get_bars_upper()))
        bars_lower.add_updater(lambda m: m.become(get_bars_lower()))
        lines1.add_updater(lambda m: m.become(get_lines1()))
        lines2.add_updater(lambda m: m.become(get_lines2()))
        lines3.add_updater(lambda m: m.become(get_lines3()))
        nums.add_updater(lambda m: m.become(get_nums()))
        nums_sum.add_updater(lambda m: m.become(get_sum()))
        self.playw(
            l1.animate.set_value(np.log(0.001)),
            l2.animate.set_value(np.log(0.03)),
            l3.animate.set_value(np.log(0.32)),
            l4.animate.set_value(np.log(0.65)),
            run_time=1.5,
        )
        

        for m in (bars_upper, bars_lower, lines1, lines2, lines3, nums, nums_sum):
            m.clear_updaters()


        ## lines show each pair 
        all_lines = [*lines1, *lines2, *lines3]
        pairs = [
            lines1,
            lines2[:2],
            lines2[2:4],
            lines3[:2],
            lines3[2:4],
            lines3[4:6],
        ]
        for pair in pairs:
            others = VGroup(*[l for l in all_lines if all(l is not p for p in pair)])
            self.play(others.animate(rate_func=there_and_back).set_opacity(0))
        self.wait(1)

        