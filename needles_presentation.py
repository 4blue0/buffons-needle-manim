import numpy as np
from manim import *
from tqdm import tqdm

# Helper function: Intro animation
def intro_animation(scene1):
    t = Text("Buffon's needle problem").scale(1.5).set_color(BLUE_C) # The "UP" command put the object on the axis y=1 (i.e. 1 unit up from the axis y=0)
    
    base_line1 = Line([-10, 2, 0], [-8, 2, 0], color=GRAY_BROWN)
    base_line2 = Line([-10, -2, 0], [-8, -2, 0], color=GRAY_BROWN)

    lines = VGroup(*[
    line
    for i in range(1, 6)
    for line in [
        base_line1.copy().shift(RIGHT * (3 * i)).rotate(PI / (2 * i)),
        base_line2.copy().shift(RIGHT *  (3.5 * i) ).rotate(- PI / (3 * i)),
    ]
    ])

    scene1.play(Write(t), Create(lines), run_time = 3)
    scene1.wait(1)

    scene1.play(
        t.animate.shift(LEFT * 10 + UP * 10).rotate(PI /2).set_opacity(0), # The "set_opacity(0)" command and especially the 0 number make the t,t2 to be totally disappeared
        lines.animate.scale(2).shift(RIGHT * 8 + DOWN * 8).rotate(PI / 2).set_opacity(0), # when the next frame appears.
        run_time=1.5
    )
    
    t2 = Text("Let's drop a needle at random!").scale(1.2) # The "DOWN" command put the object on the axis y=-1 (i.e. 1 unit down from the axis y=0)
    scene1.play(Write(t2))
    scene1.wait(1)
    scene1.play(t2.animate.shift(8 * DOWN).set_opacity(0))

