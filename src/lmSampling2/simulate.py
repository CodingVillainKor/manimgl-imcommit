from manimlib import *


class BrownianBox(VGroup):
    """
    Square container with particles in constant Brownian (Langevin) motion.

    Each particle follows an Ornstein-Uhlenbeck velocity process
        dv = -gamma * v * dt + sqrt(2 * gamma * T) * dW
    so the typical speed grows as sqrt(T) and the motion keeps jittering
    randomly. Walls reflect particles elastically.

    Usage:
        temp = ValueTracker(1.0)
        box = BrownianBox(temp)
        self.add(box)
        self.play(temp.animate.set_value(5.0))  # particles speed up
    """

    def __init__(
        self,
        temp: ValueTracker,
        n_particles: int = 40,
        side_length: float = 3.0,
        dot_radius: float = 0.05,
        dot_color=BLUE_B,
        box_color=GREY_B,
        gamma: float = 3.0,
        speed_scale: float = 1.0,
        max_dt: float = 1 / 30,
        seed: int | None = 0,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.temp = temp
        self.gamma = gamma
        self.speed_scale = speed_scale
        self.max_dt = max_dt
        self.rng = np.random.default_rng(seed)

        self.box = Square(side_length=side_length).set_stroke(box_color, width=2)
        self.half = side_length / 2 - dot_radius

        # positions/velocities are stored relative to the box center, so the
        # whole group can be moved around freely
        self.pos = self.rng.uniform(-self.half, self.half, size=(n_particles, 2))
        self.vel = self.rng.normal(0, self._sigma_v(), size=(n_particles, 2))

        self.dots = VGroup(
            *[Dot(radius=dot_radius, fill_color=dot_color) for _ in range(n_particles)]
        )
        self.add(self.box, self.dots)
        self._place_dots()
        self.dots.add_updater(lambda m, dt: self._step(dt))

    def _sigma_v(self) -> float:
        # equilibrium speed std of the OU process: sqrt(T)
        return self.speed_scale * np.sqrt(max(self.temp.get_value(), 0.0))

    def _place_dots(self):
        center = self.box.get_center()
        for dot, (x, y) in zip(self.dots, self.pos):
            dot.move_to(center + np.array([x, y, 0.0]))

    def _step(self, dt: float):
        if dt <= 0:
            return
        # clamp so a long frame (interactive lag) doesn't teleport particles
        dt = min(dt, self.max_dt)

        noise = self.rng.normal(size=self.vel.shape)
        self.vel += -self.gamma * self.vel * dt + (
            np.sqrt(2 * self.gamma * dt) * self._sigma_v() * noise
        )
        self.pos += self.vel * dt

        # reflect off walls
        for axis in range(2):
            over = self.pos[:, axis] > self.half
            under = self.pos[:, axis] < -self.half
            self.pos[over, axis] = 2 * self.half - self.pos[over, axis]
            self.pos[under, axis] = -2 * self.half - self.pos[under, axis]
            self.vel[over | under, axis] *= -1
        # very fast particles can overshoot past the opposite wall
        np.clip(self.pos, -self.half, self.half, out=self.pos)

        self._place_dots()
