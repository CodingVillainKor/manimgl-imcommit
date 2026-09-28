import json

from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


class apiio(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        logo = ImageMobject("jevlogo.png").shift(UP * 2.5).scale(0.3)
        self.playw(FadeIn(logo))

        ## llm
        llm_text = Text("LLM", font_size=28).next_to(
            logo, RIGHT, aligned_edge=DOWN, buff=0.1
        )
        self.playw(FadeIn(llm_text))

        ## api io

        reqt = Text("요청", font_size=28)
        rest = Text("응답", font_size=28)

        req_state_string = "Good morning, ..."
        req_questions = {
            "state": req_state_string,
            "questions": {"Q1": "...", "Q2": "..."},
            "model": "jev-latest",
        }
        req_json = json.dumps(req_questions, indent=4, ensure_ascii=False)
        req = rCode(req_json, language="json").scale(0.8).shift(LEFT * 2.5 + DOWN * 0.5)
        reqt.next_to(req, UP, aligned_edge=LEFT, buff=0.1)

        res_answers = {
            "answers": {"Q1": "...", "Q2": "..."},
            "model": "jev-1.13.0",
            "usage": "...",
        }
        res_json = json.dumps(res_answers, indent=4, ensure_ascii=False)
        res = (
            rCode(res_json, language="json")
            .scale(0.8)
            .align_to(req, UP)
            .shift(RIGHT * 3.5)
        )
        rest.next_to(res, UP, aligned_edge=RIGHT, buff=0.1)

        self.play(FadeIn(req), FadeIn(reqt))
        self.playw(FadeIn(res), FadeIn(rest))

        ## req state
        state_value = req.text_slice(1, '"Good morning, ..."')
        state_value_t = (
            Text("문제 지문", font_size=24 * 0.8)
            .move_to(state_value)
            .align_to(state_value, LEFT)
            .set_color(YELLOW_B)
        )
        self.play(state_value.animate.set_opacity(0), run_time=0.7)
        self.play(FadeIn(state_value_t, scale=0.7))

        ## req questions
        q1_value = req.text_slice(3, '"..."')
        q2_value = req.text_slice(4, '"..."')
        q1_value_t = (
            Text("질문 1", font_size=24 * 0.8)
            .move_to(q1_value)
            .align_to(q1_value, LEFT)
            .set_color(YELLOW_B)
        )
        q2_value_t = (
            Text("질문 2", font_size=24 * 0.8)
            .move_to(q2_value)
            .align_to(q2_value, LEFT)
            .set_color(YELLOW_B)
        )
        self.play(VGroup(q1_value, q2_value).animate.set_opacity(0), run_time=0.7)
        self.playw(FadeIn(q1_value_t, scale=0.7), FadeIn(q2_value_t, scale=0.7))

        ## res answers
        a1_value = res.text_slice(2, '"..."')
        a2_value = res.text_slice(3, '"..."')
        a1_value_t = (
            Text("답변 1", font_size=24 * 0.8)
            .move_to(a1_value)
            .align_to(a1_value, LEFT)
            .set_color(YELLOW_B)
        )
        a2_value_t = (
            Text("답변 2", font_size=24 * 0.8)
            .move_to(a2_value)
            .align_to(a2_value, LEFT)
            .set_color(YELLOW_B)
        )
        self.play(VGroup(a1_value, a2_value).animate.set_opacity(0), run_time=0.7)
        self.playw(FadeIn(a1_value_t, scale=0.7), FadeIn(a2_value_t, scale=0.7), wait=3)

        ## fadeout res

        self.playw(
            FadeOut(res),
            FadeOut(rest),
            FadeOut(a1_value_t),
            FadeOut(a2_value_t),
            VGroup(req.ls[0], req.ls[-2:]).animate.set_opacity(0.3),
        )

        ## circumscribe state and questions
        state_key = req.text_slice(1, "state")
        questions_key = req.text_slice(2, "questions")
        self.playw(Circumscribe(state_key), Circumscribe(questions_key), wait=3)

        ## fadeout state_value_t and fadein state_value
        self.playw(FadeOut(state_value_t), state_value.animate.set_opacity(1))
        self.playw(
            FadeOut(q1_value_t),
            FadeOut(q2_value_t),
            q1_value.animate.set_opacity(1),
            q2_value.animate.set_opacity(1),
        )

        ## q1
        q1_string = '{"type": "choice", \na"instructions": "...",\na"criteria": {"c1": "...", "c2": "...", ...}}'
        q1 = (
            VGroup(
                *[
                    Text(line, font=MONO_FONT, font_size=24 * 0.8)
                    for line in q1_string.split("\n")
                ]
            )
            .arrange(DOWN, aligned_edge=LEFT, buff=0.13)
            .align_to(q1_value, UL)
        )
        q1[1][0].set_opacity(0)
        q1[2][0].set_opacity(0)
        q1_comma = req.text_slice(3, ",")
        self.play(
            FadeOut(q1_value),
            q1_comma.animate.next_to(q1, RIGHT, buff=0.05, aligned_edge=DOWN),
            req.ls[4:].animate.shift(DOWN * 0.7),
            req.frame.animate.stretch_to_fit_height(req.frame.get_height() + 0.7)
            .align_to(req.frame, UP)
            .stretch_to_fit_width(req.frame.get_width() + 3.5)
            .align_to(req.frame, LEFT),
            run_time=0.7,
        )
        self.playw(FadeIn(q1))
        ## type, instructions, criteria
        type_key = q1[0][1:7]
        instructions_key = q1[1][1:14]
        criteria_key = q1[2][1:10]
        req.text_slice(3, '"..."').set_opacity(0)
        reqtg = req.generate_target()
        reqtg.set_opacity(0.3)
        reqtg.text_slice(3, '"..."').set_opacity(0)
        reqtg.text_slice(4, '"..."').set_opacity(0)
        self.playw(
            MoveToTarget(req),
            type_key.animate.set_color(RED),
            instructions_key.animate.set_color(RED),
            criteria_key.animate.set_color(RED),
        )

        ## type
        self.playw(Circumscribe(type_key, color=RED))
        ## instructions
        self.playw(Circumscribe(instructions_key, color=RED))
        ## criteria
        self.playw(Circumscribe(criteria_key, color=RED))


class types(InteractiveScene, Scene2D):
    def construct(self):
        ## types: choice, noul, score
        q1_dict = {
            "type": "choice",
            "instructions": "What is the proper answer?",
            "criteria": {"c1": "...", "c2": "..."},
        }
        q1_json = json.dumps(q1_dict, indent=4)
        q1 = rCode(q1_json, language="json").scale(0.8).shift(UP)
        q1_tag = (
            Text('"Q1":', font_size=20)
            .next_to(q1, UP, buff=0.1, aligned_edge=LEFT)
            .set_color(GREY_B)
        )
        self.addw(q1, q1_tag)

        ## 0.3 and type keeps 1
        q1.generate_target()
        q1.target.set_opacity(0.3)
        q1.target.ls[1].set_opacity(1)
        self.playw(MoveToTarget(q1))

        ## noul
        type_string = q1.text_slice(1, "choice")
        q2_type = (
            Text("noul", font_size=24 * 0.8, font=MONO_FONT)
            .set_color(YELLOW_B)
            .move_to(type_string)
            .align_to(type_string, LEFT)
        )
        type_string.save_state()
        self.play(Transform(type_string, q2_type))
        q3_type = (
            Text("score", font_size=24 * 0.8, font=MONO_FONT)
            .set_color(YELLOW_B)
            .move_to(type_string)
            .align_to(type_string, LEFT)
        )
        self.playw(Transform(type_string, q3_type))

        ## restore
        self.playw(Restore(type_string))

        ## flash under
        self.playw(FlashUnder(type_string), wait=2)

        ## opacity 1 criterias
        cs = VGroup(q1.ls[4], q1.ls[5])
        self.playw(cs.animate.set_opacity(1))

        ## get_cn and to 255
        def get_cn(n, comma=True):
            code = rCode(
                '{"' + f"c{n}" + '": "..."' + ",}" * comma, language="json"
            ).code[1:-1]
            return code.scale(0.8)

        cns = (
            VGroup(*[get_cn(n) for n in [3, 4, 5, 254, 255]])
            .arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            .next_to(cs, DOWN, buff=0.15, aligned_edge=LEFT)
        )
        cns[len(cns) // 2].become(
            Text("...", font_size=24 * 0.8, font=MONO_FONT)
            .move_to(cns[len(cns) // 2])
            .align_to(cns[len(cns) // 2], LEFT)
        )

        close_pars = q1.code[-2:]
        self.playwl(
            AnimationGroup(
                close_pars.animate.next_to(cns, DOWN, buff=0.15).align_to(
                    close_pars, LEFT
                ),
                q1.frame.animate.stretch_to_fit_height(
                    q1.frame.get_height() + 1.5
                ).align_to(q1.frame, UP),
            ),
            *[FadeIn(cn) for cn in cns],
            lag_ratio=0.1,
        )

        ## flashunder to q1.ls[1]
        self.playw(FlashUnder(q1.ls[1]))

        ## opacity 1: ql.ls[2]
        self.playw(q1.ls[2].animate.set_opacity(1))

        ## opacity 1: ql.ls[3] and circumscribe
        self.play(q1.ls[3].animate.set_opacity(1))
        self.playw(Circumscribe(q1.ls[3][:-2]))

        ## q1 left
        self.play(VGroup(q1, cns, q1_tag).animate.scale(0.8).shift(LEFT * 3))

        ## answers
        probs = [0.11, 0.08, 0.75, 0.04, 0.0, 0.01, 0.01]
        a1_dict = {
            "type": "choice",
            "probabilities": {
                "c1": 0.11,
                "c2": 0.08,
                "c3": 0.75,
                "c4": 0.04,
                "c5": 0.0,
                "c254": 0.01,
                "c255": 0.01,
            },
            "choice": "c3",
            "confidence": 0.75,
        }
        a1_json = json.dumps(a1_dict, indent=4)
        a1_json = a1_json.replace('"c5": 0.0,', "...")
        a1 = rCode(a1_json, language="json").scale(0.7).next_to(q1, RIGHT, buff=1.5)
        a1_tag = (
            Text('"Q1":', font_size=20)
            .next_to(a1, UP, buff=0.1, aligned_edge=LEFT)
            .set_color(GREY_B)
        )
        self.playw(FadeIn(a1), FadeIn(a1_tag))

        ## tags
        ol = self.overlay
        self.add(q1_tag.set_z_index(ol.z_index + 1), a1_tag.set_z_index(ol.z_index + 1))
        self.play(FadeIn(ol), Indicate(q1_tag), Indicate(a1_tag))

        ## line
        line = DashedLine(q1_tag.get_right(), a1_tag.get_left(), buff=0.1).set_z_index(
            ol.z_index + 1
        )
        self.play(FadeIn(line))

        ## fadeout line and ol
        self.playw(FadeOut(line), FadeOut(ol))

        ## opacity 1 for q1.ls[1] and a1.ls[1]
        q1t = q1.generate_target()
        a1t = a1.generate_target()
        q1t.code.set_opacity(0.3)
        a1t.code.set_opacity(0.3)
        q1t.ls[1].set_opacity(1)
        a1t.ls[1].set_opacity(1)
        self.playw(MoveToTarget(q1), MoveToTarget(a1), cns.animate.set_opacity(0.3))

        ## choice, probabilities, and confidence
        self.play(a1.ls[-3].animate.set_opacity(1))
        self.play(a1.ls[2].animate.set_opacity(1))
        self.playw(a1.ls[-2].animate.set_opacity(1))

        ## circumscribe probs
        self.playw(Circumscribe(a1.ls[2]))

        ## opacity 1 lagged
        self.playwl(
            *[a1.ls[i].animate.set_opacity(1) for i in range(3, 10)],
            lag_ratio=0.4,
        )

        ## bars
        def get_bar(p):
            width = 2
            r = (
                Rectangle(height=0.2, width=p * width)
                .set_fill(GREY_BROWN, opacity=1)
                .set_stroke(width=0)
            )
            return r

        bars = VGroup(
            *[
                get_bar(p).next_to(a1.ls[i + 3], RIGHT, buff=0.2)
                for i, p in enumerate(probs)
                if p > 0
            ]
        )
        for i, b in enumerate(bars):
            if i == len(bars) - 2:
                continue
            b.align_to(bars[-2], LEFT)
        self.playw(*[GrowFromEdge(b, edge=LEFT) for b in bars])


class choiceConfidence(InteractiveScene, Scene2D):
    def construct(self):

        ## a1
        probs = [0.02, 0.01, 0.95, 0.02]
        a1_dict = {
            "type": "choice",
            "probabilities": {
                "c1": 0.02,
                "c2": 0.01,
                "c3": 0.95,
                "c4": 0.02,
            },
            "choice": "c3",
            "confidence": 0.93,
        }
        a1_json = json.dumps(a1_dict, indent=4)
        a1 = rCode(a1_json, language="json").scale(0.8).shift(UP * 0.5)
        self.play(FadeIn(a1))

        ## bars
        def get_bar(p):
            width = 2
            r = (
                Rectangle(height=0.2, width=p * width)
                .set_fill(GREY_BROWN, opacity=1)
                .set_stroke(width=0)
            )
            return r

        bars = VGroup(
            *[
                get_bar(p).next_to(a1.ls[i + 3], RIGHT, buff=0.2)
                for i, p in enumerate(probs)
                if p > 0
            ]
        )
        for i, b in enumerate(bars):
            if i == len(bars) - 2:
                continue
            b.align_to(bars[-2], LEFT)
        self.playw(*[GrowFromEdge(b, edge=LEFT) for b in bars], run_time=0.7)

        ## c3 and choice
        a1t = a1.generate_target()
        a1t.set_opacity(0.3)
        a1t.ls[5].set_opacity(1)  # Highlight c3
        a1t.ls[-3].set_opacity(1)  # Highlight choice
        a1.save_state()
        self.playw(MoveToTarget(a1), bars[2].animate.set_color(GREEN))

        ## argmax
        argmax_tex = Tex(
            "\\text{choice} = \\text{argmax}_i(p_i)", font_size=32
        ).next_to(bars[2], RIGHT, buff=0.1)
        self.playw(FadeIn(argmax_tex, shift=RIGHT * 0.5), run_time=1.5)

        ## line
        choice_line = DashedLine(
            argmax_tex.get_corner(DL), a1.ls[-3][:-1].get_corner(UR)
        )
        self.playw(Create(choice_line), run_time=1.0)

        ## fadeout line and choice
        self.playw(Restore(a1), run_time=0.7)

        ## sr_c3
        sr_c3 = SurroundingRectangle(VGroup(a1.ls[5], bars[2]), color=GREEN, buff=0.07)
        self.playw(Create(sr_c3), run_time=0.7)

        ## shift left
        a1s = VGroup(a1, sr_c3, bars, argmax_tex, choice_line)
        self.play(a1s.animate.shift(LEFT * 4), run_time=0.7)

        ## a2
        probs2 = [0.21, 0.6, 0.14, 0.05]
        a2_dict = {
            "type": "choice",
            "probabilities": {
                "c1": 0.21,
                "c2": 0.6,
                "c3": 0.14,
                "c4": 0.05,
            },
            "choice": "c2",
            "confidence": 0.47,
        }
        a2_json = json.dumps(a2_dict, indent=4)
        a2 = rCode(a2_json, language="json").scale(0.8).shift(UP * 0.5 + RIGHT * 3)
        a2.ls[:3].set_opacity(0.3)
        a2.ls[7:].set_opacity(0.3)
        self.play(FadeIn(a2), FadeOut(argmax_tex), FadeOut(choice_line))

        bars2 = VGroup(
            *[
                get_bar(p).next_to(a2.ls[i + 3], RIGHT, buff=0.2)
                for i, p in enumerate(probs2)
                if p > 0
            ]
        )
        for i, b in enumerate(bars2):
            if i == len(bars2) - 2:
                continue
            b.align_to(bars2[-2], LEFT)
        self.playw(*[GrowFromEdge(b, edge=LEFT) for b in bars2], run_time=0.7)

        ## c2 and choice
        a2t = a2.generate_target()
        a2t.set_opacity(0.3)
        a2t.ls[4].set_opacity(1)  # Highlight c2
        a2.save_state()
        self.playw(MoveToTarget(a2), bars2[1].animate.set_color(GREEN))

        ## indicate a1's choice
        a1t = a1.generate_target()
        a1t.set_opacity(0.3)
        a1t.ls[5].set_opacity(1)  # Highlight c2
        a1.save_state()
        self.playw(MoveToTarget(a1), bars[2].animate.set_color(GREEN))

        ## rest of a1
        self.playw(a1.ls[3:7].animate.set_opacity(1))

        ## rest of a2
        self.playw(a2.ls[3:7].animate.set_opacity(1))

        ## confidence
        self.playw(
            a1.ls[3:7].animate.set_opacity(0.3),
            FadeOut(sr_c3),
            a2.ls[3:7].animate.set_opacity(0.3),
            a1.ls[-2].animate.set_opacity(1),
            a2.ls[-2].animate.set_opacity(1),
        )

        ## highlight confidence
        a1anim_in, _ = a1.highlight(-2)
        a2anim_in, _ = a2.highlight(-2)
        self.playw(a1anim_in, a2anim_in, run_time=0.7)


class confidenceEquation(InteractiveScene, Scene2D):
    def construct(self):
        ## display confidence equation
        # confidence: (p_max - 1/num_choices) / (1 - 1/num_choices)
        conf_eq = (
            Tex(
                r"\text{confidence} = ",
                r"\, \frac{p_{\max} - \frac{1}{\mathbf{N}}}{1 - \frac{1}{\mathbf{N}}}",
            )
            .move_to(ORIGIN)
            .set_color(GREY_A)
        )
        left = conf_eq[:11]
        numer = conf_eq[11:20]  # numerator
        denom = conf_eq[20:]  # denominator
        self.playw(FadeIn(left))
        self.playw(FadeIn(numer))
        self.playw(FadeIn(denom))

        self.playw(conf_eq.animate.shift(LEFT * 4))

        ## items
        strings = ["choice1", "choice2", "choice3"]
        probs = [0.0, 1.0, 0.0]
        items = (
            VGroup(*[Text(s, font_size=24, font=MONO_FONT) for s in strings])
            .set_color(BLUE_A)
            .arrange(DOWN, aligned_edge=LEFT, buff=0.5)
            .next_to(conf_eq, RIGHT, buff=1)
        )

        def get_bar(p):
            if p == 0.0:
                p = 0.01  # Avoid zero width
            bar = Rectangle(height=0.3, width=p * 2, color=BLUE)
            bar.set_fill(BLUE, opacity=1)
            return bar

        bars = VGroup(
            *[
                get_bar(p).next_to(items[i], RIGHT, buff=0.5)
                for i, p in enumerate(probs)
            ]
        )

        nums = VGroup(
            *[
                DecimalNumber(p, num_decimal_places=2, font_size=20).next_to(
                    bars[i], RIGHT, buff=0.2
                )
                for i, p in enumerate(probs)
            ]
        )

        self.playw(FadeIn(items), FadeIn(bars), FadeIn(nums))

        ## circumscribe the maximum probability bar
        self.playw(
            Circumscribe(VGroup(bars[1], items[1], nums[1]), color=YELLOW),
            VGroup(
                *[
                    VGroup(bars[i], items[i], nums[i])
                    for i in range(len(bars))
                    if i != 1
                ]
            )
            .animate(rate_func=there_and_back)
            .set_opacity(0.2),
        )

        ## pmax in numerator
        pmax = numer[:4]
        pmax.save_state()
        num1 = nums[1].copy()
        self.playw(
            pmax.animate.set_opacity(0), num1.animate(path_arc=PI / 2).move_to(pmax)
        )

        # become 1
        right = VGroup(num1, numer, denom)
        right.save_state()
        one = Text("1.0", font_size=28).move_to(right).align_to(right, LEFT)
        self.playw(Transform(right, one), wait=3)

        ## restore right, pmax
        self.play(Restore(right))
        self.playw(Restore(pmax), FadeOut(num1, shift=UP))

        ## bars: equal prob each
        anims = []
        for bar in bars:
            anims.append(
                bar.animate.stretch_to_fit_width(2 * 0.3333)
                .align_to(bar, LEFT)
                .set_color(RED)
            )
        n1, n2, n3 = nums
        n1.add_updater(
            lambda m: m.set_value(bars[0].get_width() / 2).next_to(
                bars[0], RIGHT, buff=0.2
            )
        )
        n2.add_updater(
            lambda m: m.set_value(bars[1].get_width() / 2).next_to(
                bars[1], RIGHT, buff=0.2
            )
        )
        n3.add_updater(
            lambda m: m.set_value(bars[2].get_width() / 2).next_to(
                bars[2], RIGHT, buff=0.2
            )
        )
        self.playw(*anims)

        ## 0.34, 0.32, 0.33
        anims = []
        new_probs = [0.34, 0.32, 0.33]
        for i, bar in enumerate(bars):
            anims.append(
                bar.animate.stretch_to_fit_width(2 * new_probs[i]).align_to(bar, LEFT)
            )
        self.play(*anims)
        n1.clear_updaters()
        n2.clear_updaters()
        n3.clear_updaters()
        self.playw(
            Circumscribe(VGroup(bars[1], items[1], nums[1]), color=YELLOW), run_time=0.7
        )

        ## Wiggle
        self.playw(
            RWiggle(VGroup(bars[0], items[0], nums[0]), amp=0.3, speed=3, run_time=1.5)
        )

        ## pmax be 1/N
        denomN = Tex("\\frac{1}{\\mathbf{N}}", font_size=28).move_to(pmax)
        self.playw(Transform(pmax, denomN))

        ## circumscribe numerator
        self.playw(Circumscribe(numer, color=RED))

        self.embed()
        ## zero
        zero = Text("0", font_size=28, font=MONO_FONT).move_to(numer)
        self.playw(Transform(numer[:-1], zero))

class example(InteractiveScene, Scene2D):
    def construct(self):
        self.embed()

        ## request
        req_dict = {
            "state": "HELP ME!!",
            "questions": {
                "sort": {
                    "type": "choice",
                    "instructions": "What kind of this state is?",
                    "criteria": {
                        "Informative": "giving useful information",
                        "Request": "asking for help or action",
                        "Other": "none of the above",
                    }
                }
            }
        }
        req_json = json.dumps(req_dict, indent=4)
        req = rCode(req_json, language="json")
        req.code.set_opacity(0.3)
        req.text_slice(1, '"HELP ME!!"').set_opacity(1)
        req.text_slice(5, '"What kind of this state is?"').set_opacity(1)
        req.text_slice(7, '"Informative"').set_opacity(1)
        req.text_slice(8, '"Request"').set_opacity(1)
        req.text_slice(9, '"Other"').set_opacity(1)
        self.playw(FadeIn(req))

class tilt(InteractiveScene, Scene2D):
    def construct(self):
        self.embed()

        ## tilt
        self.cf.reorient(0, 0, 0, (np.float32(-1.05), np.float32(-0.6), np.float32(0.0)), 8.00)
        logo = ImageMobject("jevlogo.png").rotate(-PI/4, axis=UP)
        self.addw(logo, wait=5)