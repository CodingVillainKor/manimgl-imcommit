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
            self.cf.animate.reorient(-90, 46, 90, (np.float32(-5.01), np.float32(4.08), np.float32(-2.64)), 8.52),
            FadeIn(sum_nums[2::2]),
            lag_ratio=0.3,
        )

        ## lagged circumscribe negative numbers
        self.playwl(
            *[
                FlashUnder(nums[i], color=RED, buff=0.05)
                for i in neg_idx
            ],
            lag_ratio=0.1,
        )

        self.embed()
        ## restore nums state
        self.playwl(Restore(nums), Restore(self.cf), FadeOut(sum_nums[2::2]))