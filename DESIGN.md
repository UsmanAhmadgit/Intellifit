# Design System Specification: The Kinetic Editorial

## 1. Overview & Creative North Star
This design system is built to transcend the "standard" fitness application. Our Creative North Star is **"The Kinetic Curator."** We are not building a static dashboard; we are building a high-performance environment that mirrors the energy of a premium training studio. 

The aesthetic rejects the rigid, boxy constraints of traditional Bootstrap layouts. Instead, we lean into **Editorial Fluidity**—using intentional asymmetry, overlapping elements (e.g., imagery breaking out of container bounds), and a sophisticated hierarchy of surfaces. We move away from "templates" by utilizing aggressive white space and high-contrast typography to create a sense of momentum and technical precision.

---

## 2. Colors: Vibrancy & Volume
The palette balances the aggressive energy of high-octane fitness with the clean, clinical precision of modern health-tech.

### The Color Logic
*   **Primary (`#6B46C1`):** Use for "High-State" actions and brand anchors. It represents the depth and focus of the athlete.
*   **Secondary (`#FF8A8A` / `secondary_container`):** Used as a "Pulse" color. Use this for progress indicators, secondary CTAs, and accents that require emotional warmth.
*   **Surface Hierarchy:** We utilize a "Neutral-Plus" approach. Backgrounds are clean (`#f8f9fa`), but depth is created through `surface-container` tiers rather than shadows.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders to section off content. Content containment must be achieved through background color shifts. For example, a card (`surface_container_lowest`) should sit on a section background (`surface_container_low`). If an element doesn't pop, increase the tonal contrast between the layers, do not add a stroke.

### Signature Textures & Glassmorphism
To create a "Tech-Forward" feel, use **Glassmorphism** for floating UI elements like navigation bars or music controllers. 
*   **Token Usage:** Use `surface` colors at 70% opacity with a `backdrop-blur` of 20px. 
*   **Gradients:** Main CTAs should use a subtle vertical gradient from `primary` (#532aa8) to `primary_container` (#6B46C1) to provide a "tactile" glow that flat colors cannot achieve.

---

## 3. Typography: The Voice of Authority
We utilize a dual-font system to balance personality with functional clarity.

*   **Headlines (Lexend):** A geometric sans-serif that feels expansive and modern. Use `display-lg` and `headline-lg` aggressively. Don't be afraid of tight letter-spacing (-2%) for large headings to create a "bold editorial" look.
*   **Body (Inter):** The technical workhorse. Inter provides the precision needed for workout data and metrics. 
*   **Visual Hierarchy:** Titles (`title-lg`) should always be high-contrast against the surface. Labels (`label-sm`) should use `on_surface_variant` to recede, ensuring the user's eye is always drawn to the most "motivating" data point first.

---

## 4. Elevation & Depth: Tonal Layering
We do not use structural lines. We use physics and light.

*   **The Layering Principle:** Depth is achieved by "stacking" the surface-container tiers. 
    *   *Base Level:* `surface` (#f8f9fa)
    *   *Section Level:* `surface_container_low`
    *   *Card/Element Level:* `surface_container_lowest` (#ffffff)
*   **Ambient Shadows:** When an element must "float" (like a primary action button or a modal), use a highly diffused shadow. 
    *   **Shadow Specs:** Blur: 32px, Y-Offset: 8px, Color: `on_surface` at 6% opacity. This mimics natural, ambient light.
*   **The Ghost Border Fallback:** If a border is required for accessibility in input fields, use the `outline_variant` token at 20% opacity. Never use 100% opaque borders.

---

## 5. Components: Bespoke Primitives

### Buttons
*   **Primary:** Rounded `xl` (1.5rem) or `full`. Use the Primary-to-Primary-Container gradient. Text should be `on_primary` (#ffffff) in Lexend Bold.
*   **Secondary:** Ghost style. No background, `outline` at 20% opacity, with `primary` text.
*   **States:** On hover, buttons should "lift" using the Ambient Shadow spec mentioned above, rather than just changing color.

### Cards & Sidebar
*   **The Sidebar:** A "sleek" sidebar must be semi-transparent (`surface` @ 80%) with a backdrop blur. Use `title-sm` for nav items with a 12px left-accent bar in `secondary` for the active state.
*   **Cards:** Forbid divider lines. Separate "Exercise Name" from "Reps/Sets" using `body-lg` (bold) and `body-sm` (muted) with a 16px vertical gap (Spacing Scale).

### Inputs & Fields
*   **Text Inputs:** Use `surface_container_high` for the field background. On focus, transition the background to `surface_container_lowest` and add a 2px "Ghost Border" in `primary`.

### Additional Custom Components
*   **The Pulse Tracker:** A custom chip using `secondary_container` background with `on_secondary_container` text to highlight active heart rate or calories.
*   **Metric Overlays:** Large, 50% opacity Lexend numbers (`display-lg`) placed *behind* foreground text to create a layered, "PowerPoint-Editorial" data visualization.

---

## 6. Do's and Don'ts

### Do
*   **Do** use asymmetrical margins (e.g., more padding on the left than the right) for hero sections to create a sense of movement.
*   **Do** lean into the "roundedness scale." All interactive elements should feel soft to the touch (`xl` or `full` rounding).
*   **Do** use `secondary` (Coral) sparingly as a "high-energy" highlight, not a primary surface color.

### Don't
*   **Don't** use black (#000000). Use `on_surface` (#191c1d) for text to maintain a premium, soft-touch feel.
*   **Don't** use Bootstrap's default `.card` borders. Use background tonal shifts only.
*   **Don't** cram content. If a screen feels full, increase the white space. This system breathes; it doesn't suffocate.