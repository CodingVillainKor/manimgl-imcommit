from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        vanilla_text = Text("Vanilla Attention:", font_size=24).set_color(RED)
        linear_text = Text("Linear Attention:", font_size=24).set_color(BLUE)

        texts = (
            VGroup(vanilla_text, linear_text)
            .arrange(DOWN, buff=0.5, aligned_edge=LEFT)
            .shift(LEFT)
        )

        ols = (
            Tex("O(L^2)", font_size=32)
            .next_to(texts[0], RIGHT, buff=0.5)
            .set_color(RED)
        )
        oln = (
            Tex("O(L)", font_size=32).next_to(texts[1], RIGHT, buff=0.5).set_color(BLUE)
        )

        self.playw(FadeIn(texts), FadeIn(ols), FadeIn(oln))

        ## fadeout oln, linear to down
        self.playw(FadeOut(oln, shift=DOWN), FadeOut(linear_text, shift=DOWN))

        ## qkv
        q = Tensor(9)
        k = Tensor(9, arrange=RIGHT, buff=0.2)
        v = Tensor(9)

        logit = VGroup(*[Tensor(9, shape="circle") for _ in range(9)]).arrange(
            RIGHT, buff=0.2
        )
        for t in logit:
            for item in t:
                item.scale(0.25).set_stroke(width=0)

        q.next_to(logit, LEFT, buff=0.8)
        k.next_to(logit, UP, buff=0.8)
        v.next_to(logit, RIGHT, buff=0.8)

        qt = Text("Query", font_size=20).next_to(q, DOWN, buff=0.15)
        kt = Text("Key", font_size=20).next_to(k, LEFT, buff=0.15)

        self.playw(FadeIn(q), FadeIn(k), FadeIn(qt), FadeIn(kt))

        ## context length
        bq = Brace(q, RIGHT)
        bl = Brace(k, DOWN)
        lq, lk = ols[2].copy(), ols[2].copy()
        self.play(
            lq.animate.next_to(bq, RIGHT, buff=0.1),
            lk.animate.next_to(bl, DOWN, buff=0.1),
        )
        self.playw(FadeIn(bq), FadeIn(bl))

        ## 제가 LA에 있을 때는 말이죠
        text = Words(
            "제가 LA에 있을 때는 말이죠 정말 제가 꿈의 ...", font_size=24
        ).set_color(GREY_C)
        for i, tw in enumerate(text.words):
            tw.next_to(q[i], LEFT, buff=0.1)
        self.playw(FadeIn(text))

        ## fadeout text and re fadein linear
        self.play(FadeOut(text))
        self.play(FadeIn(linear_text), FadeIn(oln), run_time=0.5)
        self.playw(FlashUnder(VGroup(linear_text, oln), color=BLUE))

        ## circumscribe ols
        self.playw(
            Circumscribe(ols, color=RED),
            Indicate(ols, color=PURE_RED, scale_factor=1.1),
        )

        ## fadeout ols, oln, text
        softmax_tex = Tex("\\text{Softmax}(\\frac{QK^T}{\\sqrt{d}})", font_size=36)
        softmax_tex.next_to(logit, RIGHT, buff=0.5)
        self.play(
            FadeOut(ols),
            FadeOut(oln),
            FadeOut(linear_text),
            FadeOut(vanilla_text),
            run_time=0.75,
        )
        self.playw(
            FadeOut(q.copy(), shift=RIGHT * 2),
            FadeOut(k.copy(), shift=DOWN * 2),
            FadeIn(logit),
            FadeIn(softmax_tex),
        )

        ## qk, logit's opacity to 0.3 and explain shape
        qklogit = VGroup(q, k, logit, qt, kt, bq, bl, lq, lk)
        texq = softmax_tex[8]
        texkt = softmax_tex[9:11]
        self.play(
            qklogit.animate.set_opacity(0.3),
            texq.animate.set_color(ORANGE),
            texkt.animate.set_color(GREEN),
        )

        qshape = Tex("(L, D)", font_size=28).set_color(ORANGE)
        ktshape = Tex("(D, L)", font_size=28).set_color(GREEN)
        shapes = (
            VGroup(qshape, ktshape)
            .arrange(RIGHT)
            .next_to(VGroup(texq, texkt), UP, buff=0.15)
        )
        self.playw(
            FadeIn(qshape, scale=1.5, shift=qshape.get_center() - texq.get_center())
        )
        self.playw(
            FadeIn(ktshape, scale=1.5, shift=ktshape.get_center() - texkt.get_center())
        )

        logitshape = Tex("(L, L)", font_size=28).set_color(BLUE).move_to(shapes)
        self.playw(
            Transformr(qshape[:3], logitshape[:3]),
            Transformr(ktshape[3:], logitshape[3:]),
            FadeOut(qshape[3:], shift=UP),
            FadeOut(ktshape[:3], shift=UP),
        )

        ## have logit opacity 1
        self.playw(logit.animate.set_opacity(1))

        def cover_exp(item, font_size=20):
            exp1 = Tex("\\text{exp}(", font_size=font_size).next_to(
                item, LEFT, buff=0.05
            )
            exp2 = Tex(")", font_size=font_size).next_to(item, RIGHT, buff=0.05)
            return VGroup(exp1, exp2).set_color(GREY_B)

        exps = VGroup(*[cover_exp(l) for item in logit for l in item])
        self.playw(FadeIn(exps))

        ## vanilla
        vanilla = (
            VGroup(vanilla_text, ols)
            .arrange(RIGHT, buff=0.3)
            .next_to(softmax_tex, DOWN, buff=0.75, aligned_edge=LEFT)
        )
        self.playw(FadeIn(vanilla))

        ## linear
        linear_ = (
            VGroup(linear_text, oln)
            .arrange(RIGHT, buff=0.3)
            .next_to(vanilla, DOWN, buff=0.35, aligned_edge=LEFT)
        )
        self.play(FadeIn(linear_))
        self.playw(RWiggle(linear_, amp=0.15, speed=6))


