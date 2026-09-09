from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class compare(InteractiveScene, Scene2D):
    def construct(self):
        OL = LEFT * 7.1111111111 / 2
        OR = RIGHT * 7.1111111111 / 2
        ## intro
        midline = DashedLine(UP * 10, DOWN * 10, color=GREY_D)
        self.add(midline)

        ## vanilla vs linear
        tshift = 3
        vt = (
            Text("Vanilla attention", font_size=24)
            .set_color(GREY_B)
            .move_to(OL)
            .shift(UP * tshift)
        )
        attn1 = Tex(r"\text{softmax}(\frac{QK^T}{\sqrt{D}})V", font_size=40).move_to(OL)
        lt = (
            Text("Linear attention", font_size=24)
            .set_color(GREY_B)
            .move_to(OR)
            .shift(UP * tshift)
        )
        attn2 = Tex(r"\phi(Q)\phi(K)^T V", font_size=40).move_to(OR)

        attn1[8:11].set_color(RED)
        qkt_box = SurroundingRectangle(attn1[8:11], color=RED, buff=0.05)
        qkt_shape = (
            Tex("L \\times L", font_size=36)
            .next_to(qkt_box, UP, buff=0.5)
            .set_color(RED)
        )
        qkt_line = DashedLine(qkt_box.get_top(), qkt_shape.get_bottom(), color=RED)

        llv_box = SurroundingRectangle(qkt_shape, color=PURPLE, buff=0.05)
        llv_shape = (
            Tex("L \\times D", font_size=36)
            .next_to(llv_box, RIGHT, buff=0.5)
            .set_color(PURPLE)
        )
        ll_line = DashedLine(llv_box.get_right(), llv_shape.get_left(), color=PURPLE)
        v_line = DashedLine(attn1[-1].get_top(), llv_shape.get_bottom(), color=PURPLE)

        # linear
        kv_box = SurroundingRectangle(attn2[4:], color=BLUE, buff=0.05)
        kv_shape = (
            Tex("D \\times D", font_size=36)
            .next_to(kv_box, UP, buff=0.5)
            .set_color(BLUE)
        )
        kv_line = DashedLine(kv_box.get_top(), kv_shape.get_bottom(), color=BLUE)
        qdd_box = SurroundingRectangle(kv_shape, color=PURPLE, buff=0.05)
        qdd_shape = (
            Tex("L \\times D", font_size=36)
            .next_to(qdd_box, LEFT, buff=0.5)
            .set_color(PURPLE)
        )
        dd_line = DashedLine(qdd_box.get_left(), qdd_shape.get_right(), color=PURPLE)
        q_line = DashedLine(attn2[0].get_top(), qdd_shape.get_bottom(), color=PURPLE)

        self.addw(
            vt,
            attn1,
            lt,
            attn2,
            qkt_box,
            qkt_shape,
            qkt_line,
            llv_box,
            llv_shape,
            ll_line,
            v_line,
            kv_box,
            kv_shape,
            kv_line,
            qdd_box,
            qdd_shape,
            dd_line,
            q_line,
        )

        ## circumscribe L x L
        ol = self.overlay
        self.playw(
            Indicate(
                qkt_shape.set_z_index(ol.z_index + 1), color=YELLOW, scale_factor=1.1
            ),
            FadeIn(ol, rate_func=there_and_back),
            run_time=2,
        )

        ## circumscribe D x D
        ol.set_opacity(0)
        ol = self.overlay
        self.add(qdd_shape.set_z_index(ol.z_index + 1))
        self.add(qkt_shape.set_z_index(0))
        self.playw(
            Indicate(qdd_shape, color=YELLOW, scale_factor=1.1),
            ol.animate(rate_func=there_and_back).set_opacity(0.7),
            run_time=2,
        )

        ## L ~= 1M
        l1m_tex = (
            Tex("L \\approx 1M", font_size=36)
            .next_to(qkt_shape, UP, buff=0.3, aligned_edge=LEFT)
            .set_color(RED)
        )
        self.play(FadeIn(l1m_tex))

        self.playw(RWiggle(l1m_tex, amp=0.3, speed=5))


