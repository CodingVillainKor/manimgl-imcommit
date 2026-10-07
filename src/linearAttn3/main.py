from manimlib import *
from raenimgl import *
from random import seed

seed(42)
np.random.seed(42)


class intro(InteractiveScene, Scene2D):
    def construct(self):

        ## intro
        nump1 = RaenimPlane(
            x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], width=12, height=12
        ).scale(0.5)
        nump1.x_axis.set_opacity(0.7)
        nump1.y_axis.set_opacity(0.7)
        nump2 = RaenimPlane(
            x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], width=12, height=12
        ).scale(0.5)
        nump2.x_axis.set_opacity(0.7)
        nump2.y_axis.set_opacity(0.7)

        numps = VGroup(nump1, nump2).arrange(RIGHT, buff=2.5).shift(UP * 0.5)
        text1 = Text("Linear Attention", font_size=28).next_to(nump1, UP)
        text2 = Text("DeltaNet", font_size=28).next_to(nump2, UP)
        piui = Text("321").set_opacity(0)
        self.add(numps, text1, text2, piui)

        ## np.randn into arrow
        np.random.seed(44)

        def get_arrow(plane):
            noise = np.random.randn(2)
            arrow = Arrow(
                start=plane.c2p(0, 0),
                end=plane.c2p(noise[0], noise[1]),
                buff=0,
                thickness=1.5,
            ).set_color(GREEN)
            return arrow

        def move_arrow(arrow, source: Arrow):
            # move the arrow to start at the end of the source arrow
            arrow.put_start_and_end_on(
                source.get_end(),
                source.get_end() + (arrow.get_end() - arrow.get_start()),
            )
            return arrow

        arrow1 = get_arrow(nump1)
        arrow2 = get_arrow(nump2)
        self.addw(arrow1, arrow2)

        ## nump1: just move_arrow(arrow, last_arrow)
        # nump2: interpolate between last_arrow and new random arrow
        def new_arrow_anim_nump1(last_arrow):  # nump1
            new_arr = move_arrow(get_arrow(nump1), last_arrow)
            anim = GrowArrow(new_arr)
            return new_arr, anim

        def new_arrow_anim_nump2(last_arrow):  # nump2
            new_arr = get_arrow(nump2)
            line = DashedLine(new_arr.get_end(), last_arrow.get_end())
            beta = np.random.rand()
            interp_point = beta * new_arr.get_end() + (1 - beta) * last_arrow.get_end()
            interp_dot = Dot(interp_point, radius=0.05)
            artifact = VGroup(line, interp_dot, new_arr)
            anim1 = FadeIn(artifact)
            real_line = Arrow(
                start=nump2.c2p(0, 0),
                end=interp_dot.get_center(),
                buff=0,
                thickness=1.5,
            ).set_color(GREEN)
            artifact_arrow = real_line.copy()
            anim2 = AnimationGroup(
                FadeOut(artifact),
                Transformr(new_arr, artifact_arrow),
                Transformr(last_arrow, real_line),
            )
            return real_line, anim1, anim2, artifact_arrow

        arrow1s = [arrow1]
        for i in range(10):
            run_time = 1 if i == 0 else 0.7
            arrow1, anim1 = new_arrow_anim_nump1(arrow1)
            arrow1s.append(arrow1)
            arrow2, anim21, anim22, artifact_arrow = new_arrow_anim_nump2(arrow2)
            if i == 4:
                self.playwl(
                    anim1,
                    anim21,
                    self.cf.animate.reorient(
                        0,
                        0,
                        0,
                        (np.float32(-4.24), np.float32(-1.24), np.float32(0.0)),
                        10.77,
                    ),
                    lag_ratio=0.1,
                    wait=0,
                )
            elif i == 1:
                self.playwl(
                    anim1,
                    anim21,
                    self.cf.animate.reorient(
                        0,
                        0,
                        0,
                        (np.float32(-2.77), np.float32(-0.69), np.float32(0.0)),
                        8.83,
                    ),
                    lag_ratio=0.1,
                    wait=0,
                )
            else:
                self.play(anim1, anim21, run_time=run_time)
            self.play(anim22, run_time=run_time)
            self.remove(artifact_arrow)

        self.wait()
        ## arrow1s to red
        self.playw(
            AnimationGroup(*[arr.animate.set_color(PURE_RED) for arr in arrow1s])
        )


