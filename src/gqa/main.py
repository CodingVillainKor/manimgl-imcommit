from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):
        num_samples = 7

        ## intro

        query = Tensor(num_samples, shape="square", arrange=DOWN, buff=0.2)
        key = Tensor(num_samples, shape="square", arrange=RIGHT, buff=0.2)
        value = Tensor(num_samples, shape="square", arrange=DOWN, buff=0.2)

        logits = VGroup(
            *[
                Dot(radius=0.05).set_color(random_color())
                for _ in range(num_samples * num_samples)
            ]
        ).arrange_in_grid(buff=0.5, n_rows=num_samples, n_cols=num_samples)

        query.next_to(logits, LEFT, buff=0.5)
        key.next_to(logits, UP, buff=0.5)
        value.next_to(logits, RIGHT, buff=0.5)

        query_text = Text("Query", font="Noto Sans KR", font_size=20).next_to(
            query, DOWN, buff=0.15
        )
        key_text = Text("Key", font="Noto Sans KR", font_size=20).next_to(
            key, RIGHT, buff=0.15
        )
        value_text = Text("Value", font="Noto Sans KR", font_size=20).next_to(
            value, DOWN, buff=0.15
        )
        self.playw(
            FadeIn(query),
            FadeIn(key),
            FadeIn(query_text),
            FadeIn(key_text),
        )

        ## attention logit

        self.playwl(
            AnimationGroup(
                FadeOut(query.copy(), shift=RIGHT), FadeOut(key.copy(), shift=DOWN)
            ),
            FadeIn(logits),
            lag_ratio=0.3,
        )

        ## attention eq
        # attn_eq = Tex(r"\text{Attention} = \text{Softmax}(\frac{QK^T}{\sqrt{d_k}}) V", font_size=32).next_to(logits, RIGHT)
        qkt = Tex("QK^T", font_size=32).next_to(logits, RIGHT)
        self.playw(FadeIn(qkt))

        ## shape
        q_shape = Tex("\\in R^{L \\times d_k}", font_size=28).next_to(
            query_text, RIGHT, buff=0.1
        )
        k_shape = Tex("\\in R^{L \\times d_k}", font_size=28).next_to(
            key_text, RIGHT, buff=0.1
        )
        v_shape = Tex("\\in R^{L \\times d_v}", font_size=28).next_to(
            value_text, RIGHT, buff=0.1
        )
        self.mouse.next_to(query_text, LEFT, buff=5)
        self.play(self.mouse.animate.on(query_text))
        self.playw(FadeIn(q_shape))
        self.play(self.mouse.animate.on(key_text), run_time=0.75)
        self.playw(FadeIn(k_shape))

        qkt_shape = Tex("\\in R^{L \\times L}", font_size=28).next_to(
            qkt, RIGHT, buff=0.1
        )
        self.play(self.mouse.animate.on(qkt), run_time=0.75)
        self.playw(FadeIn(qkt_shape))

        ## fadeout shapes
        self.playw(
            FadeOut(qkt_shape, shift=RIGHT * 2),
            qkt.animate.shift(RIGHT * 2),
            FadeOut(self.mouse, shift=RIGHT * 2),
            query_text.animate.shift(DOWN * 0.3),
            q_shape.animate.shift(DOWN * 0.3),
        )

        ## shape explain
        rbrace = Brace(logits, RIGHT).set_color(YELLOW_B)
        rbrace_text = (
            Tex("L", font_size=36).next_to(rbrace, RIGHT, buff=0.1).set_color(YELLOW_B)
        )
        dbrace = Brace(logits, DOWN).set_color(YELLOW_B)
        dbrace_text = (
            Tex("L", font_size=36).next_to(dbrace, DOWN, buff=0.1).set_color(YELLOW_B)
        )
        self.playw(
            FadeIn(rbrace),
            FadeIn(rbrace_text),
            FadeIn(dbrace),
            FadeIn(dbrace_text),
        )

        logit_nums_list = [
            [random.uniform(-3, 15) for i in range(num_samples)]
            for _ in range(num_samples)
        ]
        softmax_list_robust = np.exp(
            logit_nums_list - np.max(logit_nums_list, axis=-1, keepdims=True)
        )
        softmax_list_robust /= np.sum(softmax_list_robust, axis=-1, keepdims=True)
        logits_num = VGroup(
            *[
                Text(f"{logit:.2f}"[:4], font_size=20)
                .set_color(logits[i].get_color())
                .move_to(logits[i])
                for i, logit in enumerate(np.array(logit_nums_list).flatten())
            ]
        )
        softmax_num = VGroup(
            *[
                Text(f"{softmax:.2f}"[:4], font_size=20)
                .set_color(logits[i].get_color())
                .move_to(logits[i])
                for i, softmax in enumerate(np.array(softmax_list_robust).flatten())
            ]
        )
        logitsc = logits.copy()
        logits_numc = logits_num.copy()
        self.playw(Transformr(logits, logits_num, path_arc=90 * DEGREES))

        self.playw(Transformr(logits_num, logitsc, path_arc=-90 * DEGREES))

        self.playw(
            FadeOut(rbrace),
            FadeOut(rbrace_text),
            FadeOut(dbrace),
            FadeOut(dbrace_text),
            query_text.animate.shift(UP * 0.3),
            q_shape.animate.shift(UP * 0.3),
        )

        ## shape q
        arrow_q = Arrow(
            query[-1].get_left() + LEFT, query[-1].get_left(), buff=0.05, thickness=2
        ).set_color(GREY_B)
        arrow_text = Tex("R^{d_k}", font_size=36).next_to(arrow_q, LEFT, buff=0.1)
        self.playwl(FadeIn(arrow_text), GrowArrow(arrow_q), lag_ratio=0.5)

        ## detail - shape q
        self.cf.save_state()

        q_1 = query[:-1]
        q_1.save_state()
        logitsc.save_state(),
        key.save_state(),
        key_text.save_state(),
        k_shape.save_state(),
        qkt.save_state(),
        arrow_q.save_state(),
        arrow_text.save_state(),
        self.playw(
            self.cf.animate.reorient(
                0, 64, 0, (np.float32(-1.71), np.float32(-0.0), np.float32(-0.24)), 7.75
            ),
            arrow_q.animate.rotate(64 * DEGREES, axis=RIGHT),
            arrow_text.animate.rotate(64 * DEGREES, axis=RIGHT),
            q_1.animate.set_opacity(0.3),
            logitsc.animate.set_opacity(0.3),
            key.animate.set_opacity(0.3),
            key_text.animate.set_opacity(0.3),
            k_shape.animate.set_opacity(0.3),
            qkt.animate.set_opacity(0.3),
        )

        query_sample_example = (
            randn(1, 9)
            .scale(0.25)
            .rotate(64 * DEGREES, axis=RIGHT)
            .next_to(query[-1], OUT, buff=0.5)
        )
        query_sample_example[4].become(
            Text("...", font_size=12, font=MONO_FONT)
            .rotate(64 * DEGREES, axis=RIGHT)
            .move_to(query_sample_example[4])
        )
        self.playw(FadeIn(query_sample_example))

        dk_brace = (
            Brace(query_sample_example.copy().rotate(-64 * DEGREES, axis=RIGHT), UP)
            .rotate(64 * DEGREES, axis=RIGHT)
            .shift(OUT * 0.1)
            .set_color(YELLOW_B)
        )
        dk_brace_text = (
            Tex("d_k", font_size=30)
            .rotate(64 * DEGREES, axis=RIGHT)
            .next_to(dk_brace, OUT, buff=0.1)
            .set_color(YELLOW_B)
        )
        self.playw(FadeIn(dk_brace), FadeIn(dk_brace_text))
        self.playw(
            FadeOut(dk_brace), FadeOut(dk_brace_text), FadeOut(query_sample_example)
        )

        self.playw(
            Restore(self.cf),
            Restore(q_1),
            Restore(logitsc),
            Restore(key),
            Restore(key_text),
            Restore(k_shape),
            Restore(qkt),
            Restore(arrow_q),
            Restore(arrow_text),
        )

        ## inner product

        q3 = query[3].copy()
        k3 = key[3].copy()
        l3 = logitsc[3 * num_samples + 3].copy()

        self.add(q3, k3, l3)
        self.playw(
            query.animate.set_opacity(0.2),
            key.animate.set_opacity(0.2),
            logitsc.animate.set_opacity(0.2),
            FadeOut(arrow_q),
            FadeOut(arrow_text),
        )

        q3_mat = randn(1, 9).scale(0.35).next_to(q3, UP, buff=0.2)
        k3_mat = randn(1, 9).scale(0.35).next_to(k3, DOWN, buff=0.2)
        q3_mat[4].become(Text("...", font_size=12, font=MONO_FONT).move_to(q3_mat[4]))
        k3_mat[4].become(Text("...", font_size=12, font=MONO_FONT).move_to(k3_mat[4]))
        self.playw(FadeIn(q3_mat), FadeIn(k3_mat))

        self.playw(FlashAround(qkt))
        k3_matt = randn(9, 1).scale(0.35).next_to(q3_mat, RIGHT, buff=0.2)
        for i in range(9):
            k3_matt[i].become(k3_mat[i].copy().move_to(k3_matt[i]))
        self.playw(Transform(k3_mat, k3_matt))

        ## inner product result
        self.playw(q3.animate.move_to(l3), k3.animate.move_to(l3))
        get_plus = (
            lambda x, y: Text("+", font_size=24)
            .move_to((x.get_center() + y.get_center()) / 2)
            .set_color(GREY_B)
        )
        get_mult = (
            lambda x, y: Text("·", font_size=24)
            .move_to((x.get_center() + y.get_center()) / 2)
            .set_color(GREY_B)
        )
        q3_mat.generate_target()
        k3_mat.generate_target()
        items = VGroup()
        pluses = VGroup()
        mults = VGroup()
        for i in range(9):
            mult = get_mult(q3_mat.target[i], k3_mat.target[i])
            mults.add(mult)
            qk3_item = VGroup(q3_mat.target[i], mult, k3_mat.target[i]).arrange(
                RIGHT, buff=0.05
            )
            items.add(qk3_item)
            if i < 8:
                plus = get_plus(q3_mat.target[i], q3_mat.target[i + 1])
                pluses.add(plus)
                items.add(plus)
        q3_mat.target[-2:].set_opacity(0)
        k3_mat.target[-2:].set_opacity(0)
        items.arrange(RIGHT, buff=0.1).next_to(q3, UP, buff=0.2)
        self.playwl(
            AnimationGroup(MoveToTarget(q3_mat), MoveToTarget(k3_mat)),
            AnimationGroup(*[FadeIn(pluses), FadeIn(mults)]),
            lag_ratio=0.3,
        )

        self.playwl(
            *[FlashAround(VGroup(q3_mat[i], k3_mat[i])) for i in range(9)],
            FadeOut(q3),
            FadeOut(k3),
            lag_ratio=0.3,
        )

        inner_products = VGroup(q3_mat[:-2], k3_mat[:-2], pluses, mults)
        l3c = l3.copy()
        self.playw(
            FadeOut(inner_products, shift=DOWN * 0.4, scale=0.2),
            Transform(l3, logits_numc[3 * num_samples + 3], path_arc=-90 * DEGREES),
        )
        self.playw(Transform(l3, l3c, path_arc=90 * DEGREES))

        ## logits
        self.playw(
            logitsc.animate.set_opacity(1),
            query_text.animate.set_opacity(0.3),
            key_text.animate.set_opacity(0.3),
            q_shape.animate.set_opacity(0.3),
            k_shape.animate.set_opacity(0.3),
        )
        softmaxt = Tex("\\text{Softmax}(\\frac{QK^T}{\\sqrt{d_k}})", font_size=32)
        softmaxt_qkt = softmaxt[8:11]
        softmaxt.shift(qkt.get_center() - softmaxt_qkt.get_center())
        self.play(FadeIn(softmaxt))
        self.remove(qkt)
        self.wait()

        ## full attn eq
        attn_eq = Tex(
            r"\text{Softmax}(\frac{QK^T}{\sqrt{d_k}}) V",
            font_size=32,
        )
        attn_softmax = attn_eq[:-1]
        attn_eq.shift(softmaxt.get_center() - attn_softmax.get_center())
        self.play(Transformr(softmaxt, attn_softmax), FadeIn(attn_eq[-1]))
        self.add(attn_eq)
        self.wait()

        self.playwl(
            attn_eq.animate.shift(RIGHT * 0.15),
            FadeIn(VGroup(value, value_text)),
            lag_ratio=0.3,
        )

        ## attn eq is inner product
        self.mouse.set_opacity(0)
        self.playw(
            self.mouse.animate.set_opacity(1).on(attn_eq[:-1]),
            attn_eq[:-1].animate.set_color(YELLOW_B),
        )
        self.playw(
            self.mouse.animate.on(attn_eq[-1]),
            attn_eq[-1].animate.set_color(YELLOW_B),
            attn_eq[:-1].animate.set_color(WHITE),
        )

        ## inner product animation
        dot_qk = GlowDot().move_to(logitsc[0].get_center())
        path_logit = TracedPath(
            dot_qk.get_center,
            time_traced=0.75,
            stroke_opacity=[0, 1],
            stroke_width=4,
            stroke_color=YELLOW,
        )
        dot_v = GlowDot().move_to(value[0].get_center())
        path_v = TracedPath(
            dot_v.get_center,
            time_traced=0.75,
            stroke_opacity=[0, 1],
            stroke_width=4,
            stroke_color=YELLOW,
        )
        self.add(dot_qk, path_logit, dot_v, path_v)
        self.play(
            FadeOut(self.mouse),
            attn_eq[-1].animate.set_color(WHITE),
            dot_qk.animate.move_to(logitsc[num_samples - 1]),
            dot_v.animate.move_to(value[-1].get_center()),
            run_time=0.75,
        )
        dot_qks = Group(dot_qk)
        path_logits = Group(path_logit)
        for i in range(1, num_samples):
            dot_qk = GlowDot().move_to(logitsc[i * num_samples].get_center())
            path_logit = TracedPath(
                dot_qk.get_center,
                time_traced=0.75,
                stroke_opacity=[0, 1],
                stroke_width=4,
                stroke_color=YELLOW,
            )
            dot_qks.add(dot_qk)
            path_logits.add(path_logit)
            self.remove(path_v)
            dot_v.move_to(value[0].get_center())
            self.add(dot_qk, path_logit, dot_v, path_v)
            self.play(
                dot_qk.animate.move_to(logitsc[(i + 1) * num_samples - 1]),
                dot_v.animate.move_to(value[-1].get_center()),
                run_time=0.75,
            )
            self.remove(path_logits[-2], dot_qks[-2])
        self.wait()
        self.remove(path_logits[-1], dot_qks[-1], dot_v, path_v)

        self.playw(FlashAround(attn_eq))

        ## logit is scalar numbers
        self.remove(l3)
        self.playw(Transform(logitsc, softmax_num, path_arc=90 * DEGREES))

        ## unwrap attention
        logitsc.generate_target()
        values = VGroup()
        mults, pluses, items = VGroup(), VGroup(), VGroup()
        items_orig = VGroup()
        for i in range(num_samples):
            if i == 0:
                valuec = value
            else:
                valuec = value.copy()
            valuec.generate_target()
            items_row = VGroup()
            items_row_orig = VGroup()
            for j in range(num_samples):
                mult = get_mult(logitsc.target[i * num_samples + j], valuec.target[j])
                item = VGroup(
                    logitsc.target[i * num_samples + j],
                    mult,
                    valuec.target[j],
                ).arrange(RIGHT, buff=0.1)
                mults.add(mult)
                items_row.add(item)
                items_row_orig.add(
                    VGroup(logitsc[i * num_samples + j], mult, valuec[j])
                )
                if j < num_samples - 1:
                    plus = get_plus(
                        logitsc.target[i * num_samples + j],
                        logitsc.target[i * num_samples + j + 1],
                    )
                    pluses.add(plus)
                    items_row.add(plus)
                    items_row_orig.add(plus)
            items_row.arrange(RIGHT, buff=0.1)

            values.add(valuec)
            items.add(items_row)
            items_orig.add(items_row_orig)
        items.arrange(DOWN, buff=0.1)

        rests = VGroup(query, key, value_text, query_text, key_text, q_shape, k_shape)
        self.playw(
            MoveToTarget(logitsc),
            attn_eq.animate.shift(RIGHT * 3),
            self.cf.animate.scale(1.2).shift(RIGHT + DOWN),
            *[MoveToTarget(v) for v in values],
            FadeIn(pluses),
            FadeIn(mults),
            rests.animate.rotate(-PI / 2.1, axis=RIGHT)
            .shift(DOWN * 3)
            .set_opacity(0.3),
        )
        ## unwrapped value shape
        self.playw(items_orig[1:].animate.set_opacity(0.3))

        v_shape = Tex("\\in R^{d_k}", font_size=32).next_to(items_orig[0], RIGHT)
        self.playw(FadeIn(v_shape))
        rect = SurroundingRectangle(items_orig, color=ORANGE, buff=0.1)
        v_total_shape = (
            Tex("\\in R^{L \\times d_k}", font_size=40)
            .next_to(rect, RIGHT)
            .align_to(rect, DOWN)
            .set_color(ORANGE)
        )
        self.play(FadeIn(rect), FadeOut(v_shape))
        self.playw(items_orig[1:].animate.set_opacity(1), FadeIn(v_total_shape))


