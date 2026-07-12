from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)

class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        vertical_line = DashedLine(
            UP * 5, DOWN * 5, stroke_width=1, stroke_color=GREY_D
        )
        self.addw(vertical_line)

        LO = LEFT * 7.11111111 / 2
        RO = RIGHT * 7.11111111 / 2

        int32 = Text("int32", font_size=36, font=MONO_FONT).move_to(LO).shift(UP * 2)
        self.playw(FadeIn(int32))

        def get_32bits(num: int | float) -> str:
            num = int(num)
            return np.binary_repr(num & 0xFFFFFFFF, width=32)

        def join_every8(bits: str, joiner=" "):
            return joiner.join([bits[i : i + 8] for i in range(0, 32, 8)])

        def int2bit(num: int, orig=LO) -> Words:
            bits = join_every8(get_32bits(num))  # "byte byte byte byte"
            return Words(bits, font_size=24, font=MONO_FONT).move_to(orig + DOWN * 0.5)

        val = ValueTracker(0)
        bits = int2bit(val.get_value())

        def get_numText():
            t = Text(
                f"Value: {int(val.get_value()):,}", font_size=28, font=MONO_FONT
            ).next_to(bits, UP, buff=0.75)
            t[6:].set_color(YELLOW_B)
            return t

        num = get_numText()
        self.playw(FadeIn(bits), FadeIn(num))

        bit_fn = lambda m: m.become(int2bit(val.get_value()))
        bits.add_updater(bit_fn)
        num_fn = lambda m: m.become(get_numText())
        num.add_updater(num_fn)

        self.playw(val.animate.set_value(2147483647), run_time=5, wait=2)

        bit_brace = Brace(bits[1:], DOWN, buff=0.1).set_color(GREY_B)
        brace_text = (
            Tex("2^{31}-1", font_size=32)
            .set_color(YELLOW_B)
            .next_to(bit_brace, DOWN, buff=0.1)
        )
        self.playw(FadeIn(bit_brace), FadeIn(brace_text), wait=2)
        eq = (
            Text("=", font_size=28)
            .set_color(YELLOW_B)
            .next_to(brace_text, RIGHT, buff=0.1)
        )
        numc = num[6:].copy()
        self.playw(FadeIn(eq), numc.animate.next_to(eq, RIGHT, buff=0.1), wait=2)
        self.playw(FadeOut(VGroup(brace_text, bit_brace, eq, numc)))
        ## minus

        self.playw(val.animate.set_value(-1), run_time=3, wait=2)
        self.playw(val.animate.set_value(-2147483648), run_time=3)

        ## explain

        tex1 = (
            Tex("\\text{int32}: -2^{31} \sim 2^{31}-1", font_size=36)
            .move_to(LO + DOWN * 1.5)
            .set_color(YELLOW_B)
        )
        self.playw(FadeIn(tex1))

        ## right: float32
        float32 = (
            Text("float32", font_size=36, font=MONO_FONT).move_to(RO).shift(UP * 2)
        )
        self.playw(FadeIn(float32))

        def bit_to_float(bits: str):
            sign = bits[0]
            exponent = bits[1:9]
            mantissa = bits[9:]
            s = -1 if sign == "1" else 1
            e = int(exponent, 2)
            m = int(mantissa, 2)
            return s * (1 + m) * 2 ** (e - 127)

        def int_to_bits(num: int) -> str:
            bits = get_32bits(num)
            return bits

        val2 = ValueTracker(0)
        bits2 = int2bit(val2.get_value(), orig=RO)

        num2_val = bit_to_float(int_to_bits(val2.get_value()))

        def get_numText2(num):
            t = Text(f"Value: {num:,}", font_size=28, font=MONO_FONT).next_to(
                bits2, UP, buff=0.75
            )
            t[6:].set_color(YELLOW_B)
            return t

        num2 = get_numText2(num2_val)
        self.playw(FadeIn(bits2), FadeIn(num2))

        ## val2 to 2147483647
        fbit_fn = lambda m: m.become(int2bit(val2.get_value(), orig=RO))
        bits2.add_updater(fbit_fn)
        fnum_fn = lambda m: m.become(
            get_numText2(bit_to_float(int_to_bits(val2.get_value())))
        )
        num2.add_updater(fnum_fn)

        self.playw(val2.animate.set_value(2147483647), run_time=5, wait=2)

        ## up num

        bits2.remove_updater(fbit_fn)
        num2.remove_updater(fnum_fn)
        ol = self.overlay
        self.add(num2.set_z_index(ol.z_index + 1))
        self.playw(
            self.cf.animate.move_to(num2).shift(UP * 0.5),
            num2.animate.shift(UP * 0.5),
            FadeIn(ol),
        )