class linearAttnWeight(InteractiveScene, Scene2D):
    def construct(self):

        ## linear attn tex
        tex = Tex(r"\phi(Q)\phi(K)^T V", font_size=36)

        kv_box = SurroundingRectangle(tex[4:], color=BLUE, buff=0.05)
        self.playw(FadeIn(tex))
        self.play(Create(kv_box), tex[:4].animate.shift(LEFT * 0.1).set_color(GREEN_B))

        ## kv shape
        kv_shape = (
            Tex("D \\times D", font_size=36)
            .next_to(kv_box, UP, buff=0.5)
            .set_color(BLUE)
        )
        kv_line = DashedLine(kv_box.get_top(), kv_shape.get_bottom(), color=BLUE)
        self.playw(FadeIn(kv_shape), Create(kv_line))

        ## q shape
        q_box = SurroundingRectangle(tex[:4], color=GREEN_B, buff=0.05)
        self.play(Create(q_box))
        q_shape = (
            Tex("L \\times D", font_size=36)
            .next_to(q_box, UP, buff=0.5)
            .set_color(GREEN_B)
        )
        q_line = DashedLine(q_box.get_top(), q_shape.get_bottom(), color=GREEN_B)
        self.playw(FadeIn(q_shape), Create(q_line))

        ## ld
        ld_tex = (
            Tex("L \\times D", font_size=36)
            .next_to(VGroup(q_shape, kv_shape), UP, buff=0.5)
            .set_color(PURPLE)
        )
        ld_line1 = DashedLine(q_shape.get_top(), ld_tex, color=PURPLE)
        ld_line2 = DashedLine(kv_shape.get_top(), ld_tex, color=PURPLE)
        self.playw(FadeIn(ld_tex), Create(ld_line1), Create(ld_line2))

        linears = VGroup(
            q_box,
            kv_box,
            q_shape,
            kv_shape,
            q_line,
            kv_line,
            ld_tex,
            ld_line1,
            ld_line2,
            tex,
        )

        ## midline
        tshift = 3
        OL = LEFT * 7.1111111111 / 2
        OR = RIGHT * 7.1111111111 / 2
        midline = DashedLine(UP * 7, DOWN * 7, color=GREY_D)
        lt = (
            Text("Linear attention", font_size=24)
            .set_color(GREY_B)
            .move_to(OR)
            .shift(UP * tshift)
        )
        self.playw(linears.animate.move_to(OR), FadeIn(midline), FadeIn(lt))
        vt = (
            Text("Vanilla attention", font_size=24)
            .set_color(GREY_B)
            .move_to(OL)
            .shift(UP * tshift)
        )

        vtex = (
            Tex(r"\frac{\exp(QK^T)}{\sum_j\exp(QK^T)_{j}} V", font_size=36)
            .move_to(OL)
            .set_opacity(0.7)
        )
        vtex[:8].set_color(YELLOW).set_opacity(1)
        self.playw(FadeIn(vtex), FadeIn(vt))

        ## phi is positive output function

        phi1, phi2 = tex[0], tex[4]
        self.play(Indicate(phi1, color=RED), Indicate(phi2, color=RED))

        self.playw(Indicate(tex[:9], scale_factor=1.1))

        ## indicate qkt and exp
        self.play(Indicate(vtex[4:7], color=PURPLE))
        self.playw(Indicate(vtex[:8], color=PURPLE), wait=2)

        ## camera and rotate
        self.play(
            self.cf.animate.reorient(
                0,
                60,
                0,
                (np.float32(-3.26), np.float32(-0.02), np.float32(-1.21)),
                5.86,
            ),
            vtex.animate.rotate(60 * DEGREES, axis=RIGHT),
        )
        random.seed(42)
        vals = (
            VGroup(
                *[
                    DecimalNumber(random.random() * 12 - 3, font_size=14)
                    for _ in range(9)
                ]
            )
            .arrange(RIGHT, buff=0.25)
            .next_to(vtex, DOWN, buff=2)
        )
        self.play(FadeIn(vals))

        val_lines = VGroup(
            *[
                Line(
                    vals[i].get_center(),
                    vals[i].get_center() + OUT * vals[i].get_value() * 0.3,
                ).set_color(RED if vals[i].get_value() < 0 else GREEN)
                for i in range(len(vals))
            ]
        )
        self.playw(Create(val_lines))

        ## exp
        vals_exp = VGroup(
            *[
                DecimalNumber(np.exp(vals[i].get_value()), font_size=12).move_to(
                    vals[i].get_center()
                )
                for i in range(len(vals))
            ]
        )
        val_lines_exp = VGroup(
            *[
                Line(
                    vals_exp[i].get_center(),
                    vals_exp[i].get_center() + OUT * vals_exp[i].get_value() * 0.06,
                ).set_color(RED if vals_exp[i].get_value() < 0 else GREEN)
                for i in range(len(vals_exp))
            ]
        )
        self.play(Transform(val_lines, val_lines_exp), Transform(vals, vals_exp))

        ## normalized
        vals_sum = sum([vals_exp[i].get_value() for i in range(len(vals_exp))])
        vals_norm = VGroup(
            *[
                DecimalNumber(vals_exp[i].get_value() / vals_sum, font_size=16).move_to(
                    vals_exp[i].get_center()
                )
                for i in range(len(vals_exp))
            ]
        )
        val_lines_norm = VGroup(
            *[
                Line(
                    vals_norm[i].get_center(),
                    vals_norm[i].get_center() + OUT * vals_norm[i].get_value() * 1.5,
                ).set_color(RED if vals_norm[i].get_value() < 0 else GREEN)
                for i in range(len(vals_norm))
            ]
        )
        self.playw(Transform(val_lines, val_lines_norm), Transform(vals, vals_norm))

        ## discard 0
        self.playw(
            *[
                item.animate.set_color(PURE_RED)
                for item in vals_norm
                if item.get_value() < 0.01
            ],
            *[
                Circumscribe(item, color=RED)
                for item in vals_norm
                if item.get_value() < 0.01
            ],
        )

        ## camera move and rotate tex
        tex_ = VGroup(tex, kv_box, kv_shape, kv_line, q_shape, q_box, ld_line1, ld_line2, ld_tex, q_line)
        self.playw(self.cf.animate.reorient(0, 59, 0, (np.float32(3.56), np.float32(-0.1), np.float32(-1.34)), 5.86), tex_.animate.rotate(59*DEGREES, axis=RIGHT), FadeOut(lt))

        ## vals linear
        vals_linear = VGroup(
            *[
                DecimalNumber(random.random()*10, font_size=16)
                for i in range(len(vals_norm))
            ]
        ).arrange(RIGHT).next_to(tex_, DOWN, buff=2)
        val_lines_linear = VGroup(
            *[
                Line(
                    vals_linear[i].get_center(),
                    vals_linear[i].get_center() + OUT * vals_linear[i].get_value() * 0.3,
                ).set_color(RED if vals_linear[i].get_value() < 0 else YELLOW)
                for i in range(len(vals_linear))
            ]
        )
        self.playw(FadeIn(vals_linear), FadeIn(val_lines_linear))

        ## normalized vals linear
        vals_linear_sum = sum([vals_linear[i].get_value() for i in range(len(vals_linear))])
        vals_linear_norm = VGroup(
            *[
                DecimalNumber(vals_linear[i].get_value() / vals_linear_sum, font_size=16).move_to(
                    vals_linear[i].get_center()
                )
                for i in range(len(vals_linear))
            ]
        )
        val_lines_linear_norm = VGroup(
            *[
                Line(
                    vals_linear_norm[i].get_center(),
                    vals_linear_norm[i].get_center() + OUT * vals_linear_norm[i].get_value() * 2,
                ).set_color(RED if vals_linear_norm[i].get_value() < 0 else YELLOW)
                for i in range(len(vals_linear_norm))
            ]
        )
        self.playw(Transform(vals_linear, vals_linear_norm), Transform(val_lines_linear, val_lines_linear_norm), wait=4)

        ## ol
        ol = self.overlay
        fq = tex[:4].set_z_index(ol.z_index+1)
        fk = tex[4:8].set_z_index(ol.z_index+1)
        self.playw(FadeIn(ol, run_time=1), VGroup(fq, fk).set_z_index(ol.z_index+1).animate(run_time=3).scale(1.5).set_color(RED))

