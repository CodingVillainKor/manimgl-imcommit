from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)

from torchvision.datasets import CIFAR100

cifar100 = CIFAR100(root="./data", download=True)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        model = Rectangle(
            width=4,
            height=2,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_color=GREY_B,
            stroke_width=2,
        ).set_z_index(1)
        modelt = Text("Text to Image", font_size=32).set_z_index(1.5)

        model = VGroup(model, modelt).set_z_index(1)
        self.playw(FadeIn(model))
        text_input = (
            Text(
                '"한강 위를 걷는 닭, 월리를 찾아서 그림체로"',
                font="Noto Sans KR",
                font_size=24,
            )
            .next_to(model, DOWN, buff=0.3)
            .set_color(GREEN)
        )
        self.playw(FadeIn(text_input))
        self.playw(FadeOut(text_input, shift=UP, scale=0.5))
        gemini = ImageMobject("gemini.png").scale(0.75).next_to(model, UP, buff=0.5)
        self.playwl(
            FadeIn(gemini, shift=UP * 3, scale=3),
            self.cf.animate.shift(UP).scale(1.2),
            lag_ratio=0.3,
        )

        ## p_theta(x|c)
        eq = (
            Tex(
                "X \\sim p_\\theta(x|c)",
            )
            .scale(1.5)
            .next_to(model, RIGHT, buff=0.3)
        )
        self.playwl(
            FadeIn(eq, shift=RIGHT),
            FadeOut(gemini),
            self.cf.animate.move_to(VGroup(model, eq)).scale(1 / 1.2),
            lag_ratio=0.3,
        )
        # scale up eq
        self.play(FadeOut(model))
        self.playw(eq.animate.scale(2), self.cf.animate.move_to(eq))

        ## highlight
        surrounding_theta = SurroundingRectangle(
            eq[3], color=RED, buff=0.05, stroke_width=3
        )
        surrounding_x = SurroundingRectangle(
            eq[5], color=RED, buff=0.05, stroke_width=3
        )
        surrounding_c = SurroundingRectangle(
            eq[7], color=RED, buff=0.05, stroke_width=3
        )
        self.playw(
            FadeIn(surrounding_theta), FadeIn(surrounding_x), FadeIn(surrounding_c)
        )

        ## question
        question_theta = Text("???").set_color(RED)
        question_x = Text("???").set_color(RED)
        question_c = Text("???").set_color(RED)

        question_vgroup = (
            VGroup(question_theta, question_x, question_c)
            .arrange(RIGHT, buff=1.5)
            .next_to(
                VGroup(surrounding_theta, surrounding_x, surrounding_c), DOWN, buff=1.5
            )
        )
        question_x.shift(DOWN * 0.75)
        arrow_theta = Arrow(
            question_theta.get_top(), surrounding_theta.get_bottom(), buff=0.1
        ).set_color(RED)
        arrow_x = Arrow(
            question_x.get_top(), surrounding_x.get_bottom(), buff=0.1
        ).set_color(RED)
        arrow_c = Arrow(
            question_c.get_top(), surrounding_c.get_bottom(), buff=0.1
        ).set_color(RED)

        self.play(FadeIn(question_theta), FadeIn(arrow_theta))
        self.play(
            FadeIn(question_x),
            FadeIn(arrow_x),
            self.cf.animate.move_to(VGroup(eq, question_vgroup)).scale(1.2),
        )
        self.playw(FadeIn(question_c), FadeIn(arrow_c))

        ## theta, x, c
        theta_text = (
            Text("Model Parameters", font_size=36)
            .set_color(GREEN)
            .move_to(question_theta)
            .align_to(question_theta, RIGHT)
        )
        x_text = (
            Text("Random Variables", font_size=36).set_color(GREEN).move_to(question_x)
        )
        c_text = (
            Text("Model Inputs", font_size=36)
            .set_color(GREEN)
            .move_to(question_c)
            .align_to(question_c, LEFT)
        )

        self.playw(
            Transformr(question_theta, theta_text),
            arrow_theta.animate.set_color(GREEN),
            surrounding_theta.animate.set_color(GREEN),
            wait=0.3,
        )
        self.playw(
            Transformr(question_x, x_text),
            arrow_x.animate.set_color(GREEN),
            surrounding_x.animate.set_color(GREEN),
            wait=0.3,
        )
        self.playw(
            Transformr(question_c, c_text),
            arrow_c.animate.set_color(GREEN),
            surrounding_c.animate.set_color(GREEN),
        )


