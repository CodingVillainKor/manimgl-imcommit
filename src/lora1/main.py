from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class whatisLoRA(InteractiveScene, Scene2D):
    def construct(self):

        ## intro

        def get_layer():
            layer = Rectangle(width=4, height=5)
            attn = Rectangle(width=3, height=2.5, color=GREEN_B)
            ffn = Rectangle(width=3, height=1.5, color=ORANGE)
            VGroup(attn, ffn).arrange(UP, buff=0.4)
            return VGroup(layer, attn, ffn)

        layers = VGroup(*[get_layer() for _ in range(3)])
        pre_layer = Text("...").next_to(layers, DOWN).rotate(PI / 2)
        post_layer = Text("...").next_to(layers, UP).rotate(PI / 2)
        layers = (
            VGroup(pre_layer, *layers, post_layer)
            .arrange(UP, buff=1.2)
            .scale(0.3)
            .shift(UP * 0.5)
        )
        weight = randn(7, 7).scale(0.35 * 0.3).move_to(layers[2][1])
        for i in range(7):
            weight[i * 7 + 3].become(
                Text("...", font_size=8)
                .set_color(GREY_C)
                .move_to(weight[i * 7 + 3].get_center())
            )
        for item in weight[21:28]:
            item.become(
                Text("...", font_size=8).set_color(GREY_C).move_to(item.get_center())
            )

        weight.stretch_to_fit_width(weight.get_width() * 0.6)
        line1 = Line(pre_layer.get_top() + UP * 0.1, layers[1][1], color=GREY_C)
        line2 = Line(layers[1][2], layers[2][1], color=GREY_C)
        line3 = Line(layers[2][2], layers[3][1], color=GREY_C)
        line4 = Line(layers[3][2], post_layer.get_bottom() + DOWN * 0.1, color=GREY_C)

        self.playw(
            FadeIn(layers),
            FadeIn(line1),
            FadeIn(line2),
            FadeIn(line3),
            FadeIn(line4),
            FadeIn(weight),
        )

        ## scale up

        self.playw(
            VGroup(layers, line1, line2, line3, line4, weight)
            .animate.scale(5)
            .shift(UP)
        )

        ## pretrained
        t = (
            Text("Pretrained", font_size=24)
            .set_color_by_gradient(BLUE_A, BLUE_C)
            .next_to(weight, RIGHT)
            .align(weight, UP, buff=0.1)
            .add_background_rectangle(color=BLACK, opacity=0.9)
        )
        self.playw(FadeIn(t, shift=RIGHT * 0.2))

        self.playw(FlashUnder(t, color=BLUE_B, buff=0.05))

        ## Indicate weight numbers
        self.playw(*[Indicate(item) for item in weight[:-2]])

        ## transform new randn
        weight_ = randn(7, 7).scale(0.35 * 0.3).move_to(layers[2][1])
        for i in range(7):
            weight_[i * 7 + 3].become(
                Text("...", font_size=8)
                .set_color(GREY_C)
                .move_to(weight_[i * 7 + 3].get_center())
            )
        for item in weight_[21:28]:
            item.become(
                Text("...", font_size=8).set_color(GREY_C).move_to(item.get_center())
            )
        weight_.scale(5).stretch_to_fit_width(weight_.get_width() * 0.6)
        self.playw(Transform(weight, weight_))

        ## stretch layer[2]s
        lbox = layers[2][0]
        lattn = layers[2][1]
        self.playw(
            lbox.animate.stretch_to_fit_width(lbox.get_width() * 1.75).align_to(
                lbox, LEFT
            ),
            lattn.animate.stretch_to_fit_width(lattn.get_width() * 2).align_to(
                lattn, LEFT
            ),
            FadeOut(t, shift=RIGHT * 4.7),
            self.cf.animate.shift(RIGHT * 2),
        )

        ## lora weight
        lweight = randn(5, 7).scale(0.35 * 0.3).move_to(layers[2][1])
        for i in range(5):
            lweight[i * 7 + 3].become(
                Text("...", font_size=8)
                .set_color(GREY_C)
                .move_to(lweight[i * 7 + 3].get_center())
            )
        for item in lweight[14:21]:
            item.become(
                Text("...", font_size=8).set_color(GREY_C).move_to(item.get_center())
            )
        lweight.scale(5).stretch_to_fit_width(lweight.get_width() * 0.6).next_to(
            weight, RIGHT, buff=0.2
        ).set_color(GREEN)
        self.playw(FadeIn(lweight), weight.animate.set_opacity(0.5))

        ## fill weight freezed
        sr_weight = SurroundingRectangle(weight, color=BLUE, buff=0.0).set_opacity(0.3)
        tf = (
            Text("freezed", font_size=24)
            .next_to(sr_weight, LEFT)
            .align_to(sr_weight, UP)
            .set_color(BLUE)
            .add_background_rectangle(color=BLACK, opacity=0.9)
        )
        sr_ffn = SurroundingRectangle(layers[2][2], color=BLUE, buff=0.0).set_opacity(
            0.3
        )
        self.playw(FadeIn(sr_weight), FadeIn(tf), FadeIn(sr_ffn))

        ## lweight update
        lweight_ = randn(5, 7).scale(0.35 * 0.3).move_to(layers[2][1])
        for i in range(5):
            lweight_[i * 7 + 3].become(
                Text("...", font_size=8)
                .set_color(GREY_C)
                .move_to(lweight_[i * 7 + 3].get_center())
            )
        for item in lweight_[14:21]:
            item.become(
                Text("...", font_size=8).set_color(GREY_C).move_to(item.get_center())
            )
        lweight_.scale(5).stretch_to_fit_width(lweight_.get_width() * 0.6).next_to(
            weight, RIGHT, buff=0.2
        ).set_color(RED)
        self.play(Transform(lweight, lweight_), run_time=0.75)
        self.playw(lweight.animate.set_color(GREEN), run_time=0.75, wait=3)

        ## 나란히
        self.play(*[Indicate(w) for w in weight[:-2]])
        self.playw(*[Indicate(w) for w in lweight[:-2]])

        ## input
        lora_in = BrokenLine(
            line2.get_end() + DOWN * 0.25,
            [lweight.get_bottom()[0], (line2.get_end() + DOWN * 0.25)[1], 0],
            lweight.get_bottom(),
        )
        self.playw(
            FadeIn(lora_in),
            line2.animate.put_start_and_end_on(line2.get_start(), weight.get_bottom()),
            layers[2][1].animate.set_stroke(opacity=0.4),
        )

        ## output
        oplus = VGroup(
            t := Text("+", font_size=18),
            Circle(radius=0.1).move_to(t).set_color(GREY_A),
        ).next_to(weight, UP, buff=0.3)
        lo_weight = Line(weight.get_top(), oplus.get_bottom())
        lo_lora = BrokenLine(
            lweight.get_top(),
            [lweight.get_top()[0], oplus.get_right()[1], 0],
            oplus.get_right(),
        )
        lo_up = Line(oplus.get_top(), layers[2][2].get_bottom())
        self.playw(FadeIn(oplus), FadeIn(lo_weight), FadeIn(lo_lora), FadeIn(lo_up))

        ## 나란히2
        self.play(*[Indicate(w, color=BLUE) for w in weight[:-2]])
        self.playw(*[Indicate(w) for w in lweight[:-2]])

        ## lowrank and ol
        ol = self.overlay
        self.add(lweight.set_z_index(ol.z_index + 1))
        lora_t = (
            Text("Low Rank", font_size=20)
            .next_to(lweight, UP)
            .align_to(lweight, RIGHT)
            .set_color(GREEN_E)
            .set_z_index(ol.z_index + 1)
        )
        self.playw(FadeIn(lora_t), FadeIn(ol))

        ## fadeout ol
        self.play(FadeOut(ol), FadeOut(tf))

        ## weight brace
        wb1 = Brace(weight, DOWN).set_color(GREY_B)
        wb2 = Brace(weight, LEFT).set_color(GREY_B)
        tb1 = (
            Tex("D_{in}", font_size=36)
            .next_to(wb1, DOWN, buff=0.1)
            .add_background_rectangle(opacity=0.8)
        )
        tb2 = (
            Tex("D_{out}", font_size=36)
            .next_to(wb2, LEFT, buff=0.1)
            .add_background_rectangle(opacity=0.8)
        )
        self.play(FadeIn(wb1), FadeIn(wb2), FadeIn(tb1), FadeIn(tb2))
        self.playw(*[Indicate(w) for w in weight[:-2]], wait=3)

        ## indicate lweight
        self.play(*[Indicate(w) for w in lweight[:-2]])
        self.playw(lweight.animate.shift(RIGHT * 6), self.cf.animate.shift(RIGHT * 12))

        ## LoRA A, B
        aweight = randn(3, 7).scale(0.4)
        for i in range(len(aweight[:-2])):
            if i % 7 == 3 or 7 <= i < 14:
                aweight[i].become(Text("...", font_size=20).move_to(aweight[i]))
        aweight.stretch_to_fit_width(aweight.get_width() * 0.7)
        bweight = randn(7, 3).scale(0.4)
        for i in range(len(bweight[:-2])):
            if i % 3 == 1 or 9 <= i < 12:
                bweight[i].become(Text("...", font_size=20).move_to(bweight[i]))
        bweight.stretch_to_fit_width(bweight.get_width() * 0.7)
        ab = (
            VGroup(aweight, bweight)
            .arrange(RIGHT, buff=0.1)
            .next_to(lweight, RIGHT, buff=1.0)
            .set_color(GREEN_A)
        )
        self.play(FadeIn(ab))

        ## at, bt
        at = Tex("D_{in} \\times 16", font_size=32)
        bt = Tex("16 \\times D_{out}", font_size=32)
        bt.next_to(bweight, DOWN)
        at.next_to(aweight, DOWN).align_to(bt, DOWN)
        self.playw(FadeIn(at), FadeIn(bt))

        ## Di and Do is 1024, normally
        at_ = Tex("1024 \\times 16", font_size=32).move_to(at)
        at_[:4].set_color(RED)
        bt_ = Tex("16 \\times 1024", font_size=32).move_to(bt)
        bt_[-4:].set_color(RED)
        self.playw(Transform(at, at_), Transform(bt, bt_))

        self.playw(FlashUnder(at[:4], color=RED), FlashUnder(bt_[-4:], color=RED))

        ## fadeout lweight and ab, at, bt into low-rank representation
        self.remove(tb1, tb2, wb1, wb2)
        self.playw(
            self.cf.animate.shift(LEFT*12),
            FadeOut(lweight, shift=LEFT * 12),
            ab.animate.shift(LEFT * 12).stretch_to_fit_width(ab.get_width() * 0.7),
            at.animate.shift(LEFT * 11.8), bt.animate.shift(LEFT * 12.5),
            run_time=1.5
        )


        ## indicate lowrank
        self.play(*[Indicate(item) for item in ab[0][:-2]])
        self.playw(*[Indicate(item) for item in ab[1][:-2]])

