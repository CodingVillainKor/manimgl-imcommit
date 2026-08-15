from manimlib import *
from raenimgl import *
from random import seed, random as r

seed(41)
np.random.seed(41)

# ImageNet val samples, pre-extracted to PNG by prepare_images.py.
# springer/church have 5 images each, truck/parachute 1. No torch at render time.
IMGNET_LABELS = {
    "springer": "English springer",
    "church": "church",
    "truck": "garbage truck",
    "parachute": "parachute",
}


def imgnet_samples(label, n=5, **kwargs):
    if n == 1:
        return ImageMobject(f"imagenette/{label}_0.png", **kwargs)
    return Group(
        *[ImageMobject(f"imagenette/{label}_{i}.png", **kwargs) for i in range(n)]
    )


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        model_box = Rectangle(width=5.5, height=2.75, color=WHITE).set_fill(
            BLACK, opacity=0.55
        )
        model_text = Text("Model", font_size=24).align(model_box, UR, buff=0.15)
        model = VGroup(model_box, model_text)
        self.playw(FadeIn(model))

        ## text input

        text_input = Words('" 강호동 기껏 생각해낸 게 짤 "', font_size=24)
        text_input.words.arrange(RIGHT, buff=0.3, aligned_edge=UP).next_to(
            model, DOWN, buff=0.5
        ).set_color(GREY_B)
        text_boxes = VGroup(
            *[
                SurroundingRectangle(word, buff=0.1, color=GREEN)
                for word in text_input.words[1:-1]
            ]
        )
        text = VGroup(text_input, text_boxes).set_z_index(-1)
        self.play(FadeIn(text))
        self.playw(text.animate.move_to(model))

        ## camera right, Rwiggle model

        self.play(self.cf.animate.shift(RIGHT * 1.5))
        explain = (
            Text("강호동(1박2일 멤버), 모자란 생각하는 상황", font_size=24)
            .set_color(GREY_C)
            .next_to(model, RIGHT)
            .align(model, UP, buff=0.3)
        )
        hodong = (
            ImageMobject("hodong.png")
            .set_opacity(0.5)
            .scale(0.5)
            .next_to(explain, DOWN, buff=0.3)
        )

        self.playw(
            RWiggle(model, speed=0.5, amp=0.5, run_time=6),
            FadeIn(explain, shift=RIGHT * 0.5, run_time=1),
            FadeIn(hodong, shift=RIGHT * 0.5, run_time=1),
        )

        ## CLIP

        clip = (
            Text("CLIP", font_size=24).set_color(YELLOW).align(model_box, UR, buff=0.15)
        )
        self.play(Transform(model_text, clip))

        self.playw(FlashUnder(model_text, color=YELLOW), wait=5)


class naiveApproach(InteractiveScene, Scene2D):
    def construct(self):

        ## intro

        model_box = Rectangle(width=5.5, height=2.75, color=WHITE).set_fill(
            BLACK, opacity=0.55
        )
        model_text = Text("Model", font_size=24).align(model_box, UR, buff=0.15)
        model = VGroup(model_box, model_text).shift(UP * 0.5)

        self.addw(model)

        ## text input

        text_input = Words('" 강호동 기껏 생각해낸 게 짤 "', font_size=24)
        text_input.words.arrange(RIGHT, buff=0.3, aligned_edge=UP).next_to(
            model, DOWN, buff=0.5
        ).set_color(GREY_B)
        text_boxes = VGroup(
            *[
                SurroundingRectangle(word, buff=0.1, color=GREEN)
                for word in text_input.words[1:-1]
            ]
        )

        text = VGroup(text_input, text_boxes).set_z_index(-1)
        self.play(FadeIn(text))
        self.playw(text.animate.move_to(model))

        ## hodong as label

        hodong = (
            ImageMobject("hodong.png")
            .set_opacity(0.7)
            .scale(0.4)
            .next_to(model, UP, buff=0.3)
        )
        self.playw(FadeIn(hodong))

        ## train step

        self.play(FadeOut(hodong, shift=DOWN * 2, scale=0.5))
        self.playw(Indicate(model, scale_factor=1.1, color=GREEN), FadeOut(text))

        ## vice versa: input image, output text

        hodong.next_to(model, DOWN, buff=0.3).set_z_index(-1)
        text.next_to(model, UP, buff=0.3)

        self.play(FadeIn(hodong), run_time=0.5)
        self.playw(hodong.animate.move_to(model), FadeIn(text))
        self.play(FadeOut(text, shift=DOWN * 2, scale=0.5))
        self.playw(Indicate(model, scale_factor=1.1, color=GREEN), FadeOut(hodong))

        ## circumscribe

        self.playw(Circumscribe(model_box, buff=0), run_time=1.5)


