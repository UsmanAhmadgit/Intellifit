// script.js
// Custom JavaScript for IntelliFit Platform

document.addEventListener('DOMContentLoaded', () => {
    console.log('IntelliFit platform loaded successfully.');
    // Check if THREE is loaded
    if (typeof THREE === 'undefined') {
        console.error('THREE.js library not loaded');
        return;
    }

    // Add a small delay to ensure GLTFLoader is available
    setTimeout(() => {
        if (typeof THREE.GLTFLoader === 'undefined') {
            console.error('GLTFLoader not loaded, retrying...');
            setTimeout(initializeThreeJS, 500);
        } else {
            initializeThreeJS();
        }
    }, 100);
});

// Three.js 3D Model Loader
let mixer;
let model;
let mouseX = 0;
let mouseY = 0;
let isMouseDown = false;

// Animation sequence with loop counts
const animationSequence = [
    { name: 'kip_up', file: './models/kip_up.glb', loops: 1 },
    { name: 'jumping_jacks', file: './models/jumping_jacks.glb', loops: 2 },
    { name: 'combo_punch', file: './models/combo_punch.glb', loops: 1 },
    { name: 'jog_forward', file: './models/jog_forward.glb', loops: 2 },
    { name: 'air_squat', file: './models/air_squat.glb', loops: 1 },
    { name: 'pistol', file: './models/pistol.glb', loops: 1 },
    { name: 'pike_walk', file: './models/pike_walk.glb', loops: 1 },
    { name: 'pushup', file: './models/pushup.glb', loops: 2 }
];

let currentSequenceIndex = 0;
let actions = {}; // Store all animations
let currentAction = null;
let nextAction = null; // For smooth blending
let scene;
let renderer;
let camera;
let container;
let clock;
let animationFinished = false;

function initializeThreeJS() {
    container = document.getElementById('model-container');

    if (!container) {
        console.warn('Model container not found');
        return;
    }

    // Final check for GLTFLoader
    if (typeof THREE.GLTFLoader === 'undefined') {
        console.error('✗ GLTFLoader not loaded');
        return;
    }

    console.log('✓ THREE.js loaded');
    console.log('✓ GLTFLoader loaded');
    console.log('Initializing Three.js...');
    console.log('Container dimensions:', container.clientWidth, 'x', container.clientHeight);

    // Scene setup
    scene = new THREE.Scene();
    scene.background = null; // Transparent background

    // Camera setup
    camera = new THREE.PerspectiveCamera(
        75,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );
    camera.position.z = 3;

    // Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.shadowMap.enabled = true;
    renderer.setClearColor(0x000000, 0); // Transparent background
    container.appendChild(renderer.domElement);
    console.log('✓ Renderer created');

    // Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 10, 5);
    directionalLight.castShadow = true;
    directionalLight.shadow.mapSize.width = 2048;
    directionalLight.shadow.mapSize.height = 2048;
    scene.add(directionalLight);
    console.log('✓ Lights added');

    // Mouse tracking
    document.addEventListener('mousemove', (event) => {
        mouseX = (event.clientX / window.innerWidth) * 2 - 1;
        mouseY = (event.clientY / window.innerHeight) * 2 - 1;
    });

    // Mouse down/up tracking - only on model container
    container.addEventListener('mousedown', () => {
        isMouseDown = true;
    });

    container.addEventListener('mouseup', () => {
        isMouseDown = false;
    });

    // Also reset when mouse leaves the container
    container.addEventListener('mouseleave', () => {
        isMouseDown = false;
    });

    // Clock for animation
    clock = new THREE.Clock();

    // Start animation loop
    animate();

    // Load character and start animation sequence
    initializeCharacter();

    // Handle window resize
    window.addEventListener('resize', () => {
        const width = container.clientWidth;
        const height = container.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
    });
}

function initializeCharacter() {
    // Start with first animation
    currentSequenceIndex = 0;
    loadAndPlayAnimation(animationSequence[0]);
}

function loadAndPlayAnimation(animConfig) {
    const loader = new THREE.GLTFLoader();

    loader.load(
        animConfig.file,
        function (gltf) {
            // Set up new model
            const newModel = gltf.scene;
            newModel.scale.set(1, 1, 1);
            newModel.position.set(0, 0, 0);

            scene.add(newModel);

            // Remove old model if exists
            if (model) {
                scene.remove(model);
            }

            model = newModel;

            // Create new mixer
            mixer = new THREE.AnimationMixer(newModel);

            // Get animation from this model
            if (gltf.animations.length > 0) {
                const clip = gltf.animations[0];
                const action = mixer.clipAction(clip);

                console.log(`Loaded: ${animConfig.name} (${animConfig.loops}x)`);

                // Configure and play action
                action.reset();
                action.setLoop(THREE.LoopRepeat, animConfig.loops);
                action.clampWhenFinished = true;
                action.timeScale = 0.75;
                action.play();
                currentAction = action;

                // Listen for animation finished
                mixer.addEventListener('finished', onAnimationFinished);
            } else {
                console.error(`No animation found in ${animConfig.file}`);
            }
        },
        undefined,
        function (error) {
            console.error(`Error loading ${animConfig.file}:`, error);
        }
    );
}

function playNextAnimation() {
    currentSequenceIndex = (currentSequenceIndex + 1) % animationSequence.length;
    const animConfig = animationSequence[currentSequenceIndex];
    console.log(`Next: ${animConfig.name} (${animConfig.loops}x)`);

    loadAndPlayAnimation(animConfig);
}

