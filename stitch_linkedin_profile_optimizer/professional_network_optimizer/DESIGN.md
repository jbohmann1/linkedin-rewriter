---
name: Professional Network Optimizer
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#424750'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#737781'
  outline-variant: '#c3c6d2'
  surface-tint: '#2f5ea1'
  primary: '#002b5a'
  on-primary: '#ffffff'
  primary-container: '#004182'
  on-primary-container: '#84aff7'
  inverse-primary: '#a9c7ff'
  secondary: '#006c4a'
  on-secondary: '#ffffff'
  secondary-container: '#82f5c1'
  on-secondary-container: '#00714e'
  tertiary: '#1d2d41'
  on-tertiary: '#ffffff'
  tertiary-container: '#334358'
  on-tertiary-container: '#9fb0c9'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d6e3ff'
  primary-fixed-dim: '#a9c7ff'
  on-primary-fixed: '#001b3d'
  on-primary-fixed-variant: '#0c4687'
  secondary-fixed: '#85f8c4'
  secondary-fixed-dim: '#68dba9'
  on-secondary-fixed: '#002114'
  on-secondary-fixed-variant: '#005137'
  tertiary-fixed: '#d3e4fe'
  tertiary-fixed-dim: '#b7c8e1'
  on-tertiary-fixed: '#0b1c30'
  on-tertiary-fixed-variant: '#38485d'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  h1:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  h2:
    fontFamily: Inter
    fontSize: 30px
    fontWeight: '600'
    lineHeight: '1.3'
    letterSpacing: -0.01em
  h3:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.4'
    letterSpacing: '0'
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
    letterSpacing: '0'
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  body-sm:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
    letterSpacing: '0'
  label-caps:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.2'
    letterSpacing: 0.05em
  button:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.01em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 40px
  xl: 64px
  container-max: 1280px
  gutter: 24px
---

## Brand & Style
The brand personality is established on the pillars of authority, efficiency, and career advancement. It is designed to feel like a high-end productivity layer for the modern professional—offering the reliability of an enterprise tool with the agility of a specialized AI assistant. 

This design system utilizes a **Corporate / Modern** style with a focus on high-utility minimalism. The interface prioritizes content clarity and result-oriented workflows, utilizing generous whitespace and a structured information hierarchy to reduce cognitive load. The aesthetic response should be one of "effortless competence," reassuring users that their professional identity is in safe, expert hands.

## Colors
The color palette is rooted in the "Trust Blue" spectrum to establish immediate familiarity with professional networking environments. 

- **Primary (Deep Blue):** Used for navigation, primary headers, and core brand elements to signify stability and depth.
- **Secondary (Soft Emerald):** Reserved exclusively for high-priority actions, conversion points, and "Success" states, providing a vibrant, energetic contrast to the corporate blue.
- **Tertiary (Slate Gray):** Utilized for secondary text, metadata, and iconography to maintain a clean, sophisticated hierarchy.
- **Neutral (Cloud White/Slate):** A range of cool grays and whites form the background layers, ensuring the UI feels airy and modern rather than dense or dated.

## Typography
This design system relies on **Inter** for its exceptional legibility and systematic feel. The type scale is designed to handle varying lengths of professional copy, from short headlines to long-form post drafts.

Vertical rhythm is maintained through strict line-height ratios. Headlines use tighter tracking and heavier weights to anchor sections, while body text uses a generous line-height to ensure the rewritten content is easily scannable and editable. All-caps labels are used sparingly for category headers or small metadata tags to provide visual variety without sacrificing professionalism.

## Layout & Spacing
The layout follows a **Fixed Grid** model for the main content area to ensure a consistent reading experience, while the dashboard environment utilizes a flexible sidebar-and-stage composition.

A 12-column grid is employed with 24px gutters. Content blocks (like the "Original Text" and "Rewritten Text" editors) should typically sit side-by-side on desktop (6 columns each) to facilitate direct comparison. Vertical spacing follows a strict 8px linear scale, ensuring that elements feel mathematically aligned and purposeful.

## Elevation & Depth
Depth is communicated through **Tonal Layers** and **Ambient Shadows**. The design avoids heavy drop shadows in favor of a "stacked paper" aesthetic.

- **Level 0 (Background):** The base canvas uses the lightest neutral gray.
- **Level 1 (Cards/Surface):** Pure white surfaces with a subtle 1px border (#E2E8F0) and a very soft, diffused shadow (0px 4px 6px rgba(0,0,0,0.05)).
- **Level 2 (Modals/Popovers):** Higher elevation with a more pronounced shadow and a backdrop blur to focus the user’s attention on the task at hand.
- **Depth Cues:** Active states for input fields are indicated by a 2px Primary Blue border rather than a shadow, maintaining a crisp, corporate look.

## Shapes
This design system adopts a **Soft** shape language. Standard components like buttons and input fields utilize a 0.25rem (4px) corner radius. This choice strikes a balance between the precision of sharp corners and the friendliness of fully rounded shapes.

Larger containers and cards use a 0.5rem (8px) radius to feel substantial yet approachable. This geometric consistency reinforces the tool's identity as a precise, modern utility.

## Components
- **Buttons:** Primary buttons use the Soft Emerald (Secondary) background with white text to draw immediate attention. Secondary buttons use an outlined style with Primary Blue.
- **Input Fields (The Editor):** The core of the tool. Use a clean, bordered box with a subtle gray background. The "Active" state should feature a Primary Blue border. Textareas should have a "character count" label in the bottom right using the `body-sm` style.
- **Chips/Badges:** Used for "Tone Selection" (e.g., Professional, Witty, Academic). These should be light gray with Primary Blue text, switching to solid Primary Blue when selected.
- **Comparison Cards:** A specific component designed to show "Before" and "After" states. These should have a subtle header label (`label-caps`) to distinguish the versions clearly.
- **Action Bar:** A sticky or floating container at the bottom of the editor containing the "Rewrite," "Copy," and "Share" actions, ensuring the primary tools are always accessible.
- **Progress Steppers:** Horizontal indicators for multi-step profile optimization workflows, using thin lines and Primary Blue iconography.