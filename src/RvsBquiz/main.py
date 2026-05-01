from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        r1, r2, r3 = [
            Circle(radius=0.3).set_stroke(GREY, width=1.5).set_fill(RED, opacity=0.5)
            for _ in range(3)
        ]
        b1, b2, b3 = [
            Circle(radius=0.3).set_stroke(GREY, width=1.5).set_fill(BLUE, opacity=0.5)
            for _ in range(3)
        ]
        rs, bs = VGroup(r1, r2, r3), VGroup(b1, b2, b3)
        rs.arrange(RIGHT, buff=0.5)
        bs.arrange(RIGHT, buff=0.5)
        VGroup(rs, bs).arrange(DOWN, buff=0.75)

        self.play(FadeIn(rs))
        self.playw(FadeIn(bs))

        self.playw(
            *[Indicate(r, color=PURE_RED) for r in rs],
            *[Indicate(b, color=PURE_BLUE) for b in bs],
        )

        ## 빨간 공을 R, 파란 공을 B라고 할게요

        get_r_label = lambda: Text(f"R", font_size=24).set_color(RED)
        get_b_label = lambda: Text(f"B", font_size=24).set_color(BLUE)

        rl1, rl2, rl3 = [get_r_label().move_to(r) for r in rs]
        bl1, bl2, bl3 = [get_b_label().move_to(b) for b in bs]
        self.play(*[FadeIn(rl) for rl in [rl1, rl2, rl3]])
        self.playw(*[FadeIn(bl) for bl in [bl1, bl2, bl3]])

        ## 이 공들을 RR, RB, BB 이렇게 세 그룹으로 나눕니다
        r1, r2, r3 = VGroup(r1, rl1), VGroup(r2, rl2), VGroup(r3, rl3)
        b1, b2, b3 = VGroup(b1, bl1), VGroup(b2, bl2), VGroup(b3, bl3)
        g1 = VGroup(r1, r2)
        g2 = VGroup(r3, b1)
        g3 = VGroup(b2, b3)
        g1.generate_target()
        g2.generate_target()
        g3.generate_target()
        g1.target.arrange(RIGHT, buff=0.25)
        g2.target.arrange(RIGHT, buff=0.25)
        g3.target.arrange(RIGHT, buff=0.25)
        VGroup(g1.target, g2.target, g3.target).arrange(RIGHT, buff=0.75)
        self.playwl(MoveToTarget(g1), MoveToTarget(g2), MoveToTarget(g3), lag_ratio=0.9)

        ## 각 그룹을 세 개의 상자에 각각 넣고 나서요

        box1, box2, box3 = [
            Rectangle(width=2, height=1)
            .set_fill(GREY_D, opacity=1)
            .set_stroke(GREY, width=1.5)
            for _ in range(3)
        ]
        box1.move_to(g1).shift(OUT * 0.01)
        box2.move_to(g2).shift(OUT * 0.01)
        box3.move_to(g3).shift(OUT * 0.01)
        self.play(FadeIn(box1), run_time=0.5)
        self.play(FadeIn(box2), run_time=0.5)
        self.playw(FadeIn(box3), run_time=0.5)

        ## 구별을 못하게 서로 섞습니다
        self.remove(g1, g2, g3)
        boxes = VGroup(box1, box2, box3)
        self.playw(boxes.animate.shift(UP * 10))

        self.playw(boxes.animate.shift(DOWN * 10))

        # 이제 여기서 문제는 이겁니다: skip
        self.wait(1.5)
        ## 셋 중에서 공을 하나 뽑았더니 빨간 색이 나왔을 때,
        g1.move_to(box3)
        g2.move_to(box1)
        g3.move_to(box2)
        g3, g1, g2 = g1, g2, g3
        g30 = g3[0]
        box3.set_z_index(1)
        self.add(box3)
        self.playw(g30.animate.shift(UP))
        self.embed()

        ## 이 때, 그 상자에서 뽑은 나머지 공도 빨간 색일 확률은 몇일까요?

        arrow = Arrow(
            g3[1].get_top() + UP * 1.5, g3[1].get_top() + UP * 0.2, thickness=2
        )
        self.playw(GrowArrow(arrow))


