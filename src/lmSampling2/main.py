from manimlib import *
from raenimgl import *
from random import seed
import sys
from pathlib import Path

# manimgl doesn't put this file's folder on sys.path
sys.path.insert(0, str(Path(__file__).parent))
from simulate import BrownianBox

seed(41)
np.random.seed(41)


def smoother(t: float, n: int = 2) -> float:
    # smooth applied n times: flatter start/end, steeper middle (peak slope 1.875**n)
    for _ in range(n):
        t = smooth(t)
    return t


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## set-up
        _line1 = (
            DashedLine(UP * 10, DOWN * 10).shift(LEFT * 7.111111 / 3).set_color(GREY_D)
        )
        _line2 = (
            DashedLine(UP * 10, DOWN * 10).shift(RIGHT * 7.111111 / 3).set_color(GREY_D)
        )
        _a1 = LEFT * 7.111111 * 2 / 3
        _a2 = ORIGIN
        _a3 = RIGHT * 7.111111 * 2 / 3
        title_topk = (
            Text("Top-k", font_size=24).move_to(_a1).shift(UP * 2.7).set_color(GREY_B)
        )
        title_topp = (
            Text("Top-p", font_size=24).move_to(_a2).shift(UP * 2.7).set_color(GREY_B)
        )
        title_temp = (
            Text("Temperature", font_size=24)
            .move_to(_a3)
            .shift(UP * 2.7)
            .set_color(GREY_B)
        )
        self.cf.save_state()
        self.cf.reorient(
            -89, 45, 89, (np.float32(-1.94), np.float32(2.45), np.float32(-1.9)), 4.43
        )
        self.add(_line1, _line2, title_topk, title_topp, title_temp)
        self.play(Restore(self.cf), run_time=1.0, rate_func=smoother)

        w = 3.5
        prob_list = [0.4, 0.2, 0.15, 0.12, 0.05, 0.04, 0.008, 0.006, 0.006] + [
            0.004
        ] * 5

        ## top_k bar
        top_k_bar = Rectangle(width=w, height=0.5).move_to(_a1).set_color(GREY_B)
        k = 3
        top_k_probs = VGroup()
        for i, p in enumerate(prob_list):
            if i >= k:
                opacity = 0
                stroke_color = interpolate_color(YELLOW_A, BLACK, 0.8)
            else:
                opacity = 0.3
                stroke_color = YELLOW_A
            prob = (
                Rectangle(width=w * p, height=0.5)
                .set_color(YELLOW_A)
                .set_stroke(width=0.5, color=stroke_color)
            )
            if i == 0:
                prob.align_to(top_k_bar, LEFT)
            else:
                prob.next_to(top_k_probs[-1], RIGHT, buff=0)
            prob.set_fill(opacity=opacity)
            top_k_probs.add(prob)

        top_k_text = (
            Text("Top 3", font_size=18, font=MONO_FONT)
            .next_to(top_k_probs[:3], UP, buff=0.75)
            .set_color(YELLOW_B)
        )
        top_k_lines = VGroup(
            *[DashedLine(top_k_text, prob.get_top()) for prob in top_k_probs[:3]]
        ).set_color(YELLOW_B)
        self.addw(top_k_text, top_k_lines, top_k_bar, top_k_probs)
        self.playw(
            Indicate(top_k_probs[:k], scale_factor=1.01, color=PURE_GREEN),
            Indicate(top_k_probs[k:], scale_factor=1.01, color=PURE_RED),
        )

        ## top_p bar
        top_p_bar = (
            Rectangle(width=w, height=0.5).move_to(_a2).set_color(GREY_B).set_opacity(0)
        )
        _top_p90 = (
            top_p_bar.copy()
            .stretch_to_fit_width(w * 0.9)
            .align_to(top_p_bar, LEFT)
            .set_opacity(0)
        )
        line_90 = DashedLine(
            _top_p90.get_corner(UR), _top_p90.get_corner(DR)
        ).set_color(PURE_GREEN)
        topp_90b = Brace(_top_p90, UP, buff=0.05)
        topp_90b_text = Text("0.9", font_size=18, font=MONO_FONT).next_to(
            topp_90b, UP, buff=0.05
        )
        total_b = Brace(top_p_bar, DOWN, buff=0.05).set_color(GREY_C)
        total_text = (
            Text("1.0", font_size=18, font=MONO_FONT)
            .next_to(total_b, DOWN, buff=0.05)
            .set_color(GREY_B)
        )
        top_p_probs = VGroup()
        prob_num = 0
        n_top_p = 0
        for i, p in enumerate(prob_list):
            if prob_num < 0.9:
                n_top_p += 1
                opacity = 0.3
                stroke_color = YELLOW_A
            else:
                opacity = 0
                stroke_color = interpolate_color(YELLOW_A, BLACK, 0.8)
            prob = (
                Rectangle(width=w * p, height=0.5)
                .set_color(YELLOW_A)
                .set_stroke(width=0.5, color=stroke_color)
            )
            prob_num += p
            if i == 0:
                prob.align_to(top_p_bar, LEFT)
            else:
                prob.next_to(top_p_probs[-1], RIGHT, buff=0)
            prob.set_fill(opacity=opacity)
            top_p_probs.add(prob)

        self.addw(
            top_p_bar,
            top_p_probs,
            topp_90b,
            topp_90b_text,
            line_90,
            total_b,
            total_text,
        )
        self.playw(
            Indicate(top_p_probs[:n_top_p], scale_factor=1.01, color=PURE_GREEN),
            Indicate(top_p_probs[n_top_p:], scale_factor=1.01, color=PURE_RED),
        )

        ## temperature
        word_bars = VGroup()
        denom = 50
        logit_list = [math.log(p * denom) for p in prob_list]
        for i, p in enumerate(prob_list):
            bar = (
                Rectangle(height=w * p, width=0.2)
                .set_stroke(width=1)
                .set_fill(BLUE_A, opacity=0.3)
            )
            word_bars.add(bar)
        word_bars.arrange(RIGHT, buff=0.1, aligned_edge=DOWN).move_to(_a3)
        self.add(word_bars)

        ## change temperature
        temp = ValueTracker(1.0)
        temp_text = Text("temperature:", font_size=18, font=MONO_FONT).next_to(
            word_bars, DOWN, buff=0.5
        )

        def get_temp_value(temperature):
            return DecimalNumber(
                temperature, num_decimal_places=2, font_size=18
            ).next_to(temp_text, RIGHT, buff=0.1)

        temp_value = get_temp_value(temp.get_value())
        self.addw(temp_text, temp_value, wait=0.5)

        ## update temperature value when temp changes
        def update_temp_value(mob):
            mob.become(get_temp_value(temp.get_value()))

        _word_bars = word_bars.copy()

        def softmax_robust(x, temperature):
            x_max = max(x)
            e_x = [math.exp((xi - x_max) / temperature) for xi in x]
            sum_e_x = sum(e_x)
            return [xi / sum_e_x for xi in e_x]

        def update_word_bars(mob):
            probs = softmax_robust(logit_list, temp.get_value())
            for i, bar in enumerate(mob):
                bar.stretch_to_fit_height(w * probs[i]).align_to(_word_bars[i], DOWN)

        word_bars.add_updater(update_word_bars)
        temp_value.add_updater(update_temp_value)

        self.play(temp.animate.set_value(5.0), run_time=2)
        self.playw(temp.animate.set_value(0.3), run_time=2)


