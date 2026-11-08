from manimlib import *
from raenimgl import *
from random import seed, randrange

seed(41)
np.random.seed(41)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        sbox = Rectangle(width=3, height=0.6)
        stext = Text("state", font_size=24)
        state = VGroup(sbox, stext).shift(LEFT * 0.5)
        self.addw(state, wait=0.5)

        ## q1~q3
        qbox1 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext1 = Text("q1", font_size=24)
        q1 = VGroup(qbox1, qtext1)

        qbox2 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext2 = Text("q2", font_size=24)
        q2 = VGroup(qbox2, qtext2)

        qbox3 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext3 = Text("q3", font_size=24)
        q3 = VGroup(qbox3, qtext3)

        qs = VGroup(q1, q2, q3).arrange(DOWN).next_to(state, buff=0.75)

        l1 = DashedLine(state.get_right(), q1.get_left())
        l2 = DashedLine(state.get_right(), q2.get_left())
        l3 = DashedLine(state.get_right(), q3.get_left())
        self.play(FadeIn(qs))
        self.playw(*[Create(l) for l in [l1, l2, l3]], run_time=0.75, wait=1.5)

        ## q1, q2, q3
        q2q3 = VGroup(q2, q3, l2, l3)
        q3q1 = VGroup(q3, q1, l3, l1)
        q1q2 = VGroup(q1, q2, l1, l2)

        self.play(q2q3.animate(rate_func=there_and_back, run_time=1.3).set_opacity(0))
        self.play(q3q1.animate(rate_func=there_and_back, run_time=1.3).set_opacity(0))
        self.playw(
            q1q2.animate(rate_func=there_and_back, run_time=1.3).set_opacity(0),
            wait=1.5,
        )

        ## q4

        qbox4 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext4 = Text("q4", font_size=24)
        q4 = VGroup(qbox4, qtext4).next_to(q3, DOWN)

        qs.add(q4)
        l4 = DashedLine(state.get_right(), q4.get_left())
        self.playw(FadeIn(q4), Create(l4), run_time=0.75, wait=1.5)

        ## q4 dollar
        dollar = Text("$", font_size=24).next_to(q4, RIGHT)
        self.play(FadeIn(dollar, shift=RIGHT * 0.5), run_time=0.75)
        self.playw(FadeOut(dollar, shift=RIGHT * 0.5), wait=8.5)

        ## state - question indicate
        ind = (
            lambda x: x.animate(rate_func=there_and_back, run_time=0.5)
            .set_opacity(0.5)
            .set_color(YELLOW)
        )
        woq1 = VGroup(q2, q3, q4, l2, l3, l4)
        woq2 = VGroup(q1, q3, q4, l1, l3, l4)
        woq3 = VGroup(q1, q2, q4, l1, l2, l4)
        woq4 = VGroup(q1, q2, q3, l1, l2, l3)
        self.play(
            LaggedStart(ind(state), ind(l1), ind(q1), lag_ratio=0.3),
            woq1.animate(rate_func=there_and_back).set_opacity(0),
        )
        self.play(
            LaggedStart(ind(state), ind(l2), ind(q2), lag_ratio=0.3),
            woq2.animate(rate_func=there_and_back).set_opacity(0),
        )
        self.play(
            LaggedStart(ind(state), ind(l3), ind(q3), lag_ratio=0.3),
            woq3.animate(rate_func=there_and_back).set_opacity(0),
        )
        self.playw(
            LaggedStart(ind(state), ind(l4), ind(q4), lag_ratio=0.3),
            woq4.animate(rate_func=there_and_back).set_opacity(0),
            wait=2.5,
        )

        ## state and q1234
        self.play(ind(state))
        self.play(ind(q1))
        self.play(ind(q2))
        self.play(ind(q3))
        self.playw(ind(q4), wait=1.5)