class integer(InteractiveScene, Scene2D):
    def construct(self):

        ## 1 byte: 8 bits
        def int_to_bits(num: int) -> str:
            num = int(num)
            return np.binary_repr(num & 0xFFFFFFFF, width=8)

        bit0_string = int_to_bits(0)
        bit0 = Text(bit0_string, font_size=32, font=MONO_FONT).arrange(RIGHT, buff=0.1)
        self.playw(FadeIn(bit0))

        brace = Brace(bit0, DOWN, buff=0.1).set_color(GREY_B)
        brace_t = (
            Tex("\\text{8 bits} \\xrightarrow{}  2^8 = 256", font_size=32)
            .set_color(YELLOW_B)
            .next_to(brace, DOWN, buff=0.1)
            .shift(RIGHT)
        )
        brace_t[-3:].set_color(YELLOW).set_opacity(0)

        self.playw(FadeIn(brace), FadeIn(brace_t))
        self.playw(brace_t[-3:].animate.set_opacity(1))

        ## = num
        eqnum = lambda num: Text(
            f"= {int(num):,}", font_size=32, font=MONO_FONT
        ).next_to(bit0, RIGHT, buff=0.3)
        val = ValueTracker(0)
        get_bit0 = lambda: Text(
            int_to_bits(val.get_value()), font_size=32, font=MONO_FONT
        ).arrange(RIGHT, buff=0.1)
        bit0.add_updater(lambda m: m.become(get_bit0()))
        num = eqnum(val.get_value())
        self.playw(FadeIn(num))
        num.add_updater(lambda m: m.become(eqnum(val.get_value())))
        self.playw(val.animate.set_value(255), run_time=5, wait=2)

        self.playw(val.animate.set_value(0), run_time=2.5, wait=2)

        ## int_to_bits_sign
        def int_to_bits_sign(num: int) -> str:
            num = int(num)
            return np.binary_repr(num & 0xFF, width=8)

        bit1_string = int_to_bits_sign(0)
        bit1 = Text(bit1_string, font_size=32, font=MONO_FONT).arrange(RIGHT, buff=0.1)
        bit0.suspend_updating()
        self.remove(bit0)
        self.add(bit1)
        num1 = eqnum(0)
        num.suspend_updating()
        self.remove(num)
        self.add(num1)

        val = ValueTracker(0)
        get_bit1 = lambda: Text(
            int_to_bits_sign(val.get_value()), font_size=32, font=MONO_FONT
        ).arrange(RIGHT, buff=0.1)
        bit1.add_updater(lambda m: m.become(get_bit1()))
        num1.add_updater(lambda m: m.become(eqnum(val.get_value())))

        self.playw(val.animate.set_value(127), run_time=2.5, wait=2)
        self.playw(val.animate.set_value(-128), run_time=2.5, wait=2)
        self.playw(val.animate.set_value(-1), run_time=2.5, wait=2)

        ## 16 bits
        def int_to_bits_sign16(num: int) -> str:
            num = int(num)
            return np.binary_repr(num & 0xFFFF, width=16)

        bits2_string = int_to_bits_sign16(0)
        bits2_string = bits2_string[:8] + " " + bits2_string[8:]
        bits2 = Words(bits2_string, font_size=32, font=MONO_FONT).arrange(
            RIGHT, buff=0.1
        )
        bits2.words.arrange(RIGHT, buff=0.3).align_to(bit1, RIGHT)
        bit1.suspend_updating()
        brace2 = Brace(bits2, DOWN, buff=0.1).set_color(GREY_B)
        brace_t2 = (
            Tex("\\text{16 bits} \\xrightarrow{}  2^{16} = 65536", font_size=32)
            .next_to(brace2, DOWN, buff=0.1)
            .set_color(YELLOW_B)
            .shift(RIGHT)
        )
        brace_t2[-5:].set_color(YELLOW)
        bit1c = bit1.copy()
        self.playwl(
            AnimationGroup(
                Transformr(bit1, bits2[:8]),
                Transform(brace, brace2),
                FadeTransform(brace_t, brace_t2),
            ),
            AnimationGroup(
                *[FadeIn(bits2[i]) for i in reversed(range(8, 16))], lag_ratio=0.1
            ),
            lag_ratio=0.5,
        )

        ## 16bits animation 32,767
        val = ValueTracker(0)

        def get_bits2(num):
            bits2_string = int_to_bits_sign16(num)
            bits2_string = bits2_string[:8] + " " + bits2_string[8:]
            words = Words(bits2_string, font_size=32, font=MONO_FONT).arrange(
                RIGHT, buff=0.1
            )
            words.words.arrange(RIGHT, buff=0.3).align_to(bit1c, RIGHT)
            return words

        def get_num2(num):
            return Text(f"= {int(num):,}", font_size=32, font=MONO_FONT).next_to(
                bits2, RIGHT, buff=0.3
            )

        num2 = get_num2(val.get_value())
        self.add(num2)
        self.remove(num1)
        self.add(bits2)
        bits2.add_updater(lambda m: m.become(get_bits2(val.get_value())))
        num2.add_updater(lambda m: m.become(get_num2(val.get_value())))
        self.playw(val.animate.set_value(32767), run_time=3, wait=2)
        self.playw(val.animate.set_value(-1), run_time=2.5, wait=2)
        self.playw(val.animate.set_value(-32768), run_time=2.5, wait=2)

        ## 32 bits
        def int_to_bits_sign32(num: int) -> str:
            num = int(num)
            return np.binary_repr(num & 0xFFFFFFFF, width=32)

        bits4_string = int_to_bits_sign32(0)
        bits4_string = (
            bits4_string[:8]
            + " "
            + bits4_string[8:16]
            + " "
            + bits4_string[16:24]
            + " "
            + bits4_string[24:]
        )
        bits4 = Words(bits4_string, font_size=32, font=MONO_FONT).arrange(
            RIGHT, buff=0.1
        )

        def get_num3(num):
            return Text(f"= {int(num):,}", font_size=32, font=MONO_FONT).next_to(
                bits4, RIGHT, buff=0.3
            )

        bits4.words.arrange(RIGHT, buff=0.3).align_to(bits2, RIGHT)
        brace4 = Brace(bits4, DOWN, buff=0.1).set_color(GREY_B)
        brace_t4 = (
            Tex("\\text{32 bits} \\xrightarrow{}  2^{32} = 4,294,967,296", font_size=32)
            .next_to(brace4, DOWN, buff=0.1)
            .set_color(YELLOW_B)
            .shift(RIGHT)
        )
        brace_t4[-13:].set_color(YELLOW)
        bits2.suspend_updating()
        num2.suspend_updating()
        num3 = get_num3(0)
        self.playwl(
            AnimationGroup(
                Transformr(bits2, bits4[:16]),
                Transform(brace, brace4),
                FadeTransform(brace_t2, brace_t4),
            ),
            self.cf.animate.shift(LEFT * 2.1),
            Transformr(num2, num3),
            AnimationGroup(
                *[FadeIn(bits4[i]) for i in reversed(range(16, 32))], lag_ratio=0.05
            ),
            lag_ratio=0.1,
        )

        ## 32bits animation 2,147,483,647
        val = ValueTracker(0)
        bits4c = bits4.copy()

        def get_bits4(num):
            bits4_string = int_to_bits_sign32(num)
            bits4_string = (
                bits4_string[:8]
                + " "
                + bits4_string[8:16]
                + " "
                + bits4_string[16:24]
                + " "
                + bits4_string[24:]
            )
            words = Words(bits4_string, font_size=32, font=MONO_FONT).arrange(
                RIGHT, buff=0.1
            )
            words.words.arrange(RIGHT, buff=0.3).align_to(bits4c, RIGHT)
            return words

        self.add(bits4)
        bits4.add_updater(lambda m: m.become(get_bits4(val.get_value())))
        num3.add_updater(lambda m: m.become(get_num3(val.get_value())))

        self.playw(val.animate.set_value(2147483647), run_time=3, wait=2)
        self.playw(val.animate.set_value(-2147483648), run_time=6, wait=2)

        ## reset to 8 bits
        def get_bits0(num):
            bits0_string = int_to_bits_sign(num)
            words = Words(bits0_string, font_size=32, font=MONO_FONT).arrange(
                RIGHT, buff=0.1
            )
            return words

        def get_num0(num):
            return Text(f"= {int(num):,}", font_size=32, font=MONO_FONT).next_to(
                bit0, RIGHT, buff=0.3
            )

        bits0 = get_bits0(0)
        num0 = get_num0(0)
        brace0 = Brace(bit0, DOWN, buff=0.1).set_color(GREY_B)
        brace_t0 = (
            Tex("\\text{8 bits} \\xrightarrow{}  2^8 = 256", font_size=32)
            .set_color(YELLOW_B)
            .next_to(brace0, DOWN, buff=0.1)
            .shift(RIGHT)
        )
        bits4.suspend_updating()
        num3.suspend_updating()
        self.playwl(
            Transformr(bits4[-8:], bits0),
            Transformr(num3, num0),
            Transform(brace, brace0),
            FadeTransform(brace_t4, brace_t0),
            FadeOut(bits4[:24]),
            self.cf.animate.shift(RIGHT * 2.1),
            wait=2,
        )
        ## slowly change to 10

        val = ValueTracker(0)
        bits0.add_updater(lambda m: m.become(get_bits0(val.get_value())))
        num0.add_updater(lambda m: m.become(get_num0(val.get_value())))

        for i in range(1, 11):
            self.addw(val.set_value(i))
        self.wait(2)


