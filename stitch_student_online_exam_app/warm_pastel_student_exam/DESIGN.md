---
name: Warm Pastel Student Exam
colors:
  surface: '#fff8f5'
  surface-dim: '#e0d8d5'
  surface-bright: '#fff8f5'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#faf2ee'
  surface-container: '#f4ece8'
  surface-container-high: '#eee7e3'
  surface-container-highest: '#e9e1dd'
  on-surface: '#1e1b19'
  on-surface-variant: '#544249'
  inverse-surface: '#33302d'
  inverse-on-surface: '#f7efeb'
  outline: '#87717a'
  outline-variant: '#dac0c9'
  surface-tint: '#a43073'
  primary: '#a43073'
  on-primary: '#ffffff'
  primary-container: '#f472b6'
  on-primary-container: '#6d0047'
  inverse-primary: '#ffafd3'
  secondary: '#6d5e00'
  on-secondary: '#ffffff'
  secondary-container: '#fcdf46'
  on-secondary-container: '#726200'
  tertiary: '#7b41b4'
  on-tertiary: '#ffffff'
  tertiary-container: '#c084fc'
  on-tertiary-container: '#500989'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffd8e7'
  primary-fixed-dim: '#ffafd3'
  on-primary-fixed: '#3d0026'
  on-primary-fixed-variant: '#85145a'
  secondary-fixed: '#ffe24c'
  secondary-fixed-dim: '#e2c62d'
  on-secondary-fixed: '#211b00'
  on-secondary-fixed-variant: '#524600'
  tertiary-fixed: '#f0dbff'
  tertiary-fixed-dim: '#ddb8ff'
  on-tertiary-fixed: '#2c0051'
  on-tertiary-fixed-variant: '#62259b'
  background: '#fff8f5'
  on-background: '#1e1b19'
  surface-variant: '#e9e1dd'
typography:
  headline-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '800'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '800'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 28px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 17px
    fontWeight: '500'
    lineHeight: 26px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '700'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.04em
rounded:
  sm: 0.5rem
  DEFAULT: 1rem
  md: 1.5rem
  lg: 2rem
  xl: 3rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-mobile: 0.75rem
  margin: 1.5rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system translates a comforting, warm pastel aesthetic into an engaging, low-anxiety digital examination and study interface. Examinations are traditionally high-stress, sterile, and intimidating experiences. This system deliberately subverts that emotional weight by utilizing soft, nurturing surfaces, tactile organic shapes, pill-form micro-interactions, and crystal-clear high-contrast typography.

The personality is reassuring, focused, and gently motivating. Designed primarily for mobile-first testing environments, learning assessments, and adaptive quizzes, the system prioritizes clarity and calm focus while retaining playful details—such as rounded chip-selectors, soft gradient glows, and tactile button feedback—that keep students feeling supported rather than evaluated.

## Colors

The palette is rooted in creamy, peach-tinged background tones that eliminate harsh screen glare during long test sessions. High-contrast deep charcoal typography ensures accessibility and effortless legibility. Soft pastel accents designate statuses, categories, and question types without creating visual alarm.

- **Background & Canvas:** Soft warm cream (`#FAF6F0`) serves as the root surface, paired with pure white (`#FFFFFF`) or tinted ivory cards to establish distinct question areas.
- **Primary Accent:** Bubblegum / Soft Carnation Pink (`#F472B6`) drives primary actions, affirmative triggers, and key milestones.
- **Secondary Accent:** Soft Canary / Pastel Yellow (`#FDE047` / `#FEF08A`) highlights bookmarks, prompt callouts, active timers, and hints.
- **Tertiary Accents:** Pastel Lavender (`#C084FC` / `#E9D5FF`) and Gentle Sky Blue (`#93C5FD` / `#BAE6FD`) represent subject tags, category chips, and supplementary options.
- **Text & Stroke:** Charcoal Black (`#1C1917`) provides sharp, readable contrast against pastel fills. Hairline separators and inactive chip outlines use warm muted taupe (`#E7E0D8`).

## Typography

Typography is set exclusively in **Plus Jakarta Sans**, balancing contemporary geometric structure with welcoming, humanist terminal cuts. This creates an unhurried, reassuring reading rhythm ideal for reading prompts, analytical tasks, and multi-choice selections.