class wotopK(InteractiveScene, Scene2D):
    def construct(self):

        ## start
        llm_box = (
            Rectangle(width=4, height=2)
            .set_fill(GREY_E, opacity=0.7)
            .set_stroke(width=1)
        )
        llm_txt = Text("LLM", font_size=24, font=MONO_FONT).align(llm_box, UR, buff=0.1)
        llm = VGroup(llm_box, llm_txt).set_z_index(1)
        self.playw(GrowFromCenter(llm))

        ## subword seq
        num_t = 7
        tensor = (
            Tensor(num_t, shape="rectangle", arrange=RIGHT, ellipsis=True, buff=0.15)
            .set_color_by_gradient(*raenim_colors(num_t))
            .next_to(llm, DOWN)
            .align(llm, LEFT, buff=0.15)
        )
        sentence = Words(
            "[User] 핫도그 세 ... 영어로 번역해줘 [Assistant]", font_size=20
        )

        sentence.words.set_color_by_gradient(*raenim_colors(len(sentence.words)))
        for w in sentence.words:
            w.rotate(PI / 2)
        sentence.words.arrange(RIGHT, aligned_edge=UP, buff=0.15).align(
            tensor, UL, buff=0
        )
        sseq = (
            Text("Subword Sequence", font_size=24, font=MONO_FONT)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .next_to(tensor, LEFT)
        )
        sc = sentence.copy()
        self.play(FadeIn(sentence))
        self.playw(Transformr(sentence.words, tensor))
        self.playw(FadeIn(sseq))

        ## latent
        latent = Tensor(
            num_t, shape="rectangle", arrange=RIGHT, ellipsis=True, buff=0.15
        ).align(tensor, LEFT, buff=0)
        self.play(Transformr(tensor.copy(), latent), run_time=0.75)

        ## output
        output = Tensor(1).next_to(llm, UP).set_x(latent[-1].get_x())
        self.play(Transformr(latent.copy(), output), run_time=0.75)

        ## so many probs: eng, kor, japanese, chinese, ...
        words = Words(
            "... wow three ... 복싱 코사인 ... こんにちは ビール ... 演替 ...",
            font_size=20,
        )
        idxs = [1, 2, 4, 5, 7, 8, 10]
        for w in words.words:
            w.rotate(PI / 2)
        words.words.arrange(RIGHT, aligned_edge=DOWN, buff=0.35).next_to(
            output, UP, buff=0.15
        )
        self.playw(FadeIn(words))
        probs = Words(
            "a 0.01 0.53 a 0.02 0.01 a 0.01 0.02 a 0.02 a", font_size=18, font=MONO_FONT
        ).set_color(YELLOW_B)
        for i, w in enumerate(probs.words):
            if len(w) == 1:
                w.set_opacity(0)
            w.next_to(words.words[i], UP, buff=0.15)
        self.playw(FadeIn(probs))

        ## choice: three, idx is 2
        choice = SurroundingRectangle(
            VGroup(words.words[2], probs.words[2]), color=RED, buff=0.1
        )
        rest = VGroup(
            *[
                VGroup(words.words[i], probs.words[i])
                for i in range(len(words.words))
                if i != 2
            ]
        )
        self.play(FadeIn(choice), FadeOut(rest))
        choice_ = words.words[2]
        choice_.save_state()
        self.playw(
            choice_.animate.move_to(output).align(output, DOWN, buff=0),
            FadeOut(output),
            FadeOut(probs.words[2]),
            FadeOut(choice),
        )

        ## restore choice_
        self.play(Restore(choice_))
        self.playw(FadeIn(rest), FadeIn(probs.words[2]), FadeIn(output))

        ## indicate each idx index
        self.playwl(
            *[
                Indicate(VGroup(words.words[i], probs.words[i]), color=PURE_RED)
                for i in idxs
            ],
            lag_ratio=0.5,
        )

        ## input: 핫도그 ...
        tensor.save_state()
        self.playw(Transform(tensor, sc.words))

        ## please? three?
        candidate1 = (
            Text("please", font_size=20).set_color(GREY_D).next_to(tensor, RIGHT)
        )
        candidate2 = (
            Text("three", font_size=20).set_color(GREY_D).next_to(tensor, RIGHT)
        )
        self.cf.save_state()
        self.play(
            self.cf.animate.reorient(
                -90,
                45,
                90,
                (np.float32(0.81), np.float32(-1.48), np.float32(0.51)),
                3.53,
            )
        )
        self.playw(FadeIn(candidate1))
        self.playw(FadeTransform(candidate1, candidate2))

        ## restore camera, tensor and fadeout candidate2
        self.playw(Restore(tensor), Restore(self.cf), FadeOut(candidate2))

        ## wow: [1]
        self.playw(Indicate(VGroup(words.words[1], probs.words[1]), color=PURE_RED))

        ## 복싱, 코사인, こんにちは: [4, 5, 7]
        self.playwl(
            *[
                Indicate(VGroup(words.words[i], probs.words[i]), color=PURE_RED)
                for i in [4, 5, 7]
            ],
            lag_ratio=0.7,
            wait=4,
        )