class solution(InteractiveScene, Scene2D):
    def construct(self):

        ## RR 상자를 골랐거나, RB 상자를 골랐거나 ... 이 조건이었습니다
        r1, r2, r3 = [
            Circle(radius=0.3).set_stroke(GREY, width=1.5).set_fill(RED, opacity=0.5)
            for _ in range(3)
        ]
        b1, b2, b3 = [
            Circle(radius=0.3).set_stroke(GREY, width=1.5).set_fill(BLUE, opacity=0.5)
            for _ in range(3)
        ]
        rl1, rl2, rl3 = [
            Text(f"R", font_size=24).set_color(RED).move_to(r) for r in [r1, r2, r3]
        ]
        bl1, bl2, bl3 = [
            Text(f"B", font_size=24).set_color(BLUE).move_to(b) for b in [b1, b2, b3]
        ]
        r1, r2, r3 = VGroup(r1, rl1), VGroup(r2, rl2), VGroup(r3, rl3)
        rs, bs = VGroup(r1, r2, r3), VGroup(b1, b2, b3)
        g1 = VGroup(r1, r2)
        g2 = VGroup(r3, b1)
        g3 = VGroup(b2, b3)
        g1.arrange(RIGHT, buff=0.25)
        g2.arrange(RIGHT, buff=0.25)
        g3.arrange(RIGHT, buff=0.25)
        VGroup(g1, g2, g3).arrange(RIGHT, buff=0.75)
        box1 = (
            Rectangle(width=2, height=1)
            .set_fill(GREY_D, opacity=1)
            .set_stroke(GREY, width=1.5)
        )
        box2 = (
            Rectangle(width=2, height=1)
            .set_fill(GREY_D, opacity=1)
            .set_stroke(GREY, width=1.5)
        )
        box3 = (
            Rectangle(width=2, height=1)
            .set_fill(GREY_D, opacity=1)
            .set_stroke(GREY, width=1.5)
        )
        box1.move_to(g1).shift(OUT * 0.01)
        box2.move_to(g2).shift(OUT * 0.01)
        box3.move_to(g3).shift(OUT * 0.01)

        g1.move_to(box3)
        g2.move_to(box1)
        g3.move_to(box2)
        box1, box2, box3 = box3, box1, box2
        r1.shift(UP)

        self.addw(box1, box2, box3, r1)

        rrq_vs_rbq = (
            Words("RR or RB", font=MONO_FONT, font_size=24)
            .next_to(box1, DOWN)
            .set_color(YELLOW_B)
        )
        self.playwl(*[FadeIn(w) for w in rrq_vs_rbq.words], lag_ratio=0.9)
        x = (
            Text(X_STRING, font_size=24, font="Noto Sans")
            .next_to(rrq_vs_rbq, RIGHT)
            .set_color(RED)
        )
        self.playw(FadeIn(x))
        picked_red = (
            Words("Red picked", font="Noto Sans KR", font_size=24)
            .next_to(rrq_vs_rbq, DOWN, aligned_edge=LEFT)
            .set_color(YELLOW_B)
        )
        self.playwl(*[FadeIn(w) for w in picked_red.words], lag_ratio=0.99)
        c = (
            Text(CHECK_STRING, font_size=24, font="Noto Sans")
            .next_to(picked_red, RIGHT)
            .set_color(GREEN)
        )
        self.playw(FadeIn(c))

        ## 이 조건이 RR 상자와 RB 상자 두 경우를 각각 다른 가중치로 만듭니다

        self.playw(FlashAround(rrq_vs_rbq.words[0], color=GREEN))
        self.playw(FlashAround(rrq_vs_rbq.words[-1], color=GREEN))

        ## 이게 무슨 말일까요? 한 번 볼게요
        w1, w2 = rrq_vs_rbq, picked_red
        self.playwl(
            AnimationGroup(
                FadeOut(box1),
                FadeOut(box2),
                FadeOut(box3),
                FadeOut(r1),
                FadeOut(x),
                FadeOut(c),
            ),
            VGroup(w1, w2).animate.scale(1.5).arrange(RIGHT, buff=3).shift(UP * 2.5),
            lag_ratio=0.7,
        )

        ## 아까 이야기 했던 ... RB 상자를 고를 경우
        self.playw(w2.animate.set_opacity(0.3))

        ## 이 경우는 문제의 조건보다 더 넓은 조건입니다

        r1, r2, r3 = [
            Circle(radius=0.3).set_stroke(GREY, width=1.5).set_fill(RED, opacity=0.5)
            for _ in range(3)
        ]
        b1, b2, b3 = [
            Circle(radius=0.3).set_stroke(GREY, width=1.5).set_fill(BLUE, opacity=0.5)
            for _ in range(3)
        ]
        r1r2 = VGroup(r1, r2).arrange(RIGHT, buff=0.25)
        r3b1 = VGroup(r3, b1).arrange(RIGHT, buff=0.25)
        VGroup(r1r2, r3b1).arrange(RIGHT, buff=0.75).next_to(w1, DOWN, buff=2.5)
        self.playw(FadeIn(r1r2))
        self.playw(FadeIn(r3b1))

        ## 왜냐하면 RB 상자에서는 B를 고르는 경우를 포함하고 있기 때문입니다

        self.playw(FlashAround(r3b1, color=RED))
        arr = Arrow(b1.get_top() + UP * 1.3, b1.get_top(), thickness=2).set_color(
            PURE_RED
        )
        self.playw(GrowArrow(arr))

        ## 여기서 문제의 조건인 ... 로 줄이려면요
        self.play(w2.animate.set_opacity(1))
        self.playw(FlashAround(w2, color=GREEN))

        ## RR 상자를 고를 경우에서는 ... R을 뽑은 경우,
        self.playwl(Indicate(r1, color=RED), Indicate(r2, color=RED), lag_ratio=0.7)

        self.play(FadeOut(arr))
        self.playwl(Indicate(r3, color=RED), b1.animate.set_opacity(0.1), lag_ratio=0.9)
        self.embed()

        ## 즉 RB 상자 경우에서는 절반으로 줄여야합니다
        box2 = (
            Rectangle(width=2, height=1)
            .set_fill(GREY_D, opacity=0)
            .set_stroke(GREY, width=1.5)
            .move_to(r3b1)
        )
        self.playw(FadeIn(box2))

        c1, c2, c3 = r1.copy(), r2.copy(), r3.copy()
        self.playw(VGroup(c1, c2, c3).animate.next_to(w2, DOWN, buff=2.5))

        ## 그래서 이 조건을 두고 ... 다시 계산해보면은요

        self.playw(
            FadeOut(w1, shift=LEFT * 2.5),
            FadeOut(VGroup(r1, r2, r3, b1, box2), shift=LEFT * 2.5),
            w2.animate.move_to(ORIGIN).align_to(w2, UP),
            VGroup(c1, c2, c3).animate.move_to(ORIGIN).align_to(c1, UP),
        )
        check1, check2 = (
            Text(CHECK_STRING, font_size=24, font="Noto Sans")
            .set_color(GREEN)
            .next_to(c1, DOWN),
            Text(CHECK_STRING, font_size=24, font="Noto Sans")
            .set_color(GREEN)
            .next_to(c2, DOWN),
        )
        x1 = (
            Text(X_STRING, font_size=24, font="Noto Sans")
            .set_color(RED)
            .next_to(c3, DOWN)
        )
        self.play(
            FadeIn(check1),
            FadeIn(check2),
        )
        self.playw(FadeIn(x1))