class GaussianSampling(InteractiveScene, Scene2D):
    def construct(self):
        x_range = [-3, 3]

        ## gaussian distribution
        nump = RaenimPlane(x_range=x_range, y_range=[-2, 2]).scale(1.5)
        nump.y_axis.set_opacity(0)
        fn = lambda x: np.exp(-(x**2))
        gdist = nump.get_graph(fn, x_range=x_range)
        gdist.set_color_by_gradient(GREY, RED, GREEN, GREY)
        self.play(FadeIn(nump))
        self.playw(ShowCreation(gdist))

        ## sampling
        num = np.random.normal(0, 1, 1)[0]
        num_text = (
            Text(f"{num:.2f}", font_size=24)
            .set_color(interpolate_color(RED, GREEN, (num + 3) / 6))
            .next_to(nump.c2p(num, 0), DOWN, buff=0.1)
        )
        line = Line(
            nump.c2p(num, 0),
            nump.c2p(num, fn(num)),
            color=interpolate_color(RED, GREEN, (num + 3) / 6),
        )
        first = VGroup(nump, gdist, line, num_text)
        self.playw(ShowCreation(line), FadeIn(num_text), run_time=0.6)

        ## multiple sampling
        def get_sample():
            nump = RaenimPlane(x_range=x_range, y_range=[-2, 2]).scale(1.5)
            nump.y_axis.set_opacity(0)
            gdist = nump.get_graph(fn, x_range=x_range)
            gdist.set_color_by_gradient(GREY, RED, GREEN, GREY)

            num = np.random.normal(0, 1, 1)[0]
            num_text = Text(f"{num:.2f}", font_size=24)
            num_text.set_color(interpolate_color(RED, GREEN, (num + 3) / 6))
            num_text.next_to(nump.c2p(num, 0), DOWN, buff=0.1)
            line = Line(
                nump.c2p(num, 0),
                nump.c2p(num, fn(num)),
                color=interpolate_color(RED, GREEN, (num + 3) / 6),
            )
            return VGroup(nump, gdist, line, num_text)

        row, col = 4, 4
        samples = VGroup(*[get_sample() for _ in range(row * col - 1)])
        first_left = first.get_left()
        first_top = first.get_top()
        samples = (
            VGroup(first, *samples)
            .arrange_in_grid(n_rows=row, n_cols=col, buff=0.5)
            .align_to([first_left[0], first_top[1], 0], UL)
        )
        self.playwl(
            FadeIn(samples[1:], run_time=2),
            self.cf.animate.scale(2.5).move_to(samples),
            lag_ratio=0.5,
        )

        ## gather texts
        texts = VGroup(*[sample[3] for sample in samples]).copy().set_z_index(1)
        self.add(texts)
        self.play(FadeOut(samples))
        self.playw(
            texts.animate.arrange_in_grid(n_rows=row, n_cols=col, buff=0.5).move_to(
                self.cf
            ),
            self.cf.animate.scale(0.35),
        )

        boxes = VGroup(
            *[
                Rectangle(width=0.85, height=0.55)
                .move_to(text.get_center())
                .set_stroke(color=GREY_C, width=1.5)
                .set_fill(color=BLACK, opacity=1)
                for text in texts
            ]
        ).set_z_index(0.5)
        self.playw(FadeIn(boxes))

        boxes1, boxes2 = boxes.copy().set_z_index(0.25).shift(
            UR * 0.05
        ), boxes.copy().set_z_index(0).shift(UR * 0.1)
        self.playw(FadeIn(boxes1), FadeIn(boxes2))

        ## dotdotdot
        dot3 = (
            Text("...", font_size=32)
            .set_color(GREY_C)
            .rotate(-PI / 4)
            .next_to(boxes[-1], DR, buff=0.25)
        )
        self.playw(FadeIn(dot3))

        ## overlap image
        def dot_noise_image():
            row, col = 72, 100
            # noise = np.random.uniform(0, 1, size=(row, col, 3))
            noise = np.random.normal(0, 1, size=(row, col, 3)).clip(0, 1)
            dots = VGroup(
                *[
                    Square(
                        side_length=0.2,
                        color=Color(
                            "#{:02x}{:02x}{:02x}".format(
                                int(r * 255), int(g * 255), int(b * 255)
                            )
                        ),
                    )
                    .set_fill(opacity=1)
                    .set_stroke(width=0)
                    for r, g, b in noise.reshape(-1, 3)
                ]
            ).arrange_in_grid(n_rows=row, n_cols=col, buff=0)
            return dots

        dots = dot_noise_image().align_to(VGroup(boxes, boxes1, boxes2), UL)
        self.playwl(
            FadeOut(
                VGroup(boxes2, boxes1, boxes, dot3, texts),
                shift=UL * 0.6 + LEFT * 0.4,
                scale=0.6,
            ),
            FadeIn(dots),
            lag_ratio=0.5,
            wait=0.2,
        )
        dots.generate_target()
        dots.target.scale(0.2)
        self.playw(
            MoveToTarget(dots), self.cf.animate.move_to(dots.target).shift(DOWN * 0.75)
        )

        ## p(x) = N(0, I)
        eq = Tex(
            "p(\\boldsymbol{x}) = \\mathcal{N}(\\boldsymbol{x}; 0, I)", font_size=36
        ).next_to(dots, DOWN, buff=0.25)
        self.playw(FadeIn(eq, shift=DOWN * 0.5))
        comment = (
            Text("(clamp the numbers to be 0 < x < 1)", font_size=20, font="Noto Sans KR")
            .next_to(eq, RIGHT, buff=0.5)
            .set_color(GREY_C)
        )
        self.playw(FadeIn(comment, shift=RIGHT * 0.5))

        ## fadeout comment
        self.playw(FadeOut(comment, shift=RIGHT * 0.5))

        ## x is a noise of shape [row, col, channel]
        xc = eq[2].copy().set_color(GREEN_B)
        x_explanation = Words(
            ": Image of shape [row, col, channel]", font_size=20
        ).set_color(GREEN_B)
        xc_group = (
            VGroup(xc, x_explanation)
            .arrange(RIGHT, buff=0.1)
            .next_to(eq, DOWN, buff=0.15)
            .align_to(eq[2], LEFT)
        )
        self.play(Transformr(eq[2].copy(), xc))
        self.playwl(
            *[FadeIn(word) for word in x_explanation.words], lag_ratio=0.5, wait=0
        )
        self.playw(FlashAround(xc_group, color=GREEN_B, buff=0.1))

        ## image and p_theta(x|c)
        img = ImageMobject("gemini.png").scale(0.75).next_to(dots, RIGHT, buff=1)
        eq2 = Tex("p_\\theta(\\boldsymbol{x}|\\boldsymbol{c})", font_size=36).next_to(
            img, DOWN, buff=0.25
        )
        self.playw(FadeIn(img), self.cf.animate.shift(RIGHT * 3), FadeOut(xc_group))
        self.playw(FadeIn(eq2, shift=DOWN * 0.5))

        ## theta and c
        theta = eq2[1]
        condition = eq2[-2]

        self.playw(theta.animate.set_color(RED))
        self.playw(condition.animate.set_color(RED))




