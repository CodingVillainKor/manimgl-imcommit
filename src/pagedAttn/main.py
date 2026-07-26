from manimlib import *
from raenimgl import *
from random import seed, shuffle

seed(41)
np.random.seed(41)

class kvcache(InteractiveScene, Scene2D):
    def construct(self):
        
        ## intro

        kv_box = Rectangle(width=4, height=2, color=GREY_C)
        kv_text = Text("KV Cache", font_size=24).align(kv_box, UL, buff=0.1).set_color(GREY_B)
        kv = VGroup(kv_box, kv_text).to_edge(RIGHT, buff=0.2)

        self.playw(FadeIn(kv))

        ## attn layer

        attn_box = Rectangle(width=7, height=5, color=GREY_C)
        attn_text = Text("Attention Layer", font_size=24).align(attn_box, UL, buff=0.1).set_color(GREY_B)

        attn = VGroup(attn_box, attn_text).shift(LEFT * 2)

        self.playw(FadeIn(attn))

        ## key, value

        key = Tensor(7, arrange=RIGHT, buff=0.2)
        value = Tensor(7, arrange=RIGHT, buff=0.2)
        keyval = VGroup(key, value).arrange(DOWN, buff=0.5).move_to(attn_box)
        keyt = Text("Key", font_size=24).next_to(key, LEFT, buff=0.2).set_color(GREY_B)
        valuet = Text("Value", font_size=24).next_to(value, LEFT, buff=0.2).set_color(GREY_B)

        self.playw(FadeIn(keyval), FadeIn(keyt), FadeIn(valuet))
        self.cf.save_state()
        self.playw(self.cf.animate.reorient(90, 42, -90, (np.float32(-5.69), np.float32(-0.02), np.float32(5.22)), 8.00))

        ## cache

        fn_name = Text("오래 걸리고 비싼 연산", font_size=24)
        fn_box = SurroundingRectangle(fn_name, color=GREY_C, buff=0.5).set_fill(BLACK, opacity=0.5)
        DIR = LEFT * np.sin(42 * DEGREES) + OUT * np.cos(42 * DEGREES)
        rotate = lambda m: m.rotate(42*DEGREES, axis=UP)
        fn = rotate(VGroup(fn_box, fn_name)).shift(DIR * 9)
        self.play(FadeIn(fn))
        self.add(fn.set_z_index(1))

        input_text = rotate(Tex("\\text{input: }\, x_1", font_size=36)).next_to(fn, DOWN, buff=0.5)
        input_text[-2:].set_color(YELLOW)
        x1 = input_text[-2:].copy()

        output_text = rotate(Tex("\\text{output: }\, y_1", font_size=36)).next_to(fn, UP, buff=0.5)
        output_text[-2:].set_color(RED)

        self.play(FadeIn(input_text))
        self.play(Transformr(x1, output_text[-2:]), FadeIn(output_text[:-2]))

        ## cache dict

        cache_box = Rectangle(width=2, height=1.5, color=GREEN)
        cache_text = Text("Cache", font_size=22).align(cache_box, UL, buff=0.1).set_color(GREY_B).set_color_by_gradient(GREEN, GREEN_D)
        cache = rotate(VGroup(cache_box, cache_text)).next_to(fn, DIR)
        x1c = input_text[-2:].copy()
        y1c = output_text[-2:].copy()
        xy1c = VGroup(x1c, y1c)
        colon = rotate(Tex(":", font_size=36)).move_to(cache_box)
        self.playw(FadeIn(cache), xy1c.animate.arrange(-DIR).move_to(cache_box), FadeIn(colon))

        ## fadeout input, output

        self.play(FadeOut(input_text), FadeOut(output_text), run_time=0.3)

        input_text2 = input_text.copy().move_to(input_text)
        self.playw(FadeIn(input_text2, shift=UP*0.5))

        self.play(Indicate(input_text2[-2:], color=PURE_BLUE), Indicate(xy1c[0], color=PURE_BLUE))

        y1cc = xy1c[1].copy()
        self.play(y1cc.animate.move_to(output_text[-2:]))
        self.playw(FadeIn(output_text[:-2]), run_time=0.3)

        ## fadeout all caches

        self.play(FadeOut(cache), FadeOut(colon), FadeOut(xy1c), FadeOut(fn), FadeOut(input_text2), FadeOut(output_text), FadeOut(y1cc), run_time=0.3)
        self.playw(self.cf.animate.restore())

        ## keyvalue to kv box
        keyval.save_state()
        self.playw(keyval.animate.move_to(kv_box).scale(0.75))

        ## append one sample to key, value

        k = Tensor(1).next_to(keyval.saved_state[0], RIGHT, buff=0.2)
        v = Tensor(1).set_fill(color=random_color()).next_to(keyval.saved_state[1], RIGHT, buff=0.2)
        self.play(FadeIn(k, shift=DOWN*5), FadeIn(v, shift=DOWN*5))
        self.playw(Restore(keyval))

        ## circumscribe new key, value

        self.playw(Circumscribe(k, color=YELLOW), Circumscribe(v, color=YELLOW), run_time=0.7)
        self.playw(Circumscribe(VGroup(key, k)), Circumscribe(VGroup(value, v)))

        key = VGroup(*key, k)
        value = VGroup(*value, v)

        ## indicate each one
        self.playw(
            AnimationGroup(*[Indicate(k, color=RED) for k in key], lag_ratio=0.1),
            AnimationGroup(*[Indicate(v, color=RED) for v in value], lag_ratio=0.1)
        )

        ## kv caching
        keyval = VGroup(key, value)
        self.playw(
            keyval.animate.move_to(kv_box).scale(0.9).align(kv_box, LEFT, buff=0.2)
        )

        ## camera to kv box

        self.play(self.cf.animate.reorient(-90, 49, 90, (np.float32(5.59), np.float32(-0.05), np.float32(0.7)), 8.00), run_time=0.7)
        self.playw(kv_box.animate.stretch_to_fit_width(28).align_to(kv_box, LEFT))