class multiheadAttn(InteractiveScene, Scene2D):
    def construct(self):

        ## multi-head attention
        num_samples = 7
        nums = VGroup()
        value = Tensor(num_samples, shape="square")
        items = VGroup()
        get_mult = lambda: Text("·", font_size=24).set_color(GREY_B)
        get_plus = lambda: Text("+", font_size=24).set_color(GREY_B)

        logit_nums_list = [random.uniform(-3, 15) for _ in range(num_samples)]
        softmax_list_robust = np.exp(
            logit_nums_list - np.max(logit_nums_list, axis=-1, keepdims=True)
        )
        softmax_list_robust /= np.sum(softmax_list_robust, axis=-1, keepdims=True)
        softmax = VGroup(*[Text(f"{x:.2f}", font_size=24) for x in softmax_list_robust])

        for i in range(num_samples):
            nums.add(softmax[i])
            item = VGroup(nums[i], get_mult(), value[i]).arrange(RIGHT, buff=0.05)
            items.add(item)
            if i < num_samples - 1:
                items.add(get_plus())
        items.arrange(RIGHT, buff=0.1)
        self.playw(FadeIn(items))

        tensors = VGroup(*[randn(9, 1).scale(0.3) for _ in range(num_samples)])
        for t in tensors:
            t[4].become(Text("...", font_size=24).move_to(t[4]))
        items.generate_target()
        for i, idx in enumerate(range(0, len(items), 2)):
            items.target[idx][-1].become(tensors[i])
            items.target[idx].arrange(RIGHT, buff=0.05)
        items.target.arrange(RIGHT, buff=0.1)
        self.playw(MoveToTarget(items))

        ## words
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(
                0, 62, 0, (np.float32(-0.01), np.float32(0.41), np.float32(0.74)), 7.76
            )
        )
        # 7 words sentence
        words_list = ["What", "is", "the", "meaning", "of", "piui", "?"]
        color_list = [RED, BLUE, GREEN, PURPLE, ORANGE, YELLOW, PINK]
        words = VGroup(
            *[
                Text(word, font_size=24)
                .next_to(items[2 * i][-1], OUT, buff=1.2)
                .rotate(62 * DEGREES, axis=RIGHT)
                .set_color(color_list[i])
                for i, word in enumerate(words_list)
            ]
        )
        items.save_state()
        self.playw(
            FadeIn(words, shift=OUT * 1.5),
            *[
                items[2 * i][-1].animate.set_color(color_list[i])
                for i in range(num_samples)
            ],
            *[items[2 * i][:-1].animate.set_color(GREY_D) for i in range(num_samples)],
            *[
                items[2 * i + 1].animate.set_color(GREY_D)
                for i in range(num_samples - 1)
            ],
        )

        ## restore
        self.playwl(
            FadeOut(words),
            self.cf.animate.restore(),
            items.animate.restore(),
            lag_ratio=0.5,
        )

        ## items opacity to softmax values
        items.save_state()
        items.generate_target()
        for i in range(num_samples):
            items.target[2 * i][-1].set_opacity(softmax_list_robust[i])
        self.playw(MoveToTarget(items))

        ## arrows to < 0.01
        arrows = VGroup(
            *[
                Arrow(
                    items[2 * i][-1].get_top() + UP * 1.2,
                    items[2 * i][-1].get_top(),
                    thickness=2.5,
                ).set_color(RED)
                for i in range(num_samples - 1)
                if softmax_list_robust[i] < 0.01
            ]
        )
        self.playw(FadeIn(arrows))

        ## restore again
        self.playw(items.animate.restore(), FadeOut(arrows))

        ## 3 heads
        head_rects = VGroup()
        items.generate_target()
        VGroup(*[items.target[2 * i][-1][-2:] for i in range(num_samples)]).set_opacity(
            0
        )
        VGroup(*[items.target[2 * i][:-1] for i in range(num_samples)]).set_opacity(0)
        VGroup(*[items.target[2 * i + 1] for i in range(num_samples - 1)]).set_opacity(
            0
        )
        for i in range(num_samples):
            item1 = items.target[2 * i][-1][:3].shift(UP * 0.2)
            item2 = items.target[2 * i][-1][3:6]
            item3 = items.target[2 * i][-1][6:9].shift(DOWN * 0.2)
            rect1 = SurroundingRectangle(item1).set_color(RED)
            rect2 = SurroundingRectangle(item2).set_color(BLUE)
            rect3 = SurroundingRectangle(item3).set_color(GREEN)
            head_rects.add(VGroup(rect1, rect2, rect3))
        self.play(MoveToTarget(items))
        self.playw(FadeIn(head_rects))

        ## 3 qk softmax
        def softmax(x):
            x = np.array(x)
            x = x - np.max(x)
            exp_x = np.exp(x)
            return exp_x / np.sum(exp_x)

        logits_num1 = [random.uniform(-3, 15) for _ in range(num_samples)]
        logits_num2 = [random.uniform(-3, 15) for _ in range(num_samples)]
        logits_num3 = [random.uniform(-3, 15) for _ in range(num_samples)]
        softmax_num1 = softmax(logits_num1)
        softmax_num2 = softmax(logits_num2)
        softmax_num3 = softmax(logits_num3)

        softmax1 = VGroup(
            *[
                Text("+" * bool(i) + str(round(x, 2)) + "·", font_size=20).next_to(
                    head_rects[i][0], LEFT
                )
                for i, x in enumerate(softmax_num1)
            ]
        )
        softmax2 = VGroup(
            *[
                Text("+" * bool(i) + str(round(x, 2)) + "·", font_size=20).next_to(
                    head_rects[i][1], LEFT
                )
                for i, x in enumerate(softmax_num2)
            ]
        )
        softmax3 = VGroup(
            *[
                Text("+" * bool(i) + str(round(x, 2)) + "·", font_size=20).next_to(
                    head_rects[i][2], LEFT
                )
                for i, x in enumerate(softmax_num3)
            ]
        )
        self.playw(FadeIn(softmax1), FadeIn(softmax2), FadeIn(softmax3))

        ## set opacity to each head
        items.generate_target()
        head_rects.generate_target()

        def theshold_opacity(value):
            return 0.85 if value > 0.4 else 0.4 if value > 0.2 else value

        for i in range(num_samples):
            items.target[2 * i][-1][:3].set_opacity(theshold_opacity(softmax_num1[i]))
            items.target[2 * i][-1][3:6].set_opacity(theshold_opacity(softmax_num2[i]))
            items.target[2 * i][-1][6:9].set_opacity(theshold_opacity(softmax_num3[i]))
            head_rects.target[i][0].set_stroke(
                opacity=theshold_opacity(softmax_num1[i])
            )
            head_rects.target[i][1].set_stroke(
                opacity=theshold_opacity(softmax_num2[i])
            )
            head_rects.target[i][2].set_stroke(
                opacity=theshold_opacity(softmax_num3[i])
            )
        self.playw(MoveToTarget(items), MoveToTarget(head_rects))

        ## rotate
        origs = VGroup(items, head_rects, softmax1, softmax2, softmax3)
        origs.save_state()
        self.playw(origs.animate.rotate(-PI / 2.5, axis=RIGHT).shift(DOWN))

        ## sentence
        words_list = ["What", "is", "the", "meaning", "of", "piui", "?"]
        words = VGroup(
            *[
                Text(word, font_size=24)
                .set_color(color_list[i])
                .next_to(items[2 * i][-1][:3], UP, buff=0.5)
                for i, word in enumerate(words_list)
            ]
        )
        self.playw(
            FadeIn(words),
            *[softmax1[i].animate.set_color(color_list[i]) for i in range(num_samples)],
            *[softmax2[i].animate.set_color(color_list[i]) for i in range(num_samples)],
            *[softmax3[i].animate.set_color(color_list[i]) for i in range(num_samples)],
        )

        ## restore to original vectors
        self.playw(
            Restore(origs),
            words.animate.arrange(RIGHT, buff=1.2).shift(UP * 2 + RIGHT * 0.3),
        )

        ## shrink to one vector
        vector = randn(9, 1).scale(0.35)
        vector[4].become(Text("...", font_size=24).move_to(vector[4]))
        self.playwl(
            AnimationGroup(
                *[
                    FadeOut(word, shift=words[3].get_center() - word.get_center())
                    for word in words
                ],
                *[
                    FadeOut(
                        softmax1[i],
                        shift=softmax1[3].get_center() - softmax1[i].get_center(),
                    )
                    for i in range(num_samples)
                ],
                *[
                    FadeOut(
                        softmax2[i],
                        shift=softmax2[3].get_center() - softmax2[i].get_center(),
                    )
                    for i in range(num_samples)
                ],
                *[
                    FadeOut(
                        softmax3[i],
                        shift=softmax3[3].get_center() - softmax3[i].get_center(),
                    )
                    for i in range(num_samples)
                ],
                *[
                    FadeOut(
                        head_rects[i],
                        shift=head_rects[3].get_center() - head_rects[i].get_center(),
                    )
                    for i in range(num_samples)
                ],
                *[
                    FadeOut(
                        items[2 * i],
                        shift=items[6].get_center() - items[2 * i].get_center(),
                    )
                    for i in range(num_samples)
                ],
            ),
            FadeIn(vector),
            lag_ratio=0.5,
        )

        ## shape
        shape = Tex("\\in R^{d_k}", font_size=36)
        self.playw(FadeIn(shape.next_to(vector, RIGHT, buff=0.5)))

        ## different colors
        colors = [RED, GREEN_E, PINK]
        self.playw(
            vector[:3].animate.set_color(colors[0]),
            vector[3:6].animate.set_color(colors[1]),
            vector[6:9].animate.set_color(colors[2]),
        )