# Helper function: Draw two parallel lines
def draw_parallel_lines(scene2):
    line1 = Line(LEFT * 5 + UP, RIGHT * 5 + UP) # The line starts from (-5,1) and finishes at (5,1) 
    line2 = Line(LEFT * 5 + DOWN, RIGHT * 5 + DOWN) # The line starts from (-5,-1) and finishes at (5,-1)
    scene2.play(Create(line1), Create(line2))
    scene2.wait(1)
    
    # Animate line1 and line2 moving apart
    slide_distance = 1.5  # units to move each line (can increase this to 1.5 or 2)
    scene2.play(
        line1.animate.shift(UP * slide_distance),
        line2.animate.shift(DOWN * slide_distance),
        run_time=2
    )
    
    # Remark: Finally, we have d = 5

    # We create the middle dashed line between line1 and line2
    middle_line = DashedLine(LEFT * 5, RIGHT * 5, dash_length = 0.5)
    scene2.play(Create(middle_line))
    scene2.wait(1)

    # We emphasize with brace that the distance between line1 and line2 is d
    bracket = BraceBetweenPoints(
        line2.get_start(),  # bottom left point
        line1.get_start(),  # top left point
        direction = LEFT    # the position of the brace
    )
    label = MathTex("d").next_to(bracket, LEFT)
    scene2.play(Create(bracket), Write(label))
    scene2.wait(1)

    # We emphasize with brace that the distance between line2 and middle_line and the distance between line1 and middle_line is d\2
    half_down_bracket = BraceBetweenPoints(
        line2.get_end(),  # bottom right point
        middle_line.get_end(), # top right point
        direction = RIGHT
    )
    label_down = MathTex(r"\frac{d}{2}").next_to(half_down_bracket, RIGHT)

    half_up_bracket = BraceBetweenPoints(
        middle_line.get_end(),  
        line1.get_end(), 
        direction = RIGHT
    )
    label_up = MathTex(r"\frac{d}{2}").next_to(half_up_bracket, RIGHT)

    scene2.play(Create(half_down_bracket), Write(label_down), Create(half_up_bracket), Write(label_up))
    scene2.wait(1)

    # We create a needle with length (4=)l<d(=5)
    needle = Line(LEFT * 2 + UP, RIGHT * 2 + UP, color = GRAY_BROWN)
    scene2.play(Create(needle))
    scene2.wait(1)

    # We emphasize with brace that the needle length is l and set the assumption l<=d
    needle_length = BraceBetweenPoints(
        needle.get_start(),
        needle.get_end(),
        
    )
    l = MathTex("\ell").next_to(needle_length, DOWN)
    assumption = MathTex(r"\text{Assumption: } \ell \leq d").to_corner(UL) # Write the text to the upper left corner 
    scene2.play(Create(needle_length), Write(l))
    scene2.wait(1)
    scene2.play(Write(assumption), run_time = 1.5)
    scene2.wait(1)
    scene2.play(FadeOut(l), Unwrite(needle_length))
    scene2.wait(1)

    # Since the needle was drawn from (-2,1) to (2,1), we then create the middle of the needle (0,1)
    mid_needle_point = Dot(point = ORIGIN + UP, color = GRAY) # ORIGIN = (0,0). We can also do it with point = needle.get_center()
    scene2.play(FadeIn(mid_needle_point))
    scene2.wait(1)
    

    # Rotate the needle 4*π radius around of its middle.
    scene2.play(Rotate(needle, angle = 4 * PI, about_point = needle.get_center()),
                 run_time = 6,
                 rate_func = smooth)
    scene2.wait(1)

    # Rotate it until the first possible crossing
    scene2.play(Rotate(needle, angle = PI / 4 + 0.06, about_point = needle.get_center()),
                 run_time = 2)
    scene2.wait(1)
    
    # half_down_needle_length = BraceBetweenPoints(
    #    needle.get_start(),
    #    needle.get_center()
    # )

    # Paint with red the first possible crossing point
    first_point_cross = Dot(point = [1.32, 5/2, 0], color = RED)
    scene2.play(FadeIn(first_point_cross))
    scene2.wait(1)

    # We emphasize with brace that the upper half distance of the needle is l/2
    half_up_needle_length = BraceBetweenPoints(
        needle.get_center(),
        needle.get_end()
    )
    # label_half_down = MathTex(r"\frac{\ell}{2}").next_to(half_down_needle_length,)
    label_half_up = MathTex("\ell /2").next_to(half_up_needle_length)
    label_half_up.move_to(half_up_needle_length.get_center() + RIGHT * 0.7 + DOWN * 0.4) # Since this brace is π/4-rotated we need to put manually the position of l/2
    scene2.play(Create(half_up_needle_length), Write(label_half_up))
    scene2.wait(1)

    # We create the dashed perpendicular line from the needles's center to line1 and put it with label x
    x = DashedLine(needle.get_center(), [0,5/2,0], color = BLUE)
    label_x = MathTex("x", color = BLUE).next_to(x, LEFT)
    scene2.play(Create(x), Write(label_x))
    scene2.wait(1)

    # We create the Right angle between x and line1. We know that the intersection is occured at [0,2.5,0]
    perpendicular_angle = RightAngle(Line([0,2.5,0], [0,2.5,0] + DOWN),
                                     Line([0,2.5,0], [0,2.5,0] + RIGHT),
                                     length = 0.2,   
                                    )
    scene2.play(Create(perpendicular_angle))
    scene2.wait(1)
    
    # We create the θ angle between the line1 and the needle. We know from above that the particular intersection is occured at the point [1.45, 5/2, 0]
    theta_angle = Angle(Line([1.32, 5/2, 0], [1.32, 5/2, 0] + LEFT),
                        Line([1.32, 5/2, 0], [1.32, 5/2, 0] + LEFT * 0.2 + DOWN * 0.3)
                        )
    theta_label = MathTex(r"\theta", color = TEAL).move_to(theta_angle.get_center() + LEFT * 0.3 + DOWN * 0.1) # Scale(0.7) create θ by the 70% of the default size
    scene2.play(Create(theta_angle), Write(theta_label))
    scene2.wait(2)


    scene2.play(FadeOut(label), FadeOut(label_down), FadeOut(label_up))
    scene2.wait(1)
    scene2.play(
        bracket.animate.shift(RIGHT * 15).rotate(PI /2).set_opacity(0),
        half_down_bracket.animate.shift(LEFT * 15).rotate(PI / 2).set_opacity(0),
        half_up_bracket.animate.shift(LEFT * 15).rotate(PI / 2).set_opacity(0),
        line2.animate.shift(10 * UP).rotate(PI / 2).set_opacity(0),
        run_time = 1.5
    )
    # scene2.play(FadeOut(middle_line))
    # scene2.play(Unwrite(middle_line))

    #for dash in middle_line.submobjects:
    #   scene2.play(dash.animate.shift(3 * UP).rotate(PI).set_opacity(0),
    #               run_time = 0.2)

    # Focusing on the middle line, shift up half of the dashes and move down the other half
    dashes = middle_line.submobjects
    n = len(dashes)
    animations = []

    for i, dash in enumerate(dashes):
        if i < n // 2:
            animations.append(dash.animate.shift(3 * UP + 3 * LEFT).rotate(PI).set_opacity(0))
        else:
            animations.append(dash.animate.shift(3 * DOWN + 3 * RIGHT).rotate(PI).set_opacity(0))

    scene2.play(*animations, run_time=1.5) # *animation unpacks the list (i.e. turns [a1, a2, a3] into a1, a2, a3)
    scene2.wait(2)
    
    # sin(θ)= x/(l/2) iff x = (l/2)sin(θ)
    pythagor1 = MathTex(r"\sin{\theta} = \frac{x}{\frac{\ell}{2}}").move_to(DOWN) # for some reason i can't isolate the x in order to paint it blue
    pythagor2 = MathTex(r"\iff").move_to(2 * DOWN + 2 * LEFT)
    pythagor3 = MathTex(r"x = \frac{\ell}{2}\sin\theta",
                        substrings_to_isolate = [r"\theta", "x"]).move_to(2 * DOWN)
    pythagor3.set_color_by_tex(r"\theta", TEAL)
    pythagor3.set_color_by_tex("x", BLUE)

    scene2.play(Write(pythagor1))
    scene2.wait(1)
    scene2.play(Write(pythagor2), run_time=1)
    scene2.play(ReplacementTransform(pythagor1.copy(), pythagor3), run_time=2) # smoothly morph from pythagor1 to pythagor3
    scene2.wait(2)

    # Keep on the screne only the x = (l/2)sinθ
    scene2.play(
        pythagor3.animate.shift(5.4 * UP + 4 * RIGHT).rotate(PI * 2),
        pythagor1.animate.shift(6 * UP + 6 * LEFT).rotate(PI / 2).set_opacity(0),
        pythagor2.animate.shift(3 * DOWN).rotate(PI / 2).set_opacity(0),
        run_time = 2
    )
    scene2.wait(2)

    scene2.play(Write(Text("What is the 'crossing rule' ?").move_to(1.5 * DOWN)),
                pythagor3.animate.shift(10 * DOWN ).rotate(PI * 2).set_opacity(0),
                run_time = 1.5)
    
    scene2.play(
        *[FadeOut(mob) for mob in (
            first_point_cross, half_up_needle_length,
            label_half_up, theta_angle, theta_label,
        )],
        run_time=0.6,
    )

    needle_center = needle.get_center().copy()
    half_length = needle.get_length() / 2
    theta = ValueTracker(needle.get_angle())

    def upper_tip():
        return needle_center + rotate_vector(
            RIGHT * half_length, theta.get_value()
        )

    # Animate the existing needle instead of creating another one.
    needle.add_updater(lambda mob: mob.put_start_and_end_on(
        2 * needle_center - upper_tip(), upper_tip()
    ))

    horizontal_reference = Line(
        needle_center + LEFT * 0.8, needle_center + RIGHT * 0.8,
        color=WHITE, stroke_width=2,
    )

    # Separate the projection from the blue distance x.
    projection_base = needle_center + RIGHT * 2.7

    def projection_tip():
        return projection_base + UP * (
            half_length * np.sin(theta.get_value())
        )

    base_guide = DashedLine(
        needle_center, projection_base, stroke_opacity=0.35
    )
    projection = always_redraw(lambda: Line(
        projection_base, projection_tip(), color=YELLOW, stroke_width=3
    ))
    tip_guide = always_redraw(lambda: DashedLine(
        upper_tip(), projection_tip(), stroke_opacity=0.5
    ))
    projection_label = MathTex(
        r"\frac{\ell}{2}\sin\theta", color=YELLOW, font_size=28
    )
    projection_label.add_updater(
        lambda mob: mob.next_to(projection, RIGHT, buff=0.15)
    )

    # Measure the acute angle to the horizontal, including when leaning left.
    def make_angle():
        angle = theta.get_value()
        return Arc(
            radius=0.4,
            start_angle=0 if angle <= PI / 2 else angle,
            angle=min(angle, PI - angle),
            arc_center=needle_center, color=TEAL,
        )

    moving_angle = always_redraw(make_angle)
    moving_theta = MathTex(r"\theta", color=TEAL, font_size=28)
    moving_theta.add_updater(lambda mob: mob.move_to(
        needle_center + 1.8 * (
            moving_angle.point_from_proportion(0.5) - needle_center
        )
    ))

    projection_label.update()
    moving_theta.update()
    scene2.add(
        base_guide, horizontal_reference, projection, tip_guide,
        projection_label, moving_angle, moving_theta,
    )
    scene2.bring_to_front(mid_needle_point)

    scene2.play(
        theta.animate.set_value(3 * PI / 4 - 0.06),
        run_time=6, rate_func=linear,
    )
    scene2.wait(2)
    scene2.play(
        theta.animate.set_value(PI / 3),
        run_time=6, rate_func=linear,
    )
    scene2.wait(1)
    
    cros_rule = MathTex(r"x\leq\frac{\ell}{2}\sin\theta",
                         substrings_to_isolate = [r"\theta", "x"]).move_to(3 * DOWN)
    cros_rule.set_color_by_tex(r"\theta", TEAL)
    cros_rule.set_color_by_tex("x", BLUE)
    box_rule = SurroundingRectangle(cros_rule, color = WHITE)
    scene2.play(Write(cros_rule), Create(box_rule))
    scene2.wait(3)

    for mob in list(scene2.mobjects):
        mob.clear_updaters()

    scene2.play(
        *[FadeOut(mob) for mob in list(scene2.mobjects)],
        run_time=1.5,
    )


