from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        numl = NumberLine().scale(0.7)
        numl.ticks.set_opacity(0)
        numl.ticks[len(numl.ticks) // 2].set_opacity(1)
        numl.ticks[len(numl.ticks) // 2 + 3].set_opacity(1)

        day_now_string = "2026.06.21"
        day_tomorrow_string = "2026.06.22"
        day_past_string = "2024.06.21"
        day_now = Text(day_now_string, font="Times New Roman", font_size=20).next_to(
            numl.ticks[len(numl.ticks) // 2], DOWN, buff=0.05
        )
        day_tomorrow = Text(
            day_tomorrow_string, font="Times New Roman", font_size=20
        ).next_to(numl.ticks[len(numl.ticks) // 2 + 3], DOWN, buff=0.05)
        day_past = Text(day_past_string, font="Times New Roman", font_size=20).next_to(
            numl.ticks[1], DOWN, buff=0.05
        )
        day_dot3 = Text("...", font="Times New Roman", font_size=20).next_to(
            numl.ticks[5], DOWN, buff=0.05
        )
        self.playw(FadeIn(numl), FadeIn(day_now), FadeIn(day_tomorrow))

        ## projects
        prj_a_string = "Project A: ..."
        prj_b_string = "Project B: ..."
        prj_c_string = "Project C: ..."
        prj_a = (
            Text(prj_a_string, font_size=24)
            .next_to(numl.ticks[len(numl.ticks) // 2], UR, buff=0.1)
            .set_color(GREEN)
        )
        prj_b = (
            Text(prj_b_string, font_size=24)
            .next_to(prj_a, UP, buff=0.1)
            .set_color(BLUE)
        )
        prj_c = (
            Text(prj_c_string, font_size=24)
            .next_to(prj_b, UP, buff=0.1)
            .set_color(YELLOW)
        )

        self.playw(FadeIn(prj_a), wait=0.5)
        self.playw(FadeIn(prj_b), wait=0.5)
        self.playw(FadeIn(prj_c))

        ## past
        past_prj_a = (
            Text(prj_a_string, font_size=20)
            .next_to(numl.ticks[1], UR, buff=0.1)
            .set_color(GREEN)
        )
        past_prj_b = (
            Text(prj_b_string[:-2], font_size=20)
            .next_to(past_prj_a, UP, buff=0.1)
            .set_color(BLUE)
        )
        self.playw(
            FadeIn(day_past), FadeIn(day_dot3), numl.ticks[1].animate.set_opacity(1)
        )

        ## now, daily
        task_daily = (
            Text("Daily recap", font_size=28)
            .next_to(prj_c, UP, buff=0.15)
            .set_color(PURE_RED)
        )
        self.playw(FadeIn(task_daily))

        ## past tasks
        task_past = (
            Text("Project A: ...", font_size=24)
            .next_to(numl.ticks[1], UR, buff=0.1)
            .set_color(GREEN)
        )
        task_daily_past = (
            Text("Daily recap", font_size=20)
            .next_to(task_past, UP, buff=0.15, aligned_edge=LEFT)
            .set_color(RED_B)
        )

        self.playw(FadeIn(task_past))
        self.playw(FadeIn(task_daily_past))

        ## using claude code
        text = (
            Words("(using claude code)", font_size=24, font="Noto Serif KR")
            .next_to(day_now, DOWN, buff=0.3)
            .set_color(ORANGE)
        )
        self.playwl(*[FadeIn(w) for w in text.words], lag_ratio=0.5)

        ol = self.overlay
        self.add(
            prj_a.set_z_index(ol.z_index + 1),
            prj_b.set_z_index(ol.z_index + 1),
            prj_c.set_z_index(ol.z_index + 1),
            task_daily.set_z_index(ol.z_index + 1),
        )

        self.playw(FadeIn(ol))

        # howto?
        self.wait(2)

        ## conversation
        conv_a = (
            RoundedRectangle(width=3, height=2, color=GREEN, corner_radius=0.1)
            .next_to(prj_a, RIGHT, buff=0.3, aligned_edge=DOWN)
            .set_z_index(ol.z_index + 1)
        )
        conv_b = (
            RoundedRectangle(width=3, height=2, color=BLUE, corner_radius=0.1)
            .next_to(prj_b, LEFT, buff=0.3, aligned_edge=DOWN)
            .set_z_index(ol.z_index + 1)
        )
        conv_c = (
            RoundedRectangle(width=3, height=2, color=YELLOW, corner_radius=0.1)
            .next_to(conv_a, UP, buff=0.3)
            .set_z_index(ol.z_index + 1)
        )

        self.play(
            FadeIn(conv_a), FadeIn(conv_b), FadeIn(conv_c), self.cf.animate.shift(UP)
        )

        def get_conv(*strings, target):
            texts = VGroup()
            for s in strings:
                texts.add(Words(s, font_size=20))
            texts.arrange(DOWN, buff=0.15)
            texts.move_to(target)
            for i, t in enumerate(texts):
                if i % 2 == 0:
                    t.align_to(target, RIGHT).shift(LEFT * 0.1).set_color(GREY_B)
                else:
                    t.align_to(target, LEFT).shift(RIGHT * 0.1).set_color(GREY_B)
            return texts

        conv_as = get_conv(
            "Fix the bug.",
            "I'll fix a bug. ...",
            "Still exists.",
            "I'll fix it again. ...",
            target=conv_a,
        ).set_z_index(ol.z_index + 1)
        conv_bs = get_conv(
            "Implement the feature.", "Okay, ...", target=conv_b
        ).set_z_index(ol.z_index + 1)
        conv_cs = get_conv(
            "Training the model.", "I'll research first, ...", target=conv_c
        ).set_z_index(ol.z_index + 1)
        self.playw(FadeIn(conv_as), FadeIn(conv_bs), FadeIn(conv_cs))

        ## convs to daily recap
        conva = VGroup(conv_a, conv_as).set_z_index(ol.z_index + 1)
        convb = VGroup(conv_b, conv_bs).set_z_index(ol.z_index + 1)
        convc = VGroup(conv_c, conv_cs).set_z_index(ol.z_index + 1)

        self.play(
            FadeOut(
                conva, shift=task_daily.get_center() - conva.get_center(), scale=0.3
            ),
            FadeOut(
                convb, shift=task_daily.get_center() - convb.get_center(), scale=0.3
            ),
            FadeOut(
                convc, shift=task_daily.get_center() - convc.get_center(), scale=0.3
            ),
        )
        self.playw(Indicate(task_daily, color=RED))

        ## to notion
        nt = (
            SVGMobject("notion.svg")
            .scale(0.25)
            .set_z_index(ol.z_index + 1)
            .next_to(task_daily, UP, buff=1)
        )
        nt_arrow = Arrow(
            start=task_daily.get_top(), end=nt.get_bottom(), thickness=2, buff=0.1
        ).set_z_index(ol.z_index + 1)
        self.play(FadeIn(nt))
        self.playw(GrowArrow(nt_arrow))

        ## fadeout notion
        self.playw(FadeOut(nt), FadeOut(nt_arrow))

        ## re fade in convs
        self.playw(
            FadeIn(conva, shift=conva.get_center() - task_daily.get_center(), scale=2),
            FadeIn(convb, shift=convb.get_center() - task_daily.get_center(), scale=2),
            FadeIn(convc, shift=convc.get_center() - task_daily.get_center(), scale=2),
        )

        ## user's
        users_talk = VGroup(
            *[item[::2] for item in [conv_as, conv_bs, conv_cs]]
        ).set_z_index(ol.z_index + 1)
        clco_talk = VGroup(
            *[item[1::2] for item in [conv_as, conv_bs, conv_cs]]
        ).set_z_index(ol.z_index + 1)

        self.play(FadeOut(clco_talk))
        self.playw(FadeOut(users_talk), FadeIn(clco_talk))
        self.playw(FadeIn(users_talk))

        self.wait(2)
        ## to notion again
        nt = (
            SVGMobject("notion.svg")
            .scale(0.25)
            .set_z_index(ol.z_index + 1)
            .next_to(task_daily, UP, buff=1)
        )
        nt_arrow = Arrow(
            start=task_daily.get_top(), end=nt.get_bottom(), thickness=2, buff=0.1
        ).set_z_index(ol.z_index + 1)
        self.play(FadeIn(nt))
        self.playw(GrowArrow(nt_arrow))
        self.playw(FadeOut(nt), FadeOut(nt_arrow))

        self.embed()
        ## automatically
        turna1 = conv_as[:2].copy().set_z_index(ol.z_index + 1)
        turna2 = conv_as[2:].copy().set_z_index(ol.z_index + 1)
        turnb1 = conv_bs[:2].copy().set_z_index(ol.z_index + 1)
        turnc1 = conv_cs[:2].copy().set_z_index(ol.z_index + 1)

        for item in [turna1, turna2, turnb1, turnc1]:
            self.play(
                FadeOut(
                    item, shift=task_daily.get_center() - item.get_center(), scale=0.5
                )
            )
        self.wait(2)


class hookExample(InteractiveScene, Scene2D):
    def construct(self):
        self.embed()
        # 예를 들어서 세션, 첫 대화를 시작할 때, ...
        ## split to three horizontal scenario
        line_left = Line(UP * 4, DOWN * 4, color=GREY_D).to_edge(
            LEFT, buff=7.111111 * 2 / 3
        )
        orig1 = np.array([-7.111111 * 2 / 3, 0, 0])
        orig2 = ORIGIN
        orig3 = np.array([7.111111 * 2 / 3, 0, 0])
        line_right = Line(UP * 4, DOWN * 4, color=GREY_D).to_edge(
            RIGHT, buff=7.111111 * 2 / 3
        )

        rect1 = RoundedRectangle(
            width=3.5, height=5, corner_radius=0.2, color=GREY_A
        ).move_to(orig1)
        rect2 = RoundedRectangle(
            width=3.5, height=5, corner_radius=0.2, color=GREY_A
        ).move_to(orig2)
        rect3 = RoundedRectangle(
            width=3.5, height=5, corner_radius=0.2, color=GREY_A
        ).move_to(orig3)

        self.play(FadeIn(line_left), FadeIn(rect1))

        def get_conv(*strings, target):
            texts = VGroup()
            for s in strings:
                texts.add(Words(s, font_size=20))
            texts.arrange(DOWN, buff=0.15)
            texts.move_to(target)
            for i, t in enumerate(texts):
                if i % 2 == 0:
                    t.align_to(target, RIGHT).shift(LEFT * 0.1).set_color(GREEN)
                else:
                    t.align_to(target, LEFT).shift(RIGHT * 0.1).set_color(ORANGE)
            return texts

        rect_text1 = get_conv("Fix the bug that ...", target=rect1).shift(UP * 2)
        self.play(FadeIn(rect_text1))
        self.playw(Flash(rect_text1[0][-1]))
        rect_text2 = get_conv(
            "Fix the bug that ...",
            "Okay, let me start ...",
            "The bug still exists.",
            target=rect2,
        ).align_to(rect_text1, UP)
        rect_text2[-1].set_opacity(0).shift(DOWN)
        self.addw(rect2, rect_text2, line_right, wait=0.3)
        self.play(rect_text2[-1].animate.set_opacity(1))
        self.playw(Flash(rect_text2[-1][-1]))

        rect_text3 = get_conv(
            "Fix the bug that ...",
            "Okay, let me start ...",
            "...",
            "...Done!",
            target=rect3,
        ).align_to(rect_text2, UP)

        self.addw(rect3, rect_text3[0], rect_text3[1][:5], wait=0.3)
        self.playwl(
            *[FadeIn(c) for c in [*rect_text3[1][5:], *rect_text3[3]]], lag_ratio=0.15, wait=0
        )
        self.playw(Flash(rect_text3[-1][-1]))

        ## 중간마다 알아서
        self.playw(Flash(rect_text2[1][-1]), Flash(rect_text3[-1][-1]))
        

        