from manimlib import *
from raenimgl import *
from random import seed, shuffle

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        string = "Got it, let me start by\nexploring the code and implementing."
        text = Words(string, font_size=36, font=MONO_FONT).set_color(ORANGE)
        self.playwl(*[FadeIn(w) for w in text.words], lag_ratio=0.1)

        idxs = list(range(len(text)))
        shuffle(idxs)
        idxs = sorted(idxs[:6])
        upside_idx = 17

        arrows = VGroup()
        unicodes = VGroup()
        for idx in idxs:
            if idx > upside_idx:
                arrow = Arrow(
                    text[idx].get_bottom() + 0.75 * DOWN,
                    text[idx].get_bottom(),
                    thickness=2,
                    buff=0,
                ).set_color(RED)
                arrow.align_to(text[idx], LEFT).shift(LEFT * 0.5 * arrow.get_width())
                ucode = (
                    Text("U+2009", font_size=18, font=MONO_FONT)
                    .next_to(arrow, DOWN)
                    .set_color(RED)
                )
            else:
                arrow = Arrow(
                    text[idx].get_top() + 0.75 * UP,
                    text[idx].get_top(),
                    thickness=2,
                    buff=0,
                ).set_color(RED)
                arrow.align_to(text[idx], LEFT).shift(LEFT * 0.5 * arrow.get_width())
                ucode = (
                    Text("U+2009", font_size=18, font=MONO_FONT)
                    .next_to(arrow, UP)
                    .set_color(RED)
                )
            arrows.add(arrow)
            unicodes.add(ucode)
        self.playw(
            *[
                AnimationGroup(GrowArrow(arrow), FadeIn(ucode))
                for arrow, ucode in zip(arrows, unicodes)
            ],
            lag_ratio=0.3,
            wait=2,
        )

        ## sweep out the arrows and unicodes
        items = VGroup(*[VGroup(arr, ucode) for arr, ucode in zip(arrows, unicodes)])
        itt = items.generate_target()
        for item in itt:
            c = item.get_center()
            direction = (c - ORIGIN) / np.linalg.norm(c - ORIGIN)
            item.shift(direction * 7).rotate(PI / 2 * random.random())
        self.playw(MoveToTarget(items), run_time=1.3)


class scoreFunction(InteractiveScene, Scene2D):
    def construct(self):

        ## score function

        score_fn_tex = Tex("\\text{g}()", font_size=40).set_color(BLUE)
        score_box = SurroundingRectangle(score_fn_tex, color=BLUE, buff=0.3)
        score_fn = VGroup(score_box, score_fn_tex)
        self.playw(FadeIn(score_fn_tex), Create(score_box))

        ## arrows
        input_arrow = Arrow(
            score_fn.get_left() + 0.9 * LEFT, score_fn.get_left(), thickness=2, buff=0.1
        ).set_color(BLUE)

        output_arrow = Arrow(
            score_fn.get_right(),
            score_fn.get_right() + 0.9 * RIGHT,
            thickness=2,
            buff=0.1,
        ).set_color(BLUE)

        self.playwl(GrowArrow(input_arrow), GrowArrow(output_arrow), lag_ratio=0.5)

        ## text frags are input

        text_frags = Words(
            "exploring the code", font_size=28, font=MONO_FONT
        ).set_color(ORANGE)
        text_frags.words.arrange(RIGHT, buff=0.5)
        frag_boxes = VGroup(
            *[SurroundingRectangle(w, color=ORANGE, buff=0.2) for w in text_frags.words]
        ).set_opacity(0.15)
        text_input = VGroup(text_frags, frag_boxes).next_to(input_arrow, LEFT, buff=0.3)
        box_input = SurroundingRectangle(text_input, color=ORANGE, buff=0.2)
        self.play(FadeIn(text_input))
        self.playw(Create(box_input))

        ## full text
        string = "Got it, let me start by exploring the code and implementing."
        full_text = Words(string, font_size=24, font=MONO_FONT).set_color(ORANGE)
        full_text.next_to(text_input, UP, buff=0.5).shift(LEFT)
        self.cf.save_state()
        self.play(
            FadeIn(full_text.words[:6].set_opacity(0.45)),
            FadeIn(full_text.words[9:].set_opacity(0.45)),
            Transformr(text_frags.words.copy(), full_text.words[6:9]),
        )
        self.playw(self.cf.animate.shift(LEFT * 3.5))

        ## restore
        self.play(FadeOut(full_text), run_time=0.5)
        self.playw(self.cf.animate.restore())

        ## score is the output of the score function
        out_score_float = 0.68

        out_score = (
            DecimalNumber(out_score_float, num_decimal_places=2, font_size=28)
            .set_color(BLUE)
            .next_to(output_arrow, RIGHT, buff=0.3)
        )
        self.playw(FadeIn(out_score))

        ## same input same output

        self.playw(FadeOut(out_score))

        for i in range(3):
            same_input = text_input.copy()
            self.play(FadeOut(same_input, shift=RIGHT * 4, scale=0.3), run_time=0.5)
            self.playw(
                FadeIn(out_score, shift=RIGHT, scale=3.3),
                run_time=0.5,
                wait=1 if i == 2 else 0,
            )

        ## ol
        ol = self.overlay
        self.add(out_score.set_z_index(ol.z_index + 1))
        self.playw(FadeIn(ol))

        self.playw(RWiggle(out_score, amp=0.3, speed=2, run_time=3))

        ## fadeout ol
        self.playw(FadeOut(ol), self.cf.animate.shift(LEFT * 1.5))

        ## io loop

        text_inputs = ["let me start", "by exploring the", "the code and"]
        out_scores = [0.16, 0.75, 0.47]

        out_group = VGroup()
        for i in range(3):
            # self.play(FadeOut(out_score), FadeOut(text_input))
            if i == 0:
                self.play(
                    out_score.animate.shift(UP * 1.5),
                    text_input.animate.shift(UP * 1.5),
                )
            else:
                og = VGroup(out_score, text_input)
                self.play(
                    og.animate.next_to(out_group, UP, buff=0.15).align_to(og, LEFT),
                    run_time=0.5,
                )
            out_group.add(VGroup(out_score, text_input))
            text_frags = Words(text_inputs[i], font_size=28, font=MONO_FONT).set_color(
                ORANGE
            )
            text_frags.words.arrange(RIGHT, buff=0.5)
            frag_boxes = VGroup(
                *[
                    SurroundingRectangle(w, color=ORANGE, buff=0.2)
                    for w in text_frags.words
                ]
            ).set_opacity(0.15)
            text_input = VGroup(text_frags, frag_boxes).move_to(box_input)
            self.play(FadeIn(text_input), run_time=0.5)

            out_score_float = out_scores[i]
            out_score = (
                DecimalNumber(out_score_float, num_decimal_places=2, font_size=28)
                .set_color(BLUE)
                .next_to(output_arrow, RIGHT, buff=0.3)
            )
            self.play(
                FadeOut(text_input.copy(), shift=RIGHT * 4, scale=0.3), run_time=0.5
            )
            self.playw(
                FadeIn(out_score, shift=RIGHT, scale=3.3),
                run_time=0.5,
                wait=1 if i == 2 else 0,
            )
        out_group.add(VGroup(out_score, text_input))
        ## Circumscribe scores
        scores = VGroup(*[out_group[i][0] for i in range(len(out_group))])
        self.playw(*[Circumscribe(score, color=YELLOW) for score in scores])

        ## ol again
        ol = self.overlay
        ol.z_index += 2
        self.add(score_fn.set_z_index(ol.z_index + 1))
        self.playw(FadeIn(ol))


