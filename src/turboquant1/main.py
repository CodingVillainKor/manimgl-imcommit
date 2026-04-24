from manimlib import *
from raenimgl import *


class quant1(InteractiveScene, Scene2D):
    def construct(self):
        self.embed()
        ## turboquant name
        name = Text("TurboQuant", font="Noto Sans KR", font_size=36)

        turbo = name[:5].set_color(GREY_B)
        quant = name[5:].set_color(YELLOW_B)

        self.playwl(FadeIn(turbo), FadeIn(quant), lag_ratio=0.6)

        quant_full = (
            Text("Quantization", font="Noto Sans KR", font_size=24)
            .next_to(quant, DOWN, buff=0.3, aligned_edge=LEFT)
            .set_color_by_gradient(YELLOW_B, WHITE)
        )
        self.playw(FadeIn(quant_full, shift=DOWN * 0.3))

        ## quantization 1 bit

        self.play(FadeOut(name, shift=UP), FadeOut(quant_full, shift=UP))

        nump = RaenimPlane().scale(1.4)

        def add_ticks(plane: NumberPlane, value, xy="x"):
            if xy == "x":
                tick = Line(plane.c2p(value, 0.1), plane.c2p(value, -0.1), color=GREY_B)
            else:
                tick = Line(plane.c2p(0.1, value), plane.c2p(-0.1, value), color=GREY_B)
            return tick

        nump.y_axis.set_opacity(0)
        tick = add_ticks(nump, 0)
        zero = (
            Text("0", font="Noto Sans KR", font_size=24)
            .next_to(tick, DOWN, buff=0.1)
            .set_color(GREY_B)
        )
        self.playw(FadeIn(nump), FadeIn(tick), FadeIn(zero))

        dot = Dot(nump.c2p(0, 0)).set_color(RED_B).set_z_index(2)
        neg_line = Line(
            nump.c2p(0, 0), nump.c2p(-5, 0), color=RED_B, stroke_width=5
        ).set_z_index(1)
        self.playwl(FadeIn(dot), Write(neg_line), lag_ratio=0.3, wait=0)
        zero = (
            Text("0", font="Noto Sans KR", font_size=24)
            .next_to(neg_line, DOWN, buff=0.35)
            .set_color(RED_B)
        )
        self.playw(Transformr(VGroup(dot, neg_line).copy(), zero))
        pos_line = Line(
            nump.c2p(0, 0), nump.c2p(5, 0), color=BLUE_B, stroke_width=5
        ).set_z_index(1)
        self.play(Write(pos_line))
        one = (
            Text("1", font="Noto Sans KR", font_size=24)
            .next_to(pos_line, DOWN, buff=0.35)
            .set_color(BLUE_B)
        )
        self.playw(Transformr(pos_line.copy(), one))

        ## quantization 1 bit example

        nums = [2.56, -4.73, 3.12, -1.55, 0.45]

        dots = VGroup(
            *[
                Dot(
                    nump.c2p(num, 0),
                    radius=DEFAULT_DOT_RADIUS * 1.5,
                ).set_color(RED_B if num < 0 else BLUE_B)
                for num in nums
            ]
        )
        num_texts = VGroup(
            *[
                Text(
                    f"{num:.2f}: {1 if num > 0 else 0}",
                    font="Noto Sans KR",
                    font_size=18,
                )
                for num, dot in zip(nums, dots)
            ]
        )
        for nt in num_texts:
            nt[-1].set_color(RED_B if nt.get_text()[0] == "-" else BLUE_B)
        num_texts.arrange(DOWN, aligned_edge=RIGHT).next_to(
            nump.c2p(0, 0), DOWN, buff=0.75
        )

        for dot, num_text in zip(dots, num_texts):
            self.addw(dot, num_text[:-1], wait=0.5)
            self.play(Transformr(dot.copy(), num_text[-1]), run_time=0.5)
        self.wait()

        quants = VGroup(*[num_texts[i][-1] for i in range(len(num_texts))])

        self.playwl(
            AnimationGroup(
                FadeOut(VGroup(*[num_texts[i][:-1] for i in range(len(num_texts))])),
                FadeOut(dots),
            ),
            quants.animate.arrange(RIGHT, buff=0.5).next_to(
                nump.c2p(0, 0), DOWN, buff=1.2
            ),
            lag_ratio=0.5,
        )


