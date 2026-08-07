from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        chat_window = RoundedRectangle(
            corner_radius=0.2, width=6, height=4, color=WHITE, fill_opacity=0
        ).shift(UP * 0.5)
        uc1 = Words("개쩌는 기능 구현해줘", font_size=20).align(
            chat_window, UR, buff=0.2
        ).set_color(GREEN)
        cc1 = (
            VGroup(
                Words("개쩌는 기능을 구현하겠습니다", font_size=20).words,
                Words("...", font_size=20).words,
                Words("개쩌는 기능을 구현했습니다", font_size=20).words,
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            .next_to(uc1, DOWN, buff=0.5)
            .align(chat_window, LEFT, buff=0.2)
            .set_color(ORANGE)
        )
        flattened_cc1 = VGroup(*[word for words in cc1 for word in words])

        self.add(chat_window)

        ## uc1
        self.playwl(*[FadeIn(word) for word in uc1.words], lag_ratio=0.5)

        ## cc1
        self.playwl(*[FadeIn(word) for word in flattened_cc1], lag_ratio=0.5)

        ## Flash
        self.playw(Flash(cc1[-1][-1].get_right(), color=ORANGE))

        self.embed()
        ## uc2, cc2

        uc2 = Words("잘 되나?", font_size=20).next_to(cc1, DOWN, buff=0.5).align(chat_window, RIGHT, buff=0.2).set_color(GREEN)
        cc2 = Words("잘 됩니다", font_size=20).next_to(uc2, DOWN, buff=0.5).align(chat_window, LEFT, buff=0.2).set_color(ORANGE)

        self.playwl(*[FadeIn(word) for word in uc2.words], lag_ratio=0.3)
        self.playwl(*[FadeIn(word) for word in cc2.words], lag_ratio=0.3)
        self.playw(Flash(cc2[-1].get_right(), color=ORANGE))
