from manim import *


class SLModel(Scene):
    def construct(self):
        a='a'
        b='b'
        c='c'
        d='d'
        e='e'
        f='f'

        vertices = [a, b, c, d, e, f]
        edges = [(a,e), (f,e), (b,e), (e,c), (c,d)]
        ortho_layout = {a:[-1, 0, 0], b:[0, -1, 0], c:[1, 0, 0], d:[1, 1, 0], e:[0, 0, 0], f:[0, 1, 0]}

        vertex_conf = {k: {"radius":0.27} for k in vertices}

        g = Graph(vertices, edges, labels=True, vertex_config=vertex_conf, layout_scale=3)

        text = MarkupText("Un árbol <i>T</i>").next_to(g, DOWN)

        self.play(Create(g), Create(text))

        self.wait()

        text2 = MarkupText("Un s-modelo de <i>T</i>").next_to(g, DOWN)
        self.play(g.animate.change_layout(ortho_layout),
                    Transform(text, text2))

        self.highlight_edge(g, a, (a,e))

        self.wait()
        sla = Graph([a,e], [(a,e)], vertex_config=vertex_conf, labels=True, layout={a:ortho_layout[a], e:[0, 0, 0]})
        self.play(g.animate.shift(2*LEFT), FadeOut(text), sla.animate.move_to(RIGHT*3 + UP * 2.5))


        self.highlight_edge(g, c, (e,c), (c,d))

        slc = Graph([c, d, e], [(e,c), (c, d)], vertex_config=vertex_conf, labels=True, layout={c:ortho_layout[c], d:ortho_layout[d], e:[0, 0, 0]})
        self.play(slc.animate.next_to(sla, DOWN))


        self.highlight_edge(g, e, (e, c), (a, e), (b, e), (f,e))

        self.wait()
        sle = Graph([c, a, b, f, e], [(e, c), (a, e), (b, e), (f,e)], vertex_config=vertex_conf, labels=True,
            layout={c:ortho_layout[c], b:ortho_layout[b], a:ortho_layout[a], f:ortho_layout[f], e:[0, 0, 0]})
        self.play(sle.animate.next_to(slc, RIGHT))


        self.highlight_edge(g, b, (b,e))
        self.highlight_edge(g, d, (c,d))
        self.highlight_edge(g, f, (f,e))

        slb = Graph([b, e], [(b, e)], vertex_config=vertex_conf, labels=True, layout={b:ortho_layout[b], e:ortho_layout[e]})
        sld = Graph([c, d], [(c, d)], vertex_config=vertex_conf, labels=True, layout={c:ortho_layout[c], d:ortho_layout[d]})
        slf = Graph([f, e], [(f, e)], vertex_config=vertex_conf, labels=True, layout={f:ortho_layout[f], e:ortho_layout[e]})
        self.play(slb.animate.next_to(slc, DOWN),
                    sld.animate.next_to(slb, RIGHT),
                    slf.animate.next_to(sld, RIGHT))

        # group all sl-models and attach the text

        self.wait()
        slmodel = VGroup(sla, slb, slc, sld, sle, slf)
        self.play(slmodel.animate.arrange().move_to([0, 0, 0]), FadeOut(g))

        sltext = MarkupText("Un sl-modelo de <i>T</i>")
        sltext.next_to(slmodel, DOWN)
        self.play(FadeIn(sltext))
        self.wait()

    def highlight_edge(self, g, v, *edges):
        self.play(g[v].animate.set_fill(RED), *[g.edges[edge].animate.set_color(RED) for edge in edges])
        self.wait()
        self.play(g[v].animate.to_original_color(), *[g.edges[edge].animate.set_color(WHITE) for edge in edges])