class quant2(InteractiveScene, Scene2D):
    def construct(self):

        ## quantization 5
        nump = RaenimPlane().scale(1.4)
        nump.y_axis.set_opacity(0)

        def add_ticks(plane: NumberPlane, value, xy="x"):
            if xy == "x":
                tick = Line(plane.c2p(value, 0.1), plane.c2p(value, -0.1), color=GREY_B)
            else:
                tick = Line(plane.c2p(0.1, value), plane.c2p(-0.1, value), color=GREY_B)
            return tick

        tickm100 = add_ticks(nump, -3)
        ticktm100 = (
            Text("-100", font="Noto Sans KR", font_size=20)
            .next_to(tickm100, UP, buff=0.1)
            .set_color(GREY_B)
        )
        tick0 = add_ticks(nump, 0)
        tickt0 = (
            Text("0", font="Noto Sans KR", font_size=20)
            .next_to(tick0, UP, buff=0.1)
            .set_color(GREY_B)
        )
        tick100 = add_ticks(nump, 3)
        tickt100 = (
            Text("100", font="Noto Sans KR", font_size=20)
            .next_to(tick100, UP, buff=0.1)
            .set_color(GREY_B)
        )
        colors = [ORANGE, GREEN_B, YELLOW_B, RED_B, BLUE_B]

        self.playw(
            FadeIn(nump),
            FadeIn(tickm100),
            FadeIn(tick0),
            FadeIn(tick100),
            FadeIn(ticktm100),
            FadeIn(tickt0),
            FadeIn(tickt100),
        )

        r1 = Line(
            nump.c2p(-3, 0), nump.c2p(-5, 0), color=colors[0], stroke_width=5
        ).set_z_index(1)
        r2 = Line(
            nump.c2p(-3, 0), nump.c2p(0, 0), color=colors[1], stroke_width=5
        ).set_z_index(1)
        r3 = (
            Dot(nump.c2p(0, 0), radius=DEFAULT_DOT_RADIUS * 1.5)
            .set_color(colors[2])
            .set_z_index(2)
        )
        r4 = Line(
            nump.c2p(0, 0), nump.c2p(3, 0), color=colors[3], stroke_width=5
        ).set_z_index(1)
        r5 = Line(
            nump.c2p(3, 0), nump.c2p(5, 0), color=colors[4], stroke_width=5
        ).set_z_index(1)

        quant_ints = [-2, -1, 0, 1, 2]
        idxs = VGroup(
            *[
                Text(f"{i}", font="Noto Sans KR", font_size=24)
                .next_to(loc, DOWN, buff=0.2)
                .set_color(color)
                for i, loc, color in zip(quant_ints, [r1, r2, r3, r4, r5], colors)
            ]
        )

        for r, idx in zip([r1, r2, r3, r4, r5], idxs):
            self.playw(FadeIn(r), FadeIn(idx), wait=0.5)
        self.wait()

        self.playwl(*[FlashAround(idx) for idx in idxs], lag_ratio=0.3)

        bits_list = ["110", "111", "001", "001", "001"]
        bits = VGroup(
            *[
                Text(bits_list[i], font=MONO_FONT, font_size=20)
                .next_to(idx, DOWN, buff=0.2)
                .set_color(color)
                for i, idx, color in zip(range(len(idxs)), idxs, colors)
            ]
        )
        self.playwl(*[FadeIn(bit) for bit in bits], lag_ratio=0.3)

        nums = [-109.12, -17.24, 10, 20, 90]
        nums_pos = [-4.5, -0.7, 0.4, 0.8, 2.5]

        def get_color(num):
            if num < -100:
                return colors[0]
            elif num < 0:
                return colors[1]
            elif num == 0:
                return colors[2]
            elif num < 100:
                return colors[3]
            else:
                return colors[4]

        dots = VGroup(
            *[
                Dot(
                    nump.c2p(pos, 0),
                    radius=DEFAULT_DOT_RADIUS,
                ).set_color(get_color(num))
                for num, pos in zip(nums, nums_pos)
            ]
        )
        num_texts = VGroup(
            *[
                Text(
                    f"{num:.2f}: {bits_list[i]}",
                    font="Noto Sans KR",
                    font_size=18,
                ).set_color(get_color(num))
                for i, num in enumerate(nums)
            ]
        )
        num_texts.arrange(DOWN, aligned_edge=RIGHT).next_to(
            nump.c2p(0, 0), DOWN, buff=1.35
        )
        self.play(self.cf.animate.shift(DOWN))
        for dot, num_text in zip(dots, num_texts):
            self.addw(dot, num_text[:-3], wait=0.5)
            self.play(Transformr(dot.copy(), num_text[-3:]), run_time=0.5)
        self.wait()

        ol = self.overlay
        r4s = num_texts[-3:]
        self.add(r4s)
        r4s.set_z_index(ol.z_index + 1)
        self.playw(FadeIn(ol), run_time=0.5)

        ## fadeout ol

        self.playw(FadeOut(ol))

        ## fadeout all but x axis
        self.playw(
            FadeOut(VGroup(tickm100, ticktm100, tick0, tickt0, tick100, tickt100)),
            FadeOut(VGroup(r1, r2, r3, r4, r5)),
            FadeOut(idxs),
            FadeOut(bits),
            FadeOut(dots),
            FadeOut(num_texts),
            self.cf.animate.shift(UP),
        )
        ## custom ticks

        def get_ticks(n, start=-5, end=5):
            if isinstance(n, (int, float)):
                n = ValueTracker(n)
            return VGroup(
                *[
                    add_ticks(nump, start + (end - start) * i / n.get_value())
                    for i in range(1, int(n.get_value()) + 1)
                ]
            )

        tickposs1 = [-4.7, -3.2, 0.1, 0.5, 0.9, 2.3, 3.5]
        ticks1 = VGroup(*[add_ticks(nump, tickpos) for tickpos in tickposs1])
        range_lines1 = VGroup(
            *[
                Line(nump.c2p(start, 0), nump.c2p(end, 0), color=GREY_B)
                for start, end in zip([-5] + tickposs1, tickposs1 + [5])
            ]
        )
        self.playw(FadeIn(ticks1), FadeIn(range_lines1))

        tickposs2 = [-4.7 + 10 * i / 32 for i in range(1, 33)]
        ticks2 = VGroup(*[add_ticks(nump, tickpos) for tickpos in tickposs2])
        range_lines2 = VGroup(
            *[
                Line(nump.c2p(start, 0), nump.c2p(end, 0), color=GREY_B)
                for start, end in zip([-5] + tickposs2, tickposs2 + [5])
            ]
        )
        self.playw(Transformr(ticks1, ticks2), Transformr(range_lines1, range_lines2))

        self.playw(FadeOut(ticks2), FadeOut(range_lines2))

        ## 숫자 범위 정하기

        start_tick, end_tick = add_ticks(nump, -3.7), add_ticks(nump, 3.7)
        range_num = VGroup(
            Text("-10", font="Noto Sans KR", font_size=20)
            .next_to(start_tick, DOWN, buff=0.1)
            .set_color(GREY_B),
            Text("10", font="Noto Sans KR", font_size=20)
            .next_to(end_tick, DOWN, buff=0.1)
            .set_color(GREY_B),
        )
        self.playw(FadeIn(start_tick), FadeIn(end_tick), FadeIn(range_num))
        self.embed()
        ## N등분하기

        n = ValueTracker(8)

        n_text = (
            Text("n = 8", font="Noto Sans KR", font_size=24)
            .set_color(GREY_A)
            .shift(UP * 1.5)
        )
        n_ticks = get_ticks(n, start=-3.7, end=3.7)
        self.playw(FadeIn(n_text), FadeIn(n_ticks))

        ticks = VGroup(start_tick, *n_ticks)
        colors = color_gradient([RED, ORANGE, YELLOW_B, GREEN, BLUE_B], len(ticks) - 1)

        nlines = VGroup(
            *[
                Line(
                    ticks[i].get_right(),
                    ticks[i + 1].get_left(),
                    color=colors[i],
                    stroke_width=5,
                ).set_z_index(1)
                for i in range(len(ticks) - 1)
            ]
        )
        bits3_list = ["100", "101", "110", "111", "000", "001", "010", "011"]

        bits3 = VGroup(
            *[
                Text(bits3_list[i], font=MONO_FONT, font_size=20)
                .next_to(nlines[i], UP, buff=0.2)
                .set_color(colors[i])
                for i in range(len(nlines))
            ]
        )

        self.play(FadeIn(nlines))
        self.playw(FadeIn(bits3, shift=UP * 0.2))

        ## dot with number

        scale = 3.7 / 10

        def get_dot(num):
            boundaries = [
                -10 + 20 * i / n.get_value() for i in range(1, int(n.get_value()))
            ]
            if num < boundaries[0]:
                color = colors[0]
            elif num < boundaries[1]:
                color = colors[1]
            elif num < boundaries[2]:
                color = colors[2]
            elif num < boundaries[3]:
                color = colors[3]
            elif num < boundaries[4]:
                color = colors[4]
            elif num < boundaries[5]:
                color = colors[5]
            elif num < boundaries[6]:
                color = colors[6]
            else:
                color = colors[7]
            return Dot(nump.c2p(num * scale, 0)).set_color(color)

        def get_text(num):
            boundaries = [
                -10 + 20 * i / n.get_value() for i in range(1, int(n.get_value()))
            ]
            if num < boundaries[0]:
                color = colors[0]
                bit = bits3_list[0]
            elif num < boundaries[1]:
                color = colors[1]
                bit = bits3_list[1]
            elif num < boundaries[2]:
                color = colors[2]
                bit = bits3_list[2]
            elif num < boundaries[3]:
                color = colors[3]
                bit = bits3_list[3]
            elif num < boundaries[4]:
                color = colors[4]
                bit = bits3_list[4]
            elif num < boundaries[5]:
                color = colors[5]
                bit = bits3_list[5]
            elif num < boundaries[6]:
                color = colors[6]
                bit = bits3_list[6]
            else:
                color = colors[7]
                bit = bits3_list[7]
            t = (
                Text(f"{num:.1f}: {bit}", font="Noto Sans KR", font_size=18)
                .set_color(color)
                .next_to(nump.c2p(num * scale, 0), DOWN, buff=0.75)
            )
            a = Arrow(
                nump.c2p(num * scale, -0.8),
                nump.c2p(num * scale, -0.15),
                thickness=2,
                buff=0,
            ).set_color(color)
            return VGroup(t, a)

        v = ValueTracker(3)
        dot = get_dot(v.get_value())
        text = get_text(v.get_value())
        dot_text = VGroup(dot, text)
        self.playw(FadeIn(dot_text))

        def update_dot_text(dot_text):
            dot, text = dot_text
            num = v.get_value()
            new_dot = get_dot(num)
            new_text = get_text(num)
            dot.become(new_dot)
            text.become(new_text)

        dot_text.add_updater(update_dot_text)
        self.play(v.animate.set_value(-7.2), run_time=2)
        self.playw(v.animate.set_value(5.6), run_time=3.5, wait=2)

        self.playw(v.animate.set_value(12.5), run_time=2)

        ## disable updater and fadeout all but x axis
        dot_text.remove_updater(update_dot_text)

        self.playw(
            FadeOut(VGroup(start_tick, end_tick, range_num)),
            FadeOut(n_text),
            FadeOut(n_ticks),
            FadeOut(nlines),
            FadeOut(bits3),
            FadeOut(dot_text),
            self.cf.animate.shift(DOWN),
        )

        ## n = 16

        n = ValueTracker(16)

        ticks = get_ticks(n)

        self.playw(FadeIn(ticks), run_time=0.5)
        brace_n = Brace(nump.x_axis, UP, buff=0.4).set_color(GREY_B)

        def get_brace_text(n):
            return Text(
                f"n = {int(n.get_value())}", font="Noto Sans KR", font_size=24
            ).set_color(GREY_A)

        brace_text = get_brace_text(n).next_to(brace_n, UP, buff=0.15)
        self.playw(FadeIn(brace_n), FadeIn(brace_text), run_time=0.5)

        ## animate n change

        def update_ticks(mob):
            new_ticks = get_ticks(n)
            mob.become(new_ticks)

        def update_brace_text(mob):
            new_brace_text = get_brace_text(n).next_to(brace_n, UP, buff=0.15)
            mob.become(new_brace_text)

        ticks.add_updater(update_ticks)
        brace_text.add_updater(update_brace_text)

        self.playw(n.animate.set_value(64), run_time=2)

        def get_error_plot(n):
            mid_poss = [-5 + 10 * (i - 0.5) / n for i in range(1, int(n) + 1)]

            plot = nump.get_graph(
                lambda x: min([abs(x - mid_pos) for mid_pos in mid_poss]),
                x_range=(-5.5, 5.5, 0.01),
                color=RED_B,
            )
            return plot

        error_plot = get_error_plot(n.get_value())
        self.playw(FadeIn(error_plot), run_time=0.5)
        self.embed()

        ## animate even error plot
        def update_error_plot(mob):
            new_error_plot = get_error_plot(n.get_value())
            mob.become(new_error_plot)

        error_plot.add_updater(update_error_plot)
        self.playw(n.animate.set_value(96))

        self.playw(n.animate.set_value(16), run_time=1.5)

        ## cease updaters, show bits
        ticks.remove_updater(update_ticks)
        brace_text.remove_updater(update_brace_text)
        error_plot.remove_updater(update_error_plot)

        bits_list = [bin(i)[2:].zfill(4) for i in range(int(n.get_value()))]

        def get_center_pos(i, n):
            return nump.c2p(-5 + 10 * (i + 0.5) / n, 0)

        bits = VGroup(
            *[
                Text(bits_list[i], font=MONO_FONT, font_size=16).next_to(
                    get_center_pos(i, int(n.get_value())), DOWN
                )
                for i in range(int(n.get_value()))
            ]
        )
        self.playw(FadeIn(bits))

        ## eq 2^k
        k4 = Tex("k = 4", font_size=32).next_to(bits, DOWN, buff=0.3).set_color(GREY_A)
        self.playw(FadeIn(k4))

        eq = (
            Tex("= 2^k", font_size=36)
            .next_to(brace_text, RIGHT, buff=0.25)
            .set_color(YELLOW_B)
        )
        self.playw(FadeIn(eq))

        # k = 5, 6

        k5 = Tex("k = 5", font_size=32).move_to(k4).set_color(GREY_A)

        bits_list_5 = [bin(i)[2:].zfill(5) for i in range(32)]
        bits_5 = VGroup(
            *[
                Text(bits_list_5[i], font=MONO_FONT, font_size=12).next_to(
                    get_center_pos(i, 32), DOWN, buff=0.1 if i % 2 == 0 else 0.25
                )
                for i in range(32)
            ]
        )
        k4.become(k5)
        bits.become(bits_5)
        ticks.become(get_ticks(ValueTracker(32)))
        brace_text.become(
            get_brace_text(ValueTracker(32)).next_to(brace_n, UP, buff=0.15)
        )
        error_plot.become(get_error_plot(32))
        self.wait(1.5)

        k6 = Tex("k = 6", font_size=32).move_to(k4).set_color(GREY_A)
        bits_list_6 = [bin(i)[2:].zfill(6) for i in range(64)]
        bits_6 = VGroup(
            *[
                Text(bits_list_6[i], font=MONO_FONT, font_size=6).next_to(
                    get_center_pos(i, 64), DOWN, buff=0.1 if i % 2 == 0 else 0.2
                )
                for i in range(64)
            ]
        )
        k4.become(k6)
        bits.become(bits_6)
        ticks.become(get_ticks(ValueTracker(64)))
        brace_text.become(
            get_brace_text(ValueTracker(64)).next_to(brace_n, UP, buff=0.15)
        )
        error_plot.become(get_error_plot(64))
        self.wait(0.5)
        self.playw(self.cf.animate.scale(0.4))


