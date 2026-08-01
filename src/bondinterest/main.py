from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## 채권자, 채무자
        creditor = SVGMobject("assets/person.svg").scale(0.5).set_color(GREEN_B)
        debtor = SVGMobject("assets/person.svg").scale(0.5).set_color(YELLOW_B)

        people = VGroup(creditor, debtor).arrange(RIGHT, buff=3)
        creditor_label = (
            Text("채권자", font_size=24)
            .next_to(creditor, DOWN, buff=0.1)
            .set_color(GREEN_B)
        )
        debtor_label = (
            Text("채무자", font_size=24)
            .next_to(debtor, DOWN, buff=0.1)
            .set_color(YELLOW_B)
        )
        self.playw(
            FadeIn(people), FadeIn(creditor_label), FadeIn(debtor_label), run_time=0.5
        )

        ## 채권 주고 돈받기
        money = VGroup(
            t := Text("100만원", font_size=24).set_color(RED_B),
            SurroundingRectangle(t, color=RED_B),
        ).next_to(creditor, UP, buff=0.5)
        credit = VGroup(
            t := Text("채권", font_size=24).set_color(PURPLE_B),
            SurroundingRectangle(t, color=PURPLE_B),
        ).next_to(debtor, LEFT, buff=0.2)

        self.play(FadeIn(money), run_time=0.5)
        self.play(money.animate.next_to(debtor, UP, buff=0.1), run_time=0.5)
        self.playw(credit.animate.next_to(creditor, RIGHT))

        ## 이자
        int1 = VGroup(
            t := Text("104만원", font_size=24).set_color(RED_B),
            SurroundingRectangle(t, color=RED_B),
        ).next_to(debtor, LEFT, buff=0.2)

        self.playw(FadeIn(int1), FadeOut(money), run_time=0.5)

        self.playw(
            FadeOut(credit, shift=UP), int1.animate.next_to(creditor, RIGHT, buff=0.1)
        )

        ## 105만원이라면

        int2 = VGroup(
            t := Text("105만원", font_size=24).set_color(RED_B),
            SurroundingRectangle(t, color=RED_B),
        ).move_to(int1.get_center())
        self.playw(Transform(int1, int2), run_time=0.5)

        ## 채권 재등장

        self.play(FadeIn(credit.move_to(ORIGIN).to_edge(UP, buff=2)))
        self.playw(credit.animate.scale(2), run_time=5)