class associativeLawAttn(InteractiveScene, Scene2D):
    def construct(self):

        ## associative law explanation
        sm_tex = Tex(
            "\\text{Attention}(Q, K, V) = \\text{Softmax}(\\frac{QK^T}{\\sqrt{D}})V",
            font_size=40,
        )
        self.playw(FadeIn(sm_tex[:17]))
        qtex = sm_tex[25].set_color(ORANGE)
        ktex = sm_tex[26].set_color(GREEN)
        vtex = sm_tex[-1].set_color(BLUE)
        self.playw(FadeIn(sm_tex[17:]))

        ## shapes are (L, D) for all
        qshape = Tex("(L, D)", font_size=28).set_color(ORANGE)
        kshape = Tex("(L, D)", font_size=28).set_color(GREEN)
        vshape = Tex("(L, D)", font_size=28).set_color(BLUE)
        shapes = (
            VGroup(qshape, kshape, vshape)
            .arrange(RIGHT)
            .next_to(sm_tex[26], UP, buff=0.35)
        )
        lines = VGroup(
            *[
                DashedLine(t.get_top(), s.get_bottom(), color=c)
                for t, s, c in zip([qtex, ktex, vtex], shapes, [ORANGE, GREEN, BLUE])
            ]
        )
        self.playw(FadeIn(shapes), *[Create(line) for line in lines])

        ## circumscribe KT
        transtex = sm_tex[27]
        self.playw(Circumscribe(VGroup(ktex, transtex), color=GREEN))

        ## switch the order of kshape
        kst1_path = BrokenLine(
            kshape[1].get_center(),
            (kshape[1].get_center() + kshape[3].get_center()) / 2 + UP * 0.25,
            kshape[3].get_center(),
            smooth=True,
        )
        kst3_path = BrokenLine(
            kshape[3].get_center(),
            (kshape[1].get_center() + kshape[3].get_center()) / 2 + DOWN * 0.25,
            kshape[1].get_center(),
            smooth=True,
        )
        self.play(
            MoveAlongPath(kshape[1], kst1_path),
            MoveAlongPath(kshape[3], kst3_path),
            transtex.animate.set_color(GREEN),
        )

        self.playwl(*[FlashUnder(shape, buff=0.05) for shape in shapes], lag_ratio=0.7)

        ## sr kv
        sr_kv = SurroundingRectangle(VGroup(kshape, vshape), color=YELLOW)
        self.playw(Create(sr_kv))

        ## D, D
        d_tex = Tex("(D, D)", font_size=28).set_color(YELLOW_B)
        d_tex.next_to(sr_kv, UP, buff=0.2)
        self.playw(
            Transformr(VGroup(kshape[0], kshape[-2], kshape[2]).copy(), d_tex[:3]),
            Transformr(vshape[3:].copy(), d_tex[3:]),
            VGroup(kshape[1], kshape[-1], vshape[:3]).animate.set_opacity(0.3),
        )

        ## shift up q
        lineq = lines[0]
        lineq.add_updater(
            lambda l: l.put_start_and_end_on(qtex.get_top(), qshape.get_bottom())
        )
        self.playw(qshape.animate.align_to(d_tex, UP))
        lineq.clear_updaters()

        ## sr q - d_tex
        sr_q = SurroundingRectangle(VGroup(qshape, d_tex), color=PURPLE)
        self.playw(Create(sr_q))

        ## L, D
        l_tex = Tex("(L, D)", font_size=28).set_color(PURPLE)
        l_tex.next_to(sr_q, UP, buff=0.2)
        self.playw(
            Transformr(qshape[:3].copy(), l_tex[:3]),
            Transformr(d_tex[3:].copy(), l_tex[3:]),
            VGroup(qshape[3:], d_tex[:3]).animate.set_opacity(0.3),
        )

        ## dtex

        ol = self.overlay
        self.add(d_tex.set_z_index(ol.z_index + 1))
        self.playw(FadeIn(ol), d_tex.animate.set_opacity(1))

        self.play(FadeOut(ol))
        self.playw(Circumscribe(sr_q, buff=0))

        ## L, D again
        self.play(d_tex[:3].animate.set_opacity(0.3))
        self.playw(Indicate(l_tex, scale_factor=1))

        ## overlay again

        self.play(FadeIn(ol), d_tex.animate.set_opacity(1))

        self.playw(RWiggle(d_tex, amp=0.1, speed=5, run_time=4))


