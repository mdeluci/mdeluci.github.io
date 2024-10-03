from manim import *
from manim_slides import Slide
import os
import shutil
from moviepy.editor import VideoFileClip
from PIL import Image
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from manim.utils.rate_functions import linear
from scipy.integrate import solve_ivp

shared_elements = {}


class CustomSlide(Slide):  # Inherit from Slide instead of Scene
    offset = 0.0
    breaks = [0]
    video_slides_dir = "./video_slides"

    def setup(self):
        super().setup()
        self.breaks = [0]

    def slide_break(self, t=0.5):
        self.breaks += [self.renderer.time + t/2 + self.offset]
        self.wait(t)

    def add_to_offset(self, t):
        self.offset += t

    def save_times(self):
        self.breaks += [self.renderer.time + self.offset]
        out = ""
        dirname = os.path.dirname(self.renderer.file_writer.movie_file_path)
        for i in range(len(self.breaks) - 1):
            out += f"<p class=\"fragment\" type='video' time_start={self.breaks[i]} time_end={self.breaks[i+1]}></p>\n"
        with open(f"{dirname}/{type(self).__name__}.txt", 'w') as f:
            f.write(out)

    def copy_files(self):
        if self.video_slides_dir is not None:
            dirname = os.path.dirname(self.renderer.file_writer.movie_file_path)
            slide_name = type(self).__name__
            if not os.path.exists(self.video_slides_dir):
                os.makedirs(self.video_slides_dir)
            shutil.copy2(os.path.join(dirname, f"{slide_name}.mp4"), self.video_slides_dir)
            shutil.copy2(os.path.join(dirname, f"{slide_name}.txt"), self.video_slides_dir)

    def tear_down(self):
        super().tear_down()
        self.save_times()

    def print_end_message(self):
        super().print_end_message()
        self.copy_files()

toc = Group(
    Tex("1. Motivation"),
    Tex("2. Mechanics"),
    Tex("3. Drug transport and absorption"),
    Tex("4. Conclusions")
).arrange(DOWN, aligned_edge=LEFT, buff=0.4)

class Title(CustomSlide):
    def construct(self):
        title = Tex(r'A Data-Driven Finite Element Model for \\ High-Fidelity Simulation of Biotherapeutic \\ Transport and Absorption').scale(1.25).shift(2.5*UP)
        name = Tex(r'Mario de Lucio Alonso').scale(1.00).shift(0.45*DOWN)
        comp = Tex(r'Annual Robert J. Melosh Medal Competition \\ For The  Best Student Paper On Finite Element Analysis').scale(0.6).next_to(name, UP).shift(0.2*UP)
        collab = Tex('Hector Gomez').scale(0.8).next_to(name, DOWN).shift(0.2*DOWN)
        purdue = SVGMobject("purdue_logo.svg").shift(2.5*DOWN).scale(1/3)

        self.play(FadeIn(comp))
        self.next_slide()  # Adds interactivity

        self.play(FadeIn(name))
        self.next_slide()  # Adds interactivity

        self.play(FadeIn(title))
        self.next_slide()  # Adds interactivity


        self.play(FadeIn(collab))

        self.play(Write(purdue))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(name, title, purdue, collab, comp))
        self.next_slide()  # Adds interactivity

        self.add(toc)  # Ensure toc is added to the scene
        self.play(FadeIn(toc))
        self.next_slide()  # Adds interactivity

        self.play(toc[0].animate.scale(1.2).set_color(YELLOW))
        self.next_slide()  # Adds interactivity

        for i in range(1, len(toc)):
            self.play(toc[i].animate.scale(1.2).set_color(YELLOW), toc[i-1].animate.scale(1/1.2).set_color(WHITE))
            self.next_slide()  # Adds interactivity

        self.play(toc[-1].animate.scale(1/1.2).set_color(WHITE))

