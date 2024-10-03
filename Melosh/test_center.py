from manim import *

class CenteredText(Scene):
    def construct(self):
        title = Tex(r'Centered Text').move_to(ORIGIN)
        self.play(Write(title))
        self.wait()