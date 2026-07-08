<div align="center">

# 🌌 Black Hole Simulator X

### *A Real-Time Visualization of Kerr Black Hole Physics*

<img src="images/demo.gif" width="900"/>

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Panda3D](https://img.shields.io/badge/Panda3D-1.10.16-orange?style=for-the-badge)
![GLSL](https://img.shields.io/badge/OpenGL-GLSL%20330-red?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

*A real-time visualization of a rotating (Kerr) black hole featuring an animated accretion disk, procedural galaxy, plasma dynamics, relativistic effects, and custom GLSL shaders.*

</div>

---

# 📖 Overview

**Black Hole Simulator X** is a real-time visualization project inspired by modern astrophysics and the depiction of black holes in films like *Interstellar*.

The simulator recreates several physical phenomena observed around a rotating **Kerr Black Hole**, combining scientific concepts with real-time graphics using **Python**, **Panda3D**, and **OpenGL GLSL shaders**.

The primary goal of this project is to provide an educational and visually engaging representation of black hole physics while demonstrating advanced computer graphics techniques.

---

# ✨ Features

### 🌑 Black Hole
- Rotating Kerr Black Hole
- Event Horizon
- Photon Ring
- Ergosphere Visualization

### 🔥 Accretion Disk
- Multi-layer procedural plasma
- Spiral density waves
- Relativistic Doppler beaming
- Temperature-based color gradients
- Animated turbulence

### 🌌 Galaxy
- Procedurally generated spiral galaxy
- Thousands of dynamically generated stars
- Milky Way inspired distribution
- Halo star population

### ⚡ Plasma Effects
- Relativistic polar jets
- Animated plasma particles
- Dynamic brightness variation

### 🎨 Rendering
- Custom GLSL Vertex & Fragment Shaders
- HDR-inspired bloom
- Real-time lighting
- Interactive camera system

### 📚 Educational Physics Guide
- Event Horizon
- Ergosphere
- Frame Dragging
- Photon Ring
- Gravitational Lensing
- ISCO
- Relativistic Beaming
- Relativistic Jets

---

# 🧠 Physics Concepts

The simulator demonstrates several important concepts in General Relativity and Black Hole Astrophysics.

| Concept | Description |
|----------|-------------|
| 🌑 Event Horizon | Boundary beyond which nothing can escape |
| 🌀 Ergosphere | Region where spacetime itself is dragged by rotation |
| 💫 Photon Ring | Light trapped in unstable circular orbits |
| 🌠 Accretion Disk | Extremely hot plasma orbiting the black hole |
| ⚡ Relativistic Jets | Plasma expelled along the rotational axis |
| 🔥 Doppler Beaming | Plasma approaching the observer appears brighter |
| 🌌 Frame Dragging | Rotation twists spacetime around the black hole |

---

# 🖼️ Gallery

> *(Replace these with your screenshots.)*

| Side View | Top View |
|------------|----------|
| <img width="2828" height="1616" alt="Screenshot 2026-07-09 011207" src="https://github.com/user-attachments/assets/95c141a6-6aae-4a00-a61b-a74b2a865411" />
 | ![](images/top_view.png) |

---

# 🛠️ Technologies

- Python
- Panda3D 1.10.16
- OpenGL
- GLSL 330
- NumPy

---

# 📂 Project Structure

```text
BlackHole-Simulator-X
│
├── engine
│   ├── camera.py
│   ├── framebuffer.py
│   ├── lensing.py
│   ├── physics_guide.py
│   ├── postprocess.py
│   ├── renderer.py
│   ├── shader.py
│   └── objects
│       ├── blackhole.py
│       ├── disk.py
│       ├── plasma.py
│       ├── stars.py
│       └── ring.py
│
├── shaders
│   ├── blackhole.frag
│   ├── blackhole.vert
│   ├── disk.frag
│   ├── disk.vert
│   ├── lensing.frag
│   ├── lensing.vert
│   ├── stars.frag
│   └── stars.vert
│
├── config.py
├── main.py
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/ShreejayPandey123/BlackHole-Simulator-X.git
```

Move into the project directory

```bash
cd BlackHole-Simulator-X
```

Install the dependencies

```bash
pip install panda3d numpy
```

Run the simulator

```bash
python main.py
```

---

# 🎮 Controls

| Key | Action |
|------|--------|
| Mouse Drag | Rotate Camera |
| Mouse Wheel | Zoom |
| H | Toggle Physics Guide |

---

# 🚧 Future Improvements

- ✅ Real-time gravitational lensing
- ✅ Screen-space relativistic effects
- ✅ Volumetric accretion disk
- ✅ HDR rendering
- ✅ Procedural nebula generation
- ✅ Dynamic black hole parameters
- ✅ Multiple black hole presets

---

# 💡 Inspiration

This project is inspired by

- *Interstellar* (2014)
- Event Horizon Telescope (EHT)
- Kerr Black Hole solutions in General Relativity
- NASA & ESA scientific visualizations

---

# 👨‍💻 Author

**Shreejay Pandey**

Computer Science Student • Graphics Programming • Scientific Visualization

GitHub: **https://github.com/ShreejayPandey123**

---

<div align="center">

### ⭐ If you enjoyed this project, consider giving it a star!

*"Where gravity bends light and imagination meets physics."*

</div>
