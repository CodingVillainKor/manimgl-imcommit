from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):
        scale = 0.35
        ## weight
        weight = randn(7, 7).scale(scale).set_color(GREY_A).shift(LEFT * 2)
        for i in range(7):
            for j in range(7):
                idx = i * 7 + j
                if idx % 7 == 3 or 21 <= idx < 28:
                    elem = weight[i * 7 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))

        ## lweight
        lwa = randn(3, 7).scale(scale).set_color(BLUE)
        for i in range(3):
            for j in range(7):
                idx = i * 7 + j
                if idx % 7 == 3 or 7 <= idx < 14:
                    elem = lwa[i * 7 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))
        lwb = randn(7, 3).scale(scale).set_color(BLUE)
        for i in range(7):
            for j in range(3):
                idx = i * 3 + j
                if idx % 3 == 1 or 9 <= idx < 12:
                    elem = lwb[i * 3 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))
        lweight = VGroup(lwa, lwb).arrange(RIGHT)

        VGroup(weight, lweight).arrange(RIGHT, buff=1)

        ## lins, louts
        lin1 = Line(weight.get_bottom() + DOWN * 2, weight.get_bottom()).set_color(
            GREY_B
        )
        lin2 = BrokenLine(
            weight.get_bottom() + DOWN,
            [lweight.get_bottom()[0], (weight.get_bottom() + DOWN)[1], 0],
            lweight.get_bottom(),
        ).set_color(GREY_B)
        lin = VGroup(lin1, lin2)

        oplus = VGroup(
            t := Text("⊕", font_size=30).next_to(weight, UP, buff=1.5)
        ).set_color(GREEN)
        lout1 = Line(weight.get_top(), oplus.get_bottom()).set_color(GREY_B)
        lout2 = BrokenLine(
            lweight.get_top(),
            [lweight.get_top()[0], oplus.get_right()[1], 0],
            oplus.get_right(),
        ).set_color(GREY_B)
        lplus = Line(oplus.get_top(), oplus.get_top() + UP).set_color(GREY_B)
        lout = VGroup(lout1, lout2, lplus)
        self.addw(weight, lweight, lin, lout, oplus)

        ## shape
        wshape = (
            Tex("1024 \\times 1024", font_size=28)
            .next_to(weight, UP, buff=0.1)
            .align_to(weight, RIGHT)
        )
        self.playwl(
            *[FadeIn(wshape[s]) for s in [slice(0, 4), slice(4, 5), slice(5, 9)]],
            lag_ratio=0.5,
        )

        ## lshape
        lshape1 = (
            Tex("1024 \\times 16", font_size=28)
            .next_to(lwa, UP, buff=0.1)
            .align_to(lwa, RIGHT)
            .set_color(BLUE)
        )
        lshape2 = (
            Tex("16 \\times 1024", font_size=28)
            .next_to(lwb, UP, buff=0.1)
            .align_to(lwb, RIGHT)
            .set_color(BLUE)
        )
        self.playw(FadeIn(lshape1))
        self.playw(FadeIn(lshape2))

        ## approx 1M, 30k
        wapp = (
            Tex("\\approx 1M", font_size=28)
            .next_to(weight, DOWN, buff=0.1)
            .align_to(wshape, RIGHT)
        )
        lapp = (
            Tex("\\approx 30k", font_size=28)
            .next_to(lweight, DOWN, buff=0.1)
            .align_to(lshape2, RIGHT)
            .set_color(BLUE)
        )
        self.play(FadeIn(wapp))
        self.playw(FadeIn(lapp))

        ## camera
        self.playw(
            self.cf.animate.reorient(
                89,
                33,
                -89,
                (np.float32(5.53), np.float32(0.18), np.float32(-3.73)),
                8.00,
            )
        )


