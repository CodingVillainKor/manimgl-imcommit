from manimlib import *
from raenimgl import *


class ARModel(InteractiveScene, Scene2D):
    def construct(self):
        # model

        model_box = Rectangle(
            width=4, height=2, stroke_color=GREY_A, fill_color=GREY_C, fill_opacity=1
        ).shift(UP)
        modelt = (
            Text("Autoregressive Model", font="Noto Sans KR", font_size=24, color=BLACK)
            .move_to(model_box.get_center())
            .set_z_index(1)
        )
        model = VGroup(model_box, modelt).set_z_index(2)
        self.playw(FadeIn(model))

        # words
        full_sentence = (
            "4월 초 샌프란시스코랑 LA 날씨를 검색해서 알려줘. </prompt> "
            + "4월 초 기준 샌프란시스코와 LA의 날씨는 다음과 같습니다. ..."
        )
        words = Words(full_sentence, font="Noto Sans KR", font_size=18).shift(DOWN)
        start_idx = 8

        prompt = words.words[:start_idx]
        prompt.save_state()
        prompt.move_to(ORIGIN).shift(DOWN)
        prompt[-1].set_opacity(0)
        self.playwl(
            *[FadeIn(w, shift=UP * 0.3) for w in words.words[:start_idx]],
            lag_ratio=0.2,
        )

        # prompt -> model -> output
        self.play(prompt[-1].animate.set_opacity(1), run_time=0.5)
        self.playw(Restore(prompt))
        model_input = prompt.copy()

        px = Tex(r"p(", "x_i", "|", r"x_{<i}", ")", font_size=28).next_to(
            model_box, RIGHT, buff=0.5
        )
        self.playw(FadeIn(px, shift=RIGHT * 0.5))

        self.playw(
            model_input.animate.scale(0.5)
            .move_to(model_box.get_center())
            .shift(RIGHT + UP * 0.5),
            FlashAround(px[-4:-1]),
        )

        answer = words.words[start_idx:].set_color(GREEN)
        self.playw(
            FadeIn(answer[0], shift=answer[0].get_center() - model_box.get_center())
        )
        self.playw(FlashAround(answer[0], buff=0.05), FlashAround(px[2:4], buff=0.05))

        # iteration
        for i in range(1, len(answer)):
            model_input = VGroup(prompt, answer[:i]).copy()
            self.play(
                model_input.animate.scale(0.3).move_to(model_box.get_center()),
                FlashAround(px[-4:-1]),
                run_time=0.5,
            )
            self.play(
                FadeIn(
                    answer[i], shift=answer[i].get_center() - model_box.get_center()
                ),
                FlashAround(px[2:4], buff=0.05),
                run_time=0.5,
            )
        self.wait()
        # flash each word
        self.playwl(
            *[FlashAround(w, buff=0.05, color=GREEN) for w in answer], lag_ratio=0.3
        )