class condition(InteractiveScene, Scene2D):
    def construct(self):

        ## p(x)
        eq = Tex(
            "p(\\boldsymbol{x}) = \\mathcal{N}(\\boldsymbol{x}; 0, I)", font_size=36
        )
        self.playw(FadeIn(eq))

        ## get dots
        def dot_noise_image():
            row, col = 36, 50
            # noise = np.random.uniform(0, 1, size=(row, col, 3))
            noise = np.random.normal(0, 1, size=(row, col, 3)).clip(0, 1)
            dots = VGroup(
                *[
                    Square(
                        side_length=0.075,
                        color=Color(
                            "#{:02x}{:02x}{:02x}".format(
                                int(r * 255), int(g * 255), int(b * 255)
                            )
                        ),
                    )
                    .set_fill(opacity=1)
                    .set_stroke(width=0)
                    for r, g, b in noise.reshape(-1, 3)
                ]
            ).arrange_in_grid(n_rows=row, n_cols=col, buff=0)
            return dots

        dots = dot_noise_image().next_to(eq, UP, buff=0.5)
        self.playw(FadeIn(dots, shift=UP * 1.5, scale=2))

        ## resample 3 times

        for _ in range(3):
            new_dots = dot_noise_image().next_to(eq, UP, buff=0.5)
            self.playw(
                FadeOut(dots, shift=UP * 1.5), FadeIn(new_dots, shift=UP * 1.5, scale=2)
            )
            dots = new_dots

        ## conditioned p(x|c)
        eq2 = Tex(
            r"p(x \mid c) = \begin{cases} \mathcal{N}(x; \mathbf{0}, I) & \text{if } c = 0 \\ \mathcal{N}\left(x; \mathbf{1}, I\right) & \text{if } c = 1 \end{cases}",
            font_size=36,
        )

        self.play(FadeOut(dots), FadeOut(eq))
        self.playw(FadeIn(eq2))

        ol = self.overlay
        c1 = eq2[4].set_z_index(ol.z_index + 1)
        self.add(c1)
        self.playw(FadeIn(ol))
        c2 = eq2[-18:-13].copy().set_z_index(ol.z_index + 1)
        c3 = eq2[-5:].copy().set_z_index(ol.z_index + 1)
        self.playw(FadeIn(c2), FadeIn(c3))
        self.playw(FadeOut(ol))
        self.remove(c2, c3)

        ## c = 0
        def dot_conditioned_image(condition):
            row, col = 36, 50
            if condition == 0:
                noise = np.random.normal(0, 1, size=(row, col, 3)).clip(0, 1)
            else:
                noise = np.random.normal(1, 1, size=(row, col, 3)).clip(0, 1)
            dots = VGroup(
                *[
                    Square(
                        side_length=0.075,
                        color=Color(
                            "#{:02x}{:02x}{:02x}".format(
                                int(r * 255), int(g * 255), int(b * 255)
                            )
                        ),
                    )
                    .set_fill(opacity=1)
                    .set_stroke(width=0)
                    for r, g, b in noise.reshape(-1, 3)
                ]
            ).arrange_in_grid(n_rows=row, n_cols=col, buff=0)
            return dots

        input_c0 = (
            Text("c = 0", font_size=24).next_to(eq2, DOWN, buff=0.5).set_color(RED)
        )
        self.playw(FadeIn(input_c0))
        self.play(
            FadeOut(input_c0, shift=UP, scale=2), Indicate(eq2[-18:-13], color=RED)
        )

        dots_c0 = dot_conditioned_image(0).next_to(eq2, UP, buff=0.5)
        self.playw(
            FadeIn(dots_c0, shift=UP * 1.5, scale=2),
            Indicate(eq2[-26:-18], color=GREEN),
        )

        ## c = 1
        input_c1 = (
            Text("c = 1", font_size=24).next_to(eq2, DOWN, buff=0.5).set_color(RED)
        )
        self.playw(FadeIn(input_c1), FadeOut(dots_c0))
        self.play(FadeOut(input_c1, shift=UP, scale=2), Indicate(eq2[-5:], color=RED))
        dots_c1 = dot_conditioned_image(1).next_to(eq2, UP, buff=0.5)
        self.playw(
            FadeIn(dots_c1, shift=UP * 1.5, scale=2), Indicate(eq2[-13:-5], color=GREEN)
        )

        ## c = 0 three animations
        self.play(FadeOut(dots_c1))
        anims = []
        for _ in range(3):
            anim = []
            input_c0 = (
                Text("c = 0", font_size=24).next_to(eq2, DOWN, buff=0.5).set_color(RED)
            )
            anim.append(FadeIn(input_c0))
            anim.append(
                AnimationGroup(
                    FadeOut(input_c0, shift=UP, scale=2),
                    Indicate(eq2[-18:-13], color=RED),
                )
            )
            new_dots_c0 = dot_conditioned_image(0).next_to(eq2, UP, buff=0.5)
            anim.append(FadeIn(new_dots_c0, shift=UP * 1.5, scale=2))
            anim.append(FadeOut(new_dots_c0, shift=UP * 1.5))
            anims.append(anim)
        skewed_anims = SkewedAnimations(*anims)
        for anim in skewed_anims:
            self.play(*anim, run_time=0.7)
        self.wait()

        ## c = 1 three animations
        anims = []
        for _ in range(3):
            anim = []
            input_c1 = (
                Text("c = 1", font_size=24).next_to(eq2, DOWN, buff=0.5).set_color(RED)
            )
            anim.append(FadeIn(input_c1))
            anim.append(
                AnimationGroup(
                    FadeOut(input_c1, shift=UP, scale=2), Indicate(eq2[-5:], color=RED)
                )
            )
            new_dots_c1 = dot_conditioned_image(1).next_to(eq2, UP, buff=0.5)
            anim.append(FadeIn(new_dots_c1, shift=UP * 1.5, scale=2))
            anim.append(FadeOut(new_dots_c1, shift=UP * 1.5))
            anims.append(anim)
        skewed_anims = SkewedAnimations(*anims)
        for anim in skewed_anims:
            self.play(*anim, run_time=0.7)
        self.wait()

        ## overlay
        c1.set_z_index(0)
        self.play(FadeIn(ol))
        c0_text = Words("c = 0 → Gaussian noise", font_size=24).set_color(YELLOW_A)
        c1_text = Words("c = 1 → Brighter Gaussian noise", font_size=24).set_color(
            YELLOW_A
        )
        c1_text.words[4].set_color(YELLOW)

        texts = (
            VGroup(c0_text, c1_text)
            .arrange(DOWN, buff=0.25, aligned_edge=LEFT)
            .next_to(eq2, DOWN, buff=0.35)
            .set_z_index(ol.z_index + 1)
        )
        self.playw(FadeIn(texts))