class Intro(CustomSlide):
    def construct(self):
        self.add(toc)  # Add toc to the scene at the beginning

        # Move the first item in toc to heading
        heading = toc[0].copy().move_to(ORIGIN).scale(1.25).to_corner(UP)

        # Instead of fading out all of toc, first isolate toc[0]
        self.play(ReplacementTransform(toc[0], heading))

        # Now fade out the rest of toc
        self.play(FadeOut(toc[1:]))

        self.next_slide()  # Adds interactivity

        # Proceed with the rest of the scene...
        Title_mAbs = Tex("Biotherapeutics (Monoclonal Antibodies or mAbs)").move_to(2*UP)
        Advantages_mAbs = BulletedList("Effective against multiple diseases (Cancer, diabetes, arthritis)", "Allow self-administration $\\rightarrow$ reduces healthcare costs").set_color(GREEN).move_to(0.72*UP)
        Economic = Tex("$\\rightarrow$", " Increased economic importance").move_to(DOWN).set_color(YELLOW)
        self.play(Write(Title_mAbs))
        self.next_slide()  # Adds interactivity
        # Include the video frames in the bottom right corner
        frame_dir = "./Intro2"
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])
        # Select a subset of frames for debugging (e.g., every 10th frame, or the first 10 frames)
        subset_frame_files = frame_files[::1]  # Every 10th frame
        # Or to select the first 10 frames:
        # subset_frame_files = frame_files[:10]
        for frame_file in subset_frame_files:
            frame_path = os.path.join(frame_dir, frame_file)
            frame = ImageMobject(frame_path)
            frame.scale(1.5)  # Scale the frame
            frame.to_corner(DOWN + ORIGIN)  # Position it in the bottom right corner
            self.add(frame)
            self.wait(1 / 20)  # Adjust this to control the display duration of each frame
            self.remove(frame)
        self.play(FadeIn(Advantages_mAbs[0], shift=0.5*UP))
        self.next_slide()  # Adds interactivity

        self.play(FadeIn(Advantages_mAbs[1], shift=0.5*UP))

        # Include the video frames in the bottom right corner
        frame_dir = "./Intro1"
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])
        subset_frame_files = frame_files[::1]  # Every 10th frame
        for frame_file in subset_frame_files:
            frame_path = os.path.join(frame_dir, frame_file)
            frame = ImageMobject(frame_path)
            frame.scale(0.4)  # Scale the frame
            frame.to_corner(DOWN + ORIGIN)  # Position it in the bottom right corner
            self.add(frame)
            self.wait(1 / 24)  # Adjust this to control the display duration of each frame
            self.remove(frame)
        self.next_slide()  # Adds interactivity
        self.play(Write(Economic))

        self.play(FadeOut(Title_mAbs, Advantages_mAbs))
        self.next_slide()  # Adds interactivity
        # Instead of fading out all of toc, first isolate toc[0]
        Economic_top = Tex("Economic impact of mAbs").move_to(2*UP)
        self.play(ReplacementTransform(Economic, Economic_top))
        self.next_slide()  # Adds interactivity

        market_value = SVGMobject("data_spending.svg").scale(2.0).shift(ORIGIN).shift(1.2*DOWN)
        label2 = Tex("mAbs Global Market Size").next_to(market_value, UP).scale(0.6)
        self.play(Write(market_value))
        self.play(Write(label2))
        self.next_slide()  # Adds interactivity
        self.play(FadeOut(market_value, label2,Economic_top))
        self.next_slide()  # Adds interactivity

        Disadvantages_title = Tex("Disadvantages of mAbs:").move_to(2*UP)
        Disadvantages_mAbs = BulletedList("Low Bioavailability", "Only 40-60 \% of the injected drug is absorbed").set_color(RED).move_to(0.72*UP)
        Solution = Tex("$\\rightarrow$", "Larger injection volumes at higher concentrations").move_to(DOWN).set_color(YELLOW)
        self.play(Write(Disadvantages_title))
        self.next_slide()  # Adds interactivity
        self.play(Write(Disadvantages_mAbs))
        self.next_slide()  # Adds interactivity
        self.play(Write(Solution))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(Disadvantages_title,Disadvantages_mAbs))

        Solution_top = Tex("Large injection volumes at higher concentrations").move_to(2*UP)
        self.play(ReplacementTransform(Solution, Solution_top))

        #visco_volume = SVGMobject("volume_concentration_viscoisity.svg").scale(2.0).shift(ORIGIN).shift(1.2*DOWN)
        visco_volume1 = ImageMobject("volume_visco_1.png").scale(0.8).move_to(ORIGIN+DOWN)
        visco_volume2 = ImageMobject("volume_visco_2.png").scale(0.8).move_to(ORIGIN+DOWN)
        label3 = Tex("Injection volume and viscosity vs. drug concentration").next_to(market_value, UP).scale(0.6)
        self.play(Write(label3))
        self.play(FadeIn(visco_volume1))
        self.next_slide()  # Adds interactivity
        self.play(FadeIn(visco_volume2))
        self.next_slide()  # Adds interactivity
        visco_problem = Tex("$\\rightarrow$ Higher visocsity can slow down absorption rates").next_to(visco_volume2,DOWN,buff=0.2).scale(0.7)
        self.play(Write(visco_problem))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(visco_volume1,visco_volume2,label3,visco_problem,Solution_top))
        self.next_slide()  # Adds interactivity


        PKPD = Tex("Pharmacokinetic/Pharmacodynamic models ", "(PK/PD)")
        PKPD[1].set_color(YELLOW)
        self.play(Write(PKPD))
        self.play(PKPD .animate.move_to(2.2*UP))
        self.next_slide()  # Adds interactivity


        #pk_equation = MathTex("\frac{dC}{dt} = -k \cdot C")
        #self.play(Write(pk_equation))

         # Create the Dose text
        dose_text = Tex("Drug").scale(0.8).to_edge(LEFT).shift(RIGHT*0.6)

        # Create the circles for A1 and A2
        A1_circle = Circle(radius=0.8).shift(LEFT * 2)
        A2_circle = Circle(radius=0.8).shift(RIGHT * 1.8)

        # Labels for A1 and A2 using MathTex for mathematical rendering
        A1_label = MathTex("A_1").move_to(A1_circle.get_center())
        A2_label = MathTex("A_2").move_to(A2_circle.get_center())

        # Adjust the position of ka / F so it is higher above the arrow
        ka_F_label = MathTex(r"k_\text{abs}").next_to(A1_circle, RIGHT, buff=0.7).scale(0.8).shift(UP * 0.3 + LEFT * 0.1)

        # CL/V label next to A2
        CL_V_label = MathTex(r"k_e").next_to(A2_circle, RIGHT, buff=0.7).scale(0.8).shift(UP * 0.3 + RIGHT * 0.2)

        Cp_label = MathTex(r"C_p").next_to(A2_circle, RIGHT, buff=1.0).scale(0.9).shift(RIGHT * 1.5)


        # Arrows connecting the objects
        dose_to_A1 = Arrow(start=dose_text.get_right(), end=A1_circle.get_left(), buff=0.1)
        A1_to_A2 = Arrow(start=A1_circle.get_right(), end=A2_circle.get_left(), buff=0.1)
        A2_to_exit = Arrow(start=A2_circle.get_right(), end=Cp_label.get_left(), buff=0.1)

        # Equations (positioned below the diagram)
        equations = MathTex(
            r"\frac{dA_1}{dt} = -k_\text{abs} A_1",
            r"\frac{dA_2}{dt} = k_\text{abs} A_1 - k_e A_2",
            r"C_p = \frac{A_2}{V}"
        ).arrange(DOWN, buff=0.3).scale(0.7).to_edge(DOWN)

        # Shift everything up a little to make space for equations
        all_objects = VGroup(A1_circle, A2_circle, A1_label, A2_label, dose_text, ka_F_label, CL_V_label, dose_to_A1, A1_to_A2, A2_to_exit,Cp_label)
        all_objects.shift(UP * 0.6)

        # Animation steps
        self.next_slide()  # Adds interactivity
        self.play(Write(dose_text))
        self.next_slide()  # Adds interactivity
        self.play(GrowArrow(dose_to_A1))
        self.next_slide()  # Adds interactivity
        self.play(Create(A1_circle), Write(A1_label))
        self.next_slide()  # Adds interactivity
        self.play(GrowArrow(A1_to_A2), Write(ka_F_label))
        self.next_slide()  # Adds interactivity
        self.play(Create(A2_circle), Write(A2_label))
        self.next_slide()  # Adds interactivity
        self.play(GrowArrow(A2_to_exit), Write(CL_V_label), Write(Cp_label))
        self.next_slide()  # Adds interactivity

        # Add the equations below
        #self.play(Write(equations))

        # Keep the final scene on screen for a while
        self.next_slide()  # Adds interactivity

        # Move the equations to the left interactively
        self.play(Write(equations))
        self.play(equations.animate.shift(LEFT * 3.5), run_time=2, rate_func=linear)

        # Keep the animation on screen for a while
        self.next_slide()  # Adds interactivity

        # Now let's create the plot for both Absorption site and Plasma Concentration
        # Create smaller axes for the graph (time in days and plasma concentration %)
        axis = Axes(
            x_range=[0, 10, 1], y_range=[0, 100, 20],
            x_length=10, y_length=6,  # Make the graph smaller
            axis_config={"include_ticks": False}  # Smaller arrow tips
        ).shift(DOWN * 2 + RIGHT * 3).scale(0.5)  # Shift the plot down and to the right

        # Add labels for the axes
        x_label = MathTex("t").move_to(axis.coords_to_point(10.6, 0))
        #y_label = MathTex("C_p").move_to(axis.coords_to_point(0, 50))
        # Rotate the y-axis label by 90 degrees
        #y_label.rotate(90 * DEGREES).next_to(axis.y_axis, LEFT, buff=0.1)

        Cp_y_label = MathTex("C_p").set_color(RED).next_to(axis.y_axis, LEFT, buff=0.1)
        A1_y_label = MathTex("A_1").set_color(BLUE).next_to(Cp_y_label, DOWN, aligned_edge=LEFT)

        # Rotate the y-axis labels by 90 degrees
        Cp_y_label.rotate(90 * DEGREES)
        A1_y_label.rotate(90 * DEGREES)

        # Combine both labels into a VGroup for positioning
        y_labels = VGroup(Cp_y_label, A1_y_label).arrange(DOWN, aligned_edge=LEFT).next_to(axis.y_axis, LEFT, buff=0.1)

        # Create an initial absorption site decay graph (exponential decay)
        time_vals = np.linspace(0, 10, 90)
        absorption_vals = 90 * np.exp(-0.5 * time_vals)  # Example exponential decay for absorption site

        absorption_graph = axis.plot_line_graph(
            x_values=time_vals, y_values=absorption_vals, add_vertex_dots=False, line_color=BLUE
        )

        # Solve ODE for Plasma Concentration and Absorption Site
        # Parameters
        k_a = 0.5  # absorption rate constant
        k_e = 0.1  # elimination rate constant
        V = 1.0    # volume of distribution
        A_abs_0 = 100  # initial amount of drug in absorption site
        C_0 = 0     # initial concentration in the central compartment
        y0 = [A_abs_0, C_0]

        # Time span for the simulation
        def pkpd_ode(t, y):
            A_abs, C = y
            dA_abs_dt = -k_a * A_abs
            dC_dt = (k_a * A_abs) / V - k_e * C
            return [dA_abs_dt, dC_dt]

        sol = solve_ivp(pkpd_ode, (0, 10), y0, t_eval=time_vals)
        plasma_conc_vals_ode = sol.y[1]

        # Plot the plasma concentration solution (ODE result)
        plasma_graph_ode = axis.plot_line_graph(
            x_values=time_vals, y_values=plasma_conc_vals_ode, add_vertex_dots=False, line_color=RED
        )

        # Show the plot, axes, and labels
        self.play(Create(axis), FadeIn(x_label, y_labels))
        self.play(Create(absorption_graph), Create(plasma_graph_ode))

        # Pause for a moment to let the audience take in the full animation
        self.next_slide()
        self.play(FadeOut(all_objects))

        Disadvantages_PKPD = BulletedList("PKPD models ignore biomechanical effects.", "Inaccurate initial conditions.").set_color(RED).move_to(1.2*UP).scale(0.7)
        self.next_slide()  # Adds interactivity

        Solution = Tex("$\\rightarrow$", "Inform PKPD models with initial conditions from high-fidelity FEM simulations.").move_to(DOWN*0.08).set_color(YELLOW).scale(0.7)
        self.play(Write(Disadvantages_PKPD))
        self.next_slide()  # Adds interactivity
        self.play(Write(Solution))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(Disadvantages_PKPD,absorption_graph,plasma_graph_ode,axis,PKPD,y_labels,x_label))

        Solution_top = Tex("Data-Driven FEM for High-fidelity Simulation").move_to(2*UP)
        self.play(ReplacementTransform(Solution, Solution_top))


        # Create the text for each box
        PP_text = Text("Physiological \nparameters", font_size=20)  # Text with smaller font size
        IGAFEM_text = Text("IGA based FEM", font_size=20)
        PKPD_text = Text("PK/PD Models", font_size=20)
        Histology_text = Text("Histology data", font_size=20)
        Devices_text = Text("Injection devices \nand techniques", font_size=20)


        # Create rounded rectangles with width and height based on the text bounding box
        IGAFEM = RoundedRectangle(corner_radius=0.2, width=IGAFEM_text.width + 0.4, height=IGAFEM_text.height + 0.3, fill_opacity=0.1, color=YELLOW).move_to(ORIGIN)  # Center box
        PP = RoundedRectangle(corner_radius=0.2, width=PP_text.width + 0.4, height=PP_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(IGAFEM, LEFT, buff=3)  # Left box
        PKPD = RoundedRectangle(corner_radius=0.2, width=PKPD_text.width + 0.4, height=PKPD_text.height + 0.3, fill_opacity=0.1, color=YELLOW).next_to(IGAFEM, RIGHT, buff=3)  # Right box
        Histology = RoundedRectangle(corner_radius=0.2, width=Histology_text.width + 0.4, height=Histology_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, UP, buff=0.5)
        Devices = RoundedRectangle(corner_radius=0.2, width=Devices_text.width + 0.4, height=Devices_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, DOWN*4.8, buff=0.5)

        # Move the text to the center of each box
        PP_text.move_to(PP.get_center())
        IGAFEM_text.move_to(IGAFEM.get_center())
        PKPD_text.move_to(PKPD.get_center())
        Histology_text.move_to(Histology.get_center())
        Devices_text.move_to(Devices.get_center())

        # Group the box and the text together
        PKPD_group = VGroup(PKPD, PKPD_text)

        self.next_slide()  # Adds interactivity


        self.play(ReplacementTransform(equations, PKPD_group))

        self.next_slide()  # Adds interactivity


        # Create arrows to connect the boxes
        arrow1 = Arrow(PP.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow2 = Arrow(IGAFEM.get_right(), PKPD.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_histology_to_igafem = Arrow(Histology.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_devices_to_igafem = Arrow(Devices.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts1 = ["BMI", "Flow rate", "Injection depth"]
        small_boxes1 = []
        small_box_group1 = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts1):
            box_text1 = Text(text, font_size=16)
            small_box1 = RoundedRectangle(corner_radius=0.2, width=box_text1.width + 0.4, height=box_text1.height + 0.3, fill_opacity=0.1)
            box_text1.move_to(small_box1.get_center())
            small_box_group1.add(VGroup(small_box1, box_text1))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group1.arrange(DOWN, buff=0.2).next_to(PP, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts = ["Fluid Flow","Solid deformations", "Drug Transport", "Stabilization: \nFPL+SUPG+DC"]
        small_boxes = []
        small_box_group = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts):
            box_text = Text(text, font_size=16)
            small_box = RoundedRectangle(corner_radius=0.2, width=box_text.width + 0.4, height=box_text.height + 0.3, fill_opacity=0.1)
            box_text.move_to(small_box.get_center())
            small_box_group.add(VGroup(small_box, box_text))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group.arrange(DOWN, buff=0.2).next_to(IGAFEM, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box = Arrow(IGAFEM.get_bottom(), small_box_group[0][0].get_top(), buff=0.1)

        # Add everything to the scene
        self.play(Create(Histology), Create(Histology_text))
        self.next_slide()  # Adds interactivity

        self.play(Create(PP), Create(PP_text))
        self.next_slide()  # Adds interactivity

        self.play(Create(arrow_to_first_box1))
        for small_box1 in small_box_group1:
            self.play(Create(small_box1))
        self.next_slide()  # Adds interactivity

        self.play(Create(Devices), Create(Devices_text))
        self.next_slide()  # Adds interactivity

        # Add small boxes and their text below IGAFEM
        self.play(Create(IGAFEM), Create(IGAFEM_text))
        self.next_slide()  # Adds interactivity

        self.play(Create(arrow1),Create(arrow_histology_to_igafem),Create(arrow_devices_to_igafem))
        self.next_slide()  # Adds interactivity

        # Add the arrow from IGAFEM to the first small box
        self.play(Create(arrow_to_first_box))
        self.next_slide()  # Adds interactivity

        # Add small boxes and their text below IGAFEM

        for small_box in small_box_group:
            self.play(Create(small_box))
        
        self.next_slide()  # Adds interactivity

        self.play(Create(arrow2))
        self.next_slide()  # Adds interactivity

        text_better = Text("More accurate predictions", font_size=16)
        small_box_PKPD = RoundedRectangle(corner_radius=0.2, width=text_better.width + 0.4, height=text_better.height + 0.3, fill_opacity=0.1, color=GREEN)

        # Group the text and the box together
        PKPD_group = VGroup(small_box_PKPD, text_better)

        # Position the text inside the box by aligning the group
        text_better.move_to(small_box_PKPD.get_center())

        # Position the box and text group below the PKPD box
        PKPD_group.next_to(PKPD, DOWN, buff=0.4)
        arrow_to_first_box3 = Arrow(PKPD.get_bottom(), PKPD_group[0][0].get_top(), buff=0.1)
        # Play the animation to create the box and text together
        self.play(Create(arrow_to_first_box3))
        self.play(Create(PKPD_group))

         # Create smaller axes for the graph (time in days and plasma concentration %)
        axis = Axes(
            x_range=[0, 10, 1], y_range=[0, 100, 20],
            x_length=5, y_length=3,  # Make the graph smaller
            axis_config={"include_ticks": False}  # Smaller arrow tips
        ).shift(DOWN * 2.3 + RIGHT * 4.6).scale(0.75)  # Shift the plot down and to the right

        # Add labels for the axes
        x_label = MathTex("t").move_to(axis.coords_to_point(10.6, 0))
        Cp_y_label = MathTex("C_p").set_color(RED).next_to(axis.y_axis, LEFT, buff=0.1)
        A1_y_label = MathTex("A_1").set_color(BLUE).next_to(Cp_y_label, DOWN, aligned_edge=LEFT)

        # Rotate the y-axis labels by 90 degrees
        Cp_y_label.rotate(90 * DEGREES)
        A1_y_label.rotate(90 * DEGREES)
        y_labels = VGroup(Cp_y_label, A1_y_label).arrange(DOWN, aligned_edge=LEFT).next_to(axis.y_axis, LEFT, buff=0.1)

        # Solve ODE for Plasma Concentration and Absorption Site
        k_a = 0.5  # absorption rate constant
        k_e = 0.1  # elimination rate constant
        V = 1.0    # volume of distribution
        A_abs_0 = 80  # initial amount of drug in absorption site
        C_0 = 0     # initial concentration in the central compartment
        time_vals = np.linspace(0, 9, 90)
        y0 = [A_abs_0, C_0]

        def pkpd_ode(t, y):
            A_abs, C = y
            dA_abs_dt = -k_a * A_abs
            dC_dt = (k_a * A_abs) / V - k_e * C
            return [dA_abs_dt, dC_dt]

        sol = solve_ivp(pkpd_ode, (0, 9), y0, t_eval=time_vals)
        absorption_vals = sol.y[0]  # Absorption site ODE result
        plasma_conc_vals_ode = sol.y[1]  # Plasma concentration ODE result

        # Plot the absorption site decay graph (ODE result)
        absorption_graph = axis.plot_line_graph(
            x_values=time_vals, y_values=absorption_vals, add_vertex_dots=False, line_color=BLUE
        )

        # Plot the plasma concentration solution (ODE result)
        plasma_graph_ode = axis.plot_line_graph(
            x_values=time_vals, y_values=plasma_conc_vals_ode, add_vertex_dots=False, line_color=RED
        )

        # Experimental points for absorption follow the blue line (absorption)
        exp_time_vals = np.array([1, 3, 5, 7, 9])  # Time points (days)
        exp_abs_vals = absorption_vals[[10, 30, 50, 70, 89]]  # Corresponding points on the blue line
        exp_plasma_vals = plasma_conc_vals_ode[[10, 30, 50, 70, 89]]  # Corresponding points on the red line

        # Create dots for experimental points
        exp_abs_dots = VGroup(*[Dot(axis.coords_to_point(t, a), color=BLUE) for t, a in zip(exp_time_vals, exp_abs_vals)])
        exp_plasma_dots = VGroup(*[Dot(axis.coords_to_point(t, p), color=RED) for t, p in zip(exp_time_vals, exp_plasma_vals)])

        # Show the plot, axes, labels, and graphs
        self.play(Create(axis), FadeIn(x_label, y_labels))
        self.play(Create(absorption_graph), Create(plasma_graph_ode))

        # Add experimental points with some delay for effect
        self.play(FadeIn(exp_abs_dots), FadeIn(exp_plasma_dots))
        self.next_slide()  # Adds interactivity


        self.play(FadeOut(Solution_top,arrow_to_first_box3,PKPD_group,arrow_to_first_box,arrow1,arrow_devices_to_igafem,arrow_histology_to_igafem,Devices,Devices_text,PP,PP_text,Histology,exp_abs_dots,absorption_graph,plasma_graph_ode,arrow2,axis,PKPD,y_labels,x_label,exp_plasma_dots,Histology_text,Histology_text,small_box_group1,PKPD_text,arrow_to_first_box1,small_box_group,IGAFEM,IGAFEM_text,heading))
        
        #IGA_FEM_group = VGroup(IGAFEM,IGAFEM_text)
        #Gov_eqns = Tex("Governing equations").move_to(2*UP)
        #self.play(ReplacementTransform(IGA_FEM_group, Gov_eqns))



class Mechanics(CustomSlide):
    def construct(self):
        # Add TOC to the scene at the beginning
        self.add(toc)

        # Move the first item in TOC to heading
        heading = toc[1].copy().move_to(ORIGIN).scale(1.25).to_corner(UP)

        # Instead of fading out all of TOC, first isolate toc[1]
        self.play(ReplacementTransform(toc[1], heading))

        # Now fade out the rest of TOC
        self.play(FadeOut(toc[0], toc[2:]))  # Fade out other items

        # Add interactivity for the slide
        self.next_slide()

        Solution_top = Tex("Data-Driven FEM for High-fidelity Simulation").move_to(2*UP)

        # Create the text for each box
        PP_text = Text("Physiological \nparameters", font_size=20)  # Text with smaller font size
        IGAFEM_text = Text("IGA based FEM", font_size=20)
        PKPD_text = Text("PK/PD Models", font_size=20)
        Histology_text = Text("Histology data", font_size=20)
        Devices_text = Text("Injection devices \nand techniques", font_size=20)


        # Create rounded rectangles with width and height based on the text bounding box
        IGAFEM = RoundedRectangle(corner_radius=0.2, width=IGAFEM_text.width + 0.4, height=IGAFEM_text.height + 0.3, fill_opacity=0.1, color=YELLOW).move_to(ORIGIN)  # Center box
        PP = RoundedRectangle(corner_radius=0.2, width=PP_text.width + 0.4, height=PP_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(IGAFEM, LEFT, buff=3)  # Left box
        PKPD = RoundedRectangle(corner_radius=0.2, width=PKPD_text.width + 0.4, height=PKPD_text.height + 0.3, fill_opacity=0.1, color=YELLOW).next_to(IGAFEM, RIGHT, buff=3)  # Right box
        Histology = RoundedRectangle(corner_radius=0.2, width=Histology_text.width + 0.4, height=Histology_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, UP, buff=0.5)
        Devices = RoundedRectangle(corner_radius=0.2, width=Devices_text.width + 0.4, height=Devices_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, DOWN*4.8, buff=0.5)

        # Move the text to the center of each box
        PP_text.move_to(PP.get_center())
        IGAFEM_text.move_to(IGAFEM.get_center())
        PKPD_text.move_to(PKPD.get_center())
        Histology_text.move_to(Histology.get_center())
        Devices_text.move_to(Devices.get_center())

        # Group the box and the text together
        PKPD_group = VGroup(PKPD, PKPD_text)

        # Create arrows to connect the boxes
        arrow1 = Arrow(PP.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow2 = Arrow(IGAFEM.get_right(), PKPD.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_histology_to_igafem = Arrow(Histology.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_devices_to_igafem = Arrow(Devices.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts1 = ["BMI", "Flow rate", "Injection depth"]
        small_boxes1 = []
        small_box_group1 = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts1):
            box_text1 = Text(text, font_size=16)
            small_box1 = RoundedRectangle(corner_radius=0.2, width=box_text1.width + 0.4, height=box_text1.height + 0.3, fill_opacity=0.1)
            box_text1.move_to(small_box1.get_center())
            small_box_group1.add(VGroup(small_box1, box_text1))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group1.arrange(DOWN, buff=0.2).next_to(PP, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts = ["Fluid Flow","Solid deformations", "Drug Transport", "Stabilization: \nFPL+SUPG+DC"]
        small_boxes = []
        small_box_group = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts):
            box_text = Text(text, font_size=16)
            small_box = RoundedRectangle(corner_radius=0.2, width=box_text.width + 0.4, height=box_text.height + 0.3, fill_opacity=0.1)
            box_text.move_to(small_box.get_center())
            small_box_group.add(VGroup(small_box, box_text))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group.arrange(DOWN, buff=0.2).next_to(IGAFEM, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box = Arrow(IGAFEM.get_bottom(), small_box_group[0][0].get_top(), buff=0.1)

        text_better = Text("More accurate predictions", font_size=16)
        small_box_PKPD = RoundedRectangle(corner_radius=0.2, width=text_better.width + 0.4, height=text_better.height + 0.3, fill_opacity=0.1, color=GREEN)

        # Group the text and the box together
        PKPD_group = VGroup(small_box_PKPD, text_better)

        # Position the text inside the box by aligning the group
        text_better.move_to(small_box_PKPD.get_center())

        # Position the box and text group below the PKPD box
        PKPD_group.next_to(PKPD, DOWN, buff=0.4)
        arrow_to_first_box3 = Arrow(PKPD.get_bottom(), PKPD_group[0][0].get_top(), buff=0.1)
        # Play the animation to create the box and text together

        # Create a fade-in group for all elements
        fade_in_group = VGroup(
            Solution_top, PP, PP_text, IGAFEM, IGAFEM_text, PKPD, PKPD_text, 
            Histology, Histology_text, Devices, Devices_text, 
            arrow1, arrow2, arrow_histology_to_igafem, arrow_devices_to_igafem,
            small_box_group1, small_box_group
        )

        fade_out_group = VGroup(
            Solution_top, PP, PP_text, PKPD, PKPD_text, 
            Histology, Histology_text, Devices, Devices_text, 
            arrow1, arrow2, arrow_histology_to_igafem, arrow_devices_to_igafem,
            small_box_group1,small_box_group[3]
        )

        # Fade in all elements at once
        self.play(FadeIn(fade_in_group))
        self.next_slide()  # Adds interactivity
        self.play(FadeOut(fade_out_group))
        self.next_slide()  # Adds interactivity

        IGA_FEM_group = VGroup(IGAFEM,IGAFEM_text)
        Gov_eqns = Tex("Governing equations").move_to(2*UP)
        self.play(ReplacementTransform(IGA_FEM_group, Gov_eqns))

        #Gov_eqns = Tex("Governing equations").move_to(2*UP)
        #self.play(Write(Gov_eqns))

        # Define the first equation using LaTeX
        equation1  = MathTex("\\alpha","\\frac{\partial \epsilon_v}{\partial t}","+","\\frac{1}{M}","\\frac{\partial p}{\partial t}","=","\\nabla \cdot \\left (\mathbf{K}\\nabla p \\right)","+","q","-","J_l", "+", "J_b")
        # Define the second equation
        equation2 = MathTex("\\nabla\\cdot\mathbf{\\sigma}", "=", "\\alpha \\nabla p")
        equation3 = MathTex("\\frac{\partial \\left(c \phi\\right)}{\partial t}","+","\\nabla \cdot \\left(D \phi \\nabla c + \mathbf{K} \\nabla p c \\right)","=","q","-","J_l c", "+", "J_b c")
        # Position the equations on the scene
        equation1.move_to(0.7*UP).scale(0.7)
        equation2.next_to(equation1, DOWN*2.6, buff=0.3).scale(0.7)
        equation3.next_to(equation2, DOWN*2.5, buff=0.3).scale(0.7)

        # Highlight specific terms in yellow
        epsilon_v_term = equation1[1]  # Highlight \epsilon_v (adjust range if necessary)
        p_term_1 = equation1[4] # Highlight p in the second term
        k_term = equation1[6][3]  # Highlight p in the fourth term (inside the gradient)
        alpha_term = equation1[0][0] # Highlight alpha in the second term
        M_term = equation1[3][2] # Highlight alpha in the second term
        q_term = equation1[8]  # Highlight q
        J_l_term = equation1[10]  # Highlight J_l
        J_b_term = equation1[12]  # Highlight J_b
        sigma_term = equation2[0][2]  # Highlight J_b
        c_term = equation3[0][2]  # Highlight J_b
        phi_term = equation3[0][3]  # Highlight J_b
        D_term = equation3[2][3]  # Highlight J_b

        # Set target positions aligned with the equations but to the left
        target_position_1 = equation1.get_center() + LEFT * 5.5  # Aligned with equation1
        target_position_2 = equation2.get_center() + LEFT * 5.5  # Aligned with equation2
        target_position_3 = equation3.get_center() + LEFT * 5.5  # Aligned with equation3

        # Move the first box to its target position
        self.play(small_box_group[0].animate.move_to(target_position_1))
        #self.next_slide()  # Adds interactivity

        # Move the second box to its target position
        self.play(small_box_group[1].animate.move_to(target_position_2))
        #self.next_slide()  # Adds interactivity

        # Move the third box to its target position
        self.play(small_box_group[2].animate.move_to(target_position_3))
        self.next_slide()  # Adds interactivity


        # Play animations to write the equations one by one
        self.play(Write(equation1))  # Write the first equation
        self.next_slide()  # Adds interactivity

        # Highlight each term one by one
        self.play(epsilon_v_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(epsilon_v_term.animate.set_color(WHITE).scale(1/1.2))  # Reset to white
        self.next_slide()  # Adds interactivity

        self.play(p_term_1.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(p_term_1.animate.set_color(WHITE).scale(1/1.2))
        self.next_slide()  # Adds interactivity


        self.play(
        alpha_term.animate.set_color(YELLOW).scale(1.2),
        M_term.animate.set_color(YELLOW).scale(1.2)
        )

        self.next_slide()  # Adds interactivity


        self.play(
        alpha_term.animate.set_color(WHITE).scale(1/1.2),  # Reset to original size and color
        M_term.animate.set_color(WHITE).scale(1/1.2)
        )

        self.next_slide()  # Adds interactivity


        self.play(k_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(k_term.animate.set_color(WHITE).scale(1/1.2))
        self.next_slide()  # Adds interactivity

        self.play(q_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(q_term.animate.set_color(WHITE).scale(1/1.2))
        self.next_slide()  # Adds interactivity

        self.play(J_l_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(J_l_term.animate.set_color(WHITE).scale(1/1.2))
        self.next_slide()  # Adds interactivity

        self.play(J_b_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(J_b_term.animate.set_color(WHITE).scale(1/1.2))
        self.next_slide()  # Adds interactivity




        self.play(Write(equation2))  # Write the first equation
        self.next_slide()  # Adds interactivity
        self.play(sigma_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(sigma_term.animate.set_color(WHITE).scale(1/1.2))
        self.next_slide()  # Adds interactivity


        self.play(Write(equation3))  # Write the first equation
        self.next_slide()  # Adds interactivity

        
        self.play(c_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(c_term.animate.set_color(WHITE).scale(1/1.2))
        self.next_slide()  # Adds interactivity

        self.play(phi_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(phi_term.animate.set_color(WHITE).scale(1/1.2))
        self.next_slide()  # Adds interactivity

        self.play(D_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(D_term.animate.set_color(WHITE).scale(1/1.2))
        self.next_slide()  # Adds interactivity

        # Define the first text box: "Large-deformations"
        text1 = Text("Large-deformations", font_size=18)
        box1 = RoundedRectangle(corner_radius=0.2, width=text1.width + 0.4, height=text1.height + 0.3, fill_opacity=0.1)
        text1.move_to(box1.get_center())
        text1_box = VGroup(box1, text1)

        # Position the first box to the right of the equation (adjust as needed)
        text1_box.move_to(RIGHT * 5 + UP * 0.5)

        # Define the second text box: "Pull back operation"
        text2 = Text("Pull-back operation", font_size=18)
        box2 = RoundedRectangle(corner_radius=0.2, width=text2.width + 0.4, height=text2.height + 0.3, fill_opacity=0.1)
        text2.move_to(box2.get_center())
        text2_box = VGroup(box2, text2)

        # Position the second box directly below the first one
        text2_box.next_to(text1_box, DOWN, buff=1.0)

        # Create an arrow pointing from the first box to the second
        arrow = Arrow(start=text1_box.get_bottom(), end=text2_box.get_top(), buff=0.2)

        # Add the elements to the scene
        self.play(FadeIn(text1_box))
        self.play(GrowArrow(arrow))
        self.play(FadeIn(text2_box))

        self.next_slide()  # Adds interactivity


        # Define the first equation using LaTeX
        equation4  = MathTex("\\frac{\\alpha}{J}","\\frac{\mathrm{D} J}{\mathrm{D} t}","+","\\frac{1}{M}","\\frac{\mathrm{D} p}{\mathrm{D} t}","=","\\nabla^X \cdot \\left (J\mathbf{F}^{-1}\mathbf{K}\mathbf{F}^{-T}\\nabla^X p \\right)","+","Q","-","J_l", "+", "J_b")
        # Define the second equation
        equation5 = MathTex("\\nabla^X \\cdot\mathbf{P}", "=", "\\nabla^X\\cdot \\left(\\alpha p J \mathbf{F}^{-T}\\right)")
        equation6 = MathTex("\\frac{\mathrm{D} \\left(C \Phi\\right)}{\mathrm{D} t}","+","\\nabla^X \cdot \\left(\Phi J \mathbf{F}^{-1}\mathbf{D}\mathbf{F}^{-T}\\nabla^X C + J\mathbf{F}^{-1}\mathbf{K}\mathbf{F}^{-T}\\nabla^X p C\\right)","=","Q","-","J_l C", "+", "J_b C")

        equation4.move_to(0.7*UP).scale(0.5)
        equation5.next_to(equation1, DOWN*2.6, buff=0.3).scale(0.7)
        equation6.next_to(equation2, DOWN*2.5, buff=0.3).scale(0.5)

        self.play(ReplacementTransform(equation1, equation4))
        self.next_slide()  # Adds interactivity
        self.play(ReplacementTransform(equation2, equation5))
        self.next_slide()  # Adds interactivity
        self.play(ReplacementTransform(equation3, equation6))
        self.next_slide()  # Adds interactivity

         # Highlight specific terms in yellow
        F_term = equation4[6][5]  # Highlight \epsilon_v (adjust range if necessary)
        J_term = equation4[6][4]  # Highlight \epsilon_v (adjust range if necessary)

        # Highlight each term one by one
        self.play(F_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(F_term.animate.set_color(WHITE).scale(1/1.2))  # Reset to white
        self.next_slide()  # Adds interactivity
        self.play(J_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity
        self.play(J_term.animate.set_color(WHITE).scale(1/1.2))  # Reset to white
        self.next_slide()  # Adds interactivity


        #self.play(FadeOut(equation4, equation6,text1_box,text2_box,small_box_group[0],small_box_group[1],small_box_group[2],arrow))
        self.play(FadeOut(equation4, equation6,text1_box,text2_box,arrow,small_box_group[0],small_box_group[1],small_box_group[2]))

        target_position_5 = equation5.get_center() + UP * 2.0 
        self.play(equation5.animate.move_to(target_position_5))
        self.next_slide()  # Adds interactivity

        equation7  = MathTex("\mathbf{S}","=","\mathbf{F}^{-1} \mathbf{P}")
        equation8  = MathTex("\mathbf{S}","=","\mathbf{S}_{\\text{iso}}","+","\mathbf{S}_{\\text{vol}}","+","\mathbf{S}_{\\text{aniso}}")
        equation9  = MathTex("\mathbf{S}_{\\text{iso}}","=","\\mu J^{-2/3}\\left(\mathbf{I}-\\frac{1}{3}\\text{tr}\\left(\mathbf{C}\\right)\mathbf{C}^{-1}\\right)")
        equation10 = MathTex("\mathbf{S}_{\\text{vol}}","=","\\frac{K}{2}\\left(J^2-1\\right)\mathbf{C}^{-1}")
        equation11 = MathTex("\mathbf{S}_{\\text{aniso}}","=","\sum_{i=1,2}2 k_1 E_i \exp \\left(k_2 E_i^2\\right)\\left[\\kappa \mathbf{I}+\\left(1-3\\kappa\\right)\\left(a_{0i}\\times a_{0i}\\right)\\right]")

        equation7.next_to(equation5, DOWN*0.7, buff=0.3).scale(0.7).shift(LEFT * 2.3)
        equation8.next_to(equation7, DOWN*0.7, buff=0.3).scale(0.7)
        equation9.next_to(equation8, DOWN*0.7, buff=0.3).scale(0.7).set_color(RED)
        equation10.next_to(equation9, DOWN*0.7, buff=0.3).scale(0.7).set_color(RED)
        equation11.next_to(equation10, DOWN*0.7, buff=0.3).scale(0.6).set_color(GREEN)

        # Play animations to write the equations one by one
        self.play(Write(equation7))  # Write the first equation
        self.next_slide()  # Adds interactivity
        self.play(Write(equation8))  # Write the first equation
        self.next_slide()  # Adds interactivity

        Siso_term = equation8[2]  # Highlight \epsilon_v (adjust range if necessary)
        Svol_term = equation8[4]  # Highlight \epsilon_v (adjust range if necessary)
        Saniso_term = equation8[6]  # Highlight \epsilon_v (adjust range if necessary)

        frame_dir = "./"  # Directory containing your PNG files
        frame_file = "fibers1.png"  # Replace with the name of your PNG file
        frame_path = os.path.join(frame_dir, frame_file)

        # Load the single PNG image
        fibers1 = ImageMobject(frame_path).scale(0.7).shift(ORIGIN).shift(1.5*DOWN+4.0*RIGHT)
        # Add the PNG image to the slide
        self.play(FadeIn(fibers1))
        self.next_slide()  # Adds interactivity

        self.play(
        Siso_term.animate.set_color(RED),
        Svol_term.animate.set_color(RED))
        self.play(Write(equation9))  # Write the first equation
        self.next_slide()  # Adds interactivity
        self.play(Write(equation10))  # Write the first equation
        self.next_slide()  # Adds interactivity
        #self.play(Svol_term.animate.set_color(RED))
        #self.next_slide()  # Adds interactivity

        frame_dir = "./"  # Directory containing your PNG files
        frame_file = "fibers2.png"  # Replace with the name of your PNG file
        frame_path = os.path.join(frame_dir, frame_file)

        # Load the single PNG image
        fibers2 = ImageMobject(frame_path).scale(0.7).shift(ORIGIN).shift(1.5*DOWN+4.0*RIGHT)
        # Add the PNG image to the slide
        self.play(FadeIn(fibers2))   
        self.next_slide()  # Adds interactivity

        self.play(Saniso_term.animate.set_color(GREEN))
        self.play(Write(equation11))  # Write the first equation
        self.next_slide()  # Adds interactivity

        # Highlight specific terms in yellow
        C_term = equation9[2][15]  # Highlight \epsilon_v (adjust range if necessary)
        mu_term = equation9[2][0]  # Highlight \epsilon_v (adjust range if necessary)
        K_term = equation10[2][0]  # Highlight \epsilon_v (adjust range if necessary)
        k1_term = equation11[2][7:9]  # Highlight \epsilon_v (adjust range if necessary)
        k2_term = equation11[2][15:17]  # Highlight \epsilon_v (adjust range if necessary)
        kappa_term = equation11[2][22]  # Highlight \epsilon_v (adjust range if necessary)
        a0i_term = equation11[2][32:39]  # Highlight \epsilon_v (adjust range if necessary)


        # Highlight each term one by one
        self.play(C_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(C_term.animate.set_color(RED).scale(1/1.2))  # Reset to white
        self.next_slide()  # Adds interactivity
        self.play(
        mu_term.animate.set_color(YELLOW).scale(1.2),
        K_term.animate.set_color(YELLOW).scale(1.2),
        k1_term.animate.set_color(YELLOW).scale(1.2),
        k2_term.animate.set_color(YELLOW).scale(1.2),
        kappa_term.animate.set_color(YELLOW).scale(1.2),
        )
        self.next_slide()  # Adds interactivity

        self.play(
        mu_term.animate.set_color(RED).scale(1/1.2),  # Reset to original size and color
        K_term.animate.set_color(RED).scale(1/1.2),
        k1_term.animate.set_color(GREEN).scale(1/1.2),
        k2_term.animate.set_color(GREEN).scale(1/1.2),
        kappa_term.animate.set_color(GREEN).scale(1/1.2),
        )
        self.next_slide()  # Adds interactivity

        self.play(a0i_term.animate.set_color(YELLOW).scale(1.2))
        self.next_slide()  # Adds interactivity

        self.play(a0i_term.animate.set_color(GREEN).scale(1/1.2))  # Reset to white
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(fibers1,fibers2,equation7,equation8,equation9,equation10,equation11,Gov_eqns,equation5))


        Solution_top = Tex("Data-Driven FEM for High-fidelity Simulation").move_to(2*UP)

        # Create the text for each box
        PP_text = Text("Physiological \nparameters", font_size=20)  # Text with smaller font size
        IGAFEM_text = Text("IGA based FEM", font_size=20)
        PKPD_text = Text("PK/PD Models", font_size=20)
        Histology_text = Text("Histology data", font_size=20)
        Devices_text = Text("Injection devices \nand techniques", font_size=20)


        # Create rounded rectangles with width and height based on the text bounding box
        IGAFEM = RoundedRectangle(corner_radius=0.2, width=IGAFEM_text.width + 0.4, height=IGAFEM_text.height + 0.3, fill_opacity=0.1, color=YELLOW).move_to(ORIGIN)  # Center box
        PP = RoundedRectangle(corner_radius=0.2, width=PP_text.width + 0.4, height=PP_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(IGAFEM, LEFT, buff=3)  # Left box
        PKPD = RoundedRectangle(corner_radius=0.2, width=PKPD_text.width + 0.4, height=PKPD_text.height + 0.3, fill_opacity=0.1, color=YELLOW).next_to(IGAFEM, RIGHT, buff=3)  # Right box
        Histology = RoundedRectangle(corner_radius=0.2, width=Histology_text.width + 0.4, height=Histology_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, UP, buff=0.5)
        Devices = RoundedRectangle(corner_radius=0.2, width=Devices_text.width + 0.4, height=Devices_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, DOWN*4.8, buff=0.5)

        # Move the text to the center of each box
        PP_text.move_to(PP.get_center())
        IGAFEM_text.move_to(IGAFEM.get_center())
        PKPD_text.move_to(PKPD.get_center())
        Histology_text.move_to(Histology.get_center())
        Devices_text.move_to(Devices.get_center())

        # Group the box and the text together
        PKPD_group = VGroup(PKPD, PKPD_text)

        # Create arrows to connect the boxes
        arrow1 = Arrow(PP.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow2 = Arrow(IGAFEM.get_right(), PKPD.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_histology_to_igafem = Arrow(Histology.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_devices_to_igafem = Arrow(Devices.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts1 = ["BMI", "Flow rate", "Injection depth"]
        small_boxes1 = []
        small_box_group1 = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts1):
            box_text1 = Text(text, font_size=16)
            small_box1 = RoundedRectangle(corner_radius=0.2, width=box_text1.width + 0.4, height=box_text1.height + 0.3, fill_opacity=0.1)
            box_text1.move_to(small_box1.get_center())
            small_box_group1.add(VGroup(small_box1, box_text1))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group1.arrange(DOWN, buff=0.2).next_to(PP, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts = ["Fluid Flow","Solid deformations", "Drug Transport", "Stabilization: \nFPL+SUPG+DC"]
        small_boxes = []
        small_box_group = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts):
            box_text = Text(text, font_size=16)
            small_box = RoundedRectangle(corner_radius=0.2, width=box_text.width + 0.4, height=box_text.height + 0.3, fill_opacity=0.1)
            box_text.move_to(small_box.get_center())
            small_box_group.add(VGroup(small_box, box_text))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group.arrange(DOWN, buff=0.2).next_to(IGAFEM, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box = Arrow(IGAFEM.get_bottom(), small_box_group[0][0].get_top(), buff=0.1)

        text_better = Text("More accurate predictions", font_size=16)
        small_box_PKPD = RoundedRectangle(corner_radius=0.2, width=text_better.width + 0.4, height=text_better.height + 0.3, fill_opacity=0.1, color=GREEN)

        # Group the text and the box together
        PKPD_group = VGroup(small_box_PKPD, text_better)

        # Position the text inside the box by aligning the group
        text_better.move_to(small_box_PKPD.get_center())

        # Position the box and text group below the PKPD box
        PKPD_group.next_to(PKPD, DOWN, buff=0.4)
        arrow_to_first_box3 = Arrow(PKPD.get_bottom(), PKPD_group[0][0].get_top(), buff=0.1)
        # Play the animation to create the box and text together

        # Create a fade-in group for all elements
        fade_in_group = VGroup(
            Solution_top, PP, PP_text, IGAFEM, IGAFEM_text, PKPD, PKPD_text, 
            Histology, Histology_text, Devices, Devices_text, 
            arrow1, arrow2, arrow_histology_to_igafem, arrow_devices_to_igafem,
            small_box_group1, small_box_group
        )

        fade_out_group = VGroup(
            Solution_top, PP, PP_text, PKPD, PKPD_text, Devices, Devices_text, 
            arrow1, arrow2, arrow_histology_to_igafem, arrow_devices_to_igafem,
            small_box_group1,small_box_group,IGAFEM, IGAFEM_text
        )

        # Fade in all elements at once
        self.play(FadeIn(fade_in_group))
        self.next_slide()  # Adds interactivity
        self.play(FadeOut(fade_out_group))
        self.next_slide()  # Adds interactivity


        Histology_group = VGroup(Histology,Histology_text)
        Histology_title = Tex("Histology").move_to(2.5*UP)
        self.play(ReplacementTransform(Histology_group, Histology_title))
        self.next_slide()  # Adds interactivity

        frame_dir = "./"  # Directory containing your PNG files
        frame_file = "histo1.png"  # Replace with the name of your PNG file
        frame_path = os.path.join(frame_dir, frame_file)

        # Load the single PNG image
        histo1 = ImageMobject(frame_path).scale(1.0).shift(ORIGIN+DOWN*0.4)
        # Add the PNG image to the slide
        self.play(FadeIn(histo1))
        self.next_slide()  # Adds interactivity

        # Remove the frame after the wait
        #self.remove(frame)

        frame_dir = "./"  # Directory containing your PNG files
        frame_file = "histo2.png"  # Replace with the name of your PNG file
        frame_path = os.path.join(frame_dir, frame_file)

        # Load the single PNG image
        histo2 = ImageMobject(frame_path).scale(1.0).shift(ORIGIN+DOWN*0.4)
        # Add the PNG image to the slide
        self.play(FadeIn(histo2))   
        self.next_slide()  # Adds interactivity

        frame_dir = "./"  # Directory containing your PNG files
        frame_file = "histo3.png"  # Replace with the name of your PNG file
        frame_path = os.path.join(frame_dir, frame_file)

        # Load the single PNG image
        histo3 = ImageMobject(frame_path).scale(1.0).shift(ORIGIN+DOWN*0.4)
        # Add the PNG image to the slide
        self.play(FadeIn(histo3))   
        self.next_slide()  # Adds interactivity

        frame_dir = "./"  # Directory containing your PNG files
        frame_file = "histo4.png"  # Replace with the name of your PNG file
        frame_path = os.path.join(frame_dir, frame_file)

        # Load the single PNG image
        histo4 = ImageMobject(frame_path).scale(1.0).shift(ORIGIN+DOWN*0.4)
        # Add the PNG image to the slide
        self.play(FadeIn(histo4))
        self.next_slide()  # Adds interactivity  

        frame_dir = "./"  # Directory containing your PNG files
        frame_file = "histo5.png"  # Replace with the name of your PNG file
        frame_path = os.path.join(frame_dir, frame_file)

        # Load the single PNG image
        histo5 = ImageMobject(frame_path).scale(1.0).shift(ORIGIN+DOWN*0.4)
        # Add the PNG image to the slide
        self.play(FadeIn(histo5))
        self.next_slide()  # Adds interactivity  

        self.play(FadeOut(Histology_title,histo1,histo2,histo3,histo4,histo5))
        self.next_slide()  # Adds interactivity


        NM_title = Tex("Numerical Methods").move_to(2.5*UP)
        self.play(Write(NM_title))
        self.next_slide()  # Adds interactivity

        # List of points, separating text and math
        bullet1 = Tex("Spatial discretization: Isogeometric Analysis (IGA)").next_to(NM_title, DOWN, buff=0.5)
        bullet2 = BulletedList("$\\mathcal{C}^2$-continuous cubic splines for $p$, $\\mathbf{u}$, $C$", "Helps reduce $inf-sup$ instabilities").set_color(GREEN).next_to(bullet1, DOWN, buff=0.5)

        # Add splines image below Spatial_disc2
        splines = ImageMobject("splines.png").scale(1.6).next_to(bullet2, DOWN, buff=0.5)

        # Add explanation about inf-sup instabilities below splines

        # Animations
        self.play(Write(bullet1))
        self.next_slide()  # Adds interactivity
        self.play(Write(bullet2))
        #self.next_slide()  # Adds interactivity
        self.play(FadeIn(splines))  # Display the PNG image
        self.next_slide()  # Adds interactivity
        Spatial_disc4 = Tex("$\\rightarrow$ Advection-dominated problem").set_color(RED).next_to(splines, DOWN, buff=0.5)
        self.play(Write(Spatial_disc4))
        #self.next_slide()  # Adds interactivity


        self.play(FadeOut(bullet1,bullet2,splines))
        self.next_slide()  # Adds interactivity

        bullet3 = Tex("$\\rightarrow$ Stabilization techniques:").next_to(NM_title, DOWN, buff=0.5)
        bullet4 = BulletedList("Fluid-Pressure-Laplacian (FPL) for mass balance of mixture", "SUPG for advection-diffusion equation", "Discontinuity Capturing (DC) for advection-diffusion equation").set_color(GREEN).next_to(bullet3, DOWN, buff=0.5)

        self.play(ReplacementTransform(Spatial_disc4,bullet3))
        self.play(Write(bullet4))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(bullet3,bullet4))
        self.next_slide()  # Adds interactivity


        # List of points, separating text and math
        bullet5 = Tex("$\\rightarrow$ Time integration: Generalized $\\alpha$-method").next_to(NM_title, DOWN, buff=0.5)
        bullet6 = BulletedList("Second-order accurate, unconditionally stable", "$\\rho_{\\infty} = 1/2$ for high frequency dissipation").set_color(GREEN).next_to(bullet3, DOWN, buff=0.5)

        self.play(Write(bullet5))
        self.next_slide()  # Adds interactivity
        self.play(Write(bullet6))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(bullet5,bullet6))
        self.next_slide()  # Adds interactivity

        # List of points, separating text and math
        bullet7 = Tex("$\\rightarrow$ Solvers:").next_to(NM_title, DOWN, buff=0.5)
        bullet8 = BulletedList("Newton-Raphson for nonlinear systems", "GMRES with diagonal preconditioner for linear systems").set_color(GREEN).next_to(bullet3, DOWN, buff=0.5)

        self.play(Write(bullet7))
        self.next_slide()  # Adds interactivity
        self.play(Write(bullet8))
        self.next_slide()  # Adds interactivity

        Implementation=Tex("$\\rightarrow$ Implementation:").next_to(bullet8, DOWN, buff=0.5)

        # Add splines image below Spatial_disc2
        solvers = ImageMobject("solvers.png").scale(1.4).next_to(Implementation, DOWN, buff=0.5)

        self.play(Write(Implementation))
        self.next_slide()  # Adds interactivity
        self.play(FadeIn(solvers))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(solvers,Implementation,bullet7,bullet8,NM_title))


        Solution_top = Tex("Data-Driven FEM for High-fidelity Simulation").move_to(2*UP)

        # Create the text for each box
        PP_text = Text("Physiological \nparameters", font_size=20)  # Text with smaller font size
        IGAFEM_text = Text("IGA based FEM", font_size=20)
        PKPD_text = Text("PK/PD Models", font_size=20)
        Histology_text = Text("Histology data", font_size=20)
        Devices_text = Text("Injection devices \nand techniques", font_size=20)


        # Create rounded rectangles with width and height based on the text bounding box
        IGAFEM = RoundedRectangle(corner_radius=0.2, width=IGAFEM_text.width + 0.4, height=IGAFEM_text.height + 0.3, fill_opacity=0.1, color=YELLOW).move_to(ORIGIN)  # Center box
        PP = RoundedRectangle(corner_radius=0.2, width=PP_text.width + 0.4, height=PP_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(IGAFEM, LEFT, buff=3)  # Left box
        PKPD = RoundedRectangle(corner_radius=0.2, width=PKPD_text.width + 0.4, height=PKPD_text.height + 0.3, fill_opacity=0.1, color=YELLOW).next_to(IGAFEM, RIGHT, buff=3)  # Right box
        Histology = RoundedRectangle(corner_radius=0.2, width=Histology_text.width + 0.4, height=Histology_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, UP, buff=0.5)
        Devices = RoundedRectangle(corner_radius=0.2, width=Devices_text.width + 0.4, height=Devices_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, DOWN*4.8, buff=0.5)

        # Move the text to the center of each box
        PP_text.move_to(PP.get_center())
        IGAFEM_text.move_to(IGAFEM.get_center())
        PKPD_text.move_to(PKPD.get_center())
        Histology_text.move_to(Histology.get_center())
        Devices_text.move_to(Devices.get_center())

        # Group the box and the text together
        PKPD_group = VGroup(PKPD, PKPD_text)

        # Create arrows to connect the boxes
        arrow1 = Arrow(PP.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow2 = Arrow(IGAFEM.get_right(), PKPD.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_histology_to_igafem = Arrow(Histology.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_devices_to_igafem = Arrow(Devices.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts1 = ["BMI", "Flow rate", "Injection depth"]
        small_boxes1 = []
        small_box_group1 = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts1):
            box_text1 = Text(text, font_size=16)
            small_box1 = RoundedRectangle(corner_radius=0.2, width=box_text1.width + 0.4, height=box_text1.height + 0.3, fill_opacity=0.1)
            box_text1.move_to(small_box1.get_center())
            small_box_group1.add(VGroup(small_box1, box_text1))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group1.arrange(DOWN, buff=0.2).next_to(PP, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts = ["Fluid Flow","Solid deformations", "Drug Transport", "Stabilization: \nFPL+SUPG+DC"]
        small_boxes = []
        small_box_group = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts):
            box_text = Text(text, font_size=16)
            small_box = RoundedRectangle(corner_radius=0.2, width=box_text.width + 0.4, height=box_text.height + 0.3, fill_opacity=0.1)
            box_text.move_to(small_box.get_center())
            small_box_group.add(VGroup(small_box, box_text))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group.arrange(DOWN, buff=0.2).next_to(IGAFEM, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box = Arrow(IGAFEM.get_bottom(), small_box_group[0][0].get_top(), buff=0.1)

        text_better = Text("More accurate predictions", font_size=16)
        small_box_PKPD = RoundedRectangle(corner_radius=0.2, width=text_better.width + 0.4, height=text_better.height + 0.3, fill_opacity=0.1, color=GREEN)

        # Group the text and the box together
        PKPD_group = VGroup(small_box_PKPD, text_better)

        # Position the text inside the box by aligning the group
        text_better.move_to(small_box_PKPD.get_center())

        # Position the box and text group below the PKPD box
        PKPD_group.next_to(PKPD, DOWN, buff=0.4)
        arrow_to_first_box3 = Arrow(PKPD.get_bottom(), PKPD_group[0][0].get_top(), buff=0.1)
        # Play the animation to create the box and text together

        # Create a fade-in group for all elements
        fade_in_group = VGroup(
            Solution_top, PP, PP_text, IGAFEM, IGAFEM_text, PKPD, PKPD_text, 
            Histology, Histology_text, Devices, Devices_text, 
            arrow1, arrow2, arrow_histology_to_igafem, arrow_devices_to_igafem,
            small_box_group1, small_box_group
        )

        fade_out_group = VGroup(
            Solution_top, PP, PP_text, PKPD, PKPD_text, 
            arrow1, arrow2, arrow_histology_to_igafem, arrow_devices_to_igafem,
            small_box_group1,small_box_group,IGAFEM, IGAFEM_text,Histology,Histology_text
        )

        # Fade in all elements at once
        self.play(FadeIn(fade_in_group))
        self.next_slide()  # Adds interactivity
        self.play(FadeOut(fade_out_group))
        self.next_slide()  # Adds interactivity


        Devices_group = VGroup(Devices_text,Devices)
        Devices_title = Tex("Injection devices and techniques").move_to(2.5*UP)
        self.play(ReplacementTransform(Devices_group, Devices_title))
        self.next_slide()  # Adds interactivity


        # Add splines image below Spatial_disc2
        devices = ImageMobject("devices.png").scale(0.55).move_to(ORIGIN+LEFT*3.5+DOWN*0.55)
        techniques = ImageMobject("techniques.png").scale(0.47).next_to(devices, RIGHT, buff=0.5)
        self.play(FadeIn(devices))
        self.next_slide()  # Adds interactivity
        self.play(FadeIn(techniques))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(devices,techniques,Devices_title))

        Results_title1 = Tex("Results with an auto-injector base plate").move_to(2.5*UP)
        self.play(Write(Results_title1))
        self.next_slide()  # Adds interactivity


        pressure_scale = ImageMobject("pressure_scale.png").scale(0.55).move_to(ORIGIN+DOWN+RIGHT*5.8)
        AI1 = ImageMobject("AI1.png").scale(0.55).move_to(ORIGIN+DOWN+LEFT*5.5)

        self.play(FadeIn(AI1))
        self.next_slide()  # Moves to the next slide when ready

        self.play(FadeIn(pressure_scale))
        #self.next_slide()  # Moves to the next slide when ready

        # Include the video frames in the bottom right corner
        frame_dir = "./Pressure_wavy"
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])

        replay_count_pressure = 3  # Define how many times the GIF will replay

        for _ in range(replay_count_pressure):  # Loop to replay the GIF a specific number of times
            for frame_file in frame_files:
                frame_path = os.path.join(frame_dir, frame_file)
                frame = ImageMobject(frame_path)
                frame.scale(0.4)  # Scale the frame
                frame.to_corner(ORIGIN+DOWN)  # Position it in the bottom right corner
                self.add(frame)
                self.wait(1 / 30)  # Adjust this to control the display duration of each frame
                self.remove(frame)

        self.next_slide()  # Moves to the next slide when ready
        self.play(FadeOut(pressure_scale))
        self.next_slide()  # Adds interactivity


        # Define equations
        equation14  = MathTex(
            "\mathbf{\\sigma}_{\\text{isotropic}}","=",
            "\\mu J^{-5/3}\\left(\\mathbf{B}-\\frac{1}{3}\\text{tr}\\left(\\mathbf{C}\\right)\mathbf{I}\\right)", 
            "+", "\\frac{K}{2J}\\left(J^2-1\\right)\\mathbf{I}"
        )
        equation15 = MathTex(
            "\mathbf{\\sigma}_{\\text{aniso}}","=",
            "\sum_{i=1,2}2 k_1 \\left(I^*_{4i}-1\\right) \exp \\left[k_2\\left(I^*_{4i}-1\\right)^2\\right]\\left(a_{0i}\\times a_{0i}\\right)"
        )

        # Position equations and apply transformations
        equation14.scale(0.4).set_color(RED)
        equation15.scale(0.4).set_color(GREEN)

        equation14.next_to(Results_title1, DOWN, buff=0.3)
        equation15.next_to(equation14, DOWN, buff=0.2)

        # Animations to display the equations
        self.play(Write(equation14))
        self.next_slide()  # Adds interactivity

        self.play(Write(equation15))
        self.next_slide()  # Adds interactivity


        stresses = ImageMobject("stresses.png").scale(0.32).shift(ORIGIN+DOWN+RIGHT*0.25).shift(DOWN*0.34)
        self.play(FadeIn(stresses))
        self.next_slide()  # Adds interactivity

        label_stress = Tex("$\\rightarrow$ Collagen fibers contribute 95 $\\%$ of the total stress in the tissue").next_to(stresses, DOWN,buff=0.1).scale(0.6)

        self.play(Write(label_stress))
        self.next_slide()  # Moves to the next slide when ready

        self.play(FadeOut(stresses,equation14,equation15,label_stress))
        self.next_slide()  # Adds interactivity


        vol_scale = ImageMobject("vol_scale.png").scale(0.55).move_to(ORIGIN+DOWN+RIGHT*5.8)
        self.play(FadeIn(vol_scale))
        #self.next_slide()  # Moves to the next slide when ready


        # Include the video frames in the bottom right corner
        frame_dir = "./Vol_strain_wavy"
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])

        replay_count_volstrain = 3  # Define how many times the GIF will replay

        for _ in range(replay_count_volstrain):  # Loop to replay the GIF a specific number of times
            for frame_file in frame_files:
                frame_path = os.path.join(frame_dir, frame_file)
                frame = ImageMobject(frame_path)
                frame.scale(0.4)  # Scale the frame
                frame.to_corner(ORIGIN+DOWN)  # Position it in the bottom right corner
                self.add(frame)
                self.wait(1 / 30)  # Adjust this to control the display duration of each frame
                self.remove(frame)

        self.next_slide()  # Moves to the next slide when ready

        self.play(FadeOut(vol_scale))

        self.next_slide()  # Moves to the next slide when ready


        surf_elevation = ImageMobject("surf_elevation.png").scale(0.23).shift(ORIGIN+DOWN+RIGHT*0.25)
        patient_force = Tex("Increasing patient force").next_to(surf_elevation,UP,buff=0.1).scale(0.7)
        self.play(FadeIn(surf_elevation,patient_force))

        self.next_slide()  # Moves to the next slide when ready

        self.play(FadeOut(surf_elevation,AI1,Results_title1,patient_force))
        self.next_slide()  # Adds interactivity


        Results_title1 = Tex("Comparison of different auto-injectors").move_to(2.5*UP)
        self.play(Write(Results_title1))
        self.next_slide()  # Adds interactivity

        AI_defs = ImageMobject("AI_defs.png").scale(0.29).shift(ORIGIN+DOWN+RIGHT*0.25)
        self.play(FadeIn(AI_defs))

        self.next_slide()  # Adds interactivity

        self.play(FadeOut(AI_defs))
        self.next_slide()  # Adds interactivity


        Jacobian = ImageMobject("Jacobian.png").scale(0.29).shift(ORIGIN+DOWN+RIGHT*0.25)
        self.play(FadeIn(Jacobian))

        self.next_slide()  # Adds interactivity

        self.play(FadeOut(Jacobian,Results_title1))
        self.next_slide()  # Adds interactivity


        Results_title1 = Tex("Comparison with experiments").move_to(2.5*UP)
        self.play(Write(Results_title1))
        self.next_slide()  # Adds interactivity


        inj_depth = ImageMobject("inj_depth.png").scale(0.27).shift(ORIGIN+DOWN+RIGHT*0.15)
        self.play(FadeIn(inj_depth))

        self.next_slide()  # Moves to the next slide when ready

        self.play(FadeOut(inj_depth,Results_title1))
        self.next_slide()  # Adds interactivity


        Results_title3 = Tex("Pinch and Stretch Techniques").move_to(2.5*UP)
        self.play(Write(Results_title3))
        self.next_slide()  # Adds interactivity

        pinch = ImageMobject("pinch.png").scale(0.45).move_to(ORIGIN+LEFT*5.5).shift(0.25*UP+0.2*RIGHT)
        stretch = ImageMobject("stretch.png").scale(0.45).next_to(pinch, DOWN, buff=0.5)

        self.play(FadeIn(pinch,stretch))
        self.next_slide()  # Adds interactivity


        replay_count_volstrain = 3  # Define how many times the GIF will replay

        # Include the video frames in the bottom right corner
        frame_dir = "./top_view"
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])

        replay_count_pressure = 3 # Define how many times the GIF will replay

        for _ in range(replay_count_pressure):  # Loop to replay the GIF a specific number of times
            for frame_file in frame_files:
                frame_path = os.path.join(frame_dir, frame_file)
                frame = ImageMobject(frame_path)
                frame.scale(1.4)  # Scale the frame
                frame.to_corner(ORIGIN+DOWN)  # Position it in the bottom right corner
                self.add(frame)
                self.wait(1 / 16)  # Adjust this to control the display duration of each frame
                self.remove(frame)

        self.next_slide()  # Adds interactivity

        pressure_scale_pinch = ImageMobject("pressure_scale_pinch.png").scale(0.55).move_to(ORIGIN+DOWN+RIGHT*5.8)

        self.play(FadeIn(pressure_scale_pinch))
        
        # Include the video frames in the bottom right corner
        frame_dir = "./pressure_pinch"
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])

        replay_count_pressure = 3  # Define how many times the GIF will replay

        for _ in range(replay_count_pressure):  # Loop to replay the GIF a specific number of times
            for frame_file in frame_files:
                frame_path = os.path.join(frame_dir, frame_file)
                frame = ImageMobject(frame_path)
                frame.scale(0.6)  # Scale the frame
                frame.to_corner(ORIGIN+DOWN)  # Position it in the bottom right corner
                self.add(frame)
                self.wait(1 / 16)  # Adjust this to control the display duration of each frame
                self.remove(frame)
        self.next_slide()  # Adds interactivity

        velocity_scale_pinch = ImageMobject("velocity_scale_pinch.png").scale(0.55).move_to(ORIGIN+DOWN+RIGHT*5.8)


        self.play(FadeOut(pressure_scale_pinch))


        self.play(FadeIn(velocity_scale_pinch))


        # Include the video frames in the bottom right corner
        frame_dir = "./velocity_pinch"
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])

        replay_count_pressure = 3  # Define how many times the GIF will replay

        for _ in range(replay_count_pressure):  # Loop to replay the GIF a specific number of times
            for frame_file in frame_files:
                frame_path = os.path.join(frame_dir, frame_file)
                frame = ImageMobject(frame_path)
                frame.scale(0.6)  # Scale the frame
                frame.to_corner(ORIGIN+DOWN)  # Position it in the bottom right corner
                self.add(frame)
                self.wait(1 / 16)  # Adjust this to control the display duration of each frame
                self.remove(frame)

        self.next_slide()  # Adds interactivity


        # Results_title2 = Tex("Impact of tissue layer waviness").move_to(2.5*UP)
        # self.play(Write(Results_title2))
        # self.next_slide()  # Adds interactivity

        # # Define the first equation using LaTeX
        # equation14 = MathTex("\mathbf{E}","=","\\frac{1}{2}","\\left(\mathbf{C}-\mathbf{I}\\right)")
        # equation14.next_to(Results_title2, DOWN, buff=0.3).scale(0.8)
        # self.play(Write(equation14))

        # Ezz_scale = ImageMobject("Ezz.png").scale(0.55).move_to(ORIGIN+DOWN+RIGHT*5.8)
        # self.play(FadeIn(Ezz_scale))
        # self.next_slide()  # Moves to the next slide when ready


class DrugTransport(CustomSlide):
    def construct(self):
        # Add TOC to the scene at the beginning
        self.add(toc)

        # Move the first item in TOC to heading
        heading = toc[2].copy().move_to(ORIGIN).scale(1.25).to_corner(UP)

        # Instead of fading out all of TOC, first isolate toc[1]
        self.play(ReplacementTransform(toc[2], heading))

        # Now fade out the rest of TOC
        self.play(FadeOut(toc[0], toc[1],toc[3]))  # Fade out other items
        #self.play(FadeOut(toc), ReplacementTransform(toc[2],heading))

        # Add interactivity for the slide
        self.next_slide()

        Solution_top = Tex("Data-Driven FEM for High-fidelity Simulation").move_to(2*UP)

        # Create the text for each box
        PP_text = Text("Physiological \nparameters", font_size=20)  # Text with smaller font size
        IGAFEM_text = Text("IGA based FEM", font_size=20)
        PKPD_text = Text("PK/PD Models", font_size=20)
        Histology_text = Text("Histology data", font_size=20)
        Devices_text = Text("Injection devices \nand techniques", font_size=20)


        # Create rounded rectangles with width and height based on the text bounding box
        IGAFEM = RoundedRectangle(corner_radius=0.2, width=IGAFEM_text.width + 0.4, height=IGAFEM_text.height + 0.3, fill_opacity=0.1, color=YELLOW).move_to(ORIGIN)  # Center box
        PP = RoundedRectangle(corner_radius=0.2, width=PP_text.width + 0.4, height=PP_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(IGAFEM, LEFT, buff=3)  # Left box
        PKPD = RoundedRectangle(corner_radius=0.2, width=PKPD_text.width + 0.4, height=PKPD_text.height + 0.3, fill_opacity=0.1, color=YELLOW).next_to(IGAFEM, RIGHT, buff=3)  # Right box
        Histology = RoundedRectangle(corner_radius=0.2, width=Histology_text.width + 0.4, height=Histology_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, UP, buff=0.5)
        Devices = RoundedRectangle(corner_radius=0.2, width=Devices_text.width + 0.4, height=Devices_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, DOWN*4.8, buff=0.5)

        # Move the text to the center of each box
        PP_text.move_to(PP.get_center())
        IGAFEM_text.move_to(IGAFEM.get_center())
        PKPD_text.move_to(PKPD.get_center())
        Histology_text.move_to(Histology.get_center())
        Devices_text.move_to(Devices.get_center())

        # Group the box and the text together
        PKPD_group = VGroup(PKPD, PKPD_text)

        # Create arrows to connect the boxes
        arrow1 = Arrow(PP.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow2 = Arrow(IGAFEM.get_right(), PKPD.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_histology_to_igafem = Arrow(Histology.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_devices_to_igafem = Arrow(Devices.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts1 = ["BMI", "Flow rate", "Injection depth"]
        small_boxes1 = []
        small_box_group1 = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts1):
            box_text1 = Text(text, font_size=16)
            small_box1 = RoundedRectangle(corner_radius=0.2, width=box_text1.width + 0.4, height=box_text1.height + 0.3, fill_opacity=0.1)
            box_text1.move_to(small_box1.get_center())
            small_box_group1.add(VGroup(small_box1, box_text1))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group1.arrange(DOWN, buff=0.2).next_to(PP, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts = ["Fluid Flow","Solid deformations", "Drug Transport", "Stabilization: \nFPL+SUPG+DC"]
        small_boxes = []
        small_box_group = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts):
            box_text = Text(text, font_size=16)
            small_box = RoundedRectangle(corner_radius=0.2, width=box_text.width + 0.4, height=box_text.height + 0.3, fill_opacity=0.1)
            box_text.move_to(small_box.get_center())
            small_box_group.add(VGroup(small_box, box_text))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group.arrange(DOWN, buff=0.2).next_to(IGAFEM, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box = Arrow(IGAFEM.get_bottom(), small_box_group[0][0].get_top(), buff=0.1)

        text_better = Text("More accurate predictions", font_size=16)
        small_box_PKPD = RoundedRectangle(corner_radius=0.2, width=text_better.width + 0.4, height=text_better.height + 0.3, fill_opacity=0.1, color=GREEN)

        # Group the text and the box together
        PKPD_group = VGroup(small_box_PKPD, text_better)

        # Position the text inside the box by aligning the group
        text_better.move_to(small_box_PKPD.get_center())

        # Position the box and text group below the PKPD box
        PKPD_group.next_to(PKPD, DOWN, buff=0.4)
        arrow_to_first_box3 = Arrow(PKPD.get_bottom(), PKPD_group[0][0].get_top(), buff=0.1)
        # Play the animation to create the box and text together

        # Create a fade-in group for all elements
        fade_in_group = VGroup(
            Solution_top, PP, PP_text, IGAFEM, IGAFEM_text, PKPD, PKPD_text, 
            Histology, Histology_text, Devices, Devices_text, 
            arrow1, arrow2, arrow_histology_to_igafem, arrow_devices_to_igafem,
            small_box_group1, small_box_group
        )

        fade_out_group = VGroup(
            Solution_top, IGAFEM, IGAFEM_text, PKPD, PKPD_text, 
            Histology, Histology_text, Devices, Devices_text, 
            arrow1, arrow2, arrow_histology_to_igafem, arrow_devices_to_igafem,
            small_box_group
        )

        # Fade in all elements at once
        self.play(FadeIn(fade_in_group))
        self.next_slide()  # Adds interactivity
        self.play(FadeOut(fade_out_group))
        self.next_slide()  # Adds interactivity


        PP_group = VGroup(PP_text,PP,small_box_group1)
        PP_title = Tex("Effect of physiological parameters").move_to(2.5*UP)
        self.play(ReplacementTransform(PP_group, PP_title))
        self.next_slide()  # Adds interactivity

        BMI_title = Tex("$\\rightarrow$ Body Mass Index (BMI):").next_to(PP_title, DOWN, buff=0.5)
        self.play(Write(BMI_title))
        self.next_slide()  # Adds interactivity

        BMI_case = Tex("High BMI \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \  Low BMI").next_to(BMI_title, DOWN, buff=0.1).scale(0.6).shift(LEFT*1.5)

        C_scale = ImageMobject("concentration.png").scale(0.5).move_to(ORIGIN+LEFT*5.8)
        mu_scale = ImageMobject("viscosity.png").scale(0.5).next_to(C_scale,DOWN, buff=0.3)

        self.play(FadeIn(C_scale,mu_scale,BMI_case))

        # Include the video frames in the bottom right corner
        frame_dir = "./BMI"
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])

        replay_count_pressure = 3  # Define how many times the GIF will replay

        for _ in range(replay_count_pressure):  # Loop to replay the GIF a specific number of times
            for frame_file in frame_files:
                frame_path = os.path.join(frame_dir, frame_file)
                frame = ImageMobject(frame_path)
                frame.scale(0.4)  # Scale the frame
                frame.to_corner(ORIGIN+DOWN).shift(RIGHT*0.3+DOWN*0.3)  # Position it in the bottom right corner
                self.add(frame)
                self.wait(1 / 16)  # Adjust this to control the display duration of each frame
                self.remove(frame)

        self.next_slide()  # Adds interactivity
        self.play(FadeOut(C_scale,mu_scale,BMI_case))

        BMI_plume = ImageMobject("plume_BMI.png").scale(0.55).move_to(ORIGIN+DOWN)
        self.play(FadeIn(BMI_plume))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(BMI_plume,BMI_title))
        self.next_slide()  # Adds interactivity

        Flow_rate_title = Tex("$\\rightarrow$ Flow rate:").next_to(PP_title, DOWN, buff=0.5)
        self.play(Write(Flow_rate_title))
        self.next_slide()  # Adds interactivity

        Flow_rate_case = Tex("High flow rate \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ Low flow rate").next_to(Flow_rate_title, DOWN, buff=0.13).scale(0.6).shift(LEFT*1.2)

        C_scale = ImageMobject("concentration.png").scale(0.5).move_to(ORIGIN+LEFT*5.8)
        mu_scale = ImageMobject("viscosity.png").scale(0.5).next_to(C_scale,DOWN, buff=0.3)

        self.play(FadeIn(C_scale,mu_scale,Flow_rate_case))

        # Include the video frames in the bottom right corner
        frame_dir = "./Flow_rate"
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])

        replay_count_pressure = 3  # Define how many times the GIF will replay

        for _ in range(replay_count_pressure):  # Loop to replay the GIF a specific number of times
            for frame_file in frame_files:
                frame_path = os.path.join(frame_dir, frame_file)
                frame = ImageMobject(frame_path)
                frame.scale(0.4)  # Scale the frame
                frame.to_corner(ORIGIN+DOWN).shift(RIGHT*0.3+DOWN*0.3)  # Position it in the bottom right corner
                self.add(frame)
                self.wait(1 / 16)  # Adjust this to control the display duration of each frame
                self.remove(frame)

        self.next_slide()  # Adds interactivity
        self.play(FadeOut(C_scale,mu_scale,Flow_rate_case))

        Flow_rate_plume = ImageMobject("Flow_rate_plumes.png").scale(0.55).move_to(ORIGIN+DOWN)
        self.play(FadeIn(Flow_rate_plume))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(Flow_rate_plume,Flow_rate_title))
        self.next_slide()  # Adds interactivity

        Injection_depth_title = Tex("$\\rightarrow$ Injection depth:").next_to(PP_title, DOWN, buff=0.5)
        self.play(Write(Injection_depth_title))
        self.next_slide()  # Adds interactivity

        IP_case = Tex("Inj. depth = 6 mm \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ Inj. depth = 10 mm").next_to(Injection_depth_title, DOWN, buff=0.1).scale(0.6).shift(LEFT*0.8)


        C_scale = ImageMobject("concentration.png").scale(0.5).move_to(ORIGIN+LEFT*5.8)
        mu_scale = ImageMobject("viscosity.png").scale(0.5).next_to(C_scale,DOWN, buff=0.3)

        self.play(FadeIn(C_scale,mu_scale,IP_case))

        # Include the video frames in the bottom right corner
        frame_dir = "./Inj_depth"
        frame_files = sorted([f for f in os.listdir(frame_dir) if f.endswith('.png')])

        replay_count_pressure = 3  # Define how many times the GIF will replay

        for _ in range(replay_count_pressure):  # Loop to replay the GIF a specific number of times
            for frame_file in frame_files:
                frame_path = os.path.join(frame_dir, frame_file)
                frame = ImageMobject(frame_path)
                frame.scale(0.4)  # Scale the frame
                frame.to_corner(ORIGIN+DOWN).shift(RIGHT*0.3+DOWN*0.3)  # Position it in the bottom right corner
                self.add(frame)
                self.wait(1 / 16)  # Adjust this to control the display duration of each frame
                self.remove(frame)

        self.next_slide()  # Adds interactivity
        self.play(FadeOut(C_scale,mu_scale,IP_case))

        Inj_depth_plume = ImageMobject("inj_depth_plumes.png").scale(0.55).move_to(ORIGIN+DOWN)
        self.play(FadeIn(Inj_depth_plume))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(Inj_depth_plume,Injection_depth_title,PP_title))
        self.next_slide()  # Adds interactivity


        Solution_top = Tex("Data-Driven FEM for High-fidelity Simulation").move_to(2*UP)

        # Create the text for each box
        PP_text = Text("Physiological \nparameters", font_size=20)  # Text with smaller font size
        IGAFEM_text = Text("IGA based FEM", font_size=20)
        PKPD_text = Text("PK/PD Models", font_size=20)
        Histology_text = Text("Histology data", font_size=20)
        Devices_text = Text("Injection devices \nand techniques", font_size=20)


        # Create rounded rectangles with width and height based on the text bounding box
        IGAFEM = RoundedRectangle(corner_radius=0.2, width=IGAFEM_text.width + 0.4, height=IGAFEM_text.height + 0.3, fill_opacity=0.1, color=YELLOW).move_to(ORIGIN)  # Center box
        PP = RoundedRectangle(corner_radius=0.2, width=PP_text.width + 0.4, height=PP_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(IGAFEM, LEFT, buff=3)  # Left box
        PKPD = RoundedRectangle(corner_radius=0.2, width=PKPD_text.width + 0.4, height=PKPD_text.height + 0.3, fill_opacity=0.1, color=YELLOW).next_to(IGAFEM, RIGHT, buff=3)  # Right box
        Histology = RoundedRectangle(corner_radius=0.2, width=Histology_text.width + 0.4, height=Histology_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, UP, buff=0.5)
        Devices = RoundedRectangle(corner_radius=0.2, width=Devices_text.width + 0.4, height=Devices_text.height + 0.3, fill_opacity=0.1, color=PURPLE).next_to(PP, DOWN*4.8, buff=0.5)

        # Move the text to the center of each box
        PP_text.move_to(PP.get_center())
        IGAFEM_text.move_to(IGAFEM.get_center())
        PKPD_text.move_to(PKPD.get_center())
        Histology_text.move_to(Histology.get_center())
        Devices_text.move_to(Devices.get_center())

        # Group the box and the text together
        PKPD_group = VGroup(PKPD, PKPD_text)

        # Create arrows to connect the boxes
        arrow1 = Arrow(PP.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow2 = Arrow(IGAFEM.get_right(), PKPD.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_histology_to_igafem = Arrow(Histology.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)
        arrow_devices_to_igafem = Arrow(Devices.get_right(), IGAFEM.get_left(), buff=0.1,stroke_width=1.5,tip_length=0.15)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts1 = ["BMI", "Flow rate", "Injection depth"]
        small_boxes1 = []
        small_box_group1 = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts1):
            box_text1 = Text(text, font_size=16)
            small_box1 = RoundedRectangle(corner_radius=0.2, width=box_text1.width + 0.4, height=box_text1.height + 0.3, fill_opacity=0.1)
            box_text1.move_to(small_box1.get_center())
            small_box_group1.add(VGroup(small_box1, box_text1))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group1.arrange(DOWN, buff=0.2).next_to(PP, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Four smaller boxes below IGAFEM, aligned to the left
        small_box_texts = ["Fluid Flow","Solid deformations", "Drug Transport", "Stabilization: \nFPL+SUPG+DC"]
        small_boxes = []
        small_box_group = VGroup()

        # Create small boxes and add them to a VGroup, aligned to the left
        for i, text in enumerate(small_box_texts):
            box_text = Text(text, font_size=16)
            small_box = RoundedRectangle(corner_radius=0.2, width=box_text.width + 0.4, height=box_text.height + 0.3, fill_opacity=0.1)
            box_text.move_to(small_box.get_center())
            small_box_group.add(VGroup(small_box, box_text))

        # Arrange small boxes vertically below the IGAFEM box with some spacing, aligned to the left
        small_box_group.arrange(DOWN, buff=0.2).next_to(IGAFEM, DOWN, buff=0.4)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box1 = Arrow(PP.get_bottom(), small_box_group1[0][0].get_top(), buff=0.1)

        # Add an arrow from IGAFEM to the first small box
        arrow_to_first_box = Arrow(IGAFEM.get_bottom(), small_box_group[0][0].get_top(), buff=0.1)

        text_better = Text("More accurate predictions", font_size=16)
        small_box_PKPD = RoundedRectangle(corner_radius=0.2, width=text_better.width + 0.4, height=text_better.height + 0.3, fill_opacity=0.1, color=GREEN)

        # Group the text and the box together
        PKPD_group = VGroup(small_box_PKPD, text_better)

        # Position the text inside the box by aligning the group
        text_better.move_to(small_box_PKPD.get_center())

        # Position the box and text group below the PKPD box
        PKPD_group.next_to(PKPD, DOWN, buff=0.4)
        arrow_to_first_box3 = Arrow(PKPD.get_bottom(), PKPD_group[0][0].get_top(), buff=0.1)
        # Play the animation to create the box and text together

        # Create a fade-in group for all elements
        fade_in_group = VGroup(
            Solution_top, PP, PP_text, IGAFEM, IGAFEM_text, PKPD, PKPD_text, 
            Histology, Histology_text, Devices, Devices_text, 
            arrow1, arrow2, arrow_histology_to_igafem, arrow_devices_to_igafem,
            small_box_group1, small_box_group
        )

        fade_out_group = VGroup(
            Solution_top, PP, PP_text, IGAFEM, IGAFEM_text, 
            Histology, Histology_text, Devices, Devices_text, 
            arrow1, arrow2, arrow_histology_to_igafem, arrow_devices_to_igafem,
            small_box_group1, small_box_group
        )

        # Fade in all elements at once
        self.play(FadeIn(fade_in_group))
        self.next_slide()  # Adds interactivity
        self.play(FadeOut(fade_out_group))
        self.next_slide()  # Adds interactivity


        PKPD_group = VGroup(PKPD, PKPD_text)
        Drug_abs_title = Tex("Drug absorption").move_to(2.5*UP)
        self.play(ReplacementTransform(PKPD_group, Drug_abs_title))
        self.next_slide()  # Adds interactivity

        DA_devices_title = Tex("$\\rightarrow$ Effect of pre-injection technique:").next_to(Drug_abs_title, DOWN, buff=0.5)
        self.play(Write(DA_devices_title))

        abs_devices = ImageMobject("abs_devices.png").scale(0.55).move_to(ORIGIN+DOWN)
        self.play(FadeIn(abs_devices))
        self.next_slide()  # Adds interactivity
        
        DA_devices_result = Tex("$\\rightarrow$ Pre-injeciton technique increases absorption by 4$\\%$").next_to(abs_devices, DOWN, buff=0.2)
        self.play(Write(DA_devices_result))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(abs_devices,DA_devices_title,DA_devices_result))
        self.next_slide()  # Adds interactivity


        DA_BMI_title = Tex("$\\rightarrow$ Effect of BMI:").next_to(Drug_abs_title, DOWN, buff=0.5)
        self.play(Write(DA_BMI_title))

        abs_BMI = ImageMobject("abs_BMI.png").scale(0.55).move_to(ORIGIN+DOWN)
        self.play(FadeIn(abs_BMI))
        self.next_slide()  # Adds interactivity
        DA_BMI_result = Tex("$\\rightarrow$ A higher BMI increases absorption by 12$\\%$").next_to(abs_BMI, DOWN, buff=0.2)
        self.play(Write(DA_BMI_result))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(abs_BMI,DA_BMI_title,DA_BMI_result))
        self.next_slide()  # Adds interactivity

        DA_flow_rate_title = Tex("$\\rightarrow$ Effect of flow rate:").next_to(Drug_abs_title, DOWN, buff=0.5)
        self.play(Write(DA_flow_rate_title))
        self.next_slide()  # Adds interactivity

        abs_flow_rate = ImageMobject("abs_flow_rate.png").scale(0.55).move_to(ORIGIN+DOWN)
        self.play(FadeIn(abs_flow_rate))
        self.next_slide()  # Adds interactivity
        DA_flow_rate_result = Tex("$\\rightarrow$ A lower flow rate increases absorption by 3$\\%$").next_to(abs_flow_rate, DOWN, buff=0.2)
        self.play(Write(DA_flow_rate_result))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(abs_flow_rate,DA_flow_rate_title,DA_flow_rate_result))
        self.next_slide()  # Adds interactivity

        DA_inj_depth_title = Tex("$\\rightarrow$ Effect of injection depth:").next_to(Drug_abs_title, DOWN, buff=0.5)
        self.play(Write(DA_inj_depth_title))
        self.next_slide()  # Adds interactivity

        abs_inj_depth = ImageMobject("abs_inj_depth.png").scale(0.55).move_to(ORIGIN+DOWN)
        self.play(FadeIn(abs_inj_depth))
        self.next_slide()  # Adds interactivity
        DA_inj_depth_result = Tex("$\\rightarrow$ A shallower injection increases absorption by 5$\\%$").next_to(abs_inj_depth, DOWN, buff=0.2)
        self.play(Write(DA_inj_depth_result))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(abs_inj_depth,DA_inj_depth_title,DA_inj_depth_result))
        self.next_slide()  # Adds interactivity


        Exps_title = Tex("$\\rightarrow$ Comparison with experiments").next_to(Drug_abs_title,DOWN,buff=0.5)
        self.play(Write(Exps_title))

        Exps_plume1 = ImageMobject("plume_exps1.png").scale(1.1).move_to(ORIGIN+DOWN)
        self.play(FadeIn(Exps_plume1))
        self.next_slide()  # Adds interactivity

        Exps_plume2 = ImageMobject("plume_exps2.png").scale(1.1).move_to(ORIGIN + DOWN)
        self.play(FadeIn(Exps_plume2))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(Exps_plume1,Exps_plume2))

        Exps_abs = ImageMobject("Experiments_abs.png").scale(0.55).move_to(ORIGIN+DOWN)
        self.play(FadeIn(Exps_abs))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(Exps_abs,Exps_title,Drug_abs_title,heading))


class Conclusions(CustomSlide):
    def construct(self):
        # Add TOC to the scene at the beginning
        self.add(toc)

        # Move the first item in TOC to heading
        heading = toc[3].copy().move_to(ORIGIN).scale(1.25).to_corner(UP)

        # Instead of fading out all of TOC, first isolate toc[1]
        self.play(ReplacementTransform(toc[3], heading))

        # Now fade out the rest of TOC
        self.play(FadeOut(toc[0], toc[1],toc[2]))  # Fade out other items
        #self.play(FadeOut(toc), ReplacementTransform(toc[2],heading))

        # Add interactivity for the slide
        self.next_slide()

        Contributions_title = Tex("Contributions").move_to(2.5*UP+LEFT)

        Contributions = Group(
            Text("Contributions:"),
            Tex("$\\circ$ Developed a data-driven large-deformation poromechanical model coupled with drug transport and absorption dynamics, "
                "to study large-volume subcutaneous injections of high-viscosity drugs using IGA."),
            Tex("$\\circ$ Created a high-fidelity virtual patient simulation that accounts for realistic tissue geometries, "
                "anisotropic behavior from collagen fibers, injection devices, techniques, and physiological parameters."),
            Tex("$\\circ$ Informed a PKPD model using the FEM results, enabling analysis of factors like injection device, technique, BMI, and depth, "
                "which traditional PKPD models cannot account for."),
            Tex("$\\circ$ Validated the model’s mechanical behavior and drug transport through experimental data.")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).scale(0.7).shift(0.5*DOWN)


        self.next_slide()

        for i in range(len(Contributions)):
            self.next_slide()  # Adds interactivity
            self.play(FadeIn(Contributions[i], shift=0.5*LEFT))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(Contributions))
        self.next_slide()


        Role_title = Tex("My role in the project").move_to(2.5*UP+LEFT)

        Roles = Group(
            Text("My Role in the Project:"),
            Tex("$\\circ$ Collaborated with Eli Lilly for device geometry and physiological parameters."),
            Tex("$\\circ$ Worked with Prof. Vlachos and Melissa Brindise for histology data and the image processing algorithm to define tissue layers."),
            Tex("$\\circ$ Partnered with Prof. Bilionis and Atharva Hans to develop the stochastic method for generating 3D tissue surfaces from 1D histology data."),
            Tex("$\\circ$ Received guidance from Prof. Gomez on the numerical strategy."),
            Tex("$\\circ$ Led the development of the computational model and integrated all components into a cohesive system.")
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).scale(0.7).shift(0.5*DOWN)


        self.next_slide()

        for i in range(len(Roles)):
            self.next_slide()  # Adds interactivity
            self.play(FadeIn(Roles[i], shift=0.5*LEFT))
        self.next_slide()  # Adds interactivity

        self.play(FadeOut(Roles,heading))
        self.next_slide()

        # Load the image
        Casteleiro = ImageMobject("ManuelCasteleiro.png").scale(0.6).move_to(ORIGIN)

        # Create the tribute text
        tribute_text = Tex("In Memoriam, Prof. Manuel Casteleiro (1947-2021)", font_size=36).move_to(UP * 2.5)
        quote_text = Tex("``Great figures are usually beacons that cast their light far beyond their professions.''", font_size=24).next_to(Casteleiro, DOWN, buff=0.5)

        # Add the elements to the scene

        # Optionally, you can add a fade-in effect
        self.play(FadeIn(tribute_text), FadeIn(Casteleiro), FadeIn(quote_text))
        self.next_slide()















        
        

 




















    










        