class explainCredit(InteractiveScene, Scene2D):
    def construct(self):

        ## credit

        credit = VGroup(
            Text("채권", font_size=24).set_color(PURPLE_B),
            Rectangle(width=10, height=4).set_color(PURPLE_A),
        )
        credit[0].align(credit[1], UL, buff=0.2)
        self.playw(FadeIn(credit), run_time=0.5)

        ## 설명
        explain = VGroup(
            Words("채권자에게 100만원을 빌리고", font_size=24, font="Noto Serif KR"),
            Words("ㅈㄴ 오랫동안 이자를 바친 다음", font_size=24, font="Noto Serif KR"),
            Words("원금도 돌려주겠다는 계약", font_size=24, font="Noto Serif KR"),
        ).arrange(DOWN, aligned_edge=LEFT)
        explainw = VGroup(*explain[0].words, *explain[1].words, *explain[2].words)

        self.playwl(*[FadeIn(w) for w in explainw], lag_ratio=0.5)

        ## fadeout explain
        self.playw(FadeOut(explainw), run_time=0.5)

        ## 예시: 100만원 3년물 4%
        example = VGroup(
            Words("100만원 3년물 4%", font_size=24, font="Noto Serif KR"),
            Words("4만원씩 매년 이자로 바친다.", font_size=24, font="Noto Serif KR"),
            Words(
                "그래서 3년간 총 12만원을 이자로 내며",
                font_size=24,
                font="Noto Serif KR",
            ),
            Words(
                "3년 후에 원금 100만원도 돌려주겠다", font_size=24, font="Noto Serif KR"
            ),
        ).arrange(DOWN, aligned_edge=LEFT)
        _e0 = example[0].copy().set_opacity(0)
        example[0].move_to(ORIGIN).align_to(_e0, UP).set_color(GREEN_B)

        examplew = VGroup(
            *example[0].words, *example[1].words, *example[2].words, *example[3].words
        )
        self.playwl(*[FadeIn(w) for w in example[0].words], lag_ratio=0.5)

        ## 설명
        self.playwl(*[FadeIn(w) for w in examplew[3:]], lag_ratio=0.5)

        ## 4만원씩 매년
        fpy = example[1].words[:2]
        ol = self.overlay
        self.add(fpy.set_z_index(ol.z_index + 1))
        self.playw(fpy.animate.set_color(BLUE), FadeIn(ol))

        ## nl
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(
                0, 56, 0, (np.float32(-0.03), np.float32(0.3), np.float32(0.42)), 8.00
            ),
            fpy.animate.rotate(56 * DEGREES, axis=RIGHT),
        )
        nl = (
            NumberLine(x_range=[0, 5, 1], width=8, include_ticks=False)
            .next_to(fpy, UP, buff=0.75)
            .set_z_index(ol.z_index + 1)
            .align_to(fpy, LEFT)
            .set_color(BLUE)
            .rotate(56 * DEGREES, axis=RIGHT)
            .shift(OUT)
        )

        def get_tick(n):
            return Line(nl.n2p(n) + DOWN * 0.1, nl.n2p(n) + UP * 0.1)

        ticks = (
            VGroup(*[get_tick(n) for n in [0.2, 1.2, 2.2, 3.2, 4.2]])
            .set_z_index(ol.z_index + 1)
            .rotate(56 * DEGREES, axis=RIGHT)
        )
        self.playw(FadeIn(nl), FadeIn(ticks), run_time=0.5)

        ## tick labels
        tick_names_dict = {
            0.2: "지금",
            1.2: "3달후",
            2.2: "6달후",
            3.2: "9달후",
            4.2: "12달후",
        }
        tick_money_dict = {
            0.2: "-",
            1.2: "1만원",
            2.2: "1만원",
            3.2: "1만원",
            4.2: "1만원",
        }
        tick_names = (
            VGroup(
                *[
                    Text(tick_names_dict[n], font_size=20).next_to(
                        get_tick(n), DOWN + IN, buff=0.15
                    )
                    for n in [0.2, 1.2, 2.2, 3.2, 4.2]
                ]
            )
            .set_z_index(ol.z_index + 1)
            .rotate(56 * DEGREES, axis=RIGHT)
        )
        tick_money = (
            VGroup(
                *[
                    Text(tick_money_dict[n], font_size=24).next_to(
                        get_tick(n), UP + OUT, buff=0.2
                    )
                    for n in [0.2, 1.2, 2.2, 3.2, 4.2]
                ]
            )
            .set_z_index(ol.z_index + 1)
            .rotate(56 * DEGREES, axis=RIGHT)
            .set_color(BLUE)
        )

        self.playw(FadeIn(tick_names), run_time=0.5)
        money1 = tick_money[0].set_z_index(ol.z_index + 1)
        money2 = tick_money[1].set_z_index(ol.z_index + 1)
        money3 = tick_money[2].set_z_index(ol.z_index + 1)
        money4 = tick_money[3].set_z_index(ol.z_index + 1)
        money5 = tick_money[4].set_z_index(ol.z_index + 1)
        self.play(FadeIn(money1), run_time=0.5)
        self.play(FadeIn(money2), run_time=0.5)
        self.play(FadeIn(money3), run_time=0.5)
        self.play(FadeIn(money4), run_time=0.5)
        self.playw(FadeIn(money5), run_time=0.5)

        ## 6개월 단위로 변경
        self.play(
            FadeOut(tick_names[1::2]), FadeOut(tick_money[1::2]), FadeOut(ticks[1::2])
        )
        tick_money_dict2 = {0.2: "-", 2.2: "2만원", 4.2: "2만원"}
        tick_money2 = (
            VGroup(
                *[
                    Text(tick_money_dict2[n], font_size=24).next_to(
                        get_tick(n), UP + OUT, buff=0.2
                    )
                    for n in [0.2, 2.2, 4.2]
                ]
            )
            .set_z_index(ol.z_index + 1)
            .rotate(56 * DEGREES, axis=RIGHT)
            .set_color(BLUE)
        )
        tm20 = tick_money2[0].set_z_index(ol.z_index + 1)
        tm21 = tick_money2[1].set_z_index(ol.z_index + 1)
        tm22 = tick_money2[2].set_z_index(ol.z_index + 1)
        self.playw(
            Transform(money1, tm20),
            Transform(money3, tm21),
            Transform(money5, tm22),
            run_time=0.5,
        )

        ## last: all but nl, ticks are faded out
        self.play(FadeOut(ol), run_time=0.5)
        self.play(FadeOut(example), FadeOut(credit))

        ## nl, ticks, tick_names, tick_money to ORIGIN
        ticks = ticks[::2]
        tick_names = tick_names[::2]
        tick_money = tick_money[::2]
        remain = VGroup(nl, ticks, tick_names, tick_money)
        self.playw(
            remain.animate.move_to(ORIGIN).rotate(-56 * DEGREES, axis=RIGHT),
            Restore(self.cf),
        )


