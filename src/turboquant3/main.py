from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## 저번 영상의 quantize에서 quantize 에러를 보정하는 기술인데요

        nump = RaenimPlane(width=14)
        nump.x_axis.set_color(GREY_C)
        nump.y_axis.set_opacity(0)

        def get_tick(x):
            tick = Line(nump.c2p(x, -0.1), nump.c2p(x, 0.1), color=WHITE)
            return tick

        num_ticks = 16
        ticks = VGroup(*[get_tick(x) for x in np.linspace(-2, 2, num_ticks)])
        tick_nums = VGroup(
            *[
                Text(f"{bin(i)[2:]:>04}", font_size=10)
                .next_to(ticks[i], DOWN if i % 2 == 0 else UP, buff=0.2)
                .set_color(GREY_B)
                for i, x in enumerate(np.linspace(-2, 2, num_ticks))
            ]
        )
        self.play(FadeIn(nump), FadeIn(ticks), FadeIn(tick_nums), run_time=0.6)

        self.play(
            self.cf.animate.scale(0.3),
            tick_nums[::2].animate.shift(DOWN * 0.2),
            run_time=0.75,
        )

        def get_real_dot(x, real_dot=[]):
            if real_dot:
                real_dot[0].move_to(nump.c2p(x, 0))
            else:
                real_dot.append(
                    Dot(nump.c2p(x, 0), radius=DEFAULT_DOT_RADIUS * 0.5).set_color(
                        GREEN
                    )
                )
            return real_dot[0]

        def get_quant_dot(x, quant_dot=[]):
            nearest_tick = (
                np.argmin(np.abs(np.linspace(-2, 2, num_ticks) - x))
                * (4 / (num_ticks - 1))
                - 2
            )

            if quant_dot:
                quant_dot[0].move_to(nump.c2p(nearest_tick, 0))
            else:
                quant_dot.append(
                    Dot(
                        nump.c2p(nearest_tick, 0), radius=DEFAULT_DOT_RADIUS * 0.5
                    ).set_color(RED)
                )
            return quant_dot[0]

        dot_position = ValueTracker(-1.5)
        real_dot = get_real_dot(dot_position.get_value())
        quant_dot = get_quant_dot(dot_position.get_value())

        def get_label_text(x):
            text = (
                Text(f"{x:.2f}", font_size=9)
                .next_to(real_dot, UP, buff=0.1)
                .set_color(GREEN)
            )
            return text

        text = get_label_text(dot_position.get_value())

        def get_quantize_error():
            brace = (
                Brace(VGroup(real_dot, quant_dot), DOWN, buff=0.0)
                .set_color(RED)
                .set_height(0.1)
            )
            error_text = (
                Text(
                    f"Quantize error",
                    font_size=9,
                )
                .next_to(brace, DOWN, buff=0.05)
                .set_color(RED)
            )
            return VGroup(brace, error_text)

        qe = get_quantize_error()

        self.play(FadeIn(real_dot), FadeIn(quant_dot), FadeIn(text), FadeIn(qe))

        def update_dots(mob):
            x = dot_position.get_value()
            get_real_dot(x)
            get_quant_dot(x)
            text.become(get_label_text(x))

            nearest_tick_idx = np.argmin(np.abs(np.linspace(-2, 2, num_ticks) - x))
            tick_nums.set_color(GREY_B)
            tick_nums[nearest_tick_idx].set_color(RED)

            qe.become(get_quantize_error())

        real_dot.add_updater(update_dots)
        quant_dot.add_updater(update_dots)
        text.add_updater(update_dots)
        tick_nums.add_updater(update_dots)
        qe.add_updater(update_dots)

        self.playw(dot_position.animate.set_value(0.85), run_time=4)

        # 그런데 QJL이 1 bit만 쓴다는 개념 이거 때문에 특히 폭력적으로 느껴집니다: skip
        self.wait(2)

        # 그래서 QJL 가지고 ... 특유의 건방진 느낌이 더 심해지죠?: skip
        self.wait(3)

        ## 하지만 사실 QJL은 ... 사이드 디쉬 같은 거라서요

        qjl_bits = VGroup(
            *[
                Text("+ 1 bit", font_size=8)
                .set_color(YELLOW_C)
                .rotate(PI / 6 if i % 2 == 1 else -PI / 6)
                .next_to(tick_nums[i], DR if i % 2 == 0 else UR, buff=0)
                for i in range(0, num_ticks)
            ]
        )
        for item in [real_dot, quant_dot, text, qe, tick_nums]:
            item.clear_updaters()
        self.play(
            *[FadeOut(item) for item in [real_dot, quant_dot, text, qe]],
            tick_nums.animate.set_color(GREY_B),
        )
        self.playw(FadeIn(qjl_bits))

        ## 이 QJL 1bit만으로 저장하는 건 아니긴 합니다
        ol = self.overlay
        qjl_bits.set_z_index(ol.z_index + 1)
        self.playw(FadeIn(ol))