class LinearAttnDenominator(InteractiveScene, Scene2D):
    def construct(self):
        ## qkv, logit
        buff = 0.2
        q = Tensor(7, buff=buff)
        k = Tensor(7, arrange=RIGHT, buff=buff)
        v = Tensor(7, buff=buff)
        logit = VGroup(*[Tensor(7, buff=buff) for _ in range(7)]).arrange(RIGHT, buff=buff)
        for t in logit:
            for item in t:
                item.scale(0.2)

        buff_=1
        q.next_to(logit, LEFT, buff=buff_)
        k.next_to(logit, UP, buff=buff_)
        # v.next_to(logit, RIGHT, buff=buff_)
        qt = Text("query", font_size=24).next_to(q, DOWN, buff=0.2)
        kt = Text("key", font_size=24).next_to(k, LEFT, buff=0.2)
        # vt = Text("value", font_size=24).next_to(v, DOWN, buff=0.2)

        self.addw(q, k, qt, kt)

        ## animate q, k fading out and logit fading in
        self.play(FadeOut(q.copy(), shift=RIGHT*2.5), FadeOut(k.copy(), shift=DOWN*2.5), FadeIn(logit))
        def get_exp(item, font_size=20):
            pre_tex = Tex("\\text{exp}(", font_size=font_size).next_to(item, LEFT, buff=0.02)
            post_tex = Tex(")", font_size=font_size).next_to(item, RIGHT, buff=0.02)
            return VGroup(pre_tex, post_tex)

        exps = VGroup(*[VGroup(*[get_exp(item) for item in t]) for t in logit])
        self.playw(FadeIn(exps))

        ## sr_key
        sr_key = SurroundingRectangle(k, color=RED)
        self.play(FadeIn(sr_key))
        self.playw(k.animate.arrange(RIGHT, buff=0).move_to(k).set_color(PURE_RED), rate_func=there_and_back, wait=3)

        ## fadeout exps and logit
        self.playw(FadeOut(exps), FadeOut(logit), FadeOut(sr_key))

        ## get phi
        def get_phi(item, font_size=20):
            pre_tex = Tex("\\phi(", font_size=font_size).next_to(item, LEFT, buff=0.02)
            post_tex = Tex(")", font_size=font_size).next_to(item, RIGHT, buff=0.02)
            return VGroup(pre_tex, post_tex)

        qphi = get_phi(qt, font_size=32).set_color(GREEN)
        kphi = get_phi(kt, font_size=32).set_color(GREEN)
        q_ = Tensor(7, shape="circle", buff=buff).set_stroke(color=GREY).move_to(q)
        k_ = Tensor(7, shape="circle", buff=buff, arrange=RIGHT).set_stroke(color=GREY).move_to(k)
        self.playw(FadeIn(qphi), FadeIn(kphi), Transform(q, q_), Transform(k, k_))

        ## + joiner
        kc = k.copy()
        q1c = q[0].copy()
        kct = kc.generate_target()

        qcs = VGroup(*[q1c.copy() for _ in kct])
        qcst = qcs.generate_target()
        qkcs = VGroup()
        cdots = VGroup(*[Tex("\\cdot", font_size=32) for _ in kct])
        for ki, qc, cdot in zip(kct, qcst, cdots):
            qkcs.add(VGroup(qc, cdot, ki).arrange(RIGHT, buff=0.05))

        items = Joiner(*qkcs, join=lambda: Text("+", font_size=20)).arrange(RIGHT, buff=0.1).align_to(k, LEFT).align_to(q[0], DOWN)
        pluses = items[1::2]
        self.playw(MoveToTarget(kc), MoveToTarget(qcs), FadeIn(pluses), FadeIn(cdots))

        ## qcs over ol
        ol = self.overlay
        self.add(qcs.set_z_index(ol.z_index+1))
        self.playw(FadeIn(ol))

        ## 분배법칙
        qcs.generate_target()
        for i, item in enumerate(qcs.target):
            if i == 0:
                continue
            item.move_to(qcs[0])
        qcs.target.shift(LEFT*0.1)

        plus_joins = Joiner(*kc, join=lambda: Text("+", font_size=20))
        par_left = Text("(", font_size=20).next_to(kc, LEFT, buff=0.05)
        par_right = Text(")", font_size=20).next_to(kc, RIGHT, buff=0.05)
        self.playw(MoveToTarget(qcs), cdots[0].animate.shift(LEFT*0.1), FadeOut(cdots[1:]), FadeIn(par_left), FadeIn(par_right), FadeOut(ol))

        ## sr_kc
        sr_kc = SurroundingRectangle(kc, color=GREEN, buff=0.15)
        self.playw(FadeIn(sr_kc))

        self.embed()
        ## sum up k
        k_ = Tensor(1, shape="circle").move_to(k)
        kc_ = k_.copy().move_to(kc)
        self.playw(Transform(k, k_), Transform(kc, kc_), FadeOut(pluses))