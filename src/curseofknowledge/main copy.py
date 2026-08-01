from manimlib import *
from raenimgl import *
from random import seed, choice, random

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## group x, y

        def get_xman():
            xman = SVGMobject("assets/person.svg").set_color(RED_B).scale(0.3)
            return xman

        def get_yman():
            yman = SVGMobject("assets/person.svg").set_color(BLUE_B).scale(0.3)
            return yman

        xmen = VGroup(*[get_xman() for i in range(10)]).arrange_in_grid(2, 5, buff=0.2)
        ymen = VGroup(*[get_yman() for i in range(10)]).arrange_in_grid(2, 5, buff=0.2)
        men = VGroup(xmen, ymen).arrange(DOWN, buff=0.5)

        xt = Text("X", font_size=24).next_to(xmen, LEFT).set_color(RED_B)
        yt = Text("Y", font_size=24).next_to(ymen, LEFT).set_color(BLUE_B)

        self.playw(FadeIn(xmen), FadeIn(ymen), FadeIn(xt), FadeIn(yt))

        ## ~1979 data, 1980 expectations

        data1979 = SVGMobject("assets/doc.svg").scale(0.5)
        data1979[1].set_color(GREY_B)
        data1979[2:].set_color(GREY_D)

        exp1980 = SVGMobject("assets/doc.svg").scale(0.5)
        exp1980[1].set_color(GREY_B)
        exp1980[2:].set_color(GREY_D)

        data = (
            VGroup(data1979, exp1980)
            .arrange(DOWN, buff=0.5)
            .next_to(men, RIGHT, buff=0.5)
        )
        data1979t = (
            Text("~1979 실적(A~H 회사)", font_size=24)
            .next_to(data1979, RIGHT)
            .set_color(GREY_B)
        )
        exp1980t = (
            Text("1980 예상 실적(A~H 회사)", font_size=24)
            .next_to(exp1980, RIGHT)
            .set_color(GREY_B)
        )

        self.playw(
            FadeIn(data1979t, shift=LEFT),
            FadeIn(data1979, shift=LEFT),
            VGroup(xt, yt, men).animate.shift(LEFT * 1.5),
        )
        self.playw(
            FadeIn(exp1980t, shift=LEFT),
            FadeIn(exp1980, shift=LEFT),
        )

        ## actual 1980

        data1980 = SVGMobject("assets/doc.svg").scale(0.5)
        data1980[0].set_color(GREEN_B)
        data1980[1].set_color(GREEN_D)
        data1980[2:].set_color(GREY_D)
        data1980t = (
            Text("1980 실적(A~H 회사)", font_size=24)
            .next_to(data1980, RIGHT)
            .set_color(GREEN_B)
        )
        data1980 = (
            VGroup(data1980t, data1980)
            .next_to(data, DOWN, buff=0.5)
            .align_to(data, LEFT)
            .shift(RIGHT * 5)
        )
        self.play(data1980.animate.shift(LEFT * 4))
        self.playw(data1980.animate.shift(RIGHT * 4))

        ## x

        xrr = (
            RoundedRectangle(corner_radius=0.1, width=5, height=2)
            .set_color(RED_B)
            .move_to(VGroup(xmen, xt))
        )
        self.playw(FadeIn(xrr), VGroup(ymen, yt).animate.set_opacity(0.2))

        q1 = (
            Text("A~H 회사 주당 순이익은 각각 얼마?", font_size=24)
            .next_to(data1979, UP, buff=0.3)
            .set_color(RED_B)
            .shift(RIGHT * 0.5)
        )
        self.play(FadeIn(q1, shift=UP * 0.3))
        self.playw(FlashUnder(q1, color=RED_B))

        ## A~H
        no_bias = [3.47, 4.90, 4.90, 1.47, 1.25, 0.87, 0.41, 3.45]

        ## A
        a10 = np.random.rand(10) - 0.5 + no_bias[0]

        a_nums = (
            VGroup(*[DecimalNumber(a, num_decimal_places=2, font_size=20) for a in a10])
            .arrange_in_grid(2, 5, buff=0.3)
            .next_to(xmen, UP, buff=0.5)
        )
        a_str = Text("A", font_size=24).next_to(a_nums, RIGHT).set_color(RED_B)
        self.playw(FadeIn(a_nums, shift=UP * 0.5), FadeIn(a_str))

        nums_d = (
            VGroup(
                *[
                    DecimalNumber(no_bias[i], num_decimal_places=2, font_size=20)
                    .set_color(RED_D)
                    .set_opacity(0.3)
                    for i in range(8)
                ]
            )
            .arrange(RIGHT, buff=0.3)
            .next_to(a_nums, UP, buff=0.2)
        )

        ## B~H
        b10 = np.random.rand(10) - 0.5 + no_bias[1]
        b_nums = (
            VGroup(*[DecimalNumber(b, num_decimal_places=2, font_size=20) for b in b10])
            .arrange_in_grid(2, 5, buff=0.3)
            .next_to(xmen, UP, buff=0.5)
        )
        b_str = Text("B", font_size=24).next_to(b_nums, RIGHT).set_color(RED_B)
        c10 = np.random.rand(10) - 0.5 + no_bias[2]
        c_nums = (
            VGroup(*[DecimalNumber(c, num_decimal_places=2, font_size=20) for c in c10])
            .arrange_in_grid(2, 5, buff=0.3)
            .next_to(xmen, UP, buff=0.5)
        )
        c_str = Text("C", font_size=24).next_to(c_nums, RIGHT).set_color(RED_B)
        d10 = np.random.rand(10) - 0.5 + no_bias[3]
        d_nums = (
            VGroup(*[DecimalNumber(d, num_decimal_places=2, font_size=20) for d in d10])
            .arrange_in_grid(2, 5, buff=0.3)
            .next_to(xmen, UP, buff=0.5)
        )
        d_str = Text("D", font_size=24).next_to(d_nums, RIGHT).set_color(RED_B)
        e10 = np.random.rand(10) - 0.5 + no_bias[4]
        e_nums = (
            VGroup(*[DecimalNumber(e, num_decimal_places=2, font_size=20) for e in e10])
            .arrange_in_grid(2, 5, buff=0.3)
            .next_to(xmen, UP, buff=0.5)
        )
        e_str = Text("E", font_size=24).next_to(e_nums, RIGHT).set_color(RED_B)
        f10 = np.random.rand(10) - 0.5 + no_bias[5]
        f_nums = (
            VGroup(*[DecimalNumber(f, num_decimal_places=2, font_size=20) for f in f10])
            .arrange_in_grid(2, 5, buff=0.3)
            .next_to(xmen, UP, buff=0.5)
        )
        f_str = Text("F", font_size=24).next_to(f_nums, RIGHT).set_color(RED_B)
        g10 = np.random.rand(10) - 0.5 + no_bias[6]
        g_nums = (
            VGroup(*[DecimalNumber(g, num_decimal_places=2, font_size=20) for g in g10])
            .arrange_in_grid(2, 5, buff=0.3)
            .next_to(xmen, UP, buff=0.5)
        )
        g_str = Text("G", font_size=24).next_to(g_nums, RIGHT).set_color(RED_B)
        h10 = np.random.rand(10) - 0.5 + no_bias[7]
        h_nums = (
            VGroup(*[DecimalNumber(h, num_decimal_places=2, font_size=20) for h in h10])
            .arrange_in_grid(2, 5, buff=0.3)
            .next_to(xmen, UP, buff=0.5)
        )
        h_str = Text("H", font_size=24).next_to(h_nums, RIGHT).set_color(RED_B)

        ## anims
        strs = VGroup(a_str, b_str, c_str, d_str, e_str, f_str, g_str, h_str)
        nums_group = VGroup(
            a_nums, b_nums, c_nums, d_nums, e_nums, f_nums, g_nums, h_nums
        )
        anims = []

        for i in range(7):
            anims.append(
                AnimationGroup(
                    FadeOut(strs[i], shift=UP * 0.5),
                    Transformr(nums_group[i], nums_d[i]),
                    FadeIn(strs[i + 1], shift=UP * 0.5),
                    FadeIn(nums_group[i + 1], shift=UP * 2),
                )
            )
        anims.append(
            AnimationGroup(
                FadeOut(strs[7], shift=UP * 0.5),
                Transformr(nums_group[7], nums_d[7]),
            )
        )

        for i, anim in enumerate(anims):
            rt = 1 if i == 0 else 0.5
            self.play(anim, run_time=rt)
        self.wait()

        ## x gone
        xs = VGroup(xrr, xt, xmen, q1)
        ys = VGroup(yt, ymen)
        self.playw(FadeOut(xs, shift=LEFT), ys.animate.set_opacity(1))

        ## y to real answer

        actual = [3.66, 3.77, 5.62, 1.95, 1.45, 0.10, 0.55, 2.05]

        nums_actual = VGroup(
            *[
                DecimalNumber(a, num_decimal_places=2, font_size=20).set_color(GREEN_B)
                for a in actual
            ]
        ).arrange(RIGHT, buff=0.3)

        self.play(data1980.animate.shift(LEFT * 4))
        nums_actual.move_to(data1980).set_opacity(0)
        self.playw(nums_actual.animate.set_opacity(1).next_to(ymen, DOWN))

        ## y curse
        yrr = (
            RoundedRectangle(corner_radius=0.1, width=6, height=2.7)
            .set_color(BLUE_B)
            .move_to(VGroup(ymen, yt, nums_actual))
        )
        self.play(FadeIn(yrr))
        self.playw(FadeOut(yrr), Indicate(ymen, color=PURPLE_D, scale_factor=1.12))

        ## fadeout datas
        self.play(
            FadeOut(
                VGroup(data, data1980, data1979t, exp1980t, data1980t), shift=RIGHT
            ),
            FadeOut(nums_actual),
        )

        self.playw(FadeOut(yt), ymen.animate.arrange_in_grid(2, 5, buff=2))

        ## def get_note (쪽지)
        def get_note(text):
            note = SVGMobject("assets/note.svg").scale(0.25).set_color(GREY_C)
            text = Text(text, font_size=20).move_to(note.get_center())
            return VGroup(note, text)

        note_strings = "ABCDEFGH"

        notes = VGroup(
            *[
                get_note("{}".format(s)).move_to(nums_d[i])
                for i, s in enumerate(note_strings)
            ]
        )

        self.playw(FadeIn(notes))
        self.remove(nums_d)

        ## hands over notes
        notes_group = VGroup(*[notes.copy() if i != 0 else notes for i in range(10)])
        targets = VGroup()
        for i, notes in enumerate(notes_group):
            ngt = notes.generate_target()
            ngt.arrange_in_grid(2, 4, buff=0.1).scale(0.6).next_to(
                ymen[i], DOWN, buff=0.1
            )
            targets.add(ngt)

        self.playwl(*[MoveToTarget(notes_group[i]) for i in range(10)], lag_ratio=0.2)

        ## real: X's prediction
        x_predictions_list = [3.47, 4.90, 4.90, 1.47, 1.25, 0.87, 0.41, 3.45]
        x_preds = (
            VGroup(
                *[
                    DecimalNumber(
                        x_predictions_list[i], num_decimal_places=2, font_size=20
                    ).set_color(RED_B)
                    for i in range(8)
                ]
            )
            .arrange_in_grid(2, 4, buff=0.1)
            .stretch_to_fit_width(notes_group[0].get_width())
            .stretch_to_fit_height(notes_group[0].get_height())
        )
        x_preds_group = VGroup(
            *[x_preds.copy().next_to(ymen[i], DOWN, buff=0.1) for i in range(10)]
        ).set_opacity(0.4)
        notes_group.save_state()
        self.play(*[Transform(notes_group[i], x_preds_group[i]) for i in range(10)])

        self.playw(Restore(notes_group))

        ## 50$
        moneys = [ValueTracker(50) for _ in range(10)]

        get_fifty = lambda m: Text(f"${m:.2f}", font_size=20).set_color(GREEN_B)
        fifties = VGroup(
            *[
                get_fifty(moneys[i].get_value()).next_to(ymen[i], UP, buff=0.1)
                for i in range(10)
            ]
        )
        self.playw(FadeIn(fifties, shift=UP * 0.2))

        # -- implemented by claude code --
        # 잔액 표시를 ValueTracker에 연결한다.
        # FadeIn(shift=...)이 끝난 뒤에 붙여야 등장 애니메이션과 싸우지 않고,
        # 표시 문자열이 바뀔 때만 다시 그려서 매 프레임 Text를 새로 만들지 않는다.
        def follow_money(i):
            shown = [None]

            def update(label):
                text = f"${moneys[i].get_value():.2f}"
                if text == shown[0]:
                    return
                shown[0] = text
                label.become(
                    get_fifty(moneys[i].get_value()).next_to(ymen[i], UP, buff=0.1)
                )

            return update

        for i in range(10):
            fifties[i].add_updater(follow_money(i))

        ## trade notes
        # 쪽지 격자는 4열 고정, 왼쪽 위부터 채운다.
        # arrange_in_grid가 균일한 셀 격자라서 이웃 칸 중심의 차이가 곧 칸 간격이 된다.
        # (0.6배 스케일까지 이미 반영된 값이라 따로 곱할 필요가 없다)
        NOTE_COLS = 4
        col_step = notes_group[0][1].get_center() - notes_group[0][0].get_center()
        row_step = (
            notes_group[0][NOTE_COLS].get_center() - notes_group[0][0].get_center()
        )

        # 각 사람의 (0행 0열) 칸 중심을 격자의 고정 기준점으로 잡는다.
        # 좌상단을 고정해두면 쪽지가 줄거나 늘어도 앞쪽 쪽지들은 제자리에 남고,
        # 마지막 행만 자라거나 줄어들어서 당겨오는 움직임이 잘 읽힌다.
        grid_origins = [ng[0].get_center().copy() for ng in notes_group]

        # 사람별 보유 쪽지를 (라벨, mobject) 목록으로 들고, 화면 순서와 항상 일치시킨다.
        holdings = [
            [(s, note) for s, note in zip(note_strings, ng)] for ng in notes_group
        ]
        # 잔액 장부. 트레이드를 여러 개 만들어두고 나중에 한꺼번에 재생해도
        # 목표값이 어긋나지 않도록 tracker가 아니라 여기서 계산한다.
        balances = [float(m.get_value()) for m in moneys]

        def note_slot(person: int, idx: int) -> np.ndarray:
            return (
                grid_origins[person]
                + (idx % NOTE_COLS) * col_step
                + (idx // NOTE_COLS) * row_step
            )

        def trade_notes(
            buyer: int, seller: int, money: float, target: str, arc: float = -30 * DEG
        ):
            sold = next(
                (i for i, (s, _) in enumerate(holdings[seller]) if s == target), None
            )
            if sold is None:
                raise ValueError(f"ymen[{seller}] has no note {target!r}")
            label, note = holdings[seller].pop(sold)

            # 돈: 산 쪽은 줄고 판 쪽은 는다
            balances[buyer] -= money
            balances[seller] += money
            anims = [
                moneys[buyer].animate.set_value(balances[buyer]),
                moneys[seller].animate.set_value(balances[seller]),
            ]

            # 판 자리 뒤의 쪽지들을 한 칸씩 당겨서 중간에 빈 자리가 없게 한다
            anims += [
                held.animate.move_to(note_slot(seller, i))
                for i, (_, held) in enumerate(holdings[seller])
                if i >= sold
            ]

            # 산 쪽은 빈 자리가 없으니 맨 뒤에 붙인다 (4열이 차면 아래 새 행으로)
            holdings[buyer].append((label, note))
            notes_group[seller].remove(note)
            notes_group[buyer].add(note)
            anims.append(
                note.animate(path_arc=arc).move_to(
                    note_slot(buyer, len(holdings[buyer]) - 1)
                )
            )

            return AnimationGroup(*anims)

        ## trade sequence
        # 매번 그 시점의 holdings를 보고 뽑는다. 미리 뽑아두면 seller가 그 쪽지를
        # 이미 팔아버린 뒤일 수 있어서 "has no note" 가 난다.
        for i in range(10):
            seller = choice([p for p in range(10) if holdings[p]])
            buyer = choice([p for p in range(10) if p != seller])
            target = choice([s for s, _ in holdings[seller]])
            money = 1.1 + random() + 1.3
            self.play(trade_notes(buyer, seller, money, target), run_time=0.5)
        # -- /implemented by claude code --
        ## questionmarks

        qmarks = VGroup(
            *[
                Text("?", font_size=24).next_to(ymen[i], RIGHT, buff=0.1)
                for i in range(10)
            ]
        ).set_color(PURPLE_B)
        self.playw(FadeIn(qmarks, shift=RIGHT * 0.2))

        ## d1, d2, d3

        d1 = VGroup(data1979, data1979t).copy()
        d2 = VGroup(exp1980, exp1980t).copy()
        d3 = data1980.copy()

        ds = (
            VGroup(d1, d2, d3)
            .arrange(RIGHT, buff=0.5)
            .next_to(ymen, UP, buff=0.8)
            .rotate(65 * DEGREES, axis=RIGHT)
            .shift(OUT)
        )
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(
                0, 65, 0, (np.float32(0.01), np.float32(-0.01), np.float32(0.18)), 8.91
            ),
            FadeIn(ds),
        )

        ## drr
        drr = SurroundingRectangle(
            ds.copy().rotate(-65 * DEGREES, axis=RIGHT), color=BLUE, buff=0.5
        ).rotate(65 * DEGREES, axis=RIGHT)
        drrx = SurroundingRectangle(
            ds[:2].copy().rotate(-65 * DEGREES, axis=RIGHT), color=RED, buff=0.2
        ).rotate(65 * DEGREES, axis=RIGHT)
        self.playw(FadeIn(drr), FadeIn(drrx))

        ## indicate ds[:2]
        self.playwl(
            Indicate(ds[0], scale_factor=1.1),
            Indicate(ds[1], scale_factor=1.1),
            lag_ratio=0.5,
        )
        self.playw(Indicate(ds[2], scale_factor=1.1, color=RED))

        ## wval
        drrc = drr.copy()
        wval = ValueTracker(drr.get_width())
        drr.add_updater(
            lambda r: r.stretch_to_fit_width(
                wval.get_value() + 0.5 * random()
            ).align_to(drrc, LEFT)
        )
        self.play(
            wval.animate.set_value(drrx.get_width() + 0.5),
            *[RWiggle(man, amp=0.3, run_time=3) for man in ymen],
            run_time=3,
        )
        drr.clear_updaters()
        self.wait()

        ## fadeout ds, drr, drrx
        self.play(FadeOut(ds), FadeOut(drr), FadeOut(drrx), run_time=0.5)
        self.playw(self.cf.animate.restore())

        ## trades again
        for i in range(10):
            seller = choice([p for p in range(10) if holdings[p]])
            buyer = choice([p for p in range(10) if p != seller])
            target = choice([s for s, _ in holdings[seller]])
            money = 1.1 + random() + 1.3
            self.play(trade_notes(buyer, seller, money, target), run_time=0.3)
        self.wait()


