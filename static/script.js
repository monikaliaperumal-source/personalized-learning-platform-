/* =========================================================
   LEARNPATH AI • CLIENT-SIDE INTERACTIVITY & SOUND FX
   ========================================================= */

// --- 1. WEB AUDIO SYNTHESIZER (MICRO-CHIMES) ---
let audioCtx = null;
let soundEnabled = true;

function initAudio() {
    if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    }
}

function playChime(freq = 440, type = 'sine', duration = 0.15) {
    if (!soundEnabled) return;
    try {
        initAudio();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(freq * 1.5, audioCtx.currentTime + duration);

        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);

        osc.connect(gain);
        gain.connect(audioCtx.destination);

        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    } catch (e) {
        // Silent catch for audio autoplay policies
    }
}

// Sound toggle button
const soundToggle = document.getElementById("soundToggle");
const soundIcon = document.getElementById("soundIcon");
if (soundToggle) {
    soundToggle.addEventListener("click", () => {
        soundEnabled = !soundEnabled;
        soundIcon.textContent = soundEnabled ? "🔊" : "🔇";
        if (soundEnabled) playChime(600);
    });
}

// --- 2. INTERACTIVE NEURAL PARTICLE CANVAS ---
const canvas = document.getElementById("neuralCanvas");
if (canvas) {
    const ctx = canvas.getContext("2d");
    let width, height;
    let particles = [];

    function resizeCanvas() {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    }
    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();

    class Particle {
        constructor() {
            this.x = Math.random() * width;
            this.y = Math.random() * height;
            this.vx = (Math.random() - 0.5) * 0.7;
            this.vy = (Math.random() - 0.5) * 0.7;
            this.radius = Math.random() * 2 + 1;
        }
        update() {
            this.x += this.vx;
            this.y += this.vy;
            if (this.x < 0 || this.x > width) this.vx *= -1;
            if (this.y < 0 || this.y > height) this.vy *= -1;
        }
        draw() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(168, 85, 247, 0.45)";
            ctx.fill();
        }
    }

    const particleCount = Math.min(width > 768 ? 45 : 20, 60);
    for (let i = 0; i < particleCount; i++) {
        particles.push(new Particle());
    }

    function animateParticles() {
        ctx.clearRect(0, 0, width, height);

        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();

            for (let j = i + 1; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const dist = Math.sqrt(dx * dx + dy * dy);

                if (dist < 120) {
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.strokeStyle = `rgba(124, 58, 237, ${0.25 * (1 - dist / 120)})`;
                    ctx.lineWidth = 1;
                    ctx.stroke();
                }
            }
        }
        requestAnimationFrame(animateParticles);
    }
    animateParticles();
}

// --- 3. LIVE PASSPORT & INTERACTIVE FORM CONTROLS ---
const performanceSlider = document.getElementById("performance_score");
const gaugeDisplay = document.getElementById("gaugeDisplay");
const tierDisplay = document.getElementById("tierDisplay");
const passportScore = document.getElementById("passportScore");
const passportTier = document.getElementById("passportTier");
const readinessVal = document.getElementById("readinessVal");
const readinessFill = document.getElementById("readinessFill");

function updatePerformanceSync() {
    if (!performanceSlider) return;
    const score = parseFloat(performanceSlider.value);
    const pct = Math.round(score * 100);

    if (gaugeDisplay) gaugeDisplay.textContent = pct + "%";
    if (passportScore) passportScore.textContent = pct + "%";

    let tierName = "Intermediate Scholar";
    let tierColor = "#3b82f6";
    let tierBg = "rgba(59, 130, 246, 0.15)";

    if (score < 0.60) {
        tierName = "🌱 Novice Explorer";
        tierColor = "#10b981";
        tierBg = "rgba(16, 185, 129, 0.15)";
    } else if (score < 0.80) {
        tierName = "🔵 Rising Scholar";
        tierColor = "#3b82f6";
        tierBg = "rgba(59, 130, 246, 0.15)";
    } else {
        tierName = "🟣 Apex Master";
        tierColor = "#a855f7";
        tierBg = "rgba(168, 85, 247, 0.15)";
    }

    if (tierDisplay) {
        tierDisplay.textContent = tierName;
        tierDisplay.style.color = tierColor;
        tierDisplay.style.background = tierBg;
    }
    if (passportTier) passportTier.textContent = tierName.replace(/[^a-zA-Z ]/g, "");

    // Calculate cognitive readiness index
    const assessment = parseFloat(document.getElementById("assessment_score")?.value || 75);
    const readiness = Math.min(100, Math.round((pct * 0.5) + (assessment * 0.5)));
    if (readinessVal) readinessVal.textContent = readiness + "%";
    if (readinessFill) readinessFill.style.width = readiness + "%";
}

