import streamlit as st

def simple_background_test():
    """A minimal test to check if canvas backgrounds work at all."""
    st.markdown("""
    <style>
    .test-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(244, 247, 190, 0.2); /* Light cream with transparency */
        z-index: 0;
        pointer-events: none;
    }
    </style>
    <div class="test-background"></div>
    """, unsafe_allow_html=True)

def add_fluid_background():
    """Add a liquid-moving animation background inspired by Balatro."""

    # Add CSS for positioning
    st.markdown("""
    <style>
    .fluid-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: 0; /* Behind grid */
        pointer-events: none;
    }

    /* Update grid z-index to be on top of fluid but behind content */
    .grid-background,
    .main .block-container::before {
        z-index: -1; 
    }
    </style>
    """, unsafe_allow_html=True)

    # Add JavaScript for fluid animation
    st.markdown("""
    <canvas id="fluidCanvas" class="fluid-background"></canvas>

    <script>
    // Wait for the DOM to be fully loaded
    document.addEventListener('DOMContentLoaded', function() {
        // Get canvas element
        const canvas = document.getElementById('fluidCanvas');

        // Size canvas to window
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Get context for drawing
        const ctx = canvas.getContext('2d');

        // Animation parameters
        const particles = [];
        const particleCount = 30;
        const colorScheme = [
            {r: 103, g: 89, b: 122, a: 0.03},  // Deep purple
            {r: 233, g: 114, b: 76, a: 0.03},  // Coral
            {r: 229, g: 247, b: 125, a: 0.03},  // Lime
            {r: 117, g: 119, b: 97, a: 0.03}    // Olive gray
        ];

        // Create particles
        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                size: Math.random() * 300 + 150,
                color: colorScheme[Math.floor(Math.random() * colorScheme.length)],
                vx: Math.random() * 0.2 - 0.1,
                vy: Math.random() * 0.2 - 0.1,
                phase: Math.random() * Math.PI * 2,
                phaseSpeed: Math.random() * 0.005 + 0.002
            });
        }

        // Animation function
        function animate() {
            // Clear canvas with very slight opacity to create trails
            ctx.fillStyle = 'rgba(244, 247, 190, 0.01)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Update and draw particles
            for (let i = 0; i < particles.length; i++) {
                const p = particles[i];

                // Update position with sine wave motion for more organic movement
                p.x += p.vx + Math.sin(p.phase) * 0.4;
                p.y += p.vy + Math.cos(p.phase * 0.7) * 0.4;
                p.phase += p.phaseSpeed;

                // Create some slight size oscillation
                const sizeOscillation = 1 + Math.sin(p.phase * 2) * 0.1;
                const currentSize = p.size * sizeOscillation;

                // Wrap around edges
                if (p.x < -currentSize) p.x = canvas.width + currentSize;
                if (p.x > canvas.width + currentSize) p.x = -currentSize;
                if (p.y < -currentSize) p.y = canvas.height + currentSize;
                if (p.y > canvas.height + currentSize) p.y = -currentSize;

                // Draw gradient blob
                const gradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, currentSize);
                gradient.addColorStop(0, `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, ${p.color.a})`);
                gradient.addColorStop(1, `rgba(${p.color.r}, ${p.color.g}, ${p.color.b}, 0)`);

                ctx.beginPath();
                ctx.fillStyle = gradient;
                ctx.arc(p.x, p.y, currentSize, 0, Math.PI * 2);
                ctx.fill();
            }

            requestAnimationFrame(animate);
        }

        // Start animation
        animate();

        // Handle resize
        window.addEventListener('resize', function() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    });

    // Ensure this script runs even if Streamlit hot-reloads the page
    const observer = new MutationObserver(function(mutations) {
        if (!document.getElementById('fluidCanvas')) {
            const canvas = document.createElement('canvas');
            canvas.id = 'fluidCanvas';
            canvas.className = 'fluid-background';
            document.body.insertBefore(canvas, document.body.firstChild);

            // Dispatch a custom event to reinitialize canvas animation
            document.dispatchEvent(new Event('DOMContentLoaded'));
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)


def add_balatro_fluid_background():
    """
    Add a more advanced liquid animation background inspired by Balatro.
    This version includes turbulent flow, color interpolation, and more organic movement.
    """

    # Add CSS for positioning and basic styles
    st.markdown("""
    <style>
    .balatro-fluid-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -2; /* Behind grid */
        pointer-events: none;
    }

    /* Update grid z-index to be on top of fluid but behind content */
    .grid-background,
    .main .block-container::before {
        z-index: -1; 
        opacity: 0.85; /* Make grid slightly transparent to see fluid better */
    }
    </style>
    """, unsafe_allow_html=True)

    # Add JavaScript for advanced fluid animation
    st.markdown("""
    <canvas id="balatroFluidCanvas" class="balatro-fluid-background"></canvas>

    <script>
    // Wait for the DOM to be fully loaded
    document.addEventListener('DOMContentLoaded', function() {
        // Get canvas element
        const canvas = document.getElementById('balatroFluidCanvas');
        if (!canvas) return; // Safety check

        // Size canvas to window
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        // Get context for drawing
        const ctx = canvas.getContext('2d');

        // Animation parameters
        const metaballs = [];
        const metaballCount = 20;
        const baseColors = [
            { r: 103, g: 89, b: 122 },   // Deep purple
            { r: 233, g: 114, b: 76 },   // Coral
            { r: 229, g: 247, b: 125 },  // Lime
            { r: 117, g: 119, b: 97 }    // Olive gray
        ];

        // Simplex Noise implementation (simplified)
        // This simulates the turbulent flow effect
        class SimplexNoise {
            constructor() {
                this.grad3 = [
                    [1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0],
                    [1,0,1],[-1,0,1],[1,0,-1],[-1,0,-1],
                    [0,1,1],[0,-1,1],[0,1,-1],[0,-1,-1]
                ];
                this.p = [];
                for (let i = 0; i < 256; i++) {
                    this.p[i] = Math.floor(Math.random() * 256);
                }

                // To remove the need for index wrapping, double the permutation table length
                this.perm = new Array(512);
                this.gradP = new Array(512);

                // Skipping full Simplex noise implementation for brevity
                // This would be a full implementation in a real project

                this.seed(Math.random());
            }

            // Seed function to initialize the noise
            seed(seed) {
                if (seed > 0 && seed < 1) {
                    // Scale the seed out
                    seed *= 65536;
                }

                seed = Math.floor(seed);
                if (seed < 256) {
                    seed |= seed << 8;
                }

                for (let i = 0; i < 256; i++) {
                    let v;
                    if (i & 1) {
                        v = this.p[i] ^ (seed & 255);
                    } else {
                        v = this.p[i] ^ ((seed >> 8) & 255);
                    }

                    this.perm[i] = this.perm[i + 256] = v;
                    // Simplified gradient mapping
                    this.gradP[i] = this.gradP[i + 256] = this.grad3[v % 12];
                }
            }

            // Simple 2D noise function - returns a value between -1 and 1
            noise(x, y) {
                // Due to complexity, this is a simplified version that returns a value
                // based on sine waves, which approximates the effect
                return Math.sin(x * 0.1) * Math.cos(y * 0.1) * 0.5 + 
                       Math.sin(x * 0.2 + y * 0.3) * 0.5;
            }
        }

        // Create noise generator
        const simplex = new SimplexNoise();

        // Helper function to interpolate between colors
        function lerpColor(a, b, t) {
            return {
                r: a.r + (b.r - a.r) * t,
                g: a.g + (b.g - a.g) * t,
                b: a.b + (b.b - a.b) * t
            };
        }

        // Create metaballs
        for (let i = 0; i < metaballCount; i++) {
            // Select two colors to interpolate between
            const colorA = baseColors[Math.floor(Math.random() * baseColors.length)];
            const colorB = baseColors[Math.floor(Math.random() * baseColors.length)];

            metaballs.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                size: Math.random() * 350 + 200,
                colorA: colorA,
                colorB: colorB,
                colorT: 0, // Color interpolation parameter
                colorSpeed: Math.random() * 0.01 + 0.002,
                vx: Math.random() * 0.3 - 0.15,
                vy: Math.random() * 0.3 - 0.15,
                phase: Math.random() * Math.PI * 2,
                phaseSpeed: Math.random() * 0.005 + 0.001,
                turbulenceScale: Math.random() * 0.05 + 0.01,
                turbulenceStrength: Math.random() * 0.5 + 0.5
            });
        }

        // Time variables for animation
        let time = 0;
        const timeStep = 0.01;

        // Animation function
        function animate() {
            // Increment time
            time += timeStep;

            // Clear canvas with very slight opacity to create trails
            ctx.fillStyle = 'rgba(244, 247, 190, 0.03)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Update and draw metaballs
            for (let i = 0; i < metaballs.length; i++) {
                const m = metaballs[i];

                // Update color interpolation
                m.colorT += m.colorSpeed;
                if (m.colorT >= 1) {
                    m.colorT = 0;
                    m.colorA = m.colorB;
                    m.colorB = baseColors[Math.floor(Math.random() * baseColors.length)];
                }

                // Get interpolated color
                const currentColor = lerpColor(m.colorA, m.colorB, m.colorT);

                // Calculate turbulence effect
                const turbulenceX = simplex.noise(m.x * m.turbulenceScale, time) * m.turbulenceStrength;
                const turbulenceY = simplex.noise(time, m.y * m.turbulenceScale) * m.turbulenceStrength;

                // Update position with sinusoidal motion plus turbulence
                m.x += m.vx + Math.sin(m.phase) * 0.5 + turbulenceX;
                m.y += m.vy + Math.cos(m.phase * 0.7) * 0.5 + turbulenceY;
                m.phase += m.phaseSpeed;

                // Create size oscillation based on noise
                const sizeNoise = 0.1 * simplex.noise(time * 0.5, i);
                const sizeOscillation = 1 + sizeNoise;
                const currentSize = m.size * sizeOscillation;

                // Wrap around edges with padding
                if (m.x < -currentSize) m.x = canvas.width + currentSize;
                if (m.x > canvas.width + currentSize) m.x = -currentSize;
                if (m.y < -currentSize) m.y = canvas.height + currentSize;
                if (m.y > canvas.height + currentSize) m.y = -currentSize;

                // Draw gradient blob
                const gradient = ctx.createRadialGradient(m.x, m.y, 0, m.x, m.y, currentSize);
                gradient.addColorStop(0, `rgba(${currentColor.r}, ${currentColor.g}, ${currentColor.b}, 0.03)`);
                gradient.addColorStop(0.7, `rgba(${currentColor.r}, ${currentColor.g}, ${currentColor.b}, 0.01)`);
                gradient.addColorStop(1, `rgba(${currentColor.r}, ${currentColor.g}, ${currentColor.b}, 0)`);

                ctx.beginPath();
                ctx.fillStyle = gradient;

                // Draw elliptical shape for variety
                const stretchFactor = 1 + 0.2 * Math.sin(m.phase * 0.5);
                ctx.ellipse(
                    m.x, m.y, 
                    currentSize, 
                    currentSize * stretchFactor, 
                    m.phase, 0, Math.PI * 2
                );
                ctx.fill();
            }

            requestAnimationFrame(animate);
        }

        // Start animation
        animate();

        // Handle resize
        window.addEventListener('resize', function() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });
    });

    // Ensure this script runs even if Streamlit hot-reloads the page
    const observer = new MutationObserver(function(mutations) {
        if (!document.getElementById('balatroFluidCanvas')) {
            const canvas = document.createElement('canvas');
            canvas.id = 'balatroFluidCanvas';
            canvas.className = 'balatro-fluid-background';
            document.body.insertBefore(canvas, document.body.firstChild);

            // Dispatch a custom event to reinitialize canvas animation
            document.dispatchEvent(new Event('DOMContentLoaded'));
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
    </script>
    """, unsafe_allow_html=True)