class results(InteractiveScene, Scene2D):
    def construct(self):

        ## last picture of intro

        ymen = VGroup(
            *[
                SVGMobject("assets/person.svg").set_color(BLUE_B).scale(0.3)
                for i in range(10)
            ]
        ).arrange_in_grid(2, 5, buff=2)

        def get_note(text):
            note = SVGMobject("assets/note.svg").scale(0.25).set_color(GREY_C)
            text = Text(text, font_size=20).move_to(note.get_center())
            return VGroup(note, text)

        notes = VGroup(*[get_note("{}".format(s)) for s in "ABCDEFGH"]).scale(0.6)
        notes.arrange_in_grid(2, 4, buff=0.1)
        notes_group = VGroup(
            *[notes.copy().next_to(ymen[i], DOWN, buff=0.1) for i in range(10)]
        )

        moneys = [ValueTracker(50) for _ in range(10)]

        def get_fifty(m):
            return Text(f"${m:.2f}", font_size=20).set_color(GREEN_B)

        fifties = [
            get_fifty(m.get_value()).next_to(ymen[i], UP, buff=0.1)
            for i, m in enumerate(moneys)
        ]
        note_strings = "ABCDEFGH"
        self.addw(ymen, notes_group, *fifties)

        # -- implemented by claude code --
        # 잔액 표시를 ValueTracker에 연결한다.
        # FadeIn(shift=...)이 끝난 뒤에 붙여야 등장 애니메이션과 싸우지 않고,
        # 표시 문자열이 바뀔 때만 다시 그려서 매 프레임 Text를 새로 만들지 않는다.
        def follow_money(i):
            shown = [None]

            def update(label):
                text = f"${moneys[i].get_value():.2f}"
                if text == shown[0]:
                    return
                shown[0] = text
                label.become(
                    get_fifty(moneys[i].get_value()).next_to(ymen[i], UP, buff=0.1)
                )

            return update

        for i in range(10):
            fifties[i].add_updater(follow_money(i))

        ## trade notes
        # 쪽지 격자는 4열 고정, 왼쪽 위부터 채운다.
        # arrange_in_grid가 균일한 셀 격자라서 이웃 칸 중심의 차이가 곧 칸 간격이 된다.
        # (0.6배 스케일까지 이미 반영된 값이라 따로 곱할 필요가 없다)
        NOTE_COLS = 4
        col_step = notes_group[0][1].get_center() - notes_group[0][0].get_center()
        row_step = (
            notes_group[0][NOTE_COLS].get_center() - notes_group[0][0].get_center()
        )

        # 각 사람의 (0행 0열) 칸 중심을 격자의 고정 기준점으로 잡는다.
        # 좌상단을 고정해두면 쪽지가 줄거나 늘어도 앞쪽 쪽지들은 제자리에 남고,
        # 마지막 행만 자라거나 줄어들어서 당겨오는 움직임이 잘 읽힌다.
        grid_origins = [ng[0].get_center().copy() for ng in notes_group]

        # 사람별 보유 쪽지를 (라벨, mobject) 목록으로 들고, 화면 순서와 항상 일치시킨다.
        holdings = [
            [(s, note) for s, note in zip(note_strings, ng)] for ng in notes_group
        ]
        # 잔액 장부. 트레이드를 여러 개 만들어두고 나중에 한꺼번에 재생해도
        # 목표값이 어긋나지 않도록 tracker가 아니라 여기서 계산한다.
        balances = [float(m.get_value()) for m in moneys]

        def note_slot(person: int, idx: int) -> np.ndarray:
            return (
                grid_origins[person]
                + (idx % NOTE_COLS) * col_step
                + (idx // NOTE_COLS) * row_step
            )

        def trade_notes(
            buyer: int, seller: int, money: float, target: str, arc: float = -30 * DEG
        ):
            sold = next(
                (i for i, (s, _) in enumerate(holdings[seller]) if s == target), None
            )
            if sold is None:
                raise ValueError(f"ymen[{seller}] has no note {target!r}")
            label, note = holdings[seller].pop(sold)

            # 돈: 산 쪽은 줄고 판 쪽은 는다
            balances[buyer] -= money
            balances[seller] += money
            anims = [
                moneys[buyer].animate.set_value(balances[buyer]),
                moneys[seller].animate.set_value(balances[seller]),
            ]

            # 판 자리 뒤의 쪽지들을 한 칸씩 당겨서 중간에 빈 자리가 없게 한다
            anims += [
                held.animate.move_to(note_slot(seller, i))
                for i, (_, held) in enumerate(holdings[seller])
                if i >= sold
            ]

            # 산 쪽은 빈 자리가 없으니 맨 뒤에 붙인다 (4열이 차면 아래 새 행으로)
            holdings[buyer].append((label, note))
            notes_group[seller].remove(note)
            notes_group[buyer].add(note)
            anims.append(
                note.animate(path_arc=arc).move_to(
                    note_slot(buyer, len(holdings[buyer]) - 1)
                )
            )

            return AnimationGroup(*anims)

        ## trade sequence
        # 매번 그 시점의 holdings를 보고 뽑는다. 미리 뽑아두면 seller가 그 쪽지를
        # 이미 팔아버린 뒤일 수 있어서 "has no note" 가 난다.
        for i in range(20):
            seller = choice([p for p in range(10) if holdings[p]])
            buyer = choice([p for p in range(10) if p != seller])
            target = choice([s for s, _ in holdings[seller]])
            money = 1.1 + random() + 1.3
            self.play(trade_notes(buyer, seller, money, target), run_time=0.07)
        # -- /implemented by claude code --

        ## rotate scene
        scene_objects = VGroup(ymen, notes_group, *fifties)
        # self.playw(moneys.animate.rotate(PI/2.5, axis=UP), run_time=3)
        self.play(
            scene_objects.animate.rotate(PI / 1.8, axis=UP).shift(IN * 4 + LEFT * 6.5)
        )

        ## numps
        x_predictions_list = [3.47, 4.90, 4.90, 1.47, 1.25, 0.87, 0.41, 3.45]
        equil = [3.49, 5.30, 5.41, 1.78, 1.31, 0.82, 0.49, 3.19]
        actual = [3.66, 3.77, 5.62, 1.95, 1.45, 0.10, 0.55, 2.05]
        # no_bias = [3.47, 4.90, 4.90, 1.47, 1.25, 0.87, 0.41, 3.45]  # E(X|I0), 점선
        # actual  = [3.66, 3.77, 5.62, 1.95, 1.45, 0.10, 0.55, 2.05]  # 실제값, 실선
        numps = (
            VGroup(
                *[
                    RaenimPlane(
                        x_range=[0, 5],
                        y_range=[min(x_predictions_list[i], equil[i], actual[i])-0.5, max(x_predictions_list[i], equil[i], actual[i])+0.5],
                        width=5,
                        height=5,
                    ).scale(3 / 5)
                    for i in range(8)
                ]
            )
            .arrange_in_grid(2, 4, buff=0.75)
            .shift(RIGHT * 1.5)
        )
        atoh = VGroup(
            *[
                Text(s, font_size=20).next_to(numps[i].c2p(0, 5.5), LEFT, buff=0.05)
                for i, s in enumerate("ABCDEFGH")
            ]
        )
        self.playw(FadeIn(numps), FadeIn(atoh))

        self.embed()
        ## balanced price

        def get_line(i, price, color=GREEN_B, dashed=True):
            nump = numps[i]
            if dashed:
                line = DashedLine(nump.c2p(0, price), nump.c2p(5, price), color=color)
            else:
                line = Line(nump.c2p(0, price), nump.c2p(5, price), color=color)
            return line

        lines = VGroup(
            *[get_line(i, x_predictions_list[i], color=RED) for i in range(8)]
        )
        texts = VGroup(
            *[
                Text(f"${x_predictions_list[i]:.2f}", font_size=20)
                .next_to(lines[i], RIGHT, buff=0.1)
                .set_color(RED)
                for i in range(8)
            ]
        )
        legends = VGroup()
        leg1 = VGroup(
            t:=Text("실제 X 예측", font_size=20).set_color(RED),
            DashedLine(LEFT, RIGHT, color=RED).next_to(t, RIGHT, buff=0.1)
        )
        leg2 = VGroup(
            t:=Text("균형 가격", font_size=20).set_color(BLUE),
            Line(LEFT, RIGHT, color=BLUE).next_to(t, RIGHT, buff=0.1)
        )
        leg3 = VGroup(
            t:=Text("실제 실적", font_size=20).set_color(GREEN_B),
            DashedLine(LEFT, RIGHT, color=GREEN_B).next_to(t, RIGHT, buff=0.1)
        )
        legends.add(leg1, leg2, leg3).arrange(DOWN, buff=0.1, aligned_edge=RIGHT).to_corner(UR, buff=0.5)
        self.playw(*[Create(line) for line in lines], FadeIn(texts, shift=RIGHT * 0.1), FadeIn(legends[0]))

        lines_equil = VGroup(
            *[get_line(i, equil[i], color=BLUE, dashed=False) for i in range(8)]
        )
        texts_equil = VGroup(
            *[
                Text(f"${equil[i]:.2f}", font_size=20)
                .next_to(lines_equil[i], RIGHT, buff=0.1)
                .set_color(BLUE)
                for i in range(8)
            ]
        )
        self.playw(*[Create(line) for line in lines_equil], FadeIn(texts_equil, shift=RIGHT * 0.1), FadeIn(legends[1]))

        lines_actual = VGroup(
            *[get_line(i, actual[i], color=GREEN_B) for i in range(8)]
        )
        texts_actual = VGroup(
            *[
                Text(f"${actual[i]:.2f}", font_size=20)
                .next_to(lines_actual[i], RIGHT, buff=0.1)
                .set_color(GREEN_B)
                for i in range(8)
            ]
        )
        self.playw(*[Create(line) for line in lines_actual], FadeIn(texts_actual, shift=RIGHT * 0.1), FadeIn(legends[2]))

