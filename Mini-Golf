import streamlit as st
import streamlit.components.v1 as html_components

# Set page configuration
st.set_page_config(
    page_title="Streamlit Mini-Golf Tournament",
    page_icon="⛳",
    layout="wide"
)

# Custom CSS to style the Streamlit interface surrounding the game
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc;
    }
    .stAppHeader {
        background-color: transparent;
    }
    h1, h2, h3 {
        color: #38bdf8 !important;
        font-family: 'Inter', sans-serif;
    }
    .stat-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        backdrop-filter: blur(8px);
    }
    .stat-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #4ade80;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⛳ Streamlit Mini-Golf Championship")
st.caption("Aim with your mouse, click & hold to charge power, and release to shoot!")

# Streamlit sidebar for options and instructions
with st.sidebar:
    st.header("🎮 How to Play")
    st.markdown("""
    - **Aiming**: Move your mouse cursor around the golf ball to set your shot direction.
    - **Power Control**: **Click and hold** the left mouse button to charge the power meter. Release to stroke.
    - **Hazards**:
      - 🟡 **Sand Traps**: Slow down the ball significantly.
      - 🔵 **Water**: Resets ball to starting position (+1 stroke penalty).
      - 🧱 **Obstacles**: Bouncing walls and obstacles to navigate around.
    - **Objective**: Sink the ball into the hole ⛳ in as few strokes as possible!
    """)
    st.divider()
    st.info("💡 **Pro Tip**: Use wall reflections for tricky angles on later levels.")

