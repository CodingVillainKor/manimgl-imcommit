from manimlib import *
from raenimgl import *
from random import seed

import sys

sys.path.append("./")
from examples import *

seed(41)
np.random.seed(41)


def _is_letter(c: str) -> bool:
    o = ord(c)
    return (
        c.isascii()
        and c.isalpha()
        or 0x00C0 <= o <= 0x024F
        and o not in (0xD7, 0xF7)  # Latin accents (é, ñ, ü), minus × ÷
        or 0xAC00 <= o <= 0xD7A3  # Hangul syllables
        or 0x3131 <= o <= 0x318E  # Hangul jamo (ㄱ, ㅏ)
        or 0x3041 <= o <= 0x30FF  # Hiragana, Katakana
        or 0x4E00 <= o <= 0x9FFF  # CJK ideographs
        or 0x3400 <= o <= 0x4DBF  # CJK extension A
    )


def is_visual_token(tok: str, allow_punct: bool = False) -> bool:
    # Korean/Japanese/CJK/Latin letters only (+ spaces); drops �, symbols, code, other scripts
    if not any(_is_letter(c) for c in tok):
        return False
    extra = " " + ("0123456789.,!?'\"-:;()" if allow_punct else "")
    return all(_is_letter(c) or c in extra for c in tok)


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
        title_topp = (
            Text("Top-p", font_size=24).move_to(_a1).shift(UP * 2.7).set_color(GREY_B)
        )
        title_topk = (
            Text("Top-k", font_size=24).move_to(_a2).shift(UP * 2.7).set_color(GREY_B)
        )
        title_temp = (
            Text("Temperature", font_size=24)
            .move_to(_a3)
            .shift(UP * 2.7)
            .set_color(GREY_B)
        )
        self.addw(_line1, _line2, title_topp, title_topk, title_temp)

        ## top_p bar
        w = 3.5
        top_p_bar = (
            Rectangle(width=w, height=0.5).move_to(_a1).set_color(GREY_B).set_opacity(0)
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
        probs = VGroup()
        prob_num = 0
        for i, p in enumerate(
            [0.4, 0.2, 0.15, 0.12, 0.05, 0.04, 0.008, 0.006, 0.006] + [0.004] * 5
        ):
            if prob_num < 0.9:
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
                prob.next_to(probs[-1], RIGHT, buff=0)
            prob.set_fill(opacity=opacity)
            probs.add(prob)

        self.add(top_p_bar, probs)
        self.playw(
            FadeIn(topp_90b),
            FadeIn(topp_90b_text),
            FadeIn(line_90),
            FadeIn(total_b),
            FadeIn(total_text),
        )

        ## top_k bar
        top_k_bar = Rectangle(width=w, height=0.5).move_to(_a2).set_color(GREY_B)
        k = 3
        probs = VGroup()
        prob_num = 0
        for i, p in enumerate(
            [0.4, 0.2, 0.15, 0.12, 0.05, 0.04, 0.008, 0.006, 0.006] + [0.004] * 5
        ):
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
            prob_num += p
            if i == 0:
                prob.align_to(top_k_bar, LEFT)
            else:
                prob.next_to(probs[-1], RIGHT, buff=0)
            prob.set_fill(opacity=opacity)
            probs.add(prob)

        top_k_text = (
            Text("Top 3", font_size=18, font=MONO_FONT)
            .next_to(probs[:3], UP, buff=0.75)
            .set_color(YELLOW_B)
        )
        top_k_lines = VGroup(
            *[DashedLine(top_k_text, prob.get_top()) for prob in probs[:3]]
        ).set_color(YELLOW_B)
        self.playw(
            FadeIn(top_k_text), FadeIn(top_k_lines), FadeIn(top_k_bar), FadeIn(probs)
        )

        ## temperature

        word_bars = VGroup()
        prob_list = [0.4, 0.2, 0.15, 0.12, 0.05, 0.04, 0.008, 0.006, 0.006] + [
            0.004
        ] * 5
        denom = 50
        logit_list = [math.log(p * denom) for p in prob_list]
        for i, p in enumerate(prob_list):
            bar = (
                Rectangle(height=w * p, width=0.2)
                .set_stroke(width=1)
                .set_fill(BLUE_A, opacity=0.3)
            )
            word_bars.add(bar)
        # word_bars.shuffle()
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
            prob_list = softmax_robust(logit_list, temp.get_value())
            for i, bar in enumerate(mob):
                bar.stretch_to_fit_height(w * prob_list[i]).align_to(
                    _word_bars[i], DOWN
                )

        word_bars.add_updater(update_word_bars)
        temp_value.add_updater(update_temp_value)

        self.play(temp.animate.set_value(5.0), run_time=2)
        self.playw(temp.animate.set_value(0.3), run_time=2)


class LLMOutput(InteractiveScene, Scene2D):
    def construct(self):

        ## llm
        llm_box = (
            Rectangle(width=4, height=2)
            .set_color(BLUE_A)
            .set_stroke(width=2)
            .set_fill(BLACK, opacity=0.7)
        )
        llm_text = (
            Text("LLM", font_size=20).align(llm_box, UR, buff=0.05).set_color(GREY_B)
        )
        llm = VGroup(llm_box, llm_text).set_z_index(1)

        text = Words("[assistant] ... [user] piui가 뭔가요? [assistant]", font_size=18)
        for w in text.words:
            w.rotate(PI / 2)
        text.words.arrange(RIGHT, aligned_edge=UP).next_to(llm, DOWN, buff=0.3).align(
            llm, LEFT, buff=0.3
        )

        latent = (
            Tensor(len(text.words), arrange=RIGHT)
            .scale(0.85)
            .move_to(llm)
            .align(llm, LEFT, buff=0.3)
        )
        input_lines = VGroup(
            *[
                DashedLine(start=w.get_top(), end=l.get_bottom())
                for w, l in zip(text.words, latent)
            ]
        )

        output = (
            Tensor(1).scale(0.85).next_to(llm, UP, buff=0.3).align_to(latent[-1], LEFT)
        )
        output_lines = VGroup(
            *[DashedLine(start=l.get_top(), end=output.get_bottom()) for l in latent]
        )

        self.add(llm, text, latent, input_lines, output, output_lines)

        ## output probs

        def get_prob_tag(prob, text: str):
            prob = DecimalNumber(prob, num_decimal_places=2, font_size=18)
            t = Text(text, font_size=18)
            box = SurroundingRectangle(
                VGroup(prob, t).arrange(RIGHT, buff=0.15), color=GREY_B, buff=0.1
            )
            return VGroup(prob, t, box)

        prob_tags = VGroup()
        for prob, text in zip(
            [0.3, 0.4, 0.2, 0.1], ["token1", "token2", "token3", "..."]
        ):
            prob_tags.add(get_prob_tag(prob, text))
        prob_tags[0].rotate(3 * PI / 4).next_to(output, UP).shift(LEFT * 1.5)
        prob_tags[1].rotate(2 * PI / 3).next_to(prob_tags[0], RIGHT, buff=-0.1).shift(
            UP * 0.5
        )
        prob_tags[2].rotate(PI / 3).next_to(prob_tags[1], RIGHT, buff=0.2)
        prob_tags[3].rotate(PI / 4).next_to(
            prob_tags[2], RIGHT, buff=-0.3, aligned_edge=DOWN
        ).shift(DOWN * 0.5)

        prob_lines = VGroup(
            DashedLine(start=output.get_top(), end=prob_tags[0]),
            DashedLine(start=output.get_top(), end=prob_tags[1]),
            DashedLine(start=output.get_top(), end=prob_tags[2]),
            DashedLine(start=output.get_top(), end=prob_tags[3]),
        )
        pl0, pl1, pl2, pl3 = prob_lines

        self.addw(prob_tags, pl0, pl1, pl2, pl3)

        ## RWiggle
        pl0.add_updater(
            lambda m: m.become(DashedLine(start=output.get_top(), end=prob_tags[0]))
        )
        pl1.add_updater(
            lambda m: m.become(DashedLine(start=output.get_top(), end=prob_tags[1]))
        )
        pl2.add_updater(
            lambda m: m.become(DashedLine(start=output.get_top(), end=prob_tags[2]))
        )
        pl3.add_updater(
            lambda m: m.become(DashedLine(start=output.get_top(), end=prob_tags[3]))
        )

        self.playw(*[RWiggle(pt, amp=0.2, speed=2) for pt in prob_tags], run_time=4)


class LLMOutputProbs(InteractiveScene, Scene2D):
    def construct(self):

        ## prepare

        ## llm
        llm_box = (
            Rectangle(width=4, height=2)
            .set_color(BLUE_A)
            .set_stroke(width=2)
            .set_fill(BLACK, opacity=0.7)
        )
        llm_text = (
            Text("LLM", font_size=20).align(llm_box, UR, buff=0.05).set_color(GREY_B)
        )
        llm = VGroup(llm_box, llm_text).set_z_index(1)

        text = Words("[assistant] ... [user] piui가 뭔가요? [assistant]", font_size=18)
        for w in text.words:
            w.rotate(PI / 2)
        text.words.arrange(RIGHT, aligned_edge=UP).next_to(llm, DOWN, buff=0.3).align(
            llm, LEFT, buff=0.3
        )

        latent = (
            Tensor(len(text.words), arrange=RIGHT)
            .scale(0.85)
            .move_to(llm)
            .align(llm, LEFT, buff=0.3)
        )
        input_lines = VGroup(
            *[
                DashedLine(start=w.get_top(), end=l.get_bottom())
                for w, l in zip(text.words, latent)
            ]
        )

        output = (
            Tensor(1).scale(0.85).next_to(llm, UP, buff=0.3).align_to(latent[-1], LEFT)
        )
        output_lines = VGroup(
            *[DashedLine(start=l.get_top(), end=output.get_bottom()) for l in latent]
        )

        self.addw(llm, text, latent, input_lines, output, output_lines)

        ## vocab indices

        vocabs_list = [t for t in vocab() if is_visual_token(t)][1100:1400]
        vocabs = VGroup(
            *[Words(f"{i}: {t}", font_size=24) for i, t in enumerate(vocabs_list, 1100)]
        ).arrange_in_grid(n_rows=20, n_cols=15, buff=0.05, aligned_edge=LEFT)
        vocabs.next_to(output, UP)
        self.cf.save_state()
        self.playwl(
            FadeIn(vocabs),
            self.cf.animate.reorient(
                -27, 44, 0, (np.float32(-0.35), np.float32(3.63), np.float32(0.2)), 2.81
            ),
            lag_ratio=0.3,
        )

        ## numbers
        nums = VGroup(*[ws.words[0][:-1] for ws in vocabs])
        rest = VGroup(*[ws.words[1:] for ws in vocabs])
        self.playw(nums.animate.set_color(GREEN), rest.animate.set_color(GREY_D))

        ## RWiggle numbers
        self.playw(*[RWiggle(num, amp=0.05, speed=2) for num in nums], run_time=1.5)

        ## restore camera, Wo
        Wo = (
            Tex("W_o", font_size=24)
            .add_background_rectangle()
            .set_z_index(2)
            .next_to(latent[-1], UP)
            .align(llm, UP, buff=0.1)
        )
        self.add(Wo)
        self.playw(self.cf.animate.restore(), FadeOut(vocabs))

        ## wo to UR
        self.play(Wo.animate.shift(UR + RIGHT * 0.3))
        r, w = 5, 9
        eq = Text("=", font_size=20).next_to(Wo, RIGHT, buff=0.1)
        mat_Wo = randn(r, w).scale(0.22).next_to(eq, RIGHT, buff=0.1)
        for i in range(r * w):
            if i % w == w // 2:
                mat_Wo[i].become(Text("...", font_size=18).move_to(mat_Wo[i]))
            elif (w * (r // 2)) <= i < (w * (r // 2 + 1)):
                mat_Wo[i].become(Text("...", font_size=18).move_to(mat_Wo[i]))
        d_brace = Brace(mat_Wo, RIGHT, buff=0.05)
        d_text = d_brace.get_text("D", font_size=20)
        v_brace = Brace(mat_Wo, UP)
        v_text = v_brace.get_text("V", font_size=20)
        self.playw(
            FadeIn(eq),
            FadeIn(mat_Wo),
            FadeIn(d_brace),
            FadeIn(d_text),
            FadeIn(v_brace),
            FadeIn(v_text),
        )

        ## FadeOut(ds)
        self.play(Circumscribe(d_text, color=RED), run_time=0.75)
        self.playw(FadeOut(d_brace), FadeOut(d_text), run_time=0.75)

        ## V is important
        for i in range(3):
            self.playw(
                Circumscribe(v_text, color=YELLOW),
                run_time=0.5,
                wait=1 if i == 2 else 0,
            )

        ## fadeout mat, Wo and nums
        n_nums = 41
        nums = randn(1, n_nums).scale(0.3).next_to(output, UP)
        nums[n_nums // 2].become(Text("...", font_size=18).move_to(nums[n_nums // 2]))
        self.playwl(
            AnimationGroup(
                FadeOut(mat_Wo),
                FadeOut(eq),
                FadeOut(v_brace),
                FadeOut(v_text),
                FadeOut(Wo),
            ),
            FadeIn(nums, shift=nums.get_center() - output.get_center(), scale=40),
            lag_ratio=0.3,
        )

        ## z_i texts
        texs = VGroup(
            *[
                Tex("z_{" + str(idx) + "}", font_size=24).next_to(nums[i], UP)
                for i, idx in enumerate(range(1536, 1536 + n_nums))
            ]
        ).set_color(YELLOW_B)
        texs[n_nums // 2].become(Text("...", font_size=18).move_to(texs[n_nums // 2]))
        self.playwl(*[FadeIn(tex, run_time=0.25) for tex in texs], lag_ratio=0.85)

        ## negative nums in nums to be red
        nval = nums.val
        neg_idx = [i for i, val in enumerate(nval[0]) if val < 0]
        nonneg_idx = [i for i, val in enumerate(nval[0]) if val >= 0]
        self.play(
            *[nums[i].animate.set_color(RED) for i in neg_idx],
            *[nums[i].animate.set_color(GREY_C) for i in nonneg_idx],
        )
        self.playw(
            *[
                nums[i].animate(rate_func=there_and_back).shift(DOWN * 0.2)
                for i in neg_idx
            ],
            wait=3,
        )

        ## argmax_idx
        argmax_idx = nval[0].argmax()
        self.play(nums[argmax_idx].animate.set_color(GREEN))
        for i in range(3):
            self.play(Circumscribe(nums[argmax_idx], color=GREEN), run_time=0.75)
        ## word
        word = (
            Words(vocabs_list[36], font_size=32)
            .set_color(GREEN)
            .next_to(texs[argmax_idx], UP)
        )
        self.playw(FadeIn(word, shift=UP * 0.5))

        ## prob_lines
        prob_lines = VGroup(
            *[
                Line(start=output.get_top(), end=nums[i].get_bottom(), stroke_width=2)
                for i in range(n_nums)
            ]
        ).set_opacity(0.5)
        self.playw(FadeIn(prob_lines), wait=4)

        ## sum(nums) by Joiner
        nums.save_state()
        self.cf.save_state()
        nums.generate_target()
        sum_nums = (
            Joiner(*nums.target, join=lambda: Text("+", font_size=20))
            .arrange(RIGHT, buff=0.05)
            .add_background_rectangle()
            .next_to(texs, UP, buff=1.5)
        )

        self.playwl(
            MoveToTarget(nums),
            self.cf.animate.reorient(
                -90,
                46,
                90,
                (np.float32(-5.01), np.float32(4.08), np.float32(-2.64)),
                8.52,
            ),
            FadeIn(sum_nums[2::2]),
            lag_ratio=0.3,
        )

        ## lagged circumscribe negative numbers
        self.playwl(
            *[FlashUnder(nums[i], color=RED, buff=0.05) for i in neg_idx],
            lag_ratio=0.1,
        )

        ## restore nums state
        self.playwl(Restore(nums), Restore(self.cf), FadeOut(sum_nums[2::2]))


class whatisSoftmax(InteractiveScene, Scene2D):
    def construct(self):

        ## logits
        logit_nums_list = np.random.randn(1, 11) * 1.5
        logit_nums_list[0, 2] = -1.61
        logit_nums_list[0, 4] = 0
        logit_nums_list[0, 7] = 5.15
        logits = (
            DecimalMatrix(logit_nums_list, num_decimal_places=2)
            .scale(0.4)
            .shift(DOWN * 0.75)
        )
        n_logits = logit_nums_list.shape[1]
        logits[n_logits // 2].become(
            Text("...", font_size=24).move_to(logits[n_logits // 2])
        )

        def get_bars(logits_input, logits_input_nums):
            _line = (
                NumberLine(x_range=[0, n_logits], width=10)
                .next_to(logits_input, UP, buff=0.7)
                .set_opacity(0.3)
            )
            _line.ticks.set_opacity(0)
            logit_nums = logits_input_nums[0]
            h1 = 0.8
            bars = VGroup(
                *[
                    Rectangle(
                        width=0.2, height=h1 * abs(logit_nums[i]) * 0.4, stroke_width=1
                    )
                    .set_fill(opacity=1)
                    .next_to(logits[i], UP)
                    .align_to(_line.get_center(), DOWN if logit_nums[i] >= 0 else UP)
                    for i in range(n_logits)
                ]
            )
            bars[n_logits // 2].set_opacity(0)
            for i in range(n_logits):
                if logit_nums[i] < 0:
                    bars[i].set_color(RED)

            return bars, _line

        bars, _line = get_bars(logits, logit_nums_list)
        self.addw(logits, bars, _line)

        ## exp
        exp_l = Text("exp(", font_size=24).next_to(logits, LEFT, buff=0.1)
        exp_r = Text(")", font_size=24).next_to(logits, RIGHT, buff=0.1)
        exp = VGroup(exp_l, exp_r).set_color(YELLOW)

        exp_logit_nums_list = np.exp(logit_nums_list)
        exp_logits = (
            DecimalMatrix(exp_logit_nums_list, num_decimal_places=2)
            .scale(0.4)
            .shift(DOWN * 0.75)
            .stretch_to_fit_width(logits.get_width())
        )
        logit_bars, _ = get_bars(exp_logits, exp_logit_nums_list)
        self.play(FadeIn(exp))
        self.cf.save_state()
        self.playw(
            Transformr(logits, exp_logits),
            Transformr(bars, logit_bars, run_time=3),
            self.cf.animate.reorient(
                0, 66, 0, (np.float32(-0.36), np.float32(0.31), np.float32(0.79)), 6.56
            ),
            FadeOut(exp),
        )

        ## normalize
        sum_exp = np.sum(exp_logit_nums_list)

        norm_sum_exp = VGroup(
            *[
                Tex(
                    f"\\frac{{{exp_logit_nums_list[0, i]:.2f}}}{{{sum_exp:.2f}}}",
                    font_size=24,
                )
                for i in range(n_logits)
            ]
        )
        norm_mat = (
            MobjectMatrix(norm_sum_exp, n_rows=1, n_cols=n_logits)
            .scale(0.095)
            .shift(DOWN * 0.75)
        )
        norm_nums_list = [
            [exp_logit_nums_list[0, i] / sum_exp for i in range(n_logits)]
        ]
        norm_bars, _ = get_bars(norm_mat, norm_nums_list)
        self.play(
            Transformr(exp_logits[-2:], norm_mat[-2:]),
            FadeIn(VGroup(*[norm_mat[i][-7:] for i in range(len(norm_mat) - 2)])),
            *[
                FadeTransform(exp_logits[i], norm_mat[i][:-7])
                for i in range(len(exp_logits) - 2)
            ],
        )
        self.play(Transformr(logit_bars, norm_bars), run_time=2)
        self.playw(Restore(self.cf))

        ## sum = 1
        sum_l = Text("sum(", font_size=24).next_to(norm_mat, LEFT, buff=0.1)
        sum_r = Text(") = 1", font_size=24).next_to(norm_mat, RIGHT, buff=0.1)
        sum_text = VGroup(sum_l, sum_r).set_color(BLUE)
        self.play(FadeIn(sum_text))


class LLMSampling(InteractiveScene, Scene2D):
    def construct(self):

        ## llm
        llm_box = (
            Rectangle(width=4, height=2)
            .set_color(BLUE_A)
            .set_stroke(width=2)
            .set_fill(BLACK, opacity=0.7)
        )
        llm_text = (
            Text("LLM", font_size=20).align(llm_box, UR, buff=0.05).set_color(GREY_B)
        )
        llm = VGroup(llm_box, llm_text).set_z_index(1)

        text = Words("[assistant] ... [user] piui가 뭔가요? [assistant]", font_size=18)
        for w in text.words:
            w.rotate(PI / 2)
        text.words.arrange(RIGHT, aligned_edge=UP).next_to(llm, DOWN, buff=0.3).align(
            llm, LEFT, buff=0.3
        )

        latent = (
            Tensor(len(text.words), arrange=RIGHT)
            .scale(0.85)
            .move_to(llm)
            .align(llm, LEFT, buff=0.3)
        )
        input_lines = VGroup(
            *[
                DashedLine(start=w.get_top(), end=l.get_bottom())
                for w, l in zip(text.words, latent)
            ]
        )
        output_list = np.array(
            [-0.3, 0.54, 5.9, -0.1, 4.54, 1.3, 1.2, -0.5, 3.7, 0.7, 1.8]
        )[None, :]
        yellow_idx = [2, 4, 8]
        output = (
            DecimalMatrix(output_list, num_decimal_places=2)
            .scale(0.3)
            .next_to(llm, UP, buff=0.5)
            .shift(RIGHT * 0.61)
            .add_background_rectangle(
                stroke_width=1, buff=0.1, stroke_color=WHITE, stroke_opacity=1
            )
        )
        output[6].become(Text("...", font_size=18).move_to(output[6]))
        output_lines = VGroup(
            *[DashedLine(start=l.get_top(), end=output.get_bottom()) for l in latent]
        )

        softmax = (
            Text("softmax()", font=MONO_FONT, font_size=24)
            .add_background_rectangle(
                stroke_width=1, buff=0.1, stroke_color=WHITE, stroke_opacity=1
            )
            .next_to(output, UP, buff=0.3)
        )
        softmax_input_line = Line(start=output.get_top(), end=softmax.get_bottom())
        ov = output_list

        def softmax_robust(x):
            e_x = np.exp(x - np.max(x))
            return e_x / e_x.sum()

        softmax_val = softmax_robust(ov)
        softmax_output = (
            DecimalMatrix(softmax_val, num_decimal_places=2)
            .scale(0.35)
            .next_to(softmax, UP, buff=0.3)
        )
        softmax_output[5].become(Text("...", font_size=18).move_to(softmax_output[5]))
        for i in yellow_idx:
            softmax_output[i].set_color(YELLOW)
        softmax_output_line = Line(
            start=softmax.get_top(), end=softmax_output.get_bottom()
        )

        self.addw(llm, text, latent, input_lines, output, output_lines)
        self.addw(softmax, softmax_input_line)
        self.addw(softmax_output, softmax_output_line)

        ## circumscribe softmax_output
        self.playw(Circumscribe(softmax_output), run_time=0.75)

        ## pop [2]
        self.playw(
            softmax_output[2]
            .animate(rate_func=there_and_back)
            .shift(UP * 0.5)
            .set_color(RED),
            run_time=0.75,
        )

        ## pop yellow idx samples
        self.playwl(
            *[
                softmax_output[i]
                .animate(rate_func=there_and_back)
                .shift(UP * 0.5)
                .set_color(RED)
                for i in yellow_idx
            ],
            lag_ratio=0.5,
        )

        ## circumscribe [2]
        self.playw(Circumscribe(softmax_output[2]), run_time=0.75)

        ## circumscribe input - question
        self.playwl(
            Circumscribe(text.words[-3]), Circumscribe(text.words[-2]), lag_ratio=0.5
        )

        ## "pi", "지금부터", "웹"
        t1 = (
            Text('"pi"', font_size=20)
            .next_to(softmax_output[2], UP, buff=0.1)
            .set_color(YELLOW)
        )
        t2 = (
            Text('"지금부터"', font_size=20)
            .next_to(softmax_output[4], UP, buff=0.1)
            .set_color(YELLOW)
        )
        t3 = (
            Text('"웹"', font_size=20)
            .next_to(softmax_output[8], UP, buff=0.1)
            .set_color(YELLOW)
        )
        self.playwl(
            FadeIn(t1, shift=UP * 0.2),
            FadeIn(t2, shift=UP * 0.2),
            FadeIn(t3, shift=UP * 0.2),
            lag_ratio=0.5,
        )

        ## camera tilt
        self.cf.save_state()
        t1.save_state()
        t2.save_state()
        t3.save_state()
        t1t = t1.generate_target()
        t2t = t2.generate_target()
        t3t = t3.generate_target()
        t1t.rotate(PI / 2).rotate(-62 * DEGREES, axis=RIGHT).align_to(t1, OUT).shift(
            IN * 0.1
        )
        t2t.rotate(PI / 2).rotate(-62 * DEGREES, axis=RIGHT).align_to(t2, OUT).shift(
            IN * 0.1
        )
        t3t.rotate(PI / 2).rotate(-62 * DEGREES, axis=RIGHT).align_to(t3, OUT).shift(
            IN * 0.1
        )
        self.play(
            self.cf.animate.reorient(
                -179,
                62,
                -179,
                (np.float32(0.68), np.float32(0.86), np.float32(-1.47)),
                8.00,
            ),
            MoveToTarget(t1),
            MoveToTarget(t2),
            MoveToTarget(t3),
        )

        ## piui가 뭐냐면
        DIRECTION = IN * np.cos(62 * DEGREES) + UP * np.sin(62 * DEGREES)
        t1_ = (
            Text("ui가 뭐냐면...", font_size=20)
            .rotate(PI / 2)
            .rotate(-62 * DEGREES, axis=RIGHT)
            .next_to(t1[-2], DIRECTION, buff=0.05)
            .set_color(GREY_C)
        )
        self.play(
            FadeIn(t1_, shift=IN * 0.2),
            t1[-1].animate.next_to(t1_, DIRECTION, buff=0.05, aligned_edge=LEFT),
        )

        t2_ = (
            Text("piui에 대해 ...", font_size=20)
            .rotate(PI / 2)
            .rotate(-62 * DEGREES, axis=RIGHT)
            .next_to(t2[-2], DIRECTION, buff=0.15)
            .set_color(GREY_C)
        )
        self.play(
            FadeIn(t2_, shift=IN * 0.2),
            t2[-1].animate.next_to(t2_, DIRECTION, buff=0.05, aligned_edge=LEFT),
        )

        t3_ = (
            Text(" 검색을 통해 ...", font_size=20)
            .rotate(PI / 2)
            .rotate(-62 * DEGREES, axis=RIGHT)
            .next_to(t3[-2], DIRECTION, buff=0.15)
            .set_color(GREY_C)
        )
        self.playw(
            FadeIn(t3_, shift=IN * 0.2),
            t3[-1].animate.next_to(t3_, DIRECTION, buff=0.05, aligned_edge=LEFT),
        )

        ## restore camera
        self.play(self.cf.animate.restore())
        self.playw(
            t1.animate.restore(),
            t2.animate.restore(),
            t3.animate.restore(),
            FadeOut(t1_, shift=IN * 0.2),
            FadeOut(t2_, shift=IN * 0.2),
            FadeOut(t3_, shift=IN * 0.2),
        )

        ## circumscribe [2] again
        self.play(Circumscribe(VGroup(softmax_output[2], t1)), run_time=0.75)
        self.play(Circumscribe(VGroup(softmax_output[2], t1)), run_time=0.75)
        self.playw(Circumscribe(VGroup(softmax_output[2], t1)), run_time=0.75)

        ## t1 is new input[-1]
        t1_in = t1[1:-1]
        self.play(
            t1_in.animate.rotate(PI / 2).next_to(
                text.words[-1], RIGHT, aligned_edge=UP
            ),
            FadeOut(
                VGroup(
                    output,
                    softmax_input_line,
                    softmax_output,
                    softmax_output_line,
                    softmax,
                    t1[0],
                    t1[-1],
                    t2,
                    t3,
                    output_lines,
                )
            ),
        )
        l1 = Tensor(1).scale(0.85).next_to(latent, RIGHT, buff=0.085)
        t1_in_line = DashedLine(t1_in.get_top(), l1.get_bottom())
        self.play(Create(t1_in_line), run_time=0.5)
        self.play(FadeIn(l1), run_time=0.5)
        t1_out_line = DashedLine(l1.get_top(), t1_in.get_bottom())
        latent.add(l1)

        output_list = np.array(
            [1.3, 9.1, 1.1, -1.65, -3, 1.12, 0.51, 0.88, -3.1, -0.6, 1.1]
        )[None, :]
        yellow_idx = [2, 4, 8]
        output = (
            DecimalMatrix(output_list, num_decimal_places=2)
            .scale(0.3)
            .next_to(llm, UP, buff=0.5)
            .shift(RIGHT * 1.05)
            .add_background_rectangle(
                stroke_width=1, buff=0.1, stroke_color=WHITE, stroke_opacity=1
            )
        )
        output[2].set_color(YELLOW)
        output[6].become(Text("...", font_size=18).move_to(output[6]))
        output_lines = VGroup(
            *[DashedLine(start=l.get_top(), end=output.get_bottom()) for l in latent]
        )
        self.playw(
            FadeIn(output_lines),
            FadeIn(output),
        )

        ui = Text('"ui"', font_size=20).next_to(output[2], UP).set_color(YELLOW)
        self.playw(FadeIn(ui, shift=UP * 0.2))

        ## ui to "에"
        t2_in = ui[1:-1]
        self.play(
            t2_in.animate.rotate(PI / 2).next_to(t1_in, RIGHT, aligned_edge=UP),
            FadeOut(VGroup(ui[0], ui[-1], output, output_lines)),
        )
        l2 = Tensor(1).scale(0.85).next_to(l1, RIGHT, buff=0.085)
        t2_in_line = DashedLine(t2_in.get_top(), l2.get_bottom())
        self.play(Create(t2_in_line), run_time=0.5)
        self.play(FadeIn(l2), run_time=0.5)
        t2_out_line = DashedLine(l2.get_top(), t2_in.get_bottom())
        latent.add(l2)

        output_list = np.array(
            [-2.15, 3.7, -1.6, 0.37, -2.3, 0.55, 3.6, 4.5, -0.53, -0.17, 1.3]
        )[None, :]
        output = (
            DecimalMatrix(output_list, num_decimal_places=2)
            .scale(0.3)
            .next_to(llm, UP, buff=0.5)
            .shift(RIGHT * 1.45)
            .add_background_rectangle(
                stroke_width=1, buff=0.1, stroke_color=WHITE, stroke_opacity=1
            )
        )
        output[8].set_color(YELLOW)
        output[6].become(Text("...", font_size=18).move_to(output[6]))
        output_lines = VGroup(
            *[DashedLine(start=l.get_top(), end=output.get_bottom()) for l in latent]
        )
        self.playw(
            FadeIn(output_lines),
            FadeIn(output),
        )

        e = Text('"에"', font_size=20).next_to(output[8], UP).set_color(YELLOW)
        self.playw(FadeIn(e, shift=UP * 0.2))

        self.embed()
        ## "에" to "대해서"
        t3_in = e[1:-1]
        llm_box.generate_target()
        llm_box.target.stretch_to_fit_width(llm_box.get_width() * 1.1).align_to(
            llm_box, LEFT
        )
        self.play(
            t3_in.animate.rotate(PI / 2).next_to(t2_in, RIGHT, aligned_edge=UP),
            FadeOut(VGroup(e[0], e[-1])),
            MoveToTarget(llm_box),
            llm_text.animate.align(llm_box.target, UR, buff=0.05),
            FadeOut(VGroup(output, output_lines)),
        )
        l3 = Tensor(1).scale(0.85).next_to(l2, RIGHT, buff=0.085)
        t3_in_line = DashedLine(t3_in.get_top(), l3.get_bottom())
        self.play(Create(t3_in_line), run_time=0.5)
        self.play(FadeIn(l3), run_time=0.5)

        latent.add(l3)

        output_list = np.array(
            [0.13, 0.27, -0.45, 11.2, -0.33, 0.88, -1.1, 0.56, 0.99, -0.67, 0.42]
        )[None, :]
        output = (
            DecimalMatrix(output_list, num_decimal_places=2)
            .scale(0.3)
            .next_to(llm, UP, buff=0.5)
            .shift(RIGHT * 1.85)
            .add_background_rectangle(
                stroke_width=1, buff=0.1, stroke_color=WHITE, stroke_opacity=1
            )
        )
        output[4].set_color(YELLOW)
        output[6].become(Text("...", font_size=18).move_to(output[6]))
        output_lines = VGroup(
            *[DashedLine(start=l.get_top(), end=output.get_bottom()) for l in latent]
        )
        self.playw(
            FadeIn(output_lines),
            FadeIn(output),
        )
        d = Text('"대해서"', font_size=20).next_to(output[4], UP).set_color(YELLOW)
        self.playw(FadeIn(d, shift=UP * 0.2))

