from manimlib.imports import *

class SceneOne(Scene):

    def construct(self):
        self.title_sequence()
        self.wait()


    def title_sequence(self):
        title = TextMobject("Euclid's Elements").scale(2)
        book = TextMobject("Book ").scale(1.5)
        proposition = TextMobject("Proposition ").scale(1.5)

        book_number = Integer(13).scale(1.5).next_to(book, RIGHT)
        proposition_number = Integer(465).scale(1.5).next_to(proposition, RIGHT)

        book_group = VGroup(book, book_number)
        proposition_group = VGroup(proposition, proposition_number).next_to(book_group, DOWN)

        anim_group = VGroup(book_group, proposition_group).move_to(ORIGIN)

        def animate_numbers(low_num, high_num, final_num):
            def func(alpha):
                if(alpha == 1):
                    return final_num
                return np.random.uniform(low_num, high_num)
            return func
        self.play(Write(title), run_time=2)
        self.wait(3)
        self.play(
            ReplacementTransform(title,anim_group),
        )
        self.play(
            ChangingDecimal(book_number, animate_numbers(1, 13, 1)).set_run_time(2),
            ChangingDecimal(proposition_number, animate_numbers(1, 465, 1)).set_run_time(3)
        )
        self.wait(1)
        self.play(FadeOut(anim_group))

    def scene_two(self):
        pass

class Problem(Scene):

    def construct(self):
        self.move_line()

    def move_line(self):
        point_a = self.a = Dot(LEFT, color=BLACK)
        point_b = self.b =  Dot(RIGHT, color=BLACK)

        line = self.initial_line = Line(point_a, point_b, stroke_width=6, color=BLACK)
        self.wait()
        self.play(FadeIn(line),FadeIn(point_a),FadeIn(point_b))
        self.wait()
        self.move_points()


    def move_points(self):
        np.random.seed(41)
        movement_list_a = list(
            zip(
                np.random.random(4)*negative_or_positive(2),
                np.random.random(4)*negative_or_positive(2),
                [0, 0, 0, 0]
            )
        )
        np.random.seed(42)
        movement_list_b = list(
            zip(
                np.random.random(4)*negative_or_positive(2),
                np.random.random(4)*negative_or_positive(2),
                [0, 0, 0, 0]
            )
        )
        count = 0
        for a, b in zip(movement_list_a,movement_list_b):

            if count % 2 == 0:
                array_a = np.array(a) * -1
                array_b = np.array(b) * -1
            else:
                array_a = np.array(a)
                array_b = np.array(b)

            count = count + 1

            self.play(
                ApplyMethod(
                    self.initial_line.put_start_and_end_on,
                    array_a,
                    array_b
                ),
                ApplyMethod(self.a.move_to, array_a),
                ApplyMethod(self.b.move_to, array_b)
            )
            self.wait()
            length = self.initial_line.get_length()
            left = self.a.get_center()
            right = self.b.get_center()

            positive_intersection, negative_intersection = get_circle_intersection(left, right, length, length)

            if np.linalg.norm(positive_intersection) < np.linalg.norm(positive_intersection):
                triangle_point = positive_intersection
            else:
                triangle_point = negative_intersection

            triangle_point_mob=  Dot(triangle_point, color=BLACK)
            line_with_a= Line(self.a, triangle_point_mob, stroke_width=6)
            line_with_b= Line(self.b, triangle_point_mob, stroke_width=6)
            triangle = Polygon(
                triangle_point,
                left,
                right
            ).set_stroke(color=None, width=0)
            triangle.set_fill(BLACK, opacity = 0.5)

            self.play(
                FadeIn(triangle),
                FadeIn(triangle_point_mob),
                FadeIn(line_with_a),
                FadeIn(line_with_b)
            )
            self.play(
                FadeOut(triangle),
                FadeOut(triangle_point_mob),
                FadeOut(line_with_a),
                FadeOut(line_with_b)
            )

        self.play(
            ApplyMethod(
                self.initial_line.put_start_and_end_on,
                LEFT,
                RIGHT
            ),
            ApplyMethod(self.a.move_to, LEFT),
            ApplyMethod(self.b.move_to, RIGHT)
        )

        self.wait()

        self.play(Uncreate(self.initial_line))
        self.wait()


        # animations = [
        #     self.update_point_mob(self.a, movement) for movement in movement_list
        # ]
        # for anim in animations:
        #     self.play(anim)