class naiveBad(InteractiveScene, Scene2D):
    def construct(self):

        ## intro

        model_box = Rectangle(width=5.5, height=2.75, color=WHITE).set_fill(
            BLACK, opacity=0.55
        )
        model_text = Text("Model", font_size=24).align(model_box, UR, buff=0.15)
        model = VGroup(model_box, model_text).shift(UP * 0.5)

        self.addw(model)

        ## hodong as label

        hodong = (
            ImageMobject("hodong.png")
            .set_opacity(0.7)
            .scale(0.4)
            .next_to(model, DOWN, buff=0.3)
            .set_z_index(-1)
        )
        self.play(FadeIn(hodong))
        self.playw(hodong.animate.move_to(model))

        ## text input

        text_input = Words('" 강호동 기껏 생각해낸 게 짤 "', font_size=24)
        text_input.words.arrange(RIGHT, buff=0.3, aligned_edge=UP).next_to(
            model, DOWN, buff=0.3
        ).set_color(GREY_B)
        text_boxes = VGroup(
            *[
                SurroundingRectangle(word, buff=0.1, color=GREEN)
                for word in text_input.words[1:-1]
            ]
        )
        text = VGroup(text_input, text_boxes).set_z_index(-1)

        self.play(FadeIn(text))

        ## arrange

        self.playw(
            Group(hodong, text)
            .set_z_index(-1)
            .animate.arrange(RIGHT, buff=1.5)
            .shift(DOWN * 0.5),
            model.animate.shift(UP * 2).set_opacity(0.3),
        )

        ## circumscribe

        self.playwl(
            Circumscribe(hodong, color=RED),
            Circumscribe(text, color=RED),
            lag_ratio=0.5,
        )

        ## same image, different texts

        self.play(FadeOut(model, shift=UP), Group(hodong, text).animate.shift(UP * 0.5))

        text_input2 = Words('" 강호동 욕망의 항아리 짤 "', font_size=24)
        text_input2.words.arrange(RIGHT, buff=0.3, aligned_edge=UP).next_to(
            hodong, RIGHT, buff=1.5
        ).set_color(GREY_B)
        text_boxes2 = VGroup(
            *[
                SurroundingRectangle(word, buff=0.1, color=GREEN)
                for word in text_input2.words[1:-1]
            ]
        )
        text2 = (
            VGroup(text_input2, text_boxes2)
            .set_z_index(-1)
            .next_to(text, UP, aligned_edge=LEFT, buff=0.4)
        )

        text_input3 = Words('" 욕망의 항아리 기껏 생각해낸 게 "', font_size=24)
        text_input3.words.arrange(RIGHT, buff=0.3, aligned_edge=UP).next_to(
            hodong, RIGHT, buff=1.5
        ).set_color(GREY_B)
        text_boxes3 = VGroup(
            *[
                SurroundingRectangle(word, buff=0.1, color=GREEN)
                for word in text_input3.words[1:-1]
            ]
        )
        text3 = (
            VGroup(text_input3, text_boxes3)
            .set_z_index(-1)
            .next_to(text, DOWN, aligned_edge=LEFT, buff=0.4)
        )

        self.playw(FadeIn(text2))
        self.playw(FadeIn(text3))

        ## fadeout text2, 3
        self.playw(FadeOut(text2), FadeOut(text3))

        ## hodong2

        hodong2 = (
            ImageMobject("hodong2.png")
            .set_opacity(0.7)
            .scale(0.4)
            .next_to(hodong, UP, buff=0.3)
            .set_z_index(-1)
        )
        self.playw(FadeIn(hodong2))