class softmaxNotAssociative(InteractiveScene, Scene2D):
    def construct(self):

        ## softmax
        sm_tex = Tex(
            "\\text{softmax}(Q K^T) = "
            "\\frac{\\text{exp}(Q K^T)}"
            "{\\sum_{j=1}^{L} \\text{exp}(Q k_j)}",
            font_size=32,
        )
        self.playw(FadeIn(sm_tex))

        ## exps
        exp1 = sm_tex[13:16]
        exp2 = sm_tex[27:30]
        self.playw(
            VGroup(sm_tex[:13], sm_tex[16:27], sm_tex[30:]).animate.set_opacity(0.3),
            exp1.animate.set_color(RED),
            exp2.animate.set_color(RED),
        )

        ## qkt
        qkt = sm_tex[17:20]
        self.playw(
            qkt.animate.set_opacity(1).set_color(YELLOW),
            VGroup(exp1, exp2).animate.set_opacity(0.3),
        )

        ## shift up
        self.play(sm_tex.animate.scale(0.75).shift(RIGHT * 5), run_time=0.75)

        ## qk logit
        q = Tensor(9)
        k = Tensor(9, arrange=RIGHT, buff=0.2)
        v = Tensor(9)

        logit = VGroup(*[Tensor(9, shape="circle") for _ in range(9)]).arrange(
            RIGHT, buff=0.2
        )
        for t in logit:
            for item in t:
                item.scale(0.25).set_stroke(width=0)

        q.next_to(logit, LEFT, buff=0.8)
        k.next_to(logit, UP, buff=0.8)
        v.next_to(logit, RIGHT, buff=0.8)

        qt = Text("Query", font_size=20).next_to(q, DOWN, buff=0.15)
        kt = Text("Key", font_size=20).next_to(k, LEFT, buff=0.15)

        self.play(FadeIn(VGroup(q, k, logit, qt, kt)))

        ## exps
        def cover_exp(item, font_size=18):
            exp1 = Tex("\\text{exp}(", font_size=font_size).next_to(
                item, LEFT, buff=0.05
            )
            exp2 = Tex(")", font_size=font_size).next_to(item, RIGHT, buff=0.05)
            return VGroup(exp1, exp2).set_color(GREY_B)

        exps = VGroup(*[cover_exp(dot) for tensor in logit for dot in tensor])
        self.playw(FadeIn(exps))

        ## camera
        self.cf.save_state()
        self.play(
            self.cf.animate.reorient(
                0, 74, 0, (np.float32(-2.71), np.float32(2.32), np.float32(0.21)), 1.83
            )
        )

        ## shift out exp1, q0, k0
        exp1 = VGroup(exps[0], logit[0][0])
        q0, k0 = q[0], k[0]
        exp1.save_state()
        q0.save_state()
        k0.save_state()
        self.play(
            VGroup(exp1, q0, k0)
            .animate.arrange(RIGHT, buff=0.4)
            .move_to(exp1)
            .shift(OUT * 0.5 + UP * 1.5)
            .rotate(74 * DEGREES, axis=RIGHT)
        )

        self.playw(Indicate(exp1, scale_factor=1.2))

        ## cover fn
        def cover_fn(item, string="f", font_size=18):
            pre_f = Tex(f"\\text{{{string}}}(", font_size=font_size).next_to(
                item, LEFT, buff=0.05
            )
            post_f = Tex(")", font_size=font_size).next_to(item, RIGHT, buff=0.05)
            return VGroup(pre_f, post_f).set_color(GREY_B)

        q_f = cover_fn(q0, string="f").rotate(74 * DEGREES, axis=RIGHT)
        k_f = cover_fn(k0, string="g").rotate(74 * DEGREES, axis=RIGHT)
        eq = (
            Text("=", font_size=18)
            .next_to(VGroup(q_f, k_f), LEFT, buff=0.07)
            .rotate(74 * DEGREES, axis=RIGHT)
            .set_color(GREY_C)
        )
        self.playw(FadeIn(VGroup(q_f, k_f, eq)), wait=4)

        ## return to original state
        self.play(
            Restore(exp1),
            Restore(q0),
            Restore(k0),
            FadeOut(VGroup(q_f, k_f, eq)),
            run_time=0.75,
        )
        self.playw(Restore(self.cf))

        ## exp graph

        ol = self.overlay
        nump = (
            RaenimPlane(x_range=[-4, 1.8], y_range=[-2, 6], width=16, height=12)
            .scale(0.4)
            .set_z_index(ol.z_index + 1)
        )
        exp_graph = nump.get_graph(
            lambda x: np.exp(x), color=BLUE, x_range=[-4, 1.8]
        ).set_z_index(ol.z_index + 1)
        exp_text = (
            Tex("y = e^x", font_size=32)
            .next_to(exp_graph, UR)
            .set_z_index(ol.z_index + 1)
            .set_color(BLUE)
        )
        self.playw(FadeIn(ol), FadeIn(nump), FadeIn(exp_graph), FadeIn(exp_text))

        ## fadeout right before items
        self.playw(FadeOut(nump), FadeOut(exp_graph), FadeOut(exp_text), FadeOut(ol))

        ## exp, items
        flattened_dots = VGroup(*[dot for tensor in logit for dot in tensor])
        exp_items = VGroup(
            *[VGroup(dot, exp) for dot, exp in zip(flattened_dots, exps)]
        )

        logit_nums = VGroup(
            *[
                DecimalNumber(
                    num := random.random() * 10 - 3, font_size=12, num_decimal_places=1
                )
                .set_color(WHITE if num >= 0 else RED)
                .move_to(dot.get_center())
                for dot in flattened_dots
            ]
        )
        self.playw(Transform(flattened_dots, logit_nums))

        ## rwiggle negative numbers
        self.playw(
            *[
                RWiggle(fdot, amp=0.1, speed=5)
                for item, fdot in zip(logit_nums, flattened_dots)
                if float(item.get_value()) < 0
            ]
        )

        ## exps to PURPLE

        self.play(flattened_dots.animate.set_opacity(0.3))
        self.playw(exps.animate.set_color(PURPLE))