class misunderstanding(InteractiveScene, Scene2D):
    def construct(self):
        ## nl, ticks, tick_names, tick_money
        nl = NumberLine(x_range=[0, 5, 1], width=8, include_ticks=False).set_color(BLUE)

        def get_tick(n):
            return Line(nl.n2p(n) + DOWN * 0.1, nl.n2p(n) + UP * 0.1)

        ticks = VGroup(*[get_tick(n) for n in [0.2, 1.2, 2.2, 3.2, 4.2]]).set_color(
            BLUE
        )
        tick_names_dict = {
            0.2: "지금",
            1.2: "3달후",
            2.2: "6달후",
            3.2: "9달후",
            4.2: "12달후",
        }
        tick_money_dict = {
            0.2: "-",
            1.2: "1만원",
            2.2: "1만원",
            3.2: "1만원",
            4.2: "1만원",
        }
        tick_names = VGroup(
            *[
                Text(tick_names_dict[n], font_size=20).next_to(
                    get_tick(n), DOWN + IN, buff=0.15
                )
                for n in [0.2, 1.2, 2.2, 3.2, 4.2]
            ]
        )
        tick_money = VGroup(
            *[
                Text(tick_money_dict[n], font_size=24).next_to(
                    get_tick(n), UP + OUT, buff=0.2
                )
                for n in [0.2, 1.2, 2.2, 3.2, 4.2]
            ]
        ).set_color(BLUE)
        tick_money_dict2 = {0.2: "-", 2.2: "2만원", 4.2: "2만원"}
        tick_money2 = VGroup(
            *[
                Text(tick_money_dict2[n], font_size=24).next_to(
                    get_tick(n), UP + OUT, buff=0.2
                )
                for n in [0.2, 2.2, 4.2]
            ]
        ).set_color(BLUE)

        explain = (
            Words("원금 100만원, 3년물, 4% 이자", font="Noto Serif KR", font_size=28)
            .shift(UR * 2.5)
            .set_color(GREY_A)
        )

        now = VGroup(nl, ticks, tick_names[::2], tick_money2, explain)
        self.addw(now)

        ## lines

        line1 = DashedLine(
            explain.words[-2].get_bottom(),
            tick_money2[1].get_top(),
            color=GREY_A,
            buff=0.2,
        ).set_color_by_gradient(GREY_A, BLUE)
        line2 = DashedLine(
            explain.words[-2].get_bottom(),
            tick_money2[2].get_top(),
            color=GREY_A,
            buff=0.2,
        ).set_color_by_gradient(GREY_A, BLUE)
        self.playw(Create(line1), Create(line2), run_time=0.5)

        ## circumscribe 4%
        self.playw(Circumscribe(explain.words[-2], color=YELLOW_B), wait=4)
        tick_money2.save_state()
        explain.save_state()
        line1.save_state()
        line2.save_state()
        five_percent = (
            Words("5%", font="Noto Serif KR", font_size=28)
            .move_to(explain.words[-2])
            .set_color(RED_B)
        )
        self.play(Transform(explain.words[-2], five_percent), run_time=0.5)

        line1_ = DashedLine(
            explain.words[-2].get_bottom(),
            tick_money2[1].get_top(),
            color=RED_B,
            buff=0.2,
        )
        line2_ = DashedLine(
            explain.words[-2].get_bottom(),
            tick_money2[2].get_top(),
            color=RED_B,
            buff=0.2,
        )
        self.play(Transform(line1, line1_), Transform(line2, line2_))

        ## 2만원 to 2.5만원

        tick_money_dict3 = {0.2: "-", 2.2: "2.5만원", 4.2: "2.5만원"}
        tick_money3 = VGroup(
            *[
                Text(tick_money_dict3[n], font_size=24).next_to(
                    get_tick(n), UP + OUT, buff=0.2
                )
                for n in [0.2, 2.2, 4.2]
            ]
        ).set_color(RED)

        self.playw(Transform(tick_money2, tick_money3))

        ## Restore all

        self.playw(
            Restore(tick_money2), Restore(explain), Restore(line1), Restore(line2)
        )
        sr = SurroundingRectangle(VGroup(explain, tick_money2[1:]))
        self.play(FadeIn(sr))
        self.playw(sr.animate.set_fill(BLUE, opacity=0.1).set_stroke(color=BLUE))

        ## 채권 text
        text = (
            Text("채권", font_size=24)
            .set_color(PURPLE_B)
            .next_to(sr, UP, buff=0.1)
            .align(sr, LEFT, buff=0.1)
        )
        self.playw(FadeIn(text))

        ## 3년물
        three = explain.words[2]
        self.playw(FlashUnder(three, color=YELLOW))

        ## 원금과 4% 이자
        money = explain.words[:2]
        interest = explain.words[-2:]
        self.playw(
            FlashUnder(money, color=YELLOW), FlashUnder(interest, color=YELLOW), wait=3
        )

        ## 밖의 금리
        def get_intout(n=5):
            int_out = (
                Words(f"금리: {n:.1f}%", font="Noto Serif KR", font_size=24)
                .set_color(ORANGE)
                .rotate(-45 * DEGREES, axis=UP)
                .next_to(sr, RIGHT, buff=0.5)
                .align(sr, UP, buff=0.1)
            )
            return int_out

        int_out = get_intout()
        self.playw(FadeIn(int_out), run_time=0.5)
        val = ValueTracker(5)

        int_out.add_updater(lambda m: m.become(get_intout(val.get_value())))

        self.playw(val.animate.set_value(34.2), run_time=3)
        int_out.clear_updaters()
        ## sr indicate
        self.playw(Indicate(sr, color=PURE_BLUE, scale_factor=1.05))

        ## flashunder text
        self.playw(FlashUnder(explain, color=BLUE_D, stroke_width=3), run_time=2)