def different_needles(scene3):
    line3 = Line([-5, 2, 0], [5, 2, 0])
    line4 = Line([-5, -2, 0], [5, -2, 0])
    mid_line34 = DashedLine([-5, 0, 0], [5, 0, 0])
    test_needle1 = Line([-3, 1.5, 0], [0, 2.5, 0], color = GRAY_BROWN)
    mid_test_needle1 = Dot(point = test_needle1.get_center(), color  =GRAY)
    test_needle2 = Line([-3, -1.5, 0], [10**(1/2) - 3, -1.5, 0], color = GRAY_BROWN)
    mid_test_needle2 = Dot(point = test_needle2.get_center(), color  =GRAY)
    test_needle3 = Line([5 - 10**(1/2), 0, 0], [5, 0, 0], color = GRAY_BROWN)
    mid_test_needle3 = Dot(point = test_needle3.get_center(), color  =GRAY)
    
    scene3.play(Create(line3), Create(line4))
    scene3.wait(1)
    scene3.play(Create(mid_line34), Create(test_needle1),
                Create(test_needle2), Create(mid_test_needle1), Create(mid_test_needle2),
                Create(test_needle3), Create(mid_test_needle3))
    scene3.wait(2)

    label_x1 = MathTex("x=0", color = BLUE).next_to(mid_test_needle1, DOWN)
    x2 = DashedLine(test_needle2.get_center(), [test_needle2.get_center()[0], -2, 0], color = BLUE)
    label_x2 = MathTex("x", color = BLUE).next_to(x2, LEFT)
    x3_up = DashedLine(test_needle3.get_center(), [test_needle3.get_center()[0], 2, 0], color = BLUE)
    label_x3_up = MathTex(r"x = d/2", color = BLUE).next_to(x3_up, RIGHT)
    x3_down = DashedLine(test_needle3.get_center(), [test_needle3.get_center()[0], -2, 0], color = BLUE)
    label_x3_down = MathTex(r"x = d/2", color = BLUE).next_to(x3_down, RIGHT)

    scene3.play(Create(x2), Create(x3_up), Create(x3_down), Write(label_x1),
                Write(label_x2), Write(label_x3_up), Write(label_x3_down))
    scene3.wait(1)
    
    scene3.play(Rotate(test_needle1, angle = 4 * PI, about_point = mid_test_needle1.get_center()),
                Rotate(test_needle2, angle = 4 * PI, about_point = mid_test_needle2.get_center()),
                Rotate(test_needle3, angle = 4 * PI, about_point = mid_test_needle3.get_center()),
                run_time = 10,
                rate_func = smooth)
    scene3.wait(1)
    
    scene3.play(line3.animate.shift(DOWN * 8).rotate(PI / 2).set_opacity(0),
                line4.animate.shift(UP * 8).rotate(PI / 2).set_opacity(0),
                FadeOut(mid_line34), FadeOut(label_x1), FadeOut(label_x2),
                test_needle1.animate.shift(RIGHT * 15).rotate(PI /2).set_opacity(0),
                test_needle2.animate.shift(RIGHT * 15).rotate(PI /2).set_opacity(0),
                test_needle3.animate.shift(LEFT * 15).rotate(PI /2).set_opacity(0),
                FadeOut(label_x3_down), FadeOut(label_x3_up), FadeOut(x2), FadeOut(x3_down),
                FadeOut(x3_up), FadeOut(mid_test_needle1), FadeOut(mid_test_needle2),
                FadeOut(mid_test_needle3),

                run_time = 2
                )

