$(document).ready(function () {

    const exerciseTabs = $("#exerciseTabs .exercise-tab");
    const setBoxes = $("[data-set-box]");
    const doneSetBtn = $("#doneSetBtn");
    const nextExerciseBtn = $("#nextSetBtn");
    const exerciseList = $("#exerciseList");

    /* ── Full Exercise Database ── */
    const exerciseDB = {
        standard_pushup: {
            name: "Standard Pushup",
            media: "Exercises/standard_pushups.mp4",
            mediaType: "video",
            perSet: "15 reps",
            timerSeconds: 30,
            totalTime: "4m 30s",
            difficulty: "Medium",
            calories: "~15 kcal",
            description: [
                { title: "Start point:", text: "Begin in a high plank position, hands slightly wider than shoulder-width apart, arms straight, and core engaged." },
                { title: "Actions:", text: "Lower your body until your chest nearly touches the floor, keeping elbows tucked at a 45-degree angle. Push back up to the starting position." }
            ]
        },
        decline_pushup: {
            name: "Decline Pushup",
            media: "Exercises/decline_pushups.mp4",
            mediaType: "video",
            perSet: "12 reps",
            timerSeconds: 30,
            totalTime: "4m 30s",
            difficulty: "Hard",
            calories: "~18 kcal",
            description: [
                { title: "Start point:", text: "Place feet on an elevated surface (chair or box) and hands on the floor in a high plank position." },
                { title: "Actions:", text: "Lower your chest toward the floor while maintaining a straight line from heels to head. Push back up explosively." }
            ]
        },
        incline_pushup: {
            name: "Incline Pushup",
            media: "Exercises/incline_pushups.mp4",
            mediaType: "video",
            perSet: "20 reps",
            timerSeconds: 40,
            totalTime: "5m 0s",
            difficulty: "Easy",
            calories: "~15 kcal",
            description: [
                { title: "Start point:", text: "Place hands on a sturdy elevated surface (bed or table) with feet on the floor, body straight." },
                { title: "Actions:", text: "Lower your chest to the edge of the elevated surface, then press back up until arms are fully extended." }
            ]
        },
        pike_pushup: {
            name: "Pike Pushup",
            media: "Exercises/pike_pushups.mp4",
            mediaType: "video",
            perSet: "12 reps",
            timerSeconds: 30,
            totalTime: "4m 30s",
            difficulty: "Hard",
            calories: "~18 kcal",
            description: [
                { title: "Start point:", text: 'Begin in a downward dog position, hips pushed high into the air so the body forms an inverted "V".' },
                { title: "Actions:", text: 'Bend your elbows to lower the top of your head toward the floor between your hands. Press back up to the "V" position.' }
            ]
        },
        prone_y_raises: {
            name: "Prone Y-Raises",
            media: "Exercises/prone_y_raises.mp4",
            mediaType: "video",
            perSet: "15 reps",
            timerSeconds: 40,
            totalTime: "5m 0s",
            difficulty: "Medium",
            calories: "~12 kcal",
            description: [
                { title: "Start point:", text: 'Lie face down on the floor with arms extended straight out at a 45-degree angle (forming a "Y" shape), thumbs pointing up.' },
                { title: "Actions:", text: "Squeeze your upper back to lift your arms off the floor as high as possible. Hold for one second, then lower slowly." }
            ]
        },
        forearm_plank: {
            name: "Forearm Plank",
            media: "Exercises/forearm_plank.png",
            mediaType: "image",
            perSet: "60 sec",
            timerSeconds: 60,
            totalTime: "5m 0s",
            difficulty: "Medium",
            calories: "~15 kcal",
            description: [
                { title: "Start point:", text: "Lie face down, then prop your body up on your forearms and toes. Elbows should be directly under the shoulders." },
                { title: "Actions:", text: "Hold the body in a perfectly straight line from head to heels. Squeeze the glutes and brace the core tightly." }
            ]
        },
        lying_leg_raises: {
            name: "Lying Leg Raises",
            media: "Exercises/lying_leg_raises.mp4",
            mediaType: "video",
            perSet: "20 reps",
            timerSeconds: 45,
            totalTime: "5m 15s",
            difficulty: "Medium",
            calories: "~15 kcal",
            description: [
                { title: "Start point:", text: "Lie flat on your back with legs straight and hands placed flat on the floor beside your hips (or tucked under your lower back)." },
                { title: "Actions:", text: "Keeping legs straight, lift them upward until they form a 90-degree angle with the floor. Slowly lower them back down without letting heels touch the ground." }
            ]
        },
        bodyweight_squat: {
            name: "Bodyweight Squat",
            media: "Exercises/bodyweight_squat.mp4",
            mediaType: "video",
            perSet: "25 reps",
            timerSeconds: 45,
            totalTime: "5m 15s",
            difficulty: "Easy",
            calories: "~22 kcal",
            description: [
                { title: "Start point:", text: "Stand with feet shoulder-width apart, toes pointing slightly outward." },
                { title: "Actions:", text: "Push your hips back and bend your knees to lower your body as if sitting in a chair. Drive through your heels to return to standing." }
            ]
        },
        reverse_lunges: {
            name: "Reverse Lunges",
            media: "Exercises/reverse_lunges.mp4",
            mediaType: "video",
            perSet: "12 reps/leg",
            timerSeconds: 60,
            totalTime: "6m 0s",
            difficulty: "Medium",
            calories: "~25 kcal",
            description: [
                { title: "Start point:", text: "Stand tall with feet together and hands on your hips or held in front of your chest." },
                { title: "Actions:", text: "Take a large step backward with one foot, lowering your hips until both knees are bent at a 90-degree angle. Push off the back foot to return to the start." }
            ]
        },
        glute_bridges: {
            name: "Glute Bridges",
            media: "Exercises/glute_bridges.mp4",
            mediaType: "video",
            perSet: "20 reps",
            timerSeconds: 45,
            totalTime: "5m 15s",
            difficulty: "Easy",
            calories: "~15 kcal",
            description: [
                { title: "Start point:", text: "Lie on your back with knees bent, feet flat on the floor hip-width apart, and heels close to your glutes." },
                { title: "Actions:", text: "Drive through your heels and squeeze your glutes to push your hips toward the ceiling. Hold at the top, then lower slowly." }
            ]
        },
        towel_bicep_curls: {
            name: "Towel Bicep Curls",
            media: "Exercises/towel_bicep_curls.mp4",
            mediaType: "video",
            perSet: "15 reps",
            timerSeconds: 45,
            totalTime: "5m 15s",
            difficulty: "Medium",
            calories: "~12 kcal",
            description: [
                { title: "Start point:", text: "Sit on a sturdy chair. Loop a rolled-up towel under one thigh and hold the ends of the towel with both hands." },
                { title: "Actions:", text: "Curl your hands upward toward your chest, actively pressing your leg downward against the towel to create heavy resistance." }
            ]
        }
    };

    /* ── Section → exercise keys (cross-categorized, standard_pushup always first) ── */
    const workoutCatalog = {
        Chest: ["standard_pushup", "decline_pushup", "incline_pushup", "forearm_plank", "pike_pushup"],
        Shoulder: ["standard_pushup", "pike_pushup", "prone_y_raises", "decline_pushup", "forearm_plank"],
        Abs: ["standard_pushup", "forearm_plank", "lying_leg_raises", "pike_pushup"],
        Legs: ["standard_pushup", "bodyweight_squat", "reverse_lunges", "glute_bridges", "towel_bicep_curls"],
        Biceps: ["standard_pushup", "incline_pushup", "decline_pushup", "towel_bicep_curls", "prone_y_raises"]
    };

    let currentSection = "Chest";
    let currentExerciseIndex = 0;
    const completedExercises = {};
    Object.keys(workoutCatalog).forEach(k => {
        completedExercises[k] = workoutCatalog[k].map(() => false);
    });

    /* ── Helper: get current exercise object ── */
    function getCurrentExercise() {
        const keys = workoutCatalog[currentSection] || [];
        const key = keys[currentExerciseIndex];
        return exerciseDB[key] || null;
    }

    /* ── Render media (video or image) ── */
    function renderMedia(exercise) {
        const container = $("#mediaContainer");
        if (exercise.mediaType === "video") {
            container.html(`<video src="${exercise.media}" class="video-media" loop muted playsinline></video>`);
        } else {
            container.html(`<img src="${exercise.media}" alt="${exercise.name}" class="video-image">`);
        }
    }

    /* ── Video play/pause helpers ── */
    function playMainVideo() {
        const vid = $('#mediaContainer video')[0];
        if (vid) vid.play();
    }
    function pauseMainVideo() {
        const vid = $('#mediaContainer video')[0];
        if (vid) vid.pause();
    }

    /* ── Difficulty badge color ── */
    function difficultyStyle(level) {
        switch (level) {
            case "Easy": return "background:#e8f5e9; color:#2e7d32;";
            case "Hard": return "background:#ffebee; color:#c62828;";
            default: return "background:#fff3e0; color:#e65100;";
        }
    }

    /* ── Tab click ── */
    function setActiveExercise(sectionName) {
        exerciseTabs.removeClass("active");
        exerciseTabs.filter(`[data-exercise="${sectionName}"]`).addClass("active");
        currentSection = sectionName;
        currentExerciseIndex = 0;
        updateExerciseView();
    }

    exerciseTabs.on("click", function () {
        setActiveExercise($(this).data("exercise"));
    });

    /* ── Main view update ── */
    function updateExerciseView() {
        const keys = workoutCatalog[currentSection] || [];
        const exercise = getCurrentExercise();
        if (!exercise) return;

        // Title bar
        $("#selectedExerciseLabel").text(exercise.name);
        $("#exerciseStatText").text(exercise.name);
        $("#exercisePosition").text(currentExerciseIndex + 1);
        $("#exerciseTotal").text(keys.length);

        // Stats
        $("#statPerSet").text(exercise.perSet + " / set");
        $("#statTotalTime").text(exercise.totalTime);
        $("#statCalories").text(exercise.calories);

        // Difficulty badge
        const badge = $("#statDifficulty");
        badge.text(exercise.difficulty.toUpperCase());
        badge.attr("style", `font-size:0.62rem; font-weight:800; letter-spacing:0.06em; padding:3px 10px; border-radius:20px; ${difficultyStyle(exercise.difficulty)}`);

        // Description
        const descHTML = exercise.description.map((step, i) => `
            <div class="step-row">
                <div class="step-number">${i + 1}</div>
                <div>
                    <h6>${step.title}</h6>
                    <p>${step.text}</p>
                </div>
            </div>
        `).join("");
        $("#descriptionContent").html(descHTML);

        // Media
        renderMedia(exercise);

        // Next button
        const isLast = currentExerciseIndex >= keys.length - 1;
        nextExerciseBtn.toggleClass("is-disabled", isLast);
        nextExerciseBtn.prop("disabled", isLast);

        // Timer reset for new exercise
        resetTimer(exercise.timerSeconds);

        renderExerciseList();
    }

    /* ── Exercise sidebar list ── */
    function renderExerciseList() {
        const keys = workoutCatalog[currentSection] || [];
        const completedState = completedExercises[currentSection] || [];

        const items = keys.map(function (key, index) {
            const ex = exerciseDB[key];
            const isCurrent = index === currentExerciseIndex;
            const isCompleted = Boolean(completedState[index]);
            const statusClass = isCompleted ? 'is-checked' : (isCurrent ? 'is-active' : '');

            const thumbHTML = ex.mediaType === "video"
                ? `<video src="${ex.media}" class="queue-thumb" muted loop playsinline style="pointer-events:none;"></video>`
                : `<img src="${ex.media}" alt="${ex.name}" class="queue-thumb">`;

            return `
                <div class="queue-item" data-index="${index}" style="cursor:pointer;">
                    ${thumbHTML}
                    <div>
                        <h6>${ex.name}</h6>
                        <div class="queue-meta"><i class="bi bi-clock"></i> ${ex.totalTime} &nbsp; <i class="bi bi-fire"></i> ${ex.calories}</div>
                    </div>
                    <div class="status-icon ${statusClass}"><i class="bi bi-check2"></i></div>
                </div>
            `;
        }).join("");

        exerciseList.html(items);

        // Click handler to jump to exercise
        exerciseList.find(".queue-item").on("click", function () {
            const idx = parseInt($(this).data("index"));
            if (idx !== currentExerciseIndex) {
                currentExerciseIndex = idx;
                activeSetIndex = 0;
                doneSetBtn.removeClass("completed");
                setBoxes.removeClass("running completed");
                updateExerciseView();
                renderSetState();
            }
        });
    }

    /* ── Set progress ── */
    let activeSetIndex = 0;

    function renderSetState() {
        setBoxes.removeClass("running completed");
        setBoxes.each(function (index) {
            if (index <= activeSetIndex) $(this).addClass("completed");
            if (index === activeSetIndex) $(this).addClass("running");
        });
    }

    function advanceSet() {
        if (activeSetIndex < 2) {
            activeSetIndex += 1;
            renderSetState();
            // Reset timer for new set
            const ex = getCurrentExercise();
            if (ex) resetTimer(ex.timerSeconds);
            return;
        }
        activeSetIndex = 3;
        setBoxes.removeClass("running completed").addClass("completed");
        doneSetBtn.addClass("completed");

        const keys = workoutCatalog[currentSection] || [];
        if (keys.length) {
            completedExercises[currentSection][currentExerciseIndex] = true;
            renderExerciseList();
        }
    }

    /* ── Interactive SVG Timer ── */
    let isPlaying = false;
    let timeLeft = 30;
    let totalTime = 30;
    const circle = $('#timerProgress')[0];
    const circumference = 2 * Math.PI * 35;
    let timerInterval;
    const timerWrapper = $('#timerToggle');
    const timerDisplay = $('#timerDisplay');
    const playPauseIcon = $('#playPauseIcon');

    function formatSeconds(seconds) {
        return `${seconds} sec`;
    }

    function resetTimer(seconds) {
        clearInterval(timerInterval);
        totalTime = seconds;
        timeLeft = seconds;
        isPlaying = false;
        updateTimerDisplay();
        pauseMainVideo();
        playPauseIcon.removeClass('bi-pause-fill bi-arrow-clockwise').addClass('bi-play-fill');
    }

    function updateTimerDisplay() {
        timerDisplay.text(formatSeconds(timeLeft));
        const offset = circumference - (timeLeft / totalTime) * circumference;
        $(circle).css('stroke-dashoffset', offset);
    }

    function updateTimer() {
        if (timeLeft > 0) {
            timeLeft--;
            updateTimerDisplay();
        } else {
            clearInterval(timerInterval);
            isPlaying = false;
            pauseMainVideo();
            playPauseIcon.removeClass('bi-pause-fill bi-play-fill').addClass('bi-arrow-clockwise');
        }
    }

    function syncHoverIcon() {
        playPauseIcon
            .removeClass('bi-play-fill bi-pause-fill bi-arrow-clockwise')
            .addClass(isPlaying ? 'bi-pause-fill' : 'bi-play-fill');
    }

    timerWrapper.on('mouseenter', function () {
        $(this).addClass('hovering');
        syncHoverIcon();
    });

    timerWrapper.on('mouseleave', function () {
        $(this).removeClass('hovering');
        timerDisplay.text(formatSeconds(timeLeft));
    });

    timerWrapper.on('click', function () {
        if (isPlaying) {
            clearInterval(timerInterval);
            isPlaying = false;
            pauseMainVideo();
            playPauseIcon.removeClass('bi-pause-fill').addClass('bi-play-fill');
        } else {
            if (timeLeft === 0) timeLeft = totalTime;
            timerInterval = setInterval(updateTimer, 1000);
            isPlaying = true;
            playMainVideo();
            playPauseIcon.removeClass('bi-play-fill bi-arrow-clockwise').addClass('bi-pause-fill');
            updateTimerDisplay();
        }
        if (!timerWrapper.hasClass('hovering')) {
            timerDisplay.text(formatSeconds(timeLeft));
        }
    });

    doneSetBtn.on('click', function () {
        advanceSet();
    });

    nextExerciseBtn.on('click', function () {
        const keys = workoutCatalog[currentSection] || [];
        if (currentExerciseIndex < keys.length - 1) {
            currentExerciseIndex += 1;
            activeSetIndex = 0;
            doneSetBtn.removeClass("completed");
            setBoxes.removeClass("running completed");
            updateExerciseView();
            renderSetState();
        }
    });

    /* ── Motivational Quotes Rotation ── */
    const motivationalQuotes = [
        "Push harder than yesterday if you want a different tomorrow.",
        "Your body can stand almost anything — it's your mind you have to convince.",
        "The pain you feel today will be the strength you feel tomorrow.",
        "Don't stop when you're tired. Stop when you're done.",
        "Every rep brings you one step closer to the best version of yourself."
    ];
    let quoteIndex = 0;
    const motivationEl = $('#motivationText');

    setInterval(function () {
        motivationEl.css('opacity', 0);
        setTimeout(function () {
            quoteIndex = (quoteIndex + 1) % motivationalQuotes.length;
            motivationEl.text(motivationalQuotes[quoteIndex]);
            motivationEl.css('opacity', 1);
        }, 400);
    }, 5000);

    /* ── Sidebar page navigation ── */
    const navItems = $(".rail-pill .nav-icon[data-page]");
    const pageViews = $("[data-page-view]");

    function showPage(pageName) {
        navItems.removeClass("active");
        navItems.filter(`[data-page="${pageName}"]`).addClass("active");
        pageViews.removeClass("is-visible");
        $(".dashboard-grid").toggleClass("nav-page-active", pageName !== "home");
        if (pageName === "home") {
            $("#homeWorkspace").show();
        } else {
            $("#homeWorkspace").hide();
            $(`[data-page-view="${pageName}"]`).addClass("is-visible");
        }
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    navItems.on("click", function (e) {
        e.preventDefault();
        showPage($(this).data("page"));
    });

    $("[data-return-home]").on("click", function () {
        const target = $(this).data("return-home");
        showPage("home");
        setTimeout(() => document.getElementById(target)?.scrollIntoView({ behavior: "smooth", block: "center" }), 80);
    });

    $(".settings-tab").on("click", function () {
        $(this).siblings().removeClass("active");
        $(this).addClass("active");
    });

    /* ── Init ── */
    setActiveExercise("Chest");
    renderSetState();

});

// Mobile Profile Logout Toggle
$(function() {
    $('#mobileProfileToggle').on('click', function(e) {
        e.stopPropagation();
        $('#mobileLogoutPopup').toggleClass('show');
    });

    $('#mobileLogoutPopup').on('click', function(e) {
        e.stopPropagation();
        window.location.href = 'index.html';
    });

    $(document).on('click', function(e) {
        if ($('#mobileLogoutPopup').hasClass('show') && !$(e.target).closest('#mobileProfileToggle').length) {
            $('#mobileLogoutPopup').removeClass('show');
        }
    });
});

/* ── Browser camera AI coach ── */
$(function () {
    const apiBase = window.INTELLIFIT_API_URL || "http://127.0.0.1:8000";
    const camera = document.getElementById("coachCamera");
    const canvas = document.getElementById("coachCanvas");
    const placeholder = document.getElementById("cameraPlaceholder");
    const startButton = document.getElementById("startCoach");
    const stopButton = document.getElementById("stopCoach");
    const exerciseInput = document.getElementById("cvExercise");
    const targetInput = document.getElementById("cvTargetReps");
    const status = document.getElementById("coachStatus");
    const reps = document.getElementById("cvReps");
    const accuracy = document.getElementById("cvAccuracy");
    const stage = document.getElementById("cvStage");
    const feedback = document.getElementById("cvFeedback");
    let stream = null;
    let sessionId = null;
    let frameTimer = null;
    let framePending = false;

    function setFeedback(message, icon) {
        feedback.innerHTML = `<i class="bi ${icon}"></i><span>${message}</span>`;
    }

    function updateMetrics(data) {
        reps.textContent = `${data.reps} / ${data.target_reps}`;
        accuracy.textContent = `${Math.round(data.accuracy)}%`;
        stage.textContent = data.stage.replaceAll("_", " ");
        if (data.feedback.length) {
            setFeedback(data.feedback.join(" "), "bi-exclamation-triangle");
        } else if (data.detected) {
            setFeedback("Good form. Keep the movement controlled.", "bi-check-circle");
        } else {
            setFeedback("No full pose detected. Step back so your body stays in frame.", "bi-person-bounding-box");
        }
    }

    async function sendFrame() {
        if (!sessionId || framePending || !camera.videoWidth) return;
        framePending = true;
        canvas.width = 640;
        canvas.height = Math.round(640 * camera.videoHeight / camera.videoWidth);
        canvas.getContext("2d").drawImage(camera, 0, 0, canvas.width, canvas.height);
        const blob = await new Promise(resolve => canvas.toBlob(resolve, "image/jpeg", 0.72));
        const body = new FormData();
        body.append("frame", blob, "frame.jpg");
        try {
            const response = await fetch(`${apiBase}/api/sessions/${sessionId}/frames`, { method: "POST", body });
            if (!response.ok) throw new Error("Frame processing failed");
            const data = await response.json();
            updateMetrics(data);
            if (data.complete) setFeedback("Target reached. Stop and save your session.", "bi-trophy");
        } catch (error) {
            setFeedback("The AI service is unavailable. Start the Python API and try again.", "bi-wifi-off");
        } finally {
            framePending = false;
        }
    }

    async function stopCoach() {
        clearInterval(frameTimer);
        frameTimer = null;
        if (sessionId) {
            try {
                const response = await fetch(`${apiBase}/api/sessions/${sessionId}/stop`, { method: "POST" });
                if (response.ok) {
                    const summary = await response.json();
                    setFeedback(`${summary.reps} clean reps saved with ${Math.round(summary.posture_accuracy)}% accuracy.`, "bi-check-circle");
                }
            } catch (error) {
                setFeedback("Session ended, but the summary could not be saved.", "bi-exclamation-triangle");
            }
        }
        sessionId = null;
        if (stream) stream.getTracks().forEach(track => track.stop());
        stream = null;
        camera.srcObject = null;
        placeholder.classList.remove("is-hidden");
        startButton.disabled = false;
        stopButton.disabled = true;
        status.textContent = "READY";
        status.classList.remove("is-live");
        stage.textContent = "Waiting to start";
    }

    startButton.addEventListener("click", async function () {
        startButton.disabled = true;
        try {
            const response = await fetch(`${apiBase}/api/sessions`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ exercise: exerciseInput.value, target_reps: Number(targetInput.value) })
            });
            if (!response.ok) throw new Error("Could not create session");
            ({ session_id: sessionId } = await response.json());
            stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480 }, audio: false });
            camera.srcObject = stream;
            placeholder.classList.add("is-hidden");
            stopButton.disabled = false;
            status.textContent = "LIVE";
            status.classList.add("is-live");
            frameTimer = setInterval(sendFrame, 280);
            setFeedback("Camera active. Move into the starting position.", "bi-camera-video");
        } catch (error) {
            if (sessionId) await stopCoach();
            startButton.disabled = false;
            setFeedback("Allow camera access and make sure the Python API is running on port 8000.", "bi-exclamation-triangle");
        }
    });

    stopButton.addEventListener("click", stopCoach);
});