def three_piece_tensor(num_samples, shape="square", arrange=DOWN, buff=0.2):
    tensor = Tensor(num_samples, shape=shape, arrange=arrange, buff=buff)
    t1 = VGroup(
        *[
            Rectangle(width=tensor[i].get_width(), height=tensor[i].get_height() / 3)
            .move_to(tensor[i])
            .align_to(tensor[i], UP)
            .set_color(tensor[i].get_color())
            .set_stroke(width=0)
            .set_fill(opacity=1)
            for i in range(num_samples)
        ]
    )
    t2 = VGroup(
        *[
            Rectangle(width=tensor[i].get_width(), height=tensor[i].get_height() / 3)
            .move_to(tensor[i])
            .set_color(tensor[i].get_color())
            .set_stroke(width=0)
            .set_fill(opacity=1)
            for i in range(num_samples)
        ]
    )
    t3 = VGroup(
        *[
            Rectangle(width=tensor[i].get_width(), height=tensor[i].get_height() / 3)
            .set_stroke(width=0)
            .move_to(tensor[i])
            .align_to(tensor[i], DOWN)
            .set_color(tensor[i].get_color())
            .set_fill(opacity=1)
            for i in range(num_samples)
        ]
    )
    return VGroup(t1, t2, t3)


def piece_tensor(num_samples, n_pieces=4, shape="square", arrange=DOWN, buff=0.2):
    tensor = Tensor(num_samples, shape=shape, arrange=arrange, buff=buff)
    pieces = VGroup(*[VGroup() for _ in range(num_samples)])
    for i in range(n_pieces):
        piece = VGroup(
            *[
                Rectangle(
                    width=tensor[j].get_width(),
                    height=tensor[j].get_height() / n_pieces,
                )
                .move_to(tensor[j])
                .set_stroke(width=0)
                .set_color(tensor[j].get_color())
                .set_fill(opacity=1)
                for j in range(num_samples)
            ]
        )

        for j in range(num_samples):
            pieces[j].add(piece[j])
    for j in range(num_samples):
        pj_center = pieces[j].copy()
        pieces[j].arrange(DOWN, buff=0).move_to(pj_center)

    return pieces