class LinearAttention(InteractiveScene, Scene2D):
    def construct(self):

        ## exp QK
        expqk = Tex("\\exp(QK^T)", font_size=32)

        self.playw(FadeIn(expqk))

        self.playw(
            expqk[:3].animate.set_color(RED),
            expqk[3:].animate.set_opacity(0.3),
            FlashUnder(expqk[:3], color=RED),
        )

        ## shift up
        self.play(expqk.animate.shift(UP), run_time=0.5)

        ## linear attention is hidden
        linearattn = Tex("\\phi(Q) \\phi(K)^T V", font_size=32).set_z_index(-1)

        hidden_box = (
            SurroundingRectangle(linearattn[:9], buff=0.02)
            .set_stroke(color=WHITE, width=1)
            .set_fill(BLACK, opacity=1)
        )
        self.playw(FadeIn(linearattn[-1]), FadeIn(hidden_box))
        self.add(linearattn)

        ## disentangle K
        k_part = (
            linearattn[4:9].copy().set_z_index(1)
        )  # Assuming \phi(K)^T is at positions 4 to 8
        self.playw(FadeIn(k_part), run_time=0.5)

        ## associative about K, V
        kv_part = linearattn[4:]
        sr_kv = SurroundingRectangle(kv_part, buff=0.1).set_stroke(color=GREEN, width=2)
        self.playw(FadeIn(sr_kv), hidden_box.animate.set_stroke(opacity=0.3))

        ## camera
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(
                -90,
                73,
                90,
                (np.float32(3.03), np.float32(0.18), np.float32(3.15)),
                8.00,
            ),
            wait=4,
        )

        ## restore camera
        self.playw(Restore(self.cf))

        ## remove the boxes
        self.playw(FadeOut(sr_kv), FadeOut(hidden_box))

        ## function first
        self.remove(k_part)
        self.playw(
            Indicate(linearattn[0]),
            Indicate(linearattn[4]),
            VGroup(linearattn[1:4], linearattn[5:])
            .animate(rate_func=there_and_back)
            .set_opacity(0.2),
            wait=2,
        )

        ## qk first
        self.play(FlashUnder(linearattn[:9], buff=0.05))

        linear_out1 = Tex("(\\phi_Q \\phi_K^T) V", font_size=32).next_to(
            linearattn, DOWN, aligned_edge=LEFT
        )
        self.play(Transformr(linearattn[:9].copy(), linear_out1[:-1]))
        self.playw(Transformr(linearattn[-1].copy(), linear_out1[-1]))

        ## indicate linear_out1
        self.playw(Indicate(linear_out1[:-1], scale_factor=1, color=PURE_BLUE))

        ## flashunder whole linear_out1
        self.playw(FlashUnder(linear_out1))

        ## fadeout linear_out1
        self.playw(FadeOut(linear_out1, shift=DOWN))

        ## q, k func
        self.playw(
            Indicate(linearattn[0]),
            Indicate(linearattn[4]),
            VGroup(linearattn[1:4], linearattn[5:])
            .animate(rate_func=there_and_back)
            .set_opacity(0.2),
            wait=2,
        )

        ## kv first

        self.playw(
            linearattn[:4].animate.set_opacity(0.3),
            Indicate(linearattn[4:], scale_factor=1, color=PURE_BLUE, run_time=2),
        )

        ## q, kv
        funcq = linearattn[:4].copy()
        funcq_kv = Tex("\\phi(Q)(\\phi_K^T V)", font_size=32).next_to(
            linearattn, DOWN, aligned_edge=LEFT
        )

        self.playw(
            Transformr(funcq, funcq_kv[:4]),
            Transformr(linearattn[4:].copy(), funcq_kv[5:-1]),
            FadeIn(VGroup(funcq_kv[4], funcq_kv[-1])),
        )

        ## kv is D x D
        sr_kv = SurroundingRectangle(funcq_kv[4:], buff=0.1).set_stroke(
            color=GREEN, width=2
        )
        self.play(FadeIn(sr_kv), funcq_kv[:4].animate.set_opacity(0.3))

        shape = (
            Tex("D \\times D", font_size=32)
            .set_color(GREEN)
            .next_to(funcq_kv[4:], DOWN, aligned_edge=LEFT)
        )
        self.playw(FadeIn(shape, shift=DOWN * 0.3))

        ## cal q
        self.play(
            funcq_kv[:4].animate.shift(LEFT * 0.2).set_opacity(1).set_color(BLUE),
            run_time=0.75,
        )
        qshape = (
            Tex("L \\times D", font_size=32).set_color(BLUE).next_to(funcq_kv[:4], DOWN)
        )
        self.playw(FadeIn(qshape, shift=DOWN * 0.3))

        ## result: L x D
        result_shape = (
            Tex("L \\times D", font_size=32)
            .set_color(YELLOW)
            .next_to(funcq_kv, DOWN)
            .set_color_by_gradient(BLUE, GREEN)
        )
        self.playw(
            FadeOut(qshape[2:], shift=DOWN * 0.5),
            FadeOut(shape[:2], shift=DOWN * 0.5),
            Transformr(VGroup(*qshape[:2], shape[2]), result_shape),
        )

        ## overlay result
        ol = self.overlay
        self.add(result_shape.set_z_index(ol.z_index + 1))
        self.play(FadeIn(ol), result_shape.animate.scale(1.2), run_time=0.5)
        self.playw(RWiggle(result_shape, amp=0.2, speed=2))