class keyQuantize(InteractiveScene, Scene2D):
    def construct(self):

        ## 먼저 QJL이 풀려고 하는 문제부터 볼게요 ... key 값들을 저장한다고 했죠?
        nump = RaenimPlane(x_range=(-2.5, 2.5), width=14).shift(UP * 2.5)
        nump.x_axis.set_color(GREY_C)
        nump.y_axis.set_opacity(0)

        key_array = np.random.randn(7, 5)
        keys = VGroup(
            *[
                Matrix(key_array[:, i : i + 1]).scale(0.5).set_color(GREY_B)
                for i in range(5)
            ]
        ).arrange(RIGHT, buff=0.5)
        for key in keys:
            key[3].become(Text("...", font_size=24).set_color(GREY_C).move_to(key[3]))
        keys.add(
            Text("...", font_size=24)
            .set_color(GREY_C)
            .next_to(keys[-1], RIGHT, buff=0.5)
        )
        keys.move_to(ORIGIN)
        self.playw(FadeIn(keys))

        ## 그런데 quantization을 하면

        def get_tick(x):
            tick = Line(nump.c2p(x, -0.1), nump.c2p(x, 0.1), color=WHITE)
            return tick

        num_ticks = 16
        ticks = VGroup(*[get_tick(x) for x in np.linspace(-2, 2, num_ticks)])
        tick_nums = VGroup(
            *[
                Text(f"{bin(i)[2:]:>04}", font_size=12)
                .next_to(ticks[i], UP, buff=0.2)
                .set_color(GREY_B)
                for i, x in enumerate(np.linspace(-2, 2, num_ticks))
            ]
        )
        self.playw(FadeIn(nump), FadeIn(ticks), FadeIn(tick_nums), run_time=0.6)

        ## 원래 값이랑 quantize한 값이
        def get_arr(i, j):
            num = key_array[i, j]
            nearest_tick = (
                np.argmin(np.abs(np.linspace(-2, 2, num_ticks) - num))
                * (4 / (num_ticks - 1))
                - 2
            )
            obj = keys[j][i]
            arr = Arrow(
                obj.get_center(), nump.c2p(num, 0), buff=0, color=GREY_B, thickness=1.5
            ).set_opacity(0.5)
            return arr

        arrows = VGroup(*[get_arr(i, j) for i in range(7) for j in range(5) if i != 3])
        self.playw(FadeIn(arrows))

        keysc = keys.copy()
        numpc = nump.copy()
        ticksc = ticks.copy()
        tick_numsc = tick_nums.copy()
        arrowsc = arrows.copy()

        ## 완전히 같지는 않으니까요
        def get_quantized_arr(i, j):
            num = key_array[i, j]
            nearest_tick = (
                np.argmin(np.abs(np.linspace(-2, 2, num_ticks) - num))
                * (4 / (num_ticks - 1))
                - 2
            )
            obj = keys[j][i]
            arr = Arrow(
                obj.get_center(),
                nump.c2p(nearest_tick, 0),
                buff=0,
                color=RED,
                thickness=1.5,
            ).set_opacity(0.5)
            return arr

        key_array_quantized = np.array(
            [
                [
                    np.argmin(np.abs(np.linspace(-2, 2, num_ticks) - key_array[i, j]))
                    * (4 / (num_ticks - 1))
                    - 2
                    for j in range(5)
                ]
                for i in range(7)
            ]
        )
        keys_quantized = VGroup(
            *[
                Matrix(key_array_quantized[:, i : i + 1])
                .scale(0.5)
                .move_to(keys[i])
                .set_color(GREY_B)
                for i in range(5)
            ]
        )
        for key in keys_quantized:
            key[3].become(Text("...", font_size=24).set_color(GREY_C).move_to(key[3]))
        keys_quantized.add(
            Text("...", font_size=24)
            .set_color(GREY_C)
            .next_to(keys_quantized[-1], RIGHT, buff=0.5)
        )
        quant_arrows = VGroup(
            *[get_quantized_arr(i, j) for i in range(7) for j in range(5) if i != 3]
        )
        self.playw(
            arrows.animate.become(quant_arrows), keys.animate.become(keys_quantized)
        )

        ## 당연히 오차가 생깁니다
        cs = VGroup(keysc, numpc, ticksc, tick_numsc, arrowsc)
        self.add(cs)
        self.cf.save_state()
        self.playw(
            cs.animate.shift(RIGHT * 10), self.cf.animate.scale(1.7).shift(RIGHT * 5)
        )

        ## 이 둘의 차이를 잔차, residual이라고 부릅니다
        self.play(
            FadeOut(arrows),
            FadeOut(arrowsc),
            FadeOut(nump),
            FadeOut(ticks),
            FadeOut(tick_nums),
            FadeOut(numpc),
            FadeOut(ticksc),
            FadeOut(tick_numsc),
            run_time=0.5,
        )

        minus = Text("-").next_to(keys, RIGHT, buff=0.5)
        self.play(FadeIn(minus))

        residual = (
            Text("Residual", font_size=36)
            .set_color_by_gradient(RED_A, RED_C)
            .next_to(minus, UP, buff=2.5)
        )
        self.playw(FadeIn(residual, shift=UP))

        ## 이 residual만큼이 지금 발생한 오차인 셈입니다
        self.play(FadeOut(residual), FadeOut(minus), FadeOut(keys), run_time=0.5)

        nump = RaenimPlane(x_range=(-2.5, 2.5), width=14).shift(UP * 2.5)
        nump.x_axis.set_color(GREY_C)
        nump.y_axis.set_opacity(0)

        ticks = VGroup(*[get_tick(x) for x in np.linspace(-2, 2, num_ticks)])
        tick_nums = VGroup(
            *[
                Text(f"{bin(i)[2:]:>04}", font_size=12)
                .next_to(ticks[i], UP, buff=0.2)
                .set_color(GREY_B)
                for i, x in enumerate(np.linspace(-2, 2, num_ticks))
            ]
        )

        self.play(Restore(self.cf), keysc.animate.shift(LEFT * 10), run_time=0.7)
        self.play(FadeIn(nump), FadeIn(ticks), FadeIn(tick_nums), run_time=0.6)

        arrows = VGroup(*[get_arr(i, j) for i in range(7) for j in range(5) if i != 3])
        self.playw(FadeIn(arrows))

        ## 여기까지는 그냥 quantization하면 당연히 발생하는 현상입니다
        self.playw(
            self.cf.animate.reorient(
                -9, 48, 0, (np.float32(-0.53), np.float32(2.42), np.float32(0.07)), 0.96
            ),
            run_time=1.5,
        )