class llmGeneration(InteractiveScene, Scene2D):
    def construct(self):

        ## llm generation
        string = "Got it, let me start by exploring the code and"
        input_text = Words(string, font_size=20, font=MONO_FONT).set_color(ORANGE)
        input_text.words.arrange(RIGHT, buff=0.3)

        boxes = VGroup(
            *[SurroundingRectangle(w, color=ORANGE, buff=0.1) for w in input_text.words]
        ).set_opacity(0.15)
        input_box = VGroup(input_text, boxes)

        llm_tex = Tex("\\text{LLM}", font_size=40).set_color(BLUE)
        llm_box = (
            Rectangle(width=7, height=2.5)
            .set_color(GREY_B)
            .set_fill(color=BLACK, opacity=0.8)
        )
        llm = VGroup(llm_box, llm_tex)
        self.play(FadeIn(llm))
        self.playw(RWiggle(llm, amp=0.3, speed=2, run_time=2))

        ## text
        input_box.next_to(llm, DOWN).shift(LEFT * 2)
        self.playw(FadeIn(input_box))

        ## text in
        self.play(
            FadeOut(input_box.copy(), shift=UP * 1.5 + RIGHT, scale=0.5), run_time=0.75
        )
        otext1 = Text("implementing", font_size=20, font=MONO_FONT).set_color(ORANGE)
        otext2 = Text("generating", font_size=20, font=MONO_FONT).set_color(ORANGE)
        otext3 = Text("testing", font_size=20, font=MONO_FONT).set_color(ORANGE)

        out_texts = VGroup(otext1, otext2, otext3).arrange(
            RIGHT, buff=-0.2, aligned_edge=DOWN
        )
        out_boxes = VGroup(
            *[SurroundingRectangle(w, color=ORANGE, buff=0.1) for w in out_texts]
        ).set_opacity(0.15)
        outs = (
            VGroup(
                VGroup(otext1, out_boxes[0]).rotate(3 * PI / 4),
                VGroup(otext2, out_boxes[1]).rotate(2 * PI / 4),
                VGroup(otext3, out_boxes[2]).rotate(1 * PI / 4),
            )
            .next_to(llm, UP, buff=0.5)
            .align_to(input_box.get_right(), LEFT)
            .shift(LEFT)
        )

        # rotated boxes: bounding-box bottom is a corner, so anchor the lines on the
        # box edge where the text starts (the LEFT edge before rotation)
        def text_start(box):
            ur, ul, dl, dr = box.get_vertices()
            return (ul + dl) / 2

        hub = text_start(out_boxes[1])
        hub = hub + 0.5 * normalize(hub - out_boxes[1].get_center())

        lines = VGroup(
            *[DashedLine(hub, text_start(out_boxes[i]), color=ORANGE) for i in range(3)]
        )

        self.playw(FadeIn(outs), FadeIn(lines))

        ## rwiggle the output texts, and lines are anchored to the text start
        l1, l2, l3 = lines
        l1.add_updater(lambda l: l.put_start_and_end_on(hub, text_start(out_boxes[0])))
        l2.add_updater(lambda l: l.put_start_and_end_on(hub, text_start(out_boxes[1])))
        l3.add_updater(lambda l: l.put_start_and_end_on(hub, text_start(out_boxes[2])))

        self.playw(*[RWiggle(ot, amp=0.5, speed=1, run_time=3) for ot in outs])
        l1.clear_updaters()
        l2.clear_updaters()
        l3.clear_updaters()

        ## fadeout lines and outputs
        self.play(FadeOut(lines), FadeOut(outs))

        ## fadeout input_box[-4:]
        texts = VGroup(VGroup(text, box) for text, box in zip(input_text.words, boxes))
        self.playw(FadeOut(texts[-4:]))

        ## autoregressive generation
        px = Tex("p(x)", font_size=36).set_color(ORANGE).next_to(llm, UP, buff=0.3)
        for i in range(4):
            run_time = 0.75 if i == 0 else 0.3
            self.play(
                FadeOut(
                    texts[: -4 + i].copy(), shift=UP * 1.5 + RIGHT * 2.5, scale=0.5
                ),
                run_time=run_time,
            )

            self.play(FadeIn(px, shift=UP, scale=1.5), run_time=run_time)
            self.play(Indicate(px, color=BLUE_E), run_time=run_time)
            text_to_in = texts[-4 + i]
            text_to_in.save_state()
            text_to_in.next_to(px, UP, buff=0.2)
            self.play(FadeIn(text_to_in, shift=UP * 0.75, scale=1.5), run_time=run_time)
            self.play(
                Restore(text_to_in, path_arc=PI / 2), FadeOut(px), run_time=run_time
            )
            # texts.add(text_to_in)
            # break

        ## candidates from the p(x)

        self.play(
            FadeOut(texts.copy(), shift=UP * 1.5 + RIGHT * 2, scale=0.5), run_time=0.5
        )
        self.playw(FadeIn(px, shift=UP, scale=1.5), run_time=0.5)
        ot1 = Text("implementing", font_size=20, font=MONO_FONT).set_color(ORANGE)
        ot2 = Text("generating", font_size=20, font=MONO_FONT).set_color(ORANGE)
        ot3 = Text("testing", font_size=20, font=MONO_FONT).set_color(ORANGE)
        ob1 = SurroundingRectangle(ot1, color=ORANGE, buff=0.1).set_opacity(0.15)
        ob2 = SurroundingRectangle(ot2, color=ORANGE, buff=0.1).set_opacity(0.15)
        ob3 = SurroundingRectangle(ot3, color=ORANGE, buff=0.1).set_opacity(0.15)
        tb1 = VGroup(ot1, ob1)
        tb2 = VGroup(ot2, ob2)
        tb3 = VGroup(ot3, ob3)
        tbs = VGroup(tb1, tb2, tb3).arrange(RIGHT, buff=0.5).next_to(px, UP, buff=0.3)
        self.play(
            FadeIn(tb1, shift=tb1.get_center() - px.get_center(), scale=1.5),
            Indicate(px, color=BLUE_E),
            run_time=0.5,
        )
        self.play(
            FadeIn(tb2, shift=tb2.get_center() - px.get_center(), scale=1.5),
            Indicate(px, color=BLUE_E),
            run_time=0.5,
        )
        self.playw(
            FadeIn(tb3, shift=tb3.get_center() - px.get_center(), scale=1.5),
            Indicate(px, color=BLUE_E),
            run_time=0.5,
        )

        ## Flashunder the candidates
        self.play(FlashUnder(ot1, color=YELLOW), run_time=0.5)
        self.play(FlashUnder(ot2, color=YELLOW), run_time=0.5)
        self.playw(FlashUnder(ot3, color=YELLOW), run_time=0.5)

        ## dlines
        dlines = VGroup(
            *[DashedLine(px.get_top(), tb.get_bottom(), color=YELLOW_B) for tb in tbs]
        )

        self.play(*[Create(dl) for dl in dlines])

        ## rwiggle the candidates and dlines
        dl1, dl2, dl3 = dlines
        dl1.add_updater(
            lambda l: l.put_start_and_end_on(px.get_top(), tb1.get_bottom())
        )
        dl2.add_updater(
            lambda l: l.put_start_and_end_on(px.get_top(), tb2.get_bottom())
        )
        dl3.add_updater(
            lambda l: l.put_start_and_end_on(px.get_top(), tb3.get_bottom())
        )

        self.playw(*[RWiggle(tb, amp=0.5, speed=1, run_time=3) for tb in tbs])