class redundantGPU(InteractiveScene, Scene2D):
    def construct(self):
        ## intro

        gpu_box = Rectangle(width=7, height=4, color=GREY_C)
        gpu_text = Text("GPU", font_size=24).align(gpu_box, UL, buff=0.1).set_color(GREY_B)
        gpu = VGroup(gpu_box, gpu_text)

        self.playw(FadeIn(gpu))

        ## blocks

        block1 = Rectangle(width=3, height=1.7, color=GREEN)
        block1_text = Text("Block 1", font_size=22).align(block1, UL, buff=0.1).set_color(GREY_B)
        block2 = Rectangle(width=3, height=1.7, color=GREEN)
        block2_text = Text("Block 2", font_size=22).align(block2, UL, buff=0.1).set_color(GREY_B)
        block3 = Rectangle(width=3, height=1.7, color=GREEN)
        block3_text = Text("Block 3", font_size=22).align(block3, UL, buff=0.1).set_color(GREY_B)

        block1 = VGroup(block1, block1_text)
        block2 = VGroup(block2, block2_text)
        block3 = VGroup(block3, block3_text)

        block1.move_to(gpu_box).shift(UL * 0.2 + LEFT * 1.7)
        block2.move_to(gpu_box).shift(DOWN * 0.8 + RIGHT * 1.3)
        block3.move_to(gpu_box).shift(UP * 1.05 + RIGHT * 1.8)

        self.playw(FadeIn(block1), FadeIn(block2), FadeIn(block3))

        ## new block fail to allocate

        block4 = Rectangle(width=3, height=1.7, color=GREEN).next_to(block1, DOWN).shift(LEFT*8)
        block4_text = Text("Block 4", font_size=22).align(block4, UL, buff=0.1).set_color(GREY_B)
        block4 = VGroup(block4, block4_text)

        self.add(block4)

        self.playw(block4.animate.next_to(block1, DOWN, buff=0.1).shift(RIGHT*0.1))


        self.playw(block4[0].animate.set_color(PURE_RED), gpu_box.animate.set_color(PURE_RED))