class comparisonLora(InteractiveScene, Scene2D):
    def construct(self):

        ## param num
        num_param = Words("Number of Parameters:", font_size=24).set_color_by_gradient(GREEN_A, GREEN_C)
        self.playwl(*[FadeIn(word) for word in num_param.words], lag_ratio=0.5)

        ## full-rank
        tex_full = Tex("D_{in} \\times D_{out} =", font_size=32).set_color(RED)
        shape_full = Text("(1024 × 1024):", font=MONO_FONT, font_size=28).set_color(RED)
        w_full = randn(7, 7).scale(0.35)
        for i in range(len(w_full[:-2])):
            if i % 7 == 3 or 21 <= i < 28:
                w_full[i].become(Text("...", font_size=20).move_to(w_full[i]))
        fulls = VGroup(tex_full, shape_full, w_full.set_color(RED_A)).arrange(RIGHT).shift(UP*1.25)
        self.play(num_param.animate.next_to(fulls, UP).align_to(fulls, LEFT), run_time=0.5)
        self.play(FadeIn(tex_full))
        self.play(FadeIn(shape_full))
        milt = Tex("\\approx \\text{1M}", font_size=32).next_to(fulls, RIGHT).set_color(RED_A)
        self.playw(FadeIn(w_full), FadeIn(milt))

        ## low-rank
        tex_low = Tex("D_{in} \\times r \\times r \\times D_{out} =", font_size=32).set_color(BLUE)
        tex_low[:5].set_color(BLUE_A)
        tex_low[6:12].set_color(PURPLE)
        shape_low = Text("(1024 × 16 × 16 × 1024):", font=MONO_FONT, font_size=28).set_color(BLUE)
        shape_low[:8].set_color(BLUE_A)
        shape_low[9:16].set_color(PURPLE)
        w_lowa = randn(7, 3).scale(0.35)
        for i in range(len(w_lowa[:-2])):
            if i % 3 == 1 or 9 <= i < 12:
                w_lowa[i].become(Text("...", font_size=20).move_to(w_lowa[i]))
        w_lowb = randn(3, 7).scale(0.35)
        for i in range(len(w_lowb[:-2])):
            if i % 7 == 3 or 7 <= i < 14:
                w_lowb[i].become(Text("...", font_size=20).move_to(w_lowb[i]))
        w_low = VGroup(w_lowa, w_lowb).arrange(RIGHT, buff=0.1)
        lows = VGroup(tex_low, shape_low, w_low.set_color(BLUE_A)).arrange(RIGHT).shift(DOWN*1.55).align_to(fulls, LEFT)
        pa = Tex("\\approx \\text{16k}", font_size=32).next_to(w_lowa, DOWN).set_color(BLUE_A)
        pb = Tex("\\approx \\text{16k}", font_size=32).next_to(w_lowb, DOWN).set_color(BLUE_B).align_to(pa, DOWN)
        self.playw(FadeIn(tex_low), FadeIn(shape_low), self.cf.animate.shift(DOWN*0.5 + RIGHT * 2).scale(1.2))
        self.playw(FadeIn(w_low), FadeIn(pa), FadeIn(pb))
        self.embed()
        ## pab
        pab = Tex("\\approx \\text{32k}", font_size=32).move_to(VGroup(pa, pb))
        self.playw(Transformr(VGroup(pa, pb), pab))

        ## Indicate params
        ol = self.overlay
        self.add(milt.set_z_index(ol.z_index+1), pab.set_z_index(ol.z_index+1))
        self.play(FadeIn(ol))
        self.play(Indicate(milt, color=PURE_RED))
        self.playw(Indicate(pab, color=BLUE))

        