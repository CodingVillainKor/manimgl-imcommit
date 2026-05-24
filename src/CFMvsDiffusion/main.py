from manimlib import *
from raenimgl import *
from random import seed
from torchvision.datasets import MNIST

mnist = MNIST(root="../data", train=False, download=True)
img_array = mnist.data[0].numpy()

seed(41)
np.random.seed(41)


class equation(InteractiveScene, Scene2D):
    def construct(self):
        """
        ## Scene 2
        **핵심: 수식과 코드를 자세히 보자**
        1. Diffusion 수식
        2. Sampling하는 과정
        """
        ## Scene 2
        diffusion_eq = (
            Tex(
                r"L_{\mathrm{diffusion}}(\theta) = \mathbb{E}_{t,\mathbf{x}_0,\boldsymbol{\epsilon}}",
                r"\left[||\boldsymbol{\epsilon} - \boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)||^2\right]",
            )
            .scale(0.75)
            .set_color(GREY_A)
        )
        self.playw(FadeIn(diffusion_eq))
        xt_eq = (
            Tex(
                r"\mathbf{x}_t = \sqrt{\alpha_t}\mathbf{x}_0 + \sqrt{1-\alpha_t}\boldsymbol{\epsilon}"
            )
            .scale(0.75)
            .next_to(diffusion_eq[-9:-7], DOWN, buff=0.5)
            .set_color(GREEN)
        )
        epsilon_theta_tex = diffusion_eq[-12:-10].copy()
        self.play(
            diffusion_eq[-9:-7].animate.set_color(GREEN),
            diffusion_eq[:-9].animate.set_color(GREY_D),
            diffusion_eq[-7:].animate.set_color(GREY_D),
            run_time=0.7,
        )
        self.playw(FadeIn(xt_eq))

        ## img xt, x0, noise
        x0_array = img_array / 255.0
        noise_array = np.random.uniform(0, 1, x0_array.shape)
        alpha_t = 0.5
        xt_array = np.sqrt(alpha_t) * x0_array + np.sqrt(1 - alpha_t) * noise_array
        x0 = (
            VGroup(
                *[
                    Square(
                        fill_color=interpolate_color(BLACK, WHITE, v), fill_opacity=1
                    )
                    .scale(0.015)
                    .set_stroke(width=0)
                    for v in x0_array.flatten()
                ]
            )
            .arrange_in_grid(28, 28, buff=0)
            .next_to(xt_eq[7:9], DOWN)
        )
        noise = (
            VGroup(
                *[
                    Square(
                        fill_color=interpolate_color(BLACK, WHITE, v), fill_opacity=1
                    )
                    .scale(0.015)
                    .set_stroke(width=0)
                    for v in noise_array.flatten()
                ]
            )
            .arrange_in_grid(28, 28, buff=0)
            .next_to(xt_eq[-1], DOWN)
        )
        xt = (
            VGroup(
                *[
                    Square(
                        fill_color=interpolate_color(BLACK, WHITE, v), fill_opacity=1
                    )
                    .scale(0.015)
                    .set_stroke(width=0)
                    for v in xt_array.flatten()
                ]
            )
            .arrange_in_grid(28, 28, buff=0)
            .next_to(xt_eq[:2], DOWN)
        )

        x0_tex = xt_eq[7:9].copy()
        noise_tex = xt_eq[-1].copy()
        xt_tex = xt_eq[:2].copy()
        # x0
        self.add(x0_tex)
        self.play(xt_eq.animate.set_color(GREY_D), run_time=0.7)
        self.playw(FadeIn(x0), run_time=0.7)

        # noise
        self.play(
            xt_eq.animate.set_color(GREY_D),
            FadeIn(noise_tex),
            run_time=0.7,
        )
        self.playw(FadeIn(noise), run_time=0.7)

        # xt
        self.play(
            xt_eq.animate.set_color(GREY_D),
            FadeIn(xt_tex),
            run_time=0.7,
        )
        self.playw(FadeIn(xt), run_time=0.7)
        ## xt to epsilon

        self.play(FlashAround(xt_tex, color=GREEN))
        self.playw(FlashAround(diffusion_eq[-9:-7], color=GREEN))

        self.play(diffusion_eq[-14].animate.set_color(GREEN), run_time=0.7)
        self.play(FlashAround(diffusion_eq[-14], color=GREEN))
        self.playw(FlashAround(noise_tex, color=GREEN))

        ## epsilon_theta is model
        self.playw(FadeIn(epsilon_theta_tex))

        model = Rectangle(
            width=1.8, height=0.9, fill_color=BLACK, fill_opacity=1
        ).next_to(epsilon_theta_tex, UP, buff=0.5)
        model_text = Tex(r"\epsilon_{\theta}()", font_size=36).move_to(
            model.get_center()
        )
        self.playw(FadeIn(model), FadeIn(model_text))

        ## model io
        model_input = xt.copy().set_z_index(-1)
        model_output_array = np.random.uniform(0, 1, x0_array.shape)
        model_output = (
            VGroup(
                *[
                    Square(
                        fill_color=interpolate_color(BLACK, WHITE, v), fill_opacity=1
                    )
                    .scale(0.015)
                    .set_stroke(width=0)
                    for v in model_output_array.flatten()
                ]
            )
            .arrange_in_grid(28, 28, buff=0)
            .next_to(model, UP, buff=0.25)
            .set_z_index(-1)
        )
        self.playw(model_input.animate.move_to(model).scale(0.5))
        self.playw(FadeIn(model_output, shift=UP, scale=2))

        ## loss
        loss_items = VGroup(noise.copy(), model_output)
        loss_items.generate_target().arrange(RIGHT, buff=0.5).move_to(
            model_output
        ).align_to(model_output, UP)
        self.playw(MoveToTarget(loss_items), run_time=0.7)
        loss_term = VGroup(
            Tex(r"||", font_size=36)
            .set_color(GREY_B)
            .next_to(loss_items[0], LEFT, buff=0.1),
            Tex(r"-", font_size=36).set_color(GREY_B).move_to(loss_items.get_center()),
            Tex(r"||^2", font_size=36)
            .set_color(GREY_B)
            .next_to(loss_items[1], RIGHT, buff=0.1),
        )
        self.playw(FadeIn(loss_term), run_time=0.7)

        ## reset

        self.play(
            FadeOut(diffusion_eq),
            FadeOut(xt_eq),
            FadeOut(x0),
            FadeOut(noise),
            FadeOut(xt),
            FadeOut(x0_tex),
            FadeOut(noise_tex),
            FadeOut(xt_tex),
            FadeOut(epsilon_theta_tex),
            FadeOut(loss_items),
            FadeOut(loss_term),
            run_time=0.7,
        )
        self.remove(model_input)
        model = VGroup(model, model_text)
        self.playw(model.animate.move_to(ORIGIN).align_to(model, UP).shift(UP * 0.5))

        ## sampling 과정

        sampling_eq = (
            Tex(
                r"\mathbf{x}_{t-1} = ",
                r"\frac{1}{\sqrt{\alpha_t}}\left(\mathbf{x}_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha_t}}}\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\right) + \sigma_t\mathbf{z}",
            )
            .scale(0.75)
            .set_color(GREY_A)
        )
        self.playw(FadeIn(sampling_eq))

        # xt, epsilon_theta
        xt1 = sampling_eq[0:4].copy()
        xt_tex = sampling_eq[12:14].copy()
        minus = sampling_eq[14:15].copy()
        epsilon_theta_tex = sampling_eq[27:35].copy()
        xt_in_model_tex = sampling_eq[30:32].copy()
        self.play(
            sampling_eq.animate.set_color(GREY_D),
            FadeIn(epsilon_theta_tex),
            run_time=0.7,
        )

        xt = (
            VGroup(
                *[
                    Square(
                        fill_color=interpolate_color(BLACK, WHITE, v), fill_opacity=1
                    )
                    .scale(0.015)
                    .set_stroke(width=0)
                    for v in xt_array.flatten()
                ]
            )
            .arrange_in_grid(28, 28, buff=0)
            .next_to(xt_in_model_tex, DOWN, buff=0.5)
        )
        self.playw(FadeIn(xt, scale=2, shift=DOWN * 0.5), run_time=0.7)

        self.playwl(FadeIn(xt_tex), FadeIn(minus), lag_ratio=0.5)

        self.playw(FadeIn(xt1))

        ## model input
        model_input = xt.copy().set_z_index(-1)
        self.play(model_input.animate.move_to(model).scale(0.5))

        ## model output
        model_output_array = np.random.uniform(0, 1, x0_array.shape)
        model_output = (
            VGroup(
                *[
                    Square(
                        fill_color=interpolate_color(BLACK, WHITE, v), fill_opacity=1
                    )
                    .scale(0.015)
                    .set_stroke(width=0)
                    for v in model_output_array.flatten()
                ]
            )
            .arrange_in_grid(28, 28, buff=0)
            .next_to(model, UP, buff=0.25)
            .set_z_index(-1)
        )
        self.playw(FadeIn(model_output, shift=UP, scale=2))

        ## fadeout epsilon_theta
        self.playwl(
            model_output.animate.move_to(epsilon_theta_tex),
            AnimationGroup(
                FadeOut(sampling_eq[27:35]), FadeOut(epsilon_theta_tex), FadeOut(xt)
            ),
            lag_ratio=0.15,
        )

        ## flash around xt and xt1
        self.playw(FlashAround(xt_tex, color=GREEN))
        self.playw(FlashAround(xt1, color=GREEN))


