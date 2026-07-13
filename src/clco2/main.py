from manimlib import *
from raenimgl import *
from random import seed
from uuid import uuid4

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        line = DashedLine(UP * 5, DOWN * 5, color=GREY_D).shift(RIGHT * 2)
        self.addw(line)

        def get_userbox(text: str):
            text = Text(text, font_size=24).set_color(GREY_B)
            box = (
                RoundedRectangle(
                    corner_radius=0.2,
                    width=text.get_width() + 0.5,
                    height=text.get_height() + 0.5,
                )
                .move_to(text)
                .set_stroke(width=2, color=GREEN_B)
            )
            return VGroup(box, text)

        def get_botbox(text: str):
            text = Text(text, font_size=24).set_color(GREY_B)
            box = (
                RoundedRectangle(
                    corner_radius=0.2,
                    width=text.get_width() + 0.5,
                    height=text.get_height() + 0.5,
                )
                .move_to(text)
                .set_stroke(width=2, color=ORANGE)
            )
            return VGroup(box, text)

        chat = (
            Rectangle(width=8, height=7)
            .shift(LEFT * (7.1111111 - 2) / 2)
            .set_opacity(MOCK)
            .shift(UP)
        )
        self.add(chat)

        user1 = get_userbox("개쩌는 기능을 구현해줘")
        bot1 = get_botbox(
            "개쩌는 기능을 구현하기 전에\n프로젝트 파일들을 먼저 확인합니다. ..."
        )
        bot12 = Words("개쩌는 기능을 구현했습니다!", font_size=24).set_color(GREY_B)
        user2 = get_userbox("이건 개쩔지 않아. 다시 구현해줘")
        bot2 = get_botbox("다시 구현합니다. ...")
        bot22 = Words("다시 구현했습니다!", font_size=24).set_color(GREY_B)

        VGroup(user1, bot1, user2, bot2).arrange(DOWN, buff=0.5).move_to(chat)
        user1.align(chat, RIGHT, buff=0)
        bot1.align(chat, LEFT, buff=0)
        bot12.next_to(bot1[1], DOWN, buff=0.3, aligned_edge=LEFT)
        user2.shift(DOWN * 0.5).align(chat, RIGHT, buff=0)
        bot2.shift(DOWN * 0.5).align(chat, LEFT, buff=0)
        bot22.next_to(bot2[1], DOWN, buff=0.3, aligned_edge=LEFT)

        notion = (
            SVGMobject("notion.svg")
            .shift(RIGHT * (7.1111111 + 2) / 2 + UP * 2)
            .scale(0.5)
        )

        self.playw(GrowFromEdge(user1, RIGHT), run_time=0.5)
        self.playw(GrowFromEdge(bot1, LEFT), run_time=0.5)
        self.play(
            bot1[0].animate.stretch_to_fit_height(1.7).align_to(bot1[0], UP),
            run_time=0.5,
        )
        self.playwl(*[FadeIn(w) for w in bot12.words], lag_ratio=0.5, wait=0)
        self.play(FadeIn(notion), run_time=0.5)

        done1 = (
            Text(
                "· 사용자가 개쩌는 기능을 요청했다.\n  개쩌는 기능을 구현했다.",
                font_size=20,
            )
            .set_color(GREY_B)
            .next_to(notion, DOWN, buff=0.75)
            .shift(LEFT * 0.3)
        )
        self.playw(Transformr(bot1.copy(), done1))

        done2 = (
            Text("· 사용자가 마음에 들어하지 않는다.\n  다시 구현했다.", font_size=20)
            .set_color(GREY_B)
            .next_to(done1, DOWN, buff=0.3, aligned_edge=LEFT)
        )

        self.playw(GrowFromEdge(user2, RIGHT), run_time=0.5)
        self.playw(GrowFromEdge(bot2, LEFT), run_time=0.5)
        self.play(
            bot2[0].animate.stretch_to_fit_height(1.3).align_to(bot2[0], UP),
            run_time=0.5,
        )
        self.playwl(*[FadeIn(w) for w in bot22.words], lag_ratio=0.5, wait=0)
        self.playw(Transformr(bot2.copy(), done2))

        ## focus on notion

        self.playw(self.cf.animate.shift(RIGHT * (7.1111111 + 2) / 2))

        ## done: red

        self.playw(done1.animate.set_color(RED), done2.animate.set_color(RED))

        ## fadeout chats

        self.playw(FadeOut(VGroup(user1, bot1, bot12, user2, bot2, bot22)))

        ## times, day

        time1 = (
            Text("[11:21, 07/12]", font_size=20)
            .set_color(YELLOW_B)
            .next_to(done1, RIGHT)
        )
        time2 = (
            Text("[20:12, 07/12]", font_size=20)
            .set_color(YELLOW_B)
            .next_to(done2, RIGHT)
        )
        prj_brace = Brace(VGroup(time1, time2), direction=RIGHT).set_color(GREY_B)
        prj = (
            Text("<개쩌는 프로젝트>", font_size=20)
            .set_color(GREY_A)
            .next_to(prj_brace, RIGHT, buff=0.1)
        )

        self.play(FadeIn(time1, shift=RIGHT * 0.25))
        self.play(FadeIn(time2, shift=RIGHT * 0.25))
        self.playw(FadeIn(prj), FadeIn(prj_brace))


