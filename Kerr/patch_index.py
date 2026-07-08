import pathlib

file_path = pathlib.Path(r'web/index.html')
if not file_path.exists():
    file_path = pathlib.Path(r'index.html')

content = file_path.read_text(encoding='utf-8')

start_marker = '<div class="tab-content" id="tab-guide">'
start_idx = content.find(start_marker)
if start_idx == -1:
    print("Start marker not found!")
    exit(1)

# Find the matching closing </div> for this tab-content div by balancing divs
depth = 1
end_idx = start_idx + len(start_marker)
while depth > 0 and end_idx < len(content):
    if content[end_idx:end_idx+4] == '<div':
        depth += 1
        end_idx += 4
    elif content[end_idx:end_idx+6] == '</div>':
        depth -= 1
        end_idx += 6
    else:
        end_idx += 1

print(f"Start index: {start_idx}, End index: {end_idx}, Length: {len(content)}")

new_html = """<div class="tab-content" id="tab-guide">
            <div class="diagram-container-wrapper">
                <!-- Left: Detailed descriptions of parts -->
                <div class="bh-descriptions">
                    <div class="desc-item" data-part="singularity">
                        <h4>Singularity</h4>
                        <p>At the very centre of a black hole, matter has collapsed into a region of infinite density called a singularity. All the matter and energy that fall into the black hole ends up here. The prediction of infinite density by general relativity is thought to indicate the breakdown of the theory where quantum effects become important.</p>
                    </div>
                    <div class="desc-item" data-part="horizon">
                        <h4>Event horizon</h4>
                        <p>This is the radius around a singularity where matter and energy cannot escape the black hole's gravity: the point of no return. This is the "black" part of the black hole.</p>
                    </div>
                    <div class="desc-item" data-part="photon">
                        <h4>Photon sphere</h4>
                        <p>Although the black hole itself is dark, photons are emitted from nearby hot plasma in jets or an accretion disc. In the absence of gravity, these photons would travel in straight lines, but just outside the event horizon of a black hole, gravity is strong enough to bend their paths so that we see a bright ring surrounding a roughly circular dark "shadow".</p>
                    </div>
                    <div class="desc-item" data-part="jet">
                        <h4>Relativistic jets</h4>
                        <p>When a black hole feeds on stars, gas or dust, the meal produces jets of particles and radiation blasting out from the black hole's poles at near light speed. They can extend for thousands of light-years into space.</p>
                    </div>
                    <div class="desc-item" data-part="isco">
                        <h4>Innermost stable orbit</h4>
                        <p>The inner edge of an accretion disc is the last place that material can orbit safely without the risk of falling past the point of no return.</p>
                    </div>
                    <div class="desc-item" data-part="disk">
                        <h4>Accretion disc</h4>
                        <p>A disc of superheated gas and dust whirls around a black hole at immense speeds, producing electromagnetic radiation (X-rays, optical, infrared and radio) that reveal the black hole's location. Some of this material is doomed to cross the event horizon, while other parts may be forced out to create jets.</p>
                    </div>
                </div>

                <!-- Right: Interactive SVG diagram matching the target image -->
                <div class="bh-visual-diagram">
                    <svg class="diagram-svg" viewBox="0 0 320 280" xmlns="http://www.w3.org/2000/svg">
                        <defs>
                            <!-- Disc Orange/Yellow gradient -->
                            <linearGradient id="discGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                                <stop offset="0%" stop-color="#ff3c00" stop-opacity="0.9" />
                                <stop offset="35%" stop-color="#ff7700" stop-opacity="0.8" />
                                <stop offset="70%" stop-color="#ffaa00" stop-opacity="0.9" />
                                <stop offset="100%" stop-color="#ffe600" stop-opacity="1" />
                            </linearGradient>
                            
                            <!-- Relativistic Jet gradient -->
                            <linearGradient id="jetGrad" x1="0%" y1="100%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#ff00bb" stop-opacity="0.2" />
                                <stop offset="30%" stop-color="#9000ff" stop-opacity="0.7" />
                                <stop offset="70%" stop-color="#00d2ff" stop-opacity="0.9" />
                                <stop offset="100%" stop-color="#ffffff" stop-opacity="1" />
                            </linearGradient>

                            <!-- Accretion disk glow overlay -->
                            <radialGradient id="bhGlow" cx="50%" cy="50%" r="50%">
                                <stop offset="0%" stop-color="#ff5500" stop-opacity="0.4" />
                                <stop offset="70%" stop-color="#ffaa00" stop-opacity="0.1" />
                                <stop offset="100%" stop-color="#000000" stop-opacity="0" />
                            </radialGradient>
                        </defs>

                        <!-- Subtle background glow -->
                        <circle cx="160" cy="140" r="100" fill="url(#bhGlow)" />

                        <!-- Jet bottom-left -->
                        <line x1="160" y1="140" x2="80" y2="230" stroke="url(#jetGrad)" stroke-width="4" stroke-linecap="round" opacity="0.35" />

                        <!-- Back lensed disc (Einstein ring halo above black hole) -->
                        <path d="M 70,140 Q 160,75 250,140" fill="none" stroke="url(#discGrad)" stroke-width="12" opacity="0.75" />
                        
                        <!-- Event Horizon Shadow -->
                        <circle cx="160" cy="140" r="35" fill="#000000" />
                        
                        <!-- Front disc crossing in front of shadow -->
                        <path d="M 60,140 Q 160,165 260,140" fill="none" stroke="url(#discGrad)" stroke-width="14" />
                        <path d="M 60,140 Q 160,158 260,140" fill="none" stroke="#ffffff" stroke-width="1" opacity="0.3" />

                        <!-- Photon Sphere glow ring -->
                        <circle cx="160" cy="140" r="38" fill="none" stroke="#ffaa00" stroke-width="1.5" opacity="0.7" style="filter: drop-shadow(0 0 3px #ff5500);" />

                        <!-- Singularity (center) -->
                        <circle cx="160" cy="140" r="1.5" fill="#ffffff" style="filter: drop-shadow(0 0 2px #fff);" />

                        <!-- Jet top-right -->
                        <line x1="160" y1="140" x2="250" y2="40" stroke="url(#jetGrad)" stroke-width="6" stroke-linecap="round" style="filter: drop-shadow(0 0 4px #00a2ff);" />
                        <line x1="160" y1="140" x2="250" y2="40" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" />

                        <!-- Pointer Lines (Standard state: low opacity white) -->
                        <!-- Relativistic Jet Pointer -->
                        <path id="line-jet" class="pointer-line" d="M 230,45 L 205,65 Q 195,75 200,95" />
                        <circle id="dot-jet" class="pointer-dot" cx="200" cy="95" r="2.5" />

                        <!-- Accretion Disc Pointer -->
                        <path id="line-disk" class="pointer-line" d="M 90,65 L 110,65 Q 120,65 115,146" />
                        <circle id="dot-disk" class="pointer-dot" cx="115" cy="146" r="2.5" />

                        <!-- Event Horizon Pointer -->
                        <path id="line-horizon" class="pointer-line" d="M 180,85 L 175,108 Q 172,118 165,122" />
                        <circle id="dot-horizon" class="pointer-dot" cx="165" cy="122" r="2.5" />

                        <!-- Singularity Pointer -->
                        <path id="line-singularity" class="pointer-line" d="M 235,125 L 200,125 Q 185,125 161,139" />
                        <circle id="dot-singularity" class="pointer-dot" cx="161" cy="139" r="2.5" />

                        <!-- Photon Sphere Pointer -->
                        <path id="line-photon" class="pointer-line" d="M 245,195 L 220,195 Q 205,195 197,149" />
                        <circle id="dot-photon" class="pointer-dot" cx="197" cy="149" r="2.5" />

                        <!-- Innermost Stable Orbit Pointer -->
                        <path id="line-isco" class="pointer-line" d="M 180,245 L 150,245 Q 138,245 138,155" />
                        <circle id="dot-isco" class="pointer-dot" cx="138" cy="155" r="2.5" />
                    </svg>

                    <!-- Labeled overlays -->
                    <div class="diagram-label label-jet" data-part="jet" style="top: 32px; left: 232px;">Relativistic Jet</div>
                    <div class="diagram-label label-disk" data-part="disk" style="top: 52px; left: 18px;">Accretion disc</div>
                    <div class="diagram-label label-horizon" data-part="horizon" style="top: 72px; left: 182px;">Event horizon</div>
                    <div class="diagram-label label-singularity" data-part="singularity" style="top: 112px; left: 237px;">Singularity</div>
                    <div class="diagram-label label-photon" data-part="photon" style="top: 182px; left: 247px;">Photon sphere</div>
                    <div class="diagram-label label-isco" data-part="isco" style="top: 232px; left: 182px;">Innermost stable orbit</div>
                </div>
            </div>

            <!-- Interactivity binding script -->
            <script>
                (function() {
                    const descItems = document.querySelectorAll('#tab-guide .desc-item');
                    descItems.forEach(item => {
                        const part = item.getAttribute('data-part');
                        item.addEventListener('mouseenter', () => {
                            const label = document.querySelector(`#tab-guide .label-${part}`);
                            const line = document.querySelector(`#tab-guide #line-${part}`);
                            const dot = document.querySelector(`#tab-guide #dot-${part}`);
                            if (label) label.classList.add('highlighted');
                            if (line) line.classList.add('highlighted');
                            if (dot) dot.classList.add('highlighted');
                        });
                        item.addEventListener('mouseleave', () => {
                            const label = document.querySelector(`#tab-guide .label-${part}`);
                            const line = document.querySelector(`#tab-guide #line-${part}`);
                            const dot = document.querySelector(`#tab-guide #dot-${part}`);
                            if (label) label.classList.remove('highlighted');
                            if (line) line.classList.remove('highlighted');
                            if (dot) dot.classList.remove('highlighted');
                        });
                    });

                    const labels = document.querySelectorAll('#tab-guide .diagram-label');
                    labels.forEach(label => {
                        const part = label.getAttribute('data-part');
                        label.addEventListener('mouseenter', () => {
                            const desc = document.querySelector(`#tab-guide .desc-item[data-part="${part}"]`);
                            const line = document.querySelector(`#tab-guide #line-${part}`);
                            const dot = document.querySelector(`#tab-guide #dot-${part}`);
                            if (desc) {
                                desc.classList.add('highlighted');
                                desc.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                            }
                            if (line) line.classList.add('highlighted');
                            if (dot) dot.classList.add('highlighted');
                            label.classList.add('highlighted');
                        });
                        label.addEventListener('mouseleave', () => {
                            const desc = document.querySelector(`#tab-guide .desc-item[data-part="${part}"]`);
                            const line = document.querySelector(`#tab-guide #line-${part}`);
                            const dot = document.querySelector(`#tab-guide #dot-${part}`);
                            if (desc) desc.classList.remove('highlighted');
                            if (line) line.classList.remove('highlighted');
                            if (dot) dot.classList.remove('highlighted');
                            label.classList.remove('highlighted');
                        });
                    });
                })();
            </script>
        </div>"""

patched_content = content[:start_idx] + new_html + content[end_idx:]
file_path.write_text(patched_content, encoding='utf-8')
print("Successfully patched index.html with interactive diagram!")