class dimensions(InteractiveScene, Scene2D):
    def construct(self):
        ## intro
        dogs = imgnet_samples("springer").scale(0.3).arrange(RIGHT, buff=0.5)
        prompt_dog = Text("흰색 검은색 섞인 강아지", font_size=24).next_to(
            dogs, LEFT, buff=0.5
        )

        churches = imgnet_samples("church").scale(0.3).arrange(RIGHT, buff=0.5)
        prompt_church = Text("유럽 풍의 멋진 교회", font_size=24).next_to(
            churches, LEFT, buff=0.5
        )

        dog = Group(dogs, prompt_dog).shift(UP * 1.5 + RIGHT * 0.5)
        church = Group(churches, prompt_church).shift(DOWN * 0.5 + RIGHT * 0.5)
        self.play(FadeIn(prompt_dog))
        self.playwl(*[FadeIn(d) for d in dogs], lag_ratio=0.5, wait=0)
        self.play(FadeIn(prompt_church), run_time=0.5)
        self.playwl(*[FadeIn(c) for c in churches], lag_ratio=0.3, wait=0)

        ## one prompt, one dog

        prompt = prompt_dog.copy()
        dog = dogs[2].copy()

        self.add(prompt, dog)
        self.play(
            FadeOut(churches),
            FadeOut(prompt_church),
            FadeOut(dogs),
            FadeOut(prompt_dog),
        )

        self.play(Group(prompt, dog).animate.arrange(RIGHT, buff=0.5))

        ## dashed rectangle
        dashed_rect = SurroundingRectangle(
            Group(prompt, dog), buff=0.3, color=GREEN, stroke_width=2
        )
        self.playw(FadeIn(dashed_rect), run_time=1.5)

        ## model

        model_box = Rectangle(width=5.5, height=2.75, color=WHITE).set_fill(
            BLACK, opacity=0.55
        )
        model_text = Text("Model", font_size=24).align(model_box, UR, buff=0.15)
        model = VGroup(model_box, model_text).next_to(dashed_rect, UP)

        self.play(FadeIn(model))
        drpd = Group(dashed_rect, prompt, dog).set_z_index(-1)
        self.playwl(
            FadeOut(drpd, shift=UP * 2),
            Indicate(model, scale_factor=1.05, color=GREEN),
            lag_ratio=0.7,
            wait=0,
        )

        self.play(model.animate.move_to(ORIGIN).shift(UP * 0.5))
        prompt2 = Text('" 흑백 색깔 개 "', font_size=24).next_to(model, DOWN, buff=0.5)
        self.playw(FadeIn(prompt2))
        self.playw(
            FadeOut(prompt2, shift=UP * 2),
            model_box.animate.set_stroke(color=RED),
            model_text.animate.set_color(PURE_RED),
        )


class clipischoice(InteractiveScene, Scene2D):
    def construct(self):
        ## intro
        model_box = (
            Rectangle(width=5.5, height=2.75, color=WHITE)
            .set_fill(BLACK, opacity=0.55)
            .set_z_index(-0.5)
        )
        model_text = (
            Text("CLIP", font_size=24).align(model_box, UR, buff=0.15).set_color(YELLOW)
        )
        model = VGroup(model_box, model_text).shift(DOWN * 0.5)

        self.play(FadeIn(model_text, scale=0.7))
        self.playw(FadeIn(model_box))

        ## contrastive learning
        cl_t = (
            Words("Contrastive Learning", font_size=32)
            .next_to(model, UP, buff=0.5)
            .set_color_by_gradient(YELLOW, YELLOW_A)
        )

        church = imgnet_samples("church", n=1).scale(0.3).arrange(RIGHT, buff=0.5)
        dog = imgnet_samples("springer", n=1).scale(0.3).arrange(RIGHT, buff=0.5)
        truck = imgnet_samples("truck", n=1).scale(0.3).arrange(RIGHT, buff=0.5)
        parachute = imgnet_samples("parachute", n=1).scale(0.3).arrange(RIGHT, buff=0.5)

        dog_t = (
            Words("풀밭의 흰색 검은색 강아지", font_size=24)
            .move_to(model)
            .set_z_index(-1)
        )

        items = (
            Group(church, dog, truck, parachute)
            .arrange(RIGHT, buff=0.5)
            .next_to(model, UP)
        )
        self.playwl(*[FadeIn(t) for t in cl_t.words], lag_ratio=0.7)
        self.playw(FadeTransform(cl_t, items), FadeIn(dog_t))
        ## dashed line
        line = DashedLine(
            start=dog_t.get_top(),
            end=dog.get_bottom(),
            color=GREEN,
            stroke_width=2,
            buff=0.1,
        ).set_z_index(-1)
        self.playw(Create(line))

        ## text2, normal train
        model_text2 = Text("Model", font_size=24).align(model_box, UR, buff=0.15)

        self.playw(Transform(model_text, model_text2))
        self.play(FadeOut(church), FadeOut(truck), FadeOut(parachute), FadeOut(line))
        self.playw(dog.animate.next_to(model, UP, buff=0.5))

        ## train
        self.play(FadeOut(dog, shift=DOWN * 2))
        self.playw(Indicate(model, scale_factor=1.1, color=GREEN), FadeOut(dog_t))

        self.playw(FadeIn(dog_t))
        self.playw(FlashUnder(dog_t, color=GREEN))

        self.playw(FadeIn(dog))