class wtopK(InteractiveScene, Scene2D):
    def construct(self):

        ## start
        llm_box = (
            Rectangle(width=4, height=2)
            .set_fill(GREY_E, opacity=0.7)
            .set_stroke(width=1)
        )
        llm_txt = Text("LLM", font_size=24, font=MONO_FONT).align(llm_box, UR, buff=0.1)
        llm = VGroup(llm_box, llm_txt).set_z_index(1)
        self.add(llm)

        ## subword seq
        num_t = 7
        tensor = (
            Tensor(num_t, shape="rectangle", arrange=RIGHT, ellipsis=True, buff=0.15)
            .set_color_by_gradient(*raenim_colors(num_t))
            .next_to(llm, DOWN)
            .align(llm, LEFT, buff=0.15)
        )
        sseq = (
            Text("Subword Sequence", font_size=24, font=MONO_FONT)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .next_to(tensor, LEFT)
        )
        self.add(tensor, sseq)

        ## latent
        latent = Tensor(
            num_t, shape="rectangle", arrange=RIGHT, ellipsis=True, buff=0.15
        ).align(tensor, LEFT, buff=0)
        self.add(latent)

        ## output
        output = Tensor(1).next_to(llm, UP).set_x(latent[-1].get_x())
        self.addw(output)

        ## words in highest prob order
        words = Words("please three could would I ...", font_size=20)
        for w in words.words:
            w.rotate(PI / 2)
        words.words.arrange(RIGHT, aligned_edge=DOWN, buff=0.5).next_to(output, UP)
        probs = Words(
            "0.5 0.25 0.16 0.03 0.02", font_size=18, font=MONO_FONT
        ).set_color(YELLOW_B)
        for i, p in enumerate(probs.words):
            p.next_to(words.words[i], UP, buff=0.1)
        self.playw(FadeIn(words))
        self.playw(FadeIn(probs))

        ## top 3
        c1 = SurroundingRectangle(
            VGroup(words.words[0], probs.words[0]), buff=0.05, stroke_width=1
        )
        c2 = SurroundingRectangle(
            VGroup(words.words[1], probs.words[1]), buff=0.05, stroke_width=1
        )
        c3 = SurroundingRectangle(
            VGroup(words.words[2], probs.words[2]), buff=0.05, stroke_width=1
        )
        rest = VGroup(
            *[
                VGroup(words.words[i], probs.words[i] if i < len(probs.words) else None)
                for i in range(3, len(words.words))
            ]
        )
        self.playwl(*[FadeIn(c) for c in [c1, c2, c3]], lag_ratio=0.7, wait=0)
        self.playw(FadeOut(rest), wait=3)