class Construction(Scene):
    CONFIG = {
        "left_circle_center" : LEFT,
        "right_circle_center" : RIGHT,
        "random_seed" : 4,
        "radius" : 2,
        "point_color" : BLACK,
    }

    def construct(self):
        self.initial_line()

    def initial_line(self):
        # create objects
        radius_a = DashedLine(LEFT, RIGHT, color=BLACK)
        radius_b = DashedLine(RIGHT, LEFT, color=BLACK).flip(LEFT)

        positive_intersection, negative_intersection = get_circle_intersection(LEFT, RIGHT, self.radius, self.radius)
        point_c = Dot(positive_intersection, color=self.point_color)
        line_ab = Line(LEFT, RIGHT, stroke_width=6, color=self.point_color)

        circle_about_a = Circle(radius=self.radius, stroke_width=6,arc_center=LEFT, color=BYRNE_BLUE)
        point_a = self.point_a = Dot(LEFT , color=self.point_color)
        line_ac = Line(LEFT, point_c,stroke_width=6, color=BYRNE_YELLOW)


        circle_about_b = Circle(radius=self.radius,stroke_width=6, arc_center=RIGHT, color=BYRNE_RED).flip()
        point_b = Dot(RIGHT, color=self.point_color)
        line_bc = Line(RIGHT, point_c,stroke_width=6, color=BYRNE_RED)

        a_group = VGroup(
            circle_about_a,
            line_ac,
            point_c,
            line_ab,
            point_b.copy(),
            point_a,
            )
        b_group = VGroup(
            circle_about_b,
            line_bc,
            point_c.copy(),
            point_a.copy(),
            line_ab.copy(),
            point_b,
            )

        self.add(point_a)
        self.add(point_b)
        self.wait()

        # Construct circle about point A
        self.play(ShowCreation(radius_a))
        self.play(
            ShowCreation(circle_about_a),
            Rotating(radius_a, angle = 2*np.pi, about_point = LEFT),
            rate_func = smooth,
            run_time = 2,
        )
        self.play(ShowCreation(
            radius_a,
            rate_func = lambda t: smooth(1-t),
            remover = True
        ))
        # Construct circle about point B
        self.play(ShowCreation(radius_b))
        self.play(
            ShowCreation(circle_about_b),
            Rotating(radius_b, axis = IN, angle = 2*np.pi, about_point = RIGHT),
            rate_func = smooth,
            run_time = 2,
        )
        self.play(ShowCreation(
            radius_b,
            rate_func = lambda t: smooth(1-t),
            remover = True
        ))
        # Add initial line back
        self.play(ShowCreation(line_ab))

        # construct new lines
        self.play(FadeIn(point_c))
        self.play(ShowCreation(line_ac))
        self.play(ShowCreation(line_bc))

        self.play(
            ApplyMethod(a_group.shift, LEFT * 1.5),
            ApplyMethod(b_group.shift, RIGHT * 1.5)
        )

        # self.play(ApplyMethod(b_group.flip, UP))

        # compass animation
        self.play(Uncreate(line_ab))
        compass_point = point_a.get_center() + RIGHT * self.radius
        compass_point_mob = self.compass_point_mob = Dot(compass_point, color=BLACK)
        compass_line = self.compass_line =  DashedLine(point_a.get_center(), compass_point_mob)
        line_ac_angle = (np.pi/2) - angle_of_vector(point_c.get_center() - point_a.get_center())
        n_thetas = [-np.pi/2]*3 + [-line_ac_angle]

        self.play(ShowCreation(compass_line))
        self.play(FadeIn(compass_point_mob))

        self.change_points(n_thetas , point_a.get_center())
        # fade_lines = [FadeOut(line) for line, point in self.example_lines]
        remove_example_lines = [FadeOut(mob) for mob in it.chain(*self.example_lines)]
        self.play(*remove_example_lines)
        self.remove_compass(n_thetas, point_a.get_center())

        self.play(Uncreate(self.compass_line))
        print(line_ab.get_center())

        self.wait()

    '''
    Helper functions
    '''

    def get_compass_point_update(self, pm, d_theta, circle_center,func=smooth, run=1):
        current_theta = angle_of_vector(pm.get_center() - circle_center)
        new_theta = current_theta + d_theta
        def update_point(point_mob, alpha):
            theta = interpolate(current_theta, new_theta, alpha)
            point_mob.move_to(circle_center + self.radius * (
                np.cos(theta)*RIGHT + np.sin(theta)*UP
            ))
            return point_mob
        return UpdateFromAlphaFunc(pm, update_point, rate_func=func, run_time=run)

    def get_compass_update(self, circle_center):
        def update_compass(line):
            point = self.compass_point_mob.get_center() - circle_center
            line.rotate(
                (angle_of_vector(point) - line.get_angle()),
                about_point=circle_center
            )
            return line
        return UpdateFromFunc(self.compass_line, update_compass, rate_func=smooth)

    def change_points(self, n_thetas, circle_center):
        self.example_lines = []
        example_line = DashedLine(circle_center, self.compass_point_mob, color=BLACK)
        example_point = Dot(self.compass_point_mob.get_center(), color=BLACK)
        self.example_lines.append((example_line,example_point))
        self.add(example_line, example_point, self.point_a)

        for theta in n_thetas:
            self.play(
                self.get_compass_point_update(
                    self.compass_point_mob, theta , circle_center
                ),
                self.get_compass_update(circle_center)
            )
            example_line = DashedLine(circle_center, self.compass_point_mob, color=BLACK)
            example_point = Dot(self.compass_point_mob.get_center(), color=BLACK)
            self.example_lines.append((example_line,example_point))
            self.add(example_line, example_point, self.point_a)


    def remove_compass(self, n_thetas, circle_center):
        # total_theta = -sum(n_thetas)
        self.example_lines
        theta = sum(n_thetas)
        self.play(
            self.get_compass_point_update(
                self.compass_point_mob, -theta , circle_center
            ),
            self.get_compass_update(circle_center),
        )

    def pop_lines(self, circle_center):
        def pop(mobject, alpha):

            point = angle_of_vector(self.compass_point_mob.get_center() - circle_center)
            d_theta = (point+ np.pi)%(2*np.pi) - np.pi
            print(d_theta, mobject.get_angle())
            if point >= mobject.get_angle():
                print('here')
                FadeOut(mobject)
            return mobject
        return UpdateFromAlphaFunc(self.example_lines[3], pop,rate_func=smooth, run_time=1)


    def get_point_mobs(self, origin):
        points = np.array([
            origin + rotate_vector(self.radius*RIGHT, theta)
            for theta in np.random.uniform(np.pi/2, 7 * np.pi/8, size=3)
        ])
        point_mobs = self.point_mobs = VGroup(*[
            Dot().move_to(point) for point in points
        ])
        point_mobs.set_color(self.point_color)
        return point_mobs