class LinearAttnInLLM(InteractiveScene, Scene2D):
    def construct(self):

        ## layer helper function
        def get_layer():
            box = (
                Rectangle(width=2.8, height=3.3)
                .shift(LEFT * 0.2)
                .set_color(GREY_C)
                .set_stroke(width=1)
            )
            attn = Rectangle(width=2.0, height=1.3).set_color(ORANGE)
            ffn = Rectangle(width=2.0, height=0.8).set_color(GREEN)
            VGroup(attn, ffn).arrange(UP, buff=0.4)
            attn_text = (
                Text("Attention", font_size=20)
                .align(attn, UR, buff=0.1)
                .set_color(ORANGE)
            )
            ffn_text = (
                Text("FFN", font_size=20).align(ffn, UR, buff=0.1).set_color(GREEN)
            )

            line1 = Line(attn.get_bottom() + DOWN * 0.75, attn.get_bottom())
            line2 = Line(attn.get_top(), ffn.get_bottom())
            line3 = Line(ffn.get_top(), ffn.get_top() + UP * 0.75)
            xy4_1 = attn.get_bottom() + DOWN * 0.15
            xy4_2 = xy4_1 + LEFT * 1.3
            xy4_3 = xy4_2 + UP * 1.6
            xy4_4 = xy4_3 + RIGHT * 1.3
            line4 = BrokenLine(xy4_1, xy4_2, xy4_3, xy4_4).set_color(GREY)
            xy5_1 = ffn.get_bottom() + DOWN * 0.15
            xy5_2 = xy5_1 + LEFT * 1.3
            xy5_3 = xy5_2 + UP * 1.1
            xy5_4 = xy5_3 + RIGHT * 1.3
            line5 = BrokenLine(xy5_1, xy5_2, xy5_3, xy5_4).set_color(GREY)

            layer = VGroup(
                box, attn, ffn, attn_text, ffn_text, line1, line2, line3, line4, line5
            )
            return layer

        layers = (
            VGroup(*[get_layer() for _ in range(15)])
            .arrange(UP, buff=0)
            .align_to(ORIGIN, DOWN)
            .shift(DOWN * 2)
        )
        self.playw(FadeIn(layers[0]))

        ## full
        rest = layers[1:]
        self.playw(
            FadeIn(rest),
            self.cf.animate.reorient(
                0, 58, 0, (np.float32(0.15), np.float32(0.5), np.float32(0.99)), 9.24
            ),
        )

        ## pop-out the attention in the first layer
        attn1 = VGroup(layers[0][1], layers[0][3])
        attn1c = attn1.copy()
        attn1c.save_state()
        self.add(attn1c, attn1[0].set_stroke(opacity=0.3), attn1[1].set_opacity(0.3))
        self.playw(
            attn1c.animate.rotate(58 * DEGREES, axis=RIGHT).shift(OUT * 2 + RIGHT * 3)
        )

        ## linear attn
        lattn_text = (
            Text("Linear Attn", font_size=20)
            .move_to(attn1c[1])
            .align_to(attn1c[1], RIGHT)
            .rotate(58 * DEGREES, axis=RIGHT)
            .set_color(PURPLE)
        )
        self.playw(
            Transform(attn1c[1], lattn_text), attn1c[0].animate.set_stroke(color=PURPLE)
        )

        ## all attention in layers to be linearized
        layers.save_state()
        anims = []
        ol = self.overlay
        self.add(attn1c.set_z_index(ol.z_index + 1))
        for layer in layers[1:]:
            attn = VGroup(layer[1], layer[3])
            self.add(attn.set_z_index(ol.z_index + 1))
            text = (
                Text("Linear Attn", font_size=20)
                .move_to(attn[1])
                .align_to(attn[1], RIGHT)
                .set_color(PURPLE)
            )
            anims.append(Transform(attn[1], text))
            anims.append(attn[0].animate.set_stroke(color=PURPLE))
        self.playw(*anims, FadeIn(ol))

        ## restore
        self.play(FadeOut(ol), run_time=0.5)
        self.playw(Restore(layers), Restore(attn1c))

        self.remove(attn1c), attn1[0].set_stroke(opacity=1), attn1[1].set_opacity(1)
        ## RWiggle
        self.playw(RWiggle(layers, amp=0.5, speed=0.5), run_time=2, wait=2)

        ## slowly shift down
        # linear:full = 3:1
        layert = layers.generate_target()
        for i, l in enumerate(layert):
            if i % 4 != 3:
                attn = VGroup(l[1], l[3])
                text = (
                    Text("Linear Attn", font_size=20)
                    .move_to(attn[1])
                    .align_to(attn[1], RIGHT)
                    .set_color(PURPLE)
                )
                attn[1].become(text)
                attn[0].set_stroke(color=PURPLE)

        self.play(MoveToTarget(layers))
        self.playw(layers.animate.shift(DOWN * 38), run_time=8, rate_func=linear)


