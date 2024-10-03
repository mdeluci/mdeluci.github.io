from manim import *

class VideoAsImageSequence(Scene):
    def construct(self):
        frame_count = 240  # Adjust this to the actual number of frames you have
        for i in range(1, frame_count + 1):
            frame = ImageMobject(f"Intro1_frame_{i:04d}.png")
            self.add(frame)
            self.wait(1 / 24)  # Assuming 24 frames per second
            self.remove(frame)

        self.wait(1)