class question(InteractiveScene, Scene2D):
    def construct(self):
        ## intro

        model_box = (
            Rectangle(width=5.5, height=2.75, color=WHITE)
            .set_fill(BLACK, opacity=0.55)
            .set_z_index(-0.5)
        )
        model_text = (
            Text("CLIP", font_size=24).align(model_box, UR, buff=0.15).set_color(YELLOW)
        )
        model = VGroup(model_box, model_text).shift(DOWN * 0.5)

        dog = imgnet_samples("springer", n=1).scale(0.3)
        w1 = Words("오답 1", font_size=24).set_color(RED)
        w2 = Words("오답 2", font_size=24).set_color(RED)
        w3 = Words("오답 3", font_size=24).set_color(RED)

        candidates = (
            Group(w1, w2, dog, w3).arrange(RIGHT, buff=0.5).next_to(model, UP, buff=0.5)
        )

        prompt = (
            Text("풀밭의 흰색 검은색 강아지", font_size=24)
            .move_to(model)
            .set_z_index(-1)
        )

        self.addw(model, prompt)

        ## fade in candidates
        self.play(*[FadeIn(c) for c in candidates])

        ## Wiggle

        self.playw(
            RWiggle(w1, amp=0.2), RWiggle(w2, amp=0.2), RWiggle(w3, amp=0.2), run_time=2
        )

        ## rotate
        angle = 71 * DEGREES
        all_things = Group(w1, w2, dog, w3, prompt, model)
        all_things.save_state()
        self.play(all_things.animate.rotate(-angle, axis=UP).shift(RIGHT * 4))

        ## candidates are minibatch

        church = imgnet_samples("church", n=1).scale(0.3)
        truck = imgnet_samples("truck", n=1).scale(0.3)
        dog = imgnet_samples("springer", n=1).scale(0.3)
        parachute = imgnet_samples("parachute", n=1).scale(0.3)

        t1 = Words("스산한 분위기 속 웅장한 교회", font_size=24).set_color(GREY_B)
        t2 = Words("도로 위 사다리가 있는 파란 트럭", font_size=24).set_color(GREY_B)
        t3 = Words("풀밭의 흰색 검은색 강아지", font_size=24).set_color(GREY_B)
        t4 = Words("하늘 위 낙하산을 펼친 사람", font_size=24).set_color(GREY_B)

        s1 = Group(church, t1).arrange(RIGHT, buff=0.5)
        s2 = Group(truck, t2).arrange(RIGHT, buff=0.5)
        s3 = Group(dog, t3).arrange(RIGHT, buff=0.5)
        s4 = Group(parachute, t4).arrange(RIGHT, buff=0.5)
        ss = (
            Group(s1, s2, s3, s4)
            .arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            .shift(LEFT * 2 + UP * 0.5)
        )

        self.playw(FadeIn(ss))

        ## circumscribe ss

        sr = SurroundingRectangle(ss, buff=0.4, color=GREEN, stroke_width=2)
        self.play(FadeIn(sr))
        self.playw(FadeOut(sr))

        ## restore all_things
        church.generate_target().move_to(all_things.saved_state[0])
        truck.generate_target().move_to(all_things.saved_state[1])
        dog.generate_target().move_to(all_things.saved_state[2])
        parachute.generate_target().move_to(all_things.saved_state[3])
        self.play(
            all_things.animate.restore(),
            FadeOut(VGroup(t1, t2, t3, t4)),
            *[MoveToTarget(mob) for mob in [church, truck, dog, parachute]],
        )

        self.playw(*[w.animate.shift(UP * 1) for w in [w1, w2, w3]])

        ## 정답
        wc = Text("정답", font_size=24).set_color(GREEN).next_to(dog, UP, buff=0.3)
        self.playw(FadeIn(wc, shift=UP * 0.3))

        ## lines

        lines = VGroup(
            DashedLine(
                start=prompt.get_top(),
                end=church.get_bottom(),
                color=RED,
                stroke_width=2,
                buff=0.1,
            ).set_z_index(-1),
            DashedLine(
                start=prompt.get_top(),
                end=truck.get_bottom(),
                color=RED,
                stroke_width=2,
                buff=0.1,
            ).set_z_index(-1),
            DashedLine(
                start=prompt.get_top(),
                end=dog.get_bottom(),
                color=GREEN,
                stroke_width=2,
                buff=0.1,
            ).set_z_index(-1),
            DashedLine(
                start=prompt.get_top(),
                end=parachute.get_bottom(),
                color=RED,
                stroke_width=2,
                buff=0.1,
            ).set_z_index(-1),
        )

        self.playw(*[Create(line) for line in lines])