class floatFault(InteractiveScene, Scene2D):
    def construct(self):

        ## numl

        numl = NumberLine(x_range=(-3, 3, 1), tick_size=0.05).scale(2)
        numl.ticks[0].set_opacity(0)
        numl.ticks[-1].set_opacity(0)

        self.playw(FadeIn(numl))

        nums = [-2, -1, 0, 1, 2]
        tick_nums = VGroup(
            *[
                Text(str(num), font_size=24, font=MONO_FONT).next_to(
                    numl.n2p(num), DOWN
                )
                for num in nums
            ]
        )
        dots = VGroup(
            *[
                Text("...", font_size=24, font=MONO_FONT).next_to(numl.n2p(num), DOWN)
                for num in [-3, 3]
            ]
        )
        self.playw(FadeIn(tick_nums), FadeIn(dots))

        ## infinite ticks between 0 and 1
        get_tick = lambda: numl.ticks[1].copy()
        linspace01 = np.linspace(0, 1, 32)
        ticks01 = VGroup(*[get_tick().move_to(numl.n2p(num)) for num in linspace01])

        self.play(FadeIn(ticks01))
        self.cf.save_state()
        self.playw(self.cf.animate.move_to(numl.n2p(0.5)).scale(0.3), wait=2)

        linespace01_new = np.linspace(0, 1, 64)
        ticks01_new = VGroup(
            *[get_tick().move_to(numl.n2p(num)) for num in linespace01_new]
        )
        self.playw(Transform(ticks01, ticks01_new))

        ## restore self cf and fadeout ticks01

        self.playw(self.cf.animate.restore(), FadeOut(ticks01), wait=2)

        ## current numl and ticks shift up

        numls = VGroup(numl, tick_nums, dots)

        self.play(numls.animate.shift(UP * 2))

        ## new numl for whole ranges

        numl2 = NumberLine(
            x_range=(-17, 17, 1), tick_size=0.1, width=numl.get_width()
        ).shift(DOWN * 0.5)
        numl2.ticks[0].set_opacity(0)
        numl2.ticks[-1].set_opacity(0)
        numl2.ticks[2:-2].set_opacity(0)
        max_num = 2147483647
        min_num = -2147483648
        tick_max = Text(f"{max_num:,}", font_size=20, font=MONO_FONT).next_to(
            numl2.n2p(16), DOWN
        )
        tick_min = Text(f"{min_num:,}", font_size=20, font=MONO_FONT).next_to(
            numl2.n2p(-16), DOWN
        )
        tickm2 = get_tick().move_to(numl2.n2p(-0.1))
        tickp2 = get_tick().move_to(numl2.n2p(0.1))
        dlinem = DashedLine(
            tickm2.get_top(), numl.n2p(-2.8), color=GREY_D, stroke_width=3
        )
        dlinep = DashedLine(
            tickp2.get_top(), numl.n2p(2.8), color=GREY_D, stroke_width=3
        )
        self.playw(
            FadeIn(numl2),
            FadeIn(tick_max),
            FadeIn(tick_min),
            FadeIn(tickm2),
            FadeIn(tickp2),
            FadeIn(dlinem),
            FadeIn(dlinep),
            wait=2,
        )

        ## x * 32

        text_x32 = (
            Words("xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx", font_size=32, font=MONO_FONT)
            .set_color(YELLOW_E)
            .shift(DOWN * 1.75)
        )
        self.playw(FadeIn(text_x32), wait=2)

        ## one bit right to point

        new_text_x32 = (
            Words("xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxx.x", font_size=32, font=MONO_FONT)
            .set_color(YELLOW_E)
            .shift(DOWN * 1.75)
        )
        max_num_new = max_num // 2
        min_num_new = min_num // 2
        tick_max_new = Text(f"{max_num_new:,}", font_size=20, font=MONO_FONT).next_to(
            numl2.n2p(8), DOWN
        )
        tick_min_new = Text(f"{min_num_new:,}", font_size=20, font=MONO_FONT).next_to(
            numl2.n2p(-8), DOWN
        )
        new_tick_nums_list = [-2.5, -1.5, -0.5, 0.5, 1.5, 2.5]
        new_ticks = VGroup(get_tick().move_to(numl.n2p(i)) for i in new_tick_nums_list)
        new_tick_nums1 = VGroup(
            *[
                Text(str(num), font_size=18, font=MONO_FONT).next_to(
                    numl.n2p(num), DOWN
                )
                for num in new_tick_nums_list
            ]
        )
        self.playw(
            *[Transform(text_x32.words[i], new_text_x32.words[i]) for i in range(4)],
            Transform(tick_max, tick_max_new),
            Transform(tick_min, tick_min_new),
            numl2.ticks[1].animate.move_to(numl2.n2p(-8)),
            numl2.ticks[-2].animate.move_to(numl2.n2p(8)),
            FadeIn(new_ticks),
            FadeIn(new_tick_nums1),
            wait=2,
        )

        ## once more

        new_text_x32 = (
            Words("xxxxxxxx xxxxxxxx xxxxxxxx xxxxxx.xx", font_size=32, font=MONO_FONT)
            .set_color(YELLOW_E)
            .shift(DOWN * 1.75)
        )
        max_num_new2 = max_num_new // 2
        min_num_new2 = min_num_new // 2
        tick_max_new = Text(f"{max_num_new2:,}", font_size=20, font=MONO_FONT).next_to(
            numl2.n2p(4), DOWN
        )
        tick_min_new = Text(f"{min_num_new2:,}", font_size=20, font=MONO_FONT).next_to(
            numl2.n2p(-4), DOWN
        )
        new_ticks = VGroup(
            get_tick().move_to(numl.n2p(i))
            for i in [-2.25, -1.75, -1.25, -0.75, -0.25, 0.25, 0.75, 1.25, 1.75, 2.25]
        )
        new_tick_nums_list2 = [
            -2.25,
            -1.75,
            -1.25,
            -0.75,
            -0.25,
            0.25,
            0.75,
            1.25,
            1.75,
            2.25,
        ]
        new_tick_nums2 = VGroup(
            *[
                Text(str(num), font_size=16, font=MONO_FONT).next_to(
                    numl.n2p(num), DOWN
                )
                for num in new_tick_nums_list2
            ]
        )
        self.playw(
            *[Transform(text_x32.words[i], new_text_x32.words[i]) for i in range(4)],
            Transform(tick_max, tick_max_new),
            Transform(tick_min, tick_min_new),
            numl2.ticks[1].animate.move_to(numl2.n2p(-4)),
            numl2.ticks[-2].animate.move_to(numl2.n2p(4)),
            FadeIn(new_ticks),
            FadeIn(new_tick_nums2),
            wait=2,
        )

        ## once more: 3 bits right to point

        new_text_x32 = (
            Words("xxxxxxxx xxxxxxxx xxxxxxxx xxxxx.xxx", font_size=32, font=MONO_FONT)
            .set_color(YELLOW_E)
            .shift(DOWN * 1.75)
        )

        max_num_new = max_num_new // 2
        min_num_new = min_num_new // 2

        tick_max_new = Text(f"{max_num_new:,}", font_size=20, font=MONO_FONT).next_to(
            numl2.n2p(2), DOWN
        )
        tick_min_new = Text(f"{min_num_new:,}", font_size=20, font=MONO_FONT).next_to(
            numl2.n2p(-2), DOWN
        )
        new_tick_nums_list3 = [
            -2.375,
            -2.125,
            -1.875,
            -1.625,
            -1.375,
            -1.125,
            -0.875,
            -0.625,
            -0.375,
            -0.125,
            0.125,
            0.375,
            0.625,
            0.875,
            1.125,
            1.375,
            1.625,
            1.875,
            2.125,
            2.375,
        ]
        new_ticks = VGroup(get_tick().move_to(numl.n2p(i)) for i in new_tick_nums_list3)
        new_tick_nums3 = VGroup(
            *[
                Text(str(num), font_size=10, font=MONO_FONT).next_to(
                    numl.n2p(num), UP, buff=0.2
                )
                for i, num in enumerate(new_tick_nums_list3)
            ]
        )
        self.playw(
            *[Transform(text_x32.words[i], new_text_x32.words[i]) for i in range(4)],
            Transform(tick_max, tick_max_new),
            Transform(tick_min, tick_min_new),
            numl2.ticks[1].animate.move_to(numl2.n2p(-2)),
            numl2.ticks[-2].animate.move_to(numl2.n2p(2)),
            FadeIn(new_ticks),
            FadeIn(new_tick_nums3),
            wait=2,
        )


