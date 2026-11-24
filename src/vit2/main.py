from manimlib import *
from raenimgl import *
from random import seed
from PIL import Image

seed(41)
np.random.seed(41)


def patchify(path, size=56, p=14, width=2):
    # center-crop to square, resize to size x size, split into (size/p)^2 patches
    n = size // p
    arr = np.array(Image.open(path).convert("RGB"))
    h, w = arr.shape[:2]
    s = min(h, w)
    arr = arr[(h - s) // 2 : (h + s) // 2, (w - s) // 2 : (w + s) // 2]
    arr = np.array(Image.fromarray(arr).resize((size, size)))
    # (n, n, p, p, 3): patches[i, j] is the patch at row i, column j
    patches = arr.reshape(n, p, n, p, 3).swapaxes(1, 2)

    img = VGroup()
    for i in range(n):
        for j in range(n):
            patch = VGroup(
                *[
                    Pixel(width / size, fill_color=rgb_to_color(c / 255))
                    for c in patches[i, j].reshape(-1, 3)
                ]
            ).arrange_in_grid(p, p, buff=0)
            img.add(patch)
    img.arrange_in_grid(n, n, buff=0)

    # pixel (r, c) of arr, looked up through its patch
    def px(r, c):
        return img[(r // p) * n + c // p][(r % p) * p + c % p]

    return img, arr, px


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## model

        img, arr, px = patchify("ggilggil.png")
        img.save_state()
        img.arrange(RIGHT)
        self.play(FadeIn(img))

        ## 1D positional encoding idx
        pe = VGroup()
        for i in range(len(img)):
            idx = Text(str(i), font_size=20).next_to(img[i], DOWN)
            pe.add(idx)
        self.playwl(*[FadeIn(idx) for idx in pe], lag_ratio=0.2)

        ## restore
        pe.save_state()
        pe.generate_target().set_opacity(0)
        pe.target[:4].arrange(RIGHT, buff=0.4).next_to(
            img.saved_state[:4], UP, buff=0.1
        ).set_opacity(1)
        pe.target[4::4].arrange(DOWN, buff=0.4).next_to(
            img.saved_state[4::4], LEFT, buff=0.1
        ).set_opacity(1)
        self.playw(Restore(img), MoveToTarget(pe))

        ## indicate [0], [4], [8], [12]
        self.play(Indicate(img[0], color=RED), Indicate(pe[0], color=RED))
        self.play(Indicate(img[4], color=RED), Indicate(pe[4], color=RED))
        self.play(Indicate(img[8], color=RED), Indicate(pe[8], color=RED))
        self.playw(Indicate(img[12], color=RED), Indicate(pe[12], color=RED), wait=4)

        ## model
        model_box = Rectangle(width=12, height=2.5)
        model_text = (
            Text("Model", font_size=24).align(model_box, UR, buff=0.1).set_color(GREY_B)
        )
        model = VGroup(model_box, model_text).shift(UP * 1.75)
        self.play(
            img.animate.arrange(RIGHT).next_to(model, DOWN, buff=0.3), Restore(pe)
        )
        self.playw(FadeIn(model), wait=5)

        ## lagged indicate
        self.playwl(
            *[
                AnimationGroup(Indicate(img[i], color=RED), Indicate(pe[i], color=RED))
                for i in range(len(img))
            ],
            lag_ratio=0.3,
            wait=2.5,
        )

        ## indicate row-wise
        r1 = VGroup(*[VGroup(img[j], pe[j]) for j in range(4)])
        r2 = VGroup(*[VGroup(img[j], pe[j]) for j in range(4, 8)])
        r3 = VGroup(*[VGroup(img[j], pe[j]) for j in range(8, 12)])
        r4 = VGroup(*[VGroup(img[j], pe[j]) for j in range(12, 16)])
        self.play(Indicate(r1, color=RED, scale_factor=1.1))
        self.play(Indicate(r2, color=RED, scale_factor=1.1))
        self.play(Indicate(r3, color=RED, scale_factor=1.1))
        self.playw(Indicate(r4, color=RED, scale_factor=1.1))


class topology2D(InteractiveScene, Scene2D):
    def construct(self):

        ## img
        img, arr, px = patchify("ggilggil.png")
        pe0123 = VGroup(
            *[
                Text(str(i), font_size=20).next_to(img[i], UP, buff=0.1)
                for i in range(4)
            ]
        )
        pe04812 = VGroup(
            *[
                Text(str(i), font_size=20).next_to(img[i], LEFT, buff=0.1)
                for i in [0, 4, 8, 12]
            ]
        )

        self.playw(FadeIn(img), FadeIn(pe0123), FadeIn(pe04812), run_time=0.5)

        ## row-wise then column-wise indicate
        self.playwl(
            *[
                AnimationGroup(
                    Indicate(img[i], color=RED), Indicate(pe0123[i], color=RED)
                )
                for i in range(4)
            ],
            lag_ratio=0.25,
            wait=0,
        )
        self.playwl(
            *[
                AnimationGroup(
                    Indicate(img[i * 4], color=RED), Indicate(pe04812[i], color=RED)
                )
                for i in range(4)
            ],
            lag_ratio=0.25,
        )

        ## column-wise indicate
        self.playwl(
            *[
                AnimationGroup(
                    Indicate(img[i * 4], color=RED),
                    pe04812[i]
                    .animate(rate_func=there_and_back)
                    .shift(LEFT * 0.5)
                    .set_color(PURE_RED),
                )
                for i in range(4)
            ],
            lag_ratio=0.75,
            wait=12,
        )

        ## model
        model_box = Rectangle(width=12, height=2.5)
        model_text = (
            Text("Model", font_size=24).align(model_box, UR, buff=0.1).set_color(GREY_B)
        )
        model = VGroup(model_box, model_text).shift(UP * 1.75)
        img.generate_target().arrange(RIGHT).next_to(model, DOWN, buff=0.3)
        pe = VGroup(
            *[
                Text(str(i), font_size=20).next_to(img.target[i], DOWN, buff=0.1)
                for i in range(len(img))
            ]
        )
        self.remove(pe0123, pe04812)
        self.play(MoveToTarget(img), FadeIn(pe), run_time=0.75)
        self.play(FadeIn(model), run_time=0.75)

        ## 1 and 5
        pe.save_state(), img.save_state()
        pe.generate_target(), img.generate_target()
        [pe.target[i].set_opacity(0.1) for i in range(len(pe)) if i not in [1, 5]]
        [img.target[i].set_opacity(0.1) for i in range(len(img)) if i not in [1, 5]]
        bline = DashedVMobject(
            BrokenLine(
                pe[1].get_bottom() + DOWN * 0.1,
                (pe[1].get_bottom() + pe[5].get_bottom()) / 2 + DOWN * 0.5,
                pe[5].get_bottom() + DOWN * 0.1,
                smooth=True,
            )
        )
        self.playw(MoveToTarget(img), MoveToTarget(pe), FadeIn(bline))


class relativePosition(InteractiveScene, Scene2D):
    def construct(self):
        self.cf.save_state()
        self.cf.reorient(0, 74, 0, (0.35, -0.03, -0.06), 8.00)

        ## short brief: 2D
        nump = RaenimPlane(
            x_range=[-0.5, 5, 1], y_range=[-0.5, 5, 1], width=10, height=10
        )
        self.addw(nump)

        ## d1 ~ d4
        c1, c2, c3, c4 = (1, 2), (2.5, 4), (2, 1.2), (4, 2.7)
        # |c2-c1| == |c4-c3|
        d1 = Dot(nump.c2p(*c1)).set_color(GREEN)
        d2 = Dot(nump.c2p(*c2)).set_color(GREEN)
        d3 = Dot(nump.c2p(*c3)).set_color(BLUE)
        d4 = Dot(nump.c2p(*c4)).set_color(BLUE)
        l12 = DashedLine(d1.get_center(), d2.get_center()).set_color(GREEN)
        l34 = DashedLine(d3.get_center(), d4.get_center()).set_color(BLUE)
        self.playw(
            FadeIn(d1),
            FadeIn(d2),
            FadeIn(d3),
            FadeIn(d4),
            FadeIn(l12),
            FadeIn(l34),
            wait=0.75,
        )

        ## pe
        def pe(point, color):
            text = (
                Text(f"r({point[0]}, {point[1]})", font_size=20)
                .set_color(color)
                .next_to(nump.c2p(*point), OUT, buff=0.2)
                .rotate(74 * DEGREES, axis=RIGHT)
            )
            return text

        pe1 = pe(c1, GREEN)
        pe2 = pe(c2, GREEN)
        pe3 = pe(c3, BLUE)
        pe4 = pe(c4, BLUE)
        self.playw(FadeIn(pe1), FadeIn(pe2), FadeIn(pe3), FadeIn(pe4), wait=2)

        ## dot prod each color pair
        dot12 = (
            Text("·", font_size=20).rotate(74 * DEGREES, axis=RIGHT).set_color(GREEN)
        )
        dot34 = Text("·", font_size=20).rotate(74 * DEGREES, axis=RIGHT).set_color(BLUE)
        pe1.generate_target(), pe2.generate_target(), pe3.generate_target(), pe4.generate_target()
        VGroup(pe1.target, dot12, pe2.target).arrange(RIGHT, buff=0.05).next_to(
            l12, OUT, buff=0.2
        )
        VGroup(pe3.target, dot34, pe4.target).arrange(RIGHT, buff=0.05).next_to(
            l34, IN, buff=0.2
        )
        self.play(
            MoveToTarget(pe1),
            MoveToTarget(pe2),
            MoveToTarget(pe3),
            MoveToTarget(pe4),
            FadeIn(dot12),
            FadeIn(dot34),
        )

        ## ll12, ll34
        ll12 = Line(d1.get_center(), d2.get_center()).set_color(GREEN)
        ll34 = Line(d3.get_center(), d4.get_center()).set_color(BLUE)
        self.play(Create(ll12), run_time=0.75)
        self.playw(Create(ll34), run_time=0.75)

        ## remove all
        self.play(
            FadeOut(d1),
            FadeOut(d2),
            FadeOut(d3),
            FadeOut(d4),
            FadeOut(l12),
            FadeOut(l34),
            FadeOut(ll12),
            FadeOut(ll34),
            FadeOut(pe1),
            FadeOut(pe2),
            FadeOut(pe3),
            FadeOut(pe4),
            FadeOut(dot12),
            FadeOut(dot34),
            FadeOut(nump),
            run_time=0.5,
        )
        self.cf.restore()

        ## four nump
        W = [3.5, 1.3]
        np1 = RaenimPlane(x_range=[-0.5, 11, 1], y_range=[-1, 1], width=12, height=1.5)
        np2 = RaenimPlane(x_range=[-0.5, 11, 1], y_range=[-1, 1], width=12, height=1.5)
        np3 = RaenimPlane(x_range=[-0.5, 11, 1], y_range=[-1, 1], width=12, height=1.5)
        np4 = RaenimPlane(x_range=[-0.5, 11, 1], y_range=[-1, 1], width=12, height=1.5)
        np1.x_axis.tip.scale(0.7), np1.y_axis.tip.scale(0.7)
        np2.x_axis.tip.scale(0.7), np2.y_axis.tip.scale(0.7)
        np3.x_axis.tip.scale(0.7), np3.y_axis.tip.scale(0.7)
        np4.x_axis.tip.scale(0.7), np4.y_axis.tip.scale(0.7)
        fn1, fn2, fn3, fn4 = (
            lambda x: np.cos(W[0] * x),
            lambda x: np.cos(W[1] * x),
            lambda x: np.sin(W[0] * x),
            lambda x: np.sin(W[1] * x),
        )
        fns = [fn1, fn2, fn3, fn4]
        np1.add(np1.get_graph(fn1).set_color(GREEN))
        np2.add(np2.get_graph(fn2).set_color(GREEN))
        np3.add(np3.get_graph(fn3).set_color(BLUE))
        np4.add(np4.get_graph(fn4).set_color(BLUE))

        nps = VGroup(np1, np2, np3, np4).arrange(DOWN, buff=0.3)

        self.play(FadeIn(nps), run_time=0.5)
        self.playw(
            self.cf.animate.reorient(0, 74, 0, (0.00, 0, 1.00), 8.00), run_time=0.5
        )

        ## pos 3, pos 5
        pos3_dots = VGroup(*[Dot(nps[i].c2p(3, fns[i](3))) for i in range(4)])
        pos5_dots = VGroup(*[Dot(nps[i].c2p(5, fns[i](5))) for i in range(4)])
        rotate = lambda x: x.rotate(74 * DEGREES, axis=RIGHT)
        pe1 = (
            rotate(Tex("r_3", font_size=32))
            .next_to(pos3_dots, OUT, buff=2)
            .shift(LEFT * 0.5)
        )
        pe2 = (
            rotate(Tex("r_5", font_size=32))
            .next_to(pos5_dots, OUT, buff=2)
            .shift(LEFT * 0.75)
        )
        pes = VGroup(pe1, pe2)
        lines1 = VGroup(
            *[DashedLine(pos3_dots[i].get_center(), pe1.get_bottom()) for i in range(4)]
        )
        lines2 = VGroup(
            *[DashedLine(pos5_dots[i].get_center(), pe2.get_bottom()) for i in range(4)]
        )
        lines = VGroup(lines1, lines2)
        dot12 = rotate(Text("·", font_size=24)).move_to(VGroup(pe1, pe2).get_center())
        self.playw(
            FadeIn(pos3_dots),
            FadeIn(pos5_dots),
            FadeIn(pes),
            FadeIn(lines),
            FadeIn(dot12),
            wait=1.5,
        )

        ## pos 6, pos 8
        pos6_dots = VGroup(*[Dot(nps[i].c2p(6, fns[i](6))) for i in range(4)])
        pos8_dots = VGroup(*[Dot(nps[i].c2p(8, fns[i](8))) for i in range(4)])
        pe3 = (
            rotate(Tex("r_6", font_size=32))
            .next_to(pos6_dots, OUT, buff=2)
            .shift(RIGHT * 0.5)
        )
        pe4 = (
            rotate(Tex("r_8", font_size=32))
            .next_to(pos8_dots, OUT, buff=2)
            .shift(RIGHT * 0.25)
        )
        pes2 = VGroup(pe3, pe4)
        lines3 = VGroup(
            *[DashedLine(pos6_dots[i].get_center(), pe3.get_bottom()) for i in range(4)]
        )
        lines4 = VGroup(
            *[DashedLine(pos8_dots[i].get_center(), pe4.get_bottom()) for i in range(4)]
        )
        lines5 = VGroup(lines3, lines4)
        dot34 = rotate(Text("·", font_size=24)).move_to(VGroup(pe3, pe4).get_center())
        self.playw(
            FadeIn(pos6_dots),
            FadeIn(pos8_dots),
            FadeIn(pes2),
            FadeIn(lines5),
            FadeIn(dot34),
            wait=2.5,
        )

        ## indicate pe3, 5, 6, 8
        self.play(Indicate(pe1))
        self.play(Indicate(pe2))
        self.play(Indicate(pe3), run_time=0.5)
        self.playw(Indicate(pe4), run_time=0.5)

        ## neq1~3
        neq1 = rotate(Tex("\\neq", font_size=32)).move_to(VGroup(pe1, pe2).get_center())
        neq2 = rotate(Tex("\\neq", font_size=32)).move_to(VGroup(pe2, pe3).get_center())
        neq3 = rotate(Tex("\\neq", font_size=32)).move_to(VGroup(pe3, pe4).get_center())

        self.playw(
            FadeOut(dot12), FadeOut(dot34), FadeIn(neq1), FadeIn(neq2), FadeIn(neq3)
        )

        ## fadeout neq and re fadein dots
        self.play(
            FadeOut(neq1), FadeOut(neq2), FadeOut(neq3), FadeIn(dot12), FadeIn(dot34)
        )
        self.playw(Indicate(VGroup(pe1, dot12, pe2), scale_factor=1.1), wait=0.5)
        self.playw(Indicate(VGroup(pe3, dot34, pe4), scale_factor=1.1))

        ## cos(5-3), cos(8-6)
        cos53 = (
            rotate(Tex("f(\\cos(3-5))", font_size=32))
            .move_to(VGroup(pe1, pe2).get_center())
            .shift(OUT * 0.5)
            .set_color(ORANGE)
        )
        cos86 = (
            rotate(Tex("f(\\cos(6-8))", font_size=32))
            .move_to(VGroup(pe3, pe4).get_center())
            .shift(OUT * 0.5)
            .set_color(ORANGE)
        )

        self.playw(FadeIn(cos53), FadeIn(cos86), wait=1.5)
        eq = rotate(Text("=", font_size=28)).move_to(VGroup(cos53, cos86).get_center())
        self.playw(FadeIn(eq), wait=2)


class subimagePosition(InteractiveScene, Scene2D):
    def construct(self):

        ## total frame
        total_frame = Rectangle(width=10, height=6).shift(UP * 0.5).scale(0.8)
        img, arr, px = patchify("ggilggil.png")
        img.set_z_index(1)
        self.play(FadeIn(total_frame), FadeIn(img), run_time=0.5)

        img.generate_target().shift(OUT * 2)
        dpatches = VGroup(
            *[
                DashedVMobject(
                    Polygon(*[patch.get_corner(corner) for corner in [UL, UR, DR, DL]]),
                    num_dashes=12,
                )
                for patch in img
            ]
        )
        lines = VGroup(
            *[
                DashedLine(img.get_corner(UL), img.target.get_corner(UL)),
                DashedLine(img.get_corner(UR), img.target.get_corner(UR)),
                DashedLine(img.get_corner(DL), img.target.get_corner(DL)),
                DashedLine(img.get_corner(DR), img.target.get_corner(DR)),
            ]
        )

        self.playw(
            self.cf.animate.reorient(16, 57, 0, (0.29, 0.34, -0.48), 7.64),
            MoveToTarget(img),
            *[Create(line) for line in lines],
            FadeIn(dpatches),
        )

        ## lines and dpatches follow img
        base_z = dpatches.get_z()
        base_of = lambda p: np.array([p[0], p[1], base_z])

        # dpatches: shadow of img on the base plane, only move/scale (no point rebuild)
        def update_dpatches(m):
            if not np.isclose(m.get_width(), img.get_width()):
                m.set_width(img.get_width())
            m.move_to(base_of(img.get_center()))

        dpatches.add_updater(update_dpatches)

        # lines: store each dash point as a fraction along the line once,
        # then re-lay the dashes between the new ends every frame
        for line in lines:
            s, e = line.get_start_and_end()
            v = e - s
            line.alphas = [
                np.dot(dash.get_points() - s, v) / np.dot(v, v) for dash in line
            ]

        # factory so the updater takes only (m); a 2-arg lambda gets dt as its 2nd arg
        def line_updater(corner):
            def update(line):
                end = img.get_corner(corner)
                start = base_of(end)
                for dash, a in zip(line, line.alphas):
                    dash.set_points(start + a[:, None] * (end - start))

            return update

        for line, corner in zip(lines, [UL, UR, DL, DR]):
            line.add_updater(line_updater(corner))

        self.playw(img.animate.shift(UP * 0.5), run_time=0.5, wait=1.8)

        ## img shifts

        self.playw(img.animate.shift(UL + LEFT * 1.5), run_time=0.5, wait=0.8)

        self.playw(img.animate.shift(DR + RIGHT * 4), run_time=0.5, wait=0.75)

        ## clear updaters
        dpatches.clear_updaters()
        for line in lines:
            line.clear_updaters()

        ## img[5], img[-2]
        i5, i2 = img[5], img[-2]
        i5.save_state(), i2.save_state()
        dp5, dp2 = SurroundingRectangle(
            dpatches[5], buff=0, stroke_width=0
        ), SurroundingRectangle(dpatches[-2], buff=0, stroke_width=0)
        self.playw(i5.animate.set_color(RED), i2.animate.set_color(RED), run_time=0.75)
        self.playw(
            dp5.animate.set_fill(RED, opacity=1),
            dp2.animate.set_fill(RED, opacity=1),
            run_time=0.75,
            wait=0.5,
        )

        ## restore and add
        self.playw(
            i5.animate.restore(),
            i2.animate.restore(),
            FadeOut(dp5),
            FadeOut(dp2),
            run_time=0.75,
        )
        self.playw(
            img.animate.shift(IN * 2),
            dpatches.animate.set_opacity(0),
            FadeOut(lines),
            wait=1.5,
        )

        ## dpatches 1 and 0
        self.add(dpatches.set_z_index(2))
        self.playw(
            dpatches.animate(rate_func=there_and_back)
            .set_opacity(1)
            .set_color(PURE_RED),
            wait=1.5,
        )

        ## image out again
        self.playw(
            img.animate(rate_func=linear).shift(OUT * 2),
            dpatches.animate.set_opacity(1).set_color(GREY_A),
            *[Create(line) for line in lines],
        )

        ## i5, i2 shift in
        self.add(img.set_z_index(3))
        self.playw(
            i5.animate.shift(IN), i2.animate.shift(IN), FadeIn(dp5), FadeIn(dp2), wait=2
        )

        ic = VGroup(i5, i2).get_center()
        dpc = VGroup(dp5, dp2).get_center()
        self.playw(
            i5.animate(rate_func=there_and_back).move_to(ic),
            i2.animate(rate_func=there_and_back).move_to(ic),
            dp5.animate(rate_func=there_and_back).move_to(dpc),
            dp2.animate(rate_func=there_and_back).move_to(dpc),
        )

        ## copy
        cps = VGroup(img, dpatches, lines, dp5, dp2).copy().shift(UL + LEFT * 3)
        self.playw(FadeIn(cps), wait=1.5)

        ## indicate two img

        self.playwl(Indicate(img), Indicate(cps[0]), lag_ratio=0.5)

        self.embed()
        ## cp and orig
        cp_ic = VGroup(cps[0][5], cps[0][-2]).get_center()
        cp_dpc = VGroup(cps[-2], cps[-1]).get_center()
        self.playw(
            cps[0][5].animate(rate_func=there_and_back).move_to(cp_ic),
            cps[0][-2].animate(rate_func=there_and_back).move_to(cp_ic),
            cps[-2].animate(rate_func=there_and_back).move_to(cp_dpc),
            cps[-1].animate(rate_func=there_and_back).move_to(cp_dpc),
            i5.animate(rate_func=there_and_back).move_to(ic),
            i2.animate(rate_func=there_and_back).move_to(ic),
            dp5.animate(rate_func=there_and_back).move_to(dpc),
            dp2.animate(rate_func=there_and_back).move_to(dpc),
            wait=2
        )