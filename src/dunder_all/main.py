from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## from piui import
        c = PythonCode("import.py")
        self.playw(FadeIn(c))

        ## 의미는 간단하죠?
        p = PythonCode("piui.py").next_to(c, UP, buff=0.3, aligned_edge=LEFT)
        self.play(FadeIn(p, shift=UP * 0.25))
        self.playw(self.cf.animate.shift(UP * 1.5))


        ## piui.py 혹은 piui/__init__.py를 보고요
        label = (
            Text("piui.py", font=MONO_FONT, font_size=24)
            .next_to(p, LEFT, buff=0.1, aligned_edge=UP)
            .set_color(GREY_B)
        )
        self.playw(FadeIn(label, shift=LEFT * 0.25))

        ## 여기에 있는 객체들을 다 가져옵니다
        obj1 = p.text_slice(1, "DEFAULT_VALUE")
        obj2 = p.text_slice(3, "main_func")
        obj3 = p.text_slice(7, "helper_func")
        obj1c = obj1.copy()
        obj2c = obj2.copy()
        obj3c = obj3.copy()

        self.play(
            VGroup(obj1, obj2, obj3)
            .animate.arrange(DOWN, buff=0.1)
            .next_to(c, RIGHT, buff=0.3, aligned_edge=UP)
        )
        self.play(
            *[
                FadeOut(
                    obj,
                    shift=c.text_slice(1, "*").get_center() - obj.get_center(),
                    scale=0.5,
                )
                for obj in [obj1, obj2, obj3]
            ],
            run_time=0.5,
        )
        self.playw(*[FadeIn(obj) for obj in [obj1c, obj2c, obj3c]], run_time=0.5)

        ## 그런데 이 piui.py에 __all__ 리스트가 있으면요
        ol = self.overlay
        all_list = (
            Text('__all__ = ["main_func"]', font=MONO_FONT, font_size=24)
            .next_to(p, LEFT)
            .shift(UP)
            .set_z_index(ol.z_index + 1)
        )
        self.playw(FadeIn(ol), FadeIn(all_list, shift=LEFT * 0.25))

        self.embed()
        ## __all__에 있는 이름 객체들만 가져옵니다
        obj2 = obj2c.copy()
        obj2.set_z_index(ol.z_index + 1)
        mf_all = all_list[-11:-2]
        mf_all.set_z_index(ol.z_index + 1)
        self.add(mf_all)
        self.play(FadeIn(obj2), Indicate(mf_all, scale_factor=1.05), run_time=1)
        self.play(obj2.animate.next_to(c, RIGHT, buff=0.3), run_time=0.5)
        self.playw(
            FadeOut(
                obj2,
                shift=c.text_slice(1, "*").get_center() - obj2.get_center(),
                scale=0.5,
            ),
            run_time=0.5,
        )

        # 그래서 piui.py에 있지만 ... 사용할 수 없습니다: skip
        self.wait(3)