class llmBaseScore(InteractiveScene, Scene2D):
    def construct(self):
        ## llm base score

        # llm model
        llm_tex = Tex("\\text{LLM}", font_size=40).set_color(BLUE)
        llm_box = (
            Rectangle(width=7, height=2.5)
            .set_color(GREY_B)
            .set_fill(color=BLACK, opacity=0.8)
        )
        llm = VGroup(llm_box, llm_tex).set_z_index(1).shift(UP * 0.5)

        string = "You are right. I give you the wrong answer because I did not ..."
        output_text = Words(string, font_size=20, font=MONO_FONT).set_color(ORANGE)
        output_boxes = VGroup(
            *[
                SurroundingRectangle(w, color=ORANGE, buff=0.12)
                for w in output_text.words
            ]
        ).set_opacity(0.15)

        texts = VGroup(
            VGroup(text, box) for text, box in zip(output_text.words, output_boxes)
        )
        texts.arrange(RIGHT, buff=0.1).next_to(llm, UP, buff=0.3)

        self.addw(llm)

        ## output text
        self.playwl(
            *[
                FadeIn(
                    text,
                    shift=text.get_center() - llm.get_center(),
                    scale=1.5,
                    run_time=0.8 if i < 3 else 0.3,
                )
                for i, text in enumerate(texts)
            ],
            lag_ratio=0.7,
        )

        ## self.cf up
        self.playw(FadeOut(llm), self.cf.animate.shift(UP * 4))

        ## chunkwise scoring
        chunk_size = 4

        chunks = VGroup()
        for i in range(0, len(texts) - chunk_size):
            chunk = texts[i : i + chunk_size].copy()
            chunk_box = SurroundingRectangle(
                chunk, color=GREEN, buff=0.15, stroke_width=1.5
            )
            for c in chunk:
                c[1].set_fill(opacity=0)
            chunks.add(VGroup(chunk_box.set_stroke(opacity=0), chunk))
        chts = VGroup()
        for ch in chunks:
            cht = ch.generate_target()
            for c in cht[1]:
                c[1].set_fill(opacity=0.15)
            cht[0].set_stroke(opacity=1)
            chts.add(cht.scale(0.8))

        chts.arrange_in_grid(5, 2, h_buff=3, v_buff=0.2, aligned_edge=LEFT).next_to(
            texts, UP, aligned_edge=LEFT, buff=0.4
        )
        texts.save_state()
        self.playwl(
            *[MoveToTarget(ch) for ch in chunks],
            texts.animate.set_opacity(0.05),
            lag_ratio=0.3,
        )

        ## g() score functions
        def get_gfn():
            score_fn_tex = Tex("\\text{g}()", font_size=28).set_color(BLUE)
            score_box = SurroundingRectangle(
                score_fn_tex, color=BLUE, buff=0.2
            ).set_fill(color=BLACK, opacity=0.8)
            score_fn = VGroup(score_box, score_fn_tex)
            return score_fn

        fns = VGroup(
            *[get_gfn().next_to(chunks[i], RIGHT, buff=0.4) for i in range(len(chunks))]
        )

        self.playw(
            *[FadeIn(fn, shift=RIGHT * 0.5) for fn in fns],
        )

        ## scores
        scores_list = [random.random() for _ in range(len(chunks))]
        score_mean = np.mean(scores_list)
        scores = VGroup(
            *[
                DecimalNumber(score, num_decimal_places=2, font_size=24)
                .set_color(BLUE)
                .next_to(fns[i], RIGHT, buff=0.3)
                for i, score in enumerate(scores_list)
            ]
        )
        self.playwl(
            *[FadeIn(score, shift=RIGHT * 0.5, scale=2) for score in scores],
        )

        ## camera tilt
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(
                90,
                33,
                -90,
                (np.float32(2.9), np.float32(4.36), np.float32(-2.09)),
                9.17,
            )
        )

        mean_score = (
            DecimalNumber(score_mean, num_decimal_places=2, font_size=28)
            .rotate(33 * DEGREES, axis=UP)
            .set_color(BLUE_C)
            .next_to(scores, RIGHT, buff=1)
        )

        self.playw(Transformr(scores.copy(), mean_score))

        ## lines
        lines = VGroup(
            *[
                DashedLine(
                    scores[i].get_right(), mean_score.get_left(), buff=0.2, color=BLUE_A
                )
                for i in range(len(scores))
            ]
        )
        self.playw(*[Create(line, run_time=1) for line in lines])

        ## texts restore and flashunder
        self.play(Restore(texts), run_time=0.75)
        self.playw(FlashUnder(texts))

        ## flash under mean score

        self.playw(FlashUnder(mean_score, color=BLUE_D))


