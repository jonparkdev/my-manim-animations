from manimlib.imports import *
from my_animations.utils.operations import get_circle_intersection

class Intro(Scene):
    pass

class Problem(Scene):
    pass

class ConstructionProof(Scene):
    CONFIG = {
        "point_color": BLACK,
    }
    def construct(self):
        self.construction()
        self.wait(5)

    def construction(self):
        # Construct all mobjects needed
        given_point_mob = Dot(DOWN + (UP+RIGHT), color=BLACK)
        given_line_point_a_mob = Dot(DOWN + ((2 * LEFT)+UP), color=BLACK)
        given_line_point_b_mob = Dot(DOWN)
        given_line_mob = Line(DOWN, DOWN + ((2 * LEFT)+UP), stroke_width=6, color=BLACK)
        dotted_line_mob = DashedLine(
            given_line_point_b_mob,
            given_point_mob,
            stroke_width=6,
            color=BLACK
        )
        circle_about_given_line_point_a_mob = Circle(
            radius=given_line_mob.get_length(),
            stroke_width=6,
            arc_center=given_line_point_b_mob.get_center(),
            color=BYRNE_BLUE
        )

        # returns [intersection_1, intersection_2]
        proposition_one_point_c = get_circle_intersection(
            given_point_mob.get_center(),
            given_line_point_b_mob.get_center(),
            given_line_mob.get_length(),
            given_line_mob.get_length(),
        )
        point_c_mob = Dot(proposition_one_point_c[0], color=BLACK)

        self.add(point_c_mob)
        self.add(given_line_mob)
        self.add(given_point_mob)
        self.add(dotted_line_mob)
        self.add(circle_about_given_line_point_a_mob)