- **Headlines:** Set tightly in Bold (700) or ExtraBold (800) with slight negative tracking to give question cards and test section titles a confident, modern editorial appearance.
- **Body:** Renders in Medium (500) and Regular (400) with generous line heights to preserve reading stamina during dense passages.
- **Labels & Microcopy:** Utilize SemiBold (600) and Bold (700) in compact sizes, keeping timers, question indices, and badge legends crisp and legible at a glance.

## Layout & Spacing

The layout embraces a mobile-first fluid container system centered around cozy, card-based groupings. 

- **Grid & Margins:** On mobile viewports, screens use a strict single-column fluid flow with a `16px` (`margin-mobile`) horizontal boundary. On tablet and desktop views, content is clamped to an ergonomic reading container (maximum width `640px` for exam sheets; `840px` for split-pane reference exams) centered with `margin: 24px auto`.
- **Rhythm & Gaps:** Question items, answer options, and navigation docks maintain a persistent `space-md` (`16px`) stack gap. Micro-paddings inside answer buttons and tag strips default to `space-sm` (`8px`) vertical by `space-md` (`16px`) horizontal.

## Elevation & Depth

This design system avoids harsh dropshadows or industrial multi-tier z-indices. Instead, visual hierarchy is expressed via **tonal layering**, **tinted ambient blooms**, and **low-contrast borders**:

- **Card Base:** Interactive cards float on the warm background with an ultra-soft, warm-tinted ambient shadow: `0 8px 24px -4px rgba(180, 160, 140, 0.12)`.
- **Pressed & Active Elements:** Selected options pop forward with solid pastel fills rather than sharp elevation jumps, supported by a microscopic 1.5px interior stroke (`#1C1917` or tinted pastel).
- **Persistent Bottom Dock:** Floating footer docks (holding the "Next Question", question palette, and submit buttons) use a subtle blur glass layer (`backdrop-filter: blur(12px)`) infused with `rgba(250, 246, 240, 0.85)` and an ambient top shadow.

## Shapes

The shape system adopts a pill-shaped, ultra-smooth geometry (`roundedness: 3`). Corners are deeply rounded to communicate friendliness, approachability, and ease:

- **Primary Cards & Containers:** Outfitted with `rounded-xl` (`2rem` / `32px`) or `rounded-lg` (`1.5rem` / `24px`) radii, providing a bubble-soft canvas for questions and response groups.
- **Controls & Buttons:** Strictly pill-shaped (`border-radius: 9999px`) across primary action buttons, chips, index indicators, and floating navigation controls.
- **Input Fields & Selectors:** Employ an expansive 16px to 24px radius, maintaining the organic, friendly visual language.

## Components

### Action Buttons
- **Primary ("Submit Answer", "Next"):** Full-width or pill-shaped, filled with rich charcoal (`#1C1917`) with crisp white text, or vibrant pastel pink (`#F472B6`) with charcoal text. Hover/active states trigger a soft scale dip (`scale: 0.98`).
- **Secondary ("Previous", "Flag for Review"):** Warm cream background with a subtle outline (`#E7E0D8`) and charcoal typography.

### Multiple Choice Options
- Enclosed within individual rounded pill-cards (`rounded-lg`, 20px).
- **Default State:** White background, light muted border, charcoal body text, with a circular pill identifier on the left (`A`, `B`, `C`, `D`).
- **Selected State:** Full fill in pastel lavender (`#E9D5FF`) or pastel yellow (`#FEF08A`), a crisp 1.5px charcoal outline, and an accented checkmark indicator.

### Question Navigation & Palette
- A horizontal scrolling ribbon of compact pill buttons representing question numbers.
- **Answered:** Soft solid pastel fill (green/mint or lavender).
- **Flagged:** Soft yellow fill with a tiny star icon.
- **Current Question:** Charcoal black fill with high-contrast white text.

### Chips & Badges
- Ultra-compact pill badges (`height: 28px`, `px: 12px`, `rounded-full`).
- Used for section tags (e.g., "Physics", "Reading Comprehension"), time alerts, and point allocations with pastel background tints (`#FDE047`, `#C084FC`, `#93C5FD`).

### Examination Progress Bar & Timer
- Top-anchored timer housed in an oval cream pill with an animated ticking icon.
- Thin, smooth progress bar with a soft pink gradient fill and pill-capped ends.

### Cards & Question Surfaces
- High-surface white or pale peach containers featuring generous internal padding (`space-lg` / `24px`), smoothly framing the test prompt, stimulus imagery, and answer matrices.