class pagedAttn(InteractiveScene, Scene2D):
    samples = 4

    def construct(self):

        ## GPU
        gpu_box = Rectangle(width=8, height=4).shift(UP)
        gpu_text = Text("GPU", font_size=24).align(gpu_box, UR, buff=0.1)
        gpu = VGroup(gpu_box, gpu_text)
        self.playw(FadeIn(gpu), wait=1.5)

        gpu_lines = (
            VGroup(*[Rectangle(width=8, height=0.5) for _ in range(8)])
            .arrange(DOWN, buff=0)
            .move_to(gpu_box)
        )
        gpu1d = Rectangle(width=64, height=0.5)

        cell_size = 0.5
        per_row = 16

        def place(tensor, start_idx, lines=gpu_lines):
            for i in range(len(tensor)):
                idx = start_idx + i
                row = idx // per_row
                col = idx % per_row
                tensor[i].move_to(
                    lines[row].get_left() + RIGHT * cell_size * (col + 0.5)
                )
            return tensor

        ## attn 1 inference
        paragraph_text = "Manim is a powerful animation engine for explanatory math videos.\n It allows precise control over animations and is highly customizable.\n It supports complex animations and interactive scenes. ..."
        paragraph = Words(paragraph_text, font_size=24).next_to(gpu, DOWN, buff=0.5)

        attn_start = 0
        attn_tensor = Tensor(
            len(paragraph.words), shape="square", arrange=RIGHT, buff=0
        ).scale(5 / 4)
        place(attn_tensor, attn_start)
        self.playw(FadeIn(paragraph), wait=1.5)
        self.playwl(
            *[
                FadeTransform(paragraph.words[i], attn_tensor[i])
                for i in range(len(paragraph.words))
            ],
            lag_ratio=0.2,
        )

        ## FadeIn gpu_lines
        self.playw(FadeIn(gpu_lines), wait=3.5)
        gpu_text.add_updater(lambda m: m.align(gpu_lines[0], UR, buff=0.1))
        self.add(attn_tensor)
        attn_tensor.add_updater(lambda m: place(m, attn_start))
        self.remove(gpu_box)

        self.cf.save_state()
        gpu_lines.save_state()
        self.playw(
            gpu_lines.animate.arrange(RIGHT, buff=0),
            self.cf.animate.reorient(-90, 50, 90, (-7.78, -0.00, -14.05), 29.51),
            wait=2.5,
        )
        gpu_text.clear_updaters()
        gpu_text.generate_target().next_to(gpu_lines.saved_state[0], RIGHT, buff=0.05)
        self.play(Restore(self.cf), Restore(gpu_lines), MoveToTarget(gpu_text))
        attn_tensor.clear_updaters()
        ## gpu box again
        self.add(gpu_box)
        self.playw(FadeOut(gpu_lines))

        ## ptext2~4
        ptext2 = Words("What is the meaning of life?", font_size=24).next_to(
            gpu_box, DOWN, buff=0.5
        )
        p2_start = attn_start + len(attn_tensor)
        p2 = Tensor(len(ptext2.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )
        place(p2, p2_start)

        ptext3 = Words(
            "Implement a very profitable android app. I want it to be successful.",
            font_size=24,
        ).next_to(gpu_box, DOWN, buff=0.5)
        p3_start = p2_start + len(p2)
        p3 = Tensor(len(ptext3.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )
        place(p3, p3_start)

        ptext4 = Words(
            "I want a very quick and light-weight OCR model. \nIts performance should be top-notch. \nIts latency must be lower than 10ms.",
            font_size=24,
        ).next_to(gpu_box, DOWN, buff=0.5)
        p4_start = p3_start + len(p3)
        p4 = Tensor(len(ptext4.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )
        place(p4, p4_start)

        ptext5 = Words(
            "Summarize this research paper in three bullet points. \nFocus on the main contribution and the experimental results. \nKeep each bullet short and avoid technical jargon.",
            font_size=24,
        ).next_to(gpu_box, DOWN, buff=0.5)
        p5_start = p4_start + len(p4)
        p5 = Tensor(len(ptext5.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )
        place(p5, p5_start)

        ptext6 = Words(
            "Write a short story about a robot who learns to paint. \nIt lives alone in an abandoned city. \nOne day it finds an old box of brushes and colors. \nMake the ending feel warm.",
            font_size=24,
        ).next_to(gpu_box, DOWN, buff=0.5)
        p6_start = p5_start + len(p5)
        p6 = Tensor(len(ptext6.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )
        place(p6, p6_start)

        self.playw(FadeIn(ptext2))
        self.playw(
            *[FadeTransform(ptext2.words[i], p2[i]) for i in range(len(ptext2.words))],
            FadeIn(ptext3),
        )
        self.playw(
            *[FadeTransform(ptext3.words[i], p3[i]) for i in range(len(ptext3.words))],
            FadeIn(ptext4),
        )
        self.playw(
            *[FadeTransform(ptext4.words[i], p4[i]) for i in range(len(ptext4.words))],
            FadeIn(ptext5),
        )
        self.playw(
            *[FadeTransform(ptext5.words[i], p5[i]) for i in range(len(ptext5.words))],
            FadeIn(ptext6),
        )
        self.playw(
            *[FadeTransform(ptext6.words[i], p6[i]) for i in range(len(ptext6.words))],
            wait=8,
        )

        ## Fadeout p2, p5
        p1 = attn_tensor
        self.playw(FadeOut(p2), FadeOut(p5), wait=5)

        ## p7: into p5's place
        ptext7 = Words(
            "Create a new AI model that beats the current state-of-the-art.",
            font_size=24,
        ).next_to(gpu_box, DOWN, buff=0.5)
        p7_start = p5_start
        p7 = Tensor(len(ptext7.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )
        place(p7, p7_start)
        self.playw(FadeIn(ptext7))
        self.playw(
            *[FadeTransform(ptext7.words[i], p7[i]) for i in range(len(ptext7.words))],
            wait=3,
        )

        ## FadeOut p4
        self.playw(FadeOut(p4), wait=3)

        ## problem: new string's memory is lower than gpu vacancy, but there is no available contiguous block, so we need to free up space by fading out other tensors.
        ptext8 = Words(
            "Translate this whole user manual into Korean. \nKeep every technical term in English inside brackets. \nMatch the original formatting exactly and do not skip any section, \neven the long appendix at the end.",
            font_size=24,
        ).next_to(gpu_box, DOWN, buff=0.3)
        p8 = Tensor(len(ptext8.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )
        self.playw(FadeIn(ptext8))
        self.playwl(
            *[
                Indicate(ptext8.words[i], scale_factor=1.05, color=RED)
                for i in range(len(p8))
            ],
            lag_ratio=0.1,
        )

        ## indicate red on pre-occupied tensors
        self.playw(
            *[
                Indicate(cell, scale_factor=1.05, color=PURE_RED)
                for cell in [*p1, *p3, *p7, *p6]
            ],
            wait=1.5,
        )

        self.playw(RWiggle(ptext8, amp=0.2, speed=8, run_time=3.5))

        gpu2_box = Rectangle(width=8, height=4).next_to(gpu_box, RIGHT, buff=1)
        gpu2_text = (
            Text("GPU", font_size=24)
            .next_to(gpu2_box, RIGHT, buff=0.1)
            .align(gpu2_box, UP, buff=0.1)
        )
        gpu2_lines = (
            VGroup(*[Rectangle(width=8, height=0.5) for _ in range(8)])
            .arrange(DOWN, buff=0)
            .move_to(gpu2_box)
        )
        price = Text("+$$$", font_size=36, color=GREEN).next_to(gpu2_box, UP, buff=0.3)
        self.playw(
            self.cf.animate.scale(1.4).move_to(VGroup(gpu_box, gpu2_box)),
            ptext8.animate.set_color(WHITE).next_to(gpu2_box, DOWN, buff=0.3),
            FadeIn(gpu2_box),
            FadeIn(gpu2_text),
            FadeIn(price),
        )

        place(p8, 0, gpu2_lines)
        self.playw(
            *[FadeTransform(ptext8.words[i], p8[i]) for i in range(len(ptext8.words))],
            wait=5.6,
        )

        ## illustrate GPU vacancy for availability
        total_cells = per_row * len(gpu_lines)
        used_idx = []
        for start, tensor in [
            (attn_start, p1),
            (p3_start, p3),
            (p7_start, p7),
            (p6_start, p6),
        ]:
            used_idx += list(range(start, start + len(tensor)))
        empty_idx = [i for i in range(total_cells) if i not in used_idx]

        vacancy = VGroup()
        for idx in empty_idx:
            sq = Square(
                side_length=cell_size,
                stroke_width=DEFAULT_STROKE_WIDTH * 0.4,
                color=RED,
            ).set_fill(RED, opacity=0.35)
            place(VGroup(sq), idx)
            vacancy.add(sq)

        idle_text = Text(
            f"{len(empty_idx)} / {total_cells} idle", font_size=28, color=YELLOW
        ).next_to(gpu_box, DOWN, buff=0.3)

        self.playw(*[t.animate.set_opacity(0.3) for t in [p1, p3, p7, p6, p8]])
        self.playwl(*[FadeIn(v) for v in vacancy], lag_ratio=0.07)
        self.playw(FadeIn(idle_text))

class realPagedAttn(InteractiveScene, Scene2D):
    def construct(self):


        ## gpu lines
        gpu_box = Rectangle(width=8, height=4).shift(UP)
        gpu_text = Text("GPU", font_size=24).next_to(gpu_box, RIGHT, buff=0.1).align(gpu_box, UP, buff=0.1).set_color(GREY_B)
        gpu_lines = VGroup(*[Rectangle(width=8, height=0.5) for _ in range(8)]).arrange(DOWN, buff=0).move_to(gpu_box)
        self.addw(gpu_text, gpu_box)

        cell_size = 0.5
        per_row = 16
        def place(tensor, start_idx, lines=gpu_lines):
            for i in range(len(tensor)):
                idx = start_idx + i
                row = idx // per_row
                col = idx % per_row
                tensor[i].move_to(
                    lines[row].get_left() + RIGHT * cell_size * (col + 0.5)
                )
            return tensor

        ## paged attention text
        pa_text = Words("(Paged Attention)", font_size=24).next_to(gpu_text, DOWN, buff=0.1, aligned_edge=LEFT)
        self.playwl(*[FadeIn(item) for item in pa_text.words], lag_ratio=0.3)

        ## p1
        p1_text = Words(
            "I want a very quick and light-weight OCR model. \nIts performance should be top-notch. \nIts latency must be lower than 10ms.",
            font_size=24,
        ).next_to(gpu_box, DOWN, buff=0.3)
        attn_start = 0
        p1 = Tensor(len(p1_text.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )
        place(p1, attn_start)
        self.playw(*[FadeIn(item) for item in p1_text.words], wait=0.5)
        self.playw(*[FadeTransform(item, t) for item, t in zip(p1_text.words, p1)])

        ## chunk
        chunk_size=4
        free_pages = list(range(per_row * len(gpu_lines) // chunk_size))

        def place_random_page(chunk, lines=gpu_lines):
            # pick an unused slot whose start index satisfies idx % chunk_size == 0
            idx = free_pages.pop(randrange(len(free_pages))) * chunk_size
            row = idx // per_row
            col = idx % per_row
            chunk.move_to(lines[row].get_left() + RIGHT * cell_size * (col + chunk_size / 2))
            return chunk

        srs = VGroup()
        chunks = VGroup()
        for i in range(0, len(p1), chunk_size):
            chunk = p1[i:i+chunk_size]
            # measure a full page so a short last chunk still gets a 4-cell rectangle
            full_page = place(p1[:chunk_size].copy(), i)
            chunk_sr = SurroundingRectangle(full_page, buff=0.01, stroke_width=4).set_color(random_color())
            srs.add(chunk_sr)
            chunks.add(VGroup(chunk, chunk_sr))
        self.playwl(*[FadeIn(sr) for sr in srs], lag_ratio=0.07)

        ## place chunks randomly on the GPU lines
        for chunk in chunks:
            place_random_page(chunk.generate_target())
        self.playwl(*[MoveToTarget(chunk) for chunk in chunks], lag_ratio=0.07)

        ## Fully make use of the gpu lines
        p2_text = Words(
            "Plan a three day trip to Kyoto for my parents. \nThey enjoy quiet temples, local food and slow walks. \nKeep the daily budget under two hundred dollars.",
            font_size=24,
        ).next_to(gpu_box, DOWN, buff=0.3)
        p2 = Tensor(len(p2_text.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )

        p3_text = Words(
            "Review this pull request for hidden concurrency bugs. \nCheck every shared variable and explain each race condition you find. \nThen suggest a minimal fix that keeps the public interface unchanged.",
            font_size=24,
        ).next_to(gpu_box, DOWN, buff=0.3)
        p3 = Tensor(len(p3_text.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )

        p4_text = Words(
            "Compare these two database engines for an online store. \nInclude read speed, write speed, storage cost and backup options. \nAssume one million orders every month and steady growth next year. \nPresent the result as a table, then recommend one engine in two sentences.",
            font_size=24,
        ).next_to(gpu_box, DOWN, buff=0.3)
        p4 = Tensor(len(p4_text.words), shape="square", arrange=RIGHT, buff=0).scale(
            4.9 / 4
        )

        def scatter_pages(tensor):
            # lay cells out on the grid first so each page keeps the same spacing as p1
            place(tensor, 0)
            borders = VGroup()
            for i in range(0, len(tensor), chunk_size):
                chunk = tensor[i : i + chunk_size]
                # measure a full page so a short last chunk still gets a 4-cell rectangle
                full_page = place(tensor[:chunk_size].copy(), i)
                border = SurroundingRectangle(
                    full_page, buff=0.01, stroke_width=4
                ).set_color(random_color())
                place_random_page(VGroup(chunk, border))
                borders.add(border)
            return borders

        p2_srs = scatter_pages(p2)
        p3_srs = scatter_pages(p3)
        p4_srs = scatter_pages(p4)

        self.play(FadeIn(p2_text))
        self.play(
            *[FadeTransform(item, t) for item, t in zip(p2_text.words, p2)],
            FadeIn(p2_srs),
            FadeIn(p3_text),
        )
        self.play(
            *[FadeTransform(item, t) for item, t in zip(p3_text.words, p3)],
            FadeIn(p3_srs),
            FadeIn(p4_text),
        )
        self.playw(
            *[FadeTransform(item, t) for item, t in zip(p4_text.words, p4)],
            FadeIn(p4_srs),
        )

        ## indicate each request
        self.play(Indicate(p1, scale_factor=1))
        self.play(Indicate(p2, scale_factor=1))
        self.play(Indicate(p3, scale_factor=1))
        self.playw(Indicate(p4, scale_factor=1), wait=1.5)

        ## gpu box
        self.playw(gpu_box.set_z_index(1).animate(rate_func=there_and_back, run_time=3).set_fill(color=BLUE,opacity=0.9), wait=2.5)


        ## indicate scale factor 0 with PURE_RED color belong physically linked lanes
        # physical memory order: lane by lane from the top, left to right within a lane
        cells = [*p1, *p2, *p3, *p4]
        physical_order = [
            cell
            for lane in gpu_lines
            for cell in sorted(
                [c for c in cells if abs(c.get_y() - lane.get_y()) < cell_size / 2],
                key=lambda c: c.get_x(),
            )
        ]
        self.playwl(
            *[Indicate(cell, scale_factor=1, color=PURE_RED) for cell in physical_order[:16]],
            lag_ratio=0.15,
        )

        ## enumerate the order of each p1~p4
        def physical_idx(cell):
            row = min(
                range(len(gpu_lines)),
                key=lambda r: abs(cell.get_y() - gpu_lines[r].get_y()),
            )
            col = round((cell.get_x() - gpu_lines[row].get_left()[0]) / cell_size - 0.5)
            return row * per_row + col

        def page_order_text(name, tensor):
            starts = [physical_idx(tensor[i]) for i in range(0, len(tensor), chunk_size)]
            return Words(f"{name}: " + " - ".join(f"[{s}]" for s in starts), font_size=20)

        order_texts = (
            VGroup(
                page_order_text("p1", p1),
                page_order_text("p2", p2),
                page_order_text("p3", p3),
                page_order_text("p4", p4),
            )
            .arrange_in_grid(2, 2, h_buff=0, v_buff=0.3, aligned_edge=LEFT)
            .next_to(gpu_box, DOWN, buff=0.3)
        )
        order_texts[0].shift(RIGHT*0.75)
        order_texts[1].shift(LEFT*0.3)
        order_texts[2].shift(RIGHT*0.75)
        order_texts[3].shift(LEFT*0.3)
        self.play(FadeIn(order_texts[0]))
        self.play(FadeIn(order_texts[1]))
        self.play(FadeIn(order_texts[2]))
        self.playw(FadeIn(order_texts[3]))

        ## inference by the order of page_order_texts
        self.play(order_texts[1:].animate.set_opacity(0.3))

        # words alternate as "p1:", "[n]", "-", "[n]", ..., so [1::2] keeps only the indices
        idxs1 = order_texts[0].words[1::2]
        chunks1 = chunks  # p1's pages, in the same order as the indices above

        def page_anims(idxs, pages):
            anims = []
            for i, (idx, page) in enumerate(zip(idxs, pages)):
                page_anim = [Indicate(page, scale_factor=1)]
                # the last page has no next page to link to
                if i + 1 < len(pages):
                    # the flash needs many curves to fade smoothly along a straight line
                    link = (
                        Line(page.get_center(), pages[i + 1].get_center())
                        .insert_n_curves(100)
                        .set_stroke(PURPLE, 4)
                    )
                    page_anim.append(VShowPassingFlash(link, time_width=1.0, taper_width=0))
                anims.append(AnimationGroup(FlashUnder(idx), AnimationGroup(*page_anim)))
            return anims

        def quick_inference(order_idx, tensor, borders):
            self.play(
                *[
                    t.animate.set_opacity(1 if j == order_idx else 0.3)
                    for j, t in enumerate(order_texts)
                ],
                run_time=0.3,
            )
            pages = [
                VGroup(tensor[i * chunk_size : (i + 1) * chunk_size], border)
                for i, border in enumerate(borders)
            ]
            for anim in page_anims(order_texts[order_idx].words[1::2], pages):
                self.play(anim, run_time=0.5)

        anims = page_anims(idxs1, chunks1)

        for i, anim in enumerate(anims):
            self.playw(anim, wait=1 if i == len(anims)-1 else 0)


        ## p2
        quick_inference(1, p2, p2_srs)

        ## p3
        quick_inference(2, p3, p3_srs)

        self.embed()
        ## p4
        quick_inference(3, p4, p4_srs)
        self.wait(1)


class jevPagedAttn(InteractiveScene, Scene2D):
    def construct(self):

        ## gpu packed with paged requests
        gpu_box = Rectangle(width=8, height=4).shift(UP)
        gpu_text = Text("GPU", font_size=24).next_to(gpu_box, RIGHT, buff=0.1).align(gpu_box, UP, buff=0.1).set_color(GREY_B)
        gpu_lines = VGroup(*[Rectangle(width=8, height=0.5) for _ in range(8)]).arrange(DOWN, buff=0).move_to(gpu_box)
        pa_text = Words("(Paged Attention)", font_size=24).next_to(gpu_text, DOWN, buff=0.1, aligned_edge=LEFT)

        cell_size = 0.5
        per_row = 16
        chunk_size = 4
        free_pages = list(range(per_row * len(gpu_lines) // chunk_size))

        def place(tensor, start_idx, lines=gpu_lines):
            for i in range(len(tensor)):
                idx = start_idx + i
                row = idx // per_row
                col = idx % per_row
                tensor[i].move_to(
                    lines[row].get_left() + RIGHT * cell_size * (col + 0.5)
                )
            return tensor

        def place_random_page(chunk, lines=gpu_lines):
            idx = free_pages.pop(randrange(len(free_pages))) * chunk_size
            row = idx // per_row
            col = idx % per_row
            chunk.move_to(lines[row].get_left() + RIGHT * cell_size * (col + chunk_size / 2))
            return chunk

        def scatter_pages(tensor):
            place(tensor, 0)
            pages = VGroup()
            for i in range(0, len(tensor), chunk_size):
                chunk = tensor[i : i + chunk_size]
                full_page = place(tensor[:chunk_size].copy(), i)
                border = SurroundingRectangle(
                    full_page, buff=0.01, stroke_width=4
                ).set_color(random_color())
                page = VGroup(chunk, border)
                place_random_page(page)
                pages.add(page)
            return pages

        old_pages = scatter_pages(Tensor(121, shape="square", arrange=RIGHT, buff=0).scale(4.9 / 4))
        self.addw(gpu_text, pa_text, gpu_box, old_pages, wait=3.5)

        self.playw(gpu_box.set_z_index(1).animate(rate_func=there_and_back, run_time=3).set_fill(color=BLUE,opacity=0.9), wait=16.91)

        ## state and questions from before
        sbox = Rectangle(width=3, height=0.6)
        stext = Text("state", font_size=24)
        state = VGroup(sbox, stext)

        qbox1 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext1 = Text("q1", font_size=24)
        q1 = VGroup(qbox1, qtext1)

        qbox2 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext2 = Text("q2", font_size=24)
        q2 = VGroup(qbox2, qtext2)

        qbox3 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext3 = Text("q3", font_size=24)
        q3 = VGroup(qbox3, qtext3)

        qs = VGroup(q1, q2, q3).arrange(DOWN).next_to(state, buff=0.75)
        VGroup(state, qs).next_to(gpu_box, RIGHT, buff=3)

        l1 = DashedLine(state.get_right(), q1.get_left())
        l2 = DashedLine(state.get_right(), q2.get_left())
        l3 = DashedLine(state.get_right(), q3.get_left())

        self.play(
            old_pages.animate.set_opacity(0.3),
            self.cf.animate.scale(1.4).move_to(VGroup(gpu_box, state, qs)).shift(DOWN * 1.2),
            FadeIn(state),
            FadeIn(qs),
        )
        self.playw(*[Create(l) for l in [l1, l2, l3]], run_time=0.75, wait=1.36)

        ## questions do not share information
        q2q3 = VGroup(q2, q3, l2, l3)
        q3q1 = VGroup(q3, q1, l3, l1)
        q1q2 = VGroup(q1, q2, l1, l2)

        self.play(q2q3.animate(rate_func=there_and_back, run_time=1.1).set_opacity(0))
        self.play(q3q1.animate(rate_func=there_and_back, run_time=1.1).set_opacity(0))
        self.playw(q1q2.animate(rate_func=there_and_back, run_time=1.1).set_opacity(0), wait=2.74)

        ## questions hanging on the state
        ind = (
            lambda x: x.animate(rate_func=there_and_back, run_time=0.5)
            .set_opacity(0.5)
            .set_color(YELLOW)
        )
        self.playw(FadeOut(old_pages), run_time=0.75, wait=1.2)
        self.play(LaggedStart(ind(state), ind(l1), ind(q1), lag_ratio=0.3))
        self.play(LaggedStart(ind(state), ind(l2), ind(q2), lag_ratio=0.3))
        self.playw(LaggedStart(ind(state), ind(l3), ind(q3), lag_ratio=0.3), wait=1.09)

        ## place pages and write the order
        free_pages[:] = range(per_row * len(gpu_lines) // chunk_size)

        def new_tensor(n):
            return Tensor(n, shape="square", arrange=RIGHT, buff=0).scale(4.9 / 4)

        state_pages = scatter_pages(new_tensor(16))
        q1_pages = scatter_pages(new_tensor(8))
        q2_pages = scatter_pages(new_tensor(8))
        q3_pages = scatter_pages(new_tensor(8))
        q4_pages = scatter_pages(new_tensor(8))

        def physical_idx(cell):
            row = min(
                range(len(gpu_lines)),
                key=lambda r: abs(cell.get_y() - gpu_lines[r].get_y()),
            )
            col = round((cell.get_x() - gpu_lines[row].get_left()[0]) / cell_size - 0.5)
            return row * per_row + col

        def page_order_text(name, pages):
            starts = [physical_idx(page[0][0]) for page in pages]
            return Words(f"{name}: " + " - ".join(f"[{s}]" for s in starts), font_size=24)

        order_texts = (
            VGroup(
                page_order_text("q1", [*state_pages, *q1_pages]),
                page_order_text("q2", [*state_pages, *q2_pages]),
                page_order_text("q3", [*state_pages, *q3_pages]),
                page_order_text("q4", [*state_pages, *q4_pages]),
            )
            .arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            .next_to(gpu_box, DOWN, buff=0.3)
        )

        self.play(
            FadeTransform(state.copy(), state_pages),
            FadeTransform(q1.copy(), q1_pages),
            FadeTransform(q2.copy(), q2_pages),
            FadeTransform(q3.copy(), q3_pages),
        )
        for order_text in order_texts[:3]:
            order_text.words[1:8:2].set_color(YELLOW)
        self.play(FadeIn(order_texts[0]), run_time=0.6)
        self.play(FadeIn(order_texts[1]), run_time=0.6)
        self.playw(FadeIn(order_texts[2]), run_time=0.6, wait=1.66)

        ## reuse the state and continue with each question
        def page_anims(idxs, pages):
            anims = []
            for i, (idx, page) in enumerate(zip(idxs, pages)):
                page_anim = [Indicate(page, scale_factor=1)]
                if i + 1 < len(pages):
                    link = (
                        Line(page.get_center(), pages[i + 1].get_center())
                        .insert_n_curves(100)
                        .set_stroke(PURPLE, 4)
                    )
                    page_anim.append(VShowPassingFlash(link, time_width=1.0, taper_width=0))
                anims.append(AnimationGroup(FlashUnder(idx), AnimationGroup(*page_anim)))
            return anims

        def quick_inference(order_idx, idxs, pages, run_time):
            self.play(
                *[
                    t.animate.set_opacity(1 if j == order_idx else 0.3)
                    for j, t in enumerate(order_texts[:3])
                ],
                run_time=0.15,
            )
            for anim in page_anims(idxs, pages):
                self.play(anim, run_time=run_time)

        # q2 and q3 start from the last state page: words[7] is its index
        quick_inference(0, order_texts[0].words[1::2], [*state_pages, *q1_pages], 0.35)
        quick_inference(1, order_texts[1].words[7::2], [state_pages[-1], *q2_pages], 0.3)
        quick_inference(2, order_texts[2].words[7::2], [state_pages[-1], *q3_pages], 0.3)

        ## state is reused, so no recomputation
        def state_box(lines):
            return SurroundingRectangle(
                VGroup(*[t.words[1:8] for t in lines]), buff=0.06, stroke_width=3
            ).set_color(YELLOW)

        state_idxs = [t.words[1:8:2] for t in order_texts[:3]]
        state_sr = state_box(order_texts[:3])
        self.playw(order_texts[:3].animate.set_opacity(1), run_time=0.3, wait=1.33)
        self.playw(
            ind(state),
            FadeIn(state_sr),
            *[Indicate(page, scale_factor=1) for page in state_pages],
            wait=0.05,
        )
        self.playw(*[s.animate.set_opacity(0.3) for s in state_idxs[1:]], run_time=0.75, wait=1.2)

        ## new question
        qbox4 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext4 = Text("q4", font_size=24)
        q4 = VGroup(qbox4, qtext4).next_to(q3, DOWN)
        qs.add(q4)
        l4 = DashedLine(state.get_right(), q4.get_left())
        self.playw(FadeIn(q4), run_time=0.75, wait=2.69)

        ## state stays as it is
        self.playw(ind(state), *[Indicate(page, scale_factor=1) for page in state_pages], wait=0.7)

        ## one more leg
        order_texts[3].words[1:8:2].set_color(YELLOW).set_opacity(0.3)
        self.play(Create(l4), FadeTransform(q4.copy(), q4_pages), run_time=0.75)
        self.playw(FadeIn(order_texts[3]), Transform(state_sr, state_box(order_texts)), run_time=0.75, wait=1.92)

        ## questions do not affect each other
        woq1 = VGroup(q2, q3, q4, l2, l3, l4)
        woq2 = VGroup(q1, q3, q4, l1, l3, l4)
        woq3 = VGroup(q1, q2, q4, l1, l2, l4)
        woq4 = VGroup(q1, q2, q3, l1, l2, l3)
        self.play(woq1.animate(rate_func=there_and_back, run_time=0.62).set_opacity(0))
        self.play(woq2.animate(rate_func=there_and_back, run_time=0.62).set_opacity(0))
        self.play(woq3.animate(rate_func=there_and_back, run_time=0.62).set_opacity(0))
        self.playw(woq4.animate(rate_func=there_and_back, run_time=0.62).set_opacity(0), wait=0.23)

        ## pay only for the questions
        dollars = VGroup(*[Text("$", font_size=24).next_to(q, RIGHT) for q in [q1, q2, q3, q4]])
        self.playwl(*[FadeIn(d, shift=RIGHT * 0.5) for d in dollars], lag_ratio=0.3, wait=3.42)

        self.embed()


class outro(InteractiveScene, Scene2D):
    def construct(self):

        ## gpu
        gpu_box = Rectangle(width=8, height=4).shift(UP)
        gpu_text = Text("GPU", font_size=24).next_to(gpu_box, RIGHT, buff=0.1).align(gpu_box, UP, buff=0.1).set_color(GREY_B)
        gpu_lines = VGroup(*[Rectangle(width=8, height=0.5) for _ in range(8)]).arrange(DOWN, buff=0).move_to(gpu_box)
        self.addw(gpu_text, gpu_box, wait=2.21)

        cell_size = 0.5
        per_row = 16
        chunk_size = 4
        free_pages = list(range(per_row * len(gpu_lines) // chunk_size))

        def place(tensor, start_idx, lines=gpu_lines):
            for i in range(len(tensor)):
                idx = start_idx + i
                row = idx // per_row
                col = idx % per_row
                tensor[i].move_to(
                    lines[row].get_left() + RIGHT * cell_size * (col + 0.5)
                )
            return tensor

        def place_random_page(chunk, lines=gpu_lines):
            idx = free_pages.pop(randrange(len(free_pages))) * chunk_size
            row = idx // per_row
            col = idx % per_row
            chunk.move_to(lines[row].get_left() + RIGHT * cell_size * (col + chunk_size / 2))
            return chunk

        ## state and questions in one straight line
        latent = Tensor(11, shape="square", arrange=RIGHT, buff=0).scale(4.9 / 4)
        place(latent, 0)
        line_srs = VGroup(
            SurroundingRectangle(latent[:5], buff=0.01, stroke_width=4).set_color(GREEN_B),
            SurroundingRectangle(latent[5:7], buff=0.01, stroke_width=4).set_color(PURPLE_B),
            SurroundingRectangle(latent[7:9], buff=0.01, stroke_width=4).set_color(PURPLE_B),
            SurroundingRectangle(latent[9:], buff=0.01, stroke_width=4).set_color(PURPLE_B),
        )
        self.playwl(*[FadeIn(cell) for cell in latent], lag_ratio=0.1, wait=0)
        self.playw(FadeIn(line_srs), run_time=0.75, wait=0.77)

        ## jev properties 1, 2, 3
        sbox = Rectangle(width=3, height=0.6)
        stext = Text("state", font_size=24)
        state = VGroup(sbox, stext)

        qbox1 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext1 = Text("q1", font_size=24)
        q1 = VGroup(qbox1, qtext1)

        qbox2 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext2 = Text("q2", font_size=24)
        q2 = VGroup(qbox2, qtext2)

        qbox3 = Rectangle(width=2.5, height=0.6).set_stroke(width=1, color=GREY_B)
        qtext3 = Text("q3", font_size=24)
        q3 = VGroup(qbox3, qtext3)

        qs = VGroup(q1, q2, q3).arrange(DOWN).next_to(state, buff=0.75)
        diagram = VGroup(state, qs).next_to(gpu_box, RIGHT, buff=1.5)

        l1 = DashedLine(state.get_right(), q1.get_left())
        l2 = DashedLine(state.get_right(), q2.get_left())
        l3 = DashedLine(state.get_right(), q3.get_left())
        dollars = VGroup(*[Text("$", font_size=24).next_to(q, RIGHT) for q in [q1, q2, q3]])

        self.cf.save_state()
        self.play(self.cf.animate.scale(1.4).move_to(VGroup(gpu_box, diagram)), FadeIn(diagram))
        self.playw(*[Create(l) for l in [l1, l2, l3]], run_time=0.75, wait=0.66)

        ## satisfy them at the same time
        ind = (
            lambda x: x.animate(rate_func=there_and_back, run_time=0.5)
            .set_opacity(0.5)
            .set_color(YELLOW)
        )
        q2q3 = VGroup(q2, q3, l2, l3)
        self.play(LaggedStart(ind(state), ind(l1), ind(l2), ind(l3), ind(q1), ind(q2), ind(q3), lag_ratio=0.15))
        self.play(q2q3.animate(rate_func=there_and_back, run_time=1).set_opacity(0))
        self.playwl(*[FadeIn(d, shift=RIGHT * 0.5) for d in dollars], lag_ratio=0.3, run_time=0.9, wait=0.51)

        ## masking
        mask_array = np.array(
            [
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
                [1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1],
            ]
        )
        mask = IntegerMatrix(mask_array).scale(0.5).move_to(diagram).shift(RIGHT * 0.7)
        for i in range(11 * 11):
            if mask_array[i // 11][i % 11] == 1:
                mask[i].set_color(GREEN_B if i % 11 < 5 else PURPLE_B)
        self.play(FadeOut(diagram), FadeOut(VGroup(l1, l2, l3)), FadeOut(dollars), FadeIn(mask))

        ## span row and col
        lr, lc = latent.copy(), latent.copy()
        lr.generate_target().scale(0.6).next_to(mask, LEFT)
        lc.generate_target().scale(0.6).next_to(mask, UP)
        lr_x, lc_y = lr.target.get_x(), lc.target.get_y()
        for i in range(11):
            lr.target[i].move_to([lr_x, mask[i * 11].get_y(), 0])
            lc.target[i].move_to([mask[i].get_x(), lc_y, 0])
        self.playw(MoveToTarget(lr), MoveToTarget(lc), wait=0.03)

        ## zeros
        zero_idxs = np.argwhere(mask_array == 0)
        idxs = [i * 11 + j for i, j in zero_idxs]
        mask_zeros = VGroup(*[mask[i] for i in idxs])
        self.playw(mask_zeros.animate.set_fill(RED, opacity=1), wait=0.31)

        ## only the question rows are added
        mask.generate_target()
        mask.target[: 5 * 11].set_opacity(0.1)
        self.playw(
            MoveToTarget(mask),
            lr[:5].animate.set_opacity(0.1),
            *[Indicate(cell, scale_factor=1) for cell in latent[5:]],
            wait=1.92,
        )

        ## questions share the state
        q_state = VGroup(*[mask[r * 11 + c] for r in range(5, 11) for c in range(5)])
        self.play(mask.animate.set_opacity(1), lr[:5].animate.set_opacity(1), run_time=0.4)
        self.playw(
            Indicate(q_state, scale_factor=1),
            *[Indicate(cell, scale_factor=1) for cell in latent[:5]],
            run_time=0.75,
            wait=0.63,
        )

        ## back to paged attention
        pa_text = Words("(Paged Attention)", font_size=24).next_to(gpu_text, DOWN, buff=0.1, aligned_edge=LEFT)
        srs = VGroup()
        chunks = VGroup()
        for i in range(0, len(latent), chunk_size):
            chunk = latent[i : i + chunk_size]
            full_page = place(latent[:chunk_size].copy(), i)
            chunk_sr = SurroundingRectangle(full_page, buff=0.01, stroke_width=4).set_color(random_color())
            srs.add(chunk_sr)
            chunks.add(VGroup(chunk, chunk_sr))

        self.play(
            FadeOut(mask),
            FadeOut(lr),
            FadeOut(lc),
            FadeOut(line_srs),
            Restore(self.cf),
            run_time=0.6,
        )
        self.playwl(*[FadeIn(sr) for sr in srs], *[FadeIn(w) for w in pa_text.words], lag_ratio=0.07, wait=0)

        for chunk in chunks:
            place_random_page(chunk.generate_target())
        self.playwl(*[MoveToTarget(chunk) for chunk in chunks], lag_ratio=0.07, wait=0)
        self.embed()
        ## other requests fill the gpu
        others = Tensor(110, shape="square", arrange=RIGHT, buff=0).scale(4.9 / 4)
        place(others, 0)
        other_pages = VGroup()
        for i in range(0, len(others), chunk_size):
            chunk = others[i : i + chunk_size]
            full_page = place(others[:chunk_size].copy(), i)
            border = SurroundingRectangle(full_page, buff=0.01, stroke_width=4).set_color(random_color())
            page = VGroup(chunk, border)
            place_random_page(page)
            other_pages.add(page)
        self.playwl(*[FadeIn(page) for page in other_pages], lag_ratio=0.03, wait=0.1)