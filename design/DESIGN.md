---
name: MANAger
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#3e4a3d'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#6e7b6c'
  outline-variant: '#bdcaba'
  surface-tint: '#006e2d'
  primary: '#006b2c'
  on-primary: '#ffffff'
  primary-container: '#00873a'
  on-primary-container: '#f7fff2'
  inverse-primary: '#62df7d'
  secondary: '#904d00'
  on-secondary: '#ffffff'
  secondary-container: '#fe932c'
  on-secondary-container: '#663500'
  tertiary: '#a72d51'
  on-tertiary: '#ffffff'
  tertiary-container: '#c74668'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#7ffc97'
  primary-fixed-dim: '#62df7d'
  on-primary-fixed: '#002109'
  on-primary-fixed-variant: '#005320'
  secondary-fixed: '#ffdcc3'
  secondary-fixed-dim: '#ffb77d'
  on-secondary-fixed: '#2f1500'
  on-secondary-fixed-variant: '#6e3900'
  tertiary-fixed: '#ffd9de'
  tertiary-fixed-dim: '#ffb2bf'
  on-tertiary-fixed: '#3f0016'
  on-tertiary-fixed-variant: '#8a143c'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  title-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  title-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 22px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system establishes a friendly, clean, and approachable aesthetic tailored for university students in Jerusalem navigating tight budgets. The interface balances practical utility with warmth, evoking a sense of financial control, smart decision-making, and everyday ease without feeling clinical or overwhelming.

The visual language blends **Minimalism** with **Corporate / Modern** principles:
- **Generous whitespace and crisp surfaces** keep dense grocery price comparisons and weekly meal plans scannable on small mobile screens.
- **Approachable geometry** through rounded cards and buttons softens the transactional nature of budgeting.
- **Subtle warm touches** paired with a fresh green accent communicate savings, freshness, and optimism.

## Colors

The palette is built on a **light** color mode, prioritizing crisp white and light neutral surfaces to maximize legibility in bright outdoor or campus environments.

- **Primary (`#16A34A`):** A fresh, energetic green used for primary actions, savings highlights, best-price indicators, and active states.
- **Secondary (`#D97706`):** A subtle warm amber used sparingly for deal badges, budget alerts, and warm accents that echo local Jerusalem stone and sunlight.
- **Neutral (`#64748B`):** A balanced slate neutral that anchors body text, secondary labels, and subtle dividers against crisp white (`#FFFFFF`) and soft off-white (`#F8FAFC`) backgrounds.

### Usage Rules
- Reserve the primary green for high-priority CTAs (e.g., "Add to Meal Plan", "Compare Prices") and positive savings metrics.
- Use tinted neutral surfaces (`#F8FAFC`, `#F1F5F9`) to separate cards and list sections without heavy borders.

## Typography

The typography pairs **Plus Jakarta Sans** for headlines with **Inter** for body copy and UI labels, balancing a friendly, welcoming personality with high-density legibility for prices and ingredient lists.

- **Headlines (`Plus Jakarta Sans`):** Soft, rounded terminals give page titles and section headers an approachable tone. On mobile viewports, `headline-lg-mobile` (28px) replaces `headline-lg` (36px) to prevent wrapping on narrow screens.
- **Body & Labels (`Inter`):** Clean, neutral, and highly legible at small sizes, ensuring unit prices, weights, and store names remain effortless to scan. Use tabular numerals (`tabular-nums`) for all currency and price comparison columns.

## Layout & Spacing

The design system uses a **mobile-first fluid grid** that adapts cleanly across viewports:

- **Mobile (< 640px):** 4-column fluid grid with `1rem` (16px) outer margins and `1rem` (16px) gutters. Most cards and meal-plan modules span all 4 columns, while quick-action tiles or price-comparison pairs span 2 columns each.
- **Tablet (640px – 1024px):** 8-column fluid grid with `1.5rem` (24px) outer margins and `1rem` (16px) gutters. Cards reflow into 2-column grids (4 columns each).
- **Desktop (> 1024px):** 12-column fluid grid capped at a comfortable reading width (1200px max), with `2rem` (32px) margins.

