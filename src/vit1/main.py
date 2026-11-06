from manimlib import *
from raenimgl import *
from random import seed

seed(41)
np.random.seed(41)


def link(p0, n0, p1, n1, k, n=8):
    f = bezier([p0, p0 + n0 * k, p1 + n1 * k, p1])
    ts = np.linspace(0, 1, n + 1)
    pts = [f(0)]
    for t0, t1 in zip(ts[:-1], ts[1:]):
        a, b = f(t0), f(t1)
        # handle chosen so the piece passes through the cubic's midpoint of [t0, t1]
        pts += [2 * f((t0 + t1) / 2) - (a + b) / 2, b]
    return VMobject().set_points(np.array(pts))


def along(path):
    p0, p1 = path.get_start(), path.get_end()

    def func(start_points, end_points, alpha):
        bend = path.pfp(1 - alpha) - interpolate(p1, p0, alpha)
        return interpolate(start_points, end_points, alpha) + bend

    return func


def dashed_rect(mob, dash_length=0.08, n_curves=200, **kwargs):
    rect = SurroundingRectangle(mob, **kwargs).insert_n_curves(n_curves)
    perimeter = 2 * (rect.get_width() + rect.get_height())
    return DashedVMobject(rect, num_dashes=max(1, int(perimeter / (2 * dash_length))))