class topP(InteractiveScene, Scene2D):
    def construct(self):
        ## top P sampling visualization
        llm_box = (
            Rectangle(width=4, height=2)
            .set_fill(GREY_E, opacity=0.7)
            .set_stroke(width=1)
        )
        llm_txt = Text("LLM", font_size=24, font=MONO_FONT).align(llm_box, UR, buff=0.1)
        llm = VGroup(llm_box, llm_txt).set_z_index(1)
        self.add(llm)

        ## subword seq
        num_t = 7
        tensor = (
            Tensor(num_t, shape="rectangle", arrange=RIGHT, ellipsis=True, buff=0.15)
            .set_color_by_gradient(*raenim_colors(num_t))
            .next_to(llm, DOWN)
            .align(llm, LEFT, buff=0.15)
        )
        sseq = (
            Text("Subword Sequence", font_size=24, font=MONO_FONT)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .next_to(tensor, LEFT)
        )
        self.add(tensor, sseq)

        ## latent
        latent = Tensor(
            num_t, shape="rectangle", arrange=RIGHT, ellipsis=True, buff=0.15
        ).align(tensor, LEFT, buff=0)
        self.add(latent)

        ## output
        output = Tensor(1).next_to(llm, UP).set_x(latent[-1].get_x())
        self.addw(output)

        ## candidate words and their probabilities
        words = Words("please three could would I ...", font_size=20)
        for w in words.words:
            w.rotate(PI / 2)
        words.words.arrange(RIGHT, aligned_edge=DOWN, buff=0.5).next_to(output, UP)
        probs = Words(
            "0.5 0.25 0.16 0.03 0.02", font_size=18, font=MONO_FONT
        ).set_color(YELLOW_B)
        for i, p in enumerate(probs.words):
            p.next_to(words.words[i], UP, buff=0.1)
        self.playw(FadeIn(words), FadeIn(probs))

        ## bar length 1
        w, h = 4, 0.4
        bar = Rectangle(height=h, width=w).shift(UP * 3.2).set_color(GREEN)
        p_tex = Tex("\\sum_i p_i = 1", font_size=28).next_to(bar, RIGHT)
        probs_list = [0.5, 0.25, 0.16, 0.03, 0.02, 0.04]
        prob_bars = VGroup(
            *[
                Rectangle(height=h, width=w * p)
                .set_stroke(opacity=0)
                .set_fill(BLUE, opacity=0.5)
                for p in probs_list
            ]
        )
        prob_bars.set_color_by_gradient(*[random_color() for _ in probs_list])
        prob_bars.arrange(RIGHT, buff=0).move_to(bar).align_to(bar, LEFT)
        border_lines = VGroup(
            *[
                DashedLine(start=b.get_corner(UR), end=b.get_corner(DR))
                for b in prob_bars[:-1]
            ]
        ).set_color(GREY_C)
        correspond_lines = VGroup(
            *[
                DashedLine(
                    start=(probs if i < len(probs.words) else words).words[i],
                    end=prob_bars[i].get_bottom(),
                    buff=0.05,
                )
                for i in range(len(probs_list))
            ]
        )

        self.play(
            FadeIn(bar),
            FadeIn(p_tex),
            self.cf.animate.reorient(
                0, 0, 0, (np.float32(0.09), np.float32(2.87), np.float32(0.0)), 4.68
            ),
        )
        self.playw(FadeIn(prob_bars), FadeIn(border_lines), FadeIn(correspond_lines))

        ## brace and p
        p_num = ValueTracker(0.72)

        def get_p(num):
            return Text(f"p = {num.get_value():.2f}", font_size=18, font=MONO_FONT)

        def get_brace(num):
            dummy_bar = Rectangle(height=h, width=w * num.get_value()).align(
                bar, UL, buff=0
            )
            return Brace(dummy_bar, UP, buff=0.1).set_color(GREY_B)

        brace = get_brace(p_num)
        p_text = get_p(p_num).next_to(brace, UP, buff=0.1)
        self.playw(FadeIn(brace), FadeIn(p_text))

        ## update brace and p_text when p_num changes
        def update_p_text(mob):
            return mob.become(get_p(p_num).next_to(brace, UP, buff=0.1))

        def update_brace(mob):
            return mob.become(get_brace(p_num))

        p_text.add_updater(update_p_text)
        brace.add_updater(update_brace)
        self.playw(p_num.animate.set_value(0.9), run_time=2)
        p_text.clear_updaters()
        brace.clear_updaters()

        ## indicate first two prob bars
        self.playw(
            Indicate(prob_bars[0], scale_factor=1.01, color=PURE_BLUE),
            Indicate(prob_bars[1], scale_factor=1.01, color=PURE_BLUE),
        )

        ## indicate first three prob bars
        self.playw(
            Indicate(prob_bars[0], scale_factor=1.01, color=PURE_BLUE),
            Indicate(prob_bars[1], scale_factor=1.01, color=PURE_BLUE),
            Indicate(prob_bars[2], scale_factor=1.01, color=PURE_BLUE),
        )

        ## fadeout all word, prob bars and lines
        self.play(
            FadeOut(words),
            FadeOut(probs),
            FadeOut(prob_bars),
            FadeOut(border_lines),
            FadeOut(correspond_lines),
        )

        ## new word and probabilities
        words = Words("please could give ...", font_size=16, font=MONO_FONT)
        for w in words.words:
            w.rotate(PI / 2)
        words.words.arrange(RIGHT, buff=0.45, aligned_edge=DOWN).next_to(output, UP)
        probs = Words("0.68 0.25 0.04 0.03", font_size=16, font=MONO_FONT).set_color(
            YELLOW_B
        )
        for i, p in enumerate(probs.words):
            p.next_to(words.words[i], UP, buff=0.1)
        probs_list = [0.68, 0.25, 0.04, 0.03]
        w = 4
        prob_bars = VGroup(
            *[
                Rectangle(height=h, width=w * p)
                .set_stroke(opacity=0)
                .set_fill(opacity=0.5)
                for p in probs_list
            ]
        )
        prob_bars.set_color_by_gradient(*[random_color() for _ in probs_list]).arrange(
            RIGHT, buff=0
        ).align(bar, UL, buff=0)
        border_lines = VGroup(
            *[
                DashedLine(start=b.get_corner(UR), end=b.get_corner(DR))
                for b in prob_bars[:-1]
            ]
        ).set_color(GREY_C)
        correspond_lines = VGroup(
            *[
                DashedLine(
                    start=(probs if i < len(probs.words) else words).words[i],
                    end=prob_bars[i].get_bottom(),
                    buff=0.05,
                )
                for i in range(len(probs_list))
            ]
        )

        self.playw(
            FadeIn(words),
            FadeIn(probs),
            FadeIn(prob_bars),
            FadeIn(border_lines),
            FadeIn(correspond_lines),
        )

        ## fadeout last two
        self.playw(
            FadeOut(prob_bars[-2:]),
            FadeOut(border_lines[-2:]),
            FadeOut(correspond_lines[-2:]),
            FadeOut(words.words[-2:]),
            FadeOut(probs.words[-2:]),
        )

        ## fadeout remaining elements
        self.play(
            FadeOut(prob_bars),
            FadeOut(border_lines[:-2]),
            FadeOut(correspond_lines[:-2]),
            FadeOut(words.words[:-2]),
            FadeOut(probs.words[:-2]),
        )

        ## new words and probabilities: 5 candidates sum is 0.92
        words = Words("hotdog please could give I ...", font_size=16, font=MONO_FONT)
        for w in words.words:
            w.rotate(PI / 2)
        words.words.arrange(RIGHT, buff=0.45, aligned_edge=DOWN).next_to(output, UP)
        probs = Words(
            "0.40 0.25 0.15 0.07 0.05 ...", font_size=16, font=MONO_FONT
        ).set_color(YELLOW_B)
        for i, p in enumerate(probs.words):
            p.next_to(words.words[i], UP, buff=0.1)
        probs_list = [0.40, 0.25, 0.15, 0.07, 0.05]
        w = 4
        prob_bars = VGroup(
            *[
                Rectangle(height=h, width=w * p)
                .set_stroke(opacity=0)
                .set_fill(opacity=0.5)
                for p in probs_list
            ]
        )
        prob_bars.set_color_by_gradient(*[random_color() for _ in probs_list]).arrange(
            RIGHT, buff=0
        ).align(bar, UL, buff=0)
        border_lines = VGroup(
            *[
                DashedLine(start=b.get_corner(UR), end=b.get_corner(DR))
                for b in prob_bars[:-1]
            ]
        ).set_color(GREY_C)
        correspond_lines = VGroup(
            *[
                DashedLine(
                    start=(probs if i < len(probs.words) else words).words[i],
                    end=prob_bars[i].get_bottom(),
                    buff=0.05,
                )
                for i in range(len(probs_list))
            ]
        )

        self.playw(
            FadeIn(words),
            FadeIn(probs),
            FadeIn(prob_bars),
            FadeIn(border_lines),
            FadeIn(correspond_lines),
        )
        self.playwl(
            *[
                Indicate(prob_bars[i], scale_factor=1.02, color=PURE_BLUE)
                for i in range(len(prob_bars))
            ],
            lag_ratio=0.4,
        )