class realCredit(InteractiveScene, Scene2D):
    def construct(self):
        ## credit

        credit_box = Rectangle(width=6, height=2.2).set_color(PURPLE_A)
        credit_text = Words(
            "원금 100만원, 3년물, 4% 이자\n(260101)", font="Noto Serif KR", font_size=24
        ).set_color(GREY_A)
        credit1 = VGroup(credit_text, credit_box).shift(UP * 2)

        nl = (
            NumberLine(x_range=[0, 13, 1], width=12, include_ticks=False)
            .set_color(GREY_A)
            .shift(DOWN * 0.5)
        )

        def get_tick(n, loO="l"):
            if loO == "l":
                return Line(nl.n2p(n) + DOWN * 0.1, nl.n2p(n) + UP * 0.1)
            elif loO == "o":
                o = Circle(radius=0.1).move_to(nl.n2p(n)).set_stroke(BLUE)
                return o
            elif loO == "O":
                O = (
                    Circle(radius=0.1)
                    .move_to(nl.n2p(n))
                    .set_fill(BLUE, opacity=1)
                    .set_stroke(BLUE)
                )
                return O

        loOd = ["l"] + ["o"] * 11 + ["O"]
        ticks = VGroup(*[get_tick(n + 0.2, loO=loOd[n]) for n in range(13)])

        def get_intout(n=4):
            int_out = (
                Words(f"금리: {n:.1f}%", font="Noto Serif KR", font_size=24)
                .set_color(ORANGE)
                .rotate(-45 * DEGREES, axis=UP)
                .next_to(credit1, RIGHT, buff=0.5)
                .align(credit1, UP, buff=0.1)
            )
            return int_out

        int_out = get_intout()

        days_list = [
            "260101",
            "260401",
            "260701",
            "261001",
            "270101",
            "270401",
            "270701",
            "271001",
            "280101",
            "280401",
            "280701",
            "281001",
            "290101",
        ]
        days = VGroup(
            *[
                Text(day, font_size=20).next_to(get_tick(n + 0.2), DOWN + IN, buff=0.15)
                for n, day in enumerate(days_list)
            ]
        ).set_color(GREY_A)

        ## 만원 for 1~12, 100만원 in the end
        money_list = ["시작"] + [f"1만원" for _ in range(1, 12)] + ["101만원"]
        moneys = (
            VGroup(
                *[
                    Text(money, font_size=20).next_to(get_tick(n + 0.2), UP, buff=0.2)
                    for n, money in enumerate(money_list)
                ]
            )
            .set_color(BLUE)
            .set_opacity(0.2)
        )
        arrow = Arrow(
            start=nl.n2p(0.2) + UP * 1.1,
            end=nl.n2p(0.2) + UP * 0.6,
            buff=0,
            thickness=2,
            color=GREEN,
        ).next_to(nl.n2p(0.2) + UP * 1.1, DOWN, buff=0)
        moneys[0].set_opacity(1)
        self.playw(
            FadeIn(credit1),
            FadeIn(nl),
            FadeIn(ticks),
            FadeIn(int_out),
            FadeIn(days),
            FadeIn(moneys),
            FadeIn(arrow),
        )

        ## time flies

        val = ValueTracker(0.2)

        def update_arrow(m):
            return m.next_to(nl.n2p(val.get_value()) + UP * 1.1, DOWN, buff=0)

        def update_money(m):
            for n, money in enumerate(moneys):
                if val.get_value() >= n + 0.2:
                    money.set_opacity(1)
                else:
                    money.set_opacity(0.2)

        arrow.add_updater(update_arrow)
        moneys.add_updater(update_money)
        int_out.add_updater(
            lambda m: m.become(get_intout(3.87 + val.get_value() * 0.54))
        )

        self.playw(val.animate.set_value(7.7), run_time=12, rate_func=linear)

        arrow.clear_updaters()
        moneys.clear_updaters()
        int_out.clear_updaters()
        ## 새로운 채권
        c1t = credit1.generate_target()
        credit2_box = Rectangle(width=6, height=2.2).set_color(GREEN)
        credit2_text = Words(
            "원금 100만원, 1년물, 8% 이자\n(280101)", font="Noto Serif KR", font_size=24
        ).set_color(GREY_A)

        credit2 = VGroup(credit2_text, credit2_box).shift(UP * 2).scale(0.75)

        c1t.scale(0.75)
        int_out.generate_target()

        VGroup(c1t, credit2, int_out.target).arrange(RIGHT, buff=0.75).shift(UP * 2)

        self.playw(
            MoveToTarget(credit1),
            FadeIn(credit2[1], scale=3),
            FadeIn(VGroup(credit2[0].words[:-3], credit2[0].words[-2:]), scale=3),
            MoveToTarget(int_out),
            wait=0.5,
        )
        self.playw(Transformr(int_out.copy(), credit2[0].words[-3]))
        ## money2
        money_list2 = [f"시작" if i == 8 else f"2만원" for i in range(8, 12)] + [
            "102만원"
        ]
        money2 = (
            VGroup(
                *[
                    Text(money, font_size=20).next_to(get_tick(n + 0.2), UP, buff=0.6)
                    for n, money in enumerate(money_list2, start=8)
                ]
            )
            .set_color(GREEN)
            .set_opacity(0.2)
        )
        self.playwl(
            *[FadeIn(m, shift=m.get_center() - credit2.get_center()) for m in money2],
            lag_ratio=0.3,
        )

        ## circumscribe moneys[-5:]
        self.playw(Circumscribe(moneys[-5:], color=BLUE))
        self.playw(RWiggle(credit1, amp=0.3, speed=1.5), run_time=3)

        ## credit2
        self.playw(Indicate(credit2, color=PURE_GREEN, scale_factor=1.1))

        self.playw(
            Indicate(credit2_text.words[3:5], color=PURE_GREEN, scale_factor=1.3),
            Indicate(int_out, color=PURE_GREEN, scale_factor=1.4),
        )

        ## money2
        self.playw(FlashUnder(money2, color=PURE_GREEN, stroke_width=3), run_time=2)
        self.playw(FlashUnder(moneys[-5:], color=BLUE, stroke_width=3), run_time=2)


        ## int out be 2.0
        int_out.save_state()
        int_out_new = get_intout(2.0).move_to(int_out.get_center())
        credit2_text.save_state()
        credit2_text_new = (
            Words(
                "원금 100만원, 1년물, 2% 이자\n(280101)",
                font="Noto Serif KR",
                font_size=24,
            )
            .set_color(GREY_A)
            .move_to(credit2_text.get_center()).scale(0.75)
        )
        self.play(Transform(int_out, int_out_new), Transform(credit2_text, credit2_text_new), run_time=0.5)
        self.playw(
            Indicate(credit2_text.words[3:5], color=PURE_GREEN, scale_factor=1.3),
            Indicate(int_out, color=PURE_GREEN, scale_factor=1.4),
        )

        ## money2_new
        money2.save_state()
        money_list2_new = [f"시작" if i == 8 else f"5천원" for i in range(8, 12)] + [
            "100만5천원"
        ]
        money2_new = (
            VGroup(
                *[
                    Text(money, font_size=20).next_to(get_tick(n + 0.2), UP, buff=0.6)
                    for n, money in enumerate(money_list2_new, start=8)
                ]
            )
            .set_color(GREEN)
            .set_opacity(0.2)
        )
        self.playw(
            *[
                Transform(m, m2, path_arc=PI / 2)
                for m, m2 in zip(money2, money2_new)
            ],
            run_time=0.5,
        )
        self.playw(FlashUnder(money2, color=PURE_GREEN, stroke_width=3))
        self.playw(FlashUnder(moneys[-5:], color=BLUE, stroke_width=3))

        self.embed()
        ## restore money2, int_out, credit2_text
        self.playw(Restore(money2), Restore(int_out), Restore(credit2_text), run_time=0.5)


        # arrow new updater
        #
        # self.add(money2)

        # def update_arrow2(m):
        #     return m.next_to(nl.n2p(val.get_value()) + UP * 1.5, DOWN, buff=0)

        # def update_money2(m):
        #     for n, money in enumerate(money2, start=8):
        #         if val.get_value() >= n + 0.2:
        #             money.set_opacity(1)
        #         else:
        #             money.set_opacity(0.2)

        # arrow.add_updater(update_arrow2)
        # moneys.add_updater(update_money)
        # money2.add_updater(update_money2)

        # self.playw(val.animate.set_value(12.7), run_time=6, rate_func=linear)