class transformerIntro(InteractiveScene, Scene2D):
    def construct(self):

        ## transformer introduction
        tbox = Rectangle(width=7, height=3)
        ttext = Text("Transformer", font_size=24).align(tbox, UR, buff=0.1)
        transformer = VGroup(tbox, ttext).shift(UP * 0.5)
        self.playw(FadeIn(transformer), wait=0.5)
        self.playw(
            FlashUnder(ttext),
            ttext.animate(rate_func=there_and_back).set_color(YELLOW),
            wait=0.5,
        )

        ## input text
        text = Words("The quick brown fox jumps over the lazy dog", font_size=24)
        for w in text.words:
            w.rotate(PI / 2)
        text.words.arrange(RIGHT, aligned_edge=UP).next_to(transformer, DOWN, buff=0.3)
        self.play(FadeIn(text), run_time=0.5)
        latent = Tensor(len(text.words), shape="rectangle", arrange=RIGHT).move_to(tbox)
        for i, v in enumerate(latent):
            v.set_x(text.words[i].get_x())
        self.play(Transformr(text.words.copy(), latent), run_time=0.5)

        ## lines
        lines = VGroup()
        pairs = []
        for i in range(len(latent)):
            for j in range(len(latent)):
                # if i >= j:
                #     continue
                # a cubic with both handles UP * k peaks at 0.75k
                k = (random.random() * 0.5 + 0.3) / 0.75
                line = link(
                    latent[i].get_top(), UP, latent[j].get_top(), UP, k
                ).set_stroke(opacity=random.random() * 0.5 + 0.3)
                lines.add(line)
                pairs.append((i, j, k))
        self.playw(FadeIn(lines), run_time=0.5)

        ## camera
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(-90, 30, 90, (-0.50, 0.44, -0.27), 3.41),
            run_time=2.5,
        )

        self.playw(
            AnimationGroup(
                *[Indicate(line, scale_factor=1.03) for line in lines],
                lag_ratio=0.2,
                run_time=5,
            ),
            self.cf.animate.reorient(90, 35, -90, (1.43, 0.66, 0.27), 1.42),
            run_time=5,
            wait=2,
        )

        ## lc
        lc = latent.copy()
        # zero-size points on each top face, so they turn with lc
        anchors = [VectorizedPoint(v.get_top()) for v in lc]
        for v, a in zip(lc, anchors):
            v.add(a)
        self.add(lc)

        # updater with a single arg, otherwise manimgl passes dt as the second one
        def follow(i, j, k):
            def update(m):
                p1 = anchors[j].get_center()
                n1 = normalize(p1 - lc[j].get_center())
                m.set_points(link(latent[i].get_top(), UP, p1, n1, k).get_points())

            return update

        for line, (i, j, k) in zip(lines, pairs):
            line.add_updater(follow(i, j, k))

        # lc becomes a column standing left of latent, faces turned toward the lines
        lc.generate_target()
        lc.target.rotate(-PI / 2).move_to(
            latent.get_corner(UL) + UL * 0.2, aligned_edge=DR
        )

        ## self.cf.restore()
        # self.playw()
        tbox.generate_target().stretch_to_fit_height(6.5).stretch_to_fit_width(
            9
        ).align_to(tbox, DL)
        self.playw(
            MoveToTarget(lc, path_arc=-PI / 2),
            self.cf.animate.reorient(-90, 37, 90, (2.09, 1.03, 1.62), 10.17),
            MoveToTarget(tbox),
            ttext.animate.become(Text("self-attention", font_size=24)).align(
                tbox.target, UR, buff=0.1
            ),
            run_time=2.5,
            wait=2,
        )
        for line in lines:
            line.clear_updaters()

        ## mat
        mat = (
            randn(len(latent), len(latent))
            .set_x(latent.get_x())
            .set_y(lc.get_y())
            .scale(0.53)
            .stretch_to_fit_width(4.7)
        )
        # lines order transpose
        lines_transpose = VGroup()
        for i in range(len(latent)):
            for j in range(len(latent)):
                lines_transpose.add(lines[i + j * len(latent)])
        self.playwl(
            *[Transformr(lines_transpose[i], mat[i]) for i in range(len(lines))],
            lag_ratio=0.1,
            run_time=6,
            wait=1.5,
        )

        ## value
        value = (
            Tensor(len(latent), shape="rectangle", arrange=RIGHT)
            .rotate(PI / 2)
            .next_to(mat, RIGHT)
        )
        for i, l in enumerate(value):
            l.set_y(lc[i].get_y())
        self.play(
            FadeIn(value),
            self.cf.animate.reorient(90, 37, -90, (3.71, 1.65, 0.40), 8.22),
        )

        ## matmul
        o = (
            Tensor(len(latent), shape="rectangle", arrange=RIGHT)
            .rotate(PI / 2)
            .next_to(value, RIGHT)
        )
        for i, l in enumerate(o):
            l.set_y(lc[i].get_y())

        matmul_lines = VGroup()
        value_lines = VGroup()
        for i in range(len(latent)):
            mline = Line(
                mat[i * len(latent)].get_center(),
                mat[(i + 1) * len(latent) - 1].get_center(),
                stroke_width=5,
            )
            vline = Line(value[0].get_center(), value[-1].get_center(), stroke_width=5)
            matmul_lines.add(mline)
            value_lines.add(vline)
        anims = []
        for i, (mline, vline) in enumerate(zip(matmul_lines, value_lines)):
            anims.append(
                AnimationGroup(
                    ShowCreationThenDestruction(mline),
                    ShowCreationThenDestruction(vline, time_width=0.3),
                    FadeIn(o[i], shift=RIGHT),
                )
            )
        self.playwl(*anims, lag_ratio=0.8)

        ## output is o

        self.playw(
            o.animate(path_arc=PI / 2).rotate(PI / 2).next_to(mat, UP, buff=0.75),
            self.cf.animate.reorient(-179, 54, -179, (1.39, 1.03, -0.99), 11.03),
            run_time=2,
            wait=1.5,
        )