class conditionOfPhi(InteractiveScene, Scene2D):
    def construct(self):

        ## tex
        tex = Tex("\\phi(Q)\\phi(K)^T V", font_size=40)

        self.playw(FadeIn(tex))

        ## shift up and remain phi func
        self.play(VGroup(tex[2], tex[6], tex[8:]).animate.set_opacity(0.2))

        func = Tex("\\phi(\\cdot)").set_color(GREEN)
        self.playw(tex.animate.shift(UP * 2), Transformr(tex[:4].copy(), func))

        ## mathbb R
        func_r = Tex(
            "\\text{sim}(q, k): \\mathbb{R}^{2 \\times D} \\to \\mathbb{R}_{+}",
            font_size=32,
        ).next_to(tex, DOWN, aligned_edge=LEFT)
        self.playw(FadeIn(func_r), wait=4)

        ## func: R -> R+
        func_phi = (
            (Tex("\\phi: \\mathbb{R} \\to \\mathbb{R}_{+}", font_size=36))
            .next_to(func, DOWN, aligned_edge=LEFT)
            .set_color(GREEN_B)
        )
        self.playw(FadeIn(func_phi), wait=4)

        ## camera up
        self.playw(
            self.cf.animate.shift(UP * 2),
            FadeOut(VGroup(func_phi, func)),
            tex[:-1].animate.set_opacity(1).set_color(BLUE),
            func_r.animate.set_color(BLUE),
        )


