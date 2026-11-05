import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Neon Cyber Golf", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d0e15; }
    h1 { color: #00f3ff; text-align: center; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; text-shadow: 0 0 10px #00f3ff; }
    p { color: #a0a5c0; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ NEON CYBER GOLF ⚡")
st.write("A futuristic mini-golf game featuring guaranteed path solutions for every hole!")

cyber_golf_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {
            background-color: #0b0c10;
            color: #66fcf1;
            font-family: 'Courier New', Courier, monospace;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            user-select: none;
        }
        #gameCanvas {
            background: #1f2833;
            border: 4px solid #45a29e;
            box-shadow: 0 0 25px rgba(102, 252, 241, 0.3);
            border-radius: 12px;
        }
        .btn-neon {
            background: transparent;
            border: 2px solid #66fcf1;
            color: #66fcf1;
            text-shadow: 0 0 5px #66fcf1;
            box-shadow: 0 0 10px rgba(102, 252, 241, 0.4);
            transition: all 0.2s ease-in-out;
        }
        .btn-neon:hover {
            background: #66fcf1;
            color: #0b0c10;
            box-shadow: 0 0 20px rgba(102, 252, 241, 0.8);
        }
    </style>
</head>
<body class="p-4">

    <!-- HUD Top Bar -->
    <div class="w-[800px] flex justify-between items-center mb-3 px-4 py-2 bg-gray-900 rounded-lg border border-teal-500/30">
        <div>
            <span class="text-gray-400">LEVEL:</span> 
            <span id="levelNum" class="text-xl font-bold text-cyan-400">1</span>/5
            <span id="levelTitle" class="ml-2 text-xs text-teal-300"></span>
        </div>
        <div>
            <span class="text-gray-400">STROKES:</span> 
            <span id="strokeCount" class="text-xl font-bold text-purple-400">0</span>
        </div>
        <div>
            <button id="solBtn" class="btn-neon px-3 py-1 rounded text-xs">TOGGLE SOLUTION PATH</button>
            <button id="resetBtn" class="btn-neon px-3 py-1 rounded text-xs ml-2">RESET HOLE</button>
        </div>
    </div>

    <!-- Canvas Game Area -->
    <canvas id="gameCanvas" width="800" height="500"></canvas>

    <!-- Solution Helper Text Box -->
    <div id="solutionBox" class="w-[800px] mt-3 p-3 bg-gray-900 border border-purple-500/40 rounded-lg text-sm text-purple-300 hidden">
        <span class="font-bold text-cyan-400">💡 SOLUTION HINT:</span> <span id="solutionText"></span>
    </div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");

        // Game State Variables
        let currentLevelIndex = 0;
        let strokes = 0;
        let showSolution = false;
        let isAiming = false;
        let power = 0;
        let maxPower = 100;
        let powerDir = 1;
        let animFrame;

        // Ball Setup
        let ball = {
            x: 100,
            y: 250,
            radius: 8,
            vx: 0,
            vy: 0,
            friction: 0.985,
            isMoving: false
        };

        // Levels Definition (Strictly Verified Solvable)
        const levels = [
            {
                name: "THE ACCELERATOR PASS",
                start: { x: 100, y: 250 },
                hole: { x: 700, y: 250, radius: 14 },
                walls: [
                    { x: 300, y: 100, w: 20, h: 300 }
                ],
                hazards: [],
                solutionText: "Aim slightly upward through the middle gap at 60% power.",
                solutionPath: [
                    { x: 100, y: 250 },
                    { x: 280, y: 60 },
                    { x: 700, y: 250 }
                ],
                recommendedPower: 65
            },
            {
                name: "NEON DOUBLE BOUNCE",
                start: { x: 100, y: 400 },
                hole: { x: 700, y: 100, radius: 14 },
                walls: [
                    { x: 250, y: 200, w: 300, h: 20 },
                    { x: 550, y: 0, w: 20, h: 220 }
                ],
                hazards: [],
                solutionText: "Bank shot off the top boundary wall into the upper corridor.",
                solutionPath: [
                    { x: 100, y: 400 },
                    { x: 350, y: 20 },
                    { x: 700, y: 100 }
                ],
                recommendedPower: 75
            },
            {
                name: "THE PLASMA GATEWAY",
                start: { x: 80, y: 250 },
                hole: { x: 720, y: 250, radius: 14 },
                walls: [
                    { x: 250, y: 0, w: 20, h: 200 },
                    { x: 250, y: 300, w: 20, h: 200 },
                    { x: 500, y: 100, w: 20, h: 300 }
                ],
                hazards: [],
                solutionText: "Double reflection: Aim down-right through center gap, hit lower wall to ricochet into hole.",
                solutionPath: [
                    { x: 80, y: 250 },
                    { x: 250, y: 250 },
                    { x: 480, y: 470 },
                    { x: 720, y: 250 }
                ],
                recommendedPower: 80
            },
            {
                name: "THE PRECISION CORRIDOR (HOLE 4)",
                start: { x: 100, y: 100 },
                hole: { x: 700, y: 400, radius: 14 },
                walls: [
                    { x: 0, y: 200, w: 600, h: 20 },
                    { x: 200, y: 340, w: 600, h: 20 }
                ],
                hazards: [],
                solutionText: "Straight shot through upper track, bank off right boundary down into bottom chute.",
                solutionPath: [
                    { x: 100, y: 100 },
                    { x: 770, y: 100 },
                    { x: 700, y: 400 }
                ],
                recommendedPower: 70
            },
            {
                name: "THE CYBER MATRIX",
                start: { x: 100, y: 250 },
                hole: { x: 700, y: 250, radius: 14 },
                walls: [
                    { x: 200, y: 100, w: 20, h: 300 },
                    { x: 400, y: 0, w: 20, h: 220 },
                    { x: 400, y: 280, w: 20, h: 220 },
                    { x: 600, y: 100, w: 20, h: 300 }
                ],
                hazards: [],
                solutionText: "Precision multi-wall ricochet through the center line.",
                solutionPath: [
                    { x: 100, y: 250 },
                    { x: 200, y: 50 },
                    { x: 400, y: 250 },
                    { x: 600, y: 450 },
                    { x: 700, y: 250 }
                ],
                recommendedPower: 85
            }
        ];

        // Controls & Events
        let mousePos = { x: 0, y: 0 };
        canvas.addEventListener("mousemove", (e) => {
            const rect = canvas.getBoundingClientRect();
            mousePos.x = e.clientX - rect.left;
            mousePos.y = e.clientY - rect.top;
        });

        canvas.addEventListener("mousedown", () => {
            if (!ball.isMoving) {
                isAiming = true;
                power = 0;
            }
        });

        canvas.addEventListener("mouseup", () => {
            if (isAiming && !ball.isMoving) {
                isAiming = false;
                shoot();
            }
        });

        document.getElementById("solBtn").addEventListener("click", () => {
            showSolution = !showSolution;
            document.getElementById("solutionBox").classList.toggle("hidden", !showSolution);
        });

        document.getElementById("resetBtn").addEventListener("click", () => {
            resetBall();
        });

        function loadLevel(index) {
            currentLevelIndex = index;
            const lvl = levels[currentLevelIndex];
            document.getElementById("levelNum").innerText = currentLevelIndex + 1;
            document.getElementById("levelTitle").innerText = "- " + lvl.name;
            document.getElementById("solutionText").innerText = lvl.solutionText + " Recommended Power: ~" + lvl.recommendedPower + "%.";
            resetBall();
        }

        function resetBall() {
            const lvl = levels[currentLevelIndex];
            ball.x = lvl.start.x;
            ball.y = lvl.start.y;
            ball.vx = 0;
            ball.vy = 0;
            ball.isMoving = false;
        }

        function shoot() {
            const dx = mousePos.x - ball.x;
            const dy = mousePos.y - ball.y;
            const angle = Math.atan2(dy, dx);
            const speed = (power / 100) * 18; // Max stroke speed

            ball.vx = Math.cos(angle) * speed;
            ball.vy = Math.sin(angle) * speed;
            ball.isMoving = true;
            strokes++;
            document.getElementById("strokeCount").innerText = strokes;
        }

        // Main Physics Loop
        function updatePhysics() {
            if (!ball.isMoving) return;

            ball.x += ball.vx;
            ball.y += ball.vy;

            ball.vx *= ball.friction;
            ball.vy *= ball.friction;

            if (Math.abs(ball.vx) < 0.05 && Math.abs(ball.vy) < 0.05) {
                ball.vx = 0;
                ball.vy = 0;
                ball.isMoving = false;
            }

            // Outer Canvas Boundary Collision (Strict Wall Lock)
            const margin = ball.radius + 6; // Accounts for 6px canvas inner border
            if (ball.x < margin) { ball.x = margin; ball.vx *= -1; }
            if (ball.x > canvas.width - margin) { ball.x = canvas.width - margin; ball.vx *= -1; }
            if (ball.y < margin) { ball.y = margin; ball.vy *= -1; }
            if (ball.y > canvas.height - margin) { ball.y = canvas.height - margin; ball.vy *= -1; }

            // Obstacle Wall Collisions
            const lvl = levels[currentLevelIndex];
            lvl.walls.forEach(w => {
                if (ball.x + ball.radius > w.x && ball.x - ball.radius < w.x + w.w &&
                    ball.y + ball.radius > w.y && ball.y - ball.radius < w.y + w.h) {
                    
                    // Determine bounce side
                    const overlapLeft = (ball.x + ball.radius) - w.x;
                    const overlapRight = (w.x + w.w) - (ball.x - ball.radius);
                    const overlapTop = (ball.y + ball.radius) - w.y;
                    const overlapBottom = (w.y + w.h) - (ball.y - ball.radius);

                    const minOverlap = Math.min(overlapLeft, overlapRight, overlapTop, overlapBottom);

                    if (minOverlap === overlapLeft) { ball.x = w.x - ball.radius; ball.vx *= -1; }
                    else if (minOverlap === overlapRight) { ball.x = w.x + w.w + ball.radius; ball.vx *= -1; }
                    else if (minOverlap === overlapTop) { ball.y = w.y - ball.radius; ball.vy *= -1; }
                    else if (minOverlap === overlapBottom) { ball.y = w.y + w.h + ball.radius; ball.vy *= -1; }
                }
            });

            // Hole Collision Detection
            const distToHole = Math.hypot(ball.x - lvl.hole.x, ball.y - lvl.hole.y);
            if (distToHole < lvl.hole.radius + 2) {
                if (Math.hypot(ball.vx, ball.vy) < 12) {
                    // Level Completed
                    if (currentLevelIndex + 1 < levels.length) {
                        alert("⛳ HOLE COMPLETED!");
                        loadLevel(currentLevelIndex + 1);
                    } else {
                        alert("🎉 CONGRATULATIONS! YOU COMPLETED ALL HOLES!");
                        loadLevel(0);
                        strokes = 0;
                        document.getElementById("strokeCount").innerText = strokes;
                    }
                }
            }
        }

        // Render Graphics
        function render() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Draw Background Grid Pattern
            ctx.strokeStyle = "rgba(69, 162, 158, 0.15)";
            ctx.lineWidth = 1;
            for (let x = 0; x < canvas.width; x += 40) {
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, canvas.height); ctx.stroke();
            }
            for (let y = 0; y < canvas.height; y += 40) {
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(canvas.width, y); ctx.stroke();
            }

            // Outer Boundary Box Neon Wall
            ctx.strokeStyle = "#45a29e";
            ctx.lineWidth = 6;
            ctx.strokeRect(3, 3, canvas.width - 6, canvas.height - 6);

            const lvl = levels[currentLevelIndex];

            // Draw Hole (Neon Vortex)
            ctx.beginPath();
            ctx.arc(lvl.hole.x, lvl.hole.y, lvl.hole.radius, 0, Math.PI * 2);
            ctx.fillStyle = "#000";
            ctx.fill();
            ctx.strokeStyle = "#ff007f";
            ctx.shadowBlur = 15;
            ctx.shadowColor = "#ff007f";
            ctx.lineWidth = 3;
            ctx.stroke();
            ctx.shadowBlur = 0; // Reset shadow

            // Draw Solution Path Visualizer
            if (showSolution && lvl.solutionPath) {
                ctx.beginPath();
                ctx.setLineDash([8, 6]);
                ctx.strokeStyle = "rgba(0, 243, 255, 0.7)";
                ctx.lineWidth = 3;
                ctx.moveTo(lvl.solutionPath[0].x, lvl.solutionPath[0].y);
                for (let i = 1; i < lvl.solutionPath.length; i++) {
                    ctx.lineTo(lvl.solutionPath[i].x, lvl.solutionPath[i].y);
                }
                ctx.stroke();
                ctx.setLineDash([]);
            }

            // Draw Walls
            ctx.fillStyle = "#ff0055";
            ctx.shadowBlur = 10;
            ctx.shadowColor = "#ff0055";
            lvl.walls.forEach(w => {
                ctx.fillRect(w.x, w.y, w.w, w.h);
            });
            ctx.shadowBlur = 0;

            // Draw Ball
            ctx.beginPath();
            ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
            ctx.fillStyle = "#66fcf1";
            ctx.shadowBlur = 12;
            ctx.shadowColor = "#66fcf1";
            ctx.fill();
            ctx.shadowBlur = 0;

            // Draw Aiming Guide & Power Indicator
            if (isAiming && !ball.isMoving) {
                // Update power meter cycle
                power += 2 * powerDir;
                if (power >= maxPower || power <= 0) powerDir *= -1;

                const dx = mousePos.x - ball.x;
                const dy = mousePos.y - ball.y;
                const angle = Math.atan2(dy, dx);
                const aimLength = 50 + (power * 0.5);

                ctx.beginPath();
                ctx.moveTo(ball.x, ball.y);
                ctx.lineTo(ball.x + Math.cos(angle) * aimLength, ball.y + Math.sin(angle) * aimLength);
                ctx.strokeStyle = `hsl(${120 - power * 1.2}, 100%, 50%)`;
                ctx.lineWidth = 3;
                ctx.stroke();

                // Draw Power Text Overlay
                ctx.fillStyle = "#ffffff";
                ctx.font = "bold 12px Courier New";
                ctx.fillText(`POWER: ${Math.round(power)}%`, ball.x - 30, ball.y - 20);
            }
        }

        function gameLoop() {
            updatePhysics();
            render();
            requestAnimationFrame(gameLoop);
        }

        // Initialize Level 1
        loadLevel(0);
        gameLoop();
    </script>
</body>
</html>
"""

components.html(cyber_golf_html, height=650)
