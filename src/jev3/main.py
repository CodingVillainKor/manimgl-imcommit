from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        img = ImageMobject("jevlogo.png").scale(0.45)
        self.cf.save_state()
        self.cf.reorient(90, 50, -90, (-0.31, -0.41, 0.69), 3.89)
        self.addw(img)

        ## restore self.cf
        self.playw(self.cf.animate.restore(), rate_func=rush_from)


class introAttnSpan(InteractiveScene, Scene2D):
    def construct(self):

        ## llm box and text and input text
        llm_box = Rectangle(width=7, height=3.5, color=BLUE).shift(UP * 1.2)
        llm_text = Text("LLM", font_size=24).align(llm_box, UR, buff=0.1)
        llm = VGroup(llm_box, llm_text)
        input_text = Words(
            "state: 이영표를 부천의 가슴에 확실한 사람에 도장을 찍어 question: 노래 가사인가요?",
            font_size=24,
        )
        for w in input_text.words:
            w.rotate(PI / 2)
        input_text.words.arrange(RIGHT, buff=0.25, aligned_edge=UP).next_to(llm, DOWN)
        input_text.words[:-3].shift(LEFT * 0.2).set_color(GREEN_B)
        input_text.words[-3:].shift(RIGHT * 0.2).set_color(PURPLE_B)

        self.add(llm_box, llm_text, input_text)

        ## latent tensor

        latent = Tensor(
            len(input_text.words), arrange=RIGHT, shape="rectangle"
        ).move_to(llm)
        for i, l in enumerate(latent):
            l.set_x(input_text.words[i].get_x())
        self.add(latent)

        ## attn lines
        attn_lines = VGroup()
        cross_lines = VGroup()
        for i, l1 in enumerate(latent):
            for j, l2 in enumerate(latent):
                line = BrokenLine(
                    l1.get_top(),
                    VGroup(l1, l2).get_top()
                    + UP
                    * VGroup(l1, l2).get_width()
                    * 0.2
                    * (random.random() * 0.5 + 0.3),
                    l2.get_top(),
                    smooth=True,
                ).set_stroke(opacity=random.random() * 0.5)
                attn_lines.add(line)
                if i < 8 and j >= 8:
                    cross_lines.add(line)
                if i >= 8 and j < 8:
                    cross_lines.add(line)
        self.addw(attn_lines)

        ## masking matrix and disconnect attn
        mask_array = np.array(
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            ]
        )
        mask = IntegerMatrix(mask_array).scale(0.35).next_to(llm, RIGHT, buff=1.2)
        for i in range(7 * 11):
            if i % 11 < 8:
                mask[i].set_color(GREEN_B)
        for i in range(7 * 11, 10 * 11):
            if i % 11 >= 8:
                mask[i].set_color(PURPLE_B)
        self.playw(self.cf.animate.shift(RIGHT * 2), FadeIn(mask))

        ## fadeout cross lines
        zero_idxs = np.argwhere(mask_array == 0)
        idxs = [i * 11 + j for i, j in zero_idxs]
        mask_zeros = VGroup(*[mask[i] for i in idxs])
        self.playw(
            FadeOut(cross_lines, shift=UP * 0.5),
            mask_zeros.animate(rate_func=there_and_back).set_opacity(0),
        )