class LinearAttention2(InteractiveScene, Scene2D):
    def construct(self):

        ## exp QK
        expqk = Tex("\\exp(QK^T)", font_size=32)

        self.playw(FadeIn(expqk))

        self.playw(
            expqk[:3].animate.set_color(RED),
            expqk[3:].animate.set_opacity(0.3),
            FlashUnder(expqk[:3], color=RED),
        )

        ## shift up
        self.play(expqk.animate.shift(UP), run_time=0.5)

        ## linear attention is hidden
        linearattn = Tex("\\phi(Q) \\phi(K)^T V", font_size=32).set_z_index(-1)

        hidden_box = (
            SurroundingRectangle(linearattn[:9], buff=0.02)
            .set_stroke(color=WHITE, width=1)
            .set_fill(BLACK, opacity=1)
        )
        self.playw(FadeIn(linearattn[-1]), FadeIn(hidden_box))
        self.add(linearattn)

        ## disentangle K
        k_part = (
            linearattn[4:9].copy().set_z_index(1)
        )  # Assuming \phi(K)^T is at positions 4 to 8
        self.playw(FadeIn(k_part), run_time=0.5)

        ## associative about K, V
        kv_part = linearattn[4:]
        sr_kv = SurroundingRectangle(kv_part, buff=0.1).set_stroke(color=GREEN, width=2)
        self.playw(FadeIn(sr_kv), hidden_box.animate.set_stroke(opacity=0.3))

        ## camera
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(
                -90,
                73,
                90,
                (np.float32(3.03), np.float32(0.18), np.float32(3.15)),
                8.00,
            ),
            wait=4,
        )

        ## restore camera
        self.playw(Restore(self.cf))

        ## remove the boxes
        self.play(FadeOut(sr_kv), FadeOut(hidden_box), FadeOut(expqk))
        self.remove(k_part)
        self.playw(linearattn.animate.shift(UP*3 + RIGHT * 5))

        ## q, k, logit, v
        q = Tensor(9)
        k = Tensor(9, arrange=RIGHT, buff=0.2)
        v = Tensor(9)

        logit = VGroup(*[Tensor(9, shape="circle") for _ in range(9)]).arrange(
            RIGHT, buff=0.2
        )
        for t in logit:
            for item in t:
                item.scale(0.25).set_stroke(width=0)

        q.next_to(logit, LEFT, buff=0.8)
        k.next_to(logit, UP, buff=0.8)
        v.next_to(logit, RIGHT, buff=0.8)

        qt = Text("Query", font_size=20).next_to(q, DOWN, buff=0.15)
        kt = Text("Key", font_size=20).next_to(k, LEFT, buff=0.15)

        self.playw(FadeIn(q), FadeIn(k), FadeIn(qt), FadeIn(kt))

        ## q
        q.save_state()
        fq = Tensor(9, shape="circle").move_to(q).set_stroke(color=GREY_C)
        self.play(Transform(q, fq))
        self.play(Circumscribe(linearattn[:4]))

        ## k
        k.save_state()
        fk = Tensor(9, shape="circle", arrange=RIGHT, buff=0.2).move_to(k).set_stroke(color=GREY_C)
        self.play(Transform(k, fk), run_time=0.5)
        self.playw(Circumscribe(linearattn[4:9]), run_time=0.5)

        ## logit
        self.play(
            FadeOut(q.copy(), shift=RIGHT * 2),
            FadeOut(k.copy(), shift=DOWN * 2),
            FadeIn(logit),
        )
        self.play(Circumscribe(linearattn[:9]))
        lines = VGroup(*[Line(l[0].get_center(), l[-1].get_center()) for l in logit]).set_color(YELLOW)
        self.play(FadeIn(lines), run_time=0.5)
        self.playw(FadeOut(lines), run_time=0.5)

        ## v
        vt = Text("Value", font_size=20).next_to(v, DOWN, buff=0.15)
        self.play(FadeIn(v), FadeIn(vt))

        ## restore
        self.playw(Restore(q), Restore(k), FadeOut(logit))

        ## fq, fk
        self.play(Transform(q, fq), Transform(k, fk), run_time=0.75)
        self.playw(Circumscribe(linearattn[:4]), Circumscribe(linearattn[4:9]), run_time=0.75)

        ## DD bunch
        kv = Tensor(1).scale(2).move_to(logit)
        self.playw(Transformr(VGroup(k.copy(), v), kv), FadeOut(vt, shift=LEFT))
        
        self.embed()
        ## kv shape
        kv_shape = Tex("D \\times D", font_size=24).next_to(kv, DOWN).set_color(kv.get_color())
        self.playw(FadeIn(kv_shape))

        ## o
        o = Tensor(9).next_to(logit, RIGHT, buff=0.8)
        ot = Text("Output", font_size=20).next_to(o, DOWN, buff=0.15)
        self.playwl(
            *[
                FadeTransform(VGroup(q[i].copy(), kv.copy()), o[i]) for i in range(9)
            ], FadeIn(ot), lag_ratio=0.35
        )