class merge(InteractiveScene, Scene2D):
    def construct(self):

        scale = 0.35
        ## weight
        weight = randn(7, 7).scale(scale).set_color(GREY_A).shift(LEFT * 2)
        for i in range(7):
            for j in range(7):
                idx = i * 7 + j
                if idx % 7 == 3 or 21 <= idx < 28:
                    elem = weight[i * 7 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))

        ## lweight
        lwa = randn(3, 7).scale(scale).set_color(BLUE)
        for i in range(3):
            for j in range(7):
                idx = i * 7 + j
                if idx % 7 == 3 or 7 <= idx < 14:
                    elem = lwa[i * 7 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))
        lwb = randn(7, 3).scale(scale).set_color(BLUE)
        for i in range(7):
            for j in range(3):
                idx = i * 3 + j
                if idx % 3 == 1 or 9 <= idx < 12:
                    elem = lwb[i * 3 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))
        lweight = VGroup(lwa, lwb).arrange(RIGHT)

        VGroup(weight, lweight).arrange(RIGHT, buff=1)

        ## lins, louts
        lin1 = Line(weight.get_bottom() + DOWN * 2, weight.get_bottom()).set_color(
            GREY_B
        )
        lin2 = BrokenLine(
            weight.get_bottom() + DOWN,
            [lweight.get_bottom()[0], (weight.get_bottom() + DOWN)[1], 0],
            lweight.get_bottom(),
        ).set_color(GREY_B)
        lin = VGroup(lin1, lin2)

        oplus = VGroup(
            t := Text("⊕", font_size=30).next_to(weight, UP, buff=1.5)
        ).set_color(GREEN)
        lout1 = Line(weight.get_top(), oplus.get_bottom()).set_color(GREY_B)
        lout2 = BrokenLine(
            lweight.get_top(),
            [lweight.get_top()[0], oplus.get_right()[1], 0],
            oplus.get_right(),
        ).set_color(GREY_B)
        lplus = Line(oplus.get_top(), oplus.get_top() + UP).set_color(GREY_B)
        lout = VGroup(lout1, lout2, lplus)
        self.addw(weight, lweight, lin, lout, oplus)

        ## Transformer layers
        def get_layer(opacity=0.7, sop=1):
            attn = (
                Rectangle(width=0.5, height=0.5)
                .set_color(GREY_A)
                .set_stroke(opacity=sop)
                .set_fill(ORANGE, opacity=opacity)
            )
            ffn = (
                Rectangle(width=0.5, height=0.5)
                .set_color(GREY_A)
                .set_stroke(opacity=sop)
                .set_fill(WHITE, opacity=opacity)
            )
            ffnl = (
                Rectangle(width=0.5, height=0.4)
                .set_color(GREY_A)
                .set_stroke(opacity=sop)
                .set_fill(BLUE, opacity=opacity)
            )
            ffns = VGroup(ffn, ffnl).arrange(RIGHT, buff=0.1, aligned_edge=DOWN)
            layer = VGroup(attn, ffns).arrange(UP, aligned_edge=LEFT)
            box = (
                SurroundingRectangle(layer, color=GREY_B, buff=0.4)
                .shift(UP * 0.2)
                .set_stroke(opacity=sop)
            )
            return VGroup(layer, box)

        layer1 = get_layer(opacity=0.1, sop=0.2)
        l2, b2 = get_layer()
        layer3 = get_layer(opacity=0.1, sop=0.2)

        layers = VGroup(layer1, VGroup(l2, b2), layer3).arrange(UP, buff=0.5)
        lin1.generate_target().put_start_and_end_on(
            l2[0].get_top(), l2[1][0].get_bottom()
        )
        lin2.generate_target().become(
            BrokenLine(
                lin1.target.get_center(),
                [l2[1][1].get_bottom()[0], lin1.target.get_center()[1], 0],
                l2[1][1].get_bottom(),
            )
        )
        oplus.generate_target().next_to(l2[1][0], UP, buff=0.2).scale(0.5)
        lout1.generate_target().put_start_and_end_on(
            l2[1][0].get_top(), oplus.target.get_bottom()
        )
        lout2.generate_target().become(
            BrokenLine(
                l2[1][1].get_top(),
                [l2[1][1].get_top()[0], oplus.target.get_right()[1], 0],
                oplus.target.get_right(),
            )
        )
        lplus.generate_target().put_start_and_end_on(
            oplus.target.get_top(), oplus.target.get_top() + UP * 0.4
        )
        self.playwl(
            AnimationGroup(
                FadeTransform(weight, l2[1][0]),
                FadeTransform(lweight, l2[1][1]),
                MoveToTarget(lin1),
                MoveToTarget(lin2),
                MoveToTarget(oplus),
                MoveToTarget(lout1),
                MoveToTarget(lout2),
                MoveToTarget(lplus),
            ),
            AnimationGroup(*[FadeIn(item) for item in [layer1, l2[0], b2, layer3]]),
            lag_ratio=0.5,
        )

        ## rwiggle layers
        layers = VGroup(*layers, lin1, lin2, oplus, lout1, lout2, lplus)
        self.playw(RWiggle(layers, amp=0.2, speed=2), run_time=3)

        ## lora weight
        lw = l2[1][1]
        larr = Arrow(
            lw.get_right() + RIGHT, lw.get_right(), buff=0.07, thickness=2
        ).set_color(BLUE)
        tarr = (
            Text("LoRA weight", font_size=24)
            .next_to(larr, RIGHT, buff=0.1)
            .set_color(BLUE)
        )
        self.play(GrowArrow(larr), run_time=0.5)
        self.playw(FadeIn(tarr), run_time=0.5)

        ## to pure red
        ol = self.overlay
        loras = VGroup(lw, larr, tarr)
        loras.save_state()
        self.add(loras.set_z_index(ol.z_index + 1))
        self.playw(FadeToColor(loras, PURE_RED), FadeIn(ol))

        ## fadeout overlay
        self.playw(FadeOut(ol))

        ## fadeout loras
        fadeouts = VGroup(layer1[0][1][1], layer3[0][1][1], lout2, lin2)
        self.playw(FadeOut(loras), *[FadeOut(item) for item in fadeouts])

        ## fadein loras
        loras.restore()
        self.play(FadeIn(loras), *[FadeIn(item) for item in fadeouts])
        self.playw(
            fadeouts.animate.set_color(PURE_RED),
            loras.animate.set_color(PURE_RED),
            wait=3,
        )

        ## merge
        self.playw(
            FadeOut(lin2),
            FadeOut(lout2),
            FadeOut(larr),
            FadeOut(tarr),
            AnimationGroup(
                FadeOut(lw, shift=LEFT * 0.7, scale=0.5),
                Indicate(l2[1][0], scale_factor=1.05, color=RED_B),
                lag_ratio=0.4,
            ),
        )


