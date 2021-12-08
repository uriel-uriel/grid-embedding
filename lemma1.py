from manim import *
from networkx import descendants_at_distance


a='a'
b='b'
c='c'
d='d'
e='e'
f='f'
g='g'
h='h'
i='i'
j='j'
k='k'

COLORS = [RED_C, BLUE_C, YELLOW_C, GREEN_C]


class Lemma1(Scene):
    def construct(self):
        self.tree = Tree()
        self.T = self.tree.T
        self.smodel = self.tree.smodel
        self.partitions = self.tree.get_partitions_from(d)

        self.draw_tree()

        self.draw_slmodel()

        self.play(Create(self.T))
        self.wait(2)

        tree_g = VGroup(self.T)
        self.add(tree_g)

        # random root chosen
        self.play(self.T[d].animate.scale(2))
        self.play(self.T[d].animate.scale(0.5))
        self.wait()

        #

        p_text = MarkupText("Particiones de <i>T</i>").shift(DOWN*3)
        self.play(Create(p_text))
        self.highlight_partitions(d)
        self.add_labels()
        self.play(FadeOut(p_text))
        self.wait()

        # move them to the side to make space to explain
        self.play(tree_g.animate.scale(0.7))
        self.play(tree_g.animate.shift(LEFT*4))
        self.play(self.tree.sl_model.animate.scale(0.7))
        self.play(self.tree.sl_model.animate.shift(RIGHT*3))
        tree_g.add(self.tree.sl_model)
        self.play(tree_g.animate.scale(0.5))
        self.play(tree_g.animate.arrange_in_grid(rows=2, cols=1, buff=2.0))
        self.play(tree_g.animate.shift(LEFT*4.5))

        sl_text = MarkupText("Un modelo-rl de <i>T</i>").next_to(tree_g, DOWN).scale(0.7)
        self.play(Create(sl_text))

        # Build smodel
        self.play(Create(self.smodel[d].shift(RIGHT*2)))
        self.v_already_created = [d]
        self.e_already_created = []
        self.wait(2)

        # Missing in lemma when to add the vertex
        self.draw_level([d])

        self.wait(2)

        self.draw_level(self.partitions[0])

        self.wait(2)

        self.draw_level(self.partitions[1])

        self.wait()


    def draw_level(self, nbunch):
        for vertex in nbunch:
            edges_tbc = []
            edges = self.edges_of(vertex)
            for edge in edges:
                if edge not in self.e_already_created:
                    self.e_already_created.append(edge)
                    edges_tbc.append(Create(self.smodel.edges[edge].shift(RIGHT*2)))

            if len(edges_tbc) > 0: #vertex may not have uncreated edges
                self.play(*edges_tbc)

            self.wait(2)

            nodes_tbc = []
            for node in self.neighbors_of(vertex):
                if node not in self.v_already_created:
                    self.v_already_created.append(node)
                    nodes_tbc.append(Create(self.smodel[node].shift(RIGHT*2)))

            if len(nodes_tbc) > 0: #node may not have uncreated neighbors
                self.play(*nodes_tbc)

    def edges_of(self, node):
        return [tuple(sorted(ed)) for ed in self.smodel._graph.edges(node)]

    def neighbors_of(self, node):
        return list(self.smodel._graph.neighbors(node))

    def highlight_partitions(self, source):
        for index, level in enumerate(self.partitions):
            self.play(*[self.T[v].animate.set_color(COLORS[index]) for v in level])
            self.wait()

    def add_labels(self):
        for v in self.tree.V:
            self.T[v].add(MathTex(v, color=BLACK).move_to(self.T[v].get_center()))


    def draw_slmodel(self):
        sl_model = self.tree.sl_model
        text = MarkupText("Un ordenamiento local para <i>T</i>").next_to(sl_model, DOWN)
        self.play(Create(sl_model), Create(text))
        self.wait(2)
        self.play(FadeOut(sl_model), Uncreate(text))

    def draw_tree(self):
        text = MarkupText("Un árbol <i>T</i>").next_to(self.T, DOWN)
        self.play(Create(self.T), Create(text))
        self.wait(3)
        self.play(FadeOut(self.T), Uncreate(text))


class Tree():
    def __init__(self):
        self.V = [a, b, c, d, e, f, g, h, i, j, k]
        self.E = [(a, c), (b, c), (c, d), (d, e), (d, g), (f, g), (g, h), (g, j), (h, i), (h, k)]

        self.V_CFG = {v: {"radius":0.27} for v in self.V}

        self.T = Graph(self.V, self.E, labels=True, vertex_config=self.V_CFG, layout_scale=3)

        ortho_layout = {
            a:[-1,  1, 0],
            b:[-2,  0, 0],
            c:[-1,  0, 0],
            d:[ 0,  0, 0],
            e:[ 1,  0, 0],
            f:[-1, -1, 0],
            g:[ 0, -1, 0],
            h:[ 1, -1, 0],
            i:[ 2, -1, 0],
            j:[ 0, -2, 0],
            k:[ 1, -2, 0]
        }
        self.smodel = Graph(self.V, self.E, labels=True, vertex_config=self.V_CFG, layout_scale=3, layout=ortho_layout)

        self.g = self.T._graph
        self.sl_model = self._get_sl_model()

    def _get_sl_model(self):
        sl_model = []
        for v in self.V:
            neighbors = list(self.g.neighbors(v))
            mV = sorted(neighbors + [v])
            mE = list(self.g.edges(v))

            layout = self.get_orthogonal_layout(v, neighbors)

            cfg = {**self.V_CFG}
            cfg[v] = {"fill_color": GREEN_C, **cfg[v]}
            local_ordering = Graph(mV, mE, labels=True, vertex_config=cfg, layout=layout)

            sl_model.append(local_ordering)

        r1 = VGroup(*sl_model[:4]).arrange()
        r2 = VGroup(*sl_model[4:8]).arrange()
        r3 = VGroup(*sl_model[8:]).arrange()

        return VGroup(r1, r2, r3).arrange(direction=DOWN)


    def get_orthogonal_layout(self, root, neighbors):
        case = len(neighbors)

        layout = {root: [0, 0, 0]}

        if case == 1:
            layout[neighbors[0]] =  [1, 0, 0]
        elif case == 4:
            layout[neighbors[0]] = [0, 1, 0]
            layout[neighbors[1]] = [-1, 0, 0]
            layout[neighbors[2]] = [1, 0, 0]
            layout[neighbors[3]] = [0, -1, 0]
        elif case == 3:
            layout[neighbors[0]] = [-1, 0, 0]
            layout[neighbors[1]] = [1, 0, 0]
            layout[neighbors[2]] = [0, -1, 0]

        if root == c:
            layout[neighbors[0]] = [0, 1, 0]
            layout[neighbors[1]] = [-1, 0, 0]
            layout[neighbors[2]] = [1, 0, 0]

        return layout

    def get_partitions_from(self, source):
        level = 1
        partitions = []
        descendants = descendants_at_distance(self.g, source, level)

        while len(descendants) > 0:
            partitions.append(descendants)
            level+=1
            descendants = descendants_at_distance(self.g, source, level)

        return partitions