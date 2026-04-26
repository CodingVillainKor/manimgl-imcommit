from manimlib import *
from raenimgl import *
from random import seed

def hadamard(n):
    H = np.array([[1.0]])
    while H.shape[0] < n:
        H = np.block([[H, H], [H, -H]])
    return H

seed(41)
np.random.seed(41)


class kvcache(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        model = (
            Rectangle(width=6, height=3.5)
            .shift(UP * 0.5)
            .set_z_index(0.1)
            .set_fill(BLACK, opacity=0.8)
            .set_stroke(GREY_A)
        )
        model_t = Text("LLM", font_size=24).move_to(model.get_center()).set_z_index(1)

        tensor = (
            Tensor(6, shape="square", arrange=RIGHT, buff=0.2)
            .next_to(model, DOWN, buff=0.5)
            .align_to(model, LEFT)
            .shift(RIGHT * 0.2)
        )

        model_in = tensor.copy()
        self.playw(FadeIn(model), FadeIn(model_t), FadeIn(tensor))
        self.add(model_in)

        ## kv cache는요 ... 재활용하는 겁니다
        model.save_state()
        self.playwl(
            tensor.animate.shift(UP * 1.5),
            AnimationGroup(
                model.animate.scale(3).set_fill(opacity=0), FadeOut(model_t)
            ),
            lag_ratio=0.6,
            wait=0,
        )

        kv_cache_box = (
            Rectangle(width=4, height=2).to_edge(RIGHT, buff=0.3).set_color(GREEN)
        )
        kv_cache_text = (
            Text("kv cache", font_size=24)
            .next_to(kv_cache_box, UP, buff=0.2)
            .set_color(GREY_B)
            .align_to(kv_cache_box, RIGHT)
        )
        self.play(GrowFromCenter(kv_cache_box))
        self.play(FadeIn(kv_cache_text))

        kweight_box = (
            Rectangle(width=2.5, height=1)
            .set_fill(BLACK, opacity=0.7)
            .set_stroke(GREY_A)
        )
        kweight_text = (
            Text("k weight", font_size=20)
            .set_color(GREY_B)
            .move_to(kweight_box.get_center())
        )
        kweight = VGroup(kweight_box, kweight_text).set_z_index(1)
        vweight_box = (
            Rectangle(width=2.5, height=1)
            .set_fill(BLACK, opacity=0.7)
            .set_stroke(GREY_A)
        )
        vweight_text = (
            Text("v weight", font_size=20)
            .set_color(GREY_B)
            .move_to(vweight_box.get_center())
        )
        vweight = VGroup(vweight_box, vweight_text).set_z_index(1)
        VGroup(kweight, vweight).arrange(RIGHT, buff=0.5).next_to(tensor, UP, buff=0.5)
        self.play(FadeIn(kweight), FadeIn(vweight))

        kt = (
            Tensor(6, shape="square", arrange=RIGHT)
            .scale(0.5)
            .next_to(kweight, UP, buff=0.35)
            .set_z_index(-1)
        )
        kt_orig = kt.copy()
        vt = (
            Tensor(6, shape="square", arrange=RIGHT)
            .scale(0.5)
            .next_to(vweight, UP, buff=0.35)
            .set_z_index(-1)
        )
        vt_orig = vt.copy()

        self.playwl(
            Transformr(tensor.copy(), kt),
            Transformr(tensor.copy(), vt),
            lag_ratio=0.1,
            wait=0,
        )
        self.playw(VGroup(kt, vt).animate.arrange(DOWN, buff=0.3).move_to(kv_cache_box))

        ## 이게 무슨 말일까요? 한 번 볼게요

        self.play(
            FadeOut(kweight),
            FadeOut(vweight),
            VGroup(kv_cache_box, kv_cache_text, kt, vt).animate.rotate(
                -PI / 2, axis=UP
            ),
        )
        self.playw(Restore(model), FadeIn(model_t))

        ## 보통 AI 모델들은 순차적으로 반복 생성하죠?
        out = tensor.copy().next_to(model, UP, buff=0.3).align_to(tensor, LEFT)
        for o in out:
            o.set_color(random_color())
        self.play(Transformr(tensor, out))
        self.play(FadeOut(out[:-1]))
        onext = out[-1].copy()
        onext.set_z_index(5)
        path = BrokenLine(
            out[-1].get_center(),
            VGroup(out[-1], model_in).get_center() + OUT * 3 + RIGHT * 2,
            model_in.get_right() + RIGHT * 0.2 + onext.get_width() * RIGHT / 2,
            smooth=True,
            stroke_color=GREY_B,
            stroke_width=2,
        ).set_opacity(0)
        self.remove(out[-1])
        self.play(MoveAlongPath(onext, path))
        model_in = VGroup(*model_in, onext)

        tensor = model_in.copy().set_z_index(0)
        self.playw(tensor.animate.shift(UP * 1.5))
        self.embed()

        ## 이 반복 과정에서 key, value는요
        self.play(
            model.animate.scale(3).set_fill(opacity=0),
            FadeOut(model_t),
        )

        self.play(FadeIn(kweight), FadeIn(vweight))

        kt2 = kt_orig.copy()
        kt2 = VGroup(
            *kt2,
            kt2[-1].copy().set_color(random_color()).next_to(kt2, RIGHT, buff=0.05),
        )
        vt2 = vt_orig.copy()
        vt2 = VGroup(
            *vt2,
            vt2[-1]
            .copy()
            .set_color(random_bright_color())
            .next_to(vt2, RIGHT, buff=0.05),
        )
        self.playwl(
            Transformr(tensor.copy(), kt2),
            Transformr(tensor.copy(), vt2),
            lag_ratio=0.1,
            wait=0,
        )

        ## 동일 위치는 한 번 계산하고 나면 ... 값이 같습니다

        self.play(
            VGroup(kv_cache_box, kv_cache_text, kt, vt).animate.rotate(PI / 2, axis=UP)
        )
        skt1 = SurroundingRectangle(kt, color=YELLOW, buff=0.07)
        skt2 = SurroundingRectangle(kt2[:-1], color=YELLOW, buff=0.07)
        self.playw(ShowCreation(skt1), ShowCreation(skt2))
        kvt1 = SurroundingRectangle(vt, color=YELLOW, buff=0.07)
        kvt2 = SurroundingRectangle(vt2[:-1], color=YELLOW, buff=0.07)
        self.playw(ShowCreation(kvt1), ShowCreation(kvt2), wait=2)

        ## 그래서 첫 inference에 ... 재사용하면 됩니다

        self.play(
            FadeOut(skt1),
            FadeOut(kvt1),
            FadeOut(skt2),
            FadeOut(kvt2),
            FadeOut(kt2),
            FadeOut(vt2),
            tensor.animate.shift(LEFT * 2.5),
        )
        self.play(
            Transformr(tensor[-1].copy(), kt2[-1]),
            Transformr(tensor[-1].copy(), vt2[-1]),
        )
        kt_ = kt.copy()
        vt_ = vt.copy()
        self.playw(
            kt_.animate.next_to(kt2[-1], LEFT, buff=0.05),
            vt_.animate.next_to(vt2[-1], LEFT, buff=0.05),
        )

        ## 여기서 재사용할 key, value가 바로 kv cache입니다

        self.play(FlashAround(VGroup(kt, vt)))
        self.playw(ApplyWave(kv_cache_text, amplitude=0.1), run_time=1)


class sizeof_kvcache(InteractiveScene, Scene2D):
    def construct(self):
        self.embed()

        ## key랑 value 각각 shape가 .. 벡터 크기입니다
        kv_cache_box = Rectangle(width=5, height=3).set_color(GREEN)
        kv_cache_text = (
            Text("kv cache", font_size=24)
            .next_to(kv_cache_box, UP, buff=0.2)
            .set_color(GREY_B)
            .align_to(kv_cache_box, RIGHT)
        )
        kt = Tensor(6, shape="square", arrange=RIGHT).scale(0.7)
        vt = Tensor(6, shape="square", arrange=RIGHT).scale(0.7)
        VGroup(kt, vt).arrange(DOWN, buff=0.5).move_to(kv_cache_box)
        self.playw(FadeIn(kv_cache_box), FadeIn(kv_cache_text), FadeIn(kt), FadeIn(vt))

        brace_kt = Brace(kt, UP, buff=0.15).set_color(YELLOW)
        brace_text = (
            Text("Length of sentence", font_size=20)
            .next_to(brace_kt, UP, buff=0.05)
            .set_color(YELLOW)
        )

        unit = (
            Tensor(1, shape="square")
            .scale(0.7)
            .set_color(YELLOW)
            .next_to(kv_cache_box, RIGHT, buff=0.3)
        )
        self.playw(FadeIn(brace_kt), FadeIn(brace_text))
        eq_256 = (
            Text("= 256 dim", font_size=20)
            .next_to(unit, RIGHT, buff=0.1)
            .set_color(YELLOW)
        )
        self.play(FadeIn(unit))
        self.playw(FadeIn(eq_256))

        # 문장의 subword 수가 ... 512입니다: skip
        self.wait(4)

        ## 그러면 대충 k,v, ... 한 attention에서 필요합니다
        self.playw(
            FadeOut(kv_cache_box),
            FadeOut(kv_cache_text),
            FadeOut(brace_kt),
            FadeOut(brace_text),
            FadeOut(unit),
            FadeOut(eq_256),
        )

        k_numbers = (
            VGroup(*[randn(7, 1).scale(0.3) for _ in range(20)])
            .arrange(RIGHT, buff=0.1)
            .rotate(PI / 6, axis=UP)
        )
        for k in k_numbers:
            k[3].become(Text("...", font_size=20).move_to(k[3].get_center()))
        v_numbers = (
            VGroup(*[randn(7, 1).scale(0.3) for _ in range(20)])
            .arrange(RIGHT, buff=0.1)
            .rotate(PI / 6, axis=UP)
        )
        for v in v_numbers:
            v[3].become(Text("...", font_size=20).move_to(v[3].get_center()))

        VGroup(k_numbers, v_numbers).arrange(DOWN, buff=0.5).shift(
            RIGHT * 3.5
        ).set_color(GREY_B)

        self.playw(
            Transformr(kt, k_numbers),
            Transformr(vt, v_numbers),
        )

        # 그런데 모델엔 attention 모듈이 ... 굉장히 큽니다: skip
        self.wait(2)

        ## 바로 여기서 turboquant가 ... 효율적으로 kv cache를 사용할 수 있습니다

        ol = self.overlay
        self.playw(FadeIn(ol))

        num = v_numbers[0][0].copy().set_z_index(ol.z_index + 1)
        self.play(FadeIn(num))
        self.playw(
            num.animate.move_to(ORIGIN).rotate(-PI / 6, axis=UP).scale(2), run_time=1
        )


class distribution_quantize(InteractiveScene, Scene2D):
    def construct(self):

        ## 저번 영상에서 ... n등분하는 거라고 했죠?
        nump = RaenimPlane(
            x_range=[-8, 8],
            y_range=[-5, 5],
        )

        def add_tick(num):
            tick = Line(
                nump.c2p(num, -0.1), nump.c2p(num, 0.1), color=GREY_B
            ).set_z_index(1)
            return tick

        nump.y_axis.set_opacity(0)

        self.play(FadeIn(nump))

        num_range = [-7, 7]
        min_tick = add_tick(num_range[0])
        max_tick = add_tick(num_range[1])
        self.play(FadeIn(min_tick), FadeIn(max_tick))

        num_n = 16

        ticks = VGroup(
            min_tick,
            *[
                add_tick(x)
                for x in np.linspace(num_range[0], num_range[1], num_n)[1:-1]
            ],
            max_tick,
        )
        self.playw(FadeIn(ticks[1:-1]))

        ## 그런데 이건 숫자들이 ... 퍼져있다는 전제입니다
        dist_fn = lambda x: 1
        dist_graph = nump.get_graph(dist_fn, color=BLUE, x_range=num_range)
        area = nump.get_area_under_graph(dist_graph, fill_color=BLUE, fill_opacity=0.2)
        px = (
            Tex("p(x) = u(\mathrm{min}, \mathrm{max})", font_size=32)
            .set_color(GREY_A)
            .next_to(nump.c2p(0, dist_fn(0)), UP)
        )
        self.playw(FadeIn(dist_graph), FadeIn(area), FadeIn(px))

        ## 그런데 같은 4bit quantize여도 ... 다양하죠?
        min_text = (
            Tex("-100", font_size=24)
            .set_color(GREY_A)
            .next_to(min_tick, DOWN, buff=0.1)
        )
        max_text = (
            Tex("100", font_size=24).set_color(GREY_A).next_to(max_tick, DOWN, buff=0.1)
        )
        self.play(FadeIn(min_text), FadeIn(max_text))

        val = ValueTracker(-5.5)
        dot = dot = Dot(nump.c2p(val.get_value(), 0), fill_color=BLUE).set_z_index(1)

        def get_text(val):
            text = (
                Text(
                    f"{val.get_value() * 100 / 7:.1f}",
                    font_size=20,
                    font="Noto Sans KR",
                )
                .set_color(BLUE)
                .next_to(dot, DOWN, buff=0.1)
            )
            return text

        text = get_text(val)
        self.playw(FadeIn(dot), FadeIn(text))
        dot.add_updater(lambda d: d.move_to(nump.c2p(val.get_value(), 0)))
        text.add_updater(lambda t: t.become(get_text(val)))
        self.playw(val.animate.set_value(1.85), run_time=2)

        ## 그러면 quantize 간격이 듬성듬성이라서 오차가 큽니다
        dot.clear_updaters()
        text.clear_updaters()
        self.cf.save_state()
        self.playw(
            self.cf.animate.scale(0.3).move_to(dot.get_center()),
            dot.animate.scale(0.5),
            text.animate.scale(0.5).next_to(dot, DOWN, buff=0.1),
        )

        brace = (
            Brace(VGroup(ticks[9], ticks[10]), UP, buff=0.07)
            .scale(0.5)
            .align_to(ticks[9], LEFT)
            .set_color(RED)
        )
        brace_text = (
            Text("quantize error", font_size=12)
            .set_color(RED)
            .next_to(brace, UP, buff=0.05)
        )
        nums = np.linspace(num_range[0], num_range[1], num_n)
        tick9_text = (
            Tex(f"{nums[9] * 100 / 7:.2f}", font_size=12)
            .set_color(GREY_A)
            .next_to(ticks[9], DOWN, buff=0.07)
        )
        tick10_text = (
            Tex(f"{nums[10] * 100 / 7:.2f}", font_size=12)
            .set_color(GREY_A)
            .next_to(ticks[10], DOWN, buff=0.07)
        )
        self.playw(
            FadeIn(brace), FadeIn(brace_text), FadeIn(tick9_text), FadeIn(tick10_text)
        )
        self.embed()
        ## 반면에 같은 4bit지만 ... 촘촘하게 quantize할 수 있습니다
        self.play(FadeOut(brace), FadeOut(brace_text), FadeOut(dot), FadeOut(text))
        self.playw(
            Restore(self.cf),
            tick9_text.animate.scale(1.5),
            tick10_text.animate.scale(1.5),
        )

        min_text2 = (
            Tex("-1", font_size=24).set_color(GREY_A).next_to(min_tick, DOWN, buff=0.1)
        )
        max_text2 = (
            Tex("1", font_size=24).set_color(GREY_A).next_to(max_tick, DOWN, buff=0.1)
        )
        self.playwl(FlashAround(min_text), FlashAround(max_text), lag_ratio=0.5, wait=0)

        tick9_text2 = (
            Tex(f"{nums[9] * 1 / 7:.2f}", font_size=24)
            .set_color(GREY_A)
            .next_to(ticks[9], DOWN, buff=0.07)
        )
        tick10_text2 = (
            Tex(f"{nums[10] * 1 / 7:.2f}", font_size=24)
            .set_color(GREY_A)
            .next_to(ticks[10], DOWN, buff=0.07)
        )
        self.playw(
            Transform(min_text, min_text2),
            Transform(max_text, max_text2),
            Transform(tick9_text, tick9_text2),
            Transform(tick10_text, tick10_text2),
        )

        # 심지어 여기서 더 최적화를 할 수도 있는데요: skip
        self.wait(2)

        ## 전체 범위 안에서 특정 ... 더 자주 등장한다는 것도 안다면요
        dist_fn2 = lambda x: 1 - abs(x) / 7
        dist_graph2 = nump.get_graph(dist_fn2, color=BLUE, x_range=num_range)
        area2 = nump.get_area_under_graph(
            dist_graph2, fill_color=BLUE, fill_opacity=0.2
        )
        px2 = (
            Tex("p(x) = 1 - |x| / \mathrm{max}", font_size=32)
            .set_color(GREY_A)
            .next_to(nump.c2p(0, dist_fn2(0)), UP)
        )
        self.playw(
            Transform(dist_graph, dist_graph2),
            Transform(area, area2),
            Transform(px, px2),
        )

        ## 그 부분만 더 촘촘하게 quantize할 수도 있습니다
        # ticks2: non-uniform quantization, more ticks around 0, fewer ticks around the ends

        tick_nums = np.linspace(num_range[0], num_range[1], num_n)
        tick_nums = np.sign(tick_nums) * np.power(np.abs(tick_nums / 7), 2) * 7
        ticks2 = VGroup(*[add_tick(x) for x in tick_nums])
        self.playw(Transform(ticks, ticks2))

        ## 게다가 만약 확률분포가 gaussian이나 beta 분포처럼 잘 정의된 분포면 어떨까요?
        dist_fn3 = lambda x: np.exp(-(x**2) / 10)
        dist_graph3 = nump.get_graph(dist_fn3, color=BLUE, x_range=num_range)
        area3 = nump.get_area_under_graph(
            dist_graph3, fill_color=BLUE, fill_opacity=0.2
        )
        px3 = (
            Tex("p(x) = \\mathcal{N}(0, 1)", font_size=32)
            .set_color(GREY_A)
            .next_to(nump.c2p(0, dist_fn3(0)), UP)
        )
        self.playw(
            Transform(dist_graph, dist_graph3),
            Transform(area, area3),
            Transform(px, px3),
        )


class turboquant_key_problem(InteractiveScene, Scene2D):
    def construct(self):

        ## key를 quantize하려고 보니까요 문제가 하나 있습니다
        k_numbers = (
            (
                VGroup(*[randn(7, 1).scale(0.3) for _ in range(20)])
                .arrange(RIGHT, buff=0.1)
                .rotate(PI / 6, axis=UP)
            )
            .shift(RIGHT * 3.5)
            .set_color(GREY_B)
        )
        candidate_idxs = [0, 1, 2, 4, 5, 6]
        big_numbers = []
        idxs = []
        for k in k_numbers:
            k[3].become(
                Text("...", font_size=20).set_color(GREY_C).move_to(k[3].get_center())
            )
            idx = random.choice(candidate_idxs)
            random_big_number = np.random.rand() + random.randint(11, 17)
            random_big_number *= -1 if random.random() < 0.5 else 1
            big_numbers.append(random_big_number)
            idxs.append(idx)
            k[idx].become(
                Text(f"{random_big_number:.1f}", font_size=18)
                .rotate(PI / 6, axis=UP)
                .set_color(RED_B)
                .move_to(k[idx].get_center())
            )
        self.playw(FadeIn(k_numbers))
        self.embed()
        ## turboquant는 4bit로 quantize한다고 ... 너무 듬성듬성입니다
        num_range = [-7, 7]
        num_n = 16
        nump = RaenimPlane(
            x_range=[-8, 8],
            y_range=[-5, 5],
        ).shift(DOWN * 2)
        nump.y_axis.set_opacity(0)
        ticks = VGroup(
            *[
                Line(nump.c2p(x, -0.1), nump.c2p(x, 0.1), color=GREY_B).set_z_index(1)
                for x in np.linspace(num_range[0], num_range[1], num_n)
            ]
        )
        self.play(FadeIn(nump), FadeIn(ticks), self.cf.animate.shift(DOWN * 1.2))

        min_idx, min_value = min(enumerate(big_numbers), key=lambda x: x[1])
        max_idx, max_value = max(enumerate(big_numbers), key=lambda x: x[1])
        min_text = (
            Tex(f"{min_value:.1f}", font_size=18)
            .set_color(RED_B)
            .next_to(ticks[0], DOWN, buff=0.1)
        )
        max_text = (
            Tex(f"{max_value:.1f}", font_size=18)
            .set_color(RED_B)
            .next_to(ticks[-1], DOWN, buff=0.1)
        )
        self.playw(
            Transformr(k_numbers[min_idx][idxs[min_idx]].copy(), min_text),
            Transformr(k_numbers[max_idx][idxs[max_idx]].copy(), max_text),
            run_time=1.5,
        )

        # kv cache의 key는 attention에서 key weight를 통과한 결과인데요: skip
        self.wait(2)

        # 관찰해보면 특정 부분에서만 값이 튑니다: skip
        self.wait(2)

        ## 이러면 범위도 넓고 ... 잘 정의된 분포도 아닙니다
        self.play(FlashAround(min_text, color=PURE_RED))
        self.playw(FlashAround(max_text, color=PURE_RED))

        random_smooth_positive_func = (
            lambda x: (np.sin(x) + 1.5 + np.random.rand() * 0.5) / 4
        )
        dist_graph = nump.get_graph(
            random_smooth_positive_func, color=RED_B, x_range=num_range
        )
        area = nump.get_area_under_graph(dist_graph, fill_color=RED_B, fill_opacity=0.2)
        px = (
            Tex("p(x) = \\mathrm{unknown}", font_size=32)
            .set_color(GREY_A)
            .next_to(nump.c2p(0, random_smooth_positive_func(0)), UP)
        )
        self.playw(FadeIn(dist_graph), FadeIn(area), FadeIn(px))

        ## 심지어 튄다고 한 값은 ... 몇 번째 dimension에서 등장할지도 모릅니다
        high_values = VGroup(*[k_numbers[i][idxs[i]] for i in range(len(idxs))])
        self.playwl(*[Indicate(v, color=PURE_BLUE) for v in high_values], lag_ratio=0.2)

        ## 한 마디로 숫자들이 어떤 확률분포인지를 모르는데요 ... 듬성듬성 간격일거라 AI 계산이 제대로 안될 겁니다

        self.playw(Indicate(dist_graph, color=PURE_BLUE, scale_factor=1.05))

        tick_texts = VGroup(
            *[
                Tex(
                    f"{x*(max_value - min_value) / (num_range[1] - num_range[0]):.1f}",
                    font_size=18,
                )
                .set_color(RED_B)
                .next_to(ticks[i], DOWN, buff=0.1)
                for i, x in enumerate(np.linspace(num_range[0], num_range[1], num_n))
            ]
        )
        self.playw(FadeIn(tick_texts[1:-1]))


class turboquant_solution_intro(InteractiveScene, Scene2D):
    def construct(self):
        self.embed()

        ## key를 length 축으로 하나하나 본 다음에 ... quantize가 가능합니다
        k_numbers = (
            (
                VGroup(*[randn(7, 1).scale(0.3) for _ in range(20)])
                .arrange(RIGHT, buff=0.1)
                .rotate(PI / 6, axis=UP)
            )
            .shift(RIGHT * 3.5)
            .set_color(GREY_B)
        )
        candidate_idxs = [0, 1, 2, 4, 5, 6]
        big_numbers = []
        idxs = []
        for k in k_numbers:
            k[3].become(
                Text("...", font_size=20).set_color(GREY_C).move_to(k[3].get_center())
            )
            idx = random.choice(candidate_idxs)
            random_big_number = np.random.rand() + random.randint(11, 17)
            random_big_number *= -1 if random.random() < 0.5 else 1
            big_numbers.append(random_big_number)
            idxs.append(idx)
            k[idx].become(
                Text(f"{random_big_number:.1f}", font_size=18)
                .rotate(PI / 6, axis=UP)
                .set_color(RED_B)
                .move_to(k[idx].get_center())
            )
        self.addw(k_numbers)
        self.play(FadeOut(k_numbers[1:]), run_time=0.5)

        first_k = k_numbers[0]
        self.playw(
            first_k.animate.scale(1.5).rotate(-PI / 6, axis=UP).move_to(ORIGIN),
            run_time=0.75,
        )

        # flatten numbers
        nums = first_k.val.flatten()
        nums[idxs[0]] = big_numbers[0]
        nums_256 = np.concatenate([nums[:3], np.random.randn(250), nums[-3:]])
        nump = RaenimPlane(
            x_range=[-8, 8],
            y_range=[-3, 3],
        )
        nump.y_axis.set_opacity(0)

        def get_bar(x, y, color=GREY_B):
            bar = Line(nump.c2p(x, 0), nump.c2p(x, y), color=color).set_z_index(1)
            return bar

        bars = VGroup(
            *[
                get_bar(x, y, color=RED_B if abs(y) > 10 else GREY_B)
                for x, y in zip(np.linspace(-7, 7, 256), nums_256)
            ]
        )
        self.playw(FadeIn(nump), Transformr(first_k[:-2], bars), FadeOut(first_k[-2:]))

        # project to hypersphere
        nums_256_norm = nums_256 / np.linalg.norm(nums_256)
        bars_norm = VGroup(
            *[
                get_bar(x, y, color=RED_B if abs(y) > 0.75 else GREY_B)
                for x, y in zip(np.linspace(-7, 7, 256), nums_256_norm)
            ]
        )
        self.play(Transform(bars, bars_norm))

        # RHT projection
        H = hadamard(256)
        s = np.random.choice([-1, 1], size=256).astype(np.float64)
        m = (H * s) / np.sqrt(256)
        projected = m @ nums_256_norm
        projected *= 3
        bars_projected = VGroup(
            *[
                get_bar(x, y)
                for x, y in zip(np.linspace(-7, 7, 256), projected)
            ]
        )
        self.play(Transform(bars, bars_projected))

        ## beta distribution and histogram
        import math

        log_coef = math.log(6.364354734504731)  # log(1/B)

        def beta_dist(x):
            if x <= 0 or x >= 1:
                return 0
            log_p = log_coef - 0.5 * math.log(x) + 126.5 * math.log(1 - x)
            return math.exp(log_p)
        nump2 = RaenimPlane(
            x_range=[-1.5, 1.5],
            y_range=[-1, 50],
            width=15,
            height=2
        ).shift(UP * 2.5)
        nump2.y_axis.set_opacity(0)
        # beta_dist = lambda x: 6.364354734504731 * x**(-0.5) * (1-x)**126.5
        dist_graph = nump2.get_graph(beta_dist, color=BLUE, x_range=[-0.05, 0.05, 0.0001])
        area = nump2.get_area_under_graph(dist_graph, fill_color=BLUE, fill_opacity=0.2)
        px = ( # beta pdf
            Tex("p(x) = \\frac{1}{B(\\alpha, \\beta)} x^{\\alpha - 1} (1 - x)^{\\beta - 1}", font_size=28)
            .set_color(GREY_A)
            .next_to(nump2.c2p(0, beta_dist(0)), UR).shift(RIGHT*1.5)
        )
        self.playw(self.cf.animate.shift(UP*1.5), FadeIn(nump2), FadeIn(dist_graph), FadeIn(area), FadeIn(px))
        hist_bins = [[] for _ in range(256)]
        hist_centers = np.linspace(-1, 1, 256)
        for p in m @ nums_256_norm:
            idx = np.argmin(np.abs(hist_centers - p))
            hist_bins[idx].append(p)
        hist_bars = VGroup()
        def get_bar2(x, y, color=GREY_B):
            bar = Line(nump2.c2p(x, 0), nump2.c2p(x, y), color=color).set_z_index(1)
            return bar
        for x, bin in zip(hist_centers, hist_bins):
            if len(bin) > 0:
                bar = get_bar2(x, len(bin) / 10, color=GREY_B)
                hist_bars.add(bar)
        self.play(Transform(bars, hist_bars))