def negative_or_positive(max_num):

    return max_num * 1 if np.random.random() < 0.5 else -1 * max_num

def get_circle_intersection(origin_a, origin_b, r_1, r_2):
    """(numpy R^3 array, numpy R^3 array, float, float) -> numpy R^3 array

    Returns the intersection point(s) of two circles given the origin
    coordinates,origin_a and origin_b, of each circle and radii r_1, r_2

    pre-conditions:
        - The two given circles intersect at > 0 points
    """
    # For now we will be working in 2D space and will ignore the z
    # coordinate

    x_1, y_1, z_1 = origin_a
    x_2, y_2, z_2 = origin_b

    """
    Our algorithm,
    Strictly using algebraic equations of our circles,

        (1) (x-x_1)^2 + (y-y_1)^2 = r_1^2
        (2) (x-x_2)^2 + (y-y_2)^2 = r_2^2

    Subtracting (2) from (1) and magically rearranging we get,

        y = -[(x_1 - x_2)/(y_1 - y_2)]x +
            [(r_1^2-r_2^2)-(x_1^2-x_2^2)-(y_1^2-y_2^2)] / (y_1 - y_2)

            let v = [(r_1^2-r_2^2)-(x_1^2-x_2^2)-(y_1^2-y_2^2)] / -2 * (y_1 - y_2) so,

        (3) y =  -[(x_1 - x_2)/(y_1 - y_2)]x + v

    Substituting our y back into (1) and some more algebra we get the
    quadratic (if your thinking, that looks tedious, you are correct):

        (x-x_1)^2 + (-[(x_1 - x_2)/(y_1 - y_2)]x + v - y_1)^2 = r_1^2
        .
        .
        .
        Some quadratic formula

    Then use quadratic formula to solve for x, then use x in (3) to solve
    for y
    """

    # if origins of the two circles fall on the same axis
    if y_1 == y_2 and x_1 == x_2:
        raise ValueError("circles cannot be centred on the same origin")
    elif y_1 == y_2:
        # Denoting constant values in above formulas
        constant = (y_1-y_2)/(x_1-x_2)
        v = ((r_1**2-r_2**2)-(x_1**2-x_2**2)-(y_1**2-y_2**2)) / ((-2) * (x_1 - x_2))
        root = 'y'
    else:
        # Denoting constant values in above formulas
        constant = (x_1-x_2)/(y_1-y_2)
        v = ((r_1**2-r_2**2)-(x_1**2-x_2**2)-(y_1**2-y_2**2)) / ((-2) * (y_1 - y_2))
        root = 'x'

    if (root == 'x'):
         # quadratic formula to find roots along the x-axis
        a = (1.0 + constant**2)
        b = (-2) * (x_1 + (constant * (v - y_1)))
        c = x_1**2 + (v - y_1)**2  - r_1**2
        positive_x = ((-b) + np.sqrt(b**2 - 4*a*c)) / (2 * a)
        negative_x = ((-b) - np.sqrt(b**2 - 4*a*c)) / (2 * a)
        positive_y = (-constant) * positive_x + v
        negative_y = (-constant) * negative_x + v

    else:
        # quadratic formula to find the roots along the y-axis
        a = (1 + constant**2)
        b = -2 * (y_1 + (constant * (v - x_1)))
        c = y_1**2 + (v - x_1)**2  - r_1**2
        y = (-b + np.sqrt(b**2 - 4*a*c)) / 2 * a
        x = -(constant) * y + v
        positive_y = ((-b) + np.sqrt(b**2 - 4*a*c)) / (2 * a)
        negative_y = ((-b) - np.sqrt(b**2 - 4*a*c)) / (2 * a)
        positive_x = (-constant) * positive_y + v
        negative_x = (-constant) * negative_y + v

    return [np.array((positive_x, positive_y, 0)), np.array((negative_x, negative_y, 0))]