class LinearAttnRecap(InteractiveScene, Scene2D):
    def construct(self):
        ## q, k, v
        n = 9
        qk_dummy = VGroup(*[Tensor(n, buff=0.15) for _ in range(n)]).arrange(
            RIGHT, buff=0.15
        )
        q = Tensor(n, buff=0.15).next_to(qk_dummy, LEFT)
        qt = Text("Q", font_size=20).next_to(q[-1], LEFT, buff=0.15)
        k = Tensor(n, arrange=RIGHT, buff=0.15).next_to(qk_dummy, UP)
        kt = Text("K", font_size=20).next_to(k[0], UP, buff=0.15)
        v = Tensor(n, buff=0.15).next_to(qk_dummy, RIGHT)
        vt = Text("V", font_size=20).next_to(v[0], RIGHT, buff=0.15)
        self.addw(q, k, v, qt, kt, vt)

        ## q, k to \phi
        q_ = Tensor(n, buff=0.15, shape="circle").move_to(q).set_stroke(color=GREY)
        k_ = (
            Tensor(n, buff=0.15, shape="circle", arrange=RIGHT)
            .move_to(k)
            .set_stroke(color=GREY)
        )
        qt_ = Tex("\\phi(Q)", font_size=26).next_to(q[-1], LEFT, buff=0.15)
        kt_ = Tex("\\phi(K)", font_size=26).next_to(k[0], UP, buff=0.15)
        self.playw(
            Transform(q, q_), Transform(k, k_), Transform(qt, qt_), Transform(kt, kt_)
        )

        ## kv lines
        kv_lines = VGroup()
        for i in range(n):
            for j in range(n):
                kv_lines.add(
                    DashedLine(
                        k[j].get_bottom(), v[i].get_left(), stroke_width=1, color=GREY
                    )
                )
        self.playw(FadeIn(kv_lines))

        ## k -> [5, n], v -> [n, 5]
        km = randn(5, n).scale(0.3).move_to(qk_dummy).shift(RIGHT * 0.5)
        columns = VGroup(*[km[i:-2:n] for i in range(n)])
        vm = randn(n, 5).scale(0.3).next_to(km, buff=0.1)
        rows = VGroup(*[vm[i * 5 : i * 5 + 5] for i in range(n)])
        self.play(FadeOut(kv_lines), run_time=0.5)
        self.playwl(
            *[
                AnimationGroup(Transformr(k[i], columns[i]), Transformr(v[i], rows[i]))
                for i in range(n)
            ],
            FadeIn(VGroup(km[-2:], vm[-2:])),
            AnimationGroup(kt.animate.next_to(km, UP), vt.animate.next_to(vm, UP)),
            lag_ratio=0.2,
        )

        ## D dim
        brace = Brace(rows[-1], DOWN, buff=0.1).set_color(GREEN)
        d_dim = brace.get_text("D", font_size=24).set_color(GREEN)
        self.play(FadeIn(brace), FadeIn(d_dim))
        self.playw(Circumscribe(d_dim, color=PURE_GREEN))

        ## inner product
        km_array = km.val
        vm_array = vm.val
        inner_product = km_array @ vm_array
        kvm = DecimalMatrix(inner_product).scale(0.3).next_to(VGroup(km, vm), DOWN)
        self.play(FadeOut(VGroup(brace, d_dim)), run_time=0.5)

        ## prepare inner product
        rows_k = VGroup(*[km[i * n : i * n + n] for i in range(5)])
        cols_v = VGroup(*[vm[i:-2:5] for i in range(5)])
        anims = []
        for i in range(5):
            for j in range(5):
                r_line = DashedLine(
                    rows_k[i][0].get_left(),
                    rows_k[i][-1].get_right(),
                    stroke_width=1,
                    color=BLUE,
                )
                c_line = DashedLine(
                    cols_v[j][0].get_top(),
                    cols_v[j][-1].get_bottom(),
                    stroke_width=1,
                    color=RED,
                )
                anim1 = AnimationGroup(FadeIn(r_line), FadeIn(c_line))
                anim2 = AnimationGroup(
                    FadeOut(r_line),
                    FadeOut(c_line),
                    Transformr(
                        VGroup(rows_k[i].copy(), cols_v[j].copy()), kvm[i * 5 + j]
                    ),
                )
                anim = Succession(anim1, anim2)
                anims.append(anim)
        ## animate
        self.playwl(
            self.cf.animate.shift(DOWN), *anims, FadeIn(kvm[-2:]), lag_ratio=0.2
        )
        ## FadeOut km and vm
        self.play(FadeOut(VGroup(km, vm)))
        kvm.generate_target()
        kvm.target.move_to(km)
        self.playw(
            MoveToTarget(kvm),
            vt.animate.next_to(kt, RIGHT, buff=0.1).shift(UP * 0.02),
            self.cf.animate.shift(UP),
        )

        ## q to kvm
        anims = []
        qkv = (
            VGroup(*[randn(1, 5).scale(0.3) for _ in range(n)])
            .arrange(DOWN)
            .next_to(kvm, RIGHT, buff=0.5)
        )
        for i in range(n):
            anim = []
            qi = q[i].copy()
            anim.append(qi.animate.next_to(kvm, LEFT, buff=0.1))
            qkvi = qkv[i]
            anim.append(Transformr(VGroup(qi, kvm.copy()), qkvi))
            anims.append(anim)

        skew_anims = SkewedAnimations(*anims)
        for i, anim in enumerate(skew_anims):
            run_time = 0.5 if i >= 2 else 1
            self.play(*anim, run_time=run_time)
        self.wait()