class solution2(InteractiveScene, Scene2D):
    def construct(self):
        ## R1, ... B3로 두면 됩니다
        r1, r2, r3 = [
            Circle(radius=0.3).set_stroke(GREY, width=1.5).set_fill(RED, opacity=0.5)
            for _ in range(3)
        ]
        b1, b2, b3 = [
            Circle(radius=0.3).set_stroke(GREY, width=1.5).set_fill(BLUE, opacity=0.5)
            for _ in range(3)
        ]
        rl1, rl2, rl3 = [
            Text(f"R{i}", font_size=24).set_color(RED).move_to(r)
            for i, r in enumerate([r1, r2, r3], start=1)
        ]
        bl1, bl2, bl3 = [
            Text(f"B{i}", font_size=24).set_color(BLUE).move_to(b)
            for i, b in enumerate([b1, b2, b3], start=1)
        ]
        r1, r2, r3 = VGroup(r1, rl1), VGroup(r2, rl2), VGroup(r3, rl3)
        b1, b2, b3 = VGroup(b1, bl1), VGroup(b2, bl2), VGroup(b3, bl3)
        rs, bs = VGroup(r1, r2, r3), VGroup(b1, b2, b3)
        r1r2 = VGroup(r1, r2).arrange(RIGHT, buff=0.25)
        r3b1 = VGroup(r3, b1).arrange(RIGHT, buff=0.25)
        b2b3 = VGroup(b2, b3).arrange(RIGHT, buff=0.25)
        VGroup(r1r2, r3b1, b2b3).arrange(RIGHT, buff=0.75)

        self.playwl(*[FadeIn(item) for item in [r1, r2, r3, b1, b2, b3]], lag_ratio=0.8)

        ## 그래서 상자를 R1R2, R3B1, B2B3 상자라고 했을 때
        box1 = Rectangle(width=2, height=1).set_stroke(GREY, width=1.5).move_to(r1r2)
        box2 = Rectangle(width=2, height=1).set_stroke(GREY, width=1.5).move_to(r3b1)
        box3 = Rectangle(width=2, height=1).set_stroke(GREY, width=1.5).move_to(b2b3)
        self.add(r1, r2, r3, b1, b2, b3)
        self.play(FadeIn(box1), run_time=0.5)
        self.play(FadeIn(box2), run_time=0.5)
        self.playw(FadeIn(box3), run_time=0.5)

        ## R1, R2, R3 중에 하나를 뽑는게 조건이죠?
        condition_text = (
            Words("조건: 하나를 뽑았더니 빨강이다", font_size=24)
            .next_to(box2, DOWN, buff=0.5)
            .set_color(GREY_B)
        )
        condition_text[-4:-2].set_color(RED)
        self.playwl(*[FadeIn(w) for w in condition_text.words], lag_ratio=0.5, wait=0)
        self.playw(VGroup(b1, b2, b3).animate.set_opacity(0.1))

        ## 그런데 각 경우에 나머지 ... 고정적으로 정해집니다
        r1c, r2c, r3c = r1.copy(), r2.copy(), r3.copy()
        r2cc, r1cc, b1cc = r2.copy(), r1.copy(), b1.copy()
        conds = VGroup(r1c, r2c, r3c)
        results = VGroup(r2cc, r1cc, b1cc)
        for item in VGroup(*conds, *results):
            item.generate_target()
        VGroup(r1c.target, r2c.target, r3c.target).arrange(DOWN, buff=0.25).next_to(
            r1, UP, buff=0.4
        )
        VGroup(r2cc.target, r1cc.target, b1cc.target).arrange(DOWN, buff=0.25).next_to(
            VGroup(r1c.target, r2c.target, r3c.target), RIGHT, buff=1
        )
        ccx = VGroup(
            *[
                Text(CHECK_STRING, font_size=24, font="Noto Sans")
                .set_color(GREEN)
                .next_to(r2cc.target, RIGHT),
                Text(CHECK_STRING, font_size=24, font="Noto Sans")
                .set_color(GREEN)
                .next_to(r1cc.target, RIGHT),
                Text(X_STRING, font_size=24, font="Noto Sans")
                .set_color(RED)
                .next_to(b1cc.target, RIGHT),
            ]
        )
        arrs = VGroup()
        for cond, result, t in zip(conds, results, ccx):
            self.play(MoveToTarget(cond), MoveToTarget(result))
            arr = Arrow(cond.get_right(), result.get_left(), thickness=2, buff=0.1)
            arrs.add(arr)
            self.play(GrowArrow(arr))
            self.playw(FadeIn(t))

        ## 그런데 ... 확률은 서로 같으니까요
        probs = VGroup(
            *[
                Tex("\\frac{1}{3}", font_size=28)
                .next_to(r1c, LEFT, buff=0.5)
                .set_color(GREEN),
                Tex("\\frac{1}{3}", font_size=28)
                .next_to(r2c, LEFT, buff=0.5)
                .set_color(GREEN),
                Tex("\\frac{1}{3}", font_size=28)
                .next_to(r3c, LEFT, buff=0.5)
                .set_color(GREEN),
            ]
        )
        self.playwl(*[FadeIn(p) for p in probs], lag_ratio=0.5)
        ## R1 혹은 ... R3을 뽑는 경우라고 생각해서

        bbox1 = SurroundingRectangle(VGroup(probs[:2], ccx[:2])).set_color(GREY_A)
        bbox2 = SurroundingRectangle(VGroup(probs[2:], ccx[2:])).set_color(GREY_C)

        two = VGroup(bbox1, probs[:2], conds[:2], arrs[:2], results[:2], ccx[:2])
        one = VGroup(bbox2, probs[2:], conds[2:], arrs[2:], results[2:], ccx[2:])
        self.play(FadeIn(bbox1), FadeIn(bbox2), FadeOut(VGroup(r1, r2, r3, b1, b2, b3, box1, box2, box3, condition_text)))

        self.playw(
            VGroup(two, one)
            .animate.arrange(RIGHT, buff=2)
        )