class subscriptTheta(InteractiveScene, Scene2D):
    def construct(self):

        ## p_theta(x|c)

        pxc_eq = Tex("p_\\theta(x|c)", font_size=48)
        self.playw(FadeIn(pxc_eq))

        ## know x and c
        ol = self.overlay
        x = pxc_eq[3].set_z_index(ol.z_index + 1)
        self.add(x)
        self.playw(FadeIn(ol), x.animate.set_color(GREEN))

        x_text = (
            Words("Random Variable", font_size=24)
            .set_color(GREEN)
            .next_to(x, DOWN, aligned_edge=LEFT)
            .set_z_index(ol.z_index + 1)
        )
        self.playw(FadeIn(x_text))

        ## reset

        self.play(FadeOut(ol), x.animate.set_color(WHITE), FadeOut(x_text))
        x.set_z_index(0)
        ## know c
        c = pxc_eq[-2].set_z_index(ol.z_index + 1)
        self.add(c)
        self.playw(FadeIn(ol), c.animate.set_color(GREEN))

        c_text = (
            Words("User Input", font_size=24)
            .set_color(GREEN)
            .next_to(c, DOWN, aligned_edge=LEFT)
            .set_z_index(ol.z_index + 1)
        )
        self.playw(FadeIn(c_text))

        ## reset c
        self.play(FadeOut(ol), c.animate.set_color(WHITE), FadeOut(c_text))
        c.set_z_index(0)

        ## what is theta
        theta = pxc_eq[1].set_z_index(ol.z_index + 1)
        self.add(theta)
        self.playw(FadeIn(ol), theta.animate.set_color(RED))

        theta_text = (
            Words("???", font_size=32)
            .set_color(RED)
            .next_to(theta, DOWN, buff=0.75, aligned_edge=LEFT)
            .set_z_index(ol.z_index + 1)
        )
        arrow = (
            Arrow(theta_text.get_top(), theta.get_bottom(), buff=0.1, thickness=2)
            .set_z_index(ol.z_index + 1)
            .set_color(RED)
        )
        self.playw(FadeIn(theta_text), FadeIn(arrow))

        ## reset theta
        self.play(
            FadeOut(ol),
            theta.animate.set_color(WHITE),
            FadeOut(theta_text),
            FadeOut(arrow),
        )
        theta.set_z_index(0)

        ## gaussian dist. is not parameterized
        eq = Tex(
            r"p(x \mid c) = \begin{cases} \mathcal{N}(x; \mathbf{0}, I) & \text{if } c = 0 \\ \mathcal{N}\left(x; \mathbf{1}, I\right) & \text{if } c = 1 \end{cases}",
            font_size=36,
        ).next_to(pxc_eq, DOWN, buff=0.5, aligned_edge=LEFT)
        self.playw(
            FadeIn(eq, shift=DOWN * 0.5),
            self.cf.animate.shift(DOWN * 0.5),
            pxc_eq.animate.set_opacity(0.4),
        )
        ceq0 = eq[-18:-13]
        ceq1 = eq[-5:]

        no_theta = Tex("\\mathrm{No} \\ \\theta", font_size=40).next_to(
            eq[:2], DOWN, buff=0.75, aligned_edge=LEFT
        )
        arrow2 = Arrow(
            no_theta.get_top(), eq[:2].get_bottom(), buff=0.05, thickness=2
        ).set_color(GREY_B)
        self.playw(GrowArrow(arrow2), FadeIn(no_theta))

        ## gaussian noise
        def dot_conditioned_image(condition):
            row, col = 36, 50
            if condition == 0:
                noise = np.random.normal(0, 1, size=(row, col, 3)).clip(0, 1)
            else:
                noise = np.random.normal(1, 1, size=(row, col, 3)).clip(0, 1)
            dots = VGroup(
                *[
                    Square(
                        side_length=0.05,
                        color=Color(
                            "#{:02x}{:02x}{:02x}".format(
                                int(r * 255), int(g * 255), int(b * 255)
                            )
                        ),
                    )
                    .set_fill(opacity=1)
                    .set_stroke(width=0)
                    for r, g, b in noise.reshape(-1, 3)
                ]
            ).arrange_in_grid(n_rows=row, n_cols=col, buff=0)
            return dots

        dots_c0 = dot_conditioned_image(0).next_to(eq, UP, buff=0.5)
        dots_c1 = dot_conditioned_image(1).next_to(eq, UP, buff=0.5)

        dots = (
            VGroup(dots_c0, dots_c1).arrange(DOWN, buff=0.5).next_to(eq, RIGHT, buff=1)
        )
        self.play(
            FadeIn(dots_c0, shift=UR * 0.5 + RIGHT * 1.5, scale=3),
            self.cf.animate.move_to(dots).shift(LEFT * 1.5),
            Indicate(ceq0, color=GREEN),
        )
        self.playw(
            FadeIn(dots_c1, shift=DR * 0.5 + RIGHT * 1.5, scale=3),
            Indicate(ceq1, color=GREEN),
        )

        self.playw(RWiggle(dots_c0, amp=0.2), RWiggle(dots_c1, amp=0.2), run_time=5)

        ## ptheta(x|c) explanation
        self.cf.generate_target().reorient(
            0, 74, 0, (np.float32(3.77), np.float32(-0.95), np.float32(0.89)), 6.93
        )
        self.playw(
            MoveToTarget(self.cf),
            no_theta.animate.set_opacity(0.4),
            eq.animate.set_opacity(0.4),
            dots.animate.set_opacity(0.4),
            arrow2.animate.set_opacity(0.4),
            pxc_eq.animate.set_opacity(1)
            .rotate(74 * DEGREES, axis=RIGHT)
            .move_to(self.cf.target)
            .shift(OUT),
        )

        images = []

        def random_direction():
            directions = [
                OUT,
                IN,
                LEFT,
                (OUT + LEFT) / 2**0.5,
                (OUT + RIGHT) / 2**0.5,
                (IN + LEFT) / 2**0.5,
                (IN + RIGHT) / 2**0.5,
            ]
            return random.choice(directions)

        for i in range(8):
            array = cifar100.data[i]
            img = (
                PixelImage(array)
                .scale(0.15)
                .set_z_index(1)
                .rotate(74 * DEGREES, axis=RIGHT)
                .next_to(pxc_eq[1], random_direction(), buff=0.5)
            )
            images.append(img)

        anims = []
        for img in images:
            anim = []
            anim.append(FadeIn(img))
            anim.append(
                AnimationGroup(
                    FadeOut(
                        img, shift=pxc_eq[1].get_center() - img.get_center(), scale=0.5
                    ),
                    Indicate(pxc_eq[1], color=GREEN),
                    lag_ratio=0.5,
                )
            )
            anims.append(anim)
        skewed_anims = SkewedAnimations(*anims)
        for anim in skewed_anims:
            self.play(*anim, run_time=0.7)
        self.wait()

        ## generate image
        input_text = (
            Text('"Happy elephant!"', font_size=24)
            .rotate(74 * DEGREES, axis=RIGHT)
            .next_to(pxc_eq, IN)
            .set_color(GREEN)
        )
        self.playw(FadeIn(input_text), wait=0.5)
        self.playwl(
            FadeOut(
                input_text,
                shift=pxc_eq[-2].get_center() - input_text.get_center(),
                scale=0.5,
            ),
            Indicate(pxc_eq[-2], color=GREEN),
            lag_ratio=0.5,
            wait=0,
        )
        image = (
            PixelImage(cifar100.data[9])
            .scale(0.2)
            .set_z_index(1)
            .rotate(74 * DEGREES, axis=RIGHT)
            .next_to(pxc_eq, RIGHT, buff=0.75)
        )
        self.playwl(
            Indicate(pxc_eq, color=GREEN),
            FadeIn(image, shift=RIGHT, scale=2),
            lag_ratio=0.5,
        )