if (performanceSlider) {
    performanceSlider.addEventListener("input", () => {
        updatePerformanceSync();
        playChime(300 + parseFloat(performanceSlider.value) * 400, 'sine', 0.05);
    });
    updatePerformanceSync();
}

// Stepper function
window.adjustValue = function(id, delta) {
    const el = document.getElementById(id);
    if (!el) return;
    let val = parseInt(el.value, 10) + delta;
    if (val >= parseInt(el.min, 10) && val <= parseInt(el.max, 10)) {
        el.value = val;
        syncPassportDetails();
        playChime(500 + val * 5);
    }
};

// Style selection handler
window.selectStyle = function(style, elem) {
    document.querySelectorAll(".style-card").forEach(c => c.classList.remove("active"));
    elem.classList.add("active");
    const input = document.getElementById("learning_style");
    if (input) input.value = style;

    const passportStyle = document.getElementById("passportStyle");
    if (passportStyle) passportStyle.textContent = elem.querySelector(".style-title").textContent;
    playChime(520, 'triangle');
};

// Topic selection handler
const topicEmojis = {
    "AI": "🤖",
    "Data Science": "📊",
    "Math": "🔢",
    "History": "🏛️",
    "Art": "🎨",
    "Music": "🎵"
};

window.selectTopic = function(topic, elem) {
    document.querySelectorAll(".topic-pill").forEach(p => p.classList.remove("active"));
    elem.classList.add("active");
    const input = document.getElementById("preferred_topics");
    if (input) input.value = topic;

    const passportTopic = document.getElementById("passportTopic");
    const avatarEmoji = document.getElementById("avatarEmoji");
    if (passportTopic) passportTopic.textContent = topic;
    if (avatarEmoji) avatarEmoji.textContent = topicEmojis[topic] || "🧠";

    playChime(640, 'triangle');
};

// Radio Status Sync
document.querySelectorAll('input[name="completion_status"]').forEach(radio => {
    radio.addEventListener("change", function() {
        const passportStatus = document.getElementById("passportStatus");
        if (passportStatus) {
            passportStatus.textContent = this.value === "Not Started" ? "🌱 Initiation" : (this.value === "In Progress" ? "⚡ Active Flow" : "🏆 Consolidation");
        }
        playChime(480);
    });
});

function syncPassportDetails() {
    const age = document.getElementById("age")?.value || "20";
    const edu = document.getElementById("education_level")?.value || "Bachelor";
    const passportAge = document.getElementById("passportAge");
    if (passportAge) passportAge.textContent = `${age} • ${edu}`;
}

const eduSelect = document.getElementById("education_level");
const ageInput = document.getElementById("age");
if (eduSelect) eduSelect.addEventListener("change", syncPassportDetails);
if (ageInput) ageInput.addEventListener("input", syncPassportDetails);

// Form Submit Feedback
const learningForm = document.getElementById("learningForm");
if (learningForm) {
    learningForm.addEventListener("submit", function(e) {
        const btn = document.getElementById("generateButton");
        if (btn) {
            playChime(880, 'sine', 0.3);
            btn.innerHTML = `<span class="btn-content"><span>⚡ Synthesizing KNN Matrix...</span></span>`;
            btn.style.opacity = "0.8";
            btn.style.pointerEvents = "none";
        }
    });
}