class llmGenSynthID(InteractiveScene, Scene2D):
    def construct(self):
        ## llm generation and synthesis
        # llm model
        llm_tex = Tex("\\text{LLM}", font_size=40).set_color(BLUE)
        llm_box = (
            Rectangle(width=7, height=2.5)
            .set_color(GREY_B)
            .set_fill(color=BLACK, opacity=0.8)
        )
        llm = VGroup(llm_box, llm_tex).set_z_index(1).shift(UP * 0.5)
        self.addw(llm)

        ## output text

        string = "You are right. You asked me to generate a function ..."
        input_text = Words(string, font_size=20, font=MONO_FONT).set_color(ORANGE)
        input_boxes = VGroup(
            *[
                SurroundingRectangle(w, color=ORANGE, buff=0.12)
                for w in input_text.words
            ]
        ).set_opacity(0.15)
        texts = VGroup(
            VGroup(text, box) for text, box in zip(input_text.words, input_boxes)
        )
        texts.arrange(RIGHT, buff=0.1).next_to(llm, UP, buff=0.3)

        candidates = [
            ["I", "You", "What"],
            ["said", "told", "asked"],
            ["me", "for", "to"],
            ["generate", "implement", "make"],
            ["the", "this", "a"],
            ["code", "function", "program"],
        ]
        score_lists = [
            [0.32, 0.68, 0.15],
            [0.34, 0.05, 0.45],
            [0.73, 0.44, 0.34],
            [0.91, 0.12, 0.33],
            [0.21, 0.34, 0.46],
            [0.12, 0.77, 0.56],
        ]
        self.playwl(
            *[
                FadeIn(
                    text,
                    shift=text.get_center() - llm.get_center(),
                    scale=1.5,
                    run_time=0.5,
                )
                for i, text in enumerate(texts[:3])
            ],
            lag_ratio=0.5,
        )
        texts_ = VGroup(*texts[:3])

        ## self.cf up

        self.play(self.cf.animate.shift(UP * 1.5))

        ## candidates[0]
        def get_text(string):
            text = Text(string, font_size=20, font=MONO_FONT).set_color(YELLOW_B)
            box = SurroundingRectangle(text, color=YELLOW, buff=0.1).set_opacity(0.15)
            return VGroup(text, box)

        c0 = (
            VGroup(*[get_text(s) for s in candidates[0]])
            .arrange(DOWN, buff=0.15, aligned_edge=LEFT)
            .next_to(texts_, RIGHT, buff=0.3, aligned_edge=DOWN)
        )
        self.playwl(
            *[
                FadeIn(c, shift=c0.get_center() - llm.get_center(), scale=1.5)
                for c in c0[::-1]
            ],
            lag_ratio=0.5,
        )

        ## g()
        def get_gfn():
            score_fn_tex = Tex("\\text{g}()", font_size=28).set_color(BLUE)
            score_box = (
                SurroundingRectangle(score_fn_tex, color=BLUE, buff=0.2)
                .stretch_to_fit_width(1)
                .set_fill(color=BLACK, opacity=0.8)
            )
            score_fn = VGroup(score_box, score_fn_tex)
            return score_fn

        g = get_gfn().next_to(VGroup(texts_, c0), RIGHT, buff=0.5).shift(UP * 1.3)
        self.playw(FadeIn(g))

        ## skewed animation: three io
        i1 = VGroup(*texts_.copy(), c0[0].copy())
        i2 = VGroup(*texts_.copy(), c0[1].copy())
        i3 = VGroup(*texts_.copy(), c0[2].copy())

        inputs = [i1, i2, i3]

        anims = []
        scores = VGroup()
        for i in range(3):
            anim = []
            anim.append(
                inputs[i].animate.arrange(RIGHT, buff=0.1).next_to(g, LEFT, buff=0.3)
            )
            score = (
                DecimalNumber(score_lists[0][i], num_decimal_places=2, font_size=24)
                .set_color(BLUE)
                .next_to(g, RIGHT, buff=0.3)
            )
            scores.add(score)
            anim.append(Transformr(inputs[i], score))
            anim.append(
                score.animate(path_arc=-PI if i != 0 else 0)
                .next_to(c0[i], RIGHT)
                .align_to(score, LEFT)
            )
            anims.append(anim)
        skew_anims = SkewedAnimations(*anims)

        for i, a in enumerate(skew_anims):
            # if i > len(skew_anims) - 3:
            #     continue
            run_time = 0.5 if i == 0 else 0.4
            wait = 1 if i == len(skew_anims) - 1 else 0
            self.playw(*a, run_time=run_time, wait=wait)

        ## scores[1] is largest
        self.play(VGroup(scores[0], scores[2]).animate.set_opacity(0.2), run_time=0.5)
        self.playw(Circumscribe(scores[1], color=BLUE_D))

        ## candidates[1] is picked
        self.play(FadeOut(VGroup(c0[0], c0[2], scores[0], scores[2])), run_time=0.5)
        self.playw(
            c0[1].animate.next_to(texts_, RIGHT, buff=0.1).set_color(ORANGE),
            FadeOut(scores[1]),
        )

        texts_.add(c0[1])
        ## loop for candidates[1] and candidates[2]
        for i in range(1, 6):
            run_time = 0.5
            c = (
                VGroup(*[get_text(s) for s in candidates[i]])
                .arrange(DOWN, buff=0.15, aligned_edge=LEFT)
                .next_to(texts_, RIGHT, buff=0.3, aligned_edge=DOWN)
            )
            self.playwl(
                *[
                    FadeIn(
                        c_,
                        shift=c.get_center() - llm.get_center(),
                        scale=1.5,
                        run_time=run_time,
                    )
                    for c_ in c[::-1]
                ],
                g.animate.next_to(VGroup(texts_, c), RIGHT, buff=0.5).shift(UP * 1.3),
                lag_ratio=0.5,
                wait=0,
            )

            # g()

            # skewed animation: three io
            i1 = VGroup(*texts_[-3:].copy(), c[0].copy())
            i2 = VGroup(*texts_[-3:].copy(), c[1].copy())
            i3 = VGroup(*texts_[-3:].copy(), c[2].copy())

            inputs = [i1, i2, i3]

            anims = []
            scores = VGroup()
            for j in range(3):
                anim = []
                anim.append(
                    inputs[j]
                    .animate.arrange(RIGHT, buff=0.1)
                    .next_to(g, LEFT, buff=0.3)
                )
                score = (
                    DecimalNumber(score_lists[i][j], num_decimal_places=2, font_size=24)
                    .set_color(BLUE)
                    .next_to(g, RIGHT, buff=0.3)
                )
                scores.add(score)
                anim.append(Transformr(inputs[j], score))
                anim.append(
                    score.animate(path_arc=-PI if j != 0 else 0)
                    .next_to(c[j], RIGHT)
                    .align_to(score, LEFT)
                )
                # anim.append(score.animate.shift(DOWN*0.65))
                # anim.append(score.animate.shift(DOWN*0.65))
                # anim.append(score.animate.shift(DOWN*0.65))
                anims.append(anim)
            skew_anims = SkewedAnimations(*anims)

            for j, a in enumerate(skew_anims):
                # if j > len(skew_anims) - 3:
                #     continue
                run_time = 0.5 if j == 0 else 0.4
                self.play(*a, run_time=run_time)

            # scores[?] is largest
            max_idx = np.argmax([score_lists[i][j] for j in range(3)])
            self.play(Circumscribe(scores[max_idx], color=BLUE_D), run_time=0.5)

            # candidates[?] is picked
            to_remove_c = VGroup(*[c[j] for j in range(3) if j != max_idx])
            to_remove_scores = VGroup(*[scores[j] for j in range(3) if j != max_idx])
            self.play(FadeOut(VGroup(to_remove_c, to_remove_scores)), run_time=0.5)
            self.play(
                c[max_idx].animate.next_to(texts_, RIGHT, buff=0.1).set_color(ORANGE),
                FadeOut(scores[max_idx]),
                run_time=0.5,
            )
            texts_.add(c[max_idx])
        self.wait()
        ## g up to the texts
        self.play(
            # g.animate.next_to(texts_, OUT, buff=1.5).rotate(63 * DEGREES, axis=DOWN).shift(RIGHT * 2),
            FadeOut(g),
            FadeOut(llm),
            self.cf.animate.reorient(
                -90,
                63,
                90,
                (np.float32(-0.07), np.float32(2.39), np.float32(-0.1)),
                6.39,
            ),
        )

        chunk_size = 4
        color_gradients = [
            interpolate_color(GREEN_A, GREEN_E, i / (len(texts_) - chunk_size + 1))
            for i in range(len(texts_) - chunk_size + 1)
        ]
        liness = VGroup()
        scores = (
            VGroup(
                *[
                    DecimalNumber(
                        max(score_lists[i]), num_decimal_places=2, font_size=18
                    )
                    .set_color(BLUE)
                    .next_to(g, RIGHT, buff=0.3)
                    for i in range(len(texts_) - chunk_size + 1)
                ]
            )
            .arrange(RIGHT + DOWN, buff=0.2)
            .next_to(texts_, OUT, buff=2.5)
            .rotate(63 * DEGREES / 2, axis=DOWN)
        )

        for i in range(len(texts_) - chunk_size + 1):
            chunk = (
                texts_[i : i + chunk_size]
                .copy()
                .align_to(texts_[i : i + chunk_size], UP)
            )
            lines = VGroup(
                *[
                    DashedLine(
                        chunk[j].get_center(),
                        scores[i].get_left(),
                        color=color_gradients[i],
                    )
                    for j in range(chunk_size)
                ]
            ).set_opacity(0.2)
            liness.add(lines)
        self.playw(FadeIn(liness), FadeIn(scores), wait=4)

        ## mean score
        mean_score = (
            DecimalNumber(
                np.mean(
                    [max(score_lists[i]) for i in range(len(texts_) - chunk_size + 1)]
                ),
                num_decimal_places=2,
                font_size=28,
            )
            .set_color(BLUE_C)
            .next_to(scores, OUT, buff=0)
            .shift(UP)
            .rotate(63 * DEGREES, axis=DOWN)
        )
        mean_lines = VGroup(
            *[
                DashedLine(
                    scores[i].get_right(), mean_score, color=BLUE_A, buff=0.2
                ).set_opacity(0.5)
                for i in range(len(scores))
            ]
        )
        self.playw(
            Transformr(scores.copy(), mean_score),
            *[Create(line, run_time=1) for line in mean_lines],
        )