### Spacing Rhythm
- Use `space-xs` (4px) and `space-sm` (8px) for tight internal groupings, such as icon-to-label gaps and stacked price metadata.
- Use `space-md` (16px) for standard card padding and vertical rhythm between list items.
- Use `space-lg` (24px) and `space-xl` (32px) to separate major sections on a screen.

## Elevation & Depth

Visual hierarchy relies on **tonal layers** supported by **low-contrast outlines** and **subtle ambient shadows**, keeping the interface light and airy:

- **Base Canvas:** Soft off-white (`#F8FAFC`) provides a calm backdrop.
- **Primary Cards:** Crisp white (`#FFFFFF`) surfaces sit on top of the base canvas, defined by a 1px low-contrast outline (`rgba(100, 116, 139, 0.12)`) and a whisper-soft ambient shadow (`0 2px 8px rgba(15, 23, 42, 0.04)`).
- **Interactive / Floating Elements:** Sticky bottom navigation, floating action buttons, and active dropdowns use a slightly deeper diffused shadow (`0 8px 24px rgba(15, 23, 42, 0.08)`) to clearly separate from scrolling content.

## Shapes

The design system uses a **Rounded** (`2`) shape language to reinforce a friendly, approachable feel:

- **Standard Controls (`0.5rem` / 8px):** Input fields, checkboxes, and small utility buttons.
- **Cards & Containers (`1rem` / 16px, `rounded-lg`):** Meal plan cards, grocery store comparison blocks, and modal sheets.
- **Pills & Badges (`1.5rem` / 24px, `rounded-xl` or full pill):** Filter chips, savings tags, and primary pill buttons.

## Components

### Buttons
- **Primary Button:** Solid primary green (`#16A34A`) background, white `label-lg` text, `0.5rem` (or full-pill for key CTAs) radius, and `12px 20px` padding.
- **Secondary Button:** Soft tinted green (`rgba(22, 163, 74, 0.1)`) background with primary green text, or crisp white with a 1px low-contrast outline.
- **Touch Targets:** Minimum height of `44px` on mobile for comfortable thumb interaction.

### Chips
- Used for dietary filters (e.g., "Kosher", "Vegetarian", "Under ₪15") and store selectors.
- Unselected chips use `#F1F5F9` background with `#475569` text; selected chips switch to primary green with white text.

### Lists
- Grocery and ingredient lists use crisp white rows with `space-md` (16px) horizontal padding, `space-sm` (8px) vertical gaps, and subtle `1px` dividers (`#E2E8F0`).
- Right-align prices using `tabular-nums` for instant vertical scanning.

### Checkboxes & Radio Buttons
- `20px × 20px` touch-friendly controls with `0.25rem` radius for checkboxes and full circle for radios.
- Checked states fill with primary green (`#16A34A`) and a crisp white checkmark.

### Input Fields
- Crisp white background, `1px` neutral border (`#CBD5E1`), `0.5rem` radius, and `44px` minimum height.
- Focus state applies a `2px` primary green ring (`rgba(22, 163, 74, 0.25)`).

### Cards
- Crisp white (`#FFFFFF`) surface, `1rem` (`rounded-lg`) radius, `space-md` (16px) internal padding, and subtle ambient shadow.

### Product-Specific Components
- **Price Comparison Badge:** A compact pill badge highlighting the cheapest store in primary green (`Best Price: Rami Levy`) or a warm amber (`Save ₪4.50`) tag.
- **Budget Progress Bar:** A rounded `8px`-tall track (`#E2E8F0`) filled with primary green that transitions to warm amber (`#D97706`) when approaching 85% of the weekly student budget.
- **Meal Plan Day Card:** Collapsible card displaying the day header, total estimated cost in `title-md`, and nested ingredient rows.