def probability_calculations(scene4):
    
    t_reminder1 = Tex("Crossing rule: ").set_color(GREEN_B).to_corner(UL)
    t_reminder2 = MathTex(r"X \leq \frac{\ell}{2} \sin \Theta",
                         substrings_to_isolate = [r"\Theta", "X"]).next_to(t_reminder1, RIGHT)
    t_reminder2.set_color_by_tex(r"\Theta", TEAL)
    t_reminder2.set_color_by_tex("X", BLUE)
    

    # this is good, because we don't need to separate the text commands in order to paint x,θ. We can do the same above
    unif_x = MathTex(
    r"\text{So, }", 
    "X", 
    r"\sim U\left(0, \frac{d}{2}\right)", 
    r"\quad \text{and} \quad", 
    r"\Theta", 
    r"\sim U\left(0, \frac{\pi}{2}\right)"
    )

    unif_x[1].set_color(BLUE)
    unif_x[4].set_color(TEAL)
 
    scene4.play(Write(t_reminder1), Write(t_reminder2), Write(unif_x))
    scene4.wait(1)

    t3 = MathTex(r"\Longrightarrow").move_to(1.5 * DOWN + 5 * LEFT)
    dens_func0 = MathTex(r"f_X(x) = \frac{1}{\frac{d}{2} - 0}\quad\text{and}\quad f_{\Theta}(\theta)=\frac{1}{\frac{\pi}{2} - 0}",
                         substrings_to_isolate = ["X", r"\Theta"]).move_to(1.5 * DOWN)
    dens_func0.set_color_by_tex("X", BLUE)
    dens_func0.set_color_by_tex(r"\Theta", TEAL)
    scene4.play(Write(t3), ReplacementTransform(unif_x.copy(), dens_func0), run_time = 2)
    scene4.wait(2)

    dens_func = MathTex(r"f_X(x) = \frac{2}{d}\quad\text{and}\quad f_{\Theta}(\theta)=\frac{2}{\pi}",
                        substrings_to_isolate = ["X", r"\Theta"]).move_to(1.5 * DOWN)
    dens_func.set_color_by_tex("X", BLUE)
    dens_func.set_color_by_tex(r"\Theta", TEAL)
    scene4.play(Transform(dens_func0, dens_func), run_time = 2)
    scene4.wait(2)

    scene4.play(unif_x.animate.shift(10 * UP).set_opacity(0),
                t3.animate.shift(10 * UP).set_opacity(0),
                dens_func0.animate.shift(10 * UP).set_opacity(0),
                dens_func.animate.to_corner(UR))
    scene4.wait(2)

    t4 = Tex(r"Now, given the fact that the random variables are independent \\ the joint probability density function is given by")
    scene4.play(Write(t4), run_time = 2)
    
    joint_dens_func = MathTex(r"f_{X,\Theta}(x, \theta) = f_X(x)f_{\Theta}(\theta)",
                              substrings_to_isolate = ["X", r"\Theta"]).move_to(DOWN)
    joint_dens_func.set_color_by_tex("X", BLUE)
    joint_dens_func.set_color_by_tex(r"\Theta", TEAL)

    joint_dens_func1 = MathTex(r"=\frac{4}{\pi d}").move_to(2 * DOWN + 0.16 * RIGHT)

    scene4.play(Write(joint_dens_func))
    scene4.wait(1)
    scene4.play(ReplacementTransform(joint_dens_func.copy(), joint_dens_func1), run_time = 1.5)
    scene4.wait(1)
    
    tex_jpfd = Tex("Joint PDF: ").set_color(GREEN_B).next_to(t_reminder2, RIGHT, buff = 1.5) # buff is for the space
    joint_dens_func_final = MathTex(r"f_{X,\Theta}(x, \theta) = \frac{4}{\pi d}",
                                    substrings_to_isolate = ["X", r"\Theta"]).next_to(tex_jpfd, RIGHT)
    joint_dens_func_final.set_color_by_tex("X", BLUE)
    joint_dens_func_final.set_color_by_tex(r"\Theta", TEAL)

    scene4.play(t4.animate.shift(8 * DOWN).set_opacity(0),
                FadeOut(dens_func), FadeOut(joint_dens_func), FadeOut(joint_dens_func1),
                Write(joint_dens_func_final), Write(tex_jpfd),
                run_time = 2)
    
    scene4.wait(2)

    tex_prob = Text("The probability that the needle will cross a line is").scale(0.8)
    scene4.play(Write(tex_prob), run_time = 2)
    scene4.wait(1)

    cros_prob1 = MathTex(r"\mathbb{P} &= \mathbb{P}\left(0 \leq \Theta \leq \frac{\pi}{2},\quad 0 \leq X \leq \frac{\ell}{2} \sin \Theta\right) \\",
                         r"& = \int_0^{\frac{\pi}{2}}\int_0^{\frac{\ell\sin\theta}{2}} f_{X,\Theta}(x,\theta) dxd\theta",
                         substrings_to_isolate = ["X", r"\Theta"]).move_to(2 * DOWN)
    cros_prob1.set_color_by_tex("X", BLUE)
    cros_prob1.set_color_by_tex(r"\Theta", TEAL)
    
    scene4.play(Write(cros_prob1), run_time = 2)
    scene4.wait(1)
    
    scene4.play(
        tex_prob.animate.shift(2 * UP),
        cros_prob1.animate.shift(2 * UP),
        run_time = 1.5
    )
    
    scene4.wait(1)
    cros_prob2 = MathTex(r"= \int_0^{\frac{\pi}{2}}\int_0^{\frac{\ell\sin\theta}{2}} \frac{4}{\pi d}dxd\theta").move_to([-1.5,-2.5,0])
    scene4.play(ReplacementTransform(cros_prob1.copy(), cros_prob2), run_time = 2)
    scene4.wait(1)

    scene4.play(
        t_reminder1.animate.shift(10 * DOWN + 10 * RIGHT).rotate(PI / 2).set_opacity(0),
        t_reminder2.animate.shift(10 * DOWN + 10 * RIGHT).rotate(PI / 2).set_opacity(0),
        tex_jpfd.animate.shift(10 * DOWN + 10 * LEFT).rotate(PI / 2).set_opacity(0),
        joint_dens_func_final.animate.shift(10 * DOWN + 10 * LEFT).rotate(PI / 2).set_opacity(0),
        tex_prob.animate.shift(1.5 * UP),
        cros_prob1.animate.shift(1.5 * UP),
        cros_prob2.animate.shift(1.5 * UP),

        run_time = 2
    )
    
    scene4.wait(1)
    cros_prob3 = MathTex(r"= \int_0^{\frac{\pi}{2}} \frac{4}{\pi d} \frac{\ell\sin\theta}{2}  d\theta").next_to(cros_prob2, DOWN, aligned_edge = LEFT)
    scene4.play(ReplacementTransform(cros_prob2.copy(), cros_prob3), run_time = 2)
    scene4.wait(1)

    cros_prob4 = MathTex(r"= \frac{2\ell}{\pi d} \int_0^{\frac{\pi}{2}} \sin\theta d\theta").next_to(cros_prob3, RIGHT)
    scene4.play(ReplacementTransform(cros_prob3.copy(), cros_prob4), run_time = 2)
    scene4.wait(1)

    cros_prob5 = MathTex(r"= \frac{2\ell}{\pi d}").next_to(cros_prob4, RIGHT)
    scene4.play(ReplacementTransform(cros_prob4.copy(), cros_prob5))
    scene4.wait(2)

    cros_prob_final = MathTex(r"\mathbb{P} = \frac{2\ell}{\pi d}")
    box_cros_prob_final = SurroundingRectangle(cros_prob_final, color = DARK_BROWN)

    scene4.play(
        cros_prob1.animate.shift(10 * DOWN).set_opacity(0),
        cros_prob2.animate.shift(10 * UP).set_opacity(0),
        cros_prob3.animate.shift(10 * UP).set_opacity(0),
        cros_prob4.animate.shift(10 * UP).set_opacity(0),
        cros_prob5.animate.shift(10 * UP).set_opacity(0),
        tex_prob.animate.shift(2 * DOWN),
        Write(cros_prob_final),
        Create(box_cros_prob_final),
        run_time = 3
    )

    scene4.wait(1)