class contrastiveLearning(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        church = imgnet_samples("church", n=1).scale(0.3)
        truck = imgnet_samples("truck", n=1).scale(0.3)
        dog = imgnet_samples("springer", n=1).scale(0.3)
        parachute = imgnet_samples("parachute", n=1).scale(0.3)

        imgs = Group(church, truck, dog, parachute)
        t1 = Words("스산한 분위기 속 웅장한 교회", font_size=24).set_color(GREY_B)
        t2 = Words("도로 위 사다리가 있는 파란 트럭", font_size=24).set_color(GREY_B)
        t3 = Words("풀밭의 흰색 검은색 강아지", font_size=24).set_color(GREY_B)
        t4 = Words("하늘 위 낙하산을 펼친 사람", font_size=24).set_color(GREY_B)
        texts = Group(t1, t2, t3, t4)

        imgs.arrange(DR, buff=-0.6)
        t1.next_to(imgs[0], RIGHT, buff=0.2).align(imgs[0], UP, buff=0.1)
        t2.next_to(imgs[1], RIGHT, buff=0.2).align(imgs[1], UP, buff=0.1)
        t3.next_to(imgs[2], RIGHT, buff=0.2).align(imgs[2], UP, buff=0.1)
        t4.next_to(imgs[3], RIGHT, buff=0.2).align(imgs[3], UP, buff=0.1)

        self.playw(FadeIn(imgs), FadeIn(texts))

        ## Indicate each image-text pair
        self.playwl(
            *[
                Indicate(Group(img, text), scale_factor=1.05, color=GREEN)
                for img, text in zip(imgs, texts)
            ],
            lag_ratio=0.5,
            wait=1,
        )

        ## image encoder, text encoder

        img_enc_box = (
            Polygon(
                [-1.5, 1.5, 0],
                [-2.5, -1.5, 0],
                [1, -1.5, 0],
                [0, 1.5, 0],
                color=WHITE,
            )
            .rotate(-PI / 2)
            .set_fill(GREEN_B, opacity=0.5)
            .set_z_index(-0.5)
        )
        img_enc_text = Text("Image Encoder", font_size=24).move_to(img_enc_box)
        img_enc = VGroup(img_enc_box, img_enc_text).shift(RIGHT * 8)

        text_enc_box = (
            Polygon(
                [-1.5, 1.5, 0],
                [-2.5, -1.5, 0],
                [1, -1.5, 0],
                [0, 1.5, 0],
                color=WHITE,
            )
            .rotate(-PI / 2)
            .set_fill(PURPLE_B, opacity=0.5)
            .set_z_index(-0.5)
        )
        text_enc_text = Text("Text Encoder", font_size=24).move_to(text_enc_box)
        text_enc = VGroup(text_enc_box, text_enc_text).next_to(img_enc, UP, buff=1.5)

        self.playwl(
            AnimationGroup(FadeIn(img_enc), FadeIn(text_enc)),
            self.cf.animate.scale(1.5)
            .move_to(Group(imgs, text_enc, img_enc))
            .shift(DOWN * 1),
            wait=0,
        )

        ## circumscribe encoders
        self.playw(Indicate(img_enc, color=GREEN))
        self.playw(Indicate(text_enc, color=PURPLE))

        ## prepare inputs

        self.playw(
            texts.animate.arrange(DOWN, aligned_edge=RIGHT, buff=0.5).next_to(
                text_enc, LEFT, buff=1.5
            ),
            imgs.animate.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            .scale(0.75)
            .next_to(img_enc, LEFT, buff=1.5),
            self.cf.animate.shift(RIGHT * 4),
        )

        ## input imgs to img_enc
        anims = []
        img_encoding = Tensor(4, buff=0.4).next_to(img_enc, RIGHT, buff=0.9)
        img_encoding.save_state()
        [ie.next_to(img_enc, RIGHT, buff=0.2) for ie in img_encoding]
        for i in range(4):
            anim = []
            anim.append(FadeTransform(imgs[i], img_encoding[i]))
            anim.append(img_encoding[i].animate.move_to(img_encoding.saved_state[i]))
            anims.append(anim)

        skewed_anims = SkewedAnimations(*anims)
        for i, a in enumerate(skewed_anims):
            if i != len(skewed_anims) - 1:
                self.play(*a, run_time=0.5)
            else:
                self.playw(*a, run_time=0.5)

        ## input texts to text_enc
        anims = []
        text_encoding = Tensor(4, buff=0.4).next_to(text_enc, RIGHT, buff=0.9)
        text_encoding.save_state()
        [te.next_to(text_enc, RIGHT, buff=0.2) for te in text_encoding]
        for i in range(4):
            anim = []
            anim.append(FadeTransform(texts[i], text_encoding[i]))
            anim.append(text_encoding[i].animate.move_to(text_encoding.saved_state[i]))
            anims.append(anim)

        skewed_anims = SkewedAnimations(*anims)
        for i, a in enumerate(skewed_anims):
            if i != len(skewed_anims) - 1:
                self.play(*a, run_time=0.5)
            else:
                self.playw(*a, run_time=0.5)

        ## brace B
        brace_img = Brace(img_encoding, direction=RIGHT, color=GREEN)
        brace_text = Brace(text_encoding, direction=RIGHT, color=PURPLE)
        text_img = Text("B", font_size=40, font=MONO_FONT).next_to(
            brace_img, RIGHT, buff=0.2
        )
        text_text = Text("B", font_size=40, font=MONO_FONT).next_to(
            brace_text, RIGHT, buff=0.2
        )

        self.playw(
            FadeIn(brace_img), FadeIn(brace_text), FadeIn(text_img), FadeIn(text_text)
        )

        ## circumscribe including brace B
        self.playw(Circumscribe(VGroup(img_encoding, brace_img, text_img), color=GREEN))
        self.playw(
            Circumscribe(VGroup(text_encoding, brace_text, text_text), color=PURPLE)
        )

        ## fadeout b right
        self.play(
            FadeOut(VGroup(brace_img, text_img, brace_text, text_text), shift=RIGHT),
            run_time=0.7,
        )

        ## randns

        img_randns = VGroup(
            *[
                randn(1, 9)
                .scale(0.5)
                .move_to(img_encoding[i])
                .align_to(img_encoding[i], LEFT)
                for i in range(4)
            ]
        )
        text_randns = VGroup(
            *[
                randn(1, 9)
                .scale(0.5)
                .move_to(text_encoding[i])
                .align_to(text_encoding[i], LEFT)
                for i in range(4)
            ]
        )
        img_encoding.save_state()
        text_encoding.save_state()
        self.playw(
            Transform(img_encoding, img_randns), Transform(text_encoding, text_randns)
        )
        self.playw(Restore(img_encoding), Restore(text_encoding))

        ## fadeout encoders

        self.play(FadeOut(img_enc, shift=LEFT), FadeOut(text_enc, shift=LEFT))
        ieg = img_encoding.generate_target()
        teg = text_encoding.generate_target()
        ieg.arrange(DOWN, buff=0.5)
        teg.arrange(RIGHT, buff=0.8)
        nums = VGroup(
            *[
                DecimalNumber(r() * 7 - 3.5, num_decimal_places=2, font_size=24)
                for i in range(4)
                for j in range(4)
            ]
        ).arrange_in_grid(4, 4, buff=0.7)
        ieg.next_to(nums, LEFT, buff=0.5)
        teg.next_to(nums, UP, buff=0.5)
        self.playw(
            self.cf.animate.move_to(ORIGIN).scale(1 / 1.5),
            MoveToTarget(img_encoding),
            MoveToTarget(text_encoding),
        )

        ## img_tag, text_tag
        img_tag = Text("Image encoding", font_size=24).next_to(
            img_encoding, DOWN, buff=0.2, aligned_edge=RIGHT
        )
        text_tag = Text("Text encoding", font_size=24).next_to(
            text_encoding, RIGHT, buff=0.2
        )
        self.play(FadeIn(img_tag))
        self.playw(FadeIn(text_tag))

        ## lines each pair
        lines = VGroup(
            *[
                DashedLine(
                    start=img_encoding[i].get_right(),
                    end=text_encoding[i].get_bottom(),
                    color=YELLOW_C,
                    stroke_width=2,
                    buff=0.1,
                ).set_z_index(-1)
                for i in range(4)
            ]
        )
        self.playw(*[Create(line) for line in lines])

        ## fadeout lines
        self.playw(FadeOut(lines), wait=4)

        ## transform
        self.playwl(
            *[
                Transformr(
                    VGroup(img_encoding[i], text_encoding[j]).copy(),
                    nums[i * 4 + j],
                )
                for i in range(4)
                for j in range(4)
            ],
            lag_ratio=0.2,
        )

        ## flashunder each num

        self.playwl(*[FlashUnder(num, color=YELLOW) for num in nums], lag_ratio=0.1)

        ## lines for img_encoding[0]
        lines_0 = VGroup(
            *[
                DashedLine(
                    start=img_encoding[0].get_right(),
                    end=text_encoding[i].get_bottom(),
                    color=GREEN if i == 0 else RED,
                    stroke_width=2,
                    buff=0.1,
                )
                for i in range(4)
            ]
        )

        self.playwl(*[Create(line) for line in lines_0], lag_ratio=0.5)

        ## fadeout lines_0

        self.play(FadeOut(lines_0))

        ## camera angle
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(
                -1, 78, 0, (np.float32(-0.27), np.float32(0.42), np.float32(1.11)), 8.00
            )
        )

        rotate = lambda x: x.rotate(72 * DEGREES, axis=RIGHT)

        ## bars
        idxs = rotate(
            VGroup(*[Text(f"answer {i+1}", font_size=24) for i in range(7)]).arrange(
                RIGHT, buff=0.5
            )
        ).shift(OUT * 1.5)
        bars = VGroup(
            *[
                rotate(
                    Rectangle(width=0.3, height=random.random() * 2 + 0.2).set_fill(
                        color=BLUE, opacity=0.5
                    )
                ).next_to(idxs[i], OUT)
                for i in range(7)
            ]
        )
        self.playw(FadeIn(idxs), FadeIn(bars))
        self.playw(
            bars[1].animate.set_fill(color=GREEN, opacity=0.9),
            idxs[1].animate.set_color(GREEN),
            *[bars[i].animate.set_opacity(0.2) for i in range(7) if i != 1],
            *[idxs[i].animate.set_color(GREY_B) for i in range(7) if i != 1],
        )

        ## fadeout and restore camera
        self.play(FadeOut(VGroup(bars, idxs)))
        self.playw(self.cf.animate.restore())

        ## two cross entropy axis
        hori_lines = VGroup(
            *[
                DashedLine(
                    nums[i * 4].get_left() + LEFT * 0.2,
                    nums[i * 4 + 3].get_right() + RIGHT * 0.2,
                    color=YELLOW_C,
                    stroke_width=2,
                )
                for i in range(4)
            ]
        )
        self.playwl(
            *[Create(line, run_time=0.5) for line in hori_lines], lag_ratio=0.2, wait=0
        )
        self.playwl(
            *[Uncreate(line, run_time=0.5) for line in hori_lines],
            lag_ratio=0.2,
        )

        ## vertical lines
        vert_lines = VGroup(
            *[
                DashedLine(
                    nums[i].get_top() + UP * 0.2,
                    nums[i + 12].get_bottom() + DOWN * 0.2,
                    color=YELLOW_C,
                    stroke_width=2,
                )
                for i in range(4)
            ]
        )
        self.playwl(
            *[Create(line, run_time=0.5) for line in vert_lines], lag_ratio=0.2, wait=0
        )
        self.playwl(
            *[
                Uncreate(line, run_time=0.5)
                for i, line in enumerate(vert_lines)
                if i != 1
            ],
            lag_ratio=0.2,
        )

        ## text1 and images
        text1 = (
            Text("도로 위 사다리가 있는 파란 트럭", font_size=24)
            .set_color(GREY_B)
            .next_to(text_encoding[1], UP, buff=0.3)
        )
        imgs.next_to(img_encoding, LEFT, buff=0.5)
        self.playw(
            FadeIn(text1, shift=UP * 0.2, scale=2),
            FadeIn(imgs, shift=LEFT * 0.3, scale=1.3),
            img_tag.animate.shift(DOWN * 0.5),
            *[nums[i].animate.set_opacity(0.2) for i in range(16) if i % 4 != 1],
        )

        ## label: 0 1 0 0 vertical

        label = VGroup(
            *[
                Text("0" if i // 4 != 1 else "1", font_size=24).set_color(GREEN).next_to(nums[i], RIGHT, buff=0.3)
                for i in [1, 5, 9, 13]
            ],
        )
        self.play(FadeIn(label, shift=RIGHT * 0.2))
        self.playw(Circumscribe(Group(imgs[1], label[1]), color=GREEN))

        self.play(FadeOut(label), FadeOut(text1), FadeOut(vert_lines[1]), nums.animate.set_opacity(0.2), FadeOut(imgs), img_tag.animate.shift(UP * 0.5))
        ## image2 and texts
        hl2 = DashedLine(
            nums[2 * 4].get_left() + LEFT * 0.2,
            nums[2 * 4 + 3].get_right() + RIGHT * 0.2,
            color=YELLOW_C,
            stroke_width=2,
        )
        for i in range(len(texts)):
            texts[i].next_to(text_encoding[i], UP, buff=0.4*(len(texts)-i+1)).shift(DOWN *0.7).set_color(text_encoding[i].get_color())
        self.playw(FadeIn(imgs[2], shift=LEFT * 0.8, scale=1.3), Create(hl2), nums[8:12].animate.set_opacity(1), FadeIn(texts))

        ## label: 0 0 1 0 horizontal
        label = VGroup(
            *[
                Text("0" if i != 10 else "1", font_size=24).set_color(GREEN).next_to(nums[i], UP, buff=0.1)
                for i in [8, 9, 10, 11]
            ],
        )
        self.play(FadeIn(label, shift=UP * 0.2))

        self.playw(Circumscribe(VGroup(label[2], nums[10]), color=text_encoding[2].get_color()))

        self.playw(FadeOut(label), FadeOut(hl2), FadeOut(imgs[2]), nums[8:12].animate.set_opacity(0.2), FadeOut(texts))

        ## set diagonal nums opacity to 1
        self.playw(
            *[nums[i * 4 + i].animate.set_opacity(1) for i in range(4)]
        )

        lines = VGroup(
            *[
                BrokenLine(
                    img_encoding[i].get_right(),
                    nums[i * 4 + i].get_center(),
                    text_encoding[i].get_bottom(),
                    stroke_width=2,
                    buff=0.1,
                ).set_color(GREEN)
                for i in range(4)
            ]
        )
        self.playwl(*[Create(line) for line in lines], lag_ratio=0.5)

        ## fadeout lines

        self.play(FadeOut(lines))

        ## set nums opacity to 1

        self.playw(*[nums[i].animate.set_opacity(1) for i in range(16)], wait=4)
        self.embed()
        ## diagonal nums to PURE_GREEN, others to PURE_RED
        self.playw(
            *[
                nums[i * 4 + i].animate.set_color(PURE_GREEN)
                for i in range(4)
            ],
            *[
                nums[i].animate.set_color(PURE_RED)
                for i in range(16)
                if i not in [0, 5, 10, 15]
            ]
        )