class actual_diffusion(InteractiveScene, Scene2D):
    def construct(self):
        """
        ## Scene 3
        **핵심: Scene2가 어떤 의미인지 구체적으로**
        1. 수식의 설명은 이랬고, 이미지에서 봤을 때 어떤 느낌인지 보자
        2. 이미지는 픽셀로 이루어져있고 각 값은 밝을수록 값이 큰 것
        3. 깨끗 이미지는 뚜렷, 노이즈는 여기저기 뾰족
        4. xt는 적당히 섞여서 원본이 드러날듯 말듯
        5. 여기서 xt는 clean과 noise가 조합된 상태
        6. 학습땐 레시피를 아니까 당연히 구별할 수 있지만
        7. 생성땐 분리된 각각은 모르고 clean, noise가 합쳐진 상태만 앎
        8. 모델 εθ는 합쳐진 걸 구별해내는 역할
        9. 점진적으로 깎고 더해가면서 이미지를 만들어냄
        """

        # 수식의 설명: vegas에서: skip
        self.cf.save_state()
        ## 이미지는 픽셀로 이루어짐
        img_array = mnist.data[0].numpy()
        img_float = img_array / 255.0
        img = VGroup(
            *[
                Square(fill_color=interpolate_color(BLACK, WHITE, v), fill_opacity=1)
                .scale(0.075)
                .set_stroke(width=0.5, color=GREY_D)
                for v in img_float.flatten()
            ]
        ).arrange_in_grid(28, 28, buff=0)

        self.playw(FadeIn(img))

        ## 값이 밝을수록 크다
        pxs = VGroup()
        for i in range(28):
            for j in range(28):
                v = min(img_float[i, j], 0.99)
                t = (
                    Text(f"{v:.2f}"[1:], font_size=8)
                    .move_to(img[i * 28 + j])
                    .set_color(BLACK if v > 0.2 else GREY_B)
                )
                pxs.add(t)
        self.play(FadeIn(pxs))
        self.playw(
            self.cf.animate.reorient(
                0, 0, 0, (np.float32(-0.05), np.float32(-0.05), np.float32(0.0)), 2.98
            )
        )

        ## 높이로 표현
        def get_line(i, j):
            v = img_float[i, j]
            scale = 0.1
            line = (
                Prism(width=scale, height=scale, depth=v * 1.5)
                .move_to(img[i * 28 + j].get_center() + OUT * v * 1.5 / 2)
                .set_color(GREY_B)
            )
            return line

        lines = SGroup(*[get_line(i, j) for i in range(28) for j in range(28)])
        self.play(
            self.cf.animate.reorient(
                -34,
                66,
                0,
                (np.float32(-0.01), np.float32(-0.12), np.float32(-0.09)),
                4.49,
            ),
            run_time=1.5,
        )
        pxs.generate_target()
        for i, t in enumerate(pxs.target):
            line_top = img[i].get_center() + OUT * img_float[i // 28, i % 28] * 1.5
            t.move_to(line_top)
        self.playw(
            *[GrowFromEdge(line, IN) for line in lines],
            MoveToTarget(pxs.set_z_index(1)),
            run_time=0.7,
        )

        self.playw(
            self.cf.animate.reorient(
                0, 0, 0, (np.float32(0.28), np.float32(-0.16), np.float32(-0.04)), 5.91
            ),
            run_time=6,
        )

        ## reset
        self.playw(FadeOut(lines), FadeOut(pxs), FadeOut(img), Restore(self.cf))

        ## same but noise
        img_noise_array = np.random.uniform(-0.5, 0.5, img_float.shape)
        img_noise = VGroup(
            *[
                Square(
                    fill_color=(
                        interpolate_color(BLACK, WHITE, v)
                        if v >= 0
                        else interpolate_color(BLACK, RED, -v)
                    ),
                    fill_opacity=1,
                )
                .scale(0.075)
                .set_stroke(width=0.5, color=GREY_D)
                for v in img_noise_array.flatten()
            ]
        ).arrange_in_grid(28, 28, buff=0)

        self.cf.save_state()
        pxs_noise = VGroup()
        for i in range(28):
            for j in range(28):
                v = img_noise_array[i, j]
                t = (
                    Text(f"{min(v, 0.99):.2f}"[1 if v >= 0 else 2 :], font_size=8)
                    .move_to(img_noise[i * 28 + j])
                    .set_color(BLACK if v > 0.2 else GREY_B if v >= 0 else RED)
                )
                pxs_noise.add(t)
        self.play(FadeIn(img_noise), FadeIn(pxs_noise))
        self.playw(
            self.cf.animate.reorient(
                -21,
                56,
                0,
                (np.float32(-0.39), np.float32(-0.94), np.float32(-0.28)),
                3.72,
            )
        )

        ## lines for noise
        def get_noise_line(i, j):
            v = img_noise_array[i, j]
            scale = 0.1
            line = (
                Prism(width=scale, height=scale, depth=v * 1.5)
                .move_to(img_noise[i * 28 + j].get_center() + OUT * v * 1.5 / 2)
                .set_color(
                    interpolate_color(BLACK, WHITE, v)
                    if v >= 0
                    else interpolate_color(BLACK, RED, -v)
                )
            )
            return line

        noise_lines = SGroup(
            *[get_noise_line(i, j) for i in range(28) for j in range(28)]
        )
        # pxs_noise.generate_target()
        # for i, t in enumerate(pxs_noise.target):
        #     line_top = img_noise[i].get_center() + OUT * img_noise_array[i // 28, i % 28] * 1.5
        #     t.move_to(line_top)
        self.play(
            *[GrowFromEdge(line, IN) for line in noise_lines],
            FadeOut(pxs_noise),
        )
        self.play(
            self.cf.animate.reorient(
                -50,
                82,
                0,
                (np.float32(-0.29), np.float32(-0.18), np.float32(-0.19)),
                5.88,
            ),
            run_time=0.5,
        )
        self.playw(
            self.cf.animate.reorient(
                102,
                83,
                0,
                (np.float32(-0.29), np.float32(-0.18), np.float32(-0.19)),
                5.88,
            ),
            run_time=5,
        )

        ## reset noise
        self.playw(FadeOut(noise_lines), FadeOut(img_noise), Restore(self.cf))

        ## xt는 clean과 noise가 조합된 상태
        alpha_t = 0.5
        xt_array = np.sqrt(alpha_t) * img_float + np.sqrt(1 - alpha_t) * img_noise_array
        xt = VGroup(
            *[
                Square(
                    fill_color=(
                        interpolate_color(BLACK, WHITE, v)
                        if v >= 0
                        else interpolate_color(BLACK, RED, -v)
                    ),
                    fill_opacity=1,
                )
                .scale(0.075)
                .set_stroke(width=0.5, color=GREY_D)
                for v in xt_array.flatten()
            ]
        ).arrange_in_grid(28, 28, buff=0)
        self.playw(FadeIn(xt))

        def get_xt_line(i, j):
            v = xt_array[i, j]
            scale = 0.1
            line = (
                Prism(width=scale, height=scale, depth=v * 1.5)
                .move_to(xt[i * 28 + j].get_center() + OUT * v * 1.5 / 2)
                .set_color(
                    interpolate_color(BLACK, WHITE, v)
                    if v >= 0
                    else interpolate_color(BLACK, RED, -v)
                )
            )
            return line

        xt_lines = SGroup(*[get_xt_line(i, j) for i in range(28) for j in range(28)])
        self.play(*[GrowFromEdge(line, IN) for line in xt_lines])
        self.playw(
            self.cf.animate.reorient(
                -37,
                78,
                0,
                (np.float32(-0.14), np.float32(-0.18), np.float32(-0.21)),
                6.57,
            )
        )

        ## clean is left to the xt, noise is right
        cleans = SGroup(img, lines)
        cleans.next_to(xt, LEFT, buff=0.75).align_to(xt, IN)

        noises = SGroup(img_noise, noise_lines)
        noises.next_to(xt, RIGHT, buff=0.75).align_to(xt, IN)

        self.play(FadeIn(cleans), FadeIn(noises))

        x0_text = Tex("x_0", font_size=36).next_to(cleans[0], DOWN)
        noise_text = Tex("x_T", font_size=36).next_to(noises[0], DOWN)
        xt_text = Tex(
            "x_t = \\sqrt{\\alpha_t} x_0 + \\sqrt{1 - \\alpha_t} x_T", font_size=36
        ).next_to(xt, DOWN)
        self.playw(
            FadeIn(x0_text),
            FadeIn(noise_text),
            FadeIn(xt_text),
            self.cf.animate.reorient(
                0, 24, 0, (np.float32(0.26), np.float32(-0.34), np.float32(0.17)), 10.21
            ),
        )

        ## available in training
        training_text = (
            Text("Available in training", font_size=36, font="Noto Sans KR")
            .rotate(PI / 6, axis=RIGHT)
            .next_to(xt, UP, buff=2.5)
        )
        arrows = VGroup(
            Arrow(
                training_text.get_bottom(),
                cleans[0].get_corner(UR) + LEFT * 0.75,
                buff=0.25,
            ).set_color(GREY_B),
            Arrow(
                training_text.get_bottom(),
                noises[0].get_corner(UL) + UP * 0.2,
                buff=0.1,
            ).set_color(GREY_B),
        ).set_z_index(-1)
        self.playw(FadeIn(training_text), FadeIn(arrows))

        ## Not available in sampling
        sampling_text = (
            Text("Not available in sampling", font_size=36, font="Noto Sans KR")
            .rotate(PI / 6, axis=RIGHT)
            .move_to(training_text)
            .set_color(RED)
        )
        self.playw(
            Transformr(training_text, sampling_text),
        )

        ## fadeout clean and noise
        self.playw(
            FadeOut(cleans),
            FadeOut(noises),
            FadeOut(sampling_text),
            FadeOut(arrows),
            FadeOut(x0_text),
            FadeOut(noise_text),
        )

        ## epsilon_theta
        model = Rectangle(
            width=1.8, height=0.9, fill_color=BLACK, fill_opacity=1
        ).next_to(xt, RIGHT, buff=1.2)
        model_text = Tex(r"\epsilon_{\theta}()", font_size=48).move_to(
            model.get_center()
        )
        self.playw(FadeIn(model), FadeIn(model_text))

        self.playw(FadeOut(VGroup(model, model_text).copy(), scale=2, shift=LEFT * 4))

        ## 모델의 역할: output epsilon
        self.play(
            self.cf.animate.reorient(
                0, 53, 0, (np.float32(0.12), np.float32(-0.62), np.float32(-0.12)), 6.12
            )
        )

        def get_output_line(i, j, alpha_t=alpha_t):
            v = img_noise_array[i, j] * (1 - alpha_t) ** 0.5
            scale = 0.1
            xt_z = xt_lines[i * 28 + j].get_depth()
            xt_z *= 1 if xt_array[i, j] >= 0 else -1
            line = (
                Prism(width=scale, height=scale, depth=v * 1.5)
                .move_to(
                    xt[i * 28 + j].get_center()
                    + np.array([0, 0, xt_z])
                    - OUT * v * 1.5 / 2
                )
                .set_color(RED if v > 0 else RED_D)
            )
            return line

        def get_residual_line(i, j):
            v = img_float[i, j] * alpha_t**0.5
            scale = 0.1
            line = (
                Prism(width=scale, height=scale, depth=v * 1.5)
                .move_to(xt[i * 28 + j].get_center() + OUT * v * 1.5 / 2)
                .set_color(GREY_B)
            )
            return line

        output_lines = SGroup(
            *[get_output_line(i, j) for i in range(28) for j in range(28)]
        ).set_z_index(1)
        residual_lines = SGroup(
            *[get_residual_line(i, j) for i in range(28) for j in range(28)]
        ).set_z_index(1)
        self.playw(
            Transformr(xt_lines, residual_lines),
            *[GrowFromEdge(line, OUT) for line in output_lines],
        )

        ## 샘플 하나 꺼내기
        i, j = 13, 19
        sample = SGroup(output_lines[i * 28 + j], residual_lines[i * 28 + j])
        sample.save_state()
        self.cf.save_state()
        self.playwl(
            sample.animate.shift(OUT * 3),
            self.cf.animate.reorient(
                -1, 63, 0, (np.float32(0.44), np.float32(-0.22), np.float32(0.5)), 8.90
            ),
            lag_ratio=0.2,
            wait=0,
        )

        brace_noise = (
            Brace(sample[0].copy().rotate(PI / 2, axis=RIGHT), RIGHT, buff=0.1)
            .rotate(PI / 2, axis=RIGHT)
            .set_color(RED)
        )
        brace_noise_text = (
            Tex(
                r"\mathrm{noise} \mathrm{(output \,\, of \,\, }\epsilon_{\theta}\mathrm{)}",
                font_size=28,
            )
            .rotate(PI / 3, axis=RIGHT)
            .next_to(brace_noise, RIGHT, buff=0.1)
            .set_color(RED)
        )
        brace_residual = (
            Brace(sample[1].copy().rotate(PI / 2, axis=RIGHT), RIGHT, buff=0.1)
            .rotate(PI / 2, axis=RIGHT)
            .set_color(BLUE)
        )
        brace_residual_text = (
            Tex(r"\mathrm{residual}", font_size=28)
            .rotate(PI / 3, axis=RIGHT)
            .next_to(brace_residual, RIGHT, buff=0.1)
            .set_color(BLUE)
        )
        self.playw(
            FadeIn(brace_noise),
            FadeIn(brace_noise_text),
            FadeIn(brace_residual),
            FadeIn(brace_residual_text),
        )

        ## 약간 깎기
        sampling_eq = (
            Tex(
                r"\mathbf{x}_{t-1} = ",
                r"\frac{1}{\sqrt{\alpha_t}}\left(\mathbf{x}_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha_t}}}\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)\right) + \sigma_t\mathbf{z}",
            )
            .rotate(PI / 3, axis=RIGHT)
            .scale(0.75)
            .set_color(GREY_A)
            .next_to(xt_text, DOWN, buff=0.5)
        )
        epsilon_theta_part = sampling_eq[27:35].set_color(RED)
        xt_part = sampling_eq[12:14].set_color_by_gradient(BLUE, RED)
        self.playwl(
            self.cf.animate.reorient(
                0,
                52,
                0,
                (np.float32(0.16), np.float32(-0.84), np.float32(-0.41)),
                10.54,
            ),
            FadeIn(sampling_eq),
            lag_ratio=0.5,
        )


class actual_flow_matching(InteractiveScene, Scene2D):
    def construct(self):
        """
        ## Scene 4
        **핵심: Flow matching도 마찬가지로 실제로 봐야한다**
        1. Flow matching은 방향을 예측함
        2. 학습의 입력은 noise → clean 사이 위 길 아무 데서나, 학습때마다 어느 지점인지는 랜덤
        3. 출력은 항상 noise → clean 방향의 벡터
        4. flow matching은 방향을 가지고 시간에 따라 누적해서 데이터를 만듦
        5. 그렇다면 처음에 설명한 약간 돌아가는 이거, 이거는 뭘까?
        6. diffusion은 정확한 지점으로 약간씩 감을 반복
        """
        scale = 0.0625
        ## img, noise, xt는 이전 씬에서 복붙
        img_array = mnist.data[0].numpy() / 255.0
        img = VGroup(
            *[
                Square(fill_color=interpolate_color(BLACK, WHITE, v), fill_opacity=1)
                .scale(scale)
                .set_stroke(width=0.5, color=GREY_D)
                for v in img_array.flatten()
            ]
        ).arrange_in_grid(28, 28, buff=0)

        noise_array = np.random.uniform(-0.5, 0.5, img_array.shape)
        img_noise = VGroup(
            *[
                Square(
                    fill_color=(
                        interpolate_color(BLACK, WHITE, v)
                        if v >= 0
                        else interpolate_color(BLACK, RED, -v)
                    ),
                    fill_opacity=1,
                )
                .scale(scale)
                .set_stroke(width=0.5, color=GREY_D)
                for v in noise_array.flatten()
            ]
        ).arrange_in_grid(28, 28, buff=0)

        xt_array = 0.5 * img_array + (1 - 0.5) * noise_array
        xt = VGroup(
            *[
                Square(
                    fill_color=(
                        interpolate_color(BLACK, WHITE, v)
                        if v >= 0
                        else interpolate_color(BLACK, RED, -v)
                    ),
                    fill_opacity=1,
                )
                .scale(scale)
                .set_stroke(width=0.5, color=GREY_D)
                for v in xt_array.flatten()
            ]
        ).arrange_in_grid(28, 28, buff=0)

        VGroup(img, xt, img_noise).arrange(RIGHT, buff=1)

        self.playw(FadeIn(img), FadeIn(img_noise), FadeIn(xt))

        ## 높이로 표현

        def get_line(i, j, array=img_array):
            v = array[i, j]
            scale = 0.08
            line = (
                Prism(width=scale, height=scale, depth=v * 1.5)
                .move_to(img[i * 28 + j].get_center() + OUT * v * 1.5 / 2)
                .set_color(GREY_B)
            )
            return line

        def get_noise_line(i, j):
            v = noise_array[i, j]
            scale = 0.08
            line = (
                Prism(width=scale, height=scale, depth=v * 1.5)
                .move_to(img_noise[i * 28 + j].get_center() + OUT * v * 1.5 / 2)
                .set_color(
                    interpolate_color(BLACK, WHITE, v)
                    if v >= 0
                    else interpolate_color(BLACK, RED, -v)
                )
            )
            return line

        def get_xt_line(i, j):
            v = xt_array[i, j]
            scale = 0.08
            line = (
                Prism(width=scale, height=scale, depth=v * 1.5)
                .move_to(xt[i * 28 + j].get_center() + OUT * v * 1.5 / 2)
                .set_color(
                    interpolate_color(BLACK, WHITE, v)
                    if v >= 0
                    else interpolate_color(BLACK, RED, -v)
                )
            )
            return line

        lines = SGroup(*[get_line(i, j) for i in range(28) for j in range(28)])
        noise_lines = SGroup(
            *[get_noise_line(i, j) for i in range(28) for j in range(28)]
        )
        xt_lines = SGroup(*[get_xt_line(i, j) for i in range(28) for j in range(28)])
        self.playw(
            *[GrowFromEdge(line, IN) for line in lines],
            *[GrowFromEdge(line, IN) for line in noise_lines],
            *[GrowFromEdge(line, IN) for line in xt_lines],
            run_time=0.7,
        )
        self.playw(
            self.cf.animate.reorient(
                0, 57, 0, (np.float32(0.02), np.float32(0.08), np.float32(0.12)), 9.95
            )
        )

        ## text
        img_text = (
            Tex("x_1").next_to(img, UP, buff=1.5).rotate(PI / 3, axis=RIGHT).shift(OUT)
        )
        noise_text = (
            Tex("x_0")
            .next_to(img_noise, UP, buff=1.5)
            .rotate(PI / 3, axis=RIGHT)
            .shift(OUT)
        )
        xt_text = (
            Tex("x_t").next_to(xt, UP, buff=1.5).rotate(PI / 3, axis=RIGHT).shift(OUT)
        )
        self.playw(FadeIn(img_text), FadeIn(noise_text), FadeIn(xt_text))

        ## square instead of prism for vector field
        def get_square(i, j, array=img_array):
            v = array[i, j]
            square = (
                Square()
                .scale(scale)
                .move_to(img[i * 28 + j].get_center() + OUT * v * 1.5)
                .set_stroke(width=0)
                .set_fill(
                    color=(
                        interpolate_color(GREY_E, WHITE, v)
                        if v >= 0
                        else interpolate_color(GREY_E, RED, -v)
                    ),
                    opacity=1,
                )
            )
            line = Line(
                img[i * 28 + j].get_center(),
                square.get_center(),
                stroke_width=1,
                color=GREY_B,
            )
            return VGroup(square, line)

        def get_noise_square(i, j):
            v = noise_array[i, j]
            square = (
                Square()
                .scale(scale)
                .move_to(img_noise[i * 28 + j].get_center() + OUT * v * 1.5)
                .set_stroke(width=0)
                .set_fill(
                    color=(
                        interpolate_color(GREY_E, WHITE, v)
                        if v >= 0
                        else interpolate_color(GREY_E, RED, -v)
                    ),
                    opacity=1,
                )
            )
            line = Line(
                img_noise[i * 28 + j].get_center(),
                square.get_center(),
                stroke_width=1,
                color=GREY_B,
            )
            return VGroup(square, line)

        squares = VGroup(*[get_square(i, j) for i in range(28) for j in range(28)])
        noise_squares = VGroup(
            *[get_noise_square(i, j) for i in range(28) for j in range(28)]
        )

        self.playw(
            FadeOut(lines),
            FadeOut(noise_lines),
            FadeIn(squares),
            FadeIn(noise_squares),
            run_time=0.7,
        )

        ## xt up
        self.play(
            xt.animate.shift(UP * 5),
            xt_lines.animate.shift(UP * 5),
            xt_text.animate.shift(UP * 5),
        )

        ## vector field: x1 - x0
        squares, lines = VGroup(*[square[0] for square in squares]), VGroup(
            *[square[1] for square in squares]
        )
        noise_squares, noise_lines = VGroup(
            *[square[0] for square in noise_squares]
        ), VGroup(*[square[1] for square in noise_squares])
        right_shift = np.array([0, 0, 0]) - img.get_center()
        left_shift = np.array([0, 0, 0]) - img_noise.get_center()
        self.play(FadeOut(lines), FadeOut(noise_lines))
        self.playw(
            *[item.animate.shift(right_shift) for item in [squares]],
            *[item.animate.shift(left_shift) for item in [noise_squares]],
        )

        ## arrows for vector field
        arrows = VGroup()
        for i in range(28):
            for j in range(28):
                start = noise_squares[i * 28 + j].get_center()
                end = squares[i * 28 + j].get_center()
                vector = img_array[i, j] - noise_array[i, j]
                arrow = Arrow(
                    start, end, buff=0, thickness=1, tip_width_ratio=8
                ).set_color(
                    interpolate_color(GREY_E, WHITE, vector)
                    if vector >= 0
                    else interpolate_color(RED, GREY_E, -vector)
                )
                arrows.add(arrow)
        self.play(
            FadeOut(img),
            FadeOut(img_noise),
            FadeOut(img_text),
            FadeOut(noise_text),
            self.cf.animate.reorient(
                -78,
                86,
                0,
                (np.float32(0.55), np.float32(-0.09), np.float32(0.13)),
                4.87,
            ),
        )
        self.playw(FadeIn(arrows), run_time=0.7)

        dt = 0.1
        dt_arrows = VGroup()
        for arrow in arrows:
            dt_arrows.add(arrow.copy().scale(dt))

        for i, dt_arrow in enumerate(dt_arrows):
            vector = img_array[i // 28, i % 28] - noise_array[i // 28, i % 28]
            dt_arrow.next_to(
                xt[i].get_center() + xt_array[i // 28, i % 28] * OUT * 1.5,
                OUT if vector >= 0 else IN,
                buff=0,
            )
        self.remove(xt_text)
        self.playwl(
            Transformr(arrows.copy(), dt_arrows),
            self.cf.animate.reorient(
                -71,
                86,
                0,
                (np.float32(-0.56), np.float32(4.95), np.float32(0.03)),
                2.93,
            ),
            lag_ratio=0.1,
        )

        ## flow matching sampling
        sampling_eq = (
            Tex(
                r"\mathbf{x}_{t-1} = \mathbf{x}_t + \Delta t \cdot \mathbf{v}_\theta(\mathbf{x}_t, t)",
                font_size=36,
            )
            .rotate(PI / 2, axis=RIGHT)
            .rotate(PI / 2, axis=IN)
            .next_to(xt, RIGHT, buff=1.5)
            .shift(OUT * 2)
        )
        self.playw(
            FadeIn(sampling_eq),
            self.cf.animate.reorient(
                -89, 84, 0, (np.float32(-0.55), np.float32(4.9), np.float32(0.1)), 3.35
            ),
        )

        xt_part = sampling_eq[5:7]
        v_part = sampling_eq[-8:]
        self.playw(
            Indicate(xt_part, color=YELLOW, scale_factor=1.1),
            Indicate(xt_lines, color=YELLOW, scale_factor=1.0),
        )
        self.playw(
            Indicate(v_part, color=PURE_GREEN, scale_factor=1.1),
            Indicate(dt_arrows, color=PURE_GREEN, scale_factor=1.0),
        )


class paperFigure(InteractiveScene, Scene2D):
    def construct(self):
        """
        **핵심: Flow matching 논문에서의 비교 figure**
        1. 약간 돌아가는 궤적을 그리는 diffusion
        2. 직선 궤적을 따라가는 flow matching
        3. 정말 그럴까?
        """
        ## Scene 1
        cfm_fig = ImageMobject("cfm_fig.png").scale(0.75)
        self.playw(FadeIn(cfm_fig))

        ## FadeOut cfm_fig

        nump_diff = RaenimPlane()
        nump_diff.x_axis.set_opacity(0.75)
        nump_diff.y_axis.set_opacity(0.75)
        nump_cfm = RaenimPlane()
        nump_cfm.x_axis.set_opacity(0.75)
        nump_cfm.y_axis.set_opacity(0.75)

        VGroup(nump_diff, nump_cfm).arrange(RIGHT, buff=0.75)

        start_diff_arr = np.array([1.5, 1.5])
        start_cfm_arr = np.array([1.5, 1.5])
        end_diff_arr = np.array([-1.5, -1.5])
        end_cfm_arr = np.array([-1.5, -1.5])

        start_diff_dot = Dot(nump_diff.c2p(*start_diff_arr), radius=0.05).set_color(RED)
        start_cfm_dot = Dot(nump_cfm.c2p(*start_cfm_arr), radius=0.05).set_color(RED)
        end_diff_dot = Dot(nump_diff.c2p(*end_diff_arr), radius=0.05).set_color(GREEN)
        end_cfm_dot = Dot(nump_cfm.c2p(*end_cfm_arr), radius=0.05).set_color(GREEN)

        self.play(FadeOut(cfm_fig), FadeIn(nump_diff), FadeIn(nump_cfm), run_time=0.5)
        diffusion_text = (
            Text("Diffusion", font_size=24, font="Noto Sans KR")
            .next_to(nump_diff, UP)
            .set_color(GREY_A)
        )
        start_diff_text = (
            Text("start", font_size=18, font="Noto Sans KR")
            .next_to(start_diff_dot, DOWN, buff=0.1)
            .set_color(RED)
        )
        end_diff_text = (
            Text("end", font_size=18, font="Noto Sans KR")
            .next_to(end_diff_dot, DOWN, buff=0.1)
            .set_color(GREEN)
        )
        self.playw(
            FadeIn(start_diff_dot),
            FadeIn(end_diff_dot),
            FadeIn(diffusion_text),
            FadeIn(start_diff_text),
            FadeIn(end_diff_text),
        )

        ## Diffusion 궤적
        diff1_arr = np.array([0.3, 2.25])
        path = (
            BrokenLine(
                start_diff_dot.get_center(),
                nump_diff.c2p(*diff1_arr),
                end_diff_dot.get_center(),
                smooth=True,
            )
            .set_color_by_gradient(RED, GREEN)
            .set_stroke(width=2)
        )
        t_dot = Dot(path.point_from_proportion(0), radius=0.07).set_color(RED)
        value = ValueTracker(0)
        T = 1000
        t_text = (
            Text(f"t = {int(T-T*value.get_value())}", font_size=18, font="Noto Sans KR")
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(RED)
        )
        self.add(t_dot, t_text)
        t_dot_fn = lambda m: m.move_to(
            path.point_from_proportion(value.get_value() ** 0.001)
        ).set_color(interpolate_color(RED, GREEN, value.get_value()))
        t_dot.add_updater(t_dot_fn)
        t_text_fn = lambda m: m.become(
            Text(
                f"t = {int(T-T*value.get_value())}",
                font_size=18,
                font="Noto Sans KR",
            )
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(t_dot.get_color())
        )
        t_text.add_updater(t_text_fn)
        self.playw(value.animate.set_value(1), ShowCreation(path), run_time=3)

        ## reset
        value.set_value(0)

        t_dot.clear_updaters()
        t_text.clear_updaters()
        self.playw(FadeOut(t_dot), FadeOut(t_text), FadeOut(path))

        ## diffusion with img
        img_float = img_array / 255.0

        def get_img_array(t, noise=[], optimal=True):
            if optimal:
                if not noise:
                    noise.append(np.random.uniform(0, 1, img_float.shape))
                noise = noise[0]
                return (1 - t) * img_float + t * noise
            else:
                if not noise:
                    noise.append(np.random.uniform(0, 1, img_float.shape))
                    noise.append(np.random.uniform(0, 1, img_float.shape))
                another = noise[1]
                noise_arr = noise[0]
                keep = 0.25
                if t > keep:
                    v = (1 - t) / (1 - keep)
                    return (1 - v) * noise_arr + v * another
                s = t / keep
                return (1 - s) * img_float + s * another

        def get_img(t):
            img_t_array = get_img_array(1 - t, optimal=False)
            img = VGroup(
                *[
                    Square(
                        fill_color=interpolate_color(BLACK, WHITE, v), fill_opacity=1
                    )
                    .scale(0.015)
                    .set_stroke(width=0)
                    for v in img_t_array.flatten()
                ]
            ).arrange_in_grid(28, 28, buff=0)
            return img

        t_dot = Dot(nump_diff.c2p(*start_diff_arr), radius=0.07).set_color(RED)
        t_text = (
            Text(f"t = {int(T-T*value.get_value())}", font_size=18, font="Noto Sans KR")
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(RED)
        )
        img_t = get_img(value.get_value()).next_to(t_dot, LEFT, buff=0.15)
        self.add(t_dot, t_text, img_t)
        t_dot_fn = lambda m: m.move_to(
            path.point_from_proportion(value.get_value() ** 0.001)
        ).set_color(interpolate_color(RED, GREEN, value.get_value()))
        t_dot.add_updater(t_dot_fn)
        t_text_fn = lambda m: m.become(
            Text(
                f"t = {int(T-T*value.get_value())}",
                font_size=18,
                font="Noto Sans KR",
            )
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(t_dot.get_color())
        )
        t_text.add_updater(t_text_fn)
        img_t_fn = lambda m: m.become(
            get_img(value.get_value()).next_to(t_text, LEFT, buff=0.15)
        )
        img_t.add_updater(img_t_fn)
        self.playw(value.animate.set_value(1), ShowCreation(path), run_time=3)

        ## reset diffusion's updater
        t_dot.clear_updaters()
        t_text.clear_updaters()
        img_t.clear_updaters()

        ## cfm 궤적
        cfm_text = (
            Text("Flow matching", font_size=24, font="Noto Sans KR")
            .next_to(nump_cfm, UP)
            .set_color(GREY_A)
        )
        start_cfm_text = (
            Text("start", font_size=18, font="Noto Sans KR")
            .next_to(start_cfm_dot, DOWN, buff=0.1)
            .set_color(RED)
        )
        end_cfm_text = (
            Text("end", font_size=18, font="Noto Sans KR")
            .next_to(end_cfm_dot, DOWN, buff=0.1)
            .set_color(GREEN)
        )
        self.playw(
            FadeIn(start_cfm_dot),
            FadeIn(end_cfm_dot),
            FadeIn(cfm_text),
            FadeIn(start_cfm_text),
            FadeIn(end_cfm_text),
        )

        ## cfm path
        cfm_value = ValueTracker(0)
        cfm_path = (
            Line(start_cfm_dot.get_center(), end_cfm_dot.get_center())
            .set_color_by_gradient(RED, GREEN)
            .set_stroke(width=2)
        )
        t_dot = Dot(cfm_path.point_from_proportion(0), radius=0.07).set_color(RED)
        t_text = (
            Text(
                f"t = {1-cfm_value.get_value():.2f}", font_size=18, font="Noto Sans KR"
            )
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(RED)
        )
        self.add(t_dot, t_text)
        t_dot_fn = lambda m: m.move_to(
            cfm_path.point_from_proportion(cfm_value.get_value() ** 0.001)
        ).set_color(interpolate_color(RED, GREEN, cfm_value.get_value()))
        t_dot.add_updater(t_dot_fn)
        t_text_fn = lambda m: m.become(
            Text(
                f"t = {1-cfm_value.get_value():.2f}",
                font_size=18,
                font="Noto Sans KR",
            )
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(t_dot.get_color())
        )
        t_text.add_updater(t_text_fn)
        self.playw(cfm_value.animate.set_value(1), ShowCreation(cfm_path), run_time=3)

        ## reset_cfm
        cfm_value.set_value(0)
        t_dot.clear_updaters()
        t_text.clear_updaters()
        self.playw(FadeOut(t_dot), FadeOut(t_text), FadeOut(cfm_path))

        ## cfm with img
        def get_cfm_img(t):
            img_t_array = get_img_array(1 - t)
            img = VGroup(
                *[
                    Square(
                        fill_color=interpolate_color(BLACK, WHITE, v), fill_opacity=1
                    )
                    .scale(0.015)
                    .set_stroke(width=0)
                    for v in img_t_array.flatten()
                ]
            ).arrange_in_grid(28, 28, buff=0)
            return img

        t_dot = Dot(nump_cfm.c2p(*start_cfm_arr), radius=0.07).set_color(RED)
        t_text = (
            Text(
                f"t = {1-cfm_value.get_value():.2f}", font_size=18, font="Noto Sans KR"
            )
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(RED)
        )
        img_t = get_cfm_img(cfm_value.get_value()).next_to(t_dot, LEFT, buff=0.15)
        self.add(t_dot, t_text, img_t)
        t_dot_fn = lambda m: m.move_to(
            cfm_path.point_from_proportion(cfm_value.get_value() ** 0.001)
        ).set_color(interpolate_color(RED, GREEN, cfm_value.get_value()))
        t_dot.add_updater(t_dot_fn)
        t_text_fn = lambda m: m.become(
            Text(
                f"t = {1-cfm_value.get_value():.2f}",
                font_size=18,
                font="Noto Sans KR",
            )
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(t_dot.get_color())
        )
        t_text.add_updater(t_text_fn)
        img_t_fn = lambda m: m.become(
            get_cfm_img(cfm_value.get_value()).next_to(t_text, LEFT, buff=0.15)
        )
        img_t.add_updater(img_t_fn)
        self.playw(cfm_value.animate.set_value(1), ShowCreation(cfm_path), run_time=3)


class whydiffusion_notoptimal(InteractiveScene, Scene2D):
    def construct(self):
        """
        ## Scene 5
        **핵심: Diffusion이 최적이 아닌 이유**
        1. 처음에 설명한 약간 돌아가는 diffusion, 이거는 뭘까?
        2. diffusion은 정확한 interpolation이 아님, 수식으로 확인
        """

        ## cfm_figure
        cfm_figure = ImageMobject("cfm_fig.png")
        self.playw(FadeIn(cfm_figure))

        #
        nump_diff = RaenimPlane()
        nump_diff.x_axis.set_opacity(0.75)
        nump_diff.y_axis.set_opacity(0.75)
        nump_cfm = RaenimPlane()
        nump_cfm.x_axis.set_opacity(0.75)
        nump_cfm.y_axis.set_opacity(0.75)

        VGroup(nump_diff, nump_cfm).arrange(RIGHT, buff=0.75)

        start_diff_arr = np.array([1.5, 1.5])
        start_cfm_arr = np.array([1.5, 1.5])
        end_diff_arr = np.array([-1.5, -1.5])
        end_cfm_arr = np.array([-1.5, -1.5])
        start_diff_dot = Dot(nump_diff.c2p(*start_diff_arr), radius=0.02).set_color(RED)
        xT = (
            Tex("x_T", font_size=36)
            .next_to(start_diff_dot, DR, buff=0.07)
            .set_color(RED)
        )
        start_cfm_dot = Dot(nump_cfm.c2p(*start_cfm_arr), radius=0.02).set_color(RED)
        x1 = (
            Tex("x_1", font_size=36)
            .next_to(start_cfm_dot, DOWN, buff=0.1)
            .set_color(RED)
        )
        end_diff_dot = Dot(nump_diff.c2p(*end_diff_arr), radius=0.02).set_color(GREEN)
        x0 = (
            Tex("x_0", font_size=36)
            .next_to(end_diff_dot, DOWN, buff=0.1)
            .set_color(GREEN)
        )
        end_cfm_dot = Dot(nump_cfm.c2p(*end_cfm_arr), radius=0.02).set_color(GREEN)
        x0_cfm = (
            Tex("x_0", font_size=36)
            .next_to(end_cfm_dot, DOWN, buff=0.1)
            .set_color(GREEN)
        )

        diffusion_text = (
            Text("Diffusion", font_size=24, font="Noto Sans KR")
            .next_to(nump_diff, UP)
            .set_color(GREY_A)
        )
        cfm_text = (
            Text("Flow matching", font_size=24, font="Noto Sans KR")
            .next_to(nump_cfm, UP)
            .set_color(GREY_A)
        )

        self.play(FadeOut(cfm_figure))
        self.playw(
            FadeIn(nump_diff),
            FadeIn(start_diff_dot),
            FadeIn(end_diff_dot),
            FadeIn(xT),
            FadeIn(x0),
            FadeIn(diffusion_text),
        )

        ## xt-1 given xt
        xt_1_diff = Tex(
            r"x_{t-1} = \frac{1}{\sqrt{\alpha_t}}\left(x_t - \frac{1-\alpha_t}{\sqrt{1-\bar{\alpha_t}}}\epsilon_\theta(x_t, t)\right) + \sigma_t z",
            font_size=28,
        ).next_to(nump_diff, RIGHT, buff=0.75)

        self.playw(FadeIn(xt_1_diff))
        sigma = xt_1_diff[-3:]
        self.playw(
            sigma.animate.set_color(RED),
            xt_1_diff[:-3].animate.set_color(GREY_C),
        )

        ## p(xt-1|xt)

        p_xt_1_given_xt = Tex(
            r"p(x_{t-1}|x_t) = \mathcal{N}\left(x_{t-1}; \mu_{\theta}(x_t, t),\, \sigma_t^2 I\right)",
            font_size=28,
        ).next_to(xt_1_diff, DOWN, buff=0.5)
        self.playw(FadeIn(p_xt_1_given_xt))

        sigma = p_xt_1_given_xt[-5:-1]
        self.playw(
            sigma.animate.set_color(RED),
            p_xt_1_given_xt[:-5].animate.set_color(GREY_C),
            p_xt_1_given_xt[-1:].animate.set_color(GREY_C),
        )

        ## get close to x0
        value = ValueTracker(0)
        T = 1000
        def update_dt_xt(mob, state=[]):
            t_idx = T - int(T * value.get_value())
            t = value.get_value()
            if len(state) == 0:
                state.append(start_diff_arr)
            current_state = state[0]
            epsilon = current_state - end_diff_arr
            beta_start = 0.0001
            beta_end = 0.02
            beta_t = beta_start + t * (beta_end - beta_start)
            alpha_t = 1 - beta_t
            alpha_bar_t = 1 - beta_t
            for i in range(1, t_idx):
                alpha_bar_t *= 1 - (beta_start + i * (beta_end - beta_start) / (T - 1))
            mu_theta = (current_state - beta_t / np.sqrt(1 - alpha_bar_t) * epsilon) / np.sqrt(alpha_t)
            get_sigma_t = lambda: ((1-alpha_bar_t / (1-(beta_start + i * (beta_end - beta_start) / (T - 1)))) / (1-alpha_bar_t) * beta_t)**0.5
            piui = np.random.normal(size=current_state.shape)
            next_state = mu_theta + (get_sigma_t() if t_idx > 1 else 0) * np.random.normal(size=current_state.shape) * -1
            state[0] = next_state
            mob.move_to(nump_diff.c2p(*next_state))

        t_dot = Dot(nump_diff.c2p(*start_diff_arr), radius=0.07).set_color(RED)
        trace = TracedPath(t_dot.get_center, stroke_color=RED, stroke_width=2)
        t_text = (
                Text(f"t = {value.get_value():.2f}", font_size=18, font="Noto Sans KR")
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(interpolate_color(RED, GREEN, value.get_value()))
        ).set_z_index(2)
        t_text_bg = SurroundingRectangle(t_text, color=BLACK, fill_color=BLACK, fill_opacity=0.5, buff=0.05).set_z_index(1)
        self.add(t_dot, t_text, t_text_bg, trace)
        t_dot.add_updater(update_dt_xt)
        t_text_fn = lambda m: m.become(
            Text(f"t = {T - int(T * value.get_value())}", font_size=18, font="Noto Sans KR")
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(interpolate_color(RED, GREEN, value.get_value()))
        )
        t_text.add_updater(t_text_fn)
        t_text_bg.add_updater(lambda m: m.move_to(t_text))
        self.play(value.animate.set_value(1), run_time=5)
        t_text.clear_updaters()
        t_dot.clear_updaters()
        t_text_bg.clear_updaters()

        ## clear texs
        self.playw(
            FadeOut(xt_1_diff),
            FadeOut(p_xt_1_given_xt),
        )


        ## cfm
        self.playw(
            FadeIn(nump_cfm),
            FadeIn(start_cfm_dot),
            FadeIn(end_cfm_dot),
            FadeIn(x1),
            FadeIn(x0_cfm),
            FadeIn(cfm_text),
        )

        ## cfm eq
        cfm_eq = Tex(
            r"x_{t-1} = x_t + \Delta t \cdot v_\theta(x_t, t)",
            font_size=28,
        ).move_to(nump_cfm.c2p(2.75, -1))
        v_part = cfm_eq[-8:].set_color_by_gradient(RED, GREEN)
        self.playw(FadeIn(cfm_eq))

        self.embed()
        ## cfm path
        cfm_value = ValueTracker(0)
        cfm_path = (
            Line(start_cfm_dot.get_center(), end_cfm_dot.get_center())
            .set_color_by_gradient(RED, GREEN)
            .set_stroke(width=2)
        )
        t_dot = Dot(cfm_path.point_from_proportion(0), radius=0.07).set_color(RED)
        t_text = (
            Text(
                f"t = {1-cfm_value.get_value():.2f}", font_size=18, font="Noto Sans KR"
            )
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(RED)
        )
        self.add(t_dot, t_text)
        t_dot_fn = lambda m: m.move_to(
            cfm_path.point_from_proportion(cfm_value.get_value() ** 0.001)
        ).set_color(interpolate_color(RED, GREEN, cfm_value.get_value()))
        t_dot.add_updater(t_dot_fn)
        t_text_fn = lambda m: m.become(
            Text(
                f"t = {1-cfm_value.get_value():.2f}",
                font_size=18,
                font="Noto Sans KR",
            )
            .next_to(t_dot, UP, buff=0.1, aligned_edge=RIGHT)
            .set_color(t_dot.get_color())
        )
        t_text.add_updater(t_text_fn)
        self.playw(cfm_value.animate.set_value(1), ShowCreation(cfm_path), run_time=3)