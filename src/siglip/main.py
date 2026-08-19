from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


# ImageNet val samples, pre-extracted to PNG by prepare_images.py.
# springer/church have 5 images each, truck/parachute 1. No torch at render time.
IMGNET_LABELS = {
    "springer": "English springer",
    "church": "church",
    "truck": "garbage truck",
    "parachute": "parachute",
}


def imgnet_samples(label, n=5, **kwargs):
    if n == 1:
        return ImageMobject(f"imagenette/{label}_0.png", **kwargs)
    return Group(
        *[ImageMobject(f"imagenette/{label}_{i}.png", **kwargs) for i in range(n)]
    )

from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class softmax(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        def softmax(x, temperature):  # robust version
            e_x = np.exp((x - np.max(x)) / temperature)
            return e_x / e_x.sum()

        len_nums = 6
        vals = [ValueTracker(random.random() * 12 - 7) for _ in range(len_nums)]
        softmax_vals = softmax(
            np.array([vals[i].get_value() for i in range(len_nums)]), temperature=5
        )

        logits = VGroup(
            *[DecimalNumber(vals[i].get_value(), font_size=32) for i in range(len_nums)]
        )

        def get_bar(i):
            bar = Rectangle(
                width=0.5, height=softmax_vals[i] ** 2 * 9 + 0.3, color=BLUE
            ).set_fill(BLUE, opacity=0.5)
            return bar

        bars = VGroup(*[get_bar(i) for i in range(len_nums)])

        logits.arrange(RIGHT, buff=1).shift(UP * 0.5)
        for i, bar in enumerate(bars):
            if i == 0:
                bar.next_to(logits[i], UP)
            else:
                bar.next_to(logits[i], UP).align_to(bars[0], DOWN)

        softmax_eq = Tex(
            r"\sigma(\mathbf{z})_i = \frac{e^{z_i}}{\sum_{j=1}^{K} e^{z_j}}",
            font_size=48,
        ).next_to(logits, DOWN, buff=1)

        self.addw(logits, bars, softmax_eq, wait=0.2)

        ## add updater for animation

        def update_logit1(logit):
            logit.set_value(vals[2].get_value())
            return logit

        def update_bars(bars):
            softmax_vals = softmax(
                np.array([vals[i].get_value() for i in range(len_nums)]), temperature=5
            )
            for i, bar in enumerate(bars):
                bar.stretch_to_fit_height(softmax_vals[i] ** 2 * 9 + 0.3)
                if i == 0:
                    bar.next_to(logits[i], UP)
                else:
                    bar.next_to(logits[i], UP).align_to(bars[0], DOWN)
            return bars

        logit1 = logits[2]
        logit1.add_updater(update_logit1)
        bars.add_updater(update_bars)

        self.playw(vals[2].animate.set_value(6.5), run_time=2)


class sigmoidConcept(InteractiveScene, Scene2D):
    def construct(self):
        ## intro
        def sigmoid(x):
            return 1 / (1 + np.exp(-x))

        val = ValueTracker(0.94)
        sigmoid_val = sigmoid(val.get_value())

        logit = (
            DecimalNumber(val.get_value(), font_size=28)
            .shift(DOWN * 2)
            .set_color(GREEN)
        )
        nump = (
            RaenimPlane(x_range=[-7, 7, 1], y_range=[-0.1, 1.1], width=24, height=8)
            .scale(0.7)
            .set_color(GREY_B)
        )
        line1 = DashedLine(nump.c2p(-7, 1), nump.c2p(7, 1), color=GREY_C)
        plot = nump.get_graph(sigmoid, color=YELLOW_B)
        dot = Dot(nump.c2p(val.get_value(), sigmoid_val), radius=0.08).set_color(BLUE_C)
        xdot = Dot(nump.c2p(val.get_value(), 0), radius=0.08).set_color(GREEN)
        xline = DashedLine(logit.get_top(), xdot.get_bottom(), color=GREEN, buff=0.07)

        yline = DashedLine(
            dot.get_left() if val.get_value() > 0 else dot.get_right(),
            nump.c2p(0, sigmoid_val),
            color=BLUE_C,
        )
        xline2 = DashedLine(
            dot.get_bottom(), nump.c2p(val.get_value(), 0), color=BLUE_C
        )
        ynum = (
            DecimalNumber(sigmoid_val, font_size=24)
            .next_to(yline, LEFT if val.get_value() > 0 else RIGHT, buff=0.05)
            .set_color(BLUE_C)
        )

        sigmoid_eq = (
            Tex(r"\sigma(x) = \frac{1}{1 + e^{-x}}", font_size=36)
            .next_to(line1, UP, buff=0.1)
            .align_to(line1, RIGHT)
            .set_color(YELLOW_B)
        )

        self.addw(
            logit,
            nump,
            line1,
            plot,
            dot,
            xdot,
            xline,
            yline,
            xline2,
            ynum,
            sigmoid_eq,
            wait=0.2,
        )

        ## add updater for animation

        def update_logit(logit):
            logit.set_value(val.get_value())
            return logit

        def update_dot(dot):
            dot.move_to(nump.c2p(val.get_value(), sigmoid(val.get_value())))
            return dot

        def update_xdot(xdot):
            xdot.move_to(nump.c2p(val.get_value(), 0))
            return xdot

        def update_xline(xline):
            xline.put_start_and_end_on(logit.get_top(), xdot.get_bottom())
            return xline

        def update_yline(yline):
            yline.put_start_and_end_on(
                dot.get_left() if val.get_value() > 0 else dot.get_right(),
                nump.c2p(0, sigmoid(val.get_value())),
            )
            return yline

        def update_xline2(xline2):
            xline2.put_start_and_end_on(dot.get_bottom(), nump.c2p(val.get_value(), 0))
            return xline2

        def update_ynum(ynum):
            ynum.set_value(sigmoid(val.get_value()))
            ynum.next_to(yline, LEFT if val.get_value() > 0 else RIGHT, buff=0.05)
            return ynum

        logit.add_updater(update_logit)
        dot.add_updater(update_dot)
        xdot.add_updater(update_xdot)
        xline.add_updater(update_xline)
        yline.add_updater(update_yline)
        xline2.add_updater(update_xline2)
        ynum.add_updater(update_ynum)

        self.play(val.animate.set_value(3), run_time=2)
        self.playw(val.animate.set_value(-3), run_time=2)


class CLIPreview(InteractiveScene, Scene2D):
    def construct(self):

        ## image/text encoder

        width = 1.7
        height = 1.1
        val = 0.9
        img_enc = (
            Polygon(
                [-width, height, 0],
                [width, height, 0],
                [val, 0, 0],
                [-val, 0, 0],
                color=BLUE_B,
            )
            .set_fill(BLUE_B, opacity=0.7)
            .shift(UP * 1.5)
        ).set_z_index(1)
        img_enc_text = (
            Text("Image Encoder", font="Cambria Math", font_size=24)
            .move_to(img_enc.get_center())
            .set_color(BLUE_E)
        ).set_z_index(1)

        text_enc = (
            Polygon(
                [-height, width, 0],
                [0, val, 0],
                [0, -val, 0],
                [-height, -width, 0],
                color=YELLOW_B,
            )
            .set_fill(YELLOW_B, opacity=0.7)
            .shift(LEFT * 2 + DOWN * 0.5)
        ).set_z_index(0.5)
        text_enc_text = (
            VGroup(
                Text("Text", font="Cambria Math", font_size=24).next_to(
                    text_enc, UP, buff=0.1
                ),
                Text("Encoder", font="Cambria Math", font_size=24).next_to(
                    text_enc, DOWN, buff=0.1
                ),
            )
            .arrange(DOWN, buff=0.1)
            .move_to(text_enc.get_center())
            .set_color(YELLOW_E)
        ).set_z_index(1)

        self.playw(
            FadeIn(img_enc),
            FadeIn(text_enc),
            FadeIn(img_enc_text),
            FadeIn(text_enc_text),
        )

        ## indicate img/text encoder
        self.playw(Indicate(img_enc, color=BLUE_D))
        self.playw(Indicate(text_enc, color=YELLOW_D))

        encs = VGroup(img_enc, text_enc, img_enc_text, text_enc_text).set_z_index(1)
        encs.save_state()

        ## rotate and move to bottom
        self.playw(encs.animate.rotate(-PI / 2.5, axis=UP).shift(RIGHT * 5.3))

        ## image and text

        img1 = imgnet_samples("church", n=1).scale(0.3)
        img2 = imgnet_samples("springer", n=1).scale(0.3)
        img3 = imgnet_samples("truck", n=1).scale(0.3)
        img4 = imgnet_samples("parachute", n=1).scale(0.3)
        imgs = Group(img1, img2, img3, img4).arrange(RIGHT, buff=0.2).shift(UP * 2.5)

        txt1 = Text("안개 속 음산한 분위기의 교회", font_size=24)
        txt2 = Text("풀밭에 누워있는 강아지", font_size=24)
        txt3 = Text("어두운 배경 속 푸른 트럭", font_size=24)
        txt4 = Text("맑은 하늘에 낙하산을 편 사람", font_size=24)
        txts = (
            Group(txt1, txt2, txt3, txt4)
            .arrange(DOWN, aligned_edge=RIGHT, buff=0.5)
            .shift(LEFT * 5)
        )

        self.playwl(
            *[
                FadeIn(Group(img, txt))
                for img, txt in zip([img1, img2, img3, img4], [txt1, txt2, txt3, txt4])
            ],
            lag_ratio=0.7,
        )

        ## lines

        lines = VGroup(
            *[
                DashedLine(
                    img.get_bottom(),
                    txt.get_right(),
                    color=GREY_B,
                    dash_length=0.05,
                    buff=0.1,
                )
                for img, txt in zip([img1, img2, img3, img4], [txt1, txt2, txt3, txt4])
            ]
        )
        self.play(FadeIn(lines))

        ## fadeout lines and restore encs
        self.playw(
            FadeOut(lines),
            encs.animate.restore(),
            imgs.animate.scale(0.6).next_to(encs.saved_state[0], UP),
            txts.animate.scale(0.7).next_to(encs.saved_state[1], LEFT),
            run_time=1.2,
        )

        ## img_encoding, txt_encoding
        img_encoding = (
            Tensor(4, arrange=RIGHT).next_to(img_enc, DOWN, buff=0.2).scale(0.8)
        )
        txt_encoding = (
            Tensor(4, arrange=DOWN).next_to(text_enc, RIGHT, buff=0.2).scale(0.8)
        )

        self.playw(
            FadeTransform(imgs.copy(), img_encoding),
            FadeTransform(txts.copy(), txt_encoding),
        )

        ## similarity matrix: inner product
        nums_np = np.random.rand(4, 4) * 7 - 1.5
        nums = (
            VGroup(
                *[
                    DecimalNumber(nums_np[i, j], font_size=18)
                    for i in range(4)
                    for j in range(4)
                ]
            )
            .arrange_in_grid(4, 4, h_buff=0.1, v_buff=0.3)
            .move_to(
                img_encoding.get_center()[0] * RIGHT + txt_encoding.get_center()[1] * UP
            )
        )

        self.playw(
            *[
                Transformr(
                    VGroup(img_encoding[i], txt_encoding[j]).copy(),
                    nums[i * 4 + j],
                    path_arc=PI / 3,
                )
                for i in range(4)
                for j in range(4)
            ]
        )

        ## hori_lines

        hori_lines = VGroup(
            *[
                DashedLine(
                    nums[i * 4].get_left(),
                    nums[i * 4 + 3].get_right(),
                    color=GREY_B,
                    dash_length=0.05,
                    stroke_width=4,
                ).set_color(YELLOW)
                for i in range(4)
            ]
        )
        self.play(*[Create(line) for line in hori_lines], run_time=0.75)
        self.playw(*[Uncreate(line) for line in hori_lines], run_time=0.75)

        ## vert_lines

        vert_lines = VGroup(
            *[
                DashedLine(
                    nums[j].get_top(),
                    nums[j + 12].get_bottom(),
                    color=GREY_B,
                    dash_length=0.05,
                    stroke_width=4,
                ).set_color(BLUE)
                for j in range(4)
            ]
        )
        self.play(*[Create(line) for line in vert_lines], run_time=0.75)
        self.playw(*[Uncreate(line) for line in vert_lines], run_time=0.75)

        ## diagonal elements:
        num_diagonals = VGroup(*[nums[i * 4 + i] for i in range(4)])
        num_diagonals_rest = VGroup(
            *[nums[i * 4 + j] for i in range(4) for j in range(4) if i != j]
        )

        diag_arrow = VGroup(
            *[
                Text("↑", font_size=24, color=BLUE)
                .next_to(nums[i * 4 + i], RIGHT, buff=0.05)
                .set_color(RED)
                for i in range(4)
            ]
        )
        self.playw(
            *[FadeIn(arrow) for arrow in diag_arrow],
            num_diagonals_rest.animate.set_opacity(0.2),
            num_diagonals.animate.set_color(RED),
        )

        ## non-diagonal elements

        non_diag_arrow = VGroup(
            *[
                Text("↓", font_size=24, color=BLUE)
                .next_to(nums[i * 4 + j], RIGHT, buff=0.05)
                .set_color(BLUE)
                for i in range(4)
                for j in range(4)
                if i != j
            ]
        )
        self.play(
            num_diagonals_rest.animate.set_color(BLUE).set_opacity(1),
            num_diagonals.animate.set_opacity(0.2),
            diag_arrow.animate.set_opacity(0.2),
        )
        self.playw(*[FadeIn(arrow) for arrow in non_diag_arrow])

        ## fadeouts
        self.play(
            *[FadeOut(arrow) for arrow in diag_arrow],
            *[FadeOut(arrow) for arrow in non_diag_arrow],
            num_diagonals.animate.set_opacity(0.5).set_color(WHITE),
            num_diagonals_rest.animate.set_opacity(0.5).set_color(WHITE),
            FadeOut(nums),
            FadeOut(hori_lines),
            FadeOut(vert_lines),
            FadeOut(img_encoding),
            FadeOut(txt_encoding),
        )
        img_encoder = VGroup(img_enc, img_enc_text)
        text_encoder = VGroup(text_enc, text_enc_text)
        self.playw(
            imgs.animate.scale(1.5).shift(DOWN + RIGHT),
            txts.animate.scale(1.428).shift(RIGHT * 0.7),
            img_encoder.animate.rotate(PI / 2).shift(RIGHT * 4.5),
            text_encoder.animate.rotate(-PI / 2).shift(DOWN * 2.5 + LEFT),
            self.cf.animate.scale(1.2).shift(DOWN * 0.5),
        )

        ## line1
        line1 = DashedLine(
            imgs[0].get_bottom(),
            txts[0].get_right(),
            color=GREEN,
            dash_length=0.05,
            buff=0.1,
        )
        line234 = VGroup(
            *[
                DashedLine(
                    imgs[i].get_bottom(),
                    txts[0].get_right(),
                    color=PURE_RED,
                    dash_length=0.05,
                    buff=0.1,
                )
                for i in range(1, 4)
            ]
        )
        self.playw(Create(line1), run_time=0.5)
        self.playw(Create(line234))


class siglip(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        img_enc = (
            Polygon(
                [-1.7, 1.1, 0],
                [1.7, 1.1, 0],
                [0.9, 0, 0],
                [-0.9, 0, 0],
                color=BLUE_B,
            )
            .set_fill(BLUE_B, opacity=0.7)
            .shift(UP * 1.5)
        ).set_z_index(1)
        img_enc_text = (
            Text("Image Encoder", font="Cambria Math", font_size=24)
            .move_to(img_enc.get_center())
            .set_color(BLUE_E)
        ).set_z_index(1)
        img_encoder = VGroup(img_enc, img_enc_text).set_z_index(1)

        text_enc = (
            Polygon(
                [-1.1, 1.7, 0],
                [0, 0.9, 0],
                [0, -0.9, 0],
                [-1.1, -1.7, 0],
                color=YELLOW_B,
            )
            .set_fill(YELLOW_B, opacity=0.7)
            .shift(LEFT * 2 + DOWN * 0.5)
        ).set_z_index(0.5)
        text_enc_text = (
            VGroup(
                Text("Text", font="Cambria Math", font_size=24).next_to(
                    text_enc, UP, buff=0.1
                ),
                Text("Encoder", font="Cambria Math", font_size=24).next_to(
                    text_enc, DOWN, buff=0.1
                ),
            )
            .arrange(DOWN, buff=0.1)
            .move_to(text_enc.get_center())
            .set_color(YELLOW_E)
        ).set_z_index(1)
        text_encoder = VGroup(text_enc, text_enc_text).set_z_index(1)

        ## img_encoding, txt_encoding
        imgs = (
            Group(
                imgnet_samples("church", n=1).scale(0.3),
                imgnet_samples("springer", n=1).scale(0.3),
                imgnet_samples("truck", n=1).scale(0.3),
                imgnet_samples("parachute", n=1).scale(0.3),
            )
            .arrange(RIGHT, buff=0.2)
            .shift(UP * 2.5)
            .scale(0.6)
            .next_to(img_encoder, UP, buff=0.2)
        )
        txts = (
            Group(
                Text("안개 속 음산한 분위기의 교회", font_size=24),
                Text("풀밭에 누워있는 강아지", font_size=24),
                Text("어두운 배경 속 푸른 트럭", font_size=24),
                Text("맑은 하늘에 낙하산을 편 사람", font_size=24),
            )
            .arrange(DOWN, aligned_edge=RIGHT, buff=0.5)
            .scale(0.7)
            .next_to(text_encoder, LEFT, buff=0.2)
        )
        img_encoding = (
            Tensor(4, arrange=RIGHT).next_to(img_enc, DOWN, buff=0.2).scale(0.8)
        )

        text_encoding = (
            Tensor(4, arrange=DOWN).next_to(text_enc, RIGHT, buff=0.2).scale(0.8)
        )

        nums = (
            VGroup(
                *[
                    DecimalNumber(np.random.rand() * 7 - 1.5, font_size=18)
                    for i in range(4)
                    for j in range(4)
                ]
            )
            .arrange_in_grid(4, 4, h_buff=0.1, v_buff=0.3)
            .move_to(
                img_encoding.get_center()[0] * RIGHT
                + text_encoding.get_center()[1] * UP
            )
        )

        self.addw(
            img_encoder, text_encoder, img_encoding, text_encoding, imgs, txts, nums
        )

        ## hori_lines - cross entropy
        ce1 = (
            Text("Cross Entropy", font_size=24, color=GREEN)
            .next_to(nums, RIGHT, buff=0.5)
            .set_color(GREEN)
        )

        hori_lines = VGroup(
            *[
                DashedLine(
                    nums[i * 4].get_left(),
                    nums[i * 4 + 3].get_right(),
                    color=GREY_B,
                    dash_length=0.05,
                    stroke_width=4,
                ).set_color(GREEN)
                for i in range(4)
            ]
        )
        self.play(*[Create(line) for line in hori_lines], FadeIn(ce1), run_time=0.75)
        self.playw(
            *[Uncreate(line) for line in hori_lines], FadeOut(ce1), run_time=0.75
        )

        ## vert_lines - cross entropy
        ce2 = (
            Text("Cross Entropy", font_size=24)
            .next_to(nums, DOWN, buff=0.5)
            .set_color(GREEN)
        )
        vert_lines = VGroup(
            *[
                DashedLine(
                    nums[j].get_top(),
                    nums[j + 12].get_bottom(),
                    color=GREY_B,
                    dash_length=0.05,
                    stroke_width=4,
                ).set_color(GREEN)
                for j in range(4)
            ]
        )
        self.play(*[Create(line) for line in vert_lines], FadeIn(ce2), run_time=0.75)
        self.playw(
            *[Uncreate(line) for line in vert_lines], FadeOut(ce2), run_time=0.75
        )

        ## camera setting
        self.playw(
            self.cf.animate.reorient(
                90,
                39,
                -90,
                (np.float32(0.28), np.float32(-0.67), np.float32(-0.14)),
                3.07,
            )
        )

        ## bces
        def get_bce():
            bce = (
                Text("BCE", font=MONO_FONT, font_size=12)
                .set_color(YELLOW)
                .rotate(39 * DEGREES, axis=UP)
            )
            return bce

        bces = VGroup(
            *[
                get_bce().next_to(nums[i * 4 + j], UP, buff=0.05)
                for i in range(4)
                for j in range(4)
            ]
        )
        self.playw(FadeIn(bces))

        ## sigmoids
        def get_sigmoid(num):
            sigmoid_eq = Tex(r"\frac{1}{1 + e^{" + f"{-num:.2f}" + r"}}", font_size=12)
            return sigmoid_eq

        sigmoids = VGroup(
            *[
                get_sigmoid(nums[i * 4 + j].get_value()).move_to(nums[i * 4 + j])
                for i in range(4)
                for j in range(4)
            ]
        )
        self.playwl(
            AnimationGroup(
                *[Transformr(nums[i][-4:], sigmoids[i][-4:]) for i in range(16)],
                FadeOut(
                    VGroup(*[nums[i][0] for i in range(16) if nums[i].get_value() < 0])
                ),
            ),
            FadeIn(VGroup(*[sigmoids[i][:-4] for i in range(16)])),
            lag_ratio=0.5,
        )

        ## diagonal elements
        diagonal_bces = VGroup(*[bces[i * 4 + i] for i in range(4)])
        diagonal_sigmoids = VGroup(*[sigmoids[i * 4 + i] for i in range(4)])
        non_diagonal_bces = VGroup(
            *[bces[i * 4 + j] for i in range(4) for j in range(4) if i != j]
        )
        non_diagonal_sigmoids = VGroup(
            *[sigmoids[i * 4 + j] for i in range(4) for j in range(4) if i != j]
        )
        # non - 0.2
        diagonal_bces.save_state()
        diagonal_sigmoids.save_state()
        self.playw(
            diagonal_bces.animate.set_color(GREEN),
            diagonal_sigmoids.animate.set_color(GREEN),
            non_diagonal_bces.animate.set_opacity(0.2),
            non_diagonal_sigmoids.animate.set_opacity(0.2),
        )

        ## non-diagonal elements
        self.playw(
            diagonal_bces.animate.set_opacity(0.2).set_color(YELLOW),
            diagonal_sigmoids.animate.set_opacity(0.2).set_color(WHITE),
            non_diagonal_bces.animate.set_opacity(1).set_color(RED),
            non_diagonal_sigmoids.animate.set_opacity(1).set_color(RED),
        )


class siglipNegativeBias(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        img_enc = (
            Polygon(
                [-1.7, 1.1, 0],
                [1.7, 1.1, 0],
                [0.9, 0, 0],
                [-0.9, 0, 0],
                color=BLUE_B,
            )
            .set_fill(BLUE_B, opacity=0.7)
            .shift(UP * 1.5)
        ).set_z_index(1)
        img_enc_text = (
            Text("Image Encoder", font="Cambria Math", font_size=24)
            .move_to(img_enc.get_center())
            .set_color(BLUE_E)
        ).set_z_index(1)
        img_encoder = VGroup(img_enc, img_enc_text).set_z_index(1)

        text_enc = (
            Polygon(
                [-1.1, 1.7, 0],
                [0, 0.9, 0],
                [0, -0.9, 0],
                [-1.1, -1.7, 0],
                color=YELLOW_B,
            )
            .set_fill(YELLOW_B, opacity=0.7)
            .shift(LEFT * 2 + DOWN * 0.5)
        ).set_z_index(0.5)
        text_enc_text = (
            VGroup(
                Text("Text", font="Cambria Math", font_size=24).next_to(
                    text_enc, UP, buff=0.1
                ),
                Text("Encoder", font="Cambria Math", font_size=24).next_to(
                    text_enc, DOWN, buff=0.1
                ),
            )
            .arrange(DOWN, buff=0.1)
            .move_to(text_enc.get_center())
            .set_color(YELLOW_E)
        ).set_z_index(1)
        text_encoder = VGroup(text_enc, text_enc_text).set_z_index(1)

        ## img_encoding, txt_encoding
        imgs = (
            Group(
                imgnet_samples("church", n=1).scale(0.3),
                imgnet_samples("springer", n=1).scale(0.3),
                imgnet_samples("truck", n=1).scale(0.3),
                imgnet_samples("parachute", n=1).scale(0.3),
            )
            .arrange(RIGHT, buff=0.2)
            .shift(UP * 2.5)
            .scale(0.6)
            .next_to(img_encoder, UP, buff=0.2)
        )
        txts = (
            Group(
                Text("안개 속 음산한 분위기의 교회", font_size=24),
                Text("풀밭에 누워있는 강아지", font_size=24),
                Text("어두운 배경 속 푸른 트럭", font_size=24),
                Text("맑은 하늘에 낙하산을 편 사람", font_size=24),
            )
            .arrange(DOWN, aligned_edge=RIGHT, buff=0.5)
            .scale(0.7)
            .next_to(text_encoder, LEFT, buff=0.2)
        )
        img_encoding = (
            Tensor(4, arrange=RIGHT).next_to(img_enc, DOWN, buff=0.2).scale(0.8)
        )

        text_encoding = (
            Tensor(4, arrange=DOWN).next_to(text_enc, RIGHT, buff=0.2).scale(0.8)
        )

        nums = (
            VGroup(
                *[
                    DecimalNumber(np.random.rand() * 7 - 1.5, font_size=18)
                    for i in range(4)
                    for j in range(4)
                ]
            )
            .arrange_in_grid(4, 4, h_buff=0.1, v_buff=0.3)
            .move_to(
                img_encoding.get_center()[0] * RIGHT
                + text_encoding.get_center()[1] * UP
            )
        )
        self.cf.save_state()
        self.cf.reorient(
            90, 39, -90, (np.float32(0.28), np.float32(-0.67), np.float32(-0.14)), 3.07
        )
        self.addw(
            img_encoder, text_encoder, img_encoding, text_encoding, imgs, txts, nums
        )

        ## negative bias: -10
        numsn = VGroup(
            *[
                DecimalNumber(nums[i * 4 + j].get_value() - 10, font_size=14)
                .set_color(RED_B)
                .move_to(nums[i * 4 + j])
                for i in range(4)
                for j in range(4)
            ]
        )

        self.playw(Transformr(nums, numsn))

        ## resume camera
        self.play(self.cf.animate.restore(), run_time=1.25)
        ## have all but imgs, txts shifted right
        all_but_img_txt = Group(
            img_encoder, text_encoder, img_encoding, text_encoding, numsn
        )
        all_but_img_txt.save_state()
        self.play(all_but_img_txt.animate.shift(RIGHT * 10.5))

        ## imgs, txts 모으기
        self.playw(
            imgs.animate.shift(DOWN * 1.5),
            txts.animate.shift(RIGHT * 1.3),
            self.cf.animate.scale(0.75).shift(LEFT),
        )

        ## lines
        lines = VGroup(
            *[
                Line(
                    imgs[i].get_bottom(),
                    txts[j].get_right(),
                    color=GREEN if i == j else RED_B,
                    stroke_width=4 if i == j else 2,
                )
                for i in range(len(imgs))
                for j in range(len(txts))
            ]
        )
        self.playw(*[Create(line) for line in lines], run_time=0.75)

        ## linesc to arrange down and set length same
        linesc = lines.copy()
        linesct = linesc.generate_target()
        for lt in linesct:
            lt.put_start_and_end_on(RIGHT, LEFT)
        linesct.arrange(DOWN, buff=0.2).next_to(imgs, RIGHT).shift(DOWN*2)
        self.playw(MoveToTarget(linesc))

        ## indicate greens
        self.playw(
            *[Indicate(line, color=PURE_GREEN) for i, line in enumerate(linesc) if i // 4 == i % 4]
        )

        ## indicate reds
        self.playw(
            *[Indicate(line, color=PURE_RED) for i, line in enumerate(linesc) if i // 4 != i % 4]
        )

        ## shift camera right and brace
        self.play(self.cf.animate.shift(RIGHT * 1.5))

        brace = Brace(linesc, RIGHT, buff=0.1).set_color(GREY_B)
        self.playw(FadeIn(brace))

        ## ratio = 1:B-1
        def get_ratio(b):
            ratio = Text(f"1 : {int(b-1)}", font_size=24, font="Cambria Math").next_to(brace, RIGHT, buff=0.1)
            return ratio
        bval = ValueTracker(4)
        r = get_ratio(bval.get_value())
        self.playw(FadeIn(r))

        ## update r to 32768
        r.add_updater(lambda m: m.become(get_ratio(bval.get_value())))
        self.playw(bval.animate.set_value(32768), run_time=4)

class collapse(InteractiveScene, Scene2D):
    def construct(self):
        ## img and text encoder
        img_enc = (
            Polygon(
                [-1.7, 1.1, 0],
                [1.7, 1.1, 0],
                [0.9, 0, 0],
                [-0.9, 0, 0],
                color=BLUE_B,
            )
            .set_fill(BLUE_B, opacity=0.7)
            .shift(UP * 1.5)
        ).set_z_index(1)
        img_enc_text = (
            Text("Image Encoder", font="Cambria Math", font_size=24)
            .move_to(img_enc.get_center())
            .set_color(BLUE_E)
        ).set_z_index(1)
        text_enc = (
            Polygon(
                [-1.1, 1.7, 0],
                [0, 0.9, 0],
                [0, -0.9, 0],
                [-1.1, -1.7, 0],
                color=YELLOW_B,
            )
            .set_fill(YELLOW_B, opacity=0.7)
            .shift(LEFT * 2 + DOWN * 0.5)
        ).set_z_index(0.5)
        text_enc_text = (
            VGroup(
                Text("Text", font="Cambria Math", font_size=24).next_to(
                    text_enc, UP, buff=0.1
                ),
                Text("Encoder", font="Cambria Math", font_size=24).next_to(
                    text_enc, DOWN, buff=0.1
                ),
            )
            .arrange(DOWN, buff=0.1)
            .move_to(text_enc.get_center())
            .set_color(YELLOW_E)
        ).set_z_index(1)
        img_encoder = VGroup(img_enc, img_enc_text).set_z_index(1)
        text_encoder = VGroup(text_enc, text_enc_text).set_z_index(1)

        img_encoding = (
            Tensor(4, arrange=RIGHT).next_to(img_enc, DOWN, buff=0.2).scale(0.8)
        )
        text_encoding = (
            Tensor(4, arrange=DOWN).next_to(text_enc, RIGHT, buff=0.2).scale(0.8)
        )

        nums_np = np.random.rand(4, 4) * 7 - 1.5
        vals = [ValueTracker(nums_np[i, j]) for i in range(4) for j in range(4)]
        nums = (
            VGroup(
                *[
                    DecimalNumber(vals[i * 4 + j].get_value(), font_size=18)
                    for i in range(4)
                    for j in range(4)
                ]
            )
            .arrange_in_grid(4, 4, h_buff=0.1, v_buff=0.3)
            .move_to(
                img_encoding.get_center()[0] * RIGHT
                + text_encoding.get_center()[1] * UP
            )
        )
        self.addw(img_encoder, text_encoder, img_encoding, text_encoding, nums)

        self.embed()
        ## bce_loss
        def get_bceloss(vals=vals):
            array = np.array([v.get_value() for v in vals])
            array = array.reshape(array.shape[0], -1)
            diagonal_gt = np.eye(array.shape[0])
            bce_loss_np = -(diagonal_gt * np.log(sigmoid(array)) + (1 - diagonal_gt) * np.log(1 - sigmoid(array)))
            bce_loss_np = np.mean(bce_loss_np)
            return bce_loss_np

        get_bce_dn = lambda: VGroup(
            Text("BCE Loss:", font_size=24).set_color(GREEN),
            DecimalNumber(get_bceloss(), font_size=24)
            .set_color(GREEN)
        ).arrange(RIGHT, buff=0.1).next_to(nums, DOWN, buff=0.75)

        nump = RaenimPlane(x_range=(-5, 5, 1), y_range=(-0.1, 1.1, 1), width=16, height=7).scale(0.5).next_to(nums, RIGHT, buff=0.5)
        y1line = DashedLine(nump.c2p(-5, 1), nump.c2p(5, 1), color=GREY_B, dash_length=0.05)
        sig_curve = nump.get_graph(lambda x: sigmoid(x), color=BLUE, x_range=[-5, 5], stroke_width=2)
        dots = VGroup(*[Dot(nump.c2p(vals[i * 4 + j].get_value(), sigmoid(vals[i * 4 + j].get_value())), radius=0.05).set_color(RED) for i in range(4) for j in range(4)])
        graph_items = VGroup(nump, y1line, sig_curve, dots)

        bce_dn = get_bce_dn()
        
        lines = VGroup(
            *[
                DashedLine(
                    nums[i].get_bottom(),
                    dots[i].get_top(),
                    color=GREY_B,
                    dash_length=0.05,
                ).set_opacity(0.5) for i in range(16)
            ]
        )
        def update_dots(dots):
            for i in range(4):
                for j in range(4):
                    dots[i * 4 + j].move_to(nump.c2p(vals[i * 4 + j].get_value(), sigmoid(vals[i * 4 + j].get_value())))
            return dots
        def update_lines(lines):
            for i in range(16):
                lines[i].put_start_and_end_on(nums[i].get_bottom(), dots[i].get_top())
            return lines

        self.playw(FadeIn(bce_dn), FadeIn(lines), FadeIn(graph_items))
        lines.add_updater(update_lines)
        bce_dn.add_updater(lambda m: m.become(get_bce_dn()))
        dots.add_updater(update_dots)
        nums.add_updater(lambda m: m.become(VGroup(*[DecimalNumber(vals[i * 4 + j].get_value(), font_size=18) for i in range(4) for j in range(4)]).arrange_in_grid(4, 4, h_buff=0.1, v_buff=0.3).move_to(img_encoding.get_center()[0] * RIGHT + text_encoding.get_center()[1] * UP)))
        self.playw(*[v.animate.set_value(-3.0 - random.random() * 0.2) for v in vals], run_time=3)

        # remove updates
        lines.clear_updaters()
        bce_dn.clear_updaters()
        dots.clear_updaters()
        nums.clear_updaters()

        ## img_encoder, text_encoder to be red
        ol = self.overlay
        img_enc.set_z_index(ol.z_index + 1)
        img_enc_text.set_z_index(ol.z_index + 1)
        text_enc.set_z_index(ol.z_index + 1)
        text_enc_text.set_z_index(ol.z_index + 1)
        self.add(img_enc, img_enc_text, text_enc, text_enc_text)
        self.playw(
            img_enc.animate.set_color(RED),
            img_enc_text.animate.set_color(PURE_RED),
            text_enc.animate.set_color(RED),
            text_enc_text.animate.set_color(PURE_RED),
            FadeIn(ol),
        )

class two_parameter(InteractiveScene, Scene2D):
    def construct(self):

        ## nums
        nums_np = np.random.rand(4, 4) * 3 - 1.5
        vals = [ValueTracker(nums_np[i, j]) for i in range(4) for j in range(4)]
        nums = VGroup(
            *[
                DecimalNumber(vals[i * 4 + j].get_value(), font_size=18)
                for i in range(4)
                for j in range(4)
            ]
        ).arrange_in_grid(4, 4, h_buff=0.3, v_buff=0.5)
        self.addw(nums)

        ## t', b
        mul_ico = VGroup(
            t := Tex("\\times", font_size=32), Circle(radius=0.15).move_to(t)
        ).set_color(GREY_B)
        mul = Tex(r"t'", font_size=36).next_to(mul_ico, UP, buff=0.15).set_color(GREY_B)

        bias_ico = VGroup(
            t := Tex("+", font_size=32), Circle(radius=0.15).move_to(t)
        ).set_color(GREEN)
        bias = Tex(r"b", font_size=36).next_to(bias_ico, UP, buff=0.15).set_color(GREEN)

        muls = VGroup(mul_ico, mul).next_to(nums, RIGHT, buff=3).shift(UP * 0.75)
        biass = VGroup(bias_ico, bias).next_to(muls, RIGHT, buff=1.5)

        self.playwl(
            AnimationGroup(FadeIn(muls), FadeIn(biass)),
            self.cf.animate.shift(RIGHT * 3),
            lag_ratio=0.3,
        )

        ## values of t' and b
        t_val = ValueTracker(np.log(10))
        b_val = ValueTracker(-10)

        def get_tval():
            return (
                Text(f"={t_val.get_value():.2f}", font_size=24, font=MONO_FONT)
                .next_to(mul, RIGHT, buff=0.07)
                .set_color(GREY_B)
            )

        def get_bval():
            return (
                Text(f"={b_val.get_value():.2f}", font_size=24, font=MONO_FONT)
                .next_to(bias, RIGHT, buff=0.07)
                .set_color(GREEN)
            )

        t_val_text = get_tval()
        b_val_text = get_bval()
        self.playw(FadeIn(t_val_text))
        self.playw(FadeIn(b_val_text))
        t_val_text = always_redraw(get_tval)
        b_val_text = always_redraw(get_bval)

        ## sigmoid

        nump = (
            RaenimPlane(
                x_range=(-14, 5, 1), y_range=(-0.1, 1.1, 1), width=16, height=10
            )
            .scale(0.5)
            .next_to(nums, RIGHT, buff=0.5)
        )
        y1line = DashedLine(
            nump.c2p(-14, 1), nump.c2p(5, 1), color=GREY_D, dash_length=0.05
        )
        sig_curve = nump.get_graph(
            lambda x: sigmoid(x), color=BLUE, x_range=[-14, 5], stroke_width=2
        )

        def affine_transform(x):
            return t_val.get_value() * x + b_val.get_value()

        graph_items = VGroup(nump, y1line, sig_curve).next_to(bias_ico, DOWN, buff=0)
        dots = VGroup(
            *[
                Dot(
                    nump.c2p(
                        vals[i * 4 + j].get_value(),
                        sigmoid(vals[i * 4 + j].get_value()),
                    ),
                    radius=0.05,
                ).set_color(RED)
                for i in range(4)
                for j in range(4)
            ]
        )
        # dots = VGroup(*[Dot(nump.c2p(affine_transform(vals[i * 4 + j].get_value()), sigmoid(affine_transform(vals[i * 4 + j].get_value()))), radius=0.05).set_color(RED) for i in range(4) for j in range(4)])
        lines = VGroup(
            *[
                DashedLine(
                    nums[i * 4 + j].get_center(),
                    dots[i * 4 + j].get_center(),
                    color=GREY_B,
                    dash_length=0.05,
                )
                for i in range(4)
                for j in range(4)
            ]
        ).set_opacity(0.5)
        self.playwl(
            FadeIn(VGroup(graph_items, dots, lines)),
            self.cf.animate.shift(DOWN * 1.5),
            lag_ratio=0.25,
        )

        ## link lines to mul and fade in line between mul and bias
        mul_line = DashedLine(
            mul_ico.get_right(), bias_ico.get_left(), color=GREY_B, dash_length=0.05
        )

        linest = lines.generate_target()
        for lt in linest:
            lt.put_start_and_end_on(lt.get_start(), mul_ico.get_left())
        self.playwl(MoveToTarget(lines), FadeIn(mul_line), lag_ratio=0.5, wait=0)

        new_dots = VGroup(
            *[
                Dot(
                    nump.c2p(
                        affine_transform(vals[i * 4 + j].get_value()),
                        sigmoid(affine_transform(vals[i * 4 + j].get_value())),
                    ),
                    radius=0.05,
                ).set_color(RED)
                for i in range(4)
                for j in range(4)
            ]
        )
        self.play(Transform(dots, new_dots))
        lines2 = VGroup(
            *[
                DashedLine(
                    bias_ico.get_bottom(),
                    dots[i * 4 + j].get_center(),
                    color=GREY_B,
                    dash_length=0.05,
                )
                for i in range(4)
                for j in range(4)
            ]
        ).set_opacity(0.5)
        self.playw(FadeIn(lines2), wait=4)

        ## bce loss
        def get_bce_loss(num):
            text = (
                Text(f"BCE Loss: {num:.2f}", font_size=24, font=MONO_FONT)
                .next_to(nump.x_axis, LEFT, buff=0.75)
                .set_color(YELLOW_B)
            )
            return text

        val_bce = ValueTracker(0.24)
        bce_loss = get_bce_loss(val_bce.get_value())
        self.playw(FadeIn(bce_loss))

        ## diagonal, non-diagonal
        diagonal_nums = VGroup(*[nums[i * 4 + i] for i in range(4)])
        non_diagonal_nums = VGroup(
            *[nums[i * 4 + j] for i in range(4) for j in range(4) if i != j]
        )
        diagonal_lines = VGroup(*[lines[i * 4 + i] for i in range(4)])
        non_diagonal_lines = VGroup(
            *[lines[i * 4 + j] for i in range(4) for j in range(4) if i != j]
        )
        diagonal_lines2 = VGroup(*[lines2[i * 4 + i] for i in range(4)])
        non_diagonal_lines2 = VGroup(
            *[lines2[i * 4 + j] for i in range(4) for j in range(4) if i != j]
        )

        self.playw(
            non_diagonal_nums.animate.set_opacity(0.2),
            non_diagonal_lines.animate.set_opacity(0.2),
            non_diagonal_lines2.animate.set_opacity(0.2),
            diagonal_nums.animate.set_color(WHITE),
            diagonal_lines.animate.set_color(WHITE),
            diagonal_lines2.animate.set_color(WHITE),
        )

        ## diagonal vals grow

        diagonal_vals = [vals[i * 4 + i] for i in range(4)]
        dns = VGroup(*[nums[i * 4 + i] for i in range(4)])

        def update_diagonal_nums(item):
            for i in range(4):
                item[i].set_value(diagonal_vals[i].get_value())

        diagonal_dots = VGroup(*[dots[i * 4 + i] for i in range(4)])

        def update_diagonal_dots(item):
            for i in range(4):
                item[i].move_to(
                    nump.c2p(
                        affine_transform(diagonal_vals[i].get_value()),
                        sigmoid(affine_transform(diagonal_vals[i].get_value())),
                    )
                )

        diagonal_lines2 = VGroup(*[lines2[i * 4 + i] for i in range(4)])

        def update_diagonal_lines2(item):
            for i in range(4):
                item[i].put_start_and_end_on(
                    bias_ico.get_bottom(),
                    diagonal_dots[i].get_center(),
                )

        self.add(dns, diagonal_dots, diagonal_lines2)
        dns.add_updater(update_diagonal_nums)
        diagonal_dots.add_updater(update_diagonal_dots)
        diagonal_lines2.add_updater(update_diagonal_lines2)
        bce_loss.add_updater(
            lambda item: item.become(get_bce_loss(val_bce.get_value()))
        )

        self.playw(
            diagonal_vals[0].animate.set_value(4.7 + random.random() * 0.65),
            diagonal_vals[1].animate.set_value(4.7 + random.random() * 0.65),
            diagonal_vals[2].animate.set_value(4.7 + random.random() * 0.65),
            diagonal_vals[3].animate.set_value(4.7 + random.random() * 0.65),
            val_bce.animate.set_value(0.14),
            run_time=4,
        )


class ce_multigpu(InteractiveScene, Scene2D):
    def construct(self):

        ## gpus
        box_width, box_height = 8, 2.2
        gpu_box1 = Rectangle(width=box_width, height=box_height)
        gpu_txt1 = Text("GPU 1", font_size=18).align(gpu_box1, UL, buff=0.1)
        gpu1 = VGroup(gpu_box1, gpu_txt1)

        gpu_box2 = Rectangle(width=box_width, height=box_height)
        gpu_txt2 = Text("GPU 2", font_size=18).align(gpu_box2, UL, buff=0.1)
        gpu2 = VGroup(gpu_box2, gpu_txt2)

        gpus = VGroup(gpu1, gpu2).arrange(DOWN, buff=0.6).shift(UP * 0.5)

        self.playw(FadeIn(gpus))

        ## imgs, txts
        img1, img5, img7 = imgnet_samples("church", n=3).scale(0.2)
        img2, img6, img8 = imgnet_samples("springer", n=3).scale(0.2)
        img3 = imgnet_samples("truck", n=1).scale(0.2)
        img4 = imgnet_samples("parachute", n=1).scale(0.2)
        imgs1 = (
            Group(img1, img2, img3, img4)
            .arrange_in_grid(2, 2, h_buff=2.5, v_buff=0.1)
            .move_to(gpu1)
            .align(gpu1, LEFT, buff=0.8)
        )
        imgs2 = (
            Group(img5, img6, img7, img8)
            .arrange_in_grid(2, 2, h_buff=2.5, v_buff=0.1)
            .move_to(gpu2)
            .align(gpu2, LEFT, buff=0.8)
        )
        imgs = Group(*imgs1, *imgs2)

        txt1 = (
            Text("안개 속 음산한\n분위기의 교회", font_size=20)
            .next_to(imgs1[0], RIGHT, buff=0.2)
            .set_color(GREY_B)
        )
        txt2 = (
            Text("풀밭에 누워있는 강아지", font_size=20)
            .next_to(imgs1[1], RIGHT, buff=0.2)
            .set_color(GREY_B)
        )
        txt3 = (
            Text("어두운 배경 속\n푸른 트럭", font_size=20)
            .next_to(imgs1[2], RIGHT, buff=0.2)
            .set_color(GREY_B)
        )
        txt4 = (
            Text("맑은 하늘에\n낙하산을 편 사람", font_size=20)
            .next_to(imgs1[3], RIGHT, buff=0.2)
            .set_color(GREY_B)
        )
        txts1 = VGroup(txt1, txt2, txt3, txt4)
        txt5 = (
            Text("화창한 하늘 아래\n빨간 지붕의 교회", font_size=20)
            .next_to(imgs2[0], RIGHT, buff=0.2)
            .set_color(GREY_B)
        )
        txt6 = (
            Text("철제 테이블 다리 옆\n무심한 표정의 강아지", font_size=20)
            .next_to(imgs2[1], RIGHT, buff=0.2)
            .set_color(GREY_B)
        )
        txt7 = (
            Text("해안가 앞 언덕 위의\n작은 교회", font_size=20)
            .next_to(imgs2[2], RIGHT, buff=0.2)
            .set_color(GREY_B)
        )
        txt8 = (
            Text("사람이 내민 손 위에\n앞발을 올린 강아지", font_size=20)
            .next_to(imgs2[3], RIGHT, buff=0.2)
            .set_color(GREY_B)
        )
        txts2 = VGroup(txt5, txt6, txt7, txt8)
        txts = Group(*txts1, *txts2)

        self.playw(FadeIn(imgs1), FadeIn(txts1), FadeIn(imgs2), FadeIn(txts2))

        ## ce: inter-gpu
        self.play(Group(imgs[:2], imgs[3:]).animate.set_opacity(0.1))

        lines = VGroup(
            *[
                DashedLine(
                    imgs[2].get_center(),
                    txts[i].get_left(),
                    color=GREY_B,
                    dash_length=0.05,
                )
                for i in range(len(txts))
            ]
        )
        lines[4:].set_color(RED)
        self.playw(FadeIn(lines))

        ## if not ce
        explain = (
            Words("If not CLIP", font_size=24).to_edge(LEFT, buff=0.5).set_color(YELLOW_B)
        )
        self.playw(FadeIn(explain), FadeOut(lines), FadeOut(imgs), FadeOut(txts))

        imgs1.arrange_in_grid(2, 2, h_buff=2.5, v_buff=0.2).move_to(gpu1).align(
            gpu1, LEFT, buff=1.5
        )
        imgs2.arrange_in_grid(2, 2, h_buff=2.5, v_buff=0.2).move_to(gpu2).align(
            gpu2, LEFT, buff=1.5
        )
        imgs.set_opacity(1)

        label1 = Text("정답1", font_size=24).next_to(imgs[0], RIGHT, buff=0.5)
        label2 = Text("정답2", font_size=24).next_to(imgs[1], RIGHT, buff=0.5)
        label3 = Text("정답3", font_size=24).next_to(imgs[2], RIGHT, buff=0.5)
        label4 = Text("정답4", font_size=24).next_to(imgs[3], RIGHT, buff=0.5)

        label5 = Text("정답5", font_size=24).next_to(imgs[4], RIGHT, buff=0.5)
        label6 = Text("정답6", font_size=24).next_to(imgs[5], RIGHT, buff=0.5)
        label7 = Text("정답7", font_size=24).next_to(imgs[6], RIGHT, buff=0.5)
        label8 = Text("정답8", font_size=24).next_to(imgs[7], RIGHT, buff=0.5)

        labels = VGroup(label1, label2, label3, label4, label5, label6, label7, label8)
        self.playw(FadeIn(labels), FadeIn(imgs))

        ## surrounding rectangles
        rects = VGroup(
            *[
                SurroundingRectangle(
                    Group(imgs[i], labels[i]), color=YELLOW_B, buff=0.1, stroke_width=2
                )
                for i in range(len(imgs))
            ]
        )
        self.playw(FadeIn(rects))

        self.playwl(
            *[
                rects[i].animate(rate_func=there_and_back).set_fill(YELLOW, opacity=1)
                for i in range(len(rects))
            ],
            lag_ratio=0.3,
        )

        ## inter-gpu arrow

        arrow1 = (
            Arrow(gpu1.get_bottom(), gpu2.get_top(), buff=0.05, thickness=2)
            .shift(LEFT * 0.1)
            .set_color(YELLOW)
        )
        arrow2 = (
            Arrow(gpu2.get_top(), gpu1.get_bottom(), buff=0.05, thickness=2)
            .shift(RIGHT * 0.1)
            .set_color(YELLOW)
        )
        self.playw(GrowArrow(arrow1), GrowArrow(arrow2))

        ## Fadeout arrow, rects, labels, imgs
        self.play(
            FadeOut(arrow1),
            FadeOut(arrow2),
            FadeOut(rects),
            FadeOut(labels),
            FadeOut(imgs),
        )

        ## circumscribe explain and remove words[1]
        self.playw(
            Circumscribe(explain, color=YELLOW),
            explain.words[1].animate.set_opacity(0),
            VGroup(explain.words[0], explain.words[2]).animate.arrange(
                RIGHT, buff=0.07, aligned_edge=DOWN
            ).align(explain.words[0], DL, buff=0),
        )

        ## fade in imgs, txts
        imgs.shift(LEFT*0.7)
        self.playw(FadeIn(imgs1), FadeIn(txts1), FadeIn(imgs2), FadeIn(txts2))

        ## opacity 0.1 and lines
        self.play(
            Group(imgs[:2], imgs[3:]).animate.set_opacity(0.1),
            FadeIn(lines),
        )
        self.playw(
            *[line.animate(rate_func=there_and_back).set_stroke(width=8) for line in lines[4:]],
            wait=4
        )

        ## circumscribe imgs[2]

        self.playw(Circumscribe(imgs[2], color=PURE_RED))

        ## fadeout lines and explain -> siglip
        self.play(FadeOut(lines))
        explain2 = Words("If SigLIP", font_size=24).to_edge(LEFT, buff=0.5).set_color(YELLOW_B)

        self.playw(
            Circumscribe(explain2, color=YELLOW),
            Transform(explain.words[0], explain2.words[0]),
            Transform(explain.words[2][0], explain2.words[1][:3]),
            Transform(explain.words[2][1:], explain2.words[1][3:])
        )

        ## SigLIP is sample-wise OX quiz

        for i in range(4):
            self.play(Create(lines[i]), run_time=0.75)
            label = Text("O" if i == 2 else "X", font_size=24).set_color(GREEN if i == 2 else RED).move_to(lines[i])
            self.play(FadeOut(label, scale=2.5), FadeOut(lines[i].set_color(GREEN if i == 2 else RED), scale=1.2), run_time=0.75)
        self.wait()

        ## embedding shifted
        target_idx = [4, 5, 6, 7, 0, 1, 2, 3]
        self.playw(
            *[txts[i].animate.move_to(txts[tidx]).align_to(txts[tidx], LEFT) for i, tidx in enumerate(target_idx)]
        )

        self.embed()
        ## for 4, 5, 6, 7
        for i, tidx in enumerate(range(4, 8)):
            self.play(Create(lines[i].set_color(WHITE)), run_time=0.75)
            label = Text("X", font_size=24).set_color(RED).move_to(lines[i])
            self.play(FadeOut(label, scale=2.5), FadeOut(lines[i].set_color(RED), scale=1.2), run_time=0.75)