def needle_drop_animation(needle, final_color, tilt=10 * DEGREES, ceiling=3.0):
    landing = needle.copy().set_color(final_color)
    center = landing.get_center()
    half_length = landing.get_length() / 2
    drop_height = min(0.6, max(0, ceiling - center[1] - 1.12 * half_length))
    bounce_height = min(0.1, drop_height / 3)

    def update_pose(mobject, alpha):
        # Always rebuild from the sampled landing pose to avoid accumulated drift.
        mobject.become(landing)
        if alpha >= 0.9:
            return

        if alpha < 0.6:
            progress = alpha / 0.6
            height = drop_height * (1 - progress**2)
            angle = tilt * (1 - progress)
        else:
            progress = (alpha - 0.6) / 0.3
            height = 4 * bounce_height * progress * (1 - progress)
            angle = -0.3 * tilt * np.sin(PI * progress)

        mobject.set_color(WHITE)
        mobject.scale(1 + 0.12 * height / max(drop_height, 1e-6), about_point=center)
        mobject.rotate(angle, about_point=center)
        mobject.shift(UP * height)

    update_pose(needle, 0)
    return UpdateFromAlphaFunc(needle, update_pose, rate_func=linear)


def monte_carlo_simulation(scene):
    scene.clear()

    # Experiment settings
    total_throws = 10_000
    needle_length = 4
    line_spacing = 5
    rng = np.random.default_rng(42)

    # Scale the physical dimensions to fit the drawing.
    display_spacing = 0.8
    display_length = display_spacing * needle_length / line_spacing

    centers_x = rng.uniform(-6.0, -0.8, total_throws)
    centers_y = rng.uniform(-0.8, 2.4, total_throws)
    angles = rng.uniform(0, PI, total_throws)

    # Distance from each center to its nearest horizontal line.
    offsets = np.mod(centers_y, display_spacing)
    distances = np.minimum(offsets, display_spacing - offsets)

    crossings = (
        distances <= display_length / 2 * np.abs(np.sin(angles))
    )
    cumulative_crossings = np.cumsum(crossings)
    throw_numbers = np.arange(1, total_throws + 1)

    estimates = np.full(total_throws, np.nan)
    np.divide(
        2 * needle_length * throw_numbers,
        line_spacing * cumulative_crossings,
        out=estimates,
        where=cumulative_crossings > 0,
    )

    t = Text("Monte Carlo Simulation").scale(1.5).set_color(BLUE_C)
    scene.play(Write(t), run_time = 3)
    scene.wait(1)
    scene.play(
        #t.animate.shift(LEFT * 10 + UP * 10).rotate(PI /2).set_opacity(0),
        t.animate.to_edge(UP),
        #Write(formula),
        run_time = 1.5
    )
    scene.wait(1)

    reminder = Text("We have that:").move_to(UP * 2)
    cros_prob_final = MathTex(r"\mathbb{P} = \frac{2\ell}{\pi d}")
    formula = MathTex(
    r"\Longrightarrow"
    r"\widehat{\pi}_N = \frac{2\ell}{d}"
    r"\frac{\text{Number of drops}}{\text{Number of crossings}}"
    )
    formula_without_arrow = MathTex(
    r"\widehat{\pi}_N = \frac{2\ell}{d}"
    r"\frac{\text{Number of drops}}{\text{Number of crossings}}"
    )
    box_formula_without = SurroundingRectangle(formula_without_arrow, color = DARK_BROWN)
    scene.play(
        Write(reminder),
        Write(cros_prob_final),
        run_time = 2
    )
    scene.wait(1)
    scene.play(
        Write(formula.next_to(cros_prob_final, DOWN, buff = 0.5)),
        run_time = 2
    )
    scene.wait(1)
    scene.play(
        reminder.animate.shift(UP * 10).set_opacity(0),
        cros_prob_final.animate.shift(UP * 10 + RIGHT * 10).set_opacity(0),
        formula.animate.shift(UP * 10 + LEFT * 10).set_opacity(0),
        Write(formula_without_arrow),
        Write(box_formula_without),
        run_time = 1.5
    )
    scene.wait(1)
    scene.play(
        t.animate.shift(DOWN * 20).set_opacity(0),
        formula_without_arrow.animate.shift(UP * 10).set_opacity(0),
        box_formula_without.animate.shift(UP * 10).set_opacity(0),
        run_time = 1.5
    )
    scene.wait(1)
    
    title = Text("Estimating π by dropping needles", color=BLUE_C) 
    title.to_edge(UP)
    scene.play(Write(title))
    scene.wait(1)

    # Needle drawing
    parallel_lines = VGroup(*[
        Line(
            [-6.4, y-0.8, 0],
            [-0.4, y-0.8, 0],
            color=WHITE,
            stroke_width=2,
        )
        for y in np.arange(5) * display_spacing
    ])

    # board_label = Text("Recent throws", font_size=20)
    # board_label.move_to([-3.4, 2.8, 0])

        # legend = VGroup(
        #     Text("Crossing", color=GREEN, font_size=18),
        #     Text("No crossing", color=GRAY_B, font_size=18),
        # ).arrange(RIGHT, buff=0.5)
        # legend.move_to([-3.4, -0.35, 0])

    #counter

    # parameters = MathTex(
    #     r"\ell=4,\qquad d=5",
    #     font_size=26,
    # ).move_to([3.3, 1.95, 0])

    counter_labels = VGroup(
        Text("Drops:", font_size=23).move_to([3.0, 2.35, 0]),
        Text("Crossings:", font_size=23).move_to([3.0, 1.8, 0]),
        Text("Estimate:", font_size=23).move_to([3.0, 1.25, 0]),
    )

    throws_counter = Integer(0, font_size=30)
    throws_counter.move_to([5.0, 2.35, 0])

    crossings_counter = Integer(0, font_size=30, color=GREEN)
    crossings_counter.move_to([5.0, 1.8, 0])

    estimate_counter = DecimalNumber(
        0,
        num_decimal_places=5,
        font_size=32,
        color=YELLOW,
    ).move_to([5.0, 1.25, 0])

    undefined_label = Text("--", font_size=30, color=YELLOW)
    undefined_label.move_to(estimate_counter)

    # reference_text = MathTex(
    #     r"\pi \approx 3.14159",
    #     font_size=26,
    #     color=TEAL,
    # ).move_to([3.3, -0.4, 0])

    scene.play(
        Create(parallel_lines),
        #FadeIn(board_label),
        #FadeIn(legend),
        #Write(formula),
        #Write(parameters),
        FadeIn(counter_labels),
        FadeIn(throws_counter),
        FadeIn(crossings_counter),
        FadeIn(undefined_label),
        #Write(reference_text),
    )
    scene.wait(1)

    # Expand the time axis and zoom vertically at two milestones.
    finite_estimates = estimates[np.isfinite(estimates)]
    graph_max = max(4, int(np.ceil(finite_estimates.max())) + 1)
    graph_stages = [
        (100, 0, graph_max, 1),
        (1000, 2.0, 4.5, 0.5),
        (total_throws, 2.8, 3.5, 0.1),
    ]
    current_stage = 0

    def make_axes(stage):
        maximum_n, minimum_y, maximum_y, step_y = graph_stages[stage]
        result = Axes(
            x_range=[0, maximum_n, maximum_n / 4],
            y_range=[minimum_y, maximum_y, step_y],
            x_length=11.6,
            y_length=2.0,
            tips=False,
            axis_config={"font_size": 21, "include_numbers": True},
            x_axis_config={
                "decimal_number_config": {"num_decimal_places": 0},
            },
            y_axis_config={
                "decimal_number_config": {
                    "num_decimal_places": 0 if stage == 0 else 1,
                },
            },
        )
        # Tick-label widths must not move the plotting area.
        result.shift(np.array([-5.8, -3.15, 0]) - result.c2p(0, minimum_y))
        return result

    def make_reference_line(target_axes, stage):
        return DashedLine(
            target_axes.c2p(0, PI),
            target_axes.c2p(graph_stages[stage][0], PI),
            color=TEAL,
            stroke_width=3,
            dash_length=0.12,
        )

    axes = make_axes(current_stage)
    reference_line = make_reference_line(axes, current_stage)
    pi_label = MathTex(r"\pi", color=TEAL, font_size=28)
    pi_label.next_to(reference_line, RIGHT, buff=0.12)
        # graph_title = Text("Running estimate of π", font_size=23)
        # graph_title.move_to([0, -0.8, 0])
    graph_x_label = Text("Number of drops", font_size=20)
    graph_x_label.move_to([0, -3.75, 0])

    scene.play(
        Create(axes),
        Create(reference_line),
        FadeIn(pi_label),
        # FadeIn(graph_title),
        FadeIn(graph_x_label),
    )

    # First 100 drops individually, then increasingly large batches.
    checkpoints = (
        list(range(1, 101))
        + list(range(120, 1001, 20))
        + list(range(1250, total_throws + 1, 250))
    )

    visible_needles = []
    curve = VMobject(color=YELLOW, stroke_width=2)
    graph_dot = Dot(radius=0.045, color=YELLOW)
    estimate_visible = False
    previous_n = 0

    for n in checkpoints:
        next_stage = 0 if n <= 100 else 1 if n <= 1000 else 2
        if next_stage != current_stage:
            scene.wait(1.5)
            new_axes = make_axes(next_stage)
            new_reference = make_reference_line(new_axes, next_stage)
            new_pi_label = MathTex(r"\pi", color=TEAL, font_size=28)
            new_pi_label.next_to(new_reference, RIGHT, buff=0.12)
            scene.remove(curve, graph_dot)
            scene.play(
                ReplacementTransform(axes, new_axes),
                ReplacementTransform(reference_line, new_reference),
                ReplacementTransform(pi_label, new_pi_label),
                run_time=1.5,
            )
            axes = new_axes
            reference_line = new_reference
            pi_label = new_pi_label
            current_stage = next_stage

        # Show the newest 20 needles of each batch.
        # Every drop contributes to the counters and the graph.
        first_visible = max(previous_n, n - 20)
        new_needles = VGroup()
        drop_animations = []

        for i in range(first_visible, n):
            center = np.array([centers_x[i], centers_y[i], 0])
            half_vector = display_length / 2 * np.array([
                np.cos(angles[i]),
                np.sin(angles[i]),
                0,
            ])

            needle = Line(
                center - half_vector,
                center + half_vector,
                color=WHITE,
                stroke_width=2.5,
            )
            new_needles.add(needle)
            drop_animations.append(
                needle_drop_animation(
                    needle,
                    GREEN if crossings[i] else GRAY_B,
                    tilt=(1 if i % 2 == 0 else -1) * 10 * DEGREES,
                    ceiling=title.get_bottom()[1] - 0.15,
                )
            )

        # Keep only the most recent displayed needles.
        for needle in visible_needles:
            needle.set_opacity(0.3)

        excess = max(0, len(visible_needles) + len(new_needles) - 80)
        if excess:
            scene.remove(*visible_needles[:excess])
            visible_needles = visible_needles[excess:]

        scene.add(*new_needles)
        scene.play(
            LaggedStart(*drop_animations, lag_ratio=0.025),
            run_time=0.7 if n <= 20 else 0.45 if n <= 100 else 0.45,
        )

        # Count the sampled result only after the needles have settled.
        throws_counter.set_value(n).move_to([5.0, 2.35, 0])
        crossings_counter.set_value(
            int(cumulative_crossings[n - 1])
        ).move_to([5.0, 1.8, 0])

        if cumulative_crossings[n - 1] > 0:
            estimate_counter.set_value(
                estimates[n - 1]
            ).move_to([5.0, 1.25, 0])

            if not estimate_visible:
                scene.remove(undefined_label)
                scene.add(estimate_counter)
                estimate_visible = True

            # Separate visible runs instead of flattening out-of-range values.
            _, minimum_y, maximum_y, _ = graph_stages[current_stage]
            values = estimates[:n]
            inside = (
                np.isfinite(values)
                & (values >= minimum_y)
                & (values <= maximum_y)
            )
            valid_indices = np.flatnonzero(inside)
            new_curve = VMobject(color=YELLOW, stroke_width=2.5)
            if len(valid_indices):
                breaks = np.flatnonzero(np.diff(valid_indices) > 1) + 1
                for run in np.split(valid_indices, breaks):
                    if len(run) < 2:
                        continue
                    points = [
                        axes.c2p(int(i + 1), float(values[i])) for i in run
                    ]
                    new_curve.start_new_path(points[0])
                    new_curve.add_points_as_corners(points[1:])
            scene.remove(curve)
            curve = new_curve
            scene.add(curve)
            if inside[-1]:
                graph_dot.move_to(axes.c2p(n, float(values[-1])))
                scene.add(graph_dot)
            else:
                scene.remove(graph_dot)

        scene.wait(0.15 if n <= 20 else 0.07)

        # Store individual needles so old ones can be removed cleanly.
        scene.remove(new_needles)
        scene.add(*new_needles)
        visible_needles.extend(new_needles)
        previous_n = n

    scene.wait(4)