# Embedded HTML5 Canvas Game Code
html_game_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            margin: 0;
            padding: 0;
            overflow: hidden;
            background-color: #0f172a;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            user-select: none;
        }
        #game-container {
            position: relative;
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        canvas {
            border-radius: 16px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 8px 10px -6px rgba(0, 0, 0, 0.5);
            background: #15803d;
            cursor: crosshair;
            touch-action: none;
        }
        .hud-panel {
            background: rgba(15, 23, 42, 0.85);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
    </style>
</head>
<body class="p-2 sm:p-4 text-white flex flex-col items-center justify-center min-h-screen">

    <div id="game-container" class="w-full">
        <!-- HUD Header -->
        <div class="hud-panel w-full rounded-2xl p-4 mb-4 flex flex-wrap justify-between items-center shadow-lg border border-slate-700">
            <div class="flex items-center space-x-6">
                <div>
                    <span class="text-xs uppercase tracking-wider text-slate-400 font-semibold block">Hole</span>
                    <span id="level-display" class="text-2xl font-black text-amber-400">1 / 4</span>
                </div>
                <div>
                    <span class="text-xs uppercase tracking-wider text-slate-400 font-semibold block">Par</span>
                    <span id="par-display" class="text-2xl font-black text-slate-200">3</span>
                </div>
                <div>
                    <span class="text-xs uppercase tracking-wider text-slate-400 font-semibold block">Strokes</span>
                    <span id="strokes-display" class="text-2xl font-black text-emerald-400">0</span>
                </div>
                <div>
                    <span class="text-xs uppercase tracking-wider text-slate-400 font-semibold block">Total Score</span>
                    <span id="total-score-display" class="text-2xl font-black text-cyan-400">0</span>
                </div>
            </div>
            
            <div class="flex items-center space-x-2 mt-2 sm:mt-0">
                <button id="reset-btn" class="px-4 py-2 bg-slate-700 hover:bg-slate-600 active:scale-95 transition-all text-sm font-semibold rounded-xl border border-slate-500 shadow">
                    Reset Hole
                </button>
            </div>
        </div>

        <!-- Main Game Canvas -->
        <div class="relative w-full flex justify-center">
            <canvas id="golfCanvas" width="850" height="520" class="w-full h-auto max-w-full border border-emerald-600/30"></canvas>
            
            <!-- Level Complete / Game Over Overlay -->
            <div id="modal-overlay" class="hidden absolute inset-0 bg-slate-900/90 backdrop-filter backdrop-blur-md rounded-2xl flex flex-col justify-center items-center p-6 text-center z-10 transition-all">
                <h2 id="modal-title" class="text-4xl font-extrabold text-amber-400 mb-2">Hole Completed!</h2>
                <p id="modal-subtitle" class="text-lg text-slate-300 mb-6">Great shot!</p>
                <button id="modal-action-btn" class="px-6 py-3 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold rounded-xl text-lg shadow-lg hover:shadow-emerald-500/20 active:scale-95 transition-all">
                    Next Hole
                </button>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('golfCanvas');
        const ctx = canvas.getContext('2d');

        // UI Elements
        const levelDisplay = document.getElementById('level-display');
        const parDisplay = document.getElementById('par-display');
        const strokesDisplay = document.getElementById('strokes-display');
        const totalScoreDisplay = document.getElementById('total-score-display');
        const resetBtn = document.getElementById('reset-btn');
        const modalOverlay = document.getElementById('modal-overlay');
        const modalTitle = document.getElementById('modal-title');
        const modalSubtitle = document.getElementById('modal-subtitle');
        const modalActionBtn = document.getElementById('modal-action-btn');

        // Physics Constants
        const FRICTION = 0.982;
        const SAND_FRICTION = 0.88;
        const MIN_VELOCITY = 0.05;

        // Game State Variables
        let currentLevelIndex = 0;
        let strokes = 0;
        let totalStrokes = 0;
        let isAiming = false;
        let isCharging = false;
        let power = 0;
        let powerDirection = 1;
        let mousePos = { x: 0, y: 0 };
        let animationFrameId = null;

        // Ball State
        const ball = {
            x: 100,
            y: 260,
            radius: 9,
            vx: 0,
            vy: 0,
            isMoving: false,
            startPos: { x: 100, y: 260 }
        };

        // Course Levels Definition
        const levels = [
            {
                name: "Level 1: The Warmup",
                par: 3,
                start: { x: 120, y: 260 },
                hole: { x: 730, y: 260, radius: 14 },
                walls: [
                    { x: 0, y: 0, w: 850, h: 20 },
                    { x: 0, y: 500, w: 850, h: 20 },
                    { x: 0, y: 0, w: 20, h: 520 },
                    { x: 830, y: 0, w: 20, h: 520 }
                ],
                obstacles: [
                    { type: 'rect', x: 400, y: 160, w: 30, h: 200, color: '#334155' }
                ],
                hazards: []
            },
            {
                name: "Level 2: Sand & Traps",
                par: 3,
                start: { x: 100, y: 150 },
                hole: { x: 750, y: 400, radius: 14 },
                walls: [
                    { x: 0, y: 0, w: 850, h: 20 },
                    { x: 0, y: 500, w: 850, h: 20 },
                    { x: 0, y: 0, w: 20, h: 520 },
                    { x: 830, y: 0, w: 20, h: 520 },
                    { x: 250, y: 0, w: 30, h: 320 }
                ],
                obstacles: [
                    { type: 'rect', x: 550, y: 200, w: 30, h: 300, color: '#334155' }
                ],
                hazards: [
                    { type: 'sand', x: 320, y: 350, w: 180, h: 120 },
                    { type: 'sand', x: 620, y: 100, w: 150, h: 150 }
                ]
            },
            {
                name: "Level 3: Water Island",
                par: 4,
                start: { x: 100, y: 260 },
                hole: { x: 750, y: 260, radius: 14 },
                walls: [
                    { x: 0, y: 0, w: 850, h: 20 },
                    { x: 0, y: 500, w: 850, h: 20 },
                    { x: 0, y: 0, w: 20, h: 520 },
                    { x: 830, y: 0, w: 20, h: 520 }
                ],
                obstacles: [
                    { type: 'rect', x: 300, y: 120, w: 30, h: 120, color: '#334155' },
                    { type: 'rect', x: 300, y: 280, w: 30, h: 120, color: '#334155' },
                    { type: 'rect', x: 550, y: 180, w: 30, h: 160, color: '#334155' }
                ],
                hazards: [
                    { type: 'water', x: 350, y: 150, w: 160, h: 220 },
                    { type: 'sand', x: 620, y: 200, w: 100, h: 120 }
                ]
            },
            {
                name: "Level 4: The Gauntlet",
                par: 5,
                start: { x: 80, y: 80 },
                hole: { x: 760, y: 440, radius: 14 },
                walls: [
                    { x: 0, y: 0, w: 850, h: 20 },
                    { x: 0, y: 500, w: 850, h: 20 },
                    { x: 0, y: 0, w: 20, h: 520 },
                    { x: 830, y: 0, w: 20, h: 520 }
                ],
                obstacles: [
                    { type: 'rect', x: 200, y: 0, w: 30, h: 380, color: '#334155' },
                    { type: 'rect', x: 420, y: 140, w: 30, h: 380, color: '#334155' },
                    { type: 'rect', x: 620, y: 0, w: 30, h: 380, color: '#334155' }
                ],
                hazards: [
                    { type: 'water', x: 230, y: 380, w: 190, h: 120 },
                    { type: 'water', x: 450, y: 20, w: 170, h: 120 },
                    { type: 'sand', x: 670, y: 200, w: 120, h: 150 }
                ]
            }
        ];

        // Level Initialization
        function loadLevel(index) {
            const level = levels[index];
            ball.x = level.start.x;
            ball.y = level.start.y;
            ball.vx = 0;
            ball.vy = 0;
            ball.isMoving = false;
            ball.startPos = { ...level.start };

            strokes = 0;
            updateHUD();
            hideModal();
        }

        function updateHUD() {
            const level = levels[currentLevelIndex];
            levelDisplay.textContent = `${currentLevelIndex + 1} / ${levels.length}`;
            parDisplay.textContent = level.par;
            strokesDisplay.textContent = strokes;
            totalScoreDisplay.textContent = totalStrokes;
        }

        // Input Handlers
        function getCanvasMousePos(e) {
            const rect = canvas.getBoundingClientRect();
            const scaleX = canvas.width / rect.width;
            const scaleY = canvas.height / rect.height;
            
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;

            return {
                x: (clientX - rect.left) * scaleX,
                y: (clientY - rect.top) * scaleY
            };
        }

        function handlePointerDown(e) {
            if (ball.isMoving) return;
            mousePos = getCanvasMousePos(e);
            isCharging = true;
            power = 0;
            powerDirection = 1;
        }

        function handlePointerMove(e) {
            mousePos = getCanvasMousePos(e);
        }

        function handlePointerUp(e) {
            if (!isCharging || ball.isMoving) return;
            isCharging = false;

            // Calculate stroke velocity vector
            const dx = mousePos.x - ball.x;
            const dy = mousePos.y - ball.y;
            const angle = Math.atan2(dy, dx);
            const shotStrength = (power / 100) * 18; // Max speed threshold

            ball.vx = Math.cos(angle) * shotStrength;
            ball.vy = Math.sin(angle) * shotStrength;
            ball.isMoving = true;

            strokes++;
            totalStrokes++;
            updateHUD();
            power = 0;
        }

        // Event Listeners
        canvas.addEventListener('mousedown', handlePointerDown);
        canvas.addEventListener('mousemove', handlePointerMove);
        window.addEventListener('mouseup', handlePointerUp);

        canvas.addEventListener('touchstart', (e) => { handlePointerDown(e); e.preventDefault(); }, { passive: false });
        canvas.addEventListener('touchmove', (e) => { handlePointerMove(e); e.preventDefault(); }, { passive: false });
        window.addEventListener('touchend', handlePointerUp);

        resetBtn.addEventListener('click', () => {
            loadLevel(currentLevelIndex);
        });

        // Main Game Update & Render Loop
        function update() {
            // Charge Power Meter Animation
            if (isCharging) {
                power += 2 * powerDirection;
                if (power >= 100 || power <= 0) {
                    powerDirection *= -1;
                }
            }

            // Ball Physics Processing
            if (ball.isMoving) {
                const currentLevel = levels[currentLevelIndex];
                
                // Determine Surface Friction (Sand Hazard Check)
                let currentFriction = FRICTION;
                currentLevel.hazards.forEach(hazard => {
                    if (hazard.type === 'sand' && 
                        ball.x >= hazard.x && ball.x <= hazard.x + hazard.w &&
                        ball.y >= hazard.y && ball.y <= hazard.y + hazard.h) {
                        currentFriction = SAND_FRICTION;
                    }
                });

                // Apply Movement & Friction
                ball.x += ball.vx;
                ball.y += ball.vy;
                ball.vx *= currentFriction;
                ball.vy *= currentFriction;

                // Stop ball if velocity drops below threshold
                if (Math.abs(ball.vx) < MIN_VELOCITY && Math.abs(ball.vy) < MIN_VELOCITY) {
                    ball.vx = 0;
                    ball.vy = 0;
                    ball.isMoving = false;
                }

                // Check Boundary Wall Collisions
                currentLevel.walls.forEach(wall => {
                    checkRectCollision(wall);
                });

                // Check Obstacle Collisions
                currentLevel.obstacles.forEach(obs => {
                    if (obs.type === 'rect') {
                        checkRectCollision(obs);
                    }
                });

                // Check Hazard Collisions (Water)
                currentLevel.hazards.forEach(hazard => {
                    if (hazard.type === 'water') {
                        if (ball.x >= hazard.x && ball.x <= hazard.x + hazard.w &&
                            ball.y >= hazard.y && ball.y <= hazard.y + hazard.h) {
                            // Penalty & Reset Position
                            ball.x = ball.startPos.x;
                            ball.y = ball.startPos.y;
                            ball.vx = 0;
                            ball.vy = 0;
                            ball.isMoving = false;
                            strokes++;
                            totalStrokes++;
                            updateHUD();
                        }
                    }
                });

                // Check Hole Victory
                const hole = currentLevel.hole;
                const distToHole = Math.hypot(ball.x - hole.x, ball.y - hole.y);
                if (distToHole < hole.radius - 2) {
                    ball.vx = 0;
                    ball.vy = 0;
                    ball.isMoving = false;
                    ball.x = hole.x;
                    ball.y = hole.y;
                    onHoleCompleted();
                }
            }
        }

        // Circle-Rectangle Collision Resolution
        function checkRectCollision(rect) {
            const nearestX = Math.max(rect.x, Math.min(ball.x, rect.x + rect.w));
            const nearestY = Math.max(rect.y, Math.min(ball.y, rect.y + rect.h));
            
            const deltaX = ball.x - nearestX;
            const deltaY = ball.y - nearestY;
            const distance = Math.hypot(deltaX, deltaY);

            if (distance < ball.radius) {
                // Determine collision normal direction
                const overlap = ball.radius - distance;
                
                if (distance === 0) {
                    ball.y -= overlap;
                    ball.vy *= -1;
                    return;
                }

                const normalX = deltaX / distance;
                const normalY = deltaY / distance;

                // Reposition ball outside wall
                ball.x += normalX * overlap;
                ball.y += normalY * overlap;

                // Reflect Velocity Vector
                const dot = ball.vx * normalX + ball.vy * normalY;
                ball.vx -= 2 * dot * normalX;
                ball.vy -= 2 * dot * normalY;
            }
        }

        // Render Canvas Scene
        function draw() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            const level = levels[currentLevelIndex];

            // 1. Draw Turf Grid Texture
            ctx.fillStyle = '#166534';
            for (let i = 0; i < canvas.width; i += 40) {
                for (let j = 0; j < canvas.height; j += 40) {
                    if ((i / 40 + j / 40) % 2 === 0) {
                        ctx.fillRect(i, j, 40, 40);
                    }
                }
            }

            // 2. Draw Hazards
            level.hazards.forEach(hazard => {
                if (hazard.type === 'sand') {
                    ctx.fillStyle = '#fde047';
                    ctx.beginPath();
                    ctx.roundRect(hazard.x, hazard.y, hazard.w, hazard.h, 16);
                    ctx.fill();
                    ctx.strokeStyle = '#eab308';
                    ctx.lineWidth = 3;
                    ctx.stroke();
                } else if (hazard.type === 'water') {
                    ctx.fillStyle = '#0284c7';
                    ctx.beginPath();
                    ctx.roundRect(hazard.x, hazard.y, hazard.w, hazard.h, 12);
                    ctx.fill();
                    ctx.strokeStyle = '#0369a1';
                    ctx.lineWidth = 3;
                    ctx.stroke();
                }
            });

            // 3. Draw Hole
            ctx.fillStyle = '#0f172a';
            ctx.beginPath();
            ctx.arc(level.hole.x, level.hole.y, level.hole.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.strokeStyle = '#334155';
            ctx.lineWidth = 3;
            ctx.stroke();

            // Flag pole
            ctx.strokeStyle = '#f8fafc';
            ctx.lineWidth = 3;
            ctx.beginPath();
            ctx.moveTo(level.hole.x, level.hole.y);
            ctx.lineTo(level.hole.x, level.hole.y - 35);
            ctx.stroke();

            // Flag cloth
            ctx.fillStyle = '#ef4444';
            ctx.beginPath();
            ctx.moveTo(level.hole.x, level.hole.y - 35);
            ctx.lineTo(level.hole.x + 18, level.hole.y - 27);
            ctx.lineTo(level.hole.x, level.hole.y - 20);
            ctx.fill();

            // 4. Draw Walls & Obstacles
            level.walls.forEach(w => {
                ctx.fillStyle = '#1e293b';
                ctx.fillRect(w.x, w.y, w.w, w.h);
            });

            level.obstacles.forEach(obs => {
                ctx.fillStyle = obs.color || '#334155';
                ctx.beginPath();
                ctx.roundRect(obs.x, obs.y, obs.w, obs.h, 6);
                ctx.fill();
                ctx.strokeStyle = '#475569';
                ctx.lineWidth = 2;
                ctx.stroke();
            });

            // 5. Draw Aiming Line & Trajectory Indicator
            if (!ball.isMoving) {
                const dx = mousePos.x - ball.x;
                const dy = mousePos.y - ball.y;
                const angle = Math.atan2(dy, dx);
                
                ctx.save();
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
                ctx.lineWidth = 2;
                ctx.setLineDash([6, 6]);
                ctx.beginPath();
                ctx.moveTo(ball.x, ball.y);
                ctx.lineTo(ball.x + Math.cos(angle) * 80, ball.y + Math.sin(angle) * 80);
                ctx.stroke();
                ctx.restore();

                // Power Indicator Bar over ball
                if (isCharging) {
                    const barWidth = 50;
                    const barHeight = 8;
                    const barX = ball.x - barWidth / 2;
                    const barY = ball.y - 25;

                    ctx.fillStyle = 'rgba(15, 23, 42, 0.8)';
                    ctx.fillRect(barX - 2, barY - 2, barWidth + 4, barHeight + 4);

                    const fillWidth = (power / 100) * barWidth;
                    // Color transitions from green to red based on power
                    const red = Math.floor((power / 100) * 255);
                    const green = Math.floor((1 - power / 100) * 255);
                    ctx.fillStyle = `rgb(${red}, ${green}, 50)`;
                    ctx.fillRect(barX, barY, fillWidth, barHeight);
                }
            }

            // 6. Draw Golf Ball
            ctx.shadowColor = 'rgba(0, 0, 0, 0.4)';
            ctx.shadowBlur = 6;
            ctx.shadowOffsetY = 3;

            ctx.fillStyle = '#ffffff';
            ctx.beginPath();
            ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
            ctx.fill();

            // Ball highlight detail
            ctx.shadowColor = 'transparent';
            ctx.fillStyle = 'rgba(226, 232, 240, 0.6)';
            ctx.beginPath();
            ctx.arc(ball.x - 2, ball.y - 2, ball.radius * 0.4, 0, Math.PI * 2);
            ctx.fill();
        }

        function gameLoop() {
            update();
            draw();
            animationFrameId = requestAnimationFrame(gameLoop);
        }

        // Victory Modal Handler
        function onHoleCompleted() {
            const currentPar = levels[currentLevelIndex].par;
            const diff = strokes - currentPar;
            
            let term = "Par!";
            if (strokes === 1) term = "Hole-in-One! 🌟";
            else if (diff === -2) term = "Eagle! 🦅";
            else if (diff === -1) term = "Birdie! 🐤";
            else if (diff === 1) term = "Bogey";
            else if (diff > 1) term = `+${diff} Over Par`;

            modalTitle.textContent = term;
            modalSubtitle.textContent = `Completed Level ${currentLevelIndex + 1} in ${strokes} strokes.`;

            if (currentLevelIndex < levels.length - 1) {
                modalActionBtn.textContent = "Next Hole →";
                modalActionBtn.onclick = () => {
                    currentLevelIndex++;
                    loadLevel(currentLevelIndex);
                };
            } else {
                modalTitle.textContent = "🏆 Tournament Finished!";
                modalSubtitle.textContent = `Total Strokes: ${totalStrokes}`;
                modalActionBtn.textContent = "Play Again 🔄";
                modalActionBtn.onclick = () => {
                    currentLevelIndex = 0;
                    totalStrokes = 0;
                    loadLevel(0);
                };
            }

            modalOverlay.classList.remove('hidden');
        }

        function hideModal() {
            modalOverlay.classList.add('hidden');
        }

        // Initialize Game
        loadLevel(0);
        gameLoop();
    </script>
</body>
</html>
"""

# Render the HTML/JS application inside Streamlit component iframe
html_components.html(html_game_code, height=650, scrolling=False)