class attn(InteractiveScene, Scene2D):
    def construct(self):

        ## Attention의 이야기로 잠깐 돌아올게요
        attn_eq = Tex(
            "\\mathrm{Attention}(Q, K, V) = \\mathrm{softmax}(\\frac{QK^T}{\\sqrt{d_k}})V"
        ).scale(0.7)
        self.playw(FadeIn(attn_eq))

        ## 원래 key는 뭐하는 용도였죠?
        attn_eq.generate_target()
        attn_eq.target.set_opacity(0.3)
        attn_eq.target[-9].set_opacity(1)
        self.playw(MoveToTarget(attn_eq))

        ## query랑 내적하는 용도입니다
        self.playw(attn_eq[-10:-7].animate.set_color(YELLOW_C).set_opacity(1))

        ## Attention 계산에서 값이 크게 가중치를 주는 상황은
        qkt = attn_eq[-10:-7].copy()
        self.add(qkt)
        attn_eq[-10:-7].set_opacity(0)
        self.playw(FadeOut(attn_eq), qkt.animate.set_color(WHITE).move_to(ORIGIN))

        ## 방금 말한 내적 값이 높은 상황인데요
        q_arr = np.random.randn(3, 7)
        q_arr[0, 3] = 7.6
        q_arr[1, 4] = 6.8
        q_arr[2, 1] = 5.4
        q_min, q_max = q_arr.min(), q_arr.max()
        k_arr = np.random.randn(7, 3)
        k_arr[3, 0] = 5.7
        k_arr[1, 1] = 6.5
        k_arr[4, 2] = 8.1
        k_min, k_max = k_arr.min(), k_arr.max()
        colors = [GREY_B, PURE_RED]
        q = Matrix(q_arr).scale(0.3).set_color(GREY_B)
        k = Matrix(k_arr).scale(0.3).set_color(GREY_B)
        for i, item in enumerate(q[:-2]):
            item.set_color(
                interpolate_color(
                    colors[0],
                    colors[1],
                    (q_arr[i // 7, i % 7] - q_min) / (q_max - q_min),
                )
            )
        for i, item in enumerate(k[:-2]):
            item.set_color(
                interpolate_color(
                    colors[0],
                    colors[1],
                    (k_arr[i // 3, i % 3] - k_min) / (k_max - k_min),
                )
            )
        qk = (
            VGroup(q, k)
            .arrange(RIGHT, buff=0.1)
            .next_to(qkt, UP, buff=0.25)
            .shift(LEFT)
        )
        self.playw(Transformr(qkt[0].copy(), q), Transformr(qkt[1:].copy(), k))

        ## 즉, query가 key sample 중에 같은 차원 위치의 값이 높은 sample이랑 내적값이 높게 나옵니다
        self.play(q[7:-2].animate.set_opacity(0.3))

        qk_arr = q_arr @ k_arr
        qk_mat = (
            Matrix(qk_arr).scale(0.3).set_color(GREY_B).next_to(qk, RIGHT, buff=0.5)
        )
        q1 = q[:7]
        k1 = k[0:-2:3]
        k2 = k[1:-2:3]
        k3 = k[2:-2:3]
        eq = Text("=", font_size=24).next_to(qk, RIGHT, buff=0.25)
        self.playwl(
            FadeIn(VGroup(qk_mat[-2:], eq)),
            Transformr(VGroup(q1.copy(), k1.copy()), qk_mat[0]),
            Transformr(VGroup(q1.copy(), k2.copy()), qk_mat[1]),
            Transformr(VGroup(q1.copy(), k3.copy()), qk_mat[2]),
            lag_ratio=0.9,
        )
        self.playw(
            qk_mat[0].animate.set_color(RED),
            FlashAround(qk_mat[0], color=RED),
            FlashAround(q[3], color=RED),
            FlashAround(k[9], color=RED),
        )

        self.play(q[7:14].animate.set_opacity(1), run_time=0.3)
        q2 = q[7:14]
        self.playwl(
            Transformr(VGroup(q2.copy(), k1.copy()), qk_mat[3]),
            Transformr(VGroup(q2.copy(), k2.copy()), qk_mat[4]),
            Transformr(VGroup(q2.copy(), k3.copy()), qk_mat[5]),
            lag_ratio=0.9,
            wait=0,
        )
        self.play(
            qk_mat[5].animate.set_color(RED),
            FlashAround(qk_mat[5], color=RED),
            FlashAround(q[11], color=RED),
            FlashAround(k[14], color=RED),
        )

        q3 = q[14:21]
        self.play(q[14:21].animate.set_opacity(1), run_time=0.3)
        self.playwl(
            Transformr(VGroup(q3.copy(), k1.copy()), qk_mat[6]),
            Transformr(VGroup(q3.copy(), k2.copy()), qk_mat[7]),
            Transformr(VGroup(q3.copy(), k3.copy()), qk_mat[8]),
            lag_ratio=0.9,
            wait=1,
        )
        self.play(
            qk_mat[8].animate.set_color(RED),
            FlashAround(qk_mat[7], color=RED),
            FlashAround(q[16], color=RED),
            FlashAround(k[4], color=RED),
        )

        ## 이렇게 내적값이 높게 나온 sample에 attention이 크게 가중치를 주게 됩니다
        qk_arr_max_row = np.max(qk_arr, axis=1)
        qk_arr_exp = np.exp(qk_arr - qk_arr_max_row[:, None])
        qk_arr_softmax = qk_arr_exp / np.sum(qk_arr_exp, axis=1)[:, None]
        qk_softmax = Matrix(qk_arr_softmax).scale(0.3).set_color(GREY_B).move_to(qk_mat)
        qk_softmax[0].set_color(RED)
        qk_softmax[5].set_color(RED)
        qk_softmax[7].set_color(RED)
        softmax_text = (
            Text("softmax()", font_size=18, font=MONO_FONT)
            .next_to(qk_softmax, UP, buff=-0.1)
            .set_opacity(0.7)
        )
        qk_mat.save_state()
        self.playw(Transform(qk_mat, qk_softmax), FadeOut(softmax_text, shift=UP * 0.5))

        ## 그래서 내적값이 크게 나타나는 부분이 attention 계산에서 중요한데요
        self.play(FlashAround(q[3]), FlashAround(k[9]), FlashAround(qk_mat[0]))
        self.play(FlashAround(q[11]), FlashAround(k[14]), FlashAround(qk_mat[5]))
        self.play(FlashAround(q[16]), FlashAround(k[4]), FlashAround(qk_mat[7]))

        # 문제는 여기에 있습니다: skip
        self.wait()

        ## 아까말한 residual로 인한 오차의 영향이요
        self.playw(Restore(qk_mat))

        ## 이 내적값이 큰 경우에 더 크게 작용합니다
        self.play(qk_mat[3:-2].animate.set_opacity(0.3))
        self.playw(
            self.cf.animate.reorient(
                0, 52, 0, (np.float32(3.23), np.float32(1.37), np.float32(0.05)), 2.09
            )
        )

        # 이게 무슨 말이냐면요: skip
        self.wait()

        ## 내적값이 크게 날 쌍일수록
        self.play(FlashAround(qk_mat[0], color=RED, buff=0.08), run_time=0.5)
        self.playw(
            self.cf.animate.reorient(
                0, 51, 0, (np.float32(-0.3), np.float32(1.52), np.float32(0.24)), 4.38
            ),
            q[7:-2].animate.set_opacity(0.3),
            VGroup(k[1:-2:3], k[2:-2:3]).animate.set_opacity(0.3),
        )

        ## 이 quantization 오차 때문에
        def get_quantized_4bit():
            integer = np.random.randint(0, 16)
            q = bin(integer)[2:].zfill(4)
            return q

        q1_q = VGroup(
            *[Text(get_quantized_4bit(), font_size=12).move_to(q[i]) for i in range(7)]
        )
        k1_q = VGroup(
            *[
                Text(get_quantized_4bit(), font_size=12).move_to(k[i])
                for i in range(0, 19, 3)
            ]
        )
        q1 = q[:7]
        k1 = k[0:-2:3]
        q1.save_state()
        k1.save_state()
        self.play(Transform(q1, q1_q), Transform(k1, k1_q))
        self.playw(Restore(q1), Restore(k1))

        ## 이 쌍의 내적값이 작게 나타나는 편향이 있습니다
        self.play(
            self.cf.animate.reorient(
                0, 51, 0, (np.float32(3.23), np.float32(1.41), np.float32(0.1)), 3.50
            )
        )
        qk1_orig = [40.01, 5.68, 7.56]
        qk1_arr = [28.04, 4.12, 5.75]
        qk1_residual = [qk1_orig[i] - qk1_arr[i] for i in range(3)]
        qk1_q = VGroup(
            *[
                Text(f"{qk1_arr[i]:.2f}", font_size=14).move_to(qk_mat[i])
                for i in range(3)
            ]
        ).shift(OUT * 0.3)
        qk1_residual_text = VGroup(
            *[
                Text(f"({qk1_residual[i]:.2f})", font_size=12)
                .next_to(qk1_q[i], OUT, buff=0.15)
                .set_opacity(0.7)
                for i in range(3)
            ]
        )
        qk1_q[0].set_color(RED)
        self.play(FadeIn(qk1_q))
        self.playw(FadeIn(qk1_residual_text, shift=UP * 0.15))
        self.playw(FadeOut(qk_mat[:3], shift=IN * 0.15), qk1_q.animate.shift(IN * 0.3))

        ## 이렇게 중요한 부분에 더 오차가 큰 이런 편향이 있으면 성능에 안좋은 영향을 끼치겠죠?
        self.playw(
            FlashAround(qk1_q[0], color=RED, buff=0.05),
            FlashAround(qk1_residual_text[0], color=RED, buff=0.05),
        )

        ## 이 편향이 바로 QJL이 보완하고자 하는 편향입니다
        qjl_text = (
            (
                Text("QJL", font_size=36)
                .set_color_by_gradient(BLUE_A, BLUE_C)
                .next_to(qk_mat, RIGHT, buff=0.75)
            )
            .rotate(PI / 3, axis=RIGHT)
            .shift(OUT)
        )
        self.playwl(
            FadeIn(qjl_text),
            self.cf.animate.reorient(
                0, 51, 0, (np.float32(5.48), np.float32(1.79), np.float32(0.57)), 3.50
            ),
            lag_ratio=0.2,
        )


class easySolution(InteractiveScene, Scene2D):
    def construct(self):

        ## 제일 단순한 방법은 quantization의 bit 수를 늘리는 겁니다
        nump = RaenimPlane(x_range=(-2.5, 2.5), width=14).shift(UP * 2.5)
        nump.x_axis.set_color(GREY_C)
        nump.y_axis.set_opacity(0)

        def get_tick(x):
            tick = Line(nump.c2p(x, -0.1), nump.c2p(x, 0.1), color=WHITE)
            return tick

        num_ticks = 4
        ticks = VGroup(*[get_tick(x) for x in np.linspace(-2, 2, num_ticks)])

        key_array = np.random.randn(7, 5)
        keys = VGroup(
            *[
                Matrix(key_array[:, i : i + 1]).scale(0.5).set_color(GREY_B)
                for i in range(5)
            ]
        ).arrange(RIGHT, buff=0.5)
        for key in keys:
            key[3].become(Text("...", font_size=24).set_color(GREY_C).move_to(key[3]))
        keys.add(
            Text("...", font_size=24)
            .set_color(GREY_C)
            .next_to(keys[-1], RIGHT, buff=0.5)
        )
        keys.move_to(ORIGIN)

        self.playw(FadeIn(keys), FadeIn(nump), FadeIn(ticks), run_time=0.6, wait=0.5)

        def get_arr(i, j):
            num = key_array[i, j]
            nearest_tick = (
                np.argmin(np.abs(np.linspace(-2, 2, num_ticks) - num))
                * (4 / (num_ticks - 1))
                - 2
            )
            obj = keys[j][i]
            arr = Arrow(
                obj.get_center(), nump.c2p(num, 0), buff=0, color=GREY_B, thickness=1.5
            ).set_opacity(0.5)
            return arr

        def get_quantized_arr(i, j, num_ticks=4):
            num = key_array[i, j]
            nearest_tick = (
                np.argmin(np.abs(np.linspace(-2, 2, num_ticks) - num))
                * (4 / (num_ticks - 1))
                - 2
            )
            obj = keys[j][i]
            arr = Arrow(
                obj.get_center(),
                nump.c2p(nearest_tick, 0),
                buff=0,
                color=RED,
                thickness=1.5,
            ).set_opacity(0.5)
            return arr

        arrows = VGroup(*[get_arr(i, j) for i in range(7) for j in range(5) if i != 3])
        arrows_quantized = VGroup(
            *[get_quantized_arr(i, j) for i in range(7) for j in range(5) if i != 3]
        )
        self.play(FadeIn(arrows))
        self.playw(arrows.animate.become(arrows_quantized), run_time=0.7)

        ## 2 bit를 3 bit로
        num_ticks = 8
        ticks_ = VGroup(*[get_tick(x) for x in np.linspace(-2, 2, num_ticks)])
        self.playw(Transform(ticks, ticks_), run_time=0.6, wait=0)
        self.playw(
            arrows.animate.become(
                VGroup(
                    *[
                        get_quantized_arr(i, j, num_ticks)
                        for i in range(7)
                        for j in range(5)
                        if i != 3
                    ]
                )
            ),
            run_time=0.7,
        )

        ## 3 bit를 4bit로
        num_ticks = 16
        ticks_ = VGroup(*[get_tick(x) for x in np.linspace(-2, 2, num_ticks)])
        self.playw(Transform(ticks, ticks_), run_time=0.6, wait=0)
        self.playw(
            arrows.animate.become(
                VGroup(
                    *[
                        get_quantized_arr(i, j, num_ticks)
                        for i in range(7)
                        for j in range(5)
                        if i != 3
                    ]
                )
            ),
            run_time=0.7,
        )

        ## 이렇게 늘리면 quantization이 촘촘해지니까 이 오차 자체가 줄어들겠죠?
        arrows_orig = VGroup(
            *[
                get_arr(i, j).set_color(GREEN)
                for i in range(7)
                for j in range(5)
                if i != 3
            ]
        )

        def get_residual_arr(i):
            quant_end = arrows[i].get_end()
            orig_end = arrows_orig[i].get_end()
            res_line = BrokenLine(
                quant_end,
                (quant_end + orig_end) / 2 + UP * 0.04,
                orig_end,
                smooth=True,
            ).set_stroke(color=RED, width=4)
            return res_line

        res_lines = VGroup(*[get_residual_arr(i) for i in range(len(arrows))])
        self.play(
            self.cf.animate.reorient(
                0, 59, 0, (np.float32(-1.05), np.float32(2.23), np.float32(0.1)), 0.86
            ),
            run_time=1.5,
        )
        self.play(FadeIn(arrows_orig), run_time=0.7)
        self.playw(FadeIn(res_lines), run_time=0.7)


class QJL(InteractiveScene, Scene2D):
    def construct(self):

        ## 그런데 QJL은 다른 방법을 씁니다
        key_array = np.random.randn(7, 1)
        key = Matrix(key_array).scale(0.5).set_color(GREY_B)
        key[3].become(Text("...", font_size=24).set_color(GREY_C).move_to(key[3]))

        num_ticks = 16
        nump = RaenimPlane(x_range=(-2.5, 2.5), width=14).shift(UP * 2.5)
        nump.x_axis.set_color(GREY_C)
        nump.y_axis.set_opacity(0)

        def get_tick(x):
            tick = Line(nump.c2p(x, -0.1), nump.c2p(x, 0.1), color=WHITE)
            return tick

        ticks = VGroup(*[get_tick(x) for x in np.linspace(-2, 2, num_ticks)]).set_color(
            RED_B
        )

        key_quantized_arr = np.array(
            [
                np.argmin(np.abs(np.linspace(-2, 2, num_ticks) - key_array[i, 0]))
                * (4 / (num_ticks - 1))
                - 2
                for i in range(7)
            ]
        )
        key_quantized = Matrix(key_quantized_arr[:, None]).scale(0.5).set_color(GREY_B)
        key_quantized[3].become(
            Text("...", font_size=24).set_color(GREY_C).move_to(key_quantized[3])
        )

        keys = VGroup(key, key_quantized).arrange(RIGHT, buff=1.5).move_to(ORIGIN)

        arrows = VGroup(
            Arrow(
                key[i].get_center(),
                nump.c2p(key_array[i, 0], 0),
                buff=0,
                color=GREY_B,
                thickness=1.5,
            ).set_opacity(0.5)
            for i in range(7)
            if i != 3
        )
        self.playw(
            FadeIn(nump), FadeIn(ticks), FadeIn(key), FadeIn(arrows), run_time=0.6
        )
        quant_arrows = VGroup(
            Arrow(
                key_quantized[i].get_center(),
                nump.c2p(key_quantized_arr[i], 0),
                buff=0,
                thickness=1.5,
            )
            .set_opacity(0.5)
            .set_color(RED)
            for i in range(7)
            if i != 3
        )
        self.playw(
            Transformr(key.copy(), key_quantized),
            Transformr(arrows.copy(), quant_arrows),
            run_time=0.7,
        )

        ## 어떤 방법이냐면은요

        qjl_mat = Tex("M \\in \\mathbb{R}^{N \\times D}").next_to(
            nump.x_axis, UP, buff=2.5
        )
        self.add(qjl_mat)
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(
                0, 0, 0, (np.float32(-0.0), np.float32(3.91), np.float32(0.0)), 8.00
            )
        )

        ## Gaussian 분포에서 뽑은 양념 matrix를 하나 선언해둡니다
        sample_n01 = (
            Tex("\\sim \\mathcal{N}(0, 1)", font_size=32)
            .rotate(-PI / 6)
            .next_to(qjl_mat[0], DR, buff=0.05)
            .set_color(YELLOW_B)
        )
        self.playw(FadeIn(sample_n01))
        self.playw(FlashAround(qjl_mat[0]))

        ## 그 다음에 아까의 residual,
        self.play(Restore(self.cf), run_time=0.7)
        minus = Text("-", font_size=36).move_to(keys)
        self.play(FadeIn(minus), run_time=0.5)
        residual_arr = key_array[:, 0] - key_quantized_arr
        residual = (
            Matrix(residual_arr[:, None])
            .scale(0.5)
            .next_to(key_quantized, RIGHT, buff=1.5)
        )
        residual[3].become(
            Text("...", font_size=24).set_color(GREY_C).move_to(residual[3])
        )
        eq = Text("=", font_size=36).next_to(key_quantized, RIGHT, buff=0.75)
        self.playw(FadeIn(residual), FadeIn(eq), run_time=0.7)

        ## 이 오차에다가 양념 matrix를 곱하구요
        self.cf.save_state()
        self.play(
            residual.animate.next_to(qjl_mat[0], RIGHT, buff=0.5),
            self.cf.animate.reorient(
                0, 0, 0, (np.float32(-0.0), np.float32(3.91), np.float32(0.0)), 8.00
            ),
            FadeOut(qjl_mat[1:]),
            FadeOut(sample_n01),
        )
        qjl_mat_arr = np.random.randn(7, 7)
        result_arr = qjl_mat_arr @ residual_arr[:, None]
        result = Matrix(result_arr).scale(0.5).move_to(residual)
        result[3].become(Text("...", font_size=24).set_color(GREY_C).move_to(result[3]))
        self.playw(FadeOut(qjl_mat[0].copy(), shift=RIGHT), Transform(residual, result))

        ## 곱한 결과에서 부호 정보만, 즉 음수인지 양수인지 정보만 뽑습니다
        sign_result = VGroup(
            *[
                (
                    Text("+" if result_arr[i, 0] >= 0 else "-", font_size=24).move_to(
                        result[i]
                    )
                    if i != 3
                    else Text("...", font_size=24).set_color(GREY_C).move_to(result[3])
                )
                for i in range(7)
            ]
        )
        residual_nums = VGroup(*residual[:3], *residual[4:-2])
        signs = VGroup(*sign_result, *result[-2:]).next_to(
            residual_nums, RIGHT, buff=0.5
        )
        self.playw(Transformr(residual.copy(), signs))

        ## 이 부호 정보는 둘 중 하나니까 1 bit로 저장이 가능하겠죠?
        bit_result = VGroup(
            *[
                (
                    Text("1" if result_arr[i, 0] >= 0 else "0", font_size=24).move_to(
                        signs[i]
                    )
                    if i != 3
                    else Text("...", font_size=24).set_color(GREY_C).move_to(signs[3])
                )
                for i in range(7)
            ]
        )
        bit_result.add(signs[-2].copy())
        bit_result.add(signs[-1].copy())
        self.playw(Transform(signs, bit_result))

        self.embed()
        ## 이렇게 추가로 1bit를 더 저장해두는게 QJL의 핵심입니다
        self.play(
            signs.animate.next_to(eq, RIGHT, buff=0.75),
            Restore(self.cf),
            FadeOut(minus),
            FadeOut(eq),
            FadeOut(arrows),
            FadeOut(quant_arrows),
            FadeOut(residual),
        )
        rect_orig = SurroundingRectangle(key, color=GREEN, buff=0.25)
        text_orig = Text("Original", font_size=24).set_color(GREEN).next_to(rect_orig, DOWN, buff=0.1)
        rect_quant = SurroundingRectangle(VGroup(key_quantized, signs), color=RED, buff=0.25)
        text_quant = Text("Quantized, QJL", font_size=24).set_color(RED).next_to(rect_quant, DOWN, buff=0.1)
        self.play(FadeIn(rect_orig), FadeIn(rect_quant), run_time=0.5)
        self.playw(FadeIn(text_orig), FadeIn(text_quant))