class MDLModel(InteractiveScene, Scene2D):
    def construct(self):

        # model
        model_box = Rectangle(
            width=4, height=2, stroke_color=GREY_A, fill_color=GREY_C, fill_opacity=1
        ).shift(UP)
        modelt = (
            Text(
                "Masked Diffusion Language Model",
                font="Noto Sans KR",
                font_size=20,
                color=BLACK,
            )
            .move_to(model_box.get_center())
            .set_z_index(1)
        )
        model = VGroup(model_box, modelt).set_z_index(2)
        self.playw(FadeIn(model))

        # words
        full_sentence = (
            "4월 초 샌프란시스코랑 LA 날씨를 검색해서 알려줘. </prompt> "
            + "4월 초의 샌프란시스코와 LA의 날씨는 다음과 같습니다. ..."
        )
        words = Words(full_sentence, font="Noto Sans KR", font_size=18).shift(DOWN)
        start_idx = 8

        masked = (
            VGroup(
                *[
                    Square(side_length=0.3, fill_color=GREY_D, fill_opacity=1).move_to(
                        words.words[i].get_center()
                    )
                    for i in range(start_idx, len(words.words))
                ]
            )
            .arrange(RIGHT, buff=0.2)
            .next_to(words.words[start_idx - 1], RIGHT, buff=0.2)
        )
        prompt = words.words[:start_idx]

        self.playw(FadeIn(prompt))
        self.playw(FadeIn(masked))

        # a single diffusion step
        random_idx = list(range(len(words.words) - start_idx))
        random.shuffle(random_idx)
        idx_align = {idx: i for i, idx in enumerate(random_idx)}

        answer_unit = 2

        model_input = VGroup(prompt, masked).copy()
        self.play(model_input.animate.scale(0.3).move_to(model_box.get_center()))
        answer = words.words[start_idx:]
        for i, a in enumerate(answer):
            a.rotate(PI / 2).move_to(masked[i].get_center())

        answer0 = map(lambda i: answer[i], random_idx[:answer_unit])
        answer0 = VGroup(*answer0).set_color(GREEN)
        mask0 = VGroup(*[masked[i] for i in random_idx[:answer_unit]])
        self.playwl(
            AnimationGroup(
                *[
                    FadeIn(w, shift=w.get_center() - model_box.get_center())
                    for w in answer0
                ]
            ),
            FadeOut(mask0, shift=DOWN * 0.8),
            lag_ratio=0.3,
        )

        # iteration
        answers = VGroup(*answer0)
        mask_remain = VGroup(*[masked[i] for i in random_idx[answer_unit:]])
        for i in range(1, len(answer) // answer_unit):
            model_input = VGroup(prompt, answers, mask_remain).copy()
            self.play(
                model_input.animate.scale(0.3).move_to(model_box.get_center()),
                run_time=0.5,
            )
            answeri = map(
                lambda j: answer[j], random_idx[i * answer_unit : (i + 1) * answer_unit]
            )
            answeri = VGroup(*answeri).set_color(GREEN)
            maski = VGroup(
                *[
                    masked[j]
                    for j in random_idx[i * answer_unit : (i + 1) * answer_unit]
                ]
            )
            self.playwl(
                AnimationGroup(
                    *[
                        FadeIn(w, shift=w.get_center() - model_box.get_center())
                        for w in answeri
                    ]
                ),
                FadeOut(maski, shift=DOWN * 0.8),
                lag_ratio=0.3,
                run_time=0.8,
                wait=0,
            )
            answers.add(*answeri)
            mask_remain.remove(*maski)
        self.wait()
        self.embed()

        # flashing units
        """
        answer0 = VGroup(*[answer[i] for i in random_idx[:answer_unit]]).set_color(GREEN)
        answer1 = VGroup(*[answer[i] for i in random_idx[answer_unit:2*answer_unit]]).set_color(GREEN)
        ...
        """
        answers = VGroup(
            *[
                VGroup(
                    *[
                        answer[i]
                        for i in random_idx[j * answer_unit : (j + 1) * answer_unit]
                    ]
                ).set_color(GREEN)
                for j in range((len(answer) - 1) // answer_unit + 1)
            ]
        )
        answers_flattened = VGroup(*[w for ans in answers for w in ans])
        answers_ordered = VGroup(
            *[answers_flattened[idx_align[i]] for i in range(len(answers_flattened))]
        )
        answers_ordered.generate_target()
        for ans in answers_ordered.target:
            ans.rotate(-PI / 2)
        answers_ordered.target.arrange(RIGHT, buff=0.2).next_to(prompt, RIGHT, buff=0.2)

        self.play(MoveToTarget(answers_ordered))

        self.playwl(
            *[
                AnimationGroup(*[FlashAround(w, buff=0.05, color=GREEN) for w in ans])
                for ans in answers
            ],
            lag_ratio=0.9,
        )


class MDLModel_good(InteractiveScene, Scene2D):
    def construct(self):
        sentence = "4월 초 샌프란시스코랑 LA 날씨를 검색해서 알려줘. </prompt> 4월 초의 샌프란시스코와 LA의 날씨는 다음과 같습니다. ..."

        words = Words(sentence, font="Noto Sans KR", font_size=18)
        words = Words(sentence, font="Noto Sans KR", font_size=18)

        start_idx = 8
        words.words[start_idx:].set_color(GREEN)

        self.playw(FadeIn(words))

        # generation order in AR
        ar_text = (
            Text('" Autoregressive model "')
            .scale(0.5)
            .set_color_by_gradient(RED_A, RED)
            .next_to(words.words[start_idx:], UP)
        )
        self.playw(FadeIn(ar_text))
        for i in range(start_idx, len(words.words)):
            self.play(FlashAround(words.words[i], buff=0.05, color=GREEN), run_time=0.7)
        self.wait()

        # generation order in MDL
        mdl_text = (
            Text('" Masked Diffusion Language model "')
            .scale(0.5)
            .set_color_by_gradient(BLUE_A, BLUE)
            .next_to(words.words[start_idx:], UP)
        )
        self.playw(FadeOut(ar_text, shift=UP * 0.3), FadeIn(mdl_text, shift=UP * 0.3))

        random_idx = list(range(start_idx, len(words.words)))
        units = 2
        random.shuffle(random_idx)
        for i in range(0, len(random_idx), units):
            anims = []
            for j in range(i, min(i + units, len(random_idx))):
                idx = random_idx[j]
                anims.append(FlashAround(words.words[idx], buff=0.05, color=GREEN))
            self.play(*anims, run_time=0.7)
        self.wait()

        # fadeout text
        self.playw(FadeOut(mdl_text, shift=UP * 0.5))

        self.embed()
        # brace length
        brace = Brace(words.words[start_idx:], UP, buff=0.2).set_color(GREY_B)
        brace_text = (
            Tex(r"\text{length} = " + str(len(words.words) - start_idx))
            .scale(0.6)
            .next_to(brace, UP, buff=0.1)
        )
        self.play(FadeIn(brace))
        self.playw(FadeIn(brace_text))

        # # of calls
        ar_calls = (
            Words("Autoregressive: " + str(len(words.words) - start_idx))
            .scale(0.4)
            .set_color(RED)
        )
        mdl_calls = (
            Words(
                "Masked Diffusion: "
                + str((len(words.words) - start_idx - 1) // units + 1)
            )
            .scale(0.4)
            .set_color(BLUE)
        )

        calls = (
            VGroup(ar_calls, mdl_calls)
            .arrange(DOWN, aligned_edge=LEFT)
            .next_to(words.words[start_idx:], DOWN, aligned_edge=LEFT, buff=0.75)
        )
        self.playw(FadeIn(ar_calls.words[0]))
        self.play(FadeIn(ar_calls.words[1]))
        self.playwl(
            *[
                FlashAround(w, buff=0.05, color=RED, run_time=0.5)
                for w in words.words[start_idx:]
            ],
            lag_ratio=0.5,
        )
        self.playw(FadeIn(mdl_calls.words[:2]))
        self.play(FadeIn(mdl_calls.words[2]))
        for i in range(0, len(random_idx), units):
            anims = []
            for j in range(i, min(i + units, len(random_idx))):
                idx = random_idx[j]
                anims.append(FlashAround(words.words[idx], buff=0.05, color=BLUE))
            self.play(*anims, run_time=0.7)
        self.wait()


class ARModel_detail(InteractiveScene, Scene2D):
    def construct(self):
        # model
        model_box = Rectangle(
            width=9, height=2, stroke_color=GREY_A, fill_color=GREY_C, fill_opacity=0.7
        ).shift(UP)
        modelt = (
            Text("Autoregressive Model", font="Noto Sans KR", font_size=24, color=BLACK)
            .move_to(model_box.get_center())
            .set_z_index(1)
        )
        model = VGroup(model_box, modelt).set_z_index(2)
        self.playw(FadeIn(model))

        # words
        full_sentence = (
            "4월 초 샌프란시스코랑 LA 날씨를 검색해서 알려줘. </prompt> "
            + "4월 초 기준 샌프란시스코와 ..."
        )
        words = Words(full_sentence, font="Noto Sans KR", font_size=18).shift(DOWN)
        start_idx = 8

        prompt = words.words[:start_idx]
        self.playwl(FadeIn(prompt, shift=UP * 0.3), lag_ratio=0.2, wait=0)

        # rotate and arrange
        prompt.generate_target()
        for w in prompt.target:
            w.rotate(PI / 2)
        prompt.target.arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(
            prompt
        ).align_to(prompt, UL)
        self.playw(MoveToTarget(prompt))

        # first model inference
        output = (
            VGroup(
                *[
                    item.scale(0.7).next_to(prompt[i], UP)
                    for i, item in enumerate(Tensor(len(prompt), shape="square"))
                ]
            )
            .next_to(model_box, UP, buff=0.5)
            .align_to(prompt, LEFT)
        )
        self.playw(FadeTransform(prompt.copy(deep=True), output))

        idx = 0
        out_word = words.words[start_idx + idx].copy(deep=True)
        out_word.move_to(output[-1]).set_color(GREEN)
        words.words[start_idx + idx].next_to(
            prompt[-1], RIGHT, buff=0.25, aligned_edge=UP
        )
        self.playw(
            FadeOut(output[:-1], shift=UP * 0.5), Transformr(output[-1], out_word)
        )
        self.play(
            MoveAlongPath(
                out_word,
                BrokenLine(
                    out_word.get_center(),
                    (model_box.get_right()[0] + 0.5, out_word.get_center()[1], 0),
                    (
                        model_box.get_right()[0] + 0.5,
                        words.words[start_idx + idx].get_center()[1],
                        0,
                    ),
                    words.words[start_idx + idx].get_center(),
                ),
            ),
        )
        self.playw(
            out_word.animate.rotate(PI / 2)
            .next_to(prompt[-1], RIGHT, buff=0.25, aligned_edge=UP)
            .set_color(WHITE)
        )

        # iteration
        model_input = VGroup(*prompt.copy())
        result = VGroup(*prompt, out_word)
        for idx in range(1, len(words.words) - start_idx):
            model_input.add(out_word.copy())
            output = (
                VGroup(
                    *[
                        item.scale(0.7).next_to(model_input[i], UP)
                        for i, item in enumerate(
                            Tensor(len(model_input), shape="square")
                        )
                    ]
                )
                .next_to(model_box, UP, buff=0.5)
                .align_to(prompt, LEFT)
            )
            self.play(
                FadeTransform(model_input, output),
                run_time=0.5,
            )
            out_word = words.words[start_idx + idx].copy(deep=True)
            out_word.move_to(output[-1]).set_color(GREEN)
            words.words[start_idx + idx].next_to(
                prompt[-1], RIGHT, buff=0.25, aligned_edge=UP
            )
            self.play(
                FadeOut(output[:-1], shift=UP * 0.5),
                Transformr(output[-1], out_word),
                run_time=0.5,
            )
            out_word_target = out_word.copy().next_to(
                model_input[-1], RIGHT, buff=0.25, aligned_edge=UP
            )
            self.play(
                MoveAlongPath(
                    out_word,
                    BrokenLine(
                        out_word.get_center(),
                        (model_box.get_right()[0] + 0.5, out_word.get_center()[1], 0),
                        (
                            model_box.get_right()[0] + 0.5,
                            out_word_target.get_center()[1],
                            0,
                        ),
                        out_word_target.get_center(),
                    ),
                ),
                run_time=1.5,
            )
            self.play(
                out_word.animate.rotate(PI / 2)
                .next_to(model_input[-1], RIGHT, buff=0.25, aligned_edge=UP)
                .set_color(WHITE),
                run_time=0.5,
            )
            result.add(out_word)
        self.wait()
        self.embed()

        # rotate and flash each word
        result.generate_target()
        for w in result.target:
            w.rotate(-PI / 2)
        result.target.arrange(RIGHT, buff=0.1).move_to(result).align_to(result, UL)
        self.play(MoveToTarget(result))

        self.playwl(
            *[
                AnimationGroup(
                    FlashAround(w, buff=0.05, color=GREEN),
                    result[start_idx + i].animate.set_color(GREEN),
                    run_time=0.5,
                )
                for i, w in enumerate(result[len(prompt) :])
            ],
            lag_ratio=0.5,
        )

        # chat

        self.play(FadeOut(model), FadeOut(result[start_idx - 1]))
        user_chat = result[: start_idx - 1]
        bot_chat = result[start_idx:]

        self.play(
            user_chat.animate.to_edge(RIGHT, buff=2).shift(UP * 3),
            bot_chat.animate.to_edge(LEFT, buff=2).shift(UP * 1.5),
        )
        user_chat_box = SurroundingRectangle(
            user_chat,
            color=GREY_A,
            fill_color=GREY_C,
            fill_opacity=0.5,
            stroke_width=1,
            stroke_color=GREY_B,
            buff=0.2,
        ).set_z_index(-1)
        bot_chat_box = SurroundingRectangle(
            bot_chat,
            color=GREY_A,
            fill_color=GREEN_D,
            fill_opacity=0.5,
            stroke_width=1,
            stroke_color=GREEN_C,
            buff=0.2,
        ).set_z_index(-1)
        self.playw(FadeIn(user_chat_box), FadeIn(bot_chat_box))

        user_label = (
            Text("user", font="Noto Sans KR", font_size=18)
            .next_to(user_chat_box, DOWN, buff=0.1)
            .set_color(GREY_B)
        )
        bot_label = (
            Text("LLM", font="Noto Sans KR", font_size=18)
            .next_to(bot_chat_box, DOWN, buff=0.1)
            .set_color(GREEN_B)
        )
        self.playw(
            FadeIn(user_label, shift=DOWN * 0.1), FadeIn(bot_label, shift=DOWN * 0.1)
        )


class MDLModel_detail(InteractiveScene, Scene2D):
    def construct(self):
        # model
        model_box = Rectangle(
            width=9, height=2, stroke_color=GREY_A, fill_color=GREY_C, fill_opacity=0.7
        ).shift(UP)
        modelt = (
            Text(
                "Masked Diffusion Language Model",
                font="Noto Sans KR",
                font_size=20,
                color=BLACK,
            )
            .move_to(model_box.get_center())
            .set_z_index(1)
        )
        model = VGroup(model_box, modelt).set_z_index(2)
        self.playw(FadeIn(model))

        # words
        full_sentence = (
            "4월 초 샌프란시스코랑 LA 날씨를 검색해서 알려줘. </prompt> "
            + "4월 초의 샌프란시스코와 LA의 날씨는 ..."
        )
        words = Words(full_sentence, font="Noto Sans KR", font_size=18).shift(DOWN)
        start_idx = 8

        masked = (
            VGroup(
                *[
                    Text("<MASK>", font="Noto Sans KR", font_size=18).move_to(
                        words.words[i].get_center()
                    )
                    for i in range(start_idx, len(words.words))
                ]
            )
            .arrange(RIGHT, buff=0.15)
            .next_to(words.words[start_idx - 1], RIGHT, buff=0.15)
        )
        prompt = words.words[:start_idx]

        self.playw(FadeIn(prompt))
        self.playw(FadeIn(masked))

        # rotate and arrange
        total = VGroup(*prompt, *masked)
        total.generate_target()
        for w in total.target:
            w.rotate(PI / 2)
        total.target.arrange(RIGHT, buff=0.35, aligned_edge=UP).move_to(total).align_to(
            total, UL
        ).shift(RIGHT * 0.6)
        self.playw(MoveToTarget(total))

        # a single diffusion step
        output = (
            Tensor(len(total), shape="square", arrange=RIGHT, buff=0.36)
            .scale(0.7)
            .next_to(model_box, UP, buff=0.5)
            .align_to(total, LEFT)
        )
        self.playw(FadeTransform(total.copy(), output))

        self.play(FadeOut(output[: len(prompt)], shift=UP * 0.5))
        random_idx = [[1, 4], [0, 2], [3, 5]]
        out_idx = VGroup(*[output[start_idx + i] for i in random_idx[0]])
        out_word = VGroup(
            *[
                words.words[start_idx + i]
                .copy()
                .move_to(output[start_idx + i].get_center())
                for i in random_idx[0]
            ]
        ).set_color(GREEN)
        self.playw(Transform(out_idx, out_word))
        words_to_transform = VGroup(
            *[words.words[start_idx + i] for i in random_idx[0]]
        )
        words_to_transform[0].rotate(PI / 2).move_to(
            masked[random_idx[0][0]].get_center()
        ).align_to(masked[random_idx[0][0]], UP)
        words_to_transform[1].rotate(PI / 2).move_to(
            masked[random_idx[0][1]].get_center()
        ).align_to(masked[random_idx[0][1]], UP)

        self.playw(
            Transformr(masked[random_idx[0][0]], words_to_transform[0]),
            Transformr(masked[random_idx[0][1]], words_to_transform[1]),
            FadeOut(output[start_idx:], shift=UP * 0.5),
        )

        self.embed()
        # iteration

        for idx_pair in random_idx[1:]:
            model_input = VGroup(*prompt, *masked).copy()
            output = (
                Tensor(len(model_input), shape="square", arrange=RIGHT, buff=0.36)
                .scale(0.7)
                .next_to(model_box, UP, buff=0.5)
                .align_to(total, LEFT)
            )
            self.play(FadeTransform(model_input, output), run_time=0.7)

            self.play(FadeOut(output[: len(prompt)], shift=UP * 0.5), run_time=0.7)
            out_idx = VGroup(*[output[start_idx + i] for i in idx_pair])
            out_word = VGroup(
                *[
                    words.words[start_idx + i]
                    .copy()
                    .rotate(PI / 2)
                    .move_to(output[start_idx + i].get_center())
                    .align_to(output[start_idx + i], DOWN)
                    for i in idx_pair
                ]
            ).set_color(GREEN)
            self.play(Transform(out_idx, out_word), run_time=0.7)
            words_to_transform = VGroup(*[words.words[start_idx + i] for i in idx_pair])
            words_to_transform[0].rotate(PI / 2).move_to(
                masked[idx_pair[0]].get_center()
            ).align_to(masked[idx_pair[0]], UP)
            words_to_transform[1].rotate(PI / 2).move_to(
                masked[idx_pair[1]].get_center()
            ).align_to(masked[idx_pair[1]], UP)

            self.play(
                Transformr(masked[idx_pair[0]], words_to_transform[0]),
                Transformr(masked[idx_pair[1]], words_to_transform[1]),
                FadeOut(output[start_idx:], shift=UP * 0.5),
                run_time=0.7,
            )
        self.wait()