class bert(InteractiveScene, Scene2D):
    def construct(self):

        ## BERT training summary: masking and reconstruction

        bbox = Rectangle(width=7, height=3).set_fill(BLACK, opacity=0.75)
        btext = Text("BERT", font_size=24).align(bbox, UR, buff=0.1)

        bert = VGroup(bbox, btext).shift(UP * 0.75)
        self.play(FadeIn(bert.set_z_index(1)))
        self.playw(FlashUnder(btext), Indicate(btext, scale_factor=1.05))

        ## input text and output
        input_text = Words(
            "The quick brown fox jumps over the lazy dog", font=MONO_FONT, font_size=24
        )
        for t in input_text.words:
            t.rotate(PI / 2)
        input_text.words.arrange(RIGHT, aligned_edge=UP, buff=0.35).next_to(
            bert, DOWN, buff=0.3
        )
        input_text.save_state()
        masked_index = [2, 4, 7]
        for i in masked_index:
            input_text.words[i].set_opacity(0.3)
        output = (
            Tensor(len(input_text.words), shape="rectangle", arrange=RIGHT)
            .next_to(bert, UP)
            .set_color_by_gradient(*raenim_colors(len(input_text.words)))
        )
        for i, o in enumerate(output):
            if i not in masked_index:
                o.set_opacity(0.05)
            o.set_x(input_text.words[i].get_x())
        self.play(FadeIn(input_text), FadeIn(output), run_time=0.5)

        mask_srs = VGroup(
            *[dashed_rect(VGroup(input_text.words[i], output[i])) for i in masked_index]
        ).set_z_index(0)
        self.playw(FadeIn(mask_srs), wait=0.5)

        ## cls token
        cls_token = (
            Text("[CLS]", font=MONO_FONT, font_size=24)
            .rotate(PI / 2)
            .next_to(input_text.words[0], LEFT, buff=0.3, aligned_edge=UP)
            .set_color(PURPLE)
        )
        self.playw(FadeIn(cls_token))

        ## restore input text and output visibility
        ol = self.overlay
        self.add(cls_token.set_z_index(ol.z_index + 1))
        self.playw(
            input_text.animate.restore(),
            *[o.animate.set_opacity(1) for o in output],
            FadeOut(mask_srs),
            FadeOut(output),
            FadeIn(ol),
            RWiggle(cls_token, amp=0.15, speed=8, run_time=2.5),
            wait=0.5,
        )

        ## fadeout ol
        self.playw(FadeOut(ol), run_time=0.5, wait=0.5)

        input_tensor = Tensor(len(input_text.words), shape="rectangle", arrange=RIGHT)
        for i, t in enumerate(input_tensor):
            t.move_to(input_text.words[i]).align_to(input_text.words[i], UP)
        self.playwl(
            *[
                item.animate(rate_func=there_and_back).become(tensor)
                for item, tensor in zip(input_text.words, input_tensor)
            ],
            lag_ratio=0.5,
            wait=0.7,
        )

        ## indicate cls token
        self.playw(Indicate(cls_token, scale_factor=1.05))

        ## cls token opacity be 0.3
        self.playwl(
            cls_token.animate.set_opacity(0.3),
            *[Indicate(token) for token in input_text.words],
            lag_ratio=0.3,
        )

        ## cls token opacity be 1
        self.play(cls_token.animate.set_opacity(1))
        self.playw(Circumscribe(cls_token), wait=1.5)

        ## latent including cls token
        cls_token.set_z_index(0)
        latent = Tensor(
            len(input_text.words) + 1, shape="rectangle", arrange=RIGHT
        ).move_to(bbox)
        model_input = VGroup(cls_token, *input_text.words)
        for i, t in enumerate(latent):
            t.set_x(model_input[i].get_x())
        self.playw(Transformr(model_input.copy(), latent))

        ## camera
        self.cf.save_state()
        self.playw(
            self.cf.animate.reorient(-90, 30, 90, (-1.05, 0.62, -0.62), 4.24),
            model_input.animate.set_opacity(0.3),
            bbox.animate.set_opacity(0.2),
            btext.animate.set_opacity(0.2),
        )

        ## cls token text
        ct_text = Text("cls token latent", font_size=12).next_to(
            latent[0], DOWN, buff=0.1
        )
        self.playw(FadeIn(ct_text))

        ## lines latent
        lines = VGroup(
            *[
                BrokenLine(
                    latent[0].get_top(),
                    (latent[0].get_top() + latent[i].get_top()) / 2
                    + UP * (0.3 * random.random() + 0.3),
                    latent[i].get_top(),
                    smooth=True,
                ).set_stroke(opacity=(0.3 + 0.4 * random.random()))
                for i in range(1, len(latent))
            ]
        ).shuffle()
        self.playwl(*[FadeIn(line) for line in lines], lag_ratio=0.1)

        ## output latent
        self.play(self.cf.animate.restore())

        output_latent = (
            Tensor(1, shape="rectangle", arrange=RIGHT)
            .next_to(bbox, UP)
            .set_x(latent[0].get_x())
        )
        lline = DashedLine(latent[0].get_top(), output_latent.get_bottom())
        self.play(FadeTransform(latent[0].copy(), output_latent), Create(lline))
        self.play(self.cf.animate.shift(UP))

        ## downstream task model
        dbox = (
            Rectangle(width=2, height=1)
            .next_to(output_latent, UP, buff=0.2)
            .set_fill(opacity=0.8, color=BLACK)
        )
        dtext = (
            Text("downstream task", font_size=18)
            .next_to(dbox, RIGHT, buff=0.05)
            .align(dbox, UP, buff=0.05)
        )
        dtask = VGroup(dbox, dtext).set_z_index(1)
        self.playw(FadeIn(dtask))

        ## summary
        stext = (
            Text("summary", font_size=18)
            .next_to(dbox, UP, buff=0.2)
            .add_background_rectangle(color=PURPLE, buff=0.1)
        )
        self.playw(Transformr(output_latent.copy(), stext))

        ## absorb latent
        self.playwl(
            *[
                item.copy()
                .animate(path_func=along(line))
                .move_to(latent[0].get_center())
                .set_opacity(0)
                for item, line in zip(latent[1:], lines)
            ],
            lag_ratio=0.5,
        )