class pagedAttn(InteractiveScene, Scene2D):
    def construct(self):
        ## intro

        def get_gpu_box(num_row, num_col):
            block = Square(side_length=0.5, color=GREY_C)
            blocks = VGroup(*[block.copy() for _ in range(num_row * num_col)])
            blocks.arrange_in_grid(num_row, num_col, buff=0.0)
            return blocks

        gpu_box = get_gpu_box(8, 20)
        mock_box = Rectangle(width=gpu_box.get_width(), height=gpu_box.get_height(), color=GREY_C)
        gpu_text = Text("GPU", font_size=24).next_to(gpu_box, UP, buff=0.1).align(gpu_box, LEFT, buff=0.1)
        gpu = VGroup(gpu_box, gpu_text)

        self.playw(FadeIn(mock_box), FadeIn(gpu[1]))

        self.playw(FadeTransform(mock_box, gpu_box))

        ## one block

        b = gpu_box[len(gpu_box)//2 + 10].copy()
        self.cf.save_state()
        self.play(self.cf.animate.reorient(0, 61, 0, (np.float32(0.05), np.float32(0.14), np.float32(0.21))), b.animate.rotate(61 * DEGREES, axis=RIGHT).shift(OUT * 2), gpu_box.animate.set_stroke(opacity=0.2))
        rotate = lambda m: m.rotate(61 * DEGREES, axis=RIGHT)
        kvblock_text = rotate(Text("KV Block", font_size=24)).next_to(b, RIGHT).set_color(GREY_B)

        self.playw(FadeIn(kvblock_text, shift=RIGHT*0.6, scale=2))

        def get_kvs():
            kvs = Rectangle(width=gpu_box[0].get_width()/4, height=gpu_box[0].get_height(), color=GREY_C).set_stroke(width=1)
            return kvs

        kvss = rotate(VGroup(*[get_kvs().copy().set_fill(random_color(), opacity=0.5) for _ in range(4)])).arrange(RIGHT, buff=0.0).move_to(b)
        self.playw(FadeIn(kvss))

        ## fadeout all in rotated camera view

        self.play(FadeOut(kvblock_text), FadeOut(kvss), FadeOut(b), run_time=0.4)
        self.playw(Restore(self.cf), gpu_box.animate.set_stroke(opacity=1.0))

        ## kv caching "Four score and seven years ago our"
        word_seq = "Four score and seven years ago our".split(" ")

        sentence = Words(" ".join(word_seq), font_size=24).next_to(gpu_box, DOWN)
        anims = [FadeIn(w, shift=UP*0.5) for w in sentence.words]
        anims.insert(1, self.cf.animate.shift(DOWN))
        self.playwl(*anims, lag_ratio=0.5)

        kvs = VGroup(*[get_kvs().set_fill(random_color(), opacity=0.5).next_to(sentence.words[i], DOWN) for i in range(len(word_seq))])
        for kv in kvs[1:]:
            kv.align_to(kvs[0], UP)
        self.playw(Transformr(sentence.words.copy(), kvs))

        ## blocks
        len_blocks = len(gpu_box)
        box_idxs = list(range(len_blocks))
        shuffle(box_idxs)

        kvst = kvs.generate_target()

        b0 = gpu_box[box_idxs[0]]
        kvst[:4].arrange(RIGHT, buff=0).move_to(b0)

        b1 = gpu_box[box_idxs[1]]
        kvst[4:8].arrange(RIGHT, buff=0).move_to(b1).align_to(b1, LEFT)

        self.playw(MoveToTarget(kvs, path_arc=90*DEGREES), sentence.animate.shift(LEFT*4))

        ## indicate boxes
        self.playw(Circumscribe(VGroup(b0, kvs[:4])), Circumscribe(VGroup(b1, kvs[4:8])))

        ## block table

        texts = [Text(str(box_idxs[0]), font_size=24, font=MONO_FONT), Text(str(box_idxs[1]), font_size=24, font=MONO_FONT)]
        block_table = Joiner(*texts, join=lambda: Text("/", font_size=24, font=MONO_FONT)).arrange(RIGHT).next_to(gpu_box, DOWN, buff=1.2).set_color(GREEN)

        self.play(FadeIn(block_table))

        lines = VGroup(*[Arrow(start=texts[i].get_top() + UP * 0.05, end=b.get_bottom(), color=GREY_B, buff=0.1, thickness=2) for i, b in enumerate([b0, b1])])
        self.playw(FadeIn(lines))

        ## blocktable text

        blocktable_text = Text("Block Table", font_size=24).next_to(block_table, LEFT, buff=0.3).set_color(GREEN)
        self.playw(FadeIn(blocktable_text))

        ## block table scale
        block_table.save_state()
        self.playw(*[item.animate.scale(1.4).set_color(PURE_GREEN) for item in block_table], run_time=3)

        self.playw(Restore(block_table))

        ## answers:

        answer_text = "father"
        answer = Text(answer_text, font_size=24).next_to(sentence, RIGHT, buff=0.1).set_color(YELLOW)
        self.play(FadeIn(answer))

        kv_answer = get_kvs().set_fill(random_color(), opacity=0.5).next_to(answer, DOWN, buff=0.1)
        self.playw(Transformr(answer.copy(), kv_answer))

        self.playw(kv_answer.animate.next_to(kvs[-1], RIGHT, buff=0))
        kvs.add(kv_answer)

        ## answer2 : "was"

        answer_text2 = "was"
        answer2 = Text(answer_text2, font_size=24).next_to(answer, RIGHT, buff=0.1).set_color(YELLOW)
        self.play(FadeIn(answer2))

        kv_answer2 = get_kvs().set_fill(random_color(), opacity=0.5).next_to(answer2, DOWN, buff=0.1)
        self.play(Transformr(answer2.copy(), kv_answer2))

        b2 = gpu_box[box_idxs[2]]
        self.play(kv_answer2.animate.move_to(b2).align_to(b2, LEFT))

        kvs.add(kv_answer2)


        btc = block_table.copy().set_opacity(0)
        block_table.add(Text(str(box_idxs[2]), font_size=24, font=MONO_FONT).next_to(block_table[-1], RIGHT, buff=0.1)).set_color(GREEN)
        block_table.arrange(RIGHT).move_to(btc).align_to(btc, LEFT)

        line2 = Arrow(start=block_table[-1].get_top() + UP * 0.05, end=b2.get_bottom(), color=GREY_B, buff=0.1, thickness=2)

        self.playw(FadeIn(block_table[-2:]), FadeIn(line2))


        ## logically linked

        self.playwl(*[Indicate(kvs[i], color=PURE_GREEN) for i in range(len(kvs))], lag_ratio=0.1)

class pagedAttnConcurrent(InteractiveScene, Scene2D):
    def construct(self):
        ## intro

        def get_gpu_box(num_row, num_col):
            block = Square(side_length=0.5, color=GREY_C)
            blocks = VGroup(*[block.copy() for _ in range(num_row * num_col)])
            blocks.arrange_in_grid(num_row, num_col, buff=0.0)
            return blocks

        gpu_box = get_gpu_box(7, 20)
        mock_box = Rectangle(width=gpu_box.get_width(), height=gpu_box.get_height(), color=GREY_C)
        gpu_text = Text("GPU", font_size=24).next_to(gpu_box, UP, buff=0.1).align(gpu_box, LEFT, buff=0.1)
        gpu = VGroup(gpu_box, gpu_text).shift(UP * 1.5)


        self.addw(gpu)

        ## two sentences

        word_seq1 = "Solve this problem : What is the answer of 2 + 3".split(" ")
        word_seq2 = "Solve this problem : What is the answer of 5 + 7".split(" ")

        sentence1 = Words(" ".join(word_seq1), font_size=24).next_to(gpu_box, DOWN, buff=0.75).set_color(GREY_A)
        sentence2 = Words(" ".join(word_seq2), font_size=24).next_to(sentence1, DOWN, buff=0.1).set_color(GREY_A)
        sentence1.words[-3:].set_color(YELLOW)
        sentence2.words[-3:].set_color(PURPLE)

        self.playw(FadeIn(sentence1), FadeIn(sentence2))

        self.play(Circumscribe(sentence1.words[:-3], buff=0.05), Circumscribe(sentence2.words[:-3], buff=0.05))

        ## kvs1, kvs2
        def get_kvs():
            kvs = Rectangle(width=gpu_box[0].get_width()/4, height=gpu_box[0].get_height(), color=GREY_C).set_stroke(width=1)
            return kvs
        kvs1 = VGroup(*[get_kvs().set_fill(random_color(), opacity=0.5).next_to(sentence1.words[i], UP, buff=0.1) for i in range(len(word_seq1))])
        for kv in kvs1[1:]:
            kv.align_to(kvs1[0], UP)
        kvs2 = VGroup(*[get_kvs().set_fill(kvs1[i].get_fill_color() if i < 9 else random_color(), opacity=0.5).next_to(sentence2.words[i], DOWN, buff=0.1) for i in range(len(word_seq2))])
        for kv in kvs2[1:]:
            kv.align_to(kvs2[0], UP)

        self.play(Transformr(sentence1.words.copy(), kvs1), Transformr(sentence2.words.copy(), kvs2))

        self.embed()
        ## blocks
        block_idxs = list(range(len(gpu_box)))
        shuffle(block_idxs)

        b0, b1, b2 = gpu_box[block_idxs[0]], gpu_box[block_idxs[1]], gpu_box[block_idxs[2]]
        b3 = gpu_box[block_idxs[3]]

        kvs1t = kvs1.generate_target()
        kvs1t[:4].arrange(RIGHT, buff=0).move_to(b0)
        kvs1t[4:8].arrange(RIGHT, buff=0).move_to(b1)

        self.play(FadeOut(kvs2[:8], shift=DOWN))
        
        self.play(MoveToTarget(kvs1))
        sr1 = SurroundingRectangle(VGroup(sentence1.words[:4], sentence2.words[:4]), buff=0.05).set_stroke(width=2, color=GREEN)
        sr2 = SurroundingRectangle(VGroup(sentence1.words[4:8], sentence2.words[4:8]), buff=0.05).set_stroke(width=2, color=GREEN)
        line1 = Arrow(start=sr1.get_top() + UP * 0.05, end=b0.get_bottom(), color=GREY_B, buff=0.1, thickness=2)
        line2 = Arrow(start=sr2.get_top() + UP * 0.05, end=b1.get_bottom(), color=GREY_B, buff=0.1, thickness=2)
        self.playw(FadeIn(sr1), FadeIn(sr2), FadeIn(line1), FadeIn(line2), run_time=0.5)
        

        kvs1t = kvs1.generate_target()
        kvs1t[8:].arrange(RIGHT, buff=0).move_to(b2)
        kvs28 = kvs2[8:]
        kvs2t8 = kvs28.generate_target()

        kvs2t8.arrange(RIGHT, buff=0).move_to(b3).align_to(b3, LEFT)

        self.play(MoveToTarget(kvs1), MoveToTarget(kvs28))
        sr3 = SurroundingRectangle(sentence1.words[8:], buff=0.05).set_stroke(width=2, color=GREEN)
        sr4 = SurroundingRectangle(sentence2.words[8:], buff=0.05).set_stroke(width=2, color=GREEN)
        line3 = Arrow(start=sr3.get_top() + UP * 0.05, end=b2.get_bottom(), color=GREY_B, buff=0.1, thickness=2)
        line4 = Arrow(start=sr4.get_top() + UP * 0.05, end=b3.get_bottom(), color=GREY_B, buff=0.1, thickness=2)

        self.playw(FadeIn(sr3), FadeIn(sr4), FadeIn(line3), FadeIn(line4), run_time=0.5)



