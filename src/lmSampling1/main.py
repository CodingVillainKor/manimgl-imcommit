from manimlib import *
from raenimgl import *
from random import seed

import sys

sys.path.append("./")
from examples import *

seed(41)
np.random.seed(41)


def polar(deg):
    return np.array([np.cos(deg * DEGREES), np.sin(deg * DEGREES), 0])


class TokenNode(VGroup):
    # [0]: rounded box, [1]: token text
    def __init__(self, token: str, font_size=22, height=0.5):
        text = Text(token, font_size=font_size)
        box = RoundedRectangle(
            width=max(text.get_width() + 0.3, height),
            height=height,
            corner_radius=0.08,
        ).set_fill(BLACK, opacity=1)
        text.move_to(box)
        super().__init__(box, text)
        self.normal().set_z_index(2)

    def style(self, color, stroke_color=None, stroke_width=1.5):
        self[0].set_stroke(stroke_color or color, stroke_width)
        self[1].set_color(color)
        return self

    def normal(self):
        return self.style(WHITE, GREY_B)

    def mute(self):
        return self.style(GREY_D, GREY_D)

    def lit(self, color=YELLOW):
        return self.style(color, color, 3)


class generationExample(InteractiveScene, Scene2D):
    def begin_animations(self, animations):
        super().begin_animations(animations)
        # group animations pull on-screen nodes into a z=0 wrapper; lift them back above the lines
        self.add(
            *[m for m in self.get_mobject_family_members() if isinstance(m, TokenNode)]
        )

    def construct(self):
        rng = np.random.default_rng(7)
        GAP = 0.6

        def prob_width(p):
            return 1.5 + 8 * p

        def fan(src, tokens, angles, dist):
            nodes = VGroup(
                *[
                    TokenNode(t).move_to(src.get_center() + polar(a) * dist)
                    for t, a in zip(tokens, angles)
                ]
            )
            edges = VGroup(
                *[
                    DashedLine(src.get_center(), n.get_center(), dash_length=0.1)
                    .set_stroke(GREY_C, 2)
                    .set_z_index(0)
                    for n in nodes
                ]
            )
            return nodes, edges

        def half_extent(mob, direction):
            return abs(direction[0]) * mob.get_width() / 2 + abs(direction[1]) * mob.get_height() / 2

        def pct_labels(src, nodes, angles, probs, font_size=20, gap=0.15):
            # sits on the clockwise side of each edge, `gap` away from the line,
            # centred on the part of the edge visible between the two boxes
            labels = VGroup()
            for n, a, p in zip(nodes, angles, probs):
                label = Integer(round(p * 100), unit="%", font_size=font_size)
                label.set_color(GREY_B).set_z_index(2)
                d, perp = polar(a), polar(a - 90)
                start = src.get_center() + d * half_extent(src, d)
                end = n.get_center() - d * half_extent(n, d)
                mid = (start + end) / 2
                labels.add(label.move_to(mid + perp * (gap + half_extent(label, perp))))
            return labels

        SUB = 0.15  # bottom fraction of the frame kept empty for subtitles

        def frame_to(*mobs, margin=1.3, min_height=5.5):
            g = VGroup(*mobs)
            aspect = self.cf.get_width() / self.cf.get_height()
            h = max(g.get_height(), g.get_width() / aspect, min_height / margin)
            h *= margin / (1 - SUB)
            return (
                self.cf.animate.scale(h / self.cf.get_height())
                .move_to(g.get_center() + DOWN * SUB * h / 2)
            )

        def glance(nodes, color=YELLOW, lag_ratio=0.35):
            # Indicate on the text only: on the whole node it would also fill the box
            return LaggedStart(
                *[
                    AnimationGroup(
                        Indicate(n[1], scale_factor=1, color=color),
                        n[0].animate(rate_func=there_and_back).set_stroke(color, 3),
                    )
                    for n in nodes
                ],
                lag_ratio=lag_ratio,
            )

        def shoot(src, node, color=YELLOW, wait=0.5):
            # one sample: a dot leaves src and lands on node
            dot = Dot(radius=0.08).set_color(color).move_to(src).set_z_index(1)
            self.add(dot)
            self.play(dot.animate(rate_func=rush_into).move_to(node), run_time=0.6)
            self.remove(dot)
            self.playw(
                node.animate(rate_func=there_and_back).lit(color),
                run_time=0.6,
                wait=wait,
            )

        def flow(src, nodes, angles, counts, run_time=3):
            # many samples: each dot flies through its word and stacks in its own slot
            order = [i for i, c in enumerate(counts) for _ in range(c)]
            rng.shuffle(order)
            filled = [0] * len(nodes)
            dots, anims = VGroup(), []
            for i in order:
                slot = nodes[i].get_center() + polar(angles[i]) * (
                    0.55 + 0.09 * filled[i]
                )
                filled[i] += 1
                dot = Dot(radius=0.05).set_color(YELLOW).move_to(src).set_z_index(1)
                dots.add(dot)
                anims.append(dot.animate.move_to(slot))
            self.add(*dots)
            self.playwl(*anims, lag_ratio=0.12, run_time=run_time)
            return dots

        def ghost_tree(node, angle, depth=3, length=0.8, spread=32):
            levels = [VGroup() for _ in range(depth)]
            tips = VGroup()

            def grow(p, a, d, l):
                n = int(rng.choice([2, 3]))
                for da in np.linspace(-spread, spread, n) + rng.uniform(-8, 8, n):
                    q = p + polar(a + da) * l
                    levels[d].add(
                        Line(p, q).set_stroke(GREY_C, 1.5, opacity=0.8 - 0.2 * d)
                    )
                    if d + 1 < depth:
                        grow(q, a + da, d + 1, l * 0.75)
                    else:
                        tips.add(Dot(q, radius=0.03).set_color(GREY_C))

            grow(node.get_center() + polar(angle) * 0.4, angle, 0, length)
            return VGroup(*levels, tips)

        def grow_tree(tree, run_time=1.5):
            *levels, tips = tree
            return LaggedStart(
                *[AnimationGroup(*[Create(l) for l in lv]) for lv in levels],
                FadeIn(tips),
                lag_ratio=0.6,
                run_time=run_time,
            )

        def grow_step(prev, nxt, color=YELLOW):
            # fork: chosen link + two ghost stubs, then nxt fades in
            base = prev.get_right()
            link = Line(base, nxt.get_left()).set_stroke(color, 3).set_z_index(1)
            stubs = VGroup(
                *[
                    DashedLine(base, base + polar(a) * 0.5, dash_length=0.06)
                    for a in (38, -38)
                ]
            )
            stub_tips = VGroup(
                *[Circle(radius=0.04).move_to(s.get_end()) for s in stubs]
            )
            stub = VGroup(stubs, stub_tips).set_stroke(GREY_D, 1.5)
            self.play(Create(link), Create(stubs), FadeIn(stub_tips), run_time=0.3)
            self.play(FadeIn(nxt), run_time=0.4)
            return link, stub

        # question node
        root = TokenNode("piui가 뭐야?", font_size=26, height=0.65).style(
            WHITE, BLUE_A, 2
        )
        angles1 = [45, -45, -135, 135]
        probs1 = [0.70, 0.18, 0.08, 0.04]
        nodes1, edges1 = fan(root, ["pi", "지금부터", "웹", "..."], angles1, 2.3)
        pcts1 = pct_labels(root, nodes1, angles1, probs1)
        jg = nodes1[1]

        self.cf.scale(0.5)
        self.playw(FadeIn(root, scale=0.8), wait=0.5)

        # first output: four branches burst out
        self.add(*edges1, *nodes1)
        self.playw(
            self.cf.animate.scale(7.2 / self.cf.get_height()).move_to(DOWN * 0.55),
            LaggedStart(
                *[
                    AnimationGroup(Create(e), FadeIn(n, shift=polar(a) * 0.5))
                    for e, n, a in zip(edges1, nodes1, angles1)
                ],
                lag_ratio=0.2,
            ),
            run_time=1.5,
        )

        # three words are likely: eyes go to each, "..." recedes
        self.playw(
            glance(nodes1[:3]),
            nodes1[3].animate.mute(),
            edges1[3].animate.set_stroke(GREY_D),
        )

        # "pi" is the most likely: its branch gets thick
        self.playw(
            edges1[0].animate.set_stroke(GREY_B, prob_width(probs1[0])),
            nodes1[0].animate.scale(1.15),
        )

        # "지금부터", "웹" are plausible too
        self.playw(
            LaggedStart(
                *[
                    AnimationGroup(
                        edges1[i].animate.set_stroke(GREY_B, prob_width(probs1[i])),
                        RWiggle(nodes1[i], amp=0.08, speed=3, run_time=1),
                    )
                    for i in (1, 2)
                ],
                lag_ratio=0.4,
            ),
            edges1[3].animate.set_stroke(width=prob_width(probs1[3])),
        )

        # probabilistically: everything dims
        self.playw(
            *[n.animate.mute() for n in nodes1],
            *[e.animate.set_stroke(GREY_D) for e in edges1],
            wait=0.5,
        )

        # x% "pi", y% "지금부터", z% "웹": spotlight moves with a counting label
        for i in range(3):
            anims = [
                nodes1[i].animate.lit(),
                edges1[i].animate.set_stroke(YELLOW),
                FadeIn(pcts1[i].set_color(YELLOW)),
            ]
            if i > 0:
                anims += [
                    nodes1[i - 1].animate.mute(),
                    edges1[i - 1].animate.set_stroke(GREY_D),
                    pcts1[i - 1].animate.set_color(GREY_B),
                ]
            self.playw(*anims)

        # sample with those odds: 20 draws pile up next to their words
        self.play(
            *[n.animate.normal() for n in nodes1],
            *[e.animate.set_stroke(GREY_B) for e in edges1],
            pcts1[2].animate.set_color(GREY_B),
            FadeIn(pcts1[3]),
        )
        dots1 = flow(root, nodes1, angles1, [13, 4, 2, 1])

        # each time you ask, the first word can change
        self.play(FadeOut(dots1))
        shoot(root, nodes1[2])
        shoot(root, nodes1[0])

        # so everything after it differs
        trees1 = [ghost_tree(nodes1[i], angles1[i], length=0.7) for i in range(3)]
        self.playw(
            LaggedStart(*[grow_tree(t) for t in trees1], lag_ratio=0.25), wait=1.5
        )

        # this time: the second most likely, "지금부터"
        self.play(*[FadeOut(t) for t in trees1])
        self.play(Circumscribe(pcts1[1], color=YELLOW), run_time=0.75)
        shoot(root, jg, wait=0)

        # "지금부터" is sampled; the rest fall away and the camera follows
        chosen1 = Line(root.get_center(), jg.get_center()).set_stroke(YELLOW, 4)
        chosen1.set_z_index(1)
        angles2 = [90, 0, -90, 180]
        probs2 = [0.41, 0.27, 0.22, 0.10]
        nodes2, edges2 = fan(jg, ["pi", "찾아보", "검색을", "..."], angles2, 1.7)
        pcts2 = pct_labels(jg, nodes2, angles2, probs2, font_size=16, gap=0.08)
        self.playw(
            jg.animate.lit(),
            Create(chosen1),
            FadeOut(VGroup(*[nodes1[i] for i in (0, 2, 3)], edges1, pcts1)),
            frame_to(jg, nodes2, margin=1.5),
            run_time=1.5,
        )

        # what comes next? same fan, unknown words
        qs = VGroup(*[TokenNode("?").mute().move_to(n) for n in nodes2])
        self.add(*edges2, *qs)
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(Create(e), FadeIn(q, shift=polar(a) * 0.4))
                    for e, q, a in zip(edges2, qs, angles2)
                ],
                lag_ratio=0.2,
            )
        )
        self.playw(*[RWiggle(q, amp=0.05, speed=4, run_time=1) for q in qs])

        # its own next-word probabilities
        self.playw(
            LaggedStart(
                *[FadeTransform(q, n) for q, n in zip(qs, nodes2)], lag_ratio=0.15
            ),
            *[
                e.animate.set_stroke(GREY_B, prob_width(p))
                for e, p in zip(edges2, probs2)
            ],
            FadeIn(pcts2),
        )

        # sample from them
        dots2 = flow(jg, nodes2, angles2, [8, 6, 4, 2])

        # many possible outputs
        self.play(FadeOut(dots2))
        self.playw(glance(nodes2[:3]))

        # sampled sentences
        chain_specs = [["ui", "를", "알아볼", "게요"], ["겠습니다"], ["통해"]]
        chains = []
        for i, tokens in enumerate(chain_specs):
            row = VGroup(nodes2[i])
            for t in tokens:
                row.add(TokenNode(t).next_to(row[-1], RIGHT, buff=GAP))
            chains.append(row)
        tail = (
            VGroup(*[Dot(radius=0.04) for _ in range(3)])
            .arrange(RIGHT, buff=0.12)
            .next_to(chains[2], RIGHT, buff=0.3)
            .set_color(YELLOW)
        )

        def run_chain(i, *added_anims, color=YELLOW):
            row = chains[i]
            head = Line(jg.get_center(), row[0].get_center()).set_stroke(color, 4)
            head.set_z_index(1)
            self.play(
                Create(head),
                row[0].animate.lit(color),
                frame_to(jg, row, tail if i == 2 else row),
                *added_anims,
            )
            links, stubs = VGroup(head), VGroup()
            for prev, nxt in zip(row[:-1], row[1:]):
                nxt.lit(color)
                link, stub = grow_step(prev, nxt, color)
                links.add(link)
                stubs.add(stub)
            return links, stubs

        def settle(row, links):
            return [
                *[n.animate.normal() for n in row],
                links.animate.set_stroke(GREY_B),
            ]

        # "지금부터", "pi", "ui", "를", "알아볼", "게요"
        links1, _ = run_chain(0, FadeOut(pcts2))
        self.wait()

        # "지금부터", "찾아보", "겠습니다"
        links2, _ = run_chain(1, *settle(chains[0], links1))
        self.wait()

        # "지금부터", "검색을", "통해", ...
        links3, _ = run_chain(2, *settle(chains[1], links2))
        self.playwl(*[FadeIn(d, shift=RIGHT * 0.1) for d in tail], lag_ratio=0.4)

        # many possibilities
        others_tree = ghost_tree(nodes2[3], 190, length=0.7, spread=25)
        self.play(
            *settle(chains[2], links3),
            tail.animate.set_color(GREY_B),
            jg.animate.lit(WHITE),
            chosen1.animate.set_stroke(WHITE),
            frame_to(root, jg, *chains, tail, others_tree, margin=1.2),
            run_time=1.5,
        )
        self.playw(grow_tree(others_tree, run_time=2))

        # randomness at every word -> always a different output:
        # walk one sentence to its end, then the next, each in its own colour
        chain_colors = [YELLOW, RED_B, GREEN_B]
        for row, links, c in zip(chains, [links1, links2, links3], chain_colors):
            steps = [
                AnimationGroup(link.animate.set_stroke(c), n.animate.lit(c))
                for link, n in zip(links, row)
            ]
            if row is chains[2]:
                steps.append(tail.animate.set_color(c))
            self.playw(
                LaggedStart(*steps, lag_ratio=0.7),
                run_time=0.35 * len(steps) + 0.3,
                wait=0.5,
            )
        self.wait()

        # same question, different answers
        self.playw(
            root.animate.style(BLUE_A, BLUE_A, 3),
            FadeOut(others_tree),
            frame_to(root, jg, *chains, tail, margin=1.25),
            wait=2,
        )