class vit1(InteractiveScene, Scene2D):
    def construct(self):

        ## intro: transformer, bert
        tt = Text("Transformer", font_size=48).set_color_by_gradient(*raenim_colors(2))
        bt = Text("BERT", font_size=48).set_color_by_gradient(*raenim_colors(2))
        texts = VGroup(tt, bt).arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        self.playw(FadeIn(texts), wait=0.5)

        ## underlining tt, and bt
        self.playw(FlashUnder(tt, color=BLUE, buff=0.15), wait=0.2)
        self.playw(FlashUnder(bt, color=BLUE, buff=0.15))

        ## vit
        vt = Text("ViT", font_size=48).set_color(PEACH)
        self.playw(
            FadeIn(vt, shift=RIGHT * 3.5), FadeOut(texts, shift=RIGHT * 3.5), wait=1.1
        )

        ## full vt
        fvt = (
            Words("Vision Transformer", font_size=48)
            .set_color(GREY_B)
            .next_to(vt, DOWN, buff=0.3, aligned_edge=LEFT)
        )
        fvt[:2].set_color(PEACH)
        fvt.words[1][0].set_color(PEACH)

        self.playwl(
            Transformr(vt[2].copy(), fvt.words[1][0]),
            FadeIn(fvt.words[1][1:]),
            Transformr(vt[:2].copy(), fvt[:2]),
            FadeIn(fvt.words[0][1:]),
            lag_ratio=0.3,
        )

        ## fvbox
        fvbox = Rectangle(width=7, height=2.5).shift(UP * 0.5)
        fvt.generate_target().scale(0.4).align(fvbox, UR, buff=0.1)
        self.playwl(
            FadeOut(vt), AnimationGroup(FadeIn(fvbox), MoveToTarget(fvt)), lag_ratio=0.4
        )

        ## sequence: tensor
        seq = Tensor(
            19, shape="rectangle", arrange=RIGHT, buff=0.2, ellipsis=True
        ).next_to(fvbox, DOWN)
        self.playw(FadeIn(seq), run_time=0.5, wait=0.5)

        ## camera down and image
        self.play(self.cf.animate.shift(DOWN * 1.5), FadeOut(seq), run_time=0.5)

        ## image composed of patches
        from PIL import Image

        # kept small, every pixel is its own Square
        size, p = 56, 8
        n = size // p
        arr = np.array(Image.open("ggilggil.png").convert("RGB"))
        h, w = arr.shape[:2]
        s = min(h, w)
        arr = arr[(h - s) // 2 : (h + s) // 2, (w - s) // 2 : (w + s) // 2]
        arr = np.array(Image.fromarray(arr).resize((size, size)))
        # (n, n, p, p, 3): patches[i, j] is the patch at row i, column j
        patches = arr.reshape(n, p, n, p, 3).swapaxes(1, 2)

        img = VGroup()
        for i in range(n):
            for j in range(n):
                patch = VGroup(
                    *[
                        Pixel(2 / size, fill_color=rgb_to_color(c / 255))
                        for c in patches[i, j].reshape(-1, 3)
                    ]
                ).arrange_in_grid(p, p, buff=0)
                img.add(patch)
        img.arrange_in_grid(n, n, buff=0).next_to(seq, DOWN, buff=0.5)

        self.play(FadeIn(img), run_time=0.5)

        ## camera zoom in to the image
        self.cf.save_state()

        self.playw(
            self.cf.animate.reorient(-46, 64, 0, (0.63, -2.29, -0.85), 3.47), wait=0.5
        )

        ## pixels into vectors
        # pixel (r, c) of arr, looked up through its patch
        def px(r, c):
            return img[(r // p) * n + c // p][(r % p) * p + c % p]

        vecs = VGroup()

        arr_float = arr.astype(np.float32) / 255.0
        i = 15
        for j in range(arr.shape[1]):
            vec_arr = arr_float[i, j][:, None]
            vec = (
                DecimalMatrix(vec_arr)
                .scale(0.1)
                .rotate(PI / 2, axis=RIGHT)
                .move_to(px(i, j))
                .set_color(rgb_to_color(arr_float[i, j]))
            )
            vecs.add(vec)
        rowo = VGroup(*[px(i, j) for j in range(arr.shape[1])])
        row = rowo.copy()
        self.play(Transformr(row, vecs), run_time=0.5)
        self.playwl(
            *[
                item.animate(
                    rate_func=there_and_back,
                    run_time=1.5 if k < 5 else 0.2 if k < 10 else 0.1,
                ).shift(OUT * 0.5)
                for k, item in enumerate(vecs)
            ],
            lag_ratio=0.4,
            wait=0.3,
        )

        ## restore the row and camera
        self.playw(Transformr(vecs, rowo), Restore(self.cf))

        ## re fade in seq
        seq_text = Words(
            "The quick brown fox jumps over the lazy dog ... The slow orange ducks runs through the green forest",
            font_size=20,
        )
        for i, w in enumerate(seq_text.words):
            if i != len(seq_text.words) // 2:
                w.rotate(PI / 2)
            w.move_to(seq[i]).align_to(seq[i], UP)
        self.playw(FadeIn(seq), FadeOut(img), wait=0.3)
        self.playwl(
            *[
                t.animate(rate_func=there_and_back).become(seq_text.words[i])
                for i, t in enumerate(seq)
                if i != len(seq_text.words) // 2
            ],
            lag_ratio=0.3,
        )

        ## in R 512
        dim_tex = Tex("\\in \\mathbb{R}^{512}", font_size=24)
        self.cf.save_state()
        self.playwl(
            seq[-1].animate.shift(DOWN),
            self.cf.animate.reorient(0, 0, 0, (3.36, -2.26, 0.00), 4.08),
        )
        dim_tex.next_to(seq[-1], RIGHT)
        self.playw(FadeIn(dim_tex), wait=0.3)

        dim_tex2 = (
            Tex("\\in \\mathbb{R}^{1024}", font_size=24)
            .move_to(dim_tex)
            .align_to(dim_tex, LEFT)
        )
        self.playw(
            Transformr(dim_tex[:2], dim_tex2[:2]),
            Transformr(dim_tex[2:], dim_tex2[2:]),
            wait=4,
        )

        ## restore self.cf
        self.playw(Restore(self.cf), FadeOut(seq), FadeOut(dim_tex2), wait=0.3)

        idxss = []
        for s in range(arr.shape[0] + arr.shape[1] - 1):
            idxs = [
                [i, j]
                for i in range(arr.shape[0])
                for j in range(arr.shape[1])
                if i + j == s
            ]
            idxss.append(idxs)
        diags = VGroup(*[VGroup(*[px(i, j) for i, j in idxs]) for idxs in idxss])
        self.playwl(*[FadeIn(diag) for diag in diags], run_time=2)

        ## arrange
        img.save_state()
        self.playw(img.animate.scale(0.5).arrange(RIGHT, buff=0.1).next_to(fvbox, DOWN))

        ## 256 * 3 = 768
        self.cf.save_state()
        self.play(self.cf.animate.reorient(0, 0, 0, (-1.86, -1.56, 0.00), 1.37))
        self.playw(img[16].animate.shift(DOWN * 0.5), run_time=0.75, wait=0.5)

        ## 16 16
        w16 = Text("16", font_size=12).next_to(img[16], UP, buff=0.05)
        h16 = Text("16", font_size=12).next_to(img[16], LEFT, buff=0.05)
        self.playw(FadeIn(w16), FadeIn(h16), wait=0.3)

        ## p16 = img[16]
        p16 = img[16]
        self.playwl(
            *[
                p16[i].animate(rate_func=there_and_back).set_color(YELLOW)
                for i in range(len(p16))
            ],
            run_time=2.5,
        )

        ## r 768
        r768 = Tex("\\in \\mathbb{R}^{768}", font_size=18).next_to(p16, RIGHT, buff=0.1)
        self.playw(FadeIn(r768), wait=1.5)

        ## indicate 768
        self.playw(Indicate(r768[-3:]), wait=1.5)

        ## restore self.cf
        self.play(Restore(self.cf))
        self.playw(
            p16.animate.shift(UP * 0.5),
            FadeOut(r768),
            FadeOut(w16),
            FadeOut(h16),
            wait=0.75,
        )

        ## FadeIn seq and fadeout img
        seq[-1].shift(UP)
        self.play(FadeIn(seq), FadeOut(img, shift=DOWN))
        self.playwl(
            *[
                t.animate(rate_func=there_and_back, run_time=0.75).become(
                    seq_text.words[i]
                )
                for i, t in enumerate(seq)
                if i != len(seq_text.words) // 2
            ],
            lag_ratio=0.4,
        )

        ## self.cf shift up
        self.playw(FadeOut(seq, shift=DOWN), FadeIn(img))

        ## img restore
        self.playw(Restore(img), wait=0.5)
        self.playw(
            img.animate.scale(0.5).arrange(RIGHT, buff=0.1).next_to(fvbox, DOWN),
            self.cf.animate.shift(UP),
            wait=1.5,
        )

        ## image token
        img_token = Tensor(len(img), shape="rectangle", arrange=RIGHT).next_to(
            fvbox, DOWN
        )
        fvbox.generate_target().stretch_to_fit_width(11.5)
        self.playw(
            AnimationGroup(
                *[img[i].animate.become(img_token[i]) for i in range(len(img))],
                lag_ratio=0.15,
            ),
            MoveToTarget(fvbox),
            fvt.animate.align(fvbox.target, UR, buff=0.1),
        )

        ## cls token
        cls_token = Tensor(1, shape="rectangle", arrange=RIGHT).next_to(
            img_token, LEFT, buff=0.2
        )
        self.play(FadeIn(cls_token))

        ## model input: clstoken + img_token
        model_input = VGroup(cls_token, *img)
        self.playw(model_input.animate.shift(UP * 1.5))

        ## camera
        self.cf.save_state()
        self.playw(self.cf.animate.reorient(-90, 38, 90, (-1.94, 0.11, -1.55), 6.38))

        ## sr_cls
        sr_cls = DashedVMobject(SurroundingRectangle(cls_token, buff=0.05))
        self.playw(Create(sr_cls), run_time=1.5)

        ## attention lines
        attn_lines = VGroup(
            *[
                BrokenLine(
                    img[i].get_top(),
                    (img[i].get_top() + cls_token.get_top()) / 2
                    + UP * (0.8 * random.random() + 0.1),
                    cls_token.get_top(),
                    smooth=True
                ).set_stroke(width=(w:=0.5*random.random() + 0.3), opacity=w)
                for i in range(len(img))
            ]
        )
        attn_lines.shuffle()
        self.playwl(*[Create(line) for line in attn_lines], lag_ratio=0.23)

        self.embed()
        ## output token
        output_token = Tensor(1, shape="rectangle", arrange=RIGHT).next_to(
            fvbox, UP, buff=0.2
        ).set_x(cls_token.get_x())
        self.playw(Transformr(cls_token.copy(), output_token), self.cf.animate.reorient(-90, 38, 90, (-1.63, 0.46, -1.30), 7.83))