class AttentionSpan(InteractiveScene, Scene2D):
    def construct(self):
        ## attention span demonstration
        llm_box = Rectangle(width=7, height=3.5, color=BLUE).shift(UP * 1.2)
        llm_text = (
            Text("Attention", font_size=24)
            .align(llm_box, UR, buff=0.1)
            .set_color(GREY_A)
        )
        llm = VGroup(llm_box, llm_text)
        input_text = Words(
            "state: 가장 작은 여섯 자리 숫자는 100003 입니다 question: 100003은 소수인가요?",
            font_size=24,
        )
        for w in input_text.words:
            w.rotate(PI / 2)
        input_text.words.arrange(RIGHT, buff=0.25, aligned_edge=UP).next_to(llm, DOWN)
        input_text.words[:-3].shift(LEFT * 0.2).set_color(GREEN_B)
        input_text.words[-3:].shift(RIGHT * 0.2).set_color(PURPLE_B)
        self.cf.save_state()
        self.cf.reorient(-35, 68, 13, (2.80, 2.59, 0.18), 0.90)
        self.addw(llm_box, input_text, wait=2)
        self.playwl(*[FadeIn(c) for c in llm_text])

        ## latent tensor

        latent = Tensor(
            len(input_text.words), arrange=RIGHT, shape="rectangle"
        ).move_to(llm)
        for i, l in enumerate(latent):
            l.set_x(input_text.words[i].get_x())
        self.play(Restore(self.cf))
        self.playw(Transformr(input_text.words.copy(), latent))

        ## attention line
        attn_lines = VGroup()
        cross_lines = VGroup()
        for i, l1 in enumerate(latent):
            for j, l2 in enumerate(latent):
                line = BrokenLine(
                    l1.get_top(),
                    VGroup(l1, l2).get_top()
                    + UP
                    * VGroup(l1, l2).get_width()
                    * 0.2
                    * (random.random() * 0.5 + 0.35),
                    l2.get_top(),
                    smooth=True,
                ).set_stroke(opacity=random.random() * 0.5)
                attn_lines.add(line)
                if i < 8 and j >= 8:
                    cross_lines.add(line)
                if i >= 8 and j < 8:
                    cross_lines.add(line)
        attn_lines.shuffle()
        self.cf.save_state()
        self.play(
            self.cf.animate.reorient(-72, 34, 69, (-0.93, 1.26, -0.29), 2.90),
            run_time=0.75,
        )
        self.playwl(*[FadeIn(line) for line in attn_lines], run_time=10)

        ## cutting line
        line = Line(UP * 0.5, DOWN * 0.5).move_to(latent[7:9]).shift(UP * 0.5)
        self.playw(
            Circumscribe(line, buff=0),
            cross_lines.animate.set_opacity(0).set_color(PURE_RED),
        )

        ## restore self.cf
        self.play(Restore(self.cf), run_time=0.75)

        ## sr_state, sr_question
        sr_state = SurroundingRectangle(input_text.words[:8], color=RED, buff=0.15)
        sr_latent_state = SurroundingRectangle(latent[:8], color=RED, buff=0.15)
        slsc = sr_latent_state.copy()
        sr_latent_state.stretch_to_fit_height(1.25).align(slsc, DOWN, buff=0)
        sr_question = SurroundingRectangle(input_text.words[8:], color=RED, buff=0.15)
        sr_latent_question = SurroundingRectangle(latent[8:], color=RED, buff=0.15)
        slqc = sr_latent_question.copy()
        sr_latent_question.stretch_to_fit_height(0.85).align(slqc, DOWN, buff=0)
        self.play(
            FadeIn(sr_state),
            FadeIn(sr_question),
            FadeIn(sr_latent_state),
            FadeIn(sr_latent_question),
        )

        ## srs fill there and back
        self.play(
            VGroup(sr_question, sr_latent_question)
            .animate(rate_func=there_and_back)
            .set_fill(RED, opacity=1)
        )
        self.playw(
            VGroup(sr_state, sr_latent_state)
            .animate(rate_func=there_and_back)
            .set_fill(RED, opacity=1)
        )

        ## cut
        line = Line(UP * 0.75, DOWN * 0.75).move_to(latent[7:9]).shift(UP * 0.5)
        self.playw(
            Circumscribe(line, buff=0, color=RED),
            cross_lines.animate.set_opacity(0).set_color(PURE_RED),
        )

        ## mask
        mask_array = np.array(
            [
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            ]
        )
        mask = IntegerMatrix(mask_array).scale(0.35).next_to(llm, RIGHT, buff=1.2)
        for i in range(8 * 11):
            if i % 11 < 8:
                mask[i].set_color(GREEN_B)
        for i in range(8 * 11, 11 * 11):
            if i % 11 >= 8:
                mask[i].set_color(PURPLE_B)
        self.playw(self.cf.animate.shift(RIGHT * 2), FadeIn(mask), wait=0.5)

        ## span row and col
        lr, lc = latent.copy(), latent.copy()
        lr.generate_target().arrange(RIGHT).scale(0.9).rotate(-PI / 2).next_to(
            mask, LEFT
        )
        lc.generate_target().arrange(RIGHT, buff=0.18).scale(0.9).next_to(mask, UP)
        self.playw(MoveToTarget(lr), MoveToTarget(lc))

        ## zeros
        zero_idxs = np.argwhere(mask_array == 0)
        idxs = [i * 11 + j for i, j in zero_idxs]
        mask_zeros = VGroup(*[mask[i] for i in idxs])
        self.playw(mask_zeros.animate.set_fill(RED, opacity=1))

        ## span row col lines
        lines = VGroup()
        line_zeros = VGroup()
        lines_question = VGroup()
        for i in range(len(lr)):
            for j in range(len(lc)):
                line = BrokenLine(
                    lr[i].get_right(),
                    mask[i * len(lc) + j].get_center(),
                    lc[j].get_bottom(),
                    smooth=True,
                ).set_stroke(opacity=random.random() * 0.5 + 0.1)
                lines.add(line)
                if i < 8 and j >= 8:
                    line_zeros.add(line)
                if i >= 8 and j < 8:
                    line_zeros.add(line)
                if i >= 8 and j >= 8:
                    lines_question.add(line)
        lines.shuffle()
        self.playwl(
            self.cf.animate.reorient(90, 32, -90, (6.07, 1.30, 0.32), 5.28),
            *[FadeIn(line) for line in lines],
            run_time=2,
            wait=0.5,
        )
        ## fadeout zeros
        self.playwl(*[FadeOut(line) for line in line_zeros], run_time=2, wait=0.5)

        ## increse distance
        idx = 8
        lrq = lr[idx:]
        lcs = lc[idx:]
        lrq.generate_target(), lcs.generate_target(), lines_question.generate_target()
        lrq.target.shift(DOWN * 0.8)
        lcs.target.shift(RIGHT * 0.8)
        for i, line in enumerate(lines_question.target):
            line.become(
                BrokenLine(
                    lrq.target[i // 3].get_right(),
                    mask[(i // 3 + 8) * len(lc) + (i % 3 + 8)].get_center(),
                    lcs.target[i % 3].get_bottom(),
                    smooth=True,
                ).set_stroke(opacity=random.random() * 0.5 + 0.1)
            )

        self.playw(
            MoveToTarget(lrq),
            MoveToTarget(lcs),
            MoveToTarget(lines_question),
            self.cf.animate.reorient(88, 31, -88, (6.03, 0.57, 0.33), 7.03),
        )


class causalMasking(InteractiveScene, Scene2D):
    def construct(self):

        ## masking
        llm_box = Rectangle(width=7, height=3.5, color=BLUE).shift(UP * 1.2)
        llm_text = (
            Text("Attention", font_size=24)
            .align(llm_box, UR, buff=0.1)
            .set_color(GREY_A)
        )
        llm = VGroup(llm_box, llm_text)
        input_text = Words(
            "[Assistant] You are a helpful assistant. [User] 혹시 piui가 뭐야? [Response]",
            font_size=24,
        ).set_opacity(0.4)
        for w in input_text.words:
            w.rotate(PI / 2)
        input_text.words.arrange(RIGHT, buff=0.25, aligned_edge=UP).next_to(llm, DOWN)

        latent = Tensor(
            len(input_text.words), arrange=RIGHT, shape="rectangle"
        ).move_to(llm)
        for i, l in enumerate(latent):
            l.set_x(input_text.words[i].get_x())
        self.cf.save_state()
        self.cf.shift(RIGHT * 2)
        mask_array = np.tril(np.ones((len(input_text.words), len(input_text.words))))
        mask = IntegerMatrix(mask_array).scale(0.35).next_to(llm, RIGHT, buff=1.2)
        zero_idx = np.where(mask_array == 0)
        one_idx = np.where(mask_array == 1)
        for i, j in zip(*zero_idx):
            mask[i * len(input_text.words) + j].set_color(RED_B)
        for i, j in zip(*one_idx):
            mask[i * len(input_text.words) + j].set_color(GREEN_B)

        lr, lc = latent.copy(), latent.copy()
        lr.arrange(RIGHT).scale(0.9).rotate(-PI / 2).next_to(mask, LEFT)
        lc.arrange(RIGHT, buff=0.18).scale(0.9).next_to(mask, UP)
        cm_text = Text("Causal Masking", font_size=24).next_to(mask, DOWN)
        qt = Text("Query", font_size=20).next_to(lr, DOWN, buff=0.1)
        kt = Text("Key", font_size=20).next_to(lc, LEFT, buff=0.1)

        self.add(llm_box, input_text, latent, mask, lr, lc, cm_text, qt, kt)
        ## lines4
        lines4 = VGroup()
        for j in range(4 + 1):
            line = BrokenLine(
                lr[4].get_right(),
                mask[4 * len(input_text.words) + j].get_center(),
                lc[j].get_bottom(),
                smooth=True,
            ).set_stroke(opacity=random.random() * 0.5 + 0.3, color=GREEN)
            lines4.add(line)
        mask.generate_target()
        mask.target[: 4 * len(input_text.words)].set_opacity(0.1)
        mask.target[5 * len(input_text.words) :].set_opacity(0.1)
        self.play(
            self.cf.animate.reorient(-90, 42, 90, (7.53, 0.85, 1.22), 6.66),
            MoveToTarget(mask),
            run_time=0.75,
        )
        self.playwl(*[Create(line) for line in lines4], lag_ratio=0.5)

        ## lines4 future
        lines4f = VGroup()
        for j in range(4 + 1, len(input_text.words)):
            line = BrokenLine(
                lr[4].get_right(),
                mask[4 * len(input_text.words) + j].get_center(),
                lc[j].get_bottom(),
                smooth=True,
            ).set_stroke(opacity=random.random() * 0.5 + 0.3, color=RED)
            lines4f.add(line)
        self.playwl(
            *[Succession(Create(line), FadeOut(line)) for line in lines4f],
            lag_ratio=0.1,
        )

        ## restore self.cf and fadeout all about masking
        self.play(
            self.cf.animate.restore(),
            FadeOut(mask),
            FadeOut(lines4),
            FadeOut(lr),
            FadeOut(lc),
            FadeOut(cm_text),
            FadeOut(qt),
            FadeOut(kt),
        )

        ## all linked attn
        lines_all = VGroup()
        for i in range(len(input_text.words)):
            for j in range(len(input_text.words)):
                if i <= j:
                    continue
                line = (
                    BrokenLine(
                        latent[i].get_top(),
                        (latent[i].get_top() + latent[j].get_top()) / 2
                        + UP * (random.random() * 0.9 + 0.1),
                        latent[j].get_top(),
                        smooth=True,
                    )
                    .set_stroke(
                        opacity=random.random() * 0.5 + 0.1, color=BLUE, width=1
                    )
                    .add_tip(length=0.1, width=0.1)
                )
                lines_all.add(line)
        lines_future = VGroup()
        for i in range(len(input_text.words)):
            for j in range(len(input_text.words)):
                if i >= j:
                    continue
                line = (
                    BrokenLine(
                        latent[i].get_bottom(),
                        (latent[i].get_bottom() + latent[j].get_bottom()) / 2
                        + DOWN * (random.random() * 0.9 + 0.1),
                        latent[j].get_bottom(),
                        smooth=True,
                    )
                    .set_stroke(opacity=random.random() * 0.5 + 0.1, color=RED, width=1)
                    .add_tip(length=0.1, width=0.1)
                )
                lines_future.add(line)
        lines_all.shuffle()
        lines_future.shuffle()
        self.playwl(*[Create(line) for line in lines_all], lag_ratio=0.1, run_time=3)
        self.playwl(*[Create(line) for line in lines_future], lag_ratio=0.1, run_time=3)


class nomask(InteractiveScene, Scene2D):
    def construct(self):
        ## 심지어
        llm_box = Rectangle(width=8, height=3.5, color=BLUE).shift(UP * 1.2)
        llm_text = (
            Text("Attention", font_size=24)
            .align(llm_box, UR, buff=0.1)
            .set_color(GREY_A)
        )
        llm = VGroup(llm_box, llm_text)
        input_text = Words(
            "[state] it is state [qustion1] first question [qustion2] second question",
            font_size=24,
        )
        for w in input_text.words:
            w.rotate(PI / 2)
        input_text.words.arrange(RIGHT, buff=0.25, aligned_edge=UP).next_to(llm, DOWN)
        input_text.words[:4].set_color(YELLOW_B)
        input_text.words[4:7].set_color(RED_B)
        input_text.words[7:10].set_color(GREEN_B)

        latent = Tensor(
            len(input_text.words), arrange=RIGHT, shape="rectangle"
        ).move_to(llm)
        for i, l in enumerate(latent):
            l.set_x(input_text.words[i].get_x())

        self.addw(llm_box, input_text.words[:10], latent[:10])

        ## bidirectional connections
        lines_all = VGroup()
        all3 = VGroup()
        for i in range(len(input_text.words)):
            for j in range(len(input_text.words)):
                if i <= j:
                    continue
                line = (
                    BrokenLine(
                        latent[i].get_top(),
                        (latent[i].get_top() + latent[j].get_top()) / 2
                        + UP * (random.random() * 0.9 + 0.1),
                        latent[j].get_top(),
                        smooth=True,
                    )
                    .set_stroke(
                        opacity=random.random() * 0.5 + 0.1, color=BLUE, width=1
                    )
                    .add_tip(length=0.1, width=0.1)
                )
                if i > len(input_text.words) - 4:
                    all3.add(line)
                else:
                    lines_all.add(line)
        lines_future = VGroup()
        future3 = VGroup()
        for i in range(len(input_text.words)):
            for j in range(len(input_text.words)):
                if i >= j:
                    continue
                line = (
                    BrokenLine(
                        latent[i].get_bottom(),
                        (latent[i].get_bottom() + latent[j].get_bottom()) / 2
                        + DOWN * (random.random() * 0.9 + 0.1),
                        latent[j].get_bottom(),
                        smooth=True,
                    )
                    .set_stroke(opacity=random.random() * 0.5 + 0.1, color=RED, width=1)
                    .add_tip(length=0.1, width=0.1)
                )
                if j > len(input_text.words) - 4:
                    future3.add(line)
                else:
                    lines_future.add(line)
        lines_all.shuffle()
        lines_future.shuffle()
        self.playwl(
            *[
                AnimationGroup(Create(line1), Create(line2))
                for line1, line2 in zip(lines_all, lines_future)
            ],
            lag_ratio=0.1,
            run_time=3,
        )
        ## fadein and out
        self.playw(
            FadeIn(VGroup(input_text.words[10:], latent[10:], all3, future3)), wait=1.5
        )
        self.playw(
            FadeOut(VGroup(input_text.words[10:], latent[10:], all3, future3)), wait=1.5
        )

        ## indicate question1, latent 1
        sr_w1 = SurroundingRectangle(input_text.words[4:7])
        sr_l1 = SurroundingRectangle(latent[4:7], buff=0.2)
        self.playw(Create(sr_w1), Create(sr_l1), wait=1.5)


class posEnc(InteractiveScene, Scene2D):
    def construct(self):

        ## positional encoding
        llm_box = Rectangle(width=8, height=3.5, color=BLUE).shift(UP * 1.2)
        llm_text = (
            Text("Attention", font_size=24)
            .align(llm_box, UR, buff=0.1)
            .set_color(GREY_A)
        )
        llm = VGroup(llm_box, llm_text)
        input_text = Words(
            "[state] it is state [qustion1] first question [qustion2] second question",
            font_size=24,
        )
        for w in input_text.words:
            w.rotate(PI / 2)
        input_text.words.arrange(RIGHT, buff=0.25, aligned_edge=UP).next_to(llm, DOWN)
        input_text.words[:4].set_color(YELLOW_B)
        input_text.words[4:7].set_color(RED_B)
        input_text.words[7:10].set_color(GREEN_B)

        latent = (
            Tensor(len(input_text.words), arrange=RIGHT, shape="rectangle")
            .move_to(llm)
            .shift(DOWN * 0.5)
        )
        for i, l in enumerate(latent):
            l.set_x(input_text.words[i].get_x())

        pe = (
            Tensor(len(input_text.words), arrange=RIGHT, shape="circle")
            .next_to(latent, UP)
            .set_color_by_gradient(ORANGE, PURPLE_D)
        )
        for i, pt in enumerate(pe):
            pt.scale(0.5).set_stroke(color=GREY_A, width=1)
            pt.set_x(input_text.words[i].get_x())

        pluses = VGroup(
            *[
                Text("+", font_size=20).move_to(
                    (latent[i].get_top() + pe[i].get_bottom()) / 2
                )
                for i in range(len(input_text.words))
            ]
        )

        self.addw(llm_box, input_text.words, latent)
        ## fade in pluses and pe
        pe_text = Words("Positional Encoding", font_size=20)
        pe_text.words.arrange(DOWN, aligned_edge=LEFT, buff=0.05).next_to(
            pe, RIGHT, aligned_edge=UP
        )
        self.playw(FadeIn(VGroup(pluses, pe, pe_text)))

        ## abbreviate positional encoding as PE
        pe_text.generate_target()
        pe_text.target.set_opacity(0)
        VGroup(pe_text.target.words[0][0], pe_text.target.words[1][0]).set_opacity(
            1
        ).arrange(RIGHT, buff=0.05).next_to(pe, RIGHT, aligned_edge=UP)
        self.playw(MoveToTarget(pe_text))

        ## pop up the PE circles
        self.playwl(
            *[c.animate(rate_func=there_and_back).shift(UP * 0.5) for c in pe],
            lag_ratio=0.4,
            wait=0.5,
        )

        ## [0] ~ [len(input_text.words) - 1])]
        texts = VGroup(
            *[
                Text(f"[{i}]", font_size=20).next_to(pe[i], UP)
                for i in range(len(input_text.words))
            ]
        )
        self.playwl(*[FadeIn(t) for t in texts], lag_ratio=0.1, wait=1.5)

        ## sr q1, q2
        sr_q1 = SurroundingRectangle(input_text.words[4:7], color=RED_B, buff=0.1)
        sr_l1 = SurroundingRectangle(latent[4:7], color=RED_B, buff=0.1)
        sr_q2 = SurroundingRectangle(input_text.words[7:10], color=GREEN_B, buff=0.1)
        sr_l2 = SurroundingRectangle(latent[7:10], color=GREEN_B, buff=0.1)
        self.play(FadeIn(sr_q1), FadeIn(sr_l1))
        self.playw(FadeIn(sr_q2), FadeIn(sr_l2))

        ## state at first
        self.playwl(
            *[
                VGroup(input_text.words[i], texts[i])
                .animate(rate_func=there_and_back)
                .shift(UP * 0.5)
                for i in range(4)
            ],
            lag_ratio=0.5,
            wait=0.5,
        )

        ## q1, q2 start after state
        pe_q2 = texts[4:7].copy()
        self.playw(pe_q2.animate.shift(UP * 0.5))
        self.playw(
            FadeOut(texts[7:], shift=RIGHT * 2), pe_q2.animate.move_to(texts[7:])
        )

        ## 4, 5, 6
        self.playwl(
            *[
                VGroup(texts[i + 4], pe_q2[i])
                .animate(rate_func=there_and_back)
                .shift(UP * 0.5)
                for i in range(3)
            ],
            lag_ratio=0.8,
            wait=2.5,
        )

        ## a, b
        q1 = VGroup(
            texts[4:7],
            pe[4:7],
            pluses[4:7],
            latent[4:7],
            input_text.words[4:7],
            sr_q1,
            sr_l1,
        )
        q2 = VGroup(
            pe_q2,
            pe[7:10],
            pluses[7:10],
            latent[7:10],
            input_text.words[7:10],
            sr_q2,
            sr_l2,
        )
        self.play(FadeOut(q1))
        self.playw(FadeOut(q2), FadeIn(q1))
        q1c = q1.copy().set_opacity(0)
        q2c = q2.copy().set_opacity(0)
        ## swap q1 and q2 positions
        self.play(FadeIn(q2), run_time=0.5)
        self.playw(
            q1.animate(path_arc=PI).move_to(q2c), q2.animate(path_arc=PI).move_to(q1c)
        )

        ## fadeout the contents in the llm
        llm_contents = VGroup(
            pe, texts[:7], pe_q2, pluses, latent, sr_l1, sr_l2, pe_text, llm
        )
        state = input_text.words[:4]
        qa = input_text.words[4:7]
        qb = input_text.words[7:10]

        state2 = state.copy()
        qa2 = qa.copy()
        qb2 = qb.copy()

        state3 = state.copy()
        qa3 = qa.copy()
        qb3 = qb.copy()

        state4 = state.copy()
        qa4 = qa.copy()
        qb4 = qb.copy()

        sq1 = VGroup(state, qa)
        sq2 = VGroup(state2, qb2)
        sq3 = VGroup(state3, qa3, qb3)
        sq4 = VGroup(state4, qb4, qa4)

        sq1.generate_target().arrange(RIGHT, aligned_edge=UP, buff=0.3)
        sq2.generate_target().arrange(RIGHT, aligned_edge=UP, buff=0.3)
        sq3.generate_target().arrange(RIGHT, aligned_edge=UP, buff=0.3)
        sq4.generate_target().arrange(RIGHT, aligned_edge=UP, buff=0.3)
        VGroup(sq1.target, sq2.target, sq3.target, sq4.target).arrange_in_grid(n_rows=2, n_cols=2, buff=1.25, aligned_edge=LEFT).shift(UP * 0.75)

        sr_q1.add_updater(lambda m: m.surround(qa, buff=0.1))
        sr_q2.add_updater(lambda m: m.surround(qb, buff=0.1))
        self.playw(
            FadeOut(llm_contents, shift=UP),
            VGroup(qb, sr_q2).animate.set_opacity(0),
            MoveToTarget(sq1),
            wait=0.2,
        )
        sq2.move_to(sq2.target)
        sq2[1].set_opacity(0)
        sr2_q2 = SurroundingRectangle(sq2[1], buff=0.1, color=GREEN)
        self.playw(
            MoveToTarget(sq2),
            FadeIn(sr2_q2),
            wait=0.3
        )

        ## q3
        sq3.arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(sq3.target)
        sq3[1:].set_opacity(0)
        sr3_q1 = SurroundingRectangle(sq3[1], buff=0.1, color=RED)
        sr3_q2 = SurroundingRectangle(sq3[2], buff=0.1, color=GREEN)
        self.playw(
            MoveToTarget(sq3),
            FadeIn(sr3_q1),
            FadeIn(sr3_q2),
            wait=0.3
        )

        ## q4
        sq4.arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(sq4.target)
        sq4[1:].set_opacity(0)
        sr4_q1 = SurroundingRectangle(sq4[1], buff=0.1, color=RED)
        sr4_q2 = SurroundingRectangle(sq4[2], buff=0.1, color=GREEN)
        self.playw(
            MoveToTarget(sq4),
            FadeIn(sr4_q1),
            FadeIn(sr4_q2),
        )

        ## incrementally ranging 1 by 1 pe
        query1 = VGroup(*state, *qa)
        query2 = VGroup(*state2, *qb2)
        query3 = VGroup(*state3, *qa3, *qb3)
        query4 = VGroup(*state4, *qb4, *qa4)
        pe1 = VGroup(*[Text(f"[{i}]", font_size=20).next_to(query1[i], UP, buff=0.2) for i in range(len(state) + len(qa))])
        pe2 = VGroup(*[Text(f"[{i}]", font_size=20).next_to(query2[i], UP, buff=0.2) for i in range(len(state2) + len(qb2))])
        pe3 = VGroup(*[Text(f"[{i}]", font_size=20).next_to(query3[i], UP, buff=0.2) for i in range(len(state3) + len(qa3) + len(qb3))])
        pe4 = VGroup(*[Text(f"[{i}]", font_size=20).next_to(query4[i], UP, buff=0.2) for i in range(len(state4) + len(qb4) + len(qa4))])
        self.playw(
            *[FadeIn(pe, shift=UP*0.3) for pe in [pe1, pe2, pe3, pe4]],
        )

        self.embed()
        ## pop pes
        anim1 = AnimationGroup(*[pe1[i].animate(rate_func=there_and_back).shift(UP*0.3) for i in range(len(pe1))], lag_ratio=0.5)
        anim2 = AnimationGroup(*[pe2[i].animate(rate_func=there_and_back).shift(UP*0.3) for i in range(len(pe2))], lag_ratio=0.5)
        anim3 = AnimationGroup(*[pe3[i].animate(rate_func=there_and_back).shift(UP*0.3) for i in range(len(pe3))], lag_ratio=0.5)
        anim4 = AnimationGroup(*[pe4[i].animate(rate_func=there_and_back).shift(UP*0.3) for i in range(len(pe4))], lag_ratio=0.5)
        self.playw(anim1, anim2, anim3, anim4, wait=2)