class howtoMerge(InteractiveScene, Scene2D):
    def construct(self):
        scale = 0.35
        ## weight
        weight = randn(7, 7).scale(scale).set_color(GREY_A).shift(LEFT * 2)
        for i in range(7):
            for j in range(7):
                idx = i * 7 + j
                if idx % 7 == 3 or 21 <= idx < 28:
                    elem = weight[i * 7 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))

        ## lweight
        lwa = randn(3, 7).scale(scale).set_color(BLUE)
        for i in range(3):
            for j in range(7):
                idx = i * 7 + j
                if idx % 7 == 3 or 7 <= idx < 14:
                    elem = lwa[i * 7 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))
        lwb = randn(7, 3).scale(scale).set_color(BLUE)
        for i in range(7):
            for j in range(3):
                idx = i * 3 + j
                if idx % 3 == 1 or 9 <= idx < 12:
                    elem = lwb[i * 3 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))
        lweight = VGroup(lwa, lwb).arrange(RIGHT)

        VGroup(weight, lweight).arrange(RIGHT, buff=1)

        ## lins, louts
        lin1 = Line(weight.get_bottom() + DOWN * 2, weight.get_bottom()).set_color(
            GREY_B
        )
        lin2 = BrokenLine(
            weight.get_bottom() + DOWN,
            [lweight.get_bottom()[0], (weight.get_bottom() + DOWN)[1], 0],
            lweight.get_bottom(),
        ).set_color(GREY_B)
        lin = VGroup(lin1, lin2)

        oplus = VGroup(
            t := Text("⊕", font_size=30).next_to(weight, UP, buff=1.5)
        ).set_color(GREEN)
        lout1 = Line(weight.get_top(), oplus.get_bottom()).set_color(GREY_B)
        lout2 = BrokenLine(
            lweight.get_top(),
            [lweight.get_top()[0], oplus.get_right()[1], 0],
            oplus.get_right(),
        ).set_color(GREY_B)
        lplus = Line(oplus.get_top(), oplus.get_top() + UP).set_color(GREY_B)
        lout = VGroup(lout1, lout2, lplus)
        fbox = (
            SurroundingRectangle(weight)
            .set_stroke(width=1, color=BLUE_D)
            .set_fill(BLUE, opacity=0.5)
        )
        ftext = (
            Text("Freezed", font_size=24)
            .next_to(fbox, UP, buff=0.07)
            .align_to(fbox, LEFT)
        )
        self.addw(weight, lweight, lin, lout, oplus, fbox, ftext)

        ## 학습 완료
        tbox = (
            SurroundingRectangle(lweight)
            .set_stroke(width=1, color=ORANGE)
            .set_fill(ORANGE, opacity=0.2)
        )
        text = (
            Text("Train complete", font_size=24)
            .set_color(ORANGE)
            .next_to(tbox, UP, buff=0.07)
            .align_to(tbox, LEFT)
        )
        self.playw(FadeIn(tbox), FadeIn(text))

        ## weight is w, lora weight is A, B each
        wt = (
            Tex("W", font_size=36).next_to(weight, UP, buff=0.1).align_to(weight, RIGHT)
        )
        lat = (
            Tex("A", font_size=36)
            .next_to(lwa, UP, buff=0.1)
            .align_to(lwa, RIGHT)
            .set_color(BLUE)
        )
        lbt = (
            Tex("B", font_size=36)
            .next_to(lwb, UP, buff=0.1)
            .align_to(lwb, RIGHT)
            .set_color(BLUE)
        )
        self.play(FadeOut(VGroup(fbox, ftext, tbox, text)), run_time=0.5)
        self.playw(Write(wt), Write(lat), Write(lbt))

        ## indicate a, then b
        self.play(Indicate(lat), *[Indicate(aitem) for aitem in lwa[:-2]])
        self.playw(Indicate(lbt), *[Indicate(bitem) for bitem in lwb[:-2]])

        ## x is input
        xt = (
            Tex("x", font_size=36)
            .move_to(lin2.get_start())
            .add_background_rectangle(opacity=0.9, buff=0.1)
        )
        xtl = xt.copy()
        self.play(FadeIn(xtl), run_time=0.75)
        self.play(MoveAlongPath(xtl, lin2), run_time=0.75)

        ## BAx
        obxtl = xtl
        obxtl.background_rectangle.set_fill(opacity=0)
        ob = lbt.copy()
        oa = lat.copy()
        bax = VGroup(ob, oa, obxtl)
        self.playw(
            bax.animate.arrange(RIGHT, buff=0.0, aligned_edge=UP).move_to(
                lout2.get_start()
            )
        )

        ## x input into weight
        self.play(MoveAlongPath(xt, lin1), run_time=0.75)
        oxt = xt
        ow = wt.copy()
        wx = VGroup(ow, oxt)
        oxt.background_rectangle.set_fill(opacity=0)
        self.playw(
            wx.animate.arrange(RIGHT, buff=-0.07, aligned_edge=UP)
            .move_to(lout1.get_start())
            .shift(UP * 0.2)
        )

        ## sum
        self.play(
            MoveAlongPath(wx, lout1),
            MoveAlongPath(bax, lout2),
            run_time=1.2,
            rate_func=linear,
        )
        result = Tex("Wx + BAx", font_size=32).next_to(oplus, UR, buff=0.0)
        self.playw(
            Transformr(wx, result[:2]),
            Transformr(bax, result[-3:]),
            FadeIn(result[2], shift=result[2].get_center() - oplus.get_center()),
        )

        ## associative law
        assoc = Tex("(W + B A)x", font_size=32).next_to(oplus, UR, buff=0.0)
        idx_link = [
            [None, slice(0, 1)],
            [slice(0, 1), slice(1, 2)],
            [slice(1, 2), None],
            [slice(2, 5), slice(2, 5)],
            [None, slice(5, 6)],
            [slice(5, 6), slice(6, 7)],
        ]
        anims = []
        for idx_pair in idx_link:
            if idx_pair[0] is None:  # FadeIn assoc
                anims.append(FadeIn(assoc[idx_pair[1]]))
            elif idx_pair[1] is None:  # FadeOut original
                anims.append(FadeOut(result[idx_pair[0]], shift=UP * 0.5))
            else:  # Transform
                anims.append(Transformr(result[idx_pair[0]], assoc[idx_pair[1]]))
        self.playw(*anims)

        ## w + ba circumscribe and PURPLE
        self.playw(FlashUnder(assoc[1:5]), assoc[1:5].animate.set_color(YELLOW))

        ## BA
        wba = randn(7, 7).scale(0.35).set_color(BLUE).move_to(VGroup(lwb, lwa))
        for i in range(7):
            for j in range(7):
                idx = i * 7 + j
                if idx % 7 == 3 or 21 <= idx < 28:
                    elem = wba[i * 7 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))
        lbat = (
            Tex("BA", font_size=32)
            .next_to(wba, UP, buff=0.07)
            .align_to(wba, RIGHT)
            .set_color(BLUE)
        )
        self.playw(
            FadeTransform(VGroup(lwb, lwa), wba),
            FadeOut(VGroup(lat, lbt)),
            FadeIn(lbat),
        )

        ## W shape
        w_shape = Tex("D_{in} \\times D_{out}", font_size=32).next_to(wt, UP, buff=0.15)
        ba_shape = (
            Tex("D_{in} \\times r \\cdot r \\times D_{out}", font_size=32)
            .next_to(lbat, UP, buff=0.15)
            .set_color(BLUE)
        )
        ba_shape[4:7].set_color(RED)
        self.playw(FadeIn(w_shape))
        self.playw(FadeIn(ba_shape))

        ## matmul BA
        self.playw(FadeOut(ba_shape[4:8], shift=UP * 0.7), ba_shape[8:].animate.align_to(ba_shape[4], LEFT))
        ba_shape[4:8].set_opacity(0)
        ## W + BA
        wpba = randn(7, 7).scale(0.35).set_color(YELLOW_B).move_to(weight)
        for i in range(7):
            for j in range(7):
                idx = i * 7 + j
                if idx % 7 == 3 or 21 <= idx < 28:
                    elem = wpba[i * 7 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))
        lpba = (
            Tex("W + BA", font_size=32)
            .next_to(wpba, UP, buff=0.07)
            .align_to(wpba, RIGHT)
            .set_color(YELLOW_B)
        )
        self.playw(
            FadeTransform(VGroup(weight, wba), wpba),
            FadeOut(lout2),
            FadeOut(lin2),
            VGroup(ba_shape, w_shape).animate.set_opacity(0),
            FadeTransform(VGroup(lbat, wt), lpba),
            self.cf.animate.shift(LEFT*2)
        )