class multiheadAttnQK(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        num_samples = 7
        # query = Tensor(num_samples, shape="square", arrange=DOWN, buff=0.2)
        query = three_piece_tensor(num_samples, shape="square", arrange=DOWN, buff=0.2)
        # key = Tensor(num_samples, shape="square", arrange=RIGHT, buff=0.2)
        key = three_piece_tensor(num_samples, shape="square", arrange=RIGHT, buff=0.2)
        # value = Tensor(num_samples, shape="square", arrange=DOWN, buff=0.2)
        value = three_piece_tensor(num_samples, shape="square", arrange=DOWN, buff=0.2)

        logits = VGroup(
            *[
                Dot(radius=0.05).set_color(random_color())
                for _ in range(num_samples * num_samples)
            ]
        ).arrange_in_grid(buff=0.5, n_rows=num_samples, n_cols=num_samples)

        query.next_to(logits, LEFT, buff=0.5)
        key.next_to(logits, UP, buff=0.5)
        value.next_to(logits, RIGHT, buff=0.5)

        query_text = Text("Query", font="Noto Sans KR", font_size=20).next_to(
            query, DOWN, buff=0.15
        )
        key_text = Text("Key", font="Noto Sans KR", font_size=20).next_to(
            key, RIGHT, buff=0.15
        )
        value_text = Text("Value", font="Noto Sans KR", font_size=20).next_to(
            value, DOWN, buff=0.15
        )
        self.playw(
            FadeIn(query),
            FadeIn(key),
            FadeIn(query_text),
            FadeIn(key_text),
        )

        ## fade in logits
        self.playwl(
            AnimationGroup(
                FadeOut(query.copy(), shift=RIGHT),
                FadeOut(key.copy(), shift=DOWN),
            ),
            FadeIn(logits),
            lag_ratio=0.4,
        )

        ## fadeout logits
        self.playw(FadeOut(logits))

        ## set_strokes to 1 for query, key
        self.playw(
            query.animate.set_stroke(width=2, color=WHITE),
            key.animate.set_stroke(width=2, color=WHITE),
        )

        ## head1
        q_head1 = VGroup(*[query[0][i] for i in range(num_samples)])
        k_head1 = VGroup(*[key[0][i] for i in range(num_samples)])
        l_head1 = logits.copy()
        qh13 = q_head1[num_samples // 2].copy()
        kh13 = k_head1[num_samples // 2].copy()
        for i, l in enumerate(l_head1):
            l.set_color(random_color())
            l.next_to(logits[i], UP, buff=0.02)
        self.playwl(
            AnimationGroup(FadeOut(q_head1, shift=RIGHT), FadeOut(k_head1, shift=DOWN)),
            FadeIn(l_head1),
            lag_ratio=0.4,
            wait=0,
        )

        ## head2
        q_head2 = VGroup(*[query[1][i] for i in range(num_samples)])
        k_head2 = VGroup(*[key[1][i] for i in range(num_samples)])
        l_head2 = logits.copy()
        qh23 = q_head2[num_samples // 2].copy()
        kh23 = k_head2[num_samples // 2].copy()
        self.playwl(
            AnimationGroup(FadeOut(q_head2, shift=RIGHT), FadeOut(k_head2, shift=DOWN)),
            FadeIn(l_head2),
            lag_ratio=0.4,
            wait=0,
        )
        ## head3
        q_head3 = VGroup(*[query[2][i] for i in range(num_samples)])
        k_head3 = VGroup(*[key[2][i] for i in range(num_samples)])
        l_head3 = logits.copy()
        qh33 = q_head3[num_samples // 2].copy()
        kh33 = k_head3[num_samples // 2].copy()
        for i, l in enumerate(l_head3):
            l.set_color(random_color())
            l.next_to(logits[i], DOWN, buff=0.02)
        self.playwl(
            AnimationGroup(FadeOut(q_head3, shift=RIGHT), FadeOut(k_head3, shift=DOWN)),
            FadeIn(l_head3),
            lag_ratio=0.4,
        )

        ## explain with vectors
        heads = VGroup(l_head1, l_head2, l_head3)
        texts = VGroup(query_text, key_text)
        heads.save_state()
        texts.save_state()
        self.cf.save_state()
        self.play(
            self.cf.animate.reorient(
                0, 70, 0, (np.float32(-0.34), np.float32(0.41), np.float32(1.16)), 8.00
            ),
            heads.animate.set_opacity(0.2),
            texts.animate.set_opacity(0.2),
            FadeIn(VGroup(qh13, qh23, qh33, kh13, kh23, kh33)),
        )
        qh13_vec = (
            randn(1, 9)
            .scale(0.35)
            .rotate(70 * DEGREES, axis=RIGHT)
            .next_to(qh23, OUT, buff=0.5)
        )
        qh13_vec[4].become(
            Text("...", font_size=24)
            .rotate(70 * DEGREES, axis=RIGHT)
            .move_to(qh13_vec[4])
        )
        kh13_vec = (
            randn(9, 1)
            .scale(0.35)
            .rotate(70 * DEGREES, axis=RIGHT)
            .next_to(kh23, OUT, buff=0.5)
        )
        kh13_vec[4].become(
            Text("...", font_size=24)
            .rotate(70 * DEGREES, axis=RIGHT)
            .move_to(kh13_vec[4])
        )

        self.playw(FadeIn(VGroup(qh13_vec, kh13_vec)))
        self.play(qh13_vec.animate.next_to(kh13_vec, LEFT))

        ## 3 colors
        colors = [RED, GREEN, BLUE]
        self.playw(
            qh13_vec[:3].animate.set_color(colors[0]),
            kh13_vec[:3].animate.set_color(colors[0]),
            qh13_vec[3:6].animate.set_color(colors[1]),
            kh13_vec[3:6].animate.set_color(colors[1]),
            qh13_vec[6:].animate.set_color(colors[2]),
            kh13_vec[6:].animate.set_color(colors[2]),
        )

        ## multihead inner prod
        get_mult = (
            lambda: Text("·", font_size=24)
            .set_color(GREY_B)
            .rotate(70 * DEGREES, axis=RIGHT)
        )
        get_plus = (
            lambda: Text("+", font_size=24)
            .set_color(GREY_B)
            .rotate(70 * DEGREES, axis=RIGHT)
        )

        qh13_vec.generate_target()
        kh13_vec.generate_target()
        ms, ps = VGroup(), VGroup()
        row1 = VGroup()
        for i in range(3):
            m = get_mult()
            ms.add(m)
            row1.add(qh13_vec.target[i], m, kh13_vec.target[i])
            if i != 2:
                p = get_plus()
                ps.add(p)
                row1.add(p)
        row1.arrange(RIGHT, buff=0.1)
        row2 = VGroup()
        for i in range(3, 6):
            m = get_mult()
            ms.add(m)
            row2.add(qh13_vec.target[i], m, kh13_vec.target[i])
            if i != 5:
                p = get_plus()
                ps.add(p)
                row2.add(p)
        row2.arrange(RIGHT, buff=0.1)
        row3 = VGroup()
        for i in range(6, 9):
            m = get_mult()
            ms.add(m)
            row3.add(qh13_vec.target[i], m, kh13_vec.target[i])
            if i != 8:
                p = get_plus()
                ps.add(p)
                row3.add(p)
        row3.arrange(RIGHT, buff=0.1)
        rows = (
            VGroup(row1, row2, row3)
            .arrange(IN * np.sin(70 * DEGREES) + DOWN * np.cos(70 * DEGREES), buff=0.5)
            .next_to(kh13_vec, RIGHT, buff=0.5)
        )
        self.playw(
            MoveToTarget(qh13_vec), MoveToTarget(kh13_vec), FadeIn(ms), FadeIn(ps)
        )

        lh133 = l_head1[len(l_head1) // 2].copy().set_opacity(1)
        lh233 = l_head2[len(l_head2) // 2].copy().set_opacity(1)
        lh333 = l_head3[len(l_head3) // 2].copy().set_opacity(1)

        self.playw(
            FadeOut(qh13, shift=RIGHT * 2.5),
            FadeOut(kh13, shift=DOWN * 2.5),
            FadeIn(lh133),
            FadeOut(qh23, shift=RIGHT * 2.5),
            FadeOut(kh23, shift=DOWN * 2.5),
            FadeIn(lh233),
            FadeOut(qh33, shift=RIGHT * 2.5),
            FadeOut(kh33, shift=DOWN * 2.5),
            FadeIn(lh333),
        )

        ## restore to original cf
        self.play(
            FadeOut(qh13_vec),
            FadeOut(kh13_vec),
            FadeOut(ps),
            FadeOut(ms),
            FadeOut(VGroup(lh133, lh233, lh333)),
        )
        self.playw(Restore(self.cf), Restore(texts), Restore(heads))

        ## value
        self.playw(FadeIn(value), FadeIn(value_text))

        ## value stroke
        self.playw(value.animate.set_stroke(width=2, color=WHITE))

        value = VGroup(*[VGroup(a, b, c) for a, b, c in zip(*value)])
        ## inner product head
        get_mult = lambda: Text("·", font_size=24).set_color(GREY_B)
        get_plus = lambda: Text("+", font_size=24).set_color(GREY_B)

        l_head1.generate_target()
        l_head2.generate_target()
        l_head3.generate_target()

        values = VGroup(value, *[value.copy() for _ in range(num_samples - 1)])
        values.generate_target()
        rows = VGroup()
        mults, pluses = VGroup(), VGroup()
        for i in range(num_samples):
            ls = VGroup(
                *[
                    VGroup(a, b, c)
                    for a, b, c in zip(
                        l_head1.target[i * num_samples : (i + 1) * num_samples],
                        l_head2.target[i * num_samples : (i + 1) * num_samples],
                        l_head3.target[i * num_samples : (i + 1) * num_samples],
                    )
                ]
            )
            row = VGroup()
            for j, l in enumerate(ls):
                mult, plus = get_mult(), get_plus()
                mults.add(mult)
                if j < len(ls) - 1:
                    pluses.add(plus)
                item = VGroup(l, mult, values.target[i][j], plus).arrange(
                    RIGHT, buff=0.1
                )
                if j == len(ls) - 1:
                    item = item[:-1]
                row.add(item)
            row.arrange(RIGHT, buff=0.14)
            rows.add(row)
        rows.arrange(DOWN, buff=0.2)

        self.playw(
            MoveToTarget(l_head1),
            MoveToTarget(l_head2),
            MoveToTarget(l_head3),
            MoveToTarget(values),
            FadeIn(mults),
            FadeIn(pluses),
            FadeOut(VGroup(query_text, key_text, value_text)),
        )

        ## remain first row
        opa3 = lambda x: x.animate.set_opacity(0.1)
        l_head1.save_state()
        l_head2.save_state()
        l_head3.save_state()
        values.save_state()
        self.play(
            opa3(rows[1:]),
            opa3(l_head1[num_samples:]),
            opa3(l_head2[num_samples:]),
            opa3(l_head3[num_samples:]),
            opa3(values[1:]),
        )

        ## tex shape: H x d_k
        shape = Tex("\\in R^{H \\times \\frac{d_k}{H}}", font_size=36).next_to(rows[0], RIGHT)
        shape[2].set_color(RED)
        self.playw(FadeIn(shape))

        ## total shape: L x H x d_k
        self.play(
            FadeOut(shape),
            l_head1.animate.restore(),
            l_head2.animate.restore(),
            l_head3.animate.restore(),
            values.animate.restore(),
        )
        rect = SurroundingRectangle(
            VGroup(rows, l_head1, l_head2, l_head3, values), buff=0.15, stroke_width=1.5
        )
        total_shape = Tex("\\in R^{L \\times H \\times \\frac{d_k}{H}}", font_size=36).next_to(
            rect, RIGHT
        )
        self.playw(FadeIn(rect), FadeIn(total_shape))


class a_mha_gqa(InteractiveScene, Scene2D):
    def construct(self):
        shift_val = 0.75
        ## attention
        q = Tensor(4, shape="square", arrange=RIGHT).shift(DOWN * shift_val)
        q_tex = (
            Tex("q_{\\mathrm{attn}}", font_size=28)
            .next_to(q, LEFT, buff=0.1)
            .align_to(q, DOWN)
        )
        k = Tensor(4, shape="square", arrange=RIGHT).shift(UP * shift_val)
        k_tex = (
            Tex("k_{\\mathrm{attn}}", font_size=28)
            .next_to(k, LEFT, buff=0.1)
            .align_to(k, DOWN)
        )
        qk = VGroup(q, k, q_tex, k_tex)

        ## mha
        q_mha = (
            piece_tensor(4, n_pieces=4, arrange=RIGHT)
            .set_stroke(color=WHITE, width=1)
            .shift(DOWN * shift_val)
        )
        q_mha_tex = (
            Tex("q_{\\mathrm{mha}}", font_size=28)
            .next_to(q_mha, LEFT, buff=0.1)
            .align_to(q_mha, DOWN)
        )
        k_mha = (
            piece_tensor(4, n_pieces=4, arrange=RIGHT)
            .set_stroke(color=WHITE, width=1)
            .shift(UP * shift_val)
        )
        k_mha_tex = (
            Tex("k_{\\mathrm{mha}}", font_size=28)
            .next_to(k_mha, LEFT, buff=0.1)
            .align_to(k_mha, DOWN)
        )
        qk_mha = VGroup(q_mha, k_mha, q_mha_tex, k_mha_tex)

        ## gqa
        q_gqa = (
            piece_tensor(4, n_pieces=4, arrange=RIGHT)
            .set_stroke(color=WHITE, width=1)
            .shift(DOWN * shift_val)
        )
        q_gqa_tex = (
            Tex("q_{\\mathrm{gqa}}", font_size=28)
            .next_to(q_gqa, LEFT, buff=0.1)
            .align_to(q_mha_tex, DOWN)
        )
        k_gqa = (
            piece_tensor(4, n_pieces=4, arrange=RIGHT)
            .set_stroke(color=WHITE, width=1)
            .shift(UP * shift_val)
        )
        k_gqa_tex = (
            Tex("k_{\\mathrm{gqa}}", font_size=28)
            .next_to(k_gqa, LEFT, buff=0.1)
            .align_to(k_mha_tex, DOWN)
        )
        for k_piece in k_gqa:
            k_piece[0].set_opacity(0)
            k_piece[-1].set_opacity(0)

        qk_gqa = VGroup(q_gqa, k_gqa, q_gqa_tex, k_gqa_tex)

        ## arrange
        VGroup(qk, qk_mha, qk_gqa).arrange(RIGHT, buff=1.5)

        ## qk
        self.playw(FadeIn(qk))

        q0 = q[0]
        anims = []
        logits = VGroup()
        for i in range(4):
            path = BrokenLine(q0.get_center(), k[i].get_center(), q0.get_center())
            logit = (
                Dot(radius=0.05)
                .set_z_index(-1)
                .set_color(random_color())
                .next_to(k[i], UP, buff=0.5)
            )
            logits.add(logit)
            anims.append(
                AnimationGroup(
                    MoveAlongPath(q0, path),
                    AnimationGroup(FadeIn(logit, shift=UP * 0.8), Indicate(k[i])),
                    lag_ratio=0.25,
                )
            )

        for i, anim in enumerate(anims):
            self.play(anim, run_time=0.5 if i else 1)
        self.wait()

        ## qk_mha
        self.playw(FadeIn(qk_mha))

        q_mha0 = q_mha[0]
        anims = []
        logits_mha = VGroup()
        for i in range(4):
            for j in range(4):
                path = BrokenLine(
                    q_mha0[j].get_center(),
                    k_mha[i][j].get_center(),
                    q_mha0[j].get_center(),
                )
                logit = (
                    Dot(radius=0.05)
                    .set_z_index(-1)
                    .set_color(random_color())
                    .next_to(k_mha[i][j], UP, buff=0.5)
                )
                logits_mha.add(logit)
                anims.append(
                    AnimationGroup(
                        MoveAlongPath(q_mha0[j], path),
                        AnimationGroup(
                            FadeIn(logit, shift=UP * 0.8), Indicate(k_mha[i][j])
                        ),
                        lag_ratio=0.25,
                    )
                )

        for i, anim in enumerate(anims):
            self.play(anim, run_time=0.5 if i else 1)
        self.wait()

        ## qk_gqa
        self.playw(FadeIn(qk_gqa))

        q_gqa0 = q_gqa[0]
        anims = []
        logits_gqa = VGroup()
        for i in range(4):
            for j in range(4):
                idx = [1, 1, 2, 2]
                path = BrokenLine(
                    q_gqa0[j].get_center(),
                    k_gqa[i][idx[j]].get_center(),
                    q_gqa0[j].get_center(),
                )
                logit = (
                    Dot(radius=0.05)
                    .set_z_index(-1)
                    .set_color(random_color())
                    .next_to(k_gqa[i][j], UP, buff=0.5)
                )
                logits_gqa.add(logit)
                anims.append(
                    AnimationGroup(
                        MoveAlongPath(q_gqa0[j], path),
                        AnimationGroup(
                            FadeIn(logit, shift=UP * 0.8), Indicate(k_gqa[i][idx[j]])
                        ),
                        lag_ratio=0.25,
                    )
                )

        for i, anim in enumerate(anims):
            self.play(anim, run_time=0.5 if i else 1)
        self.wait()

        # 한 가지 관점, 여러 관점
        self.wait(5)

        ## camera
        self.playw(
            self.cf.animate.reorient(
                0, 0, 0, (np.float32(4.07), np.float32(0.13), np.float32(0.0)), 4.82
            ),
            FadeOut(VGroup(logits, logits_mha, qk, qk_mha)),
        )

        ## aspect1, aspect2
        aspect1 = (
            Text("Aspect 1", font_size=14)
            .next_to(k_gqa[-1][1], RIGHT, buff=0.5)
            .set_color_by_gradient(BLUE_A, BLUE_C)
        )
        aspect1_arrow = Arrow(
            aspect1.get_left(), k_gqa[-1][1].get_right(), thickness=1, buff=0.05
        ).set_color(BLUE)
        aspect2 = (
            Text("Aspect 2", font_size=14)
            .next_to(aspect1, DOWN, buff=0.2)
            .set_color_by_gradient(RED_A, RED_C)
        )
        aspect2_arrow = Arrow(
            aspect2.get_left(), k_gqa[-1][2].get_right(), thickness=1, buff=0.05
        ).set_color(RED)
        self.playwl(FadeIn(aspect1), GrowArrow(aspect1_arrow), lag_ratio=0.2)
        # self.playwl(FadeIn(aspect2), GrowArrow(aspect2_arrow), lag_ratio=0.2)

        self.playw(q_gqa0[2:].animate.set_opacity(0.2), q_gqa[1:].animate.set_opacity(0.2), k_gqa[-1][2].animate.set_opacity(0.2))

        # mha 설명: wait
        self.wait(5)

        ## gqa example - query: 4, kv: 2
        self.playw(q_gqa0[2:].animate.set_opacity(1), k_gqa[-1][2].animate.set_opacity(1))

        ## correspond
        group1q = q_gqa0[:2]
        group1k = k_gqa[-1][1]
        group2q = q_gqa0[2:]
        group2k = k_gqa[-1][2]

        group1 = VGroup(group1q, group1k)
        group2 = VGroup(group2q, group2k)
        group1.save_state()
        group2.save_state()
        group1.generate_target()
        group2.generate_target()
        group1.target.arrange(RIGHT, buff=0.35)
        group2.target.arrange(RIGHT, buff=0.35)

        VGroup(group1.target, group2.target).arrange(DOWN, buff=0.3).next_to(q_gqa, UP, buff=0.2)
        self.play(MoveToTarget(group1), MoveToTarget(group2))

        rect1 = SurroundingRectangle(group1, color=BLUE)
        rect2 = SurroundingRectangle(group2, color=RED)
        self.playw(ShowCreation(rect1), ShowCreation(rect2))

        ## restore
        self.play(FadeOut(rect1), FadeOut(rect2), run_time=0.5)
        self.playw(Restore(group1), Restore(group2), FadeOut(logits_gqa))

        self.embed()
        ## attn calculation
        path1 = BrokenLine(group1q[0].get_center(), group1k.get_center(), group1q[0].get_center())
        path2 = BrokenLine(group1q[-1].get_center(), group1k.get_center(), group1q[-1].get_center())

        self.playwl(MoveAlongPath(group1q[0], path1), AnimationGroup(Indicate(group1k), FadeIn(logits_gqa[-4], shift=UP)), lag_ratio=0.2, wait=0)
        self.playwl(MoveAlongPath(group1q[-1], path2), AnimationGroup(Indicate(group1k), FadeIn(logits_gqa[-3], shift=UP)), lag_ratio=0.2, wait=0)
        self.wait(5)

        ## value gqa
        v_gqa = (
            piece_tensor(4, n_pieces=4, arrange=RIGHT)
            .set_stroke(color=WHITE, width=1)
            .next_to(logits_gqa, UP, buff=0.5)
        )
        for v_piece in v_gqa:
            v_piece[0].set_opacity(0)
            v_piece[-1].set_opacity(0)
        v_gqa_tex = (
            Tex("v_{\\mathrm{gqa}}", font_size=28)
            .next_to(v_gqa, LEFT, buff=0.1)
        )
        self.playw(FadeIn(v_gqa), FadeIn(v_gqa_tex), self.cf.animate.scale(1.25).shift(UP * 0.5))