class temperatureLowandHigh(InteractiveScene, Scene2D):
    def construct(self):
        ## temperature expression, p(x) = \frac{e^{z_x / T}}{\sum_{i} e^{z_i / T}}
        temp_tex = Tex(
            r"p(x_i) = \frac{e^{z_{x_i} / T}}{\sum_{j} e^{z_j / T}}", font_size=48
        )
        self.addw(temp_tex)

        ## p(x_i) surrounding rectangle
        sr_px = SurroundingRectangle(temp_tex[:5], color=YELLOW_C, buff=0.15)
        self.playw(FadeIn(sr_px))

        ## actual model output: z_x_i
        zxi = temp_tex[7:10].copy()
        self.play(zxi.animate.scale(1.3).next_to(temp_tex[7:10], UP, buff=0.3))

        sr_z = SurroundingRectangle(zxi, color=YELLOW_C, buff=0.1)
        self.playw(FadeIn(sr_z), FadeOut(sr_px))

        ## indicate exp
        e1 = temp_tex[6]
        e2 = temp_tex[-5]
        self.play(FadeOut(VGroup(zxi, sr_z)))
        self.playw(
            Indicate(e1, scale_factor=1.05, color=PURE_BLUE),
            Indicate(e2, scale_factor=1.05, color=PURE_BLUE),
        )
        ## normalize
        frac_bar = temp_tex[12]
        denom = temp_tex[13:]
        self.playwl(
            Indicate(frac_bar, scale_factor=1.05, color=PURE_BLUE),
            Indicate(denom, scale_factor=1.05, color=PURE_BLUE),
            lag_ratio=0.5,
        )

        ## temperature T
        t1 = temp_tex[11]  # T in the numerator
        t2 = temp_tex[-1]  # T in the denominator
        rest = VGroup(temp_tex[:11], temp_tex[12:-1])
        self.playw(
            rest.animate.set_opacity(0.5),
            t1.animate.set_color(YELLOW_C),
            t2.animate.set_color(YELLOW_C),
        )

        ## gt0
        gt01 = Tex("> 0", font_size=36).next_to(t1, RIGHT, buff=0.1)
        gt02 = Tex("> 0", font_size=36).next_to(t2, RIGHT, buff=0.1)
        self.playw(FadeIn(gt01), FadeIn(gt02))

        ## camera
        self.cf.save_state()
        self.play(FadeOut(gt01), FadeOut(gt02), run_time=0.5)
        self.playw(
            self.cf.animate.reorient(86, 61, -86, (-0.25, 1.68, 0.79), 11.04),
            temp_tex.animate.to_corner(UR).shift(UP + IN + RIGHT * 0.75),
        )

        ## numberline nl * 3
        nl1 = NumberLine(x_range=(-5, 5), include_ticks=False)
        nl2 = NumberLine(x_range=(-5, 5), include_ticks=False)
        nl3 = NumberLine(x_range=(-5, 5), include_ticks=False)
        nls = VGroup(nl1, nl2, nl3).arrange(OUT, buff=3).shift(OUT * 3)
        nl1.shift(IN * 2.5)
        arr1 = (
            Arrow(start=nl1.get_right(), end=nl2.get_right(), buff=0.3, thickness=2)
            .shift(DOWN * 0.1)
            .set_color(GREY_C)
        )
        text1 = (
            Text("temperature", font_size=20, font=MONO_FONT)
            .next_to(arr1, DOWN, buff=0.05)
            .rotate(PI / 2, axis=UP)
            .set_color(GREY_C)
        )
        arr2 = (
            Arrow(start=nl2.get_right(), end=nl3.get_right(), buff=0.3, thickness=2)
            .shift(DOWN * 0.1)
            .set_color(GREY_C)
        )
        text2 = (
            Text("softmax()", font_size=20, font=MONO_FONT)
            .next_to(arr2, DOWN, buff=0.05)
            .rotate(PI / 2, axis=UP)
            .set_color(GREY_C)
        )

        len_nums = 9
        start_nums = [1.1, 0.5, -0.2, 3.2, 0.7, 0.5, 0.3, -0.1, 2.1]
        logit_nums = Group(*[ValueTracker(num) for num in start_nums])

        def logit_bars1(*nums):
            bars = VGroup(
                *[
                    Rectangle(width=0.2, height=abs(num))
                    .set_fill(opacity=1)
                    .set_stroke(width=1, color=GREY_C)
                    .move_to(nl1.n2p(i))
                    .align_to(nl1, DOWN if num >= 0 else UP)
                    for i, num in enumerate(nums, -len_nums // 2)
                ]
            )
            return bars.set_color_by_gradient(*raenim_colors(len_nums))

        lbars1 = logit_bars1(*[tracker.get_value() for tracker in logit_nums])
        temp = ValueTracker(1)

        def logit_bars2(*nums, temperature=1):
            bars = VGroup(
                *[
                    Rectangle(width=0.2, height=abs(num) / temperature)
                    .set_color(lbars1[i].get_color())
                    .set_fill(opacity=1)
                    .set_stroke(width=1, color=GREY_C)
                    .move_to(nl2.n2p(i))
                    .align_to(nl2, DOWN if num >= 0 else UP)
                    for i, num in enumerate(nums, -len_nums // 2)
                ]
            )
            return bars

        lbars2 = logit_bars2(
            *[tracker.get_value() for tracker in logit_nums],
            temperature=temp.get_value(),
        )

        def get_tempt(temperature: float):
            t = (
                Text(f"T = {temperature:.2f}", font_size=24, font=MONO_FONT)
                .next_to(text1, DOWN, buff=0.1)
                .rotate(PI / 2, axis=UP)
            )
            t[2:].set_color(YELLOW)
            return t

        tempt = get_tempt(temp.get_value())
        self.playw(
            FadeIn(nls[:2]),
            FadeIn(arr1),
            FadeIn(text1),
            FadeIn(lbars1),
            FadeIn(lbars2),
            FadeIn(tempt),
        )

        ## animate by temp.set_value
        lbars2.add_updater(
            lambda m: m.become(
                logit_bars2(
                    *[tracker.get_value() for tracker in logit_nums],
                    temperature=temp.get_value(),
                )
            )
        )
        tempt.add_updater(lambda m: m.become(get_tempt(temp.get_value())))

        self.play(temp.animate.set_value(3.5), run_time=2)
        lbars2.clear_updaters()
        tempt.clear_updaters()

        ## fadein nl3 and its corresponding arrow and text
        # nl3.rotate(PI/10, axis=UP)
        def softmax_robust(*nums, temperature=1):
            max_num = max(nums)
            exp_nums = [np.exp((num - max_num) / temperature) for num in nums]
            sum_exp_nums = sum(exp_nums)
            return [exp_num / sum_exp_nums for exp_num in exp_nums]

        def exp(*nums, temperature=1):
            return [np.exp(num / temperature) for num in nums]

        def logit_bars3(*nums, temperature=1):
            softmax_nums = softmax_robust(*nums, temperature=temperature)
            bars = VGroup(
                *[
                    Rectangle(width=0.2, height=abs(num))
                    .set_color(lbars1[i].get_color())
                    .set_fill(opacity=1)
                    .set_stroke(width=1, color=GREY_C)
                    .move_to(nl3.n2p(i))
                    .align_to(nl3, DOWN if num >= 0 else UP)
                    for i, num in enumerate(softmax_nums, -len_nums // 2)
                ]
            )
            return bars

        lbars3 = logit_bars3(
            *[tracker.get_value() for tracker in logit_nums],
            temperature=temp.get_value(),
        )
        self.play(FadeIn(nl3), FadeIn(arr2), FadeIn(text2), FadeIn(lbars3))
        self.cf.save_state()
        self.playw(self.cf.animate.reorient(88, 38, -86, (0.10, 1.47, 0.51), 11.04))

        ## bars[3] is highest
        lbars1.save_state()
        lbars2.save_state()
        lbars3.save_state()
        hbars1, h1rest = lbars1[3], lbars1[:3] + lbars1[4:]
        hbars2, h2rest = lbars2[3], lbars2[:3] + lbars2[4:]
        hbars3, h3rest = lbars3[3], lbars3[:3] + lbars3[4:]
        text_highest = Text("please", font_size=32).next_to(hbars1, UP)
        self.playw(
            VGroup(h1rest, h2rest, h3rest).animate.set_opacity(0.2),
            VGroup(hbars1, hbars2, hbars3).animate.set_color(YELLOW),
            FadeIn(text_highest),
        )
        ## indicate hbars2
        self.playw(Indicate(hbars2, color=PURE_RED, scale_factor=1.05))

        ## restore and indicate
        self.play(
            lbars3.animate.restore(),
        )
        self.playwl(
            *[
                item.animate(rate_func=there_and_back).shift(UP * 0.2).set_color(RED)
                for item in lbars3
            ],
            lag_ratio=0.2,
        )

        ## low temperature by animate
        self.play(
            Restore(self.cf),
            FadeOut(lbars3),
            FadeOut(nl3),
            FadeOut(arr2),
            FadeOut(text2),
            Restore(lbars2),
            Restore(lbars1),
            FadeOut(text_highest),
            run_time=0.5,
        )

        lbars2.add_updater(
            lambda m: m.become(
                logit_bars2(
                    *[tracker.get_value() for tracker in logit_nums],
                    temperature=temp.get_value(),
                )
            )
        )
        tempt.add_updater(lambda m: m.become(get_tempt(temp.get_value())))

        self.playw(temp.animate.set_value(0.5), run_time=4)
        lbars2.clear_updaters()
        tempt.clear_updaters()

        ## show lbars3 and arrow,
        lbars3 = logit_bars3(
            *[tracker.get_value() for tracker in logit_nums],
            temperature=temp.get_value(),
        )
        hbars1, h1rest = lbars1[3], lbars1[:3] + lbars1[4:]
        hbars2, h2rest = lbars2[3], lbars2[:3] + lbars2[4:]
        hbars3, h3rest = lbars3[3], lbars3[:3] + lbars3[4:]
        text_highest3 = Text("please", font_size=32).next_to(hbars3, UP)
        self.playw(
            FadeIn(lbars3),
            FadeIn(arr2),
            FadeIn(text2),
            FadeIn(nl3),
            VGroup(h1rest, h2rest).animate.set_opacity(0.1),
            h3rest.animate.set_color(PURE_RED),
            VGroup(hbars1, hbars2, hbars3).animate.set_color(YELLOW),
            FadeIn(text_highest3),
            self.cf.animate.reorient(83, 41, -84, (-1.44, 0.95, 1.88), 7.52),
        )


class temperatureMetaphor(InteractiveScene, Scene2D):
    def construct(self):
        temp = ValueTracker(1.0)
        bbox = BrownianBox(temp)
        self.add(bbox)
        self.wait(3)

        def get_text(temperature: float):
            return Text(f"Temperature: {temperature:.2f}", font_size=24)

        ttext = get_text(temp.get_value()).next_to(bbox, DOWN)
        self.playw(FadeIn(ttext))

        ## increase temperature
        ttext.add_updater(
            lambda m: m.become(get_text(temp.get_value()).next_to(bbox, DOWN))
        )

        self.playw(temp.animate.set_value(8.0), run_time=2)
        self.wait(2)

        ## camera shift right
        self.playw(self.cf.animate.shift(RIGHT * 3))

        ## words and probs
        words_list = "wow three 복싱 ... こんにちは ビール 演替".split(" ")
        words = (
            VGroup(*[Text(word, font_size=24) for word in words_list])
            .arrange(DOWN, buff=0.5, aligned_edge=RIGHT)
            .next_to(bbox, RIGHT, buff=1)
            .shift(UP * 0.5)
        )
        logit_list = [1.1, 5.1, -0.5, 0.3, 0.1, 0.2, -0.2]

        def softmax_robust(*nums, temperature):
            max_num = max(nums)
            exps = [math.exp((n - max_num) / temperature) for n in nums]
            sum_exps = sum(exps)
            return [e / sum_exps for e in exps]

        temp8_probs = softmax_robust(*logit_list, temperature=8)
        temp03_probs = softmax_robust(*logit_list, temperature=0.3)
        def get_prob_bars(probs):
            return VGroup(
                *[
                    Rectangle(width=p * 3, height=0.2, color=GREEN_B).next_to(
                        words[i], RIGHT, buff=0.2
                    )
                    for i, p in enumerate(probs)
                ]
            ).set_fill(opacity=1)
        prob_bars = get_prob_bars(temp8_probs)
        sr = SurroundingRectangle(VGroup(prob_bars, words), color=GREY_C, buff=0.3)
        self.playw(FadeIn(words), FadeIn(prob_bars), FadeIn(sr), wait=5)

        ## sample 5 times
        words_sampled = [
            [1, "three"],
            [2, "복싱"],
            [1, "three"],
            [0, "wow"],
            [-3, "こんにちは"],
        ]
        for i in range(5):
            sampled_word = (
                Text(words_sampled[i][1], font_size=24)
                .move_to(sr)
                .align(sr, RIGHT, buff=0.05)
                .add_background_rectangle(color=BLACK, opacity=0.4)
            )
            choosed = VGroup(words[words_sampled[i][0]], prob_bars[words_sampled[i][0]])
            rest = VGroup(
                *[words[j] for j in range(len(words)) if j != words_sampled[i][0]],
                *[
                    prob_bars[j]
                    for j in range(len(prob_bars))
                    if j != words_sampled[i][0]
                ],
            )
            choosed.save_state()
            rest.save_state()
            choosed.set_color(YELLOW)
            rest.set_opacity(0.2)
            self.play(
                sr.set_fill(opacity=0.5).animate.set_fill(opacity=0),
                sampled_word.animate(rate_func=rush_from).next_to(sr, RIGHT, buff=0.2),
                Restore(choosed),
                Restore(rest)
            )
            self.remove(sampled_word)
        self.wait(3.5)
        ## low temperature
        sr.add_updater(lambda m: m.surround(VGroup(prob_bars, words), buff=0.3))
        temp_probs = [ValueTracker(v) for v in temp8_probs]
        prob_bars.add_updater(
            lambda m: m.become(get_prob_bars([tp.get_value() for tp in temp_probs]))
        )
        self.playw(
            *[tp.animate.set_value(p) for tp, p in zip(temp_probs, temp03_probs)],
            temp.animate.set_value(0.3),
            wait=5.6
        )
        sr.clear_updaters()
        prob_bars.clear_updaters()

        self.embed()
        ## sample again, this time: all three
        words_sampled = [[1, "three"], [1, "three"], [1, "three"], [1, "three"]]
        for i in range(4):
            sampled_word = (
                Text(words_sampled[i][1], font_size=24)
                .move_to(sr)
                .align(sr, RIGHT, buff=0.05)
                .add_background_rectangle(color=BLACK, opacity=0.4)
            )
            choosed = VGroup(words[words_sampled[i][0]], prob_bars[words_sampled[i][0]])
            rest = VGroup(
                *[words[j] for j in range(len(words)) if j != words_sampled[i][0]],
                *[
                    prob_bars[j]
                    for j in range(len(prob_bars))
                    if j != words_sampled[i][0]
                ],
            )
            choosed.save_state()
            rest.save_state()
            choosed.set_color(YELLOW)
            rest.set_opacity(0.2)
            self.play(
                sr.set_fill(opacity=0.5).animate.set_fill(opacity=0),
                sampled_word.animate(rate_func=rush_from).next_to(sr, RIGHT, buff=0.2),
                Restore(choosed),
                Restore(rest)
            )
            self.remove(sampled_word)
        self.wait()