class floatFault8bit(InteractiveScene, Scene2D):
    def construct(self):

        ## 8 bits after point
        text_x32 = Words(
            "xxxxxxxx xxxxxxxx xxxxxxxx .xxxxxxxx", font_size=32, font=MONO_FONT
        ).set_color(YELLOW_E)

        self.playw(FadeIn(text_x32), wait=2)

        ## numl, one tick is 1/256
        numl = NumberLine(x_range=(-3, 3, 1 / 8), tick_size=0.05).scale(2).shift(DOWN)
        numl.ticks[0].set_opacity(0)
        numl.ticks[-1].set_opacity(0)
        numl.ticks[2:-2].set_opacity(0)
        numl.ticks[len(numl.ticks) // 2 : len(numl.ticks) // 2 + 2].set_opacity(1)

        max_tick = Tex("2^{23}", font_size=28).next_to(numl.n2p(3), DOWN, buff=0.25)
        min_tick = Tex("-2^{23}", font_size=28).next_to(numl.n2p(-3), DOWN, buff=0.25)
        self.playw(FadeIn(numl), FadeIn(max_tick), FadeIn(min_tick), wait=2)

        self.play(FlashAround(text_x32.words[:-1]))
        self.play(FlashAround(min_tick))
        self.playw(FlashAround(max_tick))

        ## range = 1/256
        get_par = (
            lambda x, direction, buff: Text("(", font_size=24)
            .rotate(PI / 2)
            .stretch_to_fit_width(x.get_width())
            .next_to(x, direction, buff=buff)
        )
        par = get_par(
            numl.ticks[len(numl.ticks) // 2 : len(numl.ticks) // 2 + 2], DOWN, 0.1
        ).set_color(YELLOW_B)
        range_text = (
            Tex("2^{-8} = \\frac{1}{256} = 0.00390625", font_size=32)
            .next_to(par, DOWN, buff=0.0)
            .set_color(YELLOW_B)
        ).shift(RIGHT * 1.5)
        self.playw(FadeIn(par), FadeIn(range_text), wait=2)

        ## fadeout range_text and par
        self.playw(FadeOut(par), FadeOut(range_text))

        code = Words("x = 0.1", font_size=28, font=MONO_FONT).next_to(
            numl, DOWN, buff=0.5
        )
        self.playwl(*[FadeIn(w) for w in code.words], lag_ratio=0.4)

        dot01 = Dot(numl.n2p(0.075), radius=0.04).set_color(YELLOW_B)
        self.play(FadeIn(dot01))
        self.cf.save_state()
        self.playw(self.cf.animate.move_to(dot01).scale(0.5), wait=2)

        ## camera

        self.play(
            self.cf.animate.reorient(
                -23,
                59,
                0,
                (np.float32(-0.04), np.float32(-1.19), np.float32(0.05)),
                1.09,
            ),
            code.animate.set_opacity(0.3),
        )
        tickm = numl.ticks[len(numl.ticks) // 2]
        tickp = numl.ticks[len(numl.ticks) // 2 + 1]
        minus_diff = Line(
            tickm.get_center(), dot01.get_center(), color=PURE_RED, stroke_width=12
        )
        plus_diff = Line(
            tickp.get_center(), dot01.get_center(), color=PURE_RED, stroke_width=12
        )
        tickm_text = (
            Text(f"0.09765625", font_size=6, font=MONO_FONT)
            .next_to(tickm, UP, buff=0.02, aligned_edge=RIGHT)
            .rotate(59 * DEGREES, axis=RIGHT)
        )
        m_error = (
            Text(f"error = 0.00234375", font_size=6, font=MONO_FONT)
            .next_to(minus_diff, DOWN, buff=0.1)
            .set_color(PURE_RED)
            .rotate(59 * DEGREES, axis=RIGHT)
        )
        tickp_text = (
            Text(f"0.1015625", font_size=6, font=MONO_FONT)
            .next_to(tickp, UP, buff=0.02, aligned_edge=LEFT)
            .rotate(59 * DEGREES, axis=RIGHT)
        )
        p_error = (
            Text(f"error = 0.0015625", font_size=6, font=MONO_FONT)
            .next_to(plus_diff, DOWN, buff=0.1)
            .set_color(PURE_RED)
            .rotate(59 * DEGREES, axis=RIGHT)
        )
        self.playw(FadeIn(minus_diff), FadeIn(tickm_text))
        self.playw(Transformr(minus_diff, m_error))

        self.play(FadeOut(m_error), FadeOut(tickm_text))
        self.play(FadeIn(plus_diff), FadeIn(tickp_text))
        self.playw(Transformr(plus_diff, p_error))


class actualFloat(InteractiveScene, Scene2D):
    def construct(self):
        ## 32 bits float
        text_x32 = Words(
            "xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx", font_size=32, font=MONO_FONT
        )

        i0 = 0
        im = slice(1, 24)  # mantissa
        ie = slice(24, 32)  # exponent

        text_x32[i0].set_color(RED_C)
        text_x32[im].set_color(GREEN)
        text_x32[ie].set_color(BLUE_B)

        self.playw(FadeIn(text_x32), wait=2)

        ## unwrap the float32 into sign, exponent, mantissa
        t0 = text_x32[i0]
        tm = text_x32[im]
        te = text_x32[ie]

        t0.generate_target()
        tm.generate_target()
        te.generate_target()

        VGroup(t0.target, tm.target.arrange(RIGHT, buff=0.05), te.target).arrange(
            RIGHT, buff=0.75
        )

        self.play(MoveToTarget(t0), MoveToTarget(tm), MoveToTarget(te))

        # onedot, 2x, pm
        pm = Tex("\\pm", font_size=32).move_to(t0).set_color(RED_C)
        onedot = Tex("1.", font_size=32).next_to(tm, LEFT, buff=0.1)
        double = Tex("\\times 2^1", font_size=32).next_to(tm, RIGHT, buff=0.1)
        double[-1].set_opacity(0)
        self.playw(
            FadeIn(onedot),
            FadeIn(double),
            te.animate.align(double[-1], DL, buff=0.01),
            Transformr(t0, pm),
        )

        text_bin = (
            Text("Binary", font_size=28).next_to(pm, LEFT, buff=0.5).set_color(GREY_A)
        )

        ## in decimal

        text_decimal = Tex("1972.1121 = + 1.9721121 \\times 10^3", font_size=32).shift(
            UP
        )
        text_decimal[10].set_color(RED_C)
        text_decimal[11:20].set_color(GREEN)
        text_decimal[-1].set_color(BLUE_B)
        self.playw(FadeIn(text_decimal))

        text_dec = (
            Text("Decimal", font_size=28)
            .next_to(text_decimal, LEFT, buff=0.5)
            .set_color(GREY_A)
        )

        self.playw(FadeIn(text_bin), FadeIn(text_dec), wait=2)

        ## fadeout bins

        bins = VGroup(pm, t0, tm, te, onedot, double, text_bin)
        self.playw(FadeOut(bins), self.cf.animate.shift(UP))

        ## num = (sign) * x * 10^y in decimal

        def get_decimal(sign: int, x: float, y: int):
            sign = "+" if sign == 0 else "-"
            num_float = sign + str(x * 10**y)
            num_float9 = str(num_float)[1:10] if sign == "+" else str(num_float)[:10]
            string = f"{num_float9} = {sign} {x:.7f} \\times 10^{y}"
            tex = Tex(string, font_size=32)
            tex[len(num_float9) + 1 : len(num_float9) + 2].set_color(RED_C)
            tex[len(num_float9) + 2 : len(num_float9) + 11].set_color(GREEN)
            tex[-1].set_color(BLUE_B)
            return tex.shift(UP)

        x_val = ValueTracker(1.9721121)
        text_decimal.add_updater(
            lambda m: m.become(get_decimal(0, x_val.get_value(), 3))
        )

        numl = NumberLine(x_range=(0, 11, 1), tick_size=0.075, width=13)
        numl.ticks[0].set_opacity(0)
        numl.ticks[-1].set_opacity(0)
        tick0 = Text("0", font_size=20, font=MONO_FONT).next_to(numl.n2p(0), DOWN)
        tick1 = Text("1", font_size=20, font=MONO_FONT).next_to(numl.n2p(1), DOWN)
        tick10 = Text("10", font_size=20, font=MONO_FONT).next_to(numl.n2p(10), DOWN)
        dot1 = (
            Dot(numl.n2p(1), radius=0.1).set_fill(GREEN, opacity=1).set_stroke(width=0)
        )
        dot10 = (
            Dot(numl.n2p(10), radius=0.1)
            .set_fill(GREEN, opacity=0)
            .set_stroke(color=GREEN, width=4)
        )
        line110 = Line(
            dot1.get_right(), dot10.get_left(), color=GREEN_A, stroke_width=5
        )
        dot_num = (
            Dot(numl.n2p(x_val.get_value()), radius=0.1)
            .set_fill(GREEN, opacity=1)
            .set_stroke(GREEN_E, width=2)
        )
        line_num = DashedLine(
            text_decimal[-13:-4].get_bottom(),
            dot_num.get_top(),
            color=GREEN_D,
            stroke_width=2,
        )

        self.playw(
            *[
                FadeIn(item)
                for item in [
                    numl,
                    tick0,
                    tick1,
                    tick10,
                    dot1,
                    line110,
                    dot10,
                    dot_num,
                    line_num,
                ]
            ],
        )
        line_num.add_updater(
            lambda m: m.put_start_and_end_on(
                text_decimal[-13:-4].get_bottom(), dot_num.get_top()
            )
        )
        dot_num.add_updater(lambda m: m.move_to(numl.n2p(x_val.get_value())))

        self.playw(x_val.animate.set_value(9.8765432), run_time=5)
        text_decimal.clear_updaters()
        line_num.clear_updaters()
        dot_num.clear_updaters()
        ## brace: range, 1000 <= num < 10000
        brace = Brace(VGroup(numl.ticks[1], numl.ticks[10]), DOWN, buff=0.5).set_color(
            YELLOW_B
        )
        brace_range = (
            Tex("1000 \\leq \\text{num} < 10000", font_size=28)
            .next_to(brace, DOWN, buff=0.1)
            .set_color(YELLOW_B)
        )
        self.playw(FadeIn(brace), FadeIn(brace_range), wait=2)

        ## circumscribe 3
        self.play(Circumscribe(text_decimal[-1], color=BLUE_B, buff=0.1))

        self.play(
            text_decimal.animate.become(get_decimal(0, 9.8765432, 1)),
            brace_range.animate.become(
                Tex("10 \\leq \\text{num} < 100", font_size=28)
                .next_to(brace, DOWN, buff=0.1)
                .set_color(YELLOW_B)
            ),
        )
        self.playw(Circumscribe(brace_range))

        ## fadeout decimals

        decimals = VGroup(
            text_decimal,
            brace,
            brace_range,
            numl,
            tick0,
            tick1,
            tick10,
            dot1,
            line110,
            dot10,
            dot_num,
            line_num,
            text_dec,
        )
        self.play(FadeOut(decimals), self.cf.animate.shift(DOWN))
        self.playw(FadeIn(bins))

        ## numl
        numl = NumberLine(x_range=(0.75, 2.25, 0.25), tick_size=0.075, width=13).shift(
            DOWN
        )
        numl.ticks[0].set_opacity(0)
        numl.ticks[2:-2].set_opacity(0)
        numl.ticks[-1].set_opacity(0)
        text1 = Text("1", font_size=20, font=MONO_FONT).next_to(numl.n2p(1), DOWN)
        text2 = Text("2", font_size=20, font=MONO_FONT).next_to(numl.n2p(2), DOWN)
        dot1 = (
            Dot(numl.n2p(1), radius=0.075)
            .set_fill(GREEN, opacity=1)
            .set_stroke(width=0)
        )
        dot2 = (
            Dot(numl.n2p(2), radius=0.075)
            .set_fill(GREEN, opacity=0)
            .set_stroke(color=GREEN, width=4)
        )
        line12 = Line(dot1.get_right(), dot2.get_left(), color=GREEN_A, stroke_width=5)
        self.playw(FadeIn(VGroup(text1, text2, dot1, dot2, line12, numl)))

        ## mantissa
        def get_mantissa(string: str):
            if len(string) != 23:
                print("[WARNING] Mantissa string must be 23 bits long.")
            text = (
                Text(string, font_size=32, font=MONO_FONT)
                .arrange(RIGHT, buff=0.05)
                .set_color(GREEN)
                .move_to(tm)
            )
            return text

        self.playw(tm.animate.become(get_mantissa("1" + "0" * 22)))

        ## num_dot
        val = ValueTracker(1.5)

        num_dot = (
            Dot(numl.n2p(val.get_value()), radius=0.075)
            .set_fill(GREEN, opacity=1)
            .set_stroke(width=0)
        )
        line_num_dot = DashedLine(
            tm.get_bottom(),
            num_dot.get_top(),
            color=GREEN_D,
            stroke_width=2,
        )
        self.playw(FadeIn(num_dot), FadeIn(line_num_dot))
        num_dot.add_updater(lambda m: m.move_to(numl.n2p(val.get_value())))
        line_num_dot.add_updater(
            lambda m: m.put_start_and_end_on(tm.get_bottom(), num_dot.get_top())
        )

        def mantissa_string_to_bits(num: float) -> str:
            if num < 1 or num >= 2:
                raise ValueError("Mantissa must be in the range [1, 2).")
            mantissa = num - 1
            bits = []
            for _ in range(23):
                mantissa *= 2
                if mantissa >= 1:
                    bits.append("1")
                    mantissa -= 1
                else:
                    bits.append("0")
            return "".join(bits)

        tm.add_updater(
            lambda m: m.become(get_mantissa(mantissa_string_to_bits(val.get_value())))
        )
        self.playw(val.animate.set_value(2 - 0.5**23), run_time=2)
        exact_value = (
            Tex("(2 - 2^{-23})", font_size=32)
            .next_to(num_dot, UP, buff=0.1)
            .set_color(GREEN)
            .shift(RIGHT * 0.2)
        )
        self.playw(FadeIn(exact_value))

        self.playw(val.animate.set_value(1), run_time=2)
        tm.clear_updaters()
        num_dot.clear_updaters()
        line_num_dot.clear_updaters()

        ## brace for binary, nlt
        brace = Brace(numl.ticks[1:-1], DOWN, buff=0.5).set_color(YELLOW_B)
        brace_t = (
            Tex("1 \\leq \\text{num} < 2", font_size=32)
            .next_to(brace, DOWN, buff=0.1)
            .set_color(YELLOW_B)
        )
        self.playw(FadeIn(brace), FadeIn(brace_t))
        new_brace_t = (
            Tex("2^0 \\leq \\text{num} < 2^1", font_size=32)
            .next_to(brace, DOWN, buff=0.1)
            .set_color(YELLOW_B)
        )
        self.playw(
            Transform(brace_t[0], new_brace_t[:2]),
            Transform(brace_t[1:-1], new_brace_t[2:-2]),
            Transform(brace_t[-1], new_brace_t[-2:]),
        )

        ## circumscribed exponent
        self.play(Circumscribe(te))

        def get_te(num: int):
            if num < 0 or num > 255:
                raise ValueError("Exponent must be in the range [0, 255].")
            bits = np.binary_repr(num, width=8)
            text = (
                Text(bits, font_size=32, font=MONO_FONT).set_color(BLUE_B).move_to(te)
            )
            for b in text:
                b.scale(0.75)
            return text

        self.playw(te.animate.become(get_te(0)))
        self.play(te.animate.become(get_te(1)))
        new_brace_t = (
            Tex("2^1 \\leq \\text{num} < 2^2", font_size=32)
            .next_to(brace, DOWN, buff=0.1)
            .set_color(YELLOW_B)
        )
        self.playw(
            Transform(brace_t[0], new_brace_t[:2]),
            Transform(brace_t[1:-1], new_brace_t[2:-2]),
            Transform(brace_t[-1], new_brace_t[-2:]),
            Circumscribe(brace_t[-1]),
            Circumscribe(brace_t[0]),
        )

        ## fadeout text_bin
        self.playw(FadeOut(text_bin))

        def get_float(num: float):
            if num <= 0:
                raise ValueError("Number must be positive.")
            text = Text(f"{num:.4f}... =", font_size=24, font=MONO_FONT).next_to(
                pm, LEFT, buff=0.2
            )
            return text

        t = get_float(2.0)
        val = ValueTracker(2.0)
        self.playw(FadeIn(t))
        t.add_updater(lambda m: m.become(get_float(val.get_value())))
        num_dot.add_updater(lambda m: m.move_to(numl.n2p(val.get_value() / 2)))
        line_num_dot.add_updater(
            lambda m: m.put_start_and_end_on(tm.get_bottom(), num_dot.get_top())
        )
        tm.add_updater(
            lambda m: m.become(
                get_mantissa(mantissa_string_to_bits(val.get_value() / 2))
            )
        )
        self.playw(val.animate.set_value(3.5))

        tm.clear_updaters()
        num_dot.clear_updaters()
        t.clear_updaters()

        ## + 2^-23
        self.add(tm)
        new_tm = get_mantissa(mantissa_string_to_bits(1.75 + 2**-23))
        self.play(FadeTransform(tm, new_tm))

        self.playw(Circumscribe(new_tm[-1]))

        ## error = (2^-23 * 2^1) / (1.75 * 2^1) = 2^-23 / 1.75

        error = (
            Tex("\\text{error} = \\frac{2^{-23}}{1.75} = 0.000000068 \%", font_size=32)
            .set_color(PURE_RED)
            .next_to(new_tm, UP)
        )
        self.playw(FadeIn(error, shift=UP * 0.5))

        self.playw(FadeOut(error, shift=UP * 0.5), FadeOut(t))

        ## circumscribe exponent

        self.playw(Circumscribe(te))
        tec = te.copy()

        def get_exp(num: int):
            if isinstance(num, float):
                num = int(num)
            if num < -128 or num > 127:
                raise ValueError("Exponent must be in the range [-128, 127].")
            bits = np.binary_repr(num & 0xFF, width=8)
            text = (
                Text(bits, font_size=32, font=MONO_FONT).set_color(BLUE_B).move_to(tec)
            )
            for b in text:
                b.scale(0.75)
            return text

        def get_num(num: int):
            if isinstance(num, float):
                num = int(num)
            return (
                Text(f"{num}", font_size=32, font=MONO_FONT)
                .next_to(te, UP, buff=0.2)
                .set_color(BLUE_B)
            )

        val_exp = ValueTracker(1)
        num = get_num(int(val_exp.get_value()))
        self.playw(FadeIn(num))
        te.add_updater(lambda m: m.become(get_exp(val_exp.get_value())))
        num.add_updater(lambda m: m.become(get_num(val_exp.get_value())))

        self.playw(val_exp.animate.set_value(127), run_time=2.5, wait=2)
        self.playw(val_exp.animate.set_value(-128), run_time=2.5, wait=2)
        self.playw(val_exp.animate.set_value(127), run_time=2, wait=2)

        te.clear_updaters()
        num.clear_updaters()

        ## 2 ^ {2 ^ 7}

        self.playw(FadeOut(te, shift=DOWN * 0.5), num.animate.align(te, DL, buff=0))

        new_num = (
            Tex("(2^7 - 1)", font_size=32)
            .move_to(num)
            .align_to(num, LEFT)
            .set_color(BLUE_B)
        )
        self.playw(Transformr(num, new_num))

        self.playw(Indicate(VGroup(double[1], new_num[1:3])))

        ## new_brace_t

        new_brace_t = (
            Tex("2^{127} \\leq \\text{num} < 2^{128}", font_size=32)
            .next_to(brace, DOWN, buff=0.1)
            .set_color(YELLOW_B)
        )
        self.play(Circumscribe(brace_t))
        self.playw(
            Transform(brace_t[0], new_brace_t[:4]),
            Transform(brace_t[1:-1], new_brace_t[4:-4]),
            Transform(brace_t[-1], new_brace_t[-4:]),
            wait=2,
        )

        len_2127 = len(str(2**127))
        len_2128 = len(str(2**128))
        new_brace_t = Tex(
            "{" + str(2**127) + "} \\leq \\text{num} < {" + str(2**128) + "}",
            font_size=28,
        )
        new_brace_t.set_color(YELLOW_B).next_to(brace, DOWN, buff=0.1)
        self.playw(
            Transform(brace_t[0], new_brace_t[:len_2127]),
            Transform(brace_t[1:-1], new_brace_t[len_2127:-len_2128]),
            Transform(brace_t[-1], new_brace_t[-len_2128:]),
            wait=2,
        )

        ## larger than 2147483647
        text = (
            Tex("> 2147483647", font_size=28)
            .rotate(-PI / 6)
            .set_color(RED_B)
            .next_to(brace_t[0], DR, buff=0.1)
            .shift(LEFT * 0.2)
        )
        self.playw(FadeIn(text), self.cf.animate.shift(DOWN))


class reflectIntro(InteractiveScene, Scene2D):
    def construct(self):

        ## representation: sign, mantissa, exponent
        x32 = Words(
            "xxxxxxxx xxxxxxxx xxxxxxxx xxxxxxxx", font_size=32, font=MONO_FONT
        ).set_color(YELLOW_E)
        ts = x32[0]
        tm = x32[1:24]
        te = x32[24:]
        ts.set_color(RED_C)
        tm.set_color(GREEN)
        te.set_color(BLUE_B)

        self.playw(FadeIn(x32), wait=2)

        ts.generate_target()
        tm.generate_target()
        te.generate_target()

        tm.target.arrange(RIGHT, buff=0.05)
        VGroup(ts.target, tm.target, te.target).arrange(RIGHT, buff=0.75)

        self.play(MoveToTarget(ts), MoveToTarget(tm), MoveToTarget(te))

        onedot = Tex("1.", font_size=32).next_to(tm, LEFT, buff=0.1)
        pm = Tex("\\pm", font_size=32).next_to(onedot, LEFT, buff=0.1).set_color(RED_C)
        double = Tex("\\times 2^1", font_size=32).next_to(tm, RIGHT, buff=0.1)
        double[-1].set_opacity(0)
        self.playw(
            FadeIn(onedot),
            FadeIn(double),
            te.animate.align(double[-1], DL, buff=0.01),
            Transformr(ts, pm),
        )

        representation = VGroup(pm, onedot, tm, double, te)

        ## 1 ~ 2

        numl_12 = NumberLine(x_range=(0.5, 2.5, 0.5), tick_size=0.075, width=13).shift(
            DOWN * 0.5
        )
        numl_12.ticks[0].set_opacity(0)
        numl_12.ticks[2].set_opacity(0)
        numl_12.ticks[-1].set_opacity(0)
        t1 = numl_12.ticks[1]
        t2 = numl_12.ticks[-2]

        tick1 = (
            Text("1", font_size=20, font=MONO_FONT)
            .next_to(numl_12.n2p(1), DOWN)
            .set_color(GREY_B)
        )
        tick2 = (
            Text("2", font_size=20, font=MONO_FONT)
            .next_to(numl_12.n2p(2), DOWN)
            .set_color(GREY_B)
        )

        self.playw(
            FadeIn(numl_12),
            FadeIn(tick1),
            FadeIn(tick2),
            representation.animate.shift(UP * 1.2),
        )

        ## ticks
        def get_ticks():
            return numl_12.ticks[1].copy()

        num_ticks12 = 128 + 3
        linspace12 = np.linspace(1, 2, num_ticks12)
        ticks = VGroup(*[get_ticks().move_to(numl_12.n2p(x)) for x in linspace12])
        ticks[len(ticks) // 2 - 1 : len(ticks) // 2 + 2].become(
            Text("...", font_size=12, font=MONO_FONT)
            .move_to(ticks[len(ticks) // 2 - 1 : len(ticks) // 2 + 2])
            .shift(UP * 0.1)
        )
        self.playw(FadeIn(ticks))

        brace12 = Brace(
            VGroup(numl_12.ticks[1], numl_12.ticks[-2]), UP, buff=0.15
        ).set_color(GREEN_C)
        brace_num = (
            VGroup(
                Text("표현 가능 숫자 갯수: ", font_size=24), Tex("2^{23}", font_size=32)
            )
            .arrange(RIGHT, buff=0.1)
            .next_to(brace12, UP, buff=0.1)
            .set_color(GREEN_C)
        )
        self.playw(FadeIn(brace12), FadeIn(brace_num))

        ## 1~4

        numl_14 = NumberLine(x_range=(0.5, 4.5, 0.5), tick_size=0.075, width=13).shift(
            DOWN * 0.5
        )
        numl_14.ticks[0].set_opacity(0)
        numl_14.ticks[2:-2].set_opacity(0)
        numl_14.ticks[-1].set_opacity(0)
        numl_14.ticks[3].set_opacity(1)
        t4 = numl_14.ticks[-2]

        new_ticks12 = VGroup(*[get_ticks().move_to(numl_14.n2p(x)) for x in linspace12])
        new_brace12 = Brace(
            VGroup(numl_14.ticks[1], numl_14.ticks[3]), UP, buff=0.15
        ).set_color(GREEN_C)

        self.playw(
            t1.animate.move_to(numl_14.n2p(1)),
            t2.animate.move_to(numl_14.n2p(2)),
            Transform(ticks, new_ticks12),
            Transform(brace12, new_brace12),
            brace_num.animate.next_to(new_brace12, UP, buff=0.1),
            tick1.animate.next_to(numl_14.n2p(1), DOWN),
            tick2.animate.next_to(numl_14.n2p(2), DOWN),

        )
        tick4 = (
            Text("4", font_size=20, font=MONO_FONT)
            .next_to(numl_14.n2p(4), DOWN)
            .set_color(GREY_B)
        )
        self.playw(
            FadeIn(t4), 
            FadeIn(tick4)
        )

        ## 1~4, ticks

        linspace24 = np.linspace(2, 4, num_ticks12)
        ticks24 = VGroup(*[get_ticks().move_to(numl_14.n2p(x)) for x in linspace24])
        ticks24[len(ticks24) // 2 - 1 : len(ticks24) // 2 + 2].become(
            Text("...", font_size=12, font=MONO_FONT)
            .move_to(ticks24[len(ticks24) // 2 - 1 : len(ticks24) // 2 + 2])
            .shift(UP * 0.1)
        )
        self.playw(FadeIn(ticks24))

        brace24 = Brace(
            VGroup(numl_14.ticks[3], numl_14.ticks[-2]), UP, buff=0.15
        ).set_color(GREEN_C)
        brace_num24 = (
            VGroup(
                Text("표현 가능 숫자 갯수: ", font_size=24), Tex("2^{23}", font_size=32)
            )
            .arrange(RIGHT, buff=0.1)
            .next_to(brace24, UP, buff=0.1)
            .set_color(GREEN_C)
        )
        self.playw(FadeIn(brace24), FadeIn(brace_num24))

        ## 1~8

        numl_18 = NumberLine(x_range=(0.5, 8.5, 0.5), tick_size=0.075, width=13).shift(
            DOWN * 0.5
        )
        # opacity 1 at 1, 2, 4, 8
        numl_18.ticks[0].set_opacity(0)
        numl_18.ticks[1].set_opacity(1)
        numl_18.ticks[2].set_opacity(0)
        numl_18.ticks[3].set_opacity(1)
        numl_18.ticks[4:-2].set_opacity(0)
        numl_18.ticks[7].set_opacity(1)
        numl_18.ticks[-2].set_opacity(1)

        t8 = numl_18.ticks[-2]
        tick8 = (
            Text("8", font_size=20, font=MONO_FONT)
            .next_to(numl_18.n2p(8), DOWN)
            .set_color(GREY_B)
        )

        new_brace12 = Brace(
            VGroup(numl_18.ticks[1], numl_18.ticks[3]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_ticks12 = VGroup(*[get_ticks().move_to(numl_18.n2p(x)) for x in linspace12])

        new_brace24 = Brace(
            VGroup(numl_18.ticks[3], numl_18.ticks[7]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_ticks24 = VGroup(*[get_ticks().move_to(numl_18.n2p(x)) for x in linspace24])

        self.playw(
            t1.animate.move_to(numl_18.n2p(1)),
            t2.animate.move_to(numl_18.n2p(2)),
            t4.animate.move_to(numl_18.n2p(4)),
            Transform(ticks, new_ticks12),
            Transform(brace12, new_brace12),
            Transform(ticks24, new_ticks24),
            Transform(brace24, new_brace24),
            brace_num.animate.next_to(new_brace12, UP, buff=0.1).shift(LEFT*0.6),
            brace_num24.animate.next_to(new_brace24, UP, buff=0.1).shift(RIGHT*0.2),
            tick1.animate.next_to(numl_18.n2p(1), DOWN),
            tick2.animate.next_to(numl_18.n2p(2), DOWN),
            tick4.animate.next_to(numl_18.n2p(4), DOWN),
            FadeIn(t8),
            FadeIn(tick8),
            t8.animate.move_to(numl_18.n2p(8)),
        )

        brace48 = Brace(
            VGroup(numl_18.ticks[7], numl_18.ticks[-2]), UP, buff=0.15
        ).set_color(GREEN_C)
        brace_num48 = (
            VGroup(
                Text("표현 가능 숫자 갯수: ", font_size=24), Tex("2^{23}", font_size=32)
            )
            .arrange(RIGHT, buff=0.1)
            .next_to(brace48, UP, buff=0.1)
            .set_color(GREEN_C)
        )

        ticks48 = VGroup(*[get_ticks().move_to(numl_18.n2p(x)) for x in np.linspace(4, 8, num_ticks12)])
        ticks48[len(ticks48) // 2 - 1 : len(ticks48) // 2 + 2].become(
            Text("...", font_size=12, font=MONO_FONT)
            .move_to(ticks48[len(ticks48) // 2 - 1 : len(ticks48) // 2 + 2])
            .shift(UP * 0.1)
        )

        self.playw(FadeIn(brace48), FadeIn(brace_num48), FadeIn(ticks48))

        ## 1~64

        numl_164 = NumberLine(x_range=(0.5, 64.5, 0.5), tick_size=0.075, width=13).shift(
            DOWN * 0.5
        )
        numl_164.ticks.set_opacity(0)
        for i in [1, 3, 7, 15, 31, 63, -2]:
            numl_164.ticks[i].set_opacity(1)
        t16, t32, t64 = numl_164.ticks[31], numl_164.ticks[63], numl_164.ticks[-2]

        tick16 = (
            Text("16", font_size=20, font=MONO_FONT)
            .next_to(numl_164.n2p(16), DOWN)
            .set_color(GREY_B)
        )
        tick32 = (
            Text("...", font_size=20, font=MONO_FONT)
            .next_to(numl_164.n2p(32), DOWN)
            .set_color(GREY_B)
        )
        tick64 = (
            Tex("2^{23}", font_size=28)
            .next_to(numl_164.n2p(64), DOWN)
            .set_color(GREY_B)
        )
        new_brace12 = Brace(
            VGroup(numl_164.ticks[1], numl_164.ticks[3]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_brace24 = Brace(
            VGroup(numl_164.ticks[3], numl_164.ticks[7]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_brace48 = Brace(
            VGroup(numl_164.ticks[7], numl_164.ticks[15]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_ticks12 = VGroup(*[get_ticks().move_to(numl_164.n2p(x)) for x in linspace12])
        new_ticks24 = VGroup(*[get_ticks().move_to(numl_164.n2p(x)) for x in linspace24])
        new_ticks48 = VGroup(*[get_ticks().move_to(numl_164.n2p(x)) for x in np.linspace(4, 8, num_ticks12)])

        self.play(
            FadeOut(VGroup(brace_num, brace_num24, brace_num48)),
            *[Transform(brace, new_brace) for brace, new_brace in zip([brace12, brace24, brace48], [new_brace12, new_brace24, new_brace48])],
            t1.animate.move_to(numl_164.n2p(1)),
            t2.animate.move_to(numl_164.n2p(2)),
            t4.animate.move_to(numl_164.n2p(4)),
            t8.animate.move_to(numl_164.n2p(8)),
            tick1.animate.next_to(numl_164.n2p(1), DOWN),
            tick2.animate.next_to(numl_164.n2p(2), DOWN),
            tick4.animate.next_to(numl_164.n2p(4), DOWN),
            tick8.animate.next_to(numl_164.n2p(8), DOWN),
            Transform(ticks, new_ticks12),
            Transform(ticks24, new_ticks24),
            Transform(ticks48, new_ticks48)
        )
        self.playw(
            FadeIn(t16), FadeIn(t32), FadeIn(t64),
            FadeIn(tick16), FadeIn(tick32), FadeIn(tick64)
        )

        ## brace 223

        brace223 = Brace(
            VGroup(numl_164.ticks[63], numl_164.ticks[-2]), UP, buff=0.15
        ).set_color(GREEN_C)
        brace_num223 = (
            VGroup(
                Text("표현 가능 숫자 갯수: ", font_size=24), Tex("2^{23}", font_size=32)
            )
            .arrange(RIGHT, buff=0.1)
            .next_to(brace223, UP, buff=0.1)
            .set_color(GREEN_C)
        )
        self.playw(FadeIn(brace223), FadeIn(brace_num223))

        ## 간격: 223 - 222
        interval = (
            VGroup(Text("길이: ", font_size=24), Tex("2^{23} - 2^{22} = 2^{22}", font_size=32)).arrange(RIGHT)
            .next_to(brace223, UP, buff=0.1)
            .set_color(GREEN_C)
        )
        self.playw(brace_num223.animate.shift(UP*0.5), FadeIn(interval))

        ## ticks 222~223: 32~64
        linspace222_223 = np.linspace(32, 64, num_ticks12)

        ticks222_223 = VGroup(*[get_ticks().move_to(numl_164.n2p(x)) for x in linspace222_223])
        self.playw(FadeIn(ticks222_223))
        self.cf.save_state()
        self.playw(self.cf.animate.reorient(46, 71, -16, (np.float32(5.51), np.float32(-0.38), np.float32(0.02)), 1.90), FadeOut(VGroup(ticks222_223[:-2], interval, brace_num223)))
        self.playw(Indicate(ticks222_223[-2:]))

        self.playw(Restore(self.cf))

        ## exponent: 0001 0111 == 23

        te_num = Text("00010111", font_size=32, font=MONO_FONT).set_color(BLUE_B).move_to(te)
        self.play(Circumscribe(te, color=BLUE_B, buff=0.1))
        self.playw(Transform(te, te_num))

        ## exponent: 0001 1000 == 24

        te_num = Text("00011000", font_size=32, font=MONO_FONT).set_color(BLUE_B).move_to(te)
        self.play(Circumscribe(te, color=BLUE_B, buff=0.1))
        self.playw(Transform(te, te_num))

        ## 1~128

        numl_1128 = NumberLine(x_range=(0.5, 128.5, 0.5), tick_size=0.075, width=13).shift(
            DOWN * 0.5
        )

        numl_1128.ticks.set_opacity(0)
        for i in [1, 3, 7, 15, 31, 63, 127, -2]:
            numl_1128.ticks[i].set_opacity(1)
        
        tick128 = (
            Tex("2^{24}", font_size=28)
            .next_to(numl_1128.n2p(128), DOWN)
            .set_color(GREY_B)
        )
        t128 = numl_1128.ticks[-2]

        new_brace12 = Brace(
            VGroup(numl_1128.ticks[1], numl_1128.ticks[3]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_brace24 = Brace(
            VGroup(numl_1128.ticks[3], numl_1128.ticks[7]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_brace48 = Brace(
            VGroup(numl_1128.ticks[7], numl_1128.ticks[15]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_ticks12 = VGroup(*[get_ticks().move_to(numl_1128.n2p(x)) for x in linspace12])
        new_ticks24 = VGroup(*[get_ticks().move_to(numl_1128.n2p(x)) for x in linspace24])
        new_ticks48 = VGroup(*[get_ticks().move_to(numl_1128.n2p(x)) for x in np.linspace(4, 8, num_ticks12)])

        self.play(
            FadeOut(VGroup(brace223, ticks222_223[-2:])),
            *[Transform(brace, new_brace) for brace, new_brace in zip([brace12, brace24, brace48], [new_brace12, new_brace24, new_brace48])],
            t1.animate.move_to(numl_1128.n2p(1)),
            t2.animate.move_to(numl_1128.n2p(2)),
            t4.animate.move_to(numl_1128.n2p(4)),
            t8.animate.move_to(numl_1128.n2p(8)),
            t16.animate.move_to(numl_1128.n2p(16)),
            t32.animate.move_to(numl_1128.n2p(32)),
            t64.animate.move_to(numl_1128.n2p(64)),
            tick1.animate.next_to(numl_1128.n2p(1), DOWN),
            tick2.animate.next_to(numl_1128.n2p(2), DOWN),
            tick4.animate.next_to(numl_1128.n2p(4), DOWN),
            tick8.animate.next_to(numl_1128.n2p(8), DOWN),
            tick16.animate.next_to(numl_1128.n2p(16), DOWN),
            tick32.animate.next_to(numl_1128.n2p(32), DOWN),
            tick64.animate.next_to(numl_1128.n2p(64), DOWN),
            Transform(ticks, new_ticks12),
            Transform(ticks24, new_ticks24),
            Transform(ticks48, new_ticks48),
        )
        self.playw(
            FadeIn(t128),
            FadeIn(tick128),
        )

        ## brace 224

        brace224 = Brace(
            VGroup(numl_1128.ticks[127], numl_1128.ticks[-2]), UP, buff=0.15
        ).set_color(GREEN_C)
        brace_num224 = (
            VGroup(
                Text("표현 가능 숫자 갯수: ", font_size=24), Tex("2^{23}", font_size=32)
            )
            .arrange(RIGHT, buff=0.1)
            .next_to(brace224, UP, buff=0.1)
            .set_color(GREEN_C)
        )
        self.playw(FadeIn(brace224), FadeIn(brace_num224))

        ## 간격: 224 - 223
        interval224 = (
            VGroup(Text("길이: ", font_size=24), Tex("2^{24} - 2^{23} = 2^{23}", font_size=32)).arrange(RIGHT)
            .next_to(brace224, UP, buff=0.1)
            .set_color(GREEN_C)
        )
        self.playw(brace_num224.animate.shift(UP*0.5), FadeIn(interval224))
        self.playw(Circumscribe(VGroup(interval224[-1][-3:], brace_num224[-1])))

        self.embed()
        ## ticks 223~224: 64~128
        linspace223_224 = np.linspace(64, 128, num_ticks12)

        ticks223_224 = VGroup(*[get_ticks().move_to(numl_1128.n2p(x)) for x in linspace223_224])
        self.playw(FadeIn(ticks223_224))
        self.cf.save_state()
        self.playw(self.cf.animate.reorient(46, 71, -16, (np.float32(5.51), np.float32(-0.38), np.float32(0.02)), 1.90), FadeOut(VGroup(ticks223_224[:-2], interval224, brace_num224)))
        self.playw(Indicate(ticks223_224[-2:]))

        self.playw(Restore(self.cf))

        ## exponent: 0001 1001 == 25

        te_num = Text("00011001", font_size=32, font=MONO_FONT).set_color(BLUE_B).move_to(te)
        self.play(Circumscribe(te, color=BLUE_B, buff=0.1))
        self.playw(Transform(te, te_num))

        ## 1~256

        numl_1256 = NumberLine(x_range=(0.5, 256.5, 0.5), tick_size=0.075, width=13).shift(
            DOWN * 0.5
        )

        numl_1256.ticks.set_opacity(0)
        for i in [1, 3, 7, 15, 31, 63, 127, 255, -2]:
            numl_1256.ticks[i].set_opacity(1)

        tick256 = (
            Tex("2^{25}", font_size=28)
            .next_to(numl_1256.n2p(256), DOWN)
            .set_color(GREY_B)
        )
        t256 = numl_1256.ticks[-2]

        new_brace12 = Brace(
            VGroup(numl_1256.ticks[1], numl_1256.ticks[3]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_brace24 = Brace(
            VGroup(numl_1256.ticks[3], numl_1256.ticks[7]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_brace48 = Brace(
            VGroup(numl_1256.ticks[7], numl_1256.ticks[15]), UP, buff=0.15
        ).set_color(GREEN_C)
        new_ticks12 = VGroup(*[get_ticks().move_to(numl_1256.n2p(x)) for x in linspace12])
        new_ticks24 = VGroup(*[get_ticks().move_to(numl_1256.n2p(x)) for x in linspace24])
        new_ticks48 = VGroup(*[get_ticks().move_to(numl_1256.n2p(x)) for x in np.linspace(4, 8, num_ticks12)])

        self.play(
            FadeOut(VGroup(brace224, ticks223_224[-2:])),
            *[Transform(brace, new_brace) for brace, new_brace in zip([brace12, brace24, brace48], [new_brace12, new_brace24, new_brace48])],
            t1.animate.move_to(numl_1256.n2p(1)),
            t2.animate.move_to(numl_1256.n2p(2)),
            t4.animate.move_to(numl_1256.n2p(4)),
            t8.animate.move_to(numl_1256.n2p(8)),
            t16.animate.move_to(numl_1256.n2p(16)),
            t32.animate.move_to(numl_1256.n2p(32)),
            t64.animate.move_to(numl_1256.n2p(64)),
            t128.animate.move_to(numl_1256.n2p(128)),
            tick1.animate.next_to(numl_1256.n2p(1), DOWN),
            tick2.animate.next_to(numl_1256.n2p(2), DOWN),
            tick4.animate.next_to(numl_1256.n2p(4), DOWN),
            tick8.animate.next_to(numl_1256.n2p(8), DOWN),
            tick16.animate.next_to(numl_1256.n2p(16), DOWN),
            tick32.animate.next_to(numl_1256.n2p(32), DOWN),
            tick64.animate.next_to(numl_1256.n2p(64), DOWN),
            tick128.animate.next_to(numl_1256.n2p(128), DOWN),
            Transform(ticks, new_ticks12),
            Transform(ticks24, new_ticks24),
            Transform(ticks48, new_ticks48),
        )
        self.playw(
            FadeIn(t256),
            FadeIn(tick256),
        )

        ## brace 225

        brace225 = Brace(
            VGroup(numl_1256.ticks[255], numl_1256.ticks[-2]), UP, buff=0.15
        ).set_color(GREEN_C)
        brace_num225 = (
            VGroup(
                Text("표현 가능 숫자 갯수: ", font_size=24), Tex("2^{23}", font_size=32)
            )
            .arrange(RIGHT, buff=0.1)
            .next_to(brace225, UP, buff=0.1)
            .set_color(GREEN_C)
        )
        self.playw(FadeIn(brace225), FadeIn(brace_num225))

        ## 간격: 225 - 224
        interval225 = (
            VGroup(Text("길이: ", font_size=24), Tex("2^{25} - 2^{24} = 2^{24}", font_size=32)).arrange(RIGHT)
            .next_to(brace225, UP, buff=0.1)
            .set_color(GREEN_C)
        )
        self.playw(brace_num225.animate.shift(UP*0.5), FadeIn(interval225))
        self.playw(Circumscribe(VGroup(interval225[-1][-3:], brace_num225[-1])))

        ## ticks 224~225: 128~256
        linspace224_225 = np.linspace(128, 256, num_ticks12)

        ticks224_225 = VGroup(*[get_ticks().move_to(numl_1256.n2p(x)) for x in linspace224_225])
        self.playw(FadeIn(ticks224_225))
        self.cf.save_state()
        self.playw(self.cf.animate.reorient(46, 71, -16, (np.float32(5.51), np.float32(-0.38), np.float32(0.02)), 1.90), FadeOut(VGroup(ticks224_225[:-2], interval225, brace_num225)))
        self.playw(Indicate(ticks224_225[-2:]))
