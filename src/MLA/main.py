from manimlib import *
from numpy import trapezoid
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


def get_attn_module(n_dim=7):
    attn = Rectangle(width=5.5, height=1.8)
    attn_text = (
        Text("Attention layer", font_size=24)
        .set_color(GREY_B)
        .next_to(attn, UP, buff=0.05)
        .align_to(attn, RIGHT)
    )
    key = Tensor(n_dim, shape="square", arrange=RIGHT)
    key[n_dim // 2].become(Text("...", font_size=32).move_to(key[n_dim // 2]))
    value = Tensor(n_dim, shape="square", arrange=RIGHT)
    value[n_dim // 2].become(Text("...", font_size=32).move_to(value[n_dim // 2]))
    kv = VGroup(key, value).arrange(DOWN)
    key_text = Text("Key", font_size=24).next_to(key, LEFT, buff=0.1).set_color(GREY_B)
    value_text = (
        Text("Value", font_size=24).next_to(value, LEFT, buff=0.1).set_color(GREY_B)
    )
    return VGroup(attn_text, attn, key, value, key_text, value_text)


class ideation(InteractiveScene, Scene2D):
    def construct(self):

        ## attention
        attn = get_attn_module()
        self.playw(FadeIn(attn))

        self.play(Indicate(VGroup(attn[2], attn[4]), color=BLUE_D, scale_factor=1.1))
        self.playw(Indicate(VGroup(attn[3], attn[5]), color=BLUE_D, scale_factor=1.1))

        ## shrink and revert
        key, value = attn[2], attn[3]
        key.save_state(), value.save_state()
        self.playw(
            *[k.animate.scale(0.3) for k in key], *[v.animate.scale(0.3) for v in value]
        )

        self.playw(key.animate.restore(), value.animate.restore())

        ## kv cache
        attn_box = attn[1]
        attn_text = attn[0]
        attn_box.generate_target(), attn_text.generate_target()
        attn_box.target.scale(1.4)
        attn_text.target.next_to(attn_box.target, UP, buff=0.05).align_to(
            attn_box.target, RIGHT
        )

        self.play(MoveToTarget(attn_box), MoveToTarget(attn_text))
        key_text = attn[4]
        value_text = attn[5]
        kv_box = SurroundingRectangle(
            VGroup(key, value, key_text, value_text), buff=0.2
        )
        kv_text = (
            Text("KV cache", font_size=24)
            .next_to(kv_box, RIGHT, buff=0.05)
            .align_to(kv_box, DOWN)
            .set_color(YELLOW)
        )
        self.playw(FadeIn(kv_box), FadeIn(kv_text))

        self.playw(
            *[k.animate.scale(0.25) for k in key],
            *[v.animate.scale(0.25) for v in value],
        )

        ## revert
        self.play(
            *[k.animate.scale(4) for k in key],
            *[v.animate.scale(4) for v in value],
        )
        k0 = key[0]
        k0.save_state()
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(
                0, 62, 0, (np.float32(-0.27), np.float32(0.27), np.float32(0.52)), 8.00
            ),
            k0.animate.shift(OUT * 2).rotate(62 * DEGREES, axis=RIGHT),
        )

        ## in R4096
        rot = lambda x: x.rotate(62 * DEGREES, axis=RIGHT)
        in4096 = rot(
            Tex("\\in \\mathbb{R}^{4096}", font_size=32).next_to(k0, RIGHT, buff=0.1)
        )
        self.playw(FadeIn(in4096))

        exk0 = rot(randn(9, 1).scale(0.3).next_to(in4096, RIGHT, buff=0.3))
        exk0[4].become(Text("...", font_size=24).move_to(exk0[4]))
        self.playw(FadeTransform(in4096.copy(), exk0))

        ## restore

        self.play(
            self.cf.animate.restore(),
            k0.animate.restore(),
            FadeOut(VGroup(exk0, in4096)),
        )
        self.playwl(*[Indicate(item, scale_factor=1.1) for item in key], wait=0)
        self.playwl(*[Indicate(item, scale_factor=1.1) for item in value])

        ## 1M
        key_brace = Brace(key, UP)
        params = Text("1,000,000", font_size=24).next_to(key_brace, UP, buff=0.1)
        self.playw(
            kv_box.animate.set_stroke(opacity=0.3),
            kv_text.animate.set_opacity(0.3),
            VGroup(attn_box, attn_text).animate.shift(UP * 0.3),
            FadeIn(key_brace),
            FadeIn(params),
        )
        times4096 = (
            Tex("\\times 4096\, \\text{numbers}", font_size=32)
            .next_to(params, RIGHT, buff=0.1)
            .set_color(PURE_RED)
        )
        self.playw(
            VGroup(key_brace, params).animate.set_color(PURE_RED), FadeIn(times4096)
        )

        ## times 512
        times512 = (
            Tex("\\times 512\\, \\text{numbers}", font_size=32)
            .next_to(params, RIGHT, buff=0.1)
            .set_color(RED_A)
        )
        self.play(
            Transformr(times4096, times512),
            VGroup(key_brace, params).animate.set_color(RED_A),
            *[k.animate.scale(0.25) for k in key],
            *[v.animate.scale(0.25) for v in value],
        )
        self.playw(FlashAround(times512[1:4]))

        ## restore 4
        self.play(
            *[k.animate.scale(4) for k in key],
            *[v.animate.scale(4) for v in value],
            FadeOut(VGroup(key_brace, params, times512)),
            VGroup(attn_box, attn_text).animate.shift(DOWN * 0.3),
        )

        ## nn.Linear to 512

        k0 = key[0]
        k0.save_state()
        self.play(k0.animate.shift(UP * 1.5))

        wq = Tex(r"W_{\text{down}} \cdot", font_size=36).next_to(k0, LEFT, buff=0.1)

        in512_4096 = (
            Tex("\\in \\mathbb{R}^{512\\times 4096}", font_size=36)
            .rotate(PI / 4)
            .next_to(wq, UP, buff=0.1)
            .shift(RIGHT * 0.7)
        )
        self.playw(FadeIn(in512_4096), FadeIn(wq))

        self.playw(in512_4096[1:].animate.set_color(PURE_RED))

        ## to low rank

        self.play(
            *[k.animate.scale(0.25) for k in key],
            *[v.animate.scale(0.25) for v in value],
            FadeOut(
                VGroup(in512_4096, wq),
                shift=k0.get_center() - VGroup(in512_4096, wq).get_center(),
                scale=0.2,
            ),
        )
        self.playw(k0.animate.move_to(k0.saved_state.get_center()))

        ## redish

        self.playw(
            *[
                k.animate.set_color(interpolate_color(k.get_color(), PURE_RED, 0.8))
                for k in key
            ],
            *[
                v.animate.set_color(interpolate_color(v.get_color(), PURE_RED, 0.8))
                for v in value
            ],
        )


class compactIdeation(InteractiveScene, Scene2D):
    def construct(self):
        ## start
        wq_text = Tex("W_q ", font_size=32).shift(UP).set_color(GREY_B)
        wq_box = SurroundingRectangle(
            wq_text, buff=0.2, color=GREY_B
        ).stretch_to_fit_width(4)
        wk_text = (
            Tex("W_k ", font_size=32)
            .next_to(wq_text, RIGHT, buff=1.5)
            .set_color(GREY_B)
        )
        wk_box = SurroundingRectangle(
            wk_text, buff=0.2, color=GREY_B
        ).stretch_to_fit_width(4)
        wv_text = (
            Tex("W_v ", font_size=32)
            .next_to(wk_text, RIGHT, buff=1.5)
            .set_color(GREY_B)
        )
        wv_box = SurroundingRectangle(
            wv_text, buff=0.2, color=GREY_B
        ).stretch_to_fit_width(4)
        wq = VGroup(wq_box.set_fill(color=BLACK, opacity=0.75), wq_text)
        wk = VGroup(wk_box.set_fill(color=BLACK, opacity=0.75), wk_text)
        wv = VGroup(wv_box.set_fill(color=BLACK, opacity=0.75), wv_text)
        ws = VGroup(wq, wk, wv).arrange(RIGHT, buff=0.5).shift(UP * 0.5)

        t = Tensor(7, shape="square", arrange=RIGHT).shift(DOWN * 1.5)
        t[7 // 2].become(Text("...", font_size=32).move_to(t[7 // 2]))
        self.playw(FadeIn(wq), FadeIn(wk), FadeIn(wv), FadeIn(t))

        tq, tk, tv = t.copy(), t.copy(), t.copy()
        tq.next_to(wq, DOWN, buff=0.5)
        tk.next_to(wk, DOWN, buff=0.5)
        tv.next_to(wv, DOWN, buff=0.5)
        self.play(FadeTransform(t.copy(), tq), run_time=0.7)
        self.play(FadeTransform(t.copy(), tk), run_time=0.7)
        self.play(FadeTransform(t.copy(), tv), run_time=0.7)

        self.add(wq.set_z_index(1), wk.set_z_index(1), wv.set_z_index(1))
        tq.generate_target().next_to(wq, UP)
        tk.generate_target().next_to(wk, UP)
        tv.generate_target().next_to(wv, UP)
        for ti in tq.target:
            ti.set_fill(color=random_color())
        for ti in tk.target:
            ti.set_fill(color=random_color())
        for ti in tv.target:
            ti.set_fill(color=random_color())
        self.play(MoveToTarget(tq), MoveToTarget(tk), MoveToTarget(tv))

        ## prepare for attention

        self.play(
            FadeOut(t, shift=DOWN * 2.5),
            FadeOut(ws, shift=DOWN * 2.5),
            tq.animate.rotate(PI / 2).align_to(tq, RIGHT).shift(DOWN * 1),
            tk.animate.shift(UP * 1.25),
            tv.animate.rotate(PI / 2).align_to(tv, LEFT).shift(DOWN * 1),
        )
        qt = Text("query", font_size=24).next_to(tq, DOWN, buff=0.15)
        kt = Text("key", font_size=24).next_to(tk, LEFT, buff=0.15)
        vt = Text("value", font_size=24).next_to(tv, DOWN, buff=0.15)
        self.playw(FadeIn(qt), FadeIn(kt), FadeIn(vt))

        ## down project
        dp_text = Text("Down projection", font_size=22)
        dp_box = SurroundingRectangle(dp_text, buff=0.2)
        encoder = (
            Polygon(
                [-1.5, -1, 0],  # 좌하
                [1.5, -1, 0],  # 우하
                [1.0, 1, 0],  # 우상
                [-1.0, 1, 0],  # 좌상
            )
            .scale(0.5)
            .rotate(-PI / 4)
            .shift(UR * 3.2)
        )
        encoder.set_fill(BLUE, opacity=0.5).set_stroke(WHITE, 1)
        decoder = (
            Polygon(
                [-1.0, -1, 0],
                [1.0, -1, 0],
                [1.5, 1, 0],
                [-1.5, 1, 0],
            )
            .scale(0.5)
            .rotate(-PI / 4)
            .shift(UR * 3.2)
        )
        decoder.set_fill(RED, opacity=0.5).set_stroke(WHITE, 1).next_to(
            encoder, UL, buff=-0.5
        )

        dp = VGroup(dp_box, dp_text, encoder)
        self.cf.save_state()
        self.playw(
            FadeIn(encoder),
            FadeIn(decoder),
            self.cf.animate.reorient(
                0, 0, 0, (np.float32(1.02), np.float32(1.16), np.float32(0.0)), 10.24
            ),
        )
        ## down project key, value
        tkr = tk.copy()
        tvr = tv.copy()
        lk = tk.copy()
        for l in lk:
            l.scale(0.25)
        lk = lk.rotate(PI / 4).next_to(encoder, UR, buff=-0.3).shift(UL * 0.2)

        lv = tv.copy()
        for l in lv:
            l.scale(0.25)
        lv = lv.rotate(-PI / 4).next_to(lk, DR, buff=-2)

        anims = []
        for i in range(7):
            anim = []
            anim.append(
                AnimationGroup(
                    tk[6 - i].animate.move_to(encoder.shift(UL * 0.2)).scale(0.5),
                    tv[6 - i].animate.move_to(encoder.shift(DR * 0.2)).scale(0.5),
                )
            )
            anim.append(
                AnimationGroup(
                    tk[6 - i].animate.move_to(lk[6 - i]).rotate(PI / 4).scale(0.25),
                    tv[6 - i].animate.move_to(lv[6 - i]).rotate(-PI / 4).scale(0.25),
                )
            )
            anims.append(anim)
        anims_skew = SkewedAnimations(*anims)
        for anim in anims_skew:
            self.play(*anim, run_time=0.5)
        self.wait()

        ## kv cache
        kv_box = Rectangle(width=4, height=1.5).set_stroke(color=YELLOW_B)
        kv_text = (
            Text("KV cache", color=YELLOW_B, font_size=24)
            .next_to(kv_box, RIGHT, buff=0.05)
            .align_to(kv_box, UP)
        )
        kv_cache = VGroup(kv_box, kv_text).shift(RIGHT * 6)
        self.play(FadeIn(kv_cache))

        kv = VGroup(tk, tv).copy()
        self.playw(kv.animate.rotate(-PI / 4).move_to(kv_box))

        ## recon to original
        self.playw(FadeOut(encoder, shift=DR), decoder.animate.move_to(encoder))

        anims = []
        for i in range(7):
            anim = []
            anim.append(
                AnimationGroup(
                    tk[i].animate.move_to(decoder.shift(UL * 0.2)).scale(2),
                    tv[i].animate.move_to(decoder.shift(DR * 0.2)).scale(2),
                )
            )
            anim.append(
                AnimationGroup(
                    tk[i].animate.move_to(tkr[i]).rotate(-PI / 4).scale(4),
                    tv[i].animate.move_to(tvr[i]).rotate(PI / 4).scale(4),
                )
            )
            anims.append(anim)
        anims_skew = SkewedAnimations(*anims)
        for anim in anims_skew:
            self.play(*anim, run_time=0.5)
        self.wait()

        ## fadeout decoder
        self.playw(FadeOut(decoder))

        ## attn logit
        logits = VGroup(
            *[
                Dot(
                    radius=0.05,
                    stroke_color=GREY_A,
                    fill_color=random_color(),
                    fill_opacity=1,
                ).move_to(
                    np.array([tk[i].get_center()[0], tq[6 - j].get_center()[1], 0])
                )
                for i in range(7)
                for j in range(7)
            ]
        )
        self.playw(
            FadeOut(tk.copy(), shift=DOWN * 2),
            FadeOut(tq.copy(), shift=RIGHT * 2),
            FadeIn(logits),
        )

        ## zoom recon
        self.playw(
            self.cf.animate.restore(),
            FadeOut(kv_cache),
            FadeOut(kv),
            VGroup(logits, tq, qt).animate.set_opacity(0.3),
        )

        stk = tk.copy()
        stv = tv.copy()

        self.playw(
            *[st.animate.scale(0.25) for st in stk],
            *[st.animate.scale(0.25) for st in stv],
            tk.animate.set_opacity(0.4),
            tv.animate.set_opacity(0.4),
        )


class problem1(InteractiveScene, Scene2D):
    def construct(self):

        ## start
        q = Tensor(1, shape="square").shift(LEFT * 3.5 + DOWN * 2)
        qt = Text("query", font_size=20).next_to(q, DOWN, buff=0.2).set_color(GREY_B)
        kv_box = Rectangle(7, 2).set_stroke(width=1, color=YELLOW_B)
        kv_text = (
            Text("KV cache", font_size=28)
            .set_color(YELLOW_B)
            .align(kv_box, UR, buff=0.1)
        )
        kv = VGroup(kv_box, kv_text).shift(UP * 2.3)
        decoder = (
            Polygon(
                [-1.5, -1, 0],
                [1.5, -1, 0],
                [1.0, 1, 0],
                [-1.0, 1, 0],
            )
            .scale(0.5)
            .stretch_to_fit_width(5)
            .next_to(kv, DOWN, buff=0.2)
        )
        decoder.set_fill(RED, opacity=0.5).set_stroke(WHITE, 1)

        key = Tensor(7, shape="square", arrange=RIGHT)
        keyt = key.copy()
        key[len(key) // 2].become(Text("...", font_size=48).move_to(key[len(key) // 2]))
        value = Tensor(7, shape="square", arrange=RIGHT)
        valuet = value.copy()
        value[len(key) // 2].become(
            Text("...", font_size=48).move_to(value[len(key) // 2])
        )
        for i in range(len(key)):
            key[i].scale(0.25)
            value[i].scale(0.25)
        keyvalue = VGroup(key, value).arrange(DOWN, buff=0.4).move_to(kv)
        kt = Text("key", font_size=20).next_to(key, LEFT, buff=0.2).set_color(GREY_B)
        vt = (
            Text("value", font_size=20).next_to(value, LEFT, buff=0.2).set_color(GREY_B)
        )
        kr, vr = key.copy(), value.copy()
        self.add(kr, vr)

        self.addw(q, qt, kv, decoder, key, value, kt, vt, wait=1.5)
        keyt.next_to(decoder, DOWN, buff=0.3)
        valuet.rotate(PI / 2).next_to(q, RIGHT, buff=5.5).shift(DOWN * 0.5)
        anims = []
        for i in range(len(key)):
            anim = []
            anim.append(
                AnimationGroup(
                    key[i].animate.move_to(decoder).scale(2).shift(LEFT * 0.25),
                    value[len(key) - 1 - i]
                    .animate.move_to(decoder)
                    .scale(2)
                    .shift(RIGHT * 0.25),
                )
            )
            anim.append(
                AnimationGroup(
                    key[i].animate.move_to(keyt[i]).scale(4),
                    value[len(key) - 1 - i]
                    .animate.move_to(valuet[len(key) - 1 - i])
                    .scale(4),
                )
            )
            anims.append(anim)
        anims_skew = SkewedAnimations(*anims)
        for i, anim in enumerate(anims_skew):
            if i == len(anims_skew) // 2:
                self.play(*anim, self.cf.animate.shift(DOWN * 2.5), run_time=0.5)
            else:
                self.play(*anim, run_time=0.5)
        kt = Text("Key", font_size=20).next_to(keyt, LEFT, buff=0.1).set_color(GREY_B)
        vt = (
            Text("Value", font_size=20)
            .next_to(valuet, DOWN, buff=0.1)
            .set_color(GREY_B)
        )
        self.play(FadeIn(kt), FadeIn(vt))
        self.wait()

        ## arrow to decoder

        arrow = Arrow(
            decoder.get_right() + RIGHT + DOWN * 0.3,
            decoder.get_right(),
            buff=0,
            thickness=2,
        ).set_color(PURE_RED)
        self.playw(GrowArrow(arrow))

        ## dot product
        xy = lambda i, j: np.array([keyt[i].get_center()[0], q[j].get_center()[1], 0])
        logits = VGroup(
            *[
                Dot(radius=0.05, fill_color=random_color(), fill_opacity=0.8).move_to(
                    xy(i, j)
                )
                for i in range(len(keyt))
                for j in range(len(q))
            ]
        )
        attn_logit_tex = Tex("QK^T").next_to(logits, DOWN, buff=2)

        self.play(FadeIn(attn_logit_tex))
        self.playw(
            FadeOut(key.copy(), shift=DOWN * 1.7),
            FadeOut(q.copy(), shift=RIGHT * 3),
            FadeIn(logits),
        )

        ## K is up-projected
        k = Tex("K = k_{\\text{small}} \\cdot W_{\\text{up}}", font_size=36).next_to(
            attn_logit_tex[1], DOWN, aligned_edge=LEFT
        )
        k[0].set_color(YELLOW)
        self.playw(FadeIn(k), attn_logit_tex[1].animate.set_color(YELLOW))

        new_attn = Tex(
            "Q(k_{\\text{small}} \\cdot W_{\\text{up}})^T", font_size=36
        ).move_to(attn_logit_tex)
        self.play(
            Transformr(attn_logit_tex[0], new_attn[0]),
            Transformr(attn_logit_tex[-1], new_attn[-1]),
        )
        self.play(
            FadeOut(attn_logit_tex[1:-1], shift=UP),
            Transformr(k[2:].copy(), new_attn[2:-2].set_color(YELLOW)),
            FadeIn(VGroup(new_attn[1], new_attn[-2])),
            k[0].animate.set_color(WHITE),
            k[2:].animate.set_color(YELLOW),
        )
        self.addw(new_attn)

        ## T is transposed into k Wup
        lt1 = new_attn[-1].copy()
        lt2 = new_attn[-1]

        qwtkt = (
            Tex("QW_{\\text{up}}^T k_{small}^T", font_size=36)
            .move_to(new_attn)
            .align_to(new_attn, LEFT)
        )
        self.play(FadeOut(k))
        self.playw(
            Transformr(new_attn[0], qwtkt[0]),
            FadeTransform(new_attn[9:12], VGroup(qwtkt[1], qwtkt[3:5])),
            FadeTransform(new_attn[2:8], VGroup(qwtkt[5], qwtkt[7:12])),
            FadeOut(new_attn[1]),
            FadeOut(new_attn[-2]),
            FadeOut(new_attn[8]),
            FadeTransform(lt1, qwtkt[2]),
            FadeTransform(lt2, qwtkt[6]),
        )

        ## q is x W_q
        wq = Tex("Q = x W_{q}", font_size=36).next_to(qwtkt[0], DOWN, aligned_edge=LEFT)
        wq[0].set_color(YELLOW)
        self.playw(FadeIn(wq), qwtkt[0].animate.set_color(YELLOW))
        self.play(wq.animate.align_to(qwtkt[0], RIGHT))

        ## transform
        xw = (
            Tex(r"x W_{q} W_{\text{up}}^T k_{small}^T", font_size=36)
            .move_to(qwtkt)
            .align_to(qwtkt, RIGHT)
        )
        self.play(
            FadeOut(qwtkt[0], shift=UP),
            FadeTransform(wq[-3:], xw[:3]),
            Transformr(qwtkt[1:], xw[3:]),
        )
        self.playw(FadeOut(wq[:-3]))

        ## xw [1:7]
        self.playw(xw[1:7].animate.set_color(YELLOW), FlashAround(xw[1:7], buff=0.05))

        ## W_absorbed
        w_abs = Tex(r"W_{\text{abs}}", font_size=36).move_to(xw[1:7]).set_color(YELLOW)
        self.playw(
            FadeTransform(xw[1:7], w_abs),
        )

        ## wq, wk, wv
        wq_text = Tex("W_q ", font_size=32).shift(UP).set_color(GREY_B)
        wq_box = SurroundingRectangle(
            wq_text, buff=0.2, color=GREY_B
        ).stretch_to_fit_width(4)
        wk_text = (
            Tex("W_k ", font_size=32)
            .next_to(wq_text, RIGHT, buff=1.5)
            .set_color(GREY_B)
        )
        wk_box = SurroundingRectangle(
            wk_text, buff=0.2, color=GREY_B
        ).stretch_to_fit_width(4)
        wv_text = (
            Tex("W_v ", font_size=32)
            .next_to(wk_text, RIGHT, buff=1.5)
            .set_color(GREY_B)
        )
        wv_box = SurroundingRectangle(
            wv_text, buff=0.2, color=GREY_B
        ).stretch_to_fit_width(4)
        wq = VGroup(wq_box.set_fill(color=BLACK, opacity=0.75), wq_text)
        wk = VGroup(wk_box.set_fill(color=BLACK, opacity=0.75), wk_text)
        wv = VGroup(wv_box.set_fill(color=BLACK, opacity=0.75), wv_text)
        ws = VGroup(wq, wk, wv).arrange(RIGHT, buff=0.5).shift(DOWN * 5.5)
        self.playw(
            FadeIn(ws),
            self.cf.animate.shift(DOWN * 2.5),
            decoder.animate.next_to(wq, UP).stretch_to_fit_width(wq.get_width()),
            FadeOut(VGroup(qt, kt, vt, q, value, key, logits)),
        )
        self.playw(FadeIn(xw[1:7].next_to(w_abs, UP)))

        self.playw(FlashAround(xw[1:7]), FlashAround(VGroup(wq, decoder)))

        ## wq_new
        wq_new = (
            decoder.copy()
            .stretch_to_fit_height(wq.get_height())
            .move_to(wq)
            .set_fill(color=BLACK, opacity=0.75)
            .set_stroke(color=RED)
        )
        wqt = wq[1]
        self.add(wqt.set_z_index(1))
        wqtabs = Tex("W_{\\text{abs}}", font_size=32).move_to(wqt)
        self.playw(
            FadeTransform(VGroup(wq[0], decoder), wq_new), Transformr(wqt, wqtabs)
        )
        self.add(wq_new.set_z_index(0.5), wqtabs.set_z_index(0.75))

        ## q_absorbed
        t = Tensor(7, shape="square", arrange=RIGHT).next_to(wq_new, DOWN)
        qt = (
            Tensor(7, shape="square", arrange=RIGHT, buff=1)
            .next_to(wq_new, UP)
            .scale(0.25)
        )
        self.play(FlashAround(VGroup(xw[0], w_abs)), FadeIn(t))

        q_abs = Tex("Q_{\\text{abs}}", font_size=36).move_to(w_abs).set_color(YELLOW)
        self.playw(FadeTransform(VGroup(xw[0], w_abs), q_abs), t.animate.become(qt))


class problem2(InteractiveScene, Scene2D):
    def construct(self):

        ## rope
        rope = Tex("\\text{RoPE}", font_size=36)
        self.playw(FadeIn(rope))

        ## rope up
        self.playw(rope.animate.shift(UP))

        ## attns maths
        attn1 = Tex("x W_q (k_{\\text{small}} W_{\\text{up}})^T", font_size=36)
        attn1[3:].set_color(YELLOW)
        attn2 = Tex("(x W_q) (W_{\\text{up}}^T k_{\\text{small}}^T)", font_size=36)
        attn2[5:].set_color(YELLOW)
        attn3 = Tex("x (W_q W_{\\text{up}}^T) k_{\\text{small}}^T", font_size=36)
        attn3[1:9].set_color(YELLOW)

        self.playw(FadeIn(attn1))
        attn1.generate_target()
        VGroup(attn1.target, attn2).arrange(RIGHT, buff=0.75)
        arr12 = Arrow(
            attn1.target.get_right(),
            attn2.get_left(),
            buff=0.05,
            thickness=2,
        ).set_color(GREEN)
        self.playwl(
            MoveToTarget(attn1), FadeIn(attn2), GrowArrow(arr12), lag_ratio=0.33
        )

        attn1.generate_target()
        attn2.generate_target()
        arr12.generate_target()
        VGroup(VGroup(attn1.target, arr12.target, attn2.target), attn3).arrange(
            RIGHT, buff=0.75
        )
        arr23 = Arrow(
            attn2.target.get_right(),
            attn3.get_left(),
            buff=0.05,
            thickness=2,
        ).set_color(GREEN)
        self.playwl(
            AnimationGroup(*[MoveToTarget(item) for item in [attn1, arr12, attn2]]),
            FadeIn(attn3),
            GrowArrow(arr23),
            lag_ratio=0.33,
        )

        ## rope to Wrope
        wrope = Tex("W_{\\text{RoPE}}", font_size=36).move_to(rope).set_color(RED)
        wr1 = wrope
        wr2 = wr1.copy()
        wr3 = wr1.copy()

        self.playwl(
            Transformr(rope, wrope[1:]), FadeIn(wrope[0]), lag_ratio=0.3, wait=0
        )
        self.add(wr2, wr3)
        self.play(
            wrope.animate.align_to(attn1[2], RIGHT),
            wr2.animate.align_to(attn2[5], LEFT),
            wr3.animate.align_to(attn3[4], LEFT).shift(RIGHT * (wr2.get_width() + 0.05)),
        )
        wrope.generate_target().move_to(ORIGIN).align_to(attn1[2], RIGHT)
        wr2.generate_target()
        wr3.generate_target()
        attn2.generate_target()
        arr23.generate_target()
        attn3.generate_target()
        
        VGroup(attn2.target[5:], arr23.target, attn3.target).shift(RIGHT * (wr2.get_width() + 0.05))
        attn3.target[4:].shift(RIGHT * (wr2.get_width() + 0.05))
        wr2.target.move_to(ORIGIN).align_to(wr2, RIGHT)
        wr3.target.move_to(ORIGIN).align_to(wr3, RIGHT)

        self.playw(
            *[MoveToTarget(item) for item in [wrope, wr2, wr3, attn2, arr23, attn3]],
            attn1[:3].animate.next_to(wrope.target, LEFT, buff=0.05),
        )

        ## camera up

        self.play(self.cf.animate.shift(UP*1.5))

        x = Tensor(7, shape="square", arrange=RIGHT, buff=0.2).shift(UP*3.5)
        xt = Text("x", font_size=24).next_to(x, LEFT)
        wq = Rectangle(width=x.get_width() + 0.5, height=1.1).set_fill(BLACK, opacity=0.5).shift(UP*2.5).set_z_index(0.5)
        wqt = Tex("W_q", font_size=32).move_to(wq).set_z_index(1)
        self.playw(FadeIn(x), FadeIn(wq), FadeIn(wqt), FadeIn(xt))

        query = Tensor(7, shape="square", arrange=RIGHT, buff=0.25).shift(UP*1.5)
        qt = Text("query", font_size=24).next_to(query, LEFT)
        self.play(Transformr(x, query), FadeOut(xt, shift=DOWN))
        self.playw(FadeIn(qt))

        ## rope rotate
        query.save_state()
        query.generate_target()
        for i in range(len(query)):
            query.target[i].rotate(PI/2 * (i / len(query)))
        self.playw(MoveToTarget(query))

        ## rope to wr3

        upper = VGroup(wq, wqt, qt, query)
        upper.generate_target().move_to(wr3).align_to(upper, UP)
        self.playwl(MoveToTarget(upper), self.cf.animate.shift(upper.target.get_center() - upper.get_center()), lag_ratio=0.3)

        ## lines

        lines = VGroup(*[DashedLine(wr3.get_top(), query[i].get_bottom(), buff=0.05) for i in range(len(query))]).set_color(RED)
        self.playwl(*[Create(line) for line in lines], lag_ratio=0.1)

        ## attn3 www red
        
        self.playw(attn3[1:9].animate.set_color(RED))

class solvedByRoPENoPE(InteractiveScene, Scene2D):
    def construct(self):

        ## Wq RoPE, Wq NoPE
        wq_rope_text = Tex(r"W_{\text{q}, \text{nope}}", font_size=36)
        wq_rope_box = Rectangle(8, 0.8).set_stroke(width=1.5, color=GREY_B).set_fill(BLACK, opacity=0.75)
        wq_rope = VGroup(wq_rope_box, wq_rope_text).set_z_index(1)

        wq_nope_text = Tex(r"W_{\text{q}, \text{rope}}", font_size=36)
        wq_nope_box = Rectangle(4, 0.8).set_stroke(width=1.5, color=GREY_B).set_fill(BLACK, opacity=0.75)
        wq_nope = VGroup(wq_nope_box, wq_nope_text).set_z_index(1)

        VGroup(wq_rope, wq_nope).arrange(RIGHT, buff=1)

        self.playw(FadeIn(wq_rope), FadeIn(wq_nope))

        ## x
        x = Tensor(9, shape="square", arrange=RIGHT, buff=0.2).shift(UP*2)
        xt = Text("x", font_size=24).next_to(x, LEFT)
        x[len(x)//2].become(Text("...",font_size=24).move_to(x[len(x)//2]))
        self.playw(FadeIn(x), FadeIn(xt))

        ## decoder
        decoder = (
            Polygon(
                [-1.0, -1, 0],
                [1.0, -1, 0],
                [1.5, 1, 0],
                [-1.5, 1, 0],
            )
            .scale(0.5)
            .set_fill(interpolate_color(RED_D, BLACK, 0.7), opacity=0.7)
            .set_stroke(width=1.5, color=GREY_B)
            .set_z_index(1)
            .stretch_to_fit_width(wq_rope_box.get_width())
        ).next_to(wq_rope, DOWN, buff=0.1)
        self.playw(FadeIn(decoder))

        ## q_small
        q_small = Tensor(9, ellipsis=True, arrange=RIGHT).next_to(decoder, DOWN)
        for t in q_small:
            t.scale(0.25)
        self.playw(Transformr(x.copy(), q_small))

        ## q_nope_small

        q_nope_small = Tensor(9, ellipsis=True, arrange=RIGHT, buff=0.05).next_to(wq_nope_box, DOWN)
        for t in q_nope_small:
            t.scale(0.25)
        xc = x.copy()
        self.play(xc.animate.arrange(RIGHT, buff=0.1).next_to(wq_nope_box, UP, buff=0.2))
        self.play(Transformr(xc, q_nope_small))

        ## rotate q_rope
        self.cf.save_state()
        self.play(self.cf.animate.move_to(q_nope_small).scale(0.5))
        q_nope_small.generate_target()
        for i in range(len(q_nope_small)):
            if i == len(q_nope_small) // 2: continue
            qt = q_nope_small.target[i]
            qt.rotate(PI / 2 * (i / len(q_nope_small)))
        self.playw(MoveToTarget(q_nope_small))

        ## self.cf.restore
        self.playw(self.cf.animate.restore())

        self.embed()
        ## concat and a little bit larger
        self.play(self.cf.animate.shift(DOWN*0.5))

        result = Tensor(9, ellipsis=True, arrange=RIGHT).shift(DOWN*3)
        for t in result:
            t.scale(0.5)

        anims = []
        for i in range(len(result)):
            anim = []
            qs = VGroup(q_small[i], q_nope_small[i])
            
            anim.append(qs.animate.arrange(RIGHT, buff=0.05).move_to(result[i]))
            anim.append(Transformr(qs, result[i]))
            anims.append(anim)
        anims_skew = SkewedAnimations(*anims)
        for i, anim in enumerate(anims_skew):
            if i < 2:
                self.playw(*anim)
            else:
                self.play(*anim, run_time=0.7)
        self.wait()