class QLoRA(InteractiveScene, Scene2D):
    def construct(self):
        
        scale = 0.35
        ## weight
        weight = randn(7, 7).scale(scale).set_color(GREY_A).shift(LEFT * 2)
        for i in range(7):
            for j in range(7):
                idx = i * 7 + j
                if idx % 7 == 3 or 21 <= idx < 28:
                    elem = weight[i * 7 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))

        ## lweight
        lwa = randn(3, 7).scale(scale).set_color(BLUE)
        for i in range(3):
            for j in range(7):
                idx = i * 7 + j
                if idx % 7 == 3 or 7 <= idx < 14:
                    elem = lwa[i * 7 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))
        lwb = randn(7, 3).scale(scale).set_color(BLUE)
        for i in range(7):
            for j in range(3):
                idx = i * 3 + j
                if idx % 3 == 1 or 9 <= idx < 12:
                    elem = lwb[i * 3 + j]
                    elem.become(Text("...", font_size=20).set_color(GREY).move_to(elem))
        lweight = VGroup(lwa, lwb).arrange(RIGHT)

        VGroup(weight, lweight).arrange(RIGHT, buff=1)

        ## lins, louts
        lin1 = Line(weight.get_bottom() + DOWN * 2, weight.get_bottom()).set_color(
            GREY_B
        )
        lin2 = BrokenLine(
            weight.get_bottom() + DOWN,
            [lweight.get_bottom()[0], (weight.get_bottom() + DOWN)[1], 0],
            lweight.get_bottom(),
        ).set_color(GREY_B)
        lin = VGroup(lin1, lin2)

        oplus = VGroup(
            t := Text("⊕", font_size=30).next_to(weight, UP, buff=1.5)
        ).set_color(GREEN)
        lout1 = Line(weight.get_top(), oplus.get_bottom()).set_color(GREY_B)
        lout2 = BrokenLine(
            lweight.get_top(),
            [lweight.get_top()[0], oplus.get_right()[1], 0],
            oplus.get_right(),
        ).set_color(GREY_B)
        lplus = Line(oplus.get_top(), oplus.get_top() + UP).set_color(GREY_B)
        lout = VGroup(lout1, lout2, lplus)
        self.addw(weight, lweight, lin, lout, oplus)

        ## original weight is freezed
        fbox = SurroundingRectangle(weight, color=BLUE, buff=0.1).set_fill(BLUE, opacity=0.5).set_stroke(width=1)
        ftext = Text("Freezed", font_size=20).next_to(fbox, UP, buff=0.1, aligned_edge=RIGHT).set_color(BLUE)
        self.playw(weight[:-2].animate.set_opacity(0.5),FadeIn(fbox), FadeIn(ftext))

        ## 4bit quantize
        qtext = Text("4-bit Quantize", font_size=20).next_to(fbox, UP, buff=0.07, aligned_edge=RIGHT).set_color(BLUE)
        self.play(FadeIn(qtext, shift=UP*0.3), FadeOut(ftext, shift=UP*0.3))
        self.playw(FadeOut(fbox))

        ## 32bit quantize
        btexta = Text("32-bit Quantize", font_size=20).next_to(lwa, UP, buff=0.07, aligned_edge=RIGHT).set_color(BLUE)
        btextb = Text("32-bit Quantize", font_size=20).next_to(lwb, UP, buff=0.07, aligned_edge=RIGHT).set_color(BLUE)
        self.playw(FadeIn(btexta), FadeIn(btextb))

        ## Rwiggle weight
        ol = self.overlay
        self.add(weight.set_z_index(ol.z_index+1))
        self.playw(FadeIn(ol, run_time=0.5), RWiggle(weight, amp=0.1, speed=3, run_time=2.5))

        self.embed()
        ## fadeout ol
        self.play(FadeOut(ol, run_time=0.75))
        self.playw(*[Indicate(item) for item in lwa[:-2]], *[Indicate(item) for item in lwb[:-2]])