class whatisSessionID(InteractiveScene, Scene2D):
    def construct(self):

        ## sessionID
        img1 = ImageMobject("gz.png").scale(0.2)
        img2 = ImageMobject("bg.png").scale(0.2)

        imgs = (
            Group(img1, img2)
            .arrange(DOWN, buff=1.25, aligned_edge=RIGHT)
            .shift(LEFT * 3)
        )

        self.playw(FadeIn(imgs))

        id1_str = str(uuid4())
        id2_str = str(uuid4())

        id1 = Text(id1_str, font_size=24).set_color(GREY_B).next_to(img1, UP, buff=0.2)
        id2 = Text(id2_str, font_size=24).set_color(GREY_B).next_to(img2, UP, buff=0.2)
        self.playw(FadeIn(id1, shift=UP * 0.25), FadeIn(id2, shift=UP * 0.25))

        ii1 = Group(img1, id1)
        ii2 = Group(img2, id2)

        self.embed()
        ## Rwiggle
        log11 = Text(
            "[11:21, 07/12] 사용자가 개쩌는 기능을 요청해서 구현함.", font_size=20
        ).set_color(GREY_B)
        log12 = Text(
            "[11:24, 07/12] 사용자의 마음에 들지 않아 다시 구현.", font_size=20
        ).set_color(GREY_B)
        log21 = Text(
            "[11:22, 07/12] 별거아닌 기능을 요청해서 구현함.", font_size=20
        ).set_color(GREY_B)
        log22 = Text(
            "[11:25, 07/12] 다른 기능도 요청해서 구현함.", font_size=20
        ).set_color(GREY_B)
        log23 = Text("[11:29, 07/12] 별거아닌 기능을 롤백함.", font_size=20).set_color(
            GREY_B
        )
        VGroup(log11, log12).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(
            img1, RIGHT, buff=1.35
        )
        VGroup(log21, log22, log23).arrange(DOWN, buff=0.3, aligned_edge=LEFT).next_to(
            img2, RIGHT, buff=1.35
        )
        anim1 = AnimationGroup(
            AnimationGroup(
                RWiggle(ii1, amp=0.1, speed=10, run_time=3),
                FadeIn(log11, shift=log11.get_center() - img1.get_center(), scale=2),
            ),
            FadeIn(log12, shift=log12.get_center() - img1.get_center(), scale=2),
            lag_ratio=0.4,
        )
        anim2 = AnimationGroup(
            AnimationGroup(
                RWiggle(ii2, amp=0.1, speed=10, run_time=3),
                FadeIn(log21, shift=log21.get_center() - img2.get_center(), scale=2),
            ),
            FadeIn(log22, shift=log22.get_center() - img2.get_center(), scale=2),
            FadeIn(log23, shift=log23.get_center() - img2.get_center(), scale=2),
            lag_ratio=0.4,
        )
        self.playwl(
            *[anim1, anim2],
            lag_ratio=0.3,
        )

        ## sr1, sr2

        sr1 = SurroundingRectangle(VGroup(log11, log12), color=ORANGE, buff=0.2)
        sr2 = SurroundingRectangle(VGroup(log21, log22, log23), color=ORANGE, buff=0.2)
        self.playw(Create(sr1), Create(sr2))

        self.playw(
            sr1.animate.surround(Group(log11, log12, ii1)),
            sr2.animate.surround(Group(log21, log22, log23, ii2)),
        )