class conclusion(InteractiveScene, Scene2D):
    def construct(self):
        """
        ## Scene 4: 정리 - Gaussian sampling부터 모델까지
        1. 생성 모델이 만들어주는 거: 랜덤 샘플링
        2. Gaussian sampling: 노이즈만 만듦
        3. condition 넣으면 내가 원하는 의도 입력 가능
        4. subscript theta는 딥러닝 모델
        5. p_theta(x|c)를 이해할 수 있게 됨
        """
        ## pxc eq
        eq = Tex("p_\\theta(x|c)", font_size=48)
        self.playw(FadeIn(eq))

        ol = self.overlay

        ## fade in overlay and remain x
        x = eq[3].copy().set_z_index(ol.z_index + 1)
        self.add(x)
        self.playw(FadeIn(ol), x.animate.set_color(GREEN))

        text = (
            Text("Random Variable to generate", font_size=24)
            .set_color(GREEN)
            .next_to(x, UP, aligned_edge=LEFT)
            .set_z_index(ol.z_index + 1)
        )
        self.playw(FadeIn(text))

        ## fade in condition
        c = eq[-2].copy().set_z_index(ol.z_index + 1).set_opacity(0)
        self.add(c)
        self.play(c.animate.set_color(PURPLE).set_opacity(1))
        c_text = (
            Text("Condition to control the generation", font_size=24)
            .set_color(PURPLE)
            .next_to(c, DOWN, aligned_edge=LEFT)
            .set_z_index(ol.z_index + 1)
        )
        self.playw(FadeIn(c_text))


        self.embed()
        ## fade in theta
        theta = eq[1].copy().set_z_index(ol.z_index + 1).set_opacity(0)
        self.add(theta)
        self.play(theta.animate.set_color(ORANGE).set_opacity(1))

        theta_text = (
            Text("Model Parameters learned from data", font_size=24)
            .set_color(ORANGE)
            .next_to(theta, DOWN, aligned_edge=RIGHT)
            .set_z_index(ol.z_index + 1)
        )
        self.playw(FadeIn(theta_text))

        self.playw(self.cf.animate.scale(0.8), run_time=3)



