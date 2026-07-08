from panda3d.core import *
import math

from config import (
    DEFAULT_SPIN, DEFAULT_LENSING_ON, DEFAULT_DOPPLER_ON,
    DEFAULT_REDSHIFT_ON, DEFAULT_JET_POWER, DEFAULT_DISK_R,
    DEFAULT_THICKNESS, DEFAULT_DENSITY, DEFAULT_MASS, DEFAULT_QUALITY,
    FOV, DEFAULT_JETS_ON, DEFAULT_TEMP,
)

# Disk reference temperature — hotter core (near-white/blue) fading to
# orange at the outer edge, matching the reference "halo" look.
DISK_TEMP = DEFAULT_TEMP


class BHRenderer:
    """
    Fullscreen ray-traced black hole renderer.

    Controls
    --------
    Left-drag          : orbit  (azimuth ph, elevation th)
    Right-drag up/down : zoom   (observer radius r)
    Scroll wheel       : zoom   (fast, 18 % per tick)
    Arrow keys ← →     : orbit left / right
    Arrow keys ↑ ↓     : orbit up / down
    W / S              : zoom in / out (smooth)
    = / -              : zoom in / out (smooth)
    """

    def __init__(self, base):
        self.base  = base
        self._time = 0.0

        # ── Boyer-Lindquist observer position ──────────────────
        # Higher elevation + a bit more distance so the lensed disk wraps
        # into the full "halo" silhouette instead of filling the frame
        # like a grazing-angle floor.
        self._r  = 42.0
        self._th = math.pi / 2.0 - 0.55   # ~31.5 ° above the disk plane
        self._ph = 0.0
        self._fov = FOV
        self._wobble_intensity = 0.0

        # ── Input state ────────────────────────────────────────
        self._mouse_down  = False
        self._last_mouse  = None          # (x, y) from previous frame

        self._keys = {
            "arrow_left":  False,
            "arrow_right": False,
            "arrow_up":    False,
            "arrow_down":  False,
            "equal":       False,   # zoom in  ( = / + key )
            "minus":       False,   # zoom out
            "w":           False,   # zoom in
            "s":           False,   # zoom out
        }

        # Right mouse button for drag-to-zoom
        self._rmouse_down = False
        self._last_rmouse = None

        # Mouse buttons — left = orbit, right = zoom
        base.accept("mouse1",    self._mouse_down_cb)
        base.accept("mouse1-up", self._mouse_up_cb)
        base.accept("mouse3",    self._rmouse_down_cb)
        base.accept("mouse3-up", self._rmouse_up_cb)

        # Scroll wheel — 18 % per tick for a satisfying snap
        base.accept("wheel_up",   self._zoom_in)
        base.accept("wheel_down", self._zoom_out)

        # Keyboard orbit / zoom
        for k in self._keys:
            base.accept(k,        self._set_key, [k, True])
            base.accept(k + "-up", self._set_key, [k, False])

        # ── Offscreen Texture Buffer for Constant High FPS (RTT) ──
        # Fixed resolution (e.g., 1280x720) to guarantee fast raymarching even on full screen expansion
        self.buf_w = 1280
        self.buf_h = 720
        self.buffer = base.win.makeTextureBuffer("BHBuffer", self.buf_w, self.buf_h)
        self.buffer.setClearColor(Vec4(0, 0, 0, 1))

        # Create a private 2D scene graph for the buffer
        self.buffer_render2d = NodePath("buffer_render2d")
        
        # Create camera node manually to avoid inheriting any base camera2d transforms
        cam_node = Camera("BHBufferCam")
        self.buffer_cam = self.buffer_render2d.attachNewNode(cam_node)
        cam_node.setScene(self.buffer_render2d)
        
        # Configure a clean orthographic lens
        lens = OrthographicLens()
        lens.setFilmSize(2, 2)
        lens.setNearFar(-10, 10)
        cam_node.setLens(lens)
        
        # Position camera looking directly at the 2D plane
        self.buffer_cam.setPos(0, -5, 0)
        self.buffer_cam.lookAt(0, 0, 0)
        
        # Associate camera with the buffer's display region
        dr = self.buffer.makeDisplayRegion()
        dr.setCamera(self.buffer_cam)
        
        cm = CardMaker("BHCard")
        cm.setFrame(-1, 1, -1, 1)
        self.card = self.buffer_render2d.attachNewNode(cm.generate())

        shader = Shader.load(
            Shader.SL_GLSL,
            vertex="shaders/blackhole.vert",
            fragment="shaders/blackhole.frag",
        )
        self.card.setShader(shader)

        # Apply texture of offscreen buffer to a quad in render2d to render full screen
        tex = self.buffer.getTexture()
        tex.setMinfilter(SamplerState.FT_linear)
        tex.setMagfilter(SamplerState.FT_linear)
        
        self.display_card = base.render2d.attachNewNode(cm.generate())
        self.display_card.setTexture(tex)

        # ── Static shader uniforms ──────────────────────────────
        steps = {"low": 150, "med": 400, "high": 600}.get(DEFAULT_QUALITY, 400)

        self.card.setShaderInput("u_resolution",     Vec2(self.buf_w, self.buf_h))
        self.card.setShaderInput("u_quality_steps",  steps)
        self.card.setShaderInput("u_spin",           DEFAULT_SPIN)
        self.card.setShaderInput("u_lensing",        1.0 if DEFAULT_LENSING_ON  else 0.0)
        self.card.setShaderInput("u_doppler",        1.0 if DEFAULT_DOPPLER_ON  else 0.0)
        self.card.setShaderInput("u_redshift",       1.0 if DEFAULT_REDSHIFT_ON else 0.0)
        self.card.setShaderInput("u_jets",           1.0 if DEFAULT_JETS_ON else 0.0)
        self.card.setShaderInput("u_jet_power",      DEFAULT_JET_POWER)
        self.card.setShaderInput("u_disk_r_out",     DEFAULT_DISK_R)
        self.card.setShaderInput("u_disk_thickness", DEFAULT_THICKNESS)
        self.card.setShaderInput("u_disk_temp",      DISK_TEMP)
        self.card.setShaderInput("u_opt_density",    DEFAULT_DENSITY)
        self.card.setShaderInput("u_mass",           DEFAULT_MASS)
        self.card.setShaderInput("u_wobble",         0.0)
        self.card.setShaderInput("u_quality_steps",  steps)
        
        # Dynamically set initial resolution and step count
        self._push_camera()

        # ── Physics Guide HUD ───────────────────────────────────
        from engine.objects.physics_guide import PhysicsGuide
        self.physics_guide = PhysicsGuide(base)
        base.accept("h", self.physics_guide.toggle)

    # ── Input callbacks ─────────────────────────────────────────

    def _mouse_down_cb(self):
        self._mouse_down = True
        self._last_mouse = None

    def _mouse_up_cb(self):
        self._mouse_down = False
        self._last_mouse = None

    def _rmouse_down_cb(self):
        self._rmouse_down = True
        self._last_rmouse = None

    def _rmouse_up_cb(self):
        self._rmouse_down = False
        self._last_rmouse = None

    def _zoom_in(self):
        """One scroll tick: zoom in (decrease FOV) or dolly closer if Shift is held."""
        is_shift = False
        if self.base.mouseWatcherNode.hasMouse():
            is_shift = self.base.mouseWatcherNode.isButtonDown(KeyboardButton.shift())

        if is_shift:
            self._r = max(3.5, self._r * 0.82)
        else:
            self._fov = max(2.0, self._fov * 0.85)
        # Wobble slightly on scroll zoom
        self._wobble_intensity = min(self._wobble_intensity + 0.35, 1.0)

    def _zoom_out(self):
        """One scroll tick: zoom out (increase FOV) or dolly farther if Shift is held."""
        is_shift = False
        if self.base.mouseWatcherNode.hasMouse():
            is_shift = self.base.mouseWatcherNode.isButtonDown(KeyboardButton.shift())

        if is_shift:
            self._r = min(300.0, self._r * 1.18)
        else:
            self._fov = min(120.0, self._fov * 1.15)
        # Wobble slightly on scroll zoom
        self._wobble_intensity = min(self._wobble_intensity + 0.35, 1.0)

    def _set_key(self, key, val):
        self._keys[key] = val

    # ── Per-frame update ────────────────────────────────────────

    def update(self, dt):
        self._time += dt

        prev_ph = self._ph
        prev_th = self._th

        # --- Mouse-drag orbit (left button) ---
        if self._mouse_down and self.base.mouseWatcherNode.hasMouse():
            mx = self.base.mouseWatcherNode.getMouseX()
            my = self.base.mouseWatcherNode.getMouseY()
            if self._last_mouse is not None:
                dx = mx - self._last_mouse[0]
                dy = my - self._last_mouse[1]
                self._ph += dx * 2.5
                self._th  = max(0.04, min(math.pi - 0.04,
                                          self._th - dy * 2.0))
            self._last_mouse = (mx, my)
        else:
            self._last_mouse = None

        is_shift = False
        if self.base.mouseWatcherNode.hasMouse():
            is_shift = self.base.mouseWatcherNode.isButtonDown(KeyboardButton.shift())

        # --- Right-drag zoom (drag up = zoom in) ---
        if self._rmouse_down and self.base.mouseWatcherNode.hasMouse():
            mx = self.base.mouseWatcherNode.getMouseX()
            my = self.base.mouseWatcherNode.getMouseY()
            if self._last_rmouse is not None:
                dy = my - self._last_rmouse[1]
                # dy > 0 → dragged up → zoom in
                zoom_factor = 1.0 - dy * 3.5
                if is_shift:
                    self._r = max(3.5, min(300.0, self._r * zoom_factor))
                else:
                    self._fov = max(2.0, min(120.0, self._fov * zoom_factor))
            self._last_rmouse = (mx, my)
        else:
            self._last_rmouse = None

        # --- Keyboard orbit + zoom ---
        orbit_speed = 1.0    # rad / s
        zoom_speed  = 18.0   # % per second

        if self._keys["arrow_left"]:
            self._ph -= orbit_speed * dt
        if self._keys["arrow_right"]:
            self._ph += orbit_speed * dt
        if self._keys["arrow_up"]:
            self._th = max(0.04, self._th - orbit_speed * dt)
        if self._keys["arrow_down"]:
            self._th = min(math.pi - 0.04, self._th + orbit_speed * dt)

        # W / = → zoom in,  S / - → zoom out
        if self._keys["w"] or self._keys["equal"]:
            if is_shift:
                self._r = max(3.5, self._r * (1.0 - zoom_speed * dt * 0.08))
            else:
                self._fov = max(2.0, self._fov * (1.0 - zoom_speed * dt * 0.08))
        if self._keys["s"] or self._keys["minus"]:
            if is_shift:
                self._r = min(300.0, self._r * (1.0 + zoom_speed * dt * 0.08))
            else:
                self._fov = min(120.0, self._fov * (1.0 + zoom_speed * dt * 0.08))

        # Track camera changes to compute dynamic wobble intensity
        d_ph = self._ph - prev_ph
        d_th = self._th - prev_th
        rot_speed = math.sqrt(d_ph * d_ph + d_th * d_th) / dt if dt > 0.0 else 0.0
        
        target_wobble = min(rot_speed * 0.15, 1.0)
        if target_wobble > self._wobble_intensity:
            self._wobble_intensity = target_wobble
        else:
            # Smooth exponential decay
            self._wobble_intensity += (target_wobble - self._wobble_intensity) * dt * 8.0
        self._push_camera()
        if hasattr(self.base, "physics_guide") and self.base.physics_guide:
            self.base.physics_guide.update()

    def _push_camera(self):
        """Send current BL observer position + time to the shader."""
        self.card.setShaderInput("u_time",   self._time)
        self.card.setShaderInput("u_cam_r",  self._r)
        self.card.setShaderInput("u_cam_th", self._th)
        self.card.setShaderInput("u_cam_ph", self._ph)
        self.card.setShaderInput("u_fov",    math.radians(self._fov))
        self.card.setShaderInput("u_wobble", self._wobble_intensity)
        