class linearState(InteractiveScene, Scene2D):
    def construct(self):

        ## q, k, v
        n = 9
        qk_dummy = VGroup(*[Tensor(n, buff=0.15) for _ in range(n)]).arrange(
            RIGHT, buff=0.15
        )
        q = Tensor(n, buff=0.15).next_to(qk_dummy, LEFT)
        qt = Text("Q", font_size=20).next_to(q[-1], LEFT, buff=0.15)
        k = Tensor(n, arrange=RIGHT, buff=0.15).next_to(qk_dummy, UP)
        kt = Text("K", font_size=20).next_to(k[0], UP, buff=0.15)
        v = Tensor(n, buff=0.15).next_to(qk_dummy, RIGHT)
        vt = Text("V", font_size=20).next_to(v[0], RIGHT, buff=0.15)

        ## q, k to \phi
        q_ = Tensor(n, buff=0.15, shape="circle").move_to(q).set_stroke(color=GREY)
        k_ = (
            Tensor(n, buff=0.15, shape="circle", arrange=RIGHT)
            .move_to(k)
            .set_stroke(color=GREY)
        )
        qt_ = Tex("\\phi(Q)", font_size=26).next_to(q[-1], LEFT, buff=0.15)
        kt_ = Tex("\\phi(K)", font_size=26).next_to(k[0], UP, buff=0.15)
        q.become(q_), k.become(k_), qt.become(qt_), kt.become(kt_)
        kv_state = Tensor(1).scale(1.5).move_to(qk_dummy)
        kvt = Tex("\\phi(K) V", font_size=26).next_to(kv_state, DOWN, buff=0.15)
        kkv_lines = VGroup(*[DashedLine(k[i], kv_state) for i in range(n)]).set_color(
            GREY
        )
        vkv_lines = VGroup(*[DashedLine(v[i], kv_state) for i in range(n)]).set_color(
            GREY
        )
        self.addw(q, k, v, qt, kt, vt, kv_state, kvt, kkv_lines, vkv_lines)

        ## Indicate kvt red
        self.playw(Indicate(kvt, color=PURE_RED))

        ## Indicate each lines
        self.playwl(
            *[Indicate(line, color=PURE_RED, scale_factor=1.0) for line in kkv_lines],
            *[Indicate(line, color=PURE_RED, scale_factor=1.0) for line in vkv_lines],
            lag_ratio=0.05,
        )

        ## tilt all things
        all_things = VGroup(q, k, v, qt, kt, vt, kv_state, kvt, kkv_lines, vkv_lines)
        self.playw(
            all_things.animate.scale(0.7).rotate(PI / 3, axis=UP).shift(LEFT * 5)
        )

        ## nump and... start
        nump = (
            RaenimPlane(x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], width=8, height=8)
            .scale(0.4)
            .shift(DR + UP * 0.5)
        )
        nump.x_axis.set_opacity(0.7)
        nump.y_axis.set_opacity(0.7)
        self.play(FadeIn(nump))

        ## each key is a column and each value is a row
        i = 0
        ki, vi = k[i], v[i]
        fo = AnimationGroup(FadeOut(kkv_lines[i]), FadeOut(vkv_lines[i]))
        kmi = randn(5, 1).scale(0.2)
        vmi = randn(1, 5).scale(0.2).next_to(kmi, RIGHT, buff=0.05)
        kvm = VGroup(kmi, vmi).shift(LEFT * 2.5 + UP * 1.5)
        tf = AnimationGroup(Transform(ki, kmi), Transform(vi, vmi))

        def get_arrow(plane):
            noise = np.random.randn(2)
            arrow = Arrow(
                start=plane.c2p(0, 0),
                end=plane.c2p(noise[0], noise[1]),
                buff=0,
                thickness=1.5,
            ).set_color(GREEN)
            return arrow

        arr1 = get_arrow(nump)
        self.playw(fo, tf, FadeIn(arr1))

        ## continue with more arrows
        i += 1
        ki, vi = k[i], v[i]
        fo = AnimationGroup(FadeOut(kkv_lines[i]), FadeOut(vkv_lines[i]))
        kmi = randn(5, 1).scale(0.2)
        vmi = randn(1, 5).scale(0.2).next_to(kmi, RIGHT, buff=0.05)
        plus = Text("+", font_size=18).next_to(kvm, RIGHT, buff=0.05)
        kvm = VGroup(kmi, vmi).next_to(kvm, RIGHT)
        tf = AnimationGroup(Transform(ki, kmi), Transform(vi, vmi))

        def move_arrow(arrow, source: Arrow):
            # move the arrow to start at the end of the source arrow
            arrow.put_start_and_end_on(
                source.get_end(),
                source.get_end() + (arrow.get_end() - arrow.get_start()),
            )
            return arrow

        arr2 = get_arrow(nump)
        arr2 = move_arrow(arr2, arr1)
        self.play(fo, tf, FadeIn(arr2), FadeIn(plus))

        ## continue 2
        i += 1
        ki, vi = k[i], v[i]
        fo = AnimationGroup(FadeOut(kkv_lines[i]), FadeOut(vkv_lines[i]))
        kmi = randn(5, 1).scale(0.2)
        vmi = randn(1, 5).scale(0.2).next_to(kmi, RIGHT, buff=0.05)
        plus = Text("+", font_size=18).next_to(kvm, RIGHT, buff=0.05)
        kvm = VGroup(kmi, vmi).next_to(kvm, RIGHT)
        tf = AnimationGroup(Transform(ki, kmi), Transform(vi, vmi))
        arr3 = get_arrow(nump)
        arr3 = move_arrow(arr3, arr2)
        self.play(fo, tf, FadeIn(arr3), FadeIn(plus))

        ## continue 3
        i += 1
        ki, vi = k[i], v[i]
        fo = AnimationGroup(FadeOut(kkv_lines[i]), FadeOut(vkv_lines[i]))
        kmi = randn(5, 1).scale(0.2)
        vmi = randn(1, 5).scale(0.2).next_to(kmi, RIGHT, buff=0.05)
        plus = Text("+", font_size=18).next_to(kvm, RIGHT, buff=0.05)
        kvm = VGroup(kmi, vmi).next_to(kvm, RIGHT)
        tf = AnimationGroup(Transform(ki, kmi), Transform(vi, vmi))
        arr4 = get_arrow(nump)
        arr4 = move_arrow(arr4, arr3)
        self.playw(
            fo,
            tf,
            FadeIn(arr4),
            FadeIn(plus),
            self.cf.animate.scale(1.05).align_to(self.cf, LEFT),
        )

        ## indicate arrows
        self.playwl(
            Indicate(arr1, color=PURE_RED, scale_factor=1.0),
            Indicate(arr2, color=PURE_RED, scale_factor=1.0),
            Indicate(arr3, color=PURE_RED, scale_factor=1.0),
            Indicate(arr4, color=PURE_RED, scale_factor=1.0),
            lag_ratio=0.5,
        )


class gatedDeltaNet(InteractiveScene, Scene2D):
    def construct(self):
        ## prepare tex
        gdn_tex = Tex(
            "\\mathbf{S}_t = \\alpha_t \\mathbf{S}_{t-1} (\\mathbf{I} - \\beta_t \\mathbf{k}_t \\mathbf{k}_t^\\top) + \\beta_t \\mathbf{v}_t \\mathbf{k}_t^\\top",
            font_size=32,
        )
        dn_tex = Tex(
            "\\mathbf{S}_t = \\mathbf{S}_{t-1} (\\mathbf{I} - \\beta_t \\mathbf{k}_t \\mathbf{k}_t^\\top) + \\beta_t \\mathbf{v}_t \\mathbf{k}_t^\\top",
            font_size=32,
        ).set_color(GREY_B)
        nump = (
            RaenimPlane(
                x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], width=8, height=8
            ).scale(0.7)
        ).shift(UP * 0.5)
        nump.x_axis.set_opacity(0.7)
        nump.y_axis.set_opacity(0.7)
        dn_tex.next_to(nump, UP, buff=0.5)
        self.addw(nump, dn_tex)

        ## S_{t-1} arrow
        def get_arrow(plane, piui=[3]):
            np.random.seed(piui[0])
            piui[0] += 10
            noise = np.random.randn(2)
            arrow = Arrow(
                start=plane.c2p(0, 0),
                end=plane.c2p(noise[0], noise[1]),
                buff=0,
                thickness=1.5,
            ).set_color(GREEN)
            return arrow

        arr_prev = get_arrow(nump).set_color(GREEN)
        ul_prev = Underline(
            dn_tex[3:7], buff=0.05, stretch_factor=1.5, stroke_width=[1, 2.5, 2.5, 1]
        ).set_color(GREEN)
        self.playw(
            GrowArrow(arr_prev), FadeIn(ul_prev), dn_tex[3:7].animate.set_color(GREEN)
        )

        ## S_t arrow

        arr_now = get_arrow(nump).set_color(PURPLE)
        ul_now = Underline(
            dn_tex[-5:], buff=0.05, stretch_factor=1.5, stroke_width=[1, 2.5, 2.5, 1]
        ).set_color(PURPLE)
        self.playw(
            GrowArrow(arr_now), FadeIn(ul_now), dn_tex[-5:].animate.set_color(PURPLE)
        )

        ## two beta t
        betat1 = dn_tex[10:12]  # first beta_t
        betat2 = dn_tex[19:21]  # second beta_t
        interp_line = DashedLine(arr_prev.get_end(), arr_now.get_end()).set_color(BLUE)
        beta_dot = Dot(interp_line.get_center(), radius=0.07).set_color(BLUE)
        self.playw(
            VGroup(betat1, betat2)
            .animate(rate_func=there_and_back)
            .shift(DOWN * 0.5)
            .set_color(BLUE),
            Create(interp_line),
            GrowFromCenter(beta_dot),
            run_time=1,
        )

        ## alpha
        gdn_tex.move_to(dn_tex)
        gdn_tex[5:9].set_color(GREEN)
        gdn_tex[-5:].set_color(PURPLE)
        prev_idx = [slice(0, 3), slice(0, 3)]
        next_idx = [slice(3, None), slice(5, None)]
        self.playw(
            Transformr(dn_tex[prev_idx[0]], gdn_tex[prev_idx[1]]),
            Transformr(dn_tex[next_idx[0]], gdn_tex[next_idx[1]]),
            FadeIn(gdn_tex[3:5]),
            ul_prev.animate.shift(RIGHT*0.2),
            ul_now.animate.shift(RIGHT*0.2),
        )

        self.embed()
        ## alpha, beta
        alpha = gdn_tex[3:5]
        beta = VGroup(gdn_tex[12:14], gdn_tex[21:23])
        self.play(alpha.animate(rate_func=there_and_back).shift(DOWN*0.5))
        self.playw(beta.animate(rate_func=there_and_back).shift(DOWN*0.5))