class quantize_range(InteractiveScene, Scene2D):
    def construct(self):
        ## initialize
        nump = RaenimPlane().scale(1.4)
        nump.y_axis.set_opacity(0)

        def add_ticks(plane: NumberPlane, value, xy="x"):
            if xy == "x":
                tick = Line(plane.c2p(value, 0.1), plane.c2p(value, -0.1), color=GREY_B)
            else:
                tick = Line(plane.c2p(0.1, value), plane.c2p(-0.1, value), color=GREY_B)
            return tick

        def get_k_bits(k):
            tk = Tex(f"k = {k}", font_size=32).set_color(GREY_A)

            n = 2**k
            tn = Tex("n =\\,", f"2^{k} =\\,", f"{n}", font_size=32).set_color(GREY_A)

            tg = VGroup(tk, tn).arrange(RIGHT, buff=0.5)

            return tg

        k0 = 8
        tg = get_k_bits(k0).shift(UP * 1.5)
        self.playw(FadeIn(nump))

        self.playw(FadeIn(tg[0]))
        self.playwl(
            FadeIn(tg[1][:2]),
            AnimationGroup(
                FadeIn(tg[1][2]),
                FadeIn(tg[1][4]),
                Transformr(tg[0][-1].copy(), tg[1][3]),
            ),
            FadeIn(tg[1][5:]),
            lag_ratio=0.8,
        )

        ## add tick and number for range +-32
        start_num, end_num = -4.2, 4.2
        start_tick, end_tick = add_ticks(nump, start_num), add_ticks(nump, end_num)

        range_start_num, range_end_num = -32, 32

        def get_range_start(num):
            return (
                Text(str(int(num)), font="Noto Sans KR", font_size=20)
                .set_color(GREY_B)
                .next_to(start_tick, DOWN, buff=0.1)
            )

        def get_range_end(num):
            return (
                Text(str(int(num)), font="Noto Sans KR", font_size=20)
                .set_color(GREY_B)
                .next_to(end_tick, DOWN, buff=0.1)
            )

        range_start, range_end = get_range_start(range_start_num), get_range_end(
            range_end_num
        )

        self.playw(
            FadeIn(start_tick), FadeIn(end_tick), FadeIn(range_start), FadeIn(range_end)
        )

        ## add quantization ticks
        n = 2**k0
        quant_ticks = VGroup(
            *[
                add_ticks(nump, start_num + (end_num - start_num) * i / n)
                for i in range(1, n)
            ]
        )
        self.playw(FadeIn(quant_ticks))

        ## magnify and show step size
        all_things = VGroup(
            tg, start_tick, end_tick, range_start, range_end, quant_ticks, nump
        )
        all_things.save_state()
        self.playw(all_things.animate.scale(10), run_time=1.5)

        brace = Brace(
            VGroup(
                quant_ticks[len(quant_ticks) // 2 - 1],
                quant_ticks[len(quant_ticks) // 2],
            ),
            UP,
            buff=0.05,
        ).set_color(GREY_B)
        step_size = (range_end_num - range_start_num) / n
        step_text = (
            Text(f"{step_size:.2f}", font="Noto Sans KR", font_size=18)
            .next_to(brace, UP, buff=0.1)
            .set_color(GREY_B)
        )
        self.playw(FadeIn(brace), FadeIn(step_text))

        self.play(FadeOut(brace), FadeOut(step_text))
        self.playw(Restore(all_things), run_time=1.5)

        ## shrink to +- 1
        start_num = ValueTracker(start_num)
        end_num = ValueTracker(end_num)
        range_start_num = ValueTracker(range_start_num)
        range_end_num = ValueTracker(range_end_num)
        start_tick.add_updater(
            start_tick_updater:=lambda mob: mob.become(add_ticks(nump, start_num.get_value()))
        )
        end_tick.add_updater(
            end_tick_updater:=lambda mob: mob.become(add_ticks(nump, end_num.get_value()))
        )
        range_start.add_updater(
            range_start_updater:=lambda mob: mob.become(get_range_start(range_start_num.get_value()))
        )
        range_end.add_updater(
            range_end_updater:=lambda mob: mob.become(get_range_end(range_end_num.get_value()))
        )
        quant_ticks.add_updater(
            quant_ticks_updater:=lambda mob: mob.become(
                VGroup(
                    *[
                        add_ticks(
                            nump,
                            start_num.get_value()
                            + (end_num.get_value() - start_num.get_value()) * i / n,
                        )
                        for i in range(1, n)
                    ]
                )
            )
        )
        self.playw(
            nump.x_axis.animate.scale(3),
            start_num.animate.set_value(-1.5),
            end_num.animate.set_value(1.5),
            range_start_num.animate.set_value(-1),
            range_end_num.animate.set_value(1),
            run_time=1.5,
        )
        self.embed()

        ## remove updaters
        start_tick.remove_updater(start_tick_updater)
        end_tick.remove_updater(end_tick_updater)
        range_start.remove_updater(range_start_updater)
        range_end.remove_updater(range_end_updater)
        quant_ticks.remove_updater(quant_ticks_updater)

        all_things = VGroup(
            tg, start_tick, end_tick, range_start, range_end, quant_ticks, nump
        )
        all_things.save_state()
        self.playw(all_things.animate.scale(10), run_time=1.5)

        brace = Brace(
            VGroup(
                quant_ticks[len(quant_ticks) // 2 - 1],
                quant_ticks[len(quant_ticks) // 2],
            ),
            UP,
            buff=0.05,
        ).set_color(GREY_B)
        step_size = (range_end_num.get_value() - range_start_num.get_value()) / n
        step_text = (
            Text(f"{step_size:.3f}", font="Noto Sans KR", font_size=18)
            .next_to(brace, UP, buff=0.1)
            .set_color(GREY_B)
        )
        self.playw(FadeIn(brace), FadeIn(step_text))

        self.play(FadeOut(brace), FadeOut(step_text))
        self.playw(Restore(all_things), run_time=1.5)