class metaphor(InteractiveScene, Scene2D):
    def construct(self):
        ## metaphor: univ whose new members will be 1000
        def get_student(is_dot=False):
            if is_dot:
                return Text("...", font_size=20).set_color(GREY_C)
            student = SVGMobject("svgs/student.svg").scale(0.15)
            return student

        def get_univ():
            univ = SVGMobject("svgs/school.svg").scale(0.5)
            return univ

        univ = get_univ()

        self.playw(FadeIn(univ))

        ## text short time
        _text = Text("명문대", font_size=24).next_to(univ, DOWN, buff=0.2)
        self.play(FadeIn(_text), run_time=0.75)
        self.play(FlashUnder(_text, color=YELLOW, buff=0.05), run_time=0.75)
        self.playw(FadeOut(_text), run_time=0.5)

        _text2 = Words("점수 높은 순 1000명", font_size=24).next_to(
            univ, DOWN, buff=0.2
        )
        self.play(FadeIn(_text2), run_time=0.75)
        self.play(Indicate(_text2.words[-1], color=YELLOW), run_time=0.75)
        self.playw(FadeOut(_text2), run_time=0.5)

        ## students
        self.play(univ.animate.shift(DOWN * 1.5), run_time=0.75)
        row, col = 11, 21
        students = VGroup()
        for i in range(row):
            for j in range(col):
                student = get_student(is_dot=(i == row // 2 or j == col // 2))
                students.add(student)
        students.arrange_in_grid(row, col, h_buff=0.1, v_buff=0.1).next_to(
            univ, UP, buff=0.5
        )
        _text3 = (
            Text("제발 합격시켜주세요", font_size=20)
            .set_color(RED_A)
            .next_to(students, RIGHT, buff=0.2)
            .shift(DOWN * 1.5)
        )
        self.playwl(FadeIn(students), FadeIn(_text3), lag_ratio=0.5, wait=0)
        self.playw(
            RWiggle(_text3, amp=0.2, speed=5, run_time=3),
            *[
                RWiggle(s, amp=0.1, speed=2.5, run_time=3)
                for s in students
                if not isinstance(s, Text)
            ],
        )

        ## fadeout _text3 and univ
        self.play(FadeOut(_text3), FadeOut(univ), run_time=0.5)
        self.playw(students.animate.move_to(ORIGIN).shift(UP * 0.5).scale(1.2))

        ## shuffle
        students.generate_target()
        subs = list(students.target)
        svgs = iter(VGroup(*[s for s in subs if not isinstance(s, Text)]).shuffle())
        students.target.set_submobjects(
            [s if isinstance(s, Text) else next(svgs) for s in subs]
        )
        self.play(MoveToTarget(students, path_arc=PI / 3))

        ## pair_boxes
        slots = sorted(students, key=lambda s: (-round(s.get_y(), 2), s.get_x()))
        pair_boxes = VGroup()
        for r in range(row):
            line = [
                s for s in slots[r * col : (r + 1) * col] if not isinstance(s, Text)
            ]
            for a, b in zip(line[::2], line[1::2]):
                pair_boxes.add(
                    SurroundingRectangle(VGroup(a, b), buff=0.03).set_stroke(
                        RED, width=1.5
                    )
                )
        self.play(FadeIn(pair_boxes))

        ## randint from [0, 99] (both inclusive) for each student
        scores_list = [random.randint(0, 99) for i in range(len(students))]
        scores = VGroup()
        score_of = {}
        for i, s in enumerate(students):
            if isinstance(s, Text):
                continue
            score = (
                DecimalNumber(
                    scores_list[i],
                    num_decimal_places=0,
                    min_total_width=2,
                    font_size=16,
                )
                .set_color(RED)
                .move_to(s)
                .shift(DOWN * 0.1)
                .add_background_rectangle(BLACK, buff=0.03)
            )
            scores.add(score)
            score_of[id(s)] = (scores_list[i], score)
        self.playw(FadeIn(scores))

        ## low score fadeout: loser in pair_boxes
        losers = VGroup()
        winners = VGroup()
        for box in pair_boxes:
            loser, winner = sorted(box.mobject, key=lambda s: score_of[id(s)][0])
            losers.add(loser, score_of[id(loser)][1])
            winners.add(VGroup(winner, score_of[id(winner)][1]))
        self.play(FadeOut(losers))

        ## fadeout pair_boxes and ...s(texts in students)
        self.play(
            FadeOut(pair_boxes),
            FadeOut(VGroup(*[s for s in students if isinstance(s, Text)])),
        )
        self.playw(winners.animate.arrange_in_grid(5, 20, h_buff=0.1, v_buff=0.1).shift(UP*2.5 + LEFT*1.25))

        ## scores histogram: bin size 10, range [0, 100)
        bin_size, num_bins, n_cols = 10, 10, 2

        # 각 bin에 들어갈 winner들의 인덱스
        bin_idxs = [[] for _ in range(num_bins)]
        for i, w in enumerate(winners):
            b = min(score_of[id(w[0])][0] // bin_size, num_bins - 1)
            bin_idxs[b].append(i)
        max_count = max(len(idxs) for idxs in bin_idxs)
        y_max = int(np.ceil(max_count / 10) * 10)

        nump = RaenimPlane(
            x_range=(0, 100, bin_size),
            y_range=(0, y_max, 10),
            width=18,
            height=8,
        ).shift(UP * 0.5)
        nump.x_axis.add_numbers(range(0, 101, bin_size), font_size=16)
        nump.y_axis.add_numbers(range(10, y_max + 1, 10), font_size=16)

        # 한 칸(cell) 크기: 가로는 bin 너비의 절반(2열), 세로는 y축 2칸(= 2명)
        origin = nump.c2p(0, 0)
        cell_w = (nump.c2p(bin_size, 0)[0] - origin[0]) / n_cols
        cell_h = (nump.c2p(0, n_cols)[1] - origin[1])
        # 셀에 맞게 줄이기만 하고 키우지는 않음
        scale_factor = min(
            cell_w * 0.9 / max(w.get_width() for w in winners),
            cell_h * 0.9 / max(w.get_height() for w in winners),
            1,
        )

        # bin별 외곽선(막대)
        hist_bars = VGroup()
        for b, idxs in enumerate(bin_idxs):
            if not idxs:
                continue
            rows = -(-len(idxs) // n_cols)
            bar = Rectangle(
                width=nump.c2p(bin_size, 0)[0] - origin[0],
                height=rows * cell_h,
            ).set_stroke(BLUE_D, width=1.5, opacity=0.6)
            bar.move_to(nump.c2p(b * bin_size, 0), DL)
            hist_bars.add(bar)

        # 각 winner의 목적지: bin 안에서 2열로 아래부터 채움
        for b, idxs in enumerate(bin_idxs):
            base = nump.c2p(b * bin_size, 0)
            for k, i in enumerate(idxs):
                col, r = k % n_cols, k // n_cols
                w = winners[i]
                w.generate_target()
                w.target.scale(scale_factor).move_to(
                    base + RIGHT * (col + 0.5) * cell_w + UP * (r + 0.5) * cell_h
                )
        wt = VGroup(*[w.target for w in winners])

        self.play(FadeIn(nump), run_time=0.75)
        # 점수 낮은 bin부터 한 뭉텅이씩 자기 자리로
        anims = []
        for idxs in bin_idxs[::-1]:
            if not idxs:
                continue
            anims.append(AnimationGroup(*[MoveToTarget(winners[i]) for i in idxs]))
        self.playwl(*anims, lag_ratio=0.7)
        self.playw(FadeIn(hist_bars))

class verifyingWatermark(InteractiveScene, Scene2D):
    def construct(self):

        ## text
        string = "' 본질을 놓칩니다 ' 같은 AI 소리를 그대로 붙여 넣으면 본질을 놓칩니다 ..."
        text = Words(string, font_size=20).set_color(ORANGE)
        boxes = VGroup(
            *[SurroundingRectangle(w, color=ORANGE, buff=0.12) for w in text.words]
        ).set_opacity(0.15)
        input_text = VGroup(
            VGroup(text, box) for text, box in zip(text.words, boxes)
        ).arrange(RIGHT, buff=0.1).next_to(ORIGIN, UP, buff=0.3)

        self.playw(FadeIn(input_text), run_time=0.75)

        ## chunkwise scoring
        chunk_size = 4
        text_chunks = VGroup()
        for i in range(0, len(text.words) - chunk_size + 1):
            chunk = input_text[i : i + chunk_size].copy()
            chunk_box = SurroundingRectangle(
                chunk, color=GREEN, buff=0.15, stroke_width=1.5
            )
            for c in chunk:
                c[1].set_fill(opacity=0)
            text_chunks.add(VGroup(chunk_box.set_stroke(opacity=0), chunk))
        scores_list = [random.random() * 0.6 + 0.4 for _ in range(len(text_chunks))]
        scores = VGroup(
            *[
                DecimalNumber(score, num_decimal_places=2, font_size=24)
                .set_color(BLUE)
                for i, score in enumerate(scores_list)
            ]
        ).arrange(RIGHT, buff=0.5).next_to(text_chunks, DOWN, buff=0.5)

        self.playwl(*[Transformr(text_chunks[i], scores[i]) for i in range(len(text_chunks))], lag_ratio=0.5)

        ## mean_score
        mean_score = (
            DecimalNumber(np.mean(scores_list), num_decimal_places=2, font_size=28)
            .set_color(BLUE_C)
            .next_to(scores, DOWN, buff=0.75)
        )
        self.play(FadeIn(mean_score), run_time=0.75)

        lines = VGroup(
            *[
                DashedLine(
                    scores[i], mean_score, color=BLUE_A, buff=0.1
                )
                for i in range(len(scores))
            ]
        )
        self.playw(*[Create(line, run_time=1) for line in lines])

        ## text to be red
        ol = self.overlay
        input_text.set_z_index(ol.z_index + 1)
        input_text.save_state()
        self.playw(input_text.animate.set_color(PURE_RED), FadeIn(ol))

        self.embed()
        ## fadeout ol
        self.play(FadeOut(ol), Restore(input_text))
        self.playw(FlashUnder(mean_score, color=BLUE_D))

