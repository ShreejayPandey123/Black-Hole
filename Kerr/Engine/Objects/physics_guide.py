from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectButton, DGG
import math

class PhysicsGuide:
    """
    Richer interactive physics guide that combines:
    1. Floating label buttons and pointer arrows on the left pointing to the 3D black hole.
    2. A detailed physics explanation sidebar on the right.
    Selecting any feature (either by clicking the floating buttons or the sidebar headings)
    highlights the pointer arrow, pulses the target zone, and highlights the description text.
    """

    # Target points on the black hole in aspect2d coordinates (x, z)
    _TARGETS = {
        "jet":         (0.01, 0.45),    # upper jet column
        "photon":      (-0.16, 0.12),   # photon ring outer boundary
        "horizon":     (-0.06, 0.04),   # event horizon shadow
        "singularity": (0.00, 0.00),    # center of the black hole
        "disk":        (-0.35, -0.10),  # main accretion disk plane
        "isco":        (-0.25, -0.06),  # innermost stable circular orbit edge
    }

    def __init__(self, base):
        self.base = base
        self.visible = True
        self.active_part = "horizon"

        # List of elements we toggle visibility on
        self._nodes = []

        # ── Bottom-Left Hint ─────────────────────────────────────────
        self.hint = OnscreenText(
            text="[H] Toggle Guide  |  Click any part label to inspect details",
            pos=(0.05, 0.05), scale=0.030,
            fg=(1, 1, 1, 0.70), shadow=(0, 0, 0, 0.7),
            align=TextNode.ALeft, parent=base.a2dBottomLeft
        )

        # ── Right-Side Detailed Sidebar Panel ────────────────────────
        cm = CardMaker("guide_bg")
        cm.setFrame(-0.92, -0.01, -1.98, -0.01)
        self.bg = base.a2dTopRight.attachNewNode(cm.generate())
        self.bg.setColor(0.02, 0.02, 0.03, 0.92)
        self.bg.setTransparency(TransparencyAttrib.MAlpha)
        self._nodes.append(self.bg)

        # Orange left accent bar
        bar = CardMaker("guide_bar")
        bar.setFrame(-0.925, -0.908, -1.98, -0.01)
        b = self.bg.attachNewNode(bar.generate())
        b.setColor(0.9, 0.40, 0.0, 1.0)
        b.setTransparency(TransparencyAttrib.MAlpha)

        # Attempt to load premium system fonts (Windows)
        self.font_body = None
        self.font_math = None
        try:
            segoe = base.loader.loadFont("/c/Windows/Fonts/segoeui.ttf")
            if segoe.isValid():
                self.font_body = segoe
                self.font_math = segoe  # Safe default fallback
            
            # Try to get italic math fonts
            math_f = base.loader.loadFont("/c/Windows/Fonts/segoeuii.ttf")
            if not math_f.isValid():
                math_f = base.loader.loadFont("/c/Windows/Fonts/timesi.ttf")
            if math_f.isValid():
                self.font_math = math_f
        except:
            pass

        wrap = 28.0

        # Sidebar Title
        self.title_text = OnscreenText(
            text="KERR BLACK HOLE  |  PHYSICS GUIDE",
            pos=(-0.86, -0.09), scale=0.042, fg=(1.0, 0.46, 0.0, 1.0),
            align=TextNode.ALeft, parent=self.bg
        )

        def sep(y):
            s = CardMaker("sep")
            s.setFrame(-0.88, -0.04, y - 0.003, y + 0.003)
            n = self.bg.attachNewNode(s.generate())
            n.setColor(0.9, 0.40, 0.0, 0.30)
            n.setTransparency(TransparencyAttrib.MAlpha)

        sep(-0.155)

        # We will dynamically populate the description fields based on selection
        self.desc_title = OnscreenText(
            text="", pos=(-0.86, -0.21), scale=0.038, fg=(1.0, 0.70, 0.2, 1.0),
            shadow=(0, 0, 0, 0.8), align=TextNode.ALeft, parent=self.bg,
            font=self.font_body
        )
        self.desc_body = OnscreenText(
            text="", pos=(-0.86, -0.28), scale=0.028, fg=(0.9, 0.9, 0.95, 1.0),
            shadow=(0, 0, 0, 0.5), align=TextNode.ALeft, parent=self.bg, wordwrap=wrap,
            font=self.font_body
        )

        # Math section background block
        mbg = CardMaker("math_bg")
        mbg.setFrame(-0.88, -0.04, -0.42, 0.0)  # Local frame (0.0 is top)
        self.math_bg_node = self.bg.attachNewNode(mbg.generate())
        self.math_bg_node.setColor(0.0, 0.0, 0.0, 0.4)
        self.math_bg_node.setTransparency(TransparencyAttrib.MAlpha)
        self.math_bg_node.setPos(0, 0, -0.52)  # Initial position

        self.desc_math = OnscreenText(
            text="", pos=(-0.84, -0.56), scale=0.026, fg=(0.4, 0.9, 1.0, 1.0),
            align=TextNode.ALeft, parent=self.bg, wordwrap=wrap,
            font=self.font_math
        )

        # ── Interactive Floating Diagram elements ────────────────────
        self.diagram = base.aspect2d.attachNewNode("InteractiveDiagram")
        self._nodes.append(self.diagram)

        self.parts_info = {
            "jet": {
                "title": "1. Relativistic Jet",
                "desc": "Powered by the Blandford-Znajek mechanism, rotating magnetic fields extract rotational energy from the Kerr black hole. This accelerates collimated beams of particles along the poles to near-light speed (Lorentz factors gamma ~ 10-50).\n\nThese massive jets glow across the electromagnetic spectrum and blast material thousands of light-years into the surrounding intergalactic medium.",
                "math": "Blandford-Znajek Jet Power:\n  P_jet ≈ (f_c / 64π²) · Φ² · Ω_H²\n\nWhere:\n  Ω_H = a / (2 M r_plus)\n  γ = 1 / √(1 − v²/c²)"
            },
            "photon": {
                "title": "2. Photon Sphere",
                "desc": "A spherical region where gravity is strong enough to force photons into unstable circular orbits. For a Schwarzschild black hole (a=0), this sphere exists at r = 3M. For a Kerr black hole, the photon sphere splits into prograde and retrograde orbits.",
                "math": "Schwarzschild Orbit:\n  r_ph = 3M\n\nKerr Equatorial Orbit:\n  r_ph = 2M · [1 + cos(⅔ arccos(± a/M))]"
            },
            "horizon": {
                "title": "3. Event Horizon",
                "desc": "The causal boundary of the black hole -- a one-way membrane in spacetime. Once any matter or light crosses inward, its escape velocity exceeds the speed of light, making escape physically impossible.\n\nFor a spinning Kerr black hole, the horizon radius shrinks as spin (a) increases, concentrating the mass into a tighter volume.",
                "math": "Outer Horizon Radius (Boyer-Lindquist):\n  r_plus = M + √(M² − a²)\n\nExtremal Limit:\n  r_plus → M  as  a → M"
            },
            "singularity": {
                "title": "4. Ring Singularity",
                "desc": "At the center of a Kerr black hole, the singularity is not a point but a ring in the equatorial plane, where spacetime curvature becomes infinite.\n\nIn theory, an observer avoiding the ring could pass through it into an inner spacetime region, though wormhole stability remains highly speculative.",
                "math": "Kerr Singularity Condition:\n  Σ = r² + a² cos²(θ) = 0\n\nRing Coordinates:\n  r = 0,  θ = π/2"
            },
            "disk": {
                "title": "5. Accretion Disc",
                "desc": "A swirling disk of superheated gas and plasma orbiting the black hole. Frictional and magnetic forces (magnetorotational instability) heat the disk to millions of degrees, releasing intense thermal and X-ray radiation.",
                "math": "Disk Temperature Profile:\n  T(r) ≈ T_in · (r / r_in)^(−¾)\n\nRadiation Flux:\n  F(r) = (3 G M · M_dot / 8πr³) · [1 − √(r_in / r)]"
            },
            "isco": {
                "title": "6. ISCO Boundary",
                "desc": "The Innermost Stable Circular Orbit (ISCO) defines the absolute inner boundary of the accretion disk. Outside the ISCO, gas can orbit stably; inside, centrifugal force is no longer sufficient to combat gravity, and matter plunges directly into the event horizon.",
                "math": "Innermost Stable Circular Orbit:\n  r_ISCO = M · [3 + Z₂ ± √((3 − Z₁)(3 + Z₁ + 2Z₂))]\n\nWhere:\n  Z₁ = 1 + (1 − a²/M²)^(⅓) · [...]\n  Z₂ = √(3a²/M² + Z₁²)"
            }
        }

        # Setup pointers and buttons
        self.arrows = {}
        self.buttons = {}

        # We place buttons on the left of the screen, pointing towards the center
        # button_x, button_z, target_x, target_z
        self._layout = {
            "jet":         (-0.85,  0.75, *self._TARGETS["jet"]),
            "photon":      (-0.95,  0.45, *self._TARGETS["photon"]),
            "horizon":     (-0.95,  0.15, *self._TARGETS["horizon"]),
            "singularity": (-0.95, -0.15, *self._TARGETS["singularity"]),
            "disk":        (-0.95, -0.45, *self._TARGETS["disk"]),
            "isco":        (-0.85, -0.75, *self._TARGETS["isco"]),
        }

        self._labels = {
            "jet":         "Relativistic Jet",
            "photon":      "Photon Sphere",
            "horizon":     "Event Horizon",
            "singularity": "Singularity",
            "disk":        "Accretion Disc",
            "isco":        "ISCO Boundary",
        }

        # Build lines and button components
        for part_id, (bx, bz, tx, tz) in self._layout.items():
            # Draw line
            self.arrows[part_id] = self.draw_pointer(bx + 0.15, bz, tx, tz)
            
            # Place button
            self.add_button(self._labels[part_id], part_id, bx, bz)

        # Pulse circle task at target
        self.pulse_circle = None
        self._dot_t = 0.0
        
        # Start default selection
        self.select_part("horizon")

    def draw_pointer(self, x1, z1, x2, z2, color=(0.6, 0.6, 0.6, 0.5), thickness=1.5):
        ls = LineSegs()
        ls.setColor(color)
        ls.setThickness(thickness)
        ls.moveTo(x1, 0, z1)
        ls.drawTo(x2, 0, z2)
        
        # Arrowhead at destination
        dx = x2 - x1
        dz = z2 - z1
        length = math.sqrt(dx*dx + dz*dz)
        if length > 0:
            ux = dx / length
            uz = dz / length
            wing_len = 0.025
            wing_angle = math.radians(22)
            
            lx = x2 - wing_len * (ux * math.cos(wing_angle) - uz * math.sin(wing_angle))
            lz = z2 - wing_len * (ux * math.sin(wing_angle) + uz * math.cos(wing_angle))
            ls.moveTo(x2, 0, z2)
            ls.drawTo(lx, 0, lz)
            
            rx = x2 - wing_len * (ux * math.cos(-wing_angle) - uz * math.sin(-wing_angle))
            rz = z2 - wing_len * (ux * math.sin(-wing_angle) + uz * math.cos(-wing_angle))
            ls.moveTo(x2, 0, z2)
            ls.drawTo(rx, 0, rz)
            
        node = ls.create()
        return self.diagram.attachNewNode(node)

    def add_button(self, text, part_id, x, z):
        btn = DirectButton(
            text=text,
            scale=0.03,
            frameColor=(
                (0.02, 0.02, 0.04, 0.85),  # normal
                (0.9, 0.4, 0.0, 0.8),      # click
                (0.9, 0.45, 0.0, 0.25),    # rollover
                (0.02, 0.02, 0.04, 0.5)    # disabled
            ),
            frameSize=(-3.5, 3.5, -0.6, 0.8),
            text_fg=(1.0, 1.0, 1.0, 0.85),
            text_pos=(0, -0.15),
            pos=(x, 0, z),
            parent=self.diagram,
            command=self.select_part,
            extraArgs=[part_id]
        )
        
        # Hover coloring feedback
        btn.bind(DGG.WITHIN, lambda event, b=btn: b.configure(text_fg=(1.0, 0.7, 0.1, 1.0)))
        btn.bind(DGG.WITHOUT, lambda event, b=btn, pid=part_id: b.configure(text_fg=(1.0, 0.7, 0.1, 1.0)) if pid == self.active_part else b.configure(text_fg=(1.0, 1.0, 1.0, 0.85)))
        
        self.buttons[part_id] = btn

    def select_part(self, part_id):
        self.active_part = part_id

        # Update button visual styling and pointer line colors
        for pid, btn in self.buttons.items():
            btn["frameColor"] = (
                (0.02, 0.02, 0.04, 0.85),
                (0.9, 0.4, 0.0, 0.8),
                (0.9, 0.45, 0.0, 0.25),
                (0.02, 0.02, 0.04, 0.5)
            )
            btn["text_fg"] = (1.0, 1.0, 1.0, 0.85)
            self.arrows[pid].setColor(0.5, 0.5, 0.5, 0.4)
            self.arrows[pid].setScale(1.0)
            
        # Highlight selected active elements
        self.buttons[part_id]["frameColor"] = (
            (0.9, 0.4, 0.0, 0.45),
            (0.9, 0.4, 0.0, 0.8),
            (0.9, 0.45, 0.0, 0.6),
            (0.02, 0.02, 0.04, 0.5)
        )
        self.buttons[part_id]["text_fg"] = (1.0, 0.7, 0.1, 1.0)
        self.arrows[part_id].setColor(1.0, 0.50, 0.05, 1.0)
        self.arrows[part_id].setScale(1.03)

        # Clear existing pulsing target indicator
        if self.pulse_circle and not self.pulse_circle.isEmpty():
            self.pulse_circle.removeNode()
            self.pulse_circle = None

        # Draw a fresh pulsing target dot at the feature location
        tx, tz = self._TARGETS[part_id]
        
        # Build pulsing dot root
        self.pulse_circle = self.diagram.attachNewNode("pulse_target")
        
        dot_cm = CardMaker("pulse_dot")
        r = 0.020
        dot_cm.setFrame(tx - r, tx + r, tz - r, tz + r)
        dot_np = self.pulse_circle.attachNewNode(dot_cm.generate())
        dot_np.setTransparency(TransparencyAttrib.MAlpha)
        dot_np.setColor(1.0, 0.55, 0.05, 1.0)

        # Draw surrounding glowing ring
        ring = LineSegs()
        ring.setThickness(1.8)
        ring.setColor(1.0, 0.80, 0.20, 0.85)
        for i in range(25):
            ang = 2 * math.pi * i / 24
            ring.drawTo(tx + 0.042 * math.cos(ang), 0,
                        tz + 0.042 * math.sin(ang))
        self.pulse_circle.attachNewNode(ring.create())

        # Update sidebar texts
        info = self.parts_info[part_id]
        self.desc_title.setText(info["title"].upper())
        self.desc_body.setText(info["desc"])
        self.desc_math.setText(info["math"])

        # Dynamically position the math block based on body text height
        # Force a text layout update so the height is computed accurately
        self.desc_body.node().setWordwrap(28.0)
        body_height = self.desc_body.node().getHeight() * 0.028
        
        # Set new positions
        math_top = -0.28 - body_height - 0.04
        self.math_bg_node.setPos(0, 0, math_top)
        self.desc_math.setPos(-0.84, math_top - 0.04)

        # Setup simple task to pulse target dot scale
        if not self.base.taskMgr.hasTaskNamed("dot_pulse_task"):
            self.base.taskMgr.add(self._pulse_task, "dot_pulse_task")

    def _pulse_task(self, task):
        self._dot_t += globalClock.getDt() * 2.5
        s = 0.85 + 0.15 * math.sin(self._dot_t)
        if self.pulse_circle and not self.pulse_circle.isEmpty():
            self.pulse_circle.setScale(s, 1, s)
        return task.cont

    def toggle(self):
        self.visible = not self.visible
        if self.visible:
            for node in self._nodes:
                node.show()
            self.hint.show()
        else:
            for node in self._nodes:
                node.hide()
            self.hint.hide()
            if self.pulse_circle:
                self.pulse_circle.hide()