function onAnimationFinished(event) {
    console.log('Animation finished, loading next...');
    playNextAnimation();
}

function animate() {
    requestAnimationFrame(animate);

    const delta = clock.getDelta();

    // Update mixer
    if (mixer) {
        mixer.update(delta);
    }

    // Rotate model based on mouse position only if mouse is down
    if (model && isMouseDown) {
        model.rotation.y = mouseX * Math.PI * 2;
        model.rotation.x = mouseY * Math.PI * 0.5;
    }

    renderer.render(scene, camera);
}

// -------------------------------------------------------------
// GSAP Card Stack Scroll Animation for Second Section
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    // Wait for GSAP and ScrollTrigger
    if (typeof gsap === 'undefined' || typeof ScrollTrigger === 'undefined') {
        console.warn('GSAP or ScrollTrigger not loaded');
        return;
    }

    gsap.registerPlugin(ScrollTrigger);

    const cards = gsap.utils.toArray('.card');
    if (cards.length === 0) return;

    // Reverse the array so we process from TOP card (last in DOM) to BOTTOM card (first in DOM)
    const reversedCards = [...cards].reverse();

    // 1. Initial State Setup
    // Give each card a slight random rotation to make the stack look organic
    reversedCards.forEach((card, index) => {
        let rotation;
        if (index === 0) {
            rotation = 5;
        } else if (index === 1) {
            rotation = -5;
        } else {
            rotation = -5 - (index * 5); // 3rd is -15, 4th is -20, etc.
        }

        // Set the initial transforms
        gsap.set(card, {
            rotation: rotation,
            x: index * 2, // Slight offset
            y: index * 2
        });

        // Store the initial rotation so we can add to it later
        card.dataset.initialRotation = rotation;
    });

    // 2. Create the Timeline linked to scroll
    const tl = gsap.timeline({
        scrollTrigger: {
            trigger: "#pinned-section",
            start: "center center", // Start when the section hits the center of the viewport
            end: "+=400%", // Increased scroll distance to accommodate all cards and delays
            scrub: 1, // Smooth scrubbing effect (1 second lag for smoothness)
            pin: true, // Pin the section in place while scrolling
        }
    });

    // 3. Animate the cards
    // We loop through the reversed cards (Top to Bottom) and animate all of them sequentially.
    reversedCards.forEach((card, index) => {
        const rotateDir = 25; // All cards rotate to the right as they move up
        const initRot = parseFloat(card.dataset.initialRotation);

        tl.to(card, {
            y: -window.innerHeight - 100, // Move it way up above the screen
            rotation: initRot + rotateDir, // Rotate it further right as it goes up
            ease: "power2.inOut",
        }, "+=0.2");
        // "+=0.2" adds a gap so the next card waits until the previous one is fully off-screen
    });
});

// -------------------------------------------------------------
// Interactive Pricing Cards
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const pricingCards = document.querySelectorAll('.pricing-card');

    pricingCards.forEach(card => {
        card.addEventListener('click', () => {
            // Remove highlight class from all cards
            pricingCards.forEach(c => c.classList.remove('pricing-highlight-card'));

            // Add highlight class to clicked card
            card.classList.add('pricing-highlight-card');
        });
    });
});

// -------------------------------------------------------------
// Active Nav Link Update on Scroll
// -------------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll("section[id]");
    const navLinks = document.querySelectorAll(".nav-links .nav-link");
    const footerAbout = document.getElementById("about");
    let isFooterVisible = false;

    const setActiveNavById = (id) => {
        navLinks.forEach((link) => {
            link.classList.remove("nav-link-active");
            if (link.getAttribute("href") === `#${id}`) {
                link.classList.add("nav-link-active");
            }
        });
    };

    const setActiveByCurrentViewportSection = () => {
        let currentSectionId = null;
        sections.forEach((section) => {
            const rect = section.getBoundingClientRect();
            if (rect.top <= window.innerHeight * 0.35 && rect.bottom >= window.innerHeight * 0.35) {
                currentSectionId = section.id;
            }
        });

        if (currentSectionId) {
            setActiveNavById(currentSectionId);
        }
    };

    const observerOptions = {
        root: null,
        rootMargin: "-20% 0px -50% 0px",
        threshold: 0
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                if (isFooterVisible) {
                    return;
                }
                const currentId = entry.target.getAttribute("id");
                setActiveNavById(currentId);
            }
        });
    }, observerOptions);

    sections.forEach((section) => observer.observe(section));

    if (footerAbout) {
        const footerObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                isFooterVisible = entry.isIntersecting;
                if (isFooterVisible) {
                    setActiveNavById("about");
                } else {
                    setActiveByCurrentViewportSection();
                }
            });
        }, {
            root: null,
            threshold: 0
        });

        footerObserver.observe(footerAbout);
    }
});

// Mobile Menu Logic
function toggleMobileMenu() {
    const menu = document.getElementById('mobileOverlayMenu');
    if (menu) {
        menu.classList.toggle('show');
    }
}

function closeMobileMenu() {
    const menu = document.getElementById('mobileOverlayMenu');
    if (menu) {
        menu.classList.remove('show');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const mobileMenuClose = document.getElementById('mobileMenuClose');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', toggleMobileMenu);
    }
    if (mobileMenuClose) {
        mobileMenuClose.addEventListener('click', closeMobileMenu);
    }
    
    // FAQ Accordion Click Logic for Mobile
    const faqItems = document.querySelectorAll('.faq-item');
    faqItems.forEach(item => {
        item.addEventListener('click', () => {
            item.classList.toggle('active');
        });
    });
});