class ProgressScene(Scene):
    def render(self, preview=False):
        first = config.from_animation_number
        last = config.upto_animation_number
        self._progress_first = first
        self._progress_last = last

        if np.isfinite(last):
            # Manim includes both endpoints of -n a,b.
            total = max(0, int(last) - first + 1)
        else:
            print("Counting animation steps...")
            with tempconfig({
                "dry_run": True,
                "preview": False,
                "progress_bar": "none",
                "verbosity": "ERROR",
                "from_animation_number": 0,
                "upto_animation_number": float("inf"),
            }):
                counter = Scene(skip_animations=True)
                self.construct.__func__(counter)
                total = max(0, counter.renderer.num_plays - first)

        description = "Selected animations" if first > 0 or np.isfinite(last) else "Whole scene"
        with tempconfig({
            "progress_bar": "none",
            "verbosity": "WARNING",
        }):
            with tqdm(
                total=total,
                desc=description,
                unit="step",
                dynamic_ncols=True,
                bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} [{elapsed} | {remaining}]",
            ) as bar:
                self._overall_progress = bar
                try:
                    result = super().render(preview=preview)
                    # The scene may end before the requested upper limit.
                    if bar.n < total:
                        bar.total = bar.n
                        bar.refresh()
                    return result
                finally:
                    self._overall_progress = None

    def play(self, *args, **kwargs):
        animation_number = self.renderer.num_plays
        result = super().play(*args, **kwargs)
        bar = getattr(self, "_overall_progress", None)
        if (
            bar is not None
            and self._progress_first <= animation_number <= self._progress_last
            and self.renderer.num_plays > animation_number
        ):
            bar.update(1)
        return result

# Main scene that plays everything
class FullScene(ProgressScene): 
    def construct(self):
        run_intro = True
        run_draw_lines = True  # If you want to run some of the created functions, set True for the
        run_dif_need = True   # preferred ones and False for the others
        run_prob_calc = True
        run_monte_carlo = True

        if run_intro:
            intro_animation(self)
        if run_draw_lines:
            draw_parallel_lines(self)
        if run_dif_need:
            different_needles(self)
        if run_prob_calc:
            probability_calculations(self)
        if run_monte_carlo:
            monte_carlo_simulation(self)     

class IntroScene(ProgressScene):
    def construct(self):
        intro_animation(self)

class CrossingRuleScene(ProgressScene):
    def construct(self):
        draw_parallel_lines(self)

class  ThreeNeedlesScene(ProgressScene):
    def construct(self):
        different_needles(self)

class ProbCalcScene(ProgressScene):
    def construct(self):
        probability_calculations(self)

class MonteCarloScene(ProgressScene):
    def construct(self):
        monte_carlo_simulation(self)
