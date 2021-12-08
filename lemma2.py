from manim import *


"""
    Lemma 2:
        Dados los valores de b(e_1, u_1), ... , b(e_d-1, u_d-1)
        y sl-modelos M_1 de T[e_1, u_1], ..., M_d-1 de T[e_d-1, u_d-1]
        que logran fuertemente esos valores, respectivamente,
        es posible computar b(e_d, v) y un sl-modelo de T[e_d, v]
        que logra fuertemente b(e_d, v) en tiempo constante.

        Parafraseando; se pueden pegar dos subarboles optimos
        para crear un nuevo subarbol optimo en tiempo constante.

"""


class Lemma2part1(Scene):
    """Lemma 2 will be fragmented for speed reasons"""
    def construct(self):
        """ Here we will define the b(M)"""
        self.play(Create(Text("Hello")))