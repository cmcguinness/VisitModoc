# Web Accessibility Checklist (WCAG 2.1 Level AA)

**Version:** 1.0  
**Standard:** WCAG 2.1 Level AA  
**Last Updated:** November 2025

## Document Structure for AI Parsing

This document uses the following conventions:
- Each checklist item has a unique ID in format `[CATEGORY-###]`
- Compliance levels: `[Level A]` (minimum), `[Level AA]` (target), `[Level AAA]` (enhanced)
- Test methods: `[Auto]` (automated tools), `[Manual]` (human testing), `[AT]` (assistive technology)
- Priority: `[Critical]`, `[High]`, `[Medium]`, `[Low]`

---

## Table of Contents

1. [Perceivable](#1-perceivable)
   - [Text Alternatives](#11-text-alternatives)
   - [Time-Based Media](#12-time-based-media)
   - [Adaptable Content](#13-adaptable-content)
   - [Distinguishable Content](#14-distinguishable-content)
2. [Operable](#2-operable)
   - [Keyboard Accessible](#21-keyboard-accessible)
   - [Enough Time](#22-enough-time)
   - [Seizures and Physical Reactions](#23-seizures-and-physical-reactions)
   - [Navigable](#24-navigable)
   - [Input Modalities](#25-input-modalities)
3. [Understandable](#3-understandable)
   - [Readable](#31-readable)
   - [Predictable](#32-predictable)
   - [Input Assistance](#33-input-assistance)
4. [Robust](#4-robust)
   - [Compatible](#41-compatible)
5. [Additional Considerations](#5-additional-considerations)

---

## 1. PERCEIVABLE

Information and user interface components must be presentable to users in ways they can perceive.

### 1.1 Text Alternatives

Provide text alternatives for non-text content.

#### [PERCEIVE-101] Images - Decorative
- [ ] **Requirement:** Decorative images have empty alt text (`alt=""`) or are implemented as CSS backgrounds
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Review all `<img>` tags and background images
- **Success:** Screen reader skips decorative images
- **Common Issues:** Missing alt attribute, alt="image" or alt="spacer"

#### [PERCEIVE-102] Images - Informative
- [ ] **Requirement:** Informative images have descriptive alt text that conveys the same information
- **Level:** [Level A] [Critical]
- **Test:** [Auto] + [Manual] Check all `<img>` tags with WAVE or axe DevTools, verify meaning
- **Success:** Alt text provides equivalent information to visual content
- **Common Issues:** Generic alt text like "image123.jpg", overly verbose descriptions
- **Example:** `<img src="chart.png" alt="Bar chart showing 25% increase in sales from Q1 to Q2 2024">`

#### [PERCEIVE-103] Images - Functional
- [ ] **Requirement:** Images used as links/buttons have alt text describing the function/destination
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Test all clickable images
- **Success:** User knows what will happen when clicking the image
- **Example:** `<a href="/search"><img src="icon.png" alt="Search"></a>`

#### [PERCEIVE-104] Complex Images
- [ ] **Requirement:** Complex images (charts, diagrams, infographics) have detailed descriptions via aria-describedby or adjacent text
- **Level:** [Level A] [High]
- **Test:** [Manual] Review complex visuals
- **Success:** All data and relationships in the image are conveyed in text
- **Example:** Use `<figure>` with detailed `<figcaption>` or link to long description

#### [PERCEIVE-105] Image Maps
- [ ] **Requirement:** Each area in an image map has appropriate alt text
- **Level:** [Level A] [Medium]
- **Test:** [Manual] Test with screen reader
- **Success:** Each clickable region is announced with its purpose

#### [PERCEIVE-106] Icons and Icon Fonts
- [ ] **Requirement:** Icon fonts and SVG icons have accessible text labels via aria-label or visually-hidden text
- **Level:** [Level A] [High]
- **Test:** [AT] Screen reader announces icon purpose
- **Example:** `<button aria-label="Close dialog"><i class="icon-close"></i></button>`

#### [PERCEIVE-107] CAPTCHA Alternatives
- [ ] **Requirement:** If CAPTCHA is used, provide alternative methods (audio CAPTCHA, logic question)
- **Level:** [Level A] [High]
- **Test:** [Manual] Try to complete CAPTCHA without vision
- **Success:** Users can verify their humanity through multiple sensory modalities

### 1.2 Time-Based Media

Provide alternatives for time-based media (audio and video).

#### [PERCEIVE-201] Audio-Only Content
- [ ] **Requirement:** Pre-recorded audio-only content has a text transcript
- **Level:** [Level A] [High]
- **Test:** [Manual] Verify transcript accuracy
- **Success:** Transcript conveys all audio information and speaker identification
- **Example:** Podcast with downloadable/accessible transcript

#### [PERCEIVE-202] Video-Only Content
- [ ] **Requirement:** Pre-recorded video-only content has audio track or text description
- **Level:** [Level A] [Medium]
- **Test:** [Manual] Verify alternative conveys same information
- **Success:** Non-visual users understand video content

#### [PERCEIVE-203] Captions for Pre-recorded Video
- [ ] **Requirement:** Pre-recorded video with audio has synchronized captions
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Play video and verify caption accuracy, timing, and speaker identification
- **Success:** Captions include all dialogue, sound effects, and relevant audio information
- **Common Issues:** Auto-generated captions with errors, missing sound descriptions

#### [PERCEIVE-204] Audio Description or Media Alternative
- [ ] **Requirement:** Pre-recorded video has audio description OR full text alternative
- **Level:** [Level A] [High]
- **Test:** [Manual] Verify visual information is conveyed
- **Success:** Users who cannot see can understand visual-only content
- **Example:** Description track describing on-screen actions, expressions, scene changes

#### [PERCEIVE-205] Captions for Live Content
- [ ] **Requirement:** Live audio content has real-time captions
- **Level:** [Level AA] [High]
- **Test:** [Manual] Verify during live broadcast
- **Success:** Captions appear with minimal delay and reasonable accuracy
- **Example:** Live webinar with professional captioning service

#### [PERCEIVE-206] Audio Description for Pre-recorded Video
- [ ] **Requirement:** Pre-recorded video has extended audio description for all visual information
- **Level:** [Level AA] [Medium]
- **Test:** [Manual] Listen to audio description track
- **Success:** All important visual information is described in audio

#### [PERCEIVE-207] Media Player Accessibility
- [ ] **Requirement:** Media player controls are keyboard accessible and screen reader compatible
- **Level:** [Level A] [High]
- **Test:** [Manual] + [AT] Navigate player with keyboard only
- **Success:** All controls (play, pause, volume, captions toggle) are reachable and operable

### 1.3 Adaptable Content

Create content that can be presented in different ways without losing information.

#### [PERCEIVE-301] Semantic Structure
- [ ] **Requirement:** HTML elements are used according to their semantic meaning
- **Level:** [Level A] [Critical]
- **Test:** [Auto] HTML validator, [Manual] Review code
- **Success:** Headers are `<h1>`-`<h6>`, lists are `<ul>`/`<ol>`, paragraphs are `<p>`, etc.
- **Common Issues:** `<div>` or `<span>` used for everything, `<table>` for layout

#### [PERCEIVE-302] Heading Hierarchy
- [ ] **Requirement:** Headings follow logical order (h1, h2, h3) without skipping levels
- **Level:** [Level A] [Critical]
- **Test:** [Auto] HeadingsMap extension, [AT] Screen reader heading navigation
- **Success:** Users can navigate by headings and understand document structure
- **Common Issues:** h1 → h3 (skipping h2), multiple h1 elements, headings chosen for visual size

#### [PERCEIVE-303] Page Title
- [ ] **Requirement:** Each page has a unique, descriptive `<title>` element
- **Level:** [Level A] [Critical]
- **Test:** [Auto] Check title tags, [Manual] Review browser tabs
- **Success:** Title identifies page topic and site (e.g., "Contact Us - ACME Corp")
- **Example:** `<title>Product Search Results - Online Store</title>`

#### [PERCEIVE-304] Reading Order
- [ ] **Requirement:** DOM order matches visual reading order
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Disable CSS and verify content order, [AT] Navigate with screen reader
- **Success:** Content makes sense when read linearly
- **Common Issues:** CSS repositioning breaking logical flow, floated elements

#### [PERCEIVE-305] Sensory Characteristics
- [ ] **Requirement:** Instructions don't rely solely on shape, size, position, or sound
- **Level:** [Level A] [High]
- **Test:** [Manual] Review all instructions
- **Success:** Instructions include multiple cues (text, icon, position)
- **Bad Example:** "Click the round button" or "Select the item on the right"
- **Good Example:** "Click the Submit button (blue, bottom right)"

#### [PERCEIVE-306] Orientation
- [ ] **Requirement:** Content works in both portrait and landscape orientations
- **Level:** [Level AA] [High]
- **Test:** [Manual] Rotate device/browser window
- **Success:** All functionality available in both orientations (unless specific orientation is essential)

#### [PERCEIVE-307] Identify Input Purpose
- [ ] **Requirement:** Form fields for user information use appropriate autocomplete attributes
- **Level:** [Level AA] [Medium]
- **Test:** [Manual] Check autocomplete attributes on forms
- **Success:** Browsers can autofill common fields (name, email, address, phone)
- **Example:** `<input type="email" name="email" autocomplete="email">`

#### [PERCEIVE-308] Tables - Headers
- [ ] **Requirement:** Data tables use `<th>` elements with proper scope attributes
- **Level:** [Level A] [Critical]
- **Test:** [AT] Screen reader table navigation
- **Success:** Screen readers announce row/column headers for each cell
- **Example:** `<th scope="col">Product</th>`, `<th scope="row">Q1 Sales</th>`

#### [PERCEIVE-309] Tables - Complex
- [ ] **Requirement:** Complex tables use `id` and `headers` attributes to associate cells
- **Level:** [Level A] [High]
- **Test:** [AT] Screen reader table navigation
- **Success:** Relationships between headers and data cells are clear
- **When:** Multi-level headers, irregular table structures

#### [PERCEIVE-310] Lists
- [ ] **Requirement:** Lists use proper markup: `<ul>`, `<ol>`, `<dl>`
- **Level:** [Level A] [Medium]
- **Test:** [Auto] + [AT] Screen reader list navigation
- **Success:** Screen readers announce "list of X items" and allow list navigation
- **Common Issues:** Using `<div>` or `<p>` with CSS bullets instead of list markup

#### [PERCEIVE-311] Section Elements with Headings
- [ ] **Requirement:** `<section>` elements contain heading elements (h2-h6) to identify their purpose
- **Level:** [Level A] [Medium]
- **Test:** [Auto] W3C HTML Validator, [Manual] Review all `<section>` elements
- **Success:** Every `<section>` element contains at least one heading that describes the section
- **Common Issues:** Using `<section>` for styling/layout purposes without semantic structure
- **Alternative:** Use `<div>` for generic containers that don't represent a distinct content section
- **Example:** `<section><h2>About Us</h2><p>...</p></section>` or use `<div class="callout">` instead
- **Reference:** HTML5 spec recommends sections have headings for accessibility and document outline

### 1.4 Distinguishable Content

Make it easier for users to see and hear content.

#### [PERCEIVE-401] Color Not Sole Indicator
- [ ] **Requirement:** Color is not the only visual means of conveying information
- **Level:** [Level A] [Critical]
- **Test:** [Manual] View in grayscale or with color blindness simulator
- **Success:** Information is still understandable without color
- **Bad Example:** "Required fields are in red"
- **Good Example:** "Required fields are marked with an asterisk (*) and highlighted in red"

#### [PERCEIVE-402] Audio Control
- [ ] **Requirement:** If audio plays automatically for >3 seconds, provide pause/stop control
- **Level:** [Level A] [High]
- **Test:** [Manual] Load page and check for auto-playing audio
- **Success:** Users can control audio without stopping all system audio
- **Best Practice:** Don't autoplay audio at all

#### [PERCEIVE-403] Contrast - Normal Text
- [ ] **Requirement:** Normal text (under 18pt or 14pt bold) has 4.5:1 contrast ratio with background
- **Level:** [Level AA] [Critical]
- **Test:** [Auto] WebAIM Contrast Checker, WAVE, or browser DevTools
- **Success:** All body text passes 4.5:1 ratio
- **Common Issues:** Light gray text on white (#999 fails, #767676 passes)
- **Tool:** https://webaim.org/resources/contrastchecker/

#### [PERCEIVE-404] Contrast - Large Text
- [ ] **Requirement:** Large text (18pt+ or 14pt+ bold) has 3:1 contrast ratio with background
- **Level:** [Level AA] [Critical]
- **Test:** [Auto] WebAIM Contrast Checker
- **Success:** Headings and large text pass 3:1 ratio
- **Note:** 18pt = 24px, 14pt bold = 18.66px bold

#### [PERCEIVE-405] Contrast - UI Components
- [ ] **Requirement:** UI components and graphical objects have 3:1 contrast ratio
- **Level:** [Level AA] [Critical]
- **Test:** [Auto] + [Manual] Check form borders, icons, focus indicators
- **Success:** Buttons, form fields, charts, and interactive elements are visible
- **Examples:** Input borders, button boundaries, chart data points, icons

#### [PERCEIVE-406] Contrast - Focus Indicators
- [ ] **Requirement:** Focus indicators have 3:1 contrast ratio against adjacent colors
- **Level:** [Level AA] [Critical]
- **Test:** [Manual] Tab through page and measure focus indicator contrast
- **Success:** Keyboard focus is always clearly visible
- **Common Issues:** Light blue focus on white background

#### [PERCEIVE-407] Text Resize
- [ ] **Requirement:** Text can be resized up to 200% without loss of content or functionality
- **Level:** [Level AA] [Critical]
- **Test:** [Manual] Zoom browser to 200% (Ctrl/Cmd +)
- **Success:** All content remains accessible, no horizontal scrolling, no text truncation
- **Common Issues:** Fixed pixel sizes, overlapping content, cut-off text

#### [PERCEIVE-408] Images of Text
- [ ] **Requirement:** Use actual text rather than images of text (except logos or essential images)
- **Level:** [Level AA] [High]
- **Test:** [Manual] Review site for text rendered as images
- **Success:** Text is selectable, resizable, and accessible to screen readers
- **Exceptions:** Logos, brand names, or when text presentation is essential

#### [PERCEIVE-409] Reflow
- [ ] **Requirement:** Content reflows to 320px width without horizontal scrolling or loss of information
- **Level:** [Level AA] [Critical]
- **Test:** [Manual] Resize browser to 320px width or zoom to 400%
- **Success:** Content adapts to narrow viewport without horizontal scrolling
- **Exceptions:** Data tables, complex diagrams, toolbars
- **Note:** Equivalent to 400% zoom at 1280px width

#### [PERCEIVE-410] Non-Text Contrast
- [ ] **Requirement:** Graphical objects required for understanding have 3:1 contrast
- **Level:** [Level AA] [High]
- **Test:** [Manual] Check icons, chart components, infographic elements
- **Success:** Important visual information is distinguishable
- **Examples:** Chart bars, pie slices, map regions, diagram components

#### [PERCEIVE-411] Text Spacing
- [ ] **Requirement:** Content is readable when text spacing is increased to specified values
- **Level:** [Level AA] [High]
- **Test:** [Manual] Apply CSS: line-height 1.5x, paragraph spacing 2x, letter spacing 0.12x, word spacing 0.16x
- **Success:** No loss of content or functionality with increased spacing
- **Test Bookmarklet:** Available at https://www.html5accessibility.com/tests/tsbookmarklet.html

#### [PERCEIVE-412] Content on Hover or Focus
- [ ] **Requirement:** Tooltips/popovers triggered by hover/focus are dismissible, hoverable, and persistent
- **Level:** [Level AA] [Medium]
- **Test:** [Manual] Test all hover/focus triggered content
- **Success:** User can dismiss without moving pointer, pointer can move to tooltip, tooltip stays visible until dismissed
- **Requirements:** Press Escape to dismiss, mouse can enter tooltip area, doesn't auto-dismiss

---

## 2. OPERABLE

User interface components and navigation must be operable.

### 2.1 Keyboard Accessible

Make all functionality available from a keyboard.

#### [OPERATE-101] Keyboard Access - All Functionality
- [ ] **Requirement:** All functionality is operable through keyboard interface
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Navigate entire site using only keyboard (Tab, Enter, Space, Arrows)
- **Success:** Every interactive element is reachable and operable
- **Common Issues:** Custom widgets, hover-only menus, drag-and-drop without keyboard alternative

#### [OPERATE-102] No Keyboard Trap
- [ ] **Requirement:** Keyboard focus is never trapped; user can always navigate away
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Tab through entire page including modals, ensure you can always exit
- **Success:** Pressing Tab or Shift+Tab always moves focus to another element
- **Common Issues:** Modal dialogs, embedded players, custom widgets

#### [OPERATE-103] Keyboard Shortcuts - No Conflicts
- [ ] **Requirement:** Single-key shortcuts can be turned off, remapped, or only active when component has focus
- **Level:** [Level A] [Medium]
- **Test:** [Manual] Test any single-key shortcuts (letters, numbers, punctuation)
- **Success:** Shortcuts don't interfere with assistive technology or browser controls
- **Exception:** Standard system shortcuts (Ctrl+C, etc.)

#### [OPERATE-104] Tab Order
- [ ] **Requirement:** Tab order follows logical reading order
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Tab through page and verify order makes sense
- **Success:** Focus moves in predictable, logical sequence
- **Common Issues:** Incorrect tabindex values, CSS positioning disrupting visual order

#### [OPERATE-105] Focus Visible
- [ ] **Requirement:** Keyboard focus indicator is visible at all times
- **Level:** [Level AA] [Critical]
- **Test:** [Manual] Tab through page and verify focus indicator is always visible
- **Success:** Current focused element is clearly indicated with sufficient contrast
- **Common Issues:** outline: none without replacement, focus indicator same color as background

#### [OPERATE-106] Skip Links
- [ ] **Requirement:** Skip navigation link provided to bypass repeated content blocks
- **Level:** [Level A] [High]
- **Test:** [Manual] Press Tab on page load
- **Success:** First Tab reveals "Skip to main content" or similar link
- **Example:** `<a href="#main" class="skip-link">Skip to main content</a>`

#### [OPERATE-107] Focus Order
- [ ] **Requirement:** Focus order preserves meaning and operability
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Navigate with keyboard and verify logical flow
- **Success:** Tabbing through interactive elements follows visual and functional logic
- **Common Issues:** Modals with focus jumping around, forms with illogical tab order

### 2.2 Enough Time

Provide users enough time to read and use content.

#### [OPERATE-201] Timing Adjustable
- [ ] **Requirement:** Time limits can be turned off, adjusted, or extended
- **Level:** [Level A] [High]
- **Test:** [Manual] Test any timed features (session timeouts, timed tests)
- **Success:** Users can extend time limit at least 10x or turn off entirely
- **Exceptions:** Real-time events (auctions), time limits >20 hours, essential security timeouts
- **Example:** Session timeout warning with option to extend

#### [OPERATE-202] Pause, Stop, Hide
- [ ] **Requirement:** Moving, blinking, scrolling, or auto-updating content can be paused, stopped, or hidden
- **Level:** [Level A] [High]
- **Test:** [Manual] Test carousels, animations, auto-updating news tickers
- **Success:** Users can control or pause any auto-moving content
- **Exceptions:** Content that moves/updates for <5 seconds
- **Examples:** Carousel with pause button, auto-updating stock ticker with pause

#### [OPERATE-203] No Timing on Form Input
- [ ] **Requirement:** No time limits on user input except for essential security
- **Level:** [Level A] [Medium]
- **Test:** [Manual] Test forms for timeout during data entry
- **Success:** Users aren't logged out while actively completing forms
- **Example:** Session timeout paused during active form interaction

#### [OPERATE-204] Interruptions
- [ ] **Requirement:** Interruptions can be postponed or suppressed (except emergencies)
- **Level:** [Level AA] [Medium]
- **Test:** [Manual] Check for auto-appearing alerts, notifications, pop-ups
- **Success:** Users can disable or control non-essential interruptions
- **Examples:** Chat widgets with minimize option, notification preferences

#### [OPERATE-205] Re-authenticating
- [ ] **Requirement:** User can continue activity after re-authenticating without data loss
- **Level:** [Level AA] [High]
- **Test:** [Manual] Let session expire during form completion, re-authenticate
- **Success:** Form data is preserved after re-authentication
- **Implementation:** Store form data in session or localStorage

### 2.3 Seizures and Physical Reactions

Do not design content in a way that is known to cause seizures or physical reactions.

#### [OPERATE-301] Three Flashes or Below Threshold
- [ ] **Requirement:** No content flashes more than 3 times per second, or flashes are below threshold
- **Level:** [Level A] [Critical]
- **Test:** [Manual] + [Tool] Photosensitive Epilepsy Analysis Tool (PEAT)
- **Success:** No rapid flashing that could trigger seizures
- **Definition:** General flash threshold: 15% of screen area, 3 flashes/sec

#### [OPERATE-302] No Three Flashes
- [ ] **Requirement:** No content flashes more than 3 times in any 1 second period
- **Level:** [Level AA] [Critical]
- **Test:** [Manual] Review all animations, videos, transitions
- **Success:** Zero flashing content throughout site
- **Safest Option:** Avoid flashing entirely

#### [OPERATE-303] Animation from Interactions
- [x] **Requirement:** Motion animation from interactions can be disabled (unless essential)
- **Level:** [Level AA] [Medium]
- **Test:** [Manual] Test with prefers-reduced-motion media query
- **Success:** Animations reduced or removed when user prefers reduced motion
- **Implementation:** `@media (prefers-reduced-motion: reduce) { * { animation: none; transition: none; }}`

### 2.4 Navigable

Provide ways to help users navigate, find content, and determine where they are.

#### [OPERATE-401] Bypass Blocks
- [ ] **Requirement:** Skip mechanism to bypass repeated navigation blocks
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Tab on page, verify skip link appears and works
- **Success:** First Tab stop is "Skip to main content" link that jumps to main content
- **Alternative:** ARIA landmarks (main, nav, aside, etc.)

#### [OPERATE-402] Page Titled
- [ ] **Requirement:** Every page has descriptive, unique title
- **Level:** [Level A] [Critical]
- **Test:** [Auto] Check `<title>` elements, [Manual] Review titles for clarity
- **Success:** Title describes page topic and site
- **Format:** "Page Name - Section - Site Name"
- **Example:** `<title>Shopping Cart - Checkout - ACME Store</title>`

#### [OPERATE-403] Focus Order Meaningful
- [ ] **Requirement:** Focus order follows meaningful sequence
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Tab through page, verify order makes sense
- **Success:** Focus moves logically through content and interactive elements
- **Related to:** [OPERATE-104] Tab Order

#### [OPERATE-404] Link Purpose in Context
- [ ] **Requirement:** Link purpose is clear from link text or surrounding context
- **Level:** [Level A] [High]
- **Test:** [Manual] Read link text alone, verify purpose is clear
- **Success:** Users understand link destination without needing surrounding text
- **Bad Example:** "Click here" or "Read more"
- **Good Example:** "Download Q4 2024 Financial Report (PDF, 2.4MB)"

#### [OPERATE-405] Multiple Ways to Navigate
- [ ] **Requirement:** Multiple ways to find pages (menu, search, site map, list)
- **Level:** [Level AA] [High]
- **Test:** [Manual] Verify at least two navigation methods available
- **Success:** Users can find content through multiple paths
- **Examples:** Main navigation + search, breadcrumbs + site map

#### [OPERATE-406] Headings and Labels
- [ ] **Requirement:** Headings and labels describe topic or purpose
- **Level:** [Level AA] [High]
- **Test:** [Manual] Review all headings and form labels
- **Success:** Headings and labels are clear, descriptive, and unique where needed
- **Bad Example:** "Details" or "Information"
- **Good Example:** "Shipping Address" or "Product Specifications"

#### [OPERATE-407] Focus Visible (Repeated)
- [ ] **Requirement:** Keyboard focus indicator is visible
- **Level:** [Level AA] [Critical]
- **Test:** [Manual] Tab through entire page
- **Success:** Focus indicator always visible with 3:1 contrast
- **Same as:** [OPERATE-105]

#### [OPERATE-408] Location
- [ ] **Requirement:** Information about user's location within site is available
- **Level:** [Level AA] [Medium]
- **Test:** [Manual] Check for breadcrumbs, highlighted nav, or current page indicator
- **Success:** Users know where they are in site hierarchy
- **Examples:** Breadcrumbs, highlighted current nav item, page heading

#### [OPERATE-409] Link Purpose (Link Only)
- [ ] **Requirement:** Link purpose can be determined from link text alone (except where ambiguous for everyone)
- **Level:** [Level AAA] [Low]
- **Test:** [Manual] Read each link out of context
- **Success:** Every link is self-descriptive
- **Note:** This is AAA (enhanced), AA only requires context

#### [OPERATE-410] Section Headings
- [ ] **Requirement:** Section headings organize content
- **Level:** [Level AAA] [Low]
- **Test:** [Manual] Review content structure
- **Success:** Content is broken into logical sections with descriptive headings
- **Note:** AAA level, but best practice for all sites

#### [OPERATE-411] Landmarks
- [ ] **Requirement:** ARIA landmarks or HTML5 sectioning elements define page regions
- **Level:** [Best Practice] [High]
- **Test:** [AT] Screen reader landmark navigation, [Auto] axe DevTools
- **Success:** Page has main, nav, aside, footer regions properly marked
- **Example:** `<main>`, `<nav>`, `<aside>`, `<footer>` or role="navigation", etc.

#### [OPERATE-412] Consistent Navigation
- [ ] **Requirement:** Navigation mechanisms appear in same location across pages
- **Level:** [Level AA] [High]
- **Test:** [Manual] Navigate between pages, verify nav location consistency
- **Success:** Navigation elements appear in same relative position site-wide
- **Common Issues:** Different nav layouts on different sections

#### [OPERATE-413] Consistent Identification
- [ ] **Requirement:** Components with same functionality are identified consistently
- **Level:** [Level AA] [High]
- **Test:** [Manual] Review icons, buttons, and elements across pages
- **Success:** Search icon always labeled "Search", print icon always labeled "Print"
- **Common Issues:** "Sign In" on one page, "Login" on another

### 2.5 Input Modalities

Make it easier for users to operate functionality through various inputs beyond keyboard.

#### [OPERATE-501] Pointer Gestures
- [ ] **Requirement:** Functions requiring multipoint or path-based gestures have single-pointer alternative
- **Level:** [Level A] [Medium]
- **Test:** [Manual] Test all touch interactions with single finger
- **Success:** No functionality requires pinch-zoom, swipe, or multi-finger gestures exclusively
- **Example:** Provide zoom buttons as alternative to pinch-zoom

#### [OPERATE-502] Pointer Cancellation
- [ ] **Requirement:** Single-pointer functions can be cancelled (mouseup/touchend required)
- **Level:** [Level A] [Medium]
- **Test:** [Manual] Press on interactive element, move pointer away before releasing
- **Success:** Action only triggered on mouseup/touchend, or can be cancelled/undone
- **Implementation:** Use click events (mouseup) rather than mousedown

#### [OPERATE-503] Label in Name
- [ ] **Requirement:** Visible label text is included in accessible name
- **Level:** [Level A] [High]
- **Test:** [Manual] + [AT] Compare visible text to screen reader announcement
- **Success:** Accessible name starts with or contains visible label text
- **Bad Example:** Button shows "Submit" but aria-label="Send form"
- **Good Example:** Button shows "Submit" and accessible name is "Submit" or "Submit Form"

#### [OPERATE-504] Motion Actuation
- [ ] **Requirement:** Functions activated by device motion can be disabled and have UI alternative
- **Level:** [Level A] [Medium]
- **Test:** [Manual] Test any shake-to-undo or tilt features
- **Success:** Motion activation can be turned off, UI control available
- **Examples:** Shake to refresh with refresh button, tilt navigation with arrow keys

#### [OPERATE-505] Target Size
- [ ] **Requirement:** Touch targets are at least 44×44 CSS pixels (with exceptions)
- **Level:** [Level AAA] [Medium]
- **Test:** [Manual] Measure clickable areas with browser DevTools
- **Success:** Buttons, links, and form controls meet minimum size
- **Exceptions:** Inline links in text, targets with sufficient spacing, essential small targets
- **Best Practice:** 48×48px or larger, 8px spacing between targets

---

## 3. UNDERSTANDABLE

Information and user interface operation must be understandable.

### 3.1 Readable

Make text content readable and understandable.

#### [UNDERSTAND-101] Language of Page
- [ ] **Requirement:** Default human language of page is programmatically determined
- **Level:** [Level A] [Critical]
- **Test:** [Auto] Check `<html lang="en">` attribute
- **Success:** html element has lang attribute with valid language code
- **Example:** `<html lang="en">` for English, `<html lang="es">` for Spanish
- **Tool:** Use ISO 639-1 language codes

#### [UNDERSTAND-102] Language of Parts
- [ ] **Requirement:** Language changes within content are marked with lang attribute
- **Level:** [Level AA] [High]
- **Test:** [Manual] Review multilingual content
- **Success:** Any content in different language has lang attribute
- **Example:** `<span lang="fr">Bonjour</span>` within English page

#### [UNDERSTAND-103] Reading Level
- [ ] **Requirement:** Supplemental content or simplified version available for text requiring advanced reading ability
- **Level:** [Level AAA] [Low]
- **Test:** [Manual] + [Tool] Flesch-Kincaid readability test
- **Success:** Complex content has plain language alternative
- **Exception:** Technical documentation where advanced reading is required
- **Target:** 8th-9th grade reading level for general audience

#### [UNDERSTAND-104] Unusual Words
- [ ] **Requirement:** Mechanism available for identifying specific definitions of words used unusually
- **Level:** [Level AAA] [Low]
- **Test:** [Manual] Review for idioms, jargon, technical terms
- **Success:** Definitions, glossary, or tooltips available for unusual usage
- **Example:** Glossary page linked from footer, inline definitions

#### [UNDERSTAND-105] Abbreviations
- [ ] **Requirement:** Mechanism for identifying expanded form of abbreviations
- **Level:** [Level AAA] [Low]
- **Test:** [Manual] Check all abbreviations have explanation
- **Success:** First use of abbreviation includes full text, or glossary available
- **Example:** `<abbr title="Web Content Accessibility Guidelines">WCAG</abbr>`

#### [UNDERSTAND-106] Pronunciation
- [ ] **Requirement:** Pronunciation provided where meaning ambiguous without it
- **Level:** [Level AAA] [Low]
- **Test:** [Manual] Review content for words with ambiguous pronunciation
- **Success:** Pronunciation guide available for proper nouns, technical terms
- **Example:** IPA notation, audio pronunciation, or parenthetical guide

### 3.2 Predictable

Make web pages appear and operate in predictable ways.

#### [UNDERSTAND-201] On Focus
- [ ] **Requirement:** Receiving focus doesn't automatically trigger change of context
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Tab through page and verify no unexpected actions
- **Success:** Focusing an element doesn't open modals, submit forms, or change page
- **Acceptable:** Focus triggering visible change (dropdown appearing) is fine
- **Not Acceptable:** Focus automatically selecting option or submitting form

#### [UNDERSTAND-202] On Input
- [ ] **Requirement:** Changing form input doesn't automatically trigger change of context unless user is warned
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Interact with all form controls
- **Success:** Changing input doesn't auto-submit form or navigate away without warning
- **Acceptable:** Auto-suggest dropdown appearing
- **Not Acceptable:** Selecting dropdown option auto-submits form (unless warned)

#### [UNDERSTAND-203] Consistent Navigation
- [ ] **Requirement:** Navigation mechanisms repeated on multiple pages appear in same order
- **Level:** [Level AA] [High]
- **Test:** [Manual] Compare navigation across pages
- **Success:** Navigation menu, search box, breadcrumbs in consistent position
- **Acceptable:** User can customize navigation order
- **Related to:** [OPERATE-412]

#### [UNDERSTAND-204] Consistent Identification
- [ ] **Requirement:** Components with same functionality are identified consistently
- **Level:** [Level AA] [High]
- **Test:** [Manual] Review recurring elements across pages
- **Success:** Same icon/label used for same function site-wide
- **Related to:** [OPERATE-413]

#### [UNDERSTAND-205] Change on Request
- [ ] **Requirement:** Context changes only occur on user request or user can turn off auto-changes
- **Level:** [Level AAA] [Low]
- **Test:** [Manual] Review all automatic behaviors
- **Success:** All major changes (new window, form submission, navigation) require explicit action
- **Example:** Provide "Submit" button rather than auto-submit on last field

#### [UNDERSTAND-206] Navigation Consistency
- [ ] **Requirement:** Repeated navigation follows same relative order unless user initiates change
- **Level:** [Best Practice] [Medium]
- **Test:** [Manual] Navigate site, verify menu order doesn't randomly change
- **Success:** Navigation structure remains stable across user session

### 3.3 Input Assistance

Help users avoid and correct mistakes.

#### [UNDERSTAND-301] Error Identification
- [ ] **Requirement:** Input errors are identified and described to user in text
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Submit forms with errors
- **Success:** Error messages clearly indicate which fields have errors and why
- **Bad Example:** "Error: Invalid input"
- **Good Example:** "Email Address: Please enter a valid email address (e.g., user@example.com)"

#### [UNDERSTAND-302] Labels or Instructions
- [ ] **Requirement:** Labels or instructions provided when content requires user input
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Review all form fields
- **Success:** Every input has visible label, required fields marked, format examples provided
- **Examples:** "Email Address (required)", "Date (MM/DD/YYYY)", "Password (8+ characters)"

#### [UNDERSTAND-303] Error Suggestion
- [ ] **Requirement:** Suggestions for correcting errors provided (unless security risk)
- **Level:** [Level AA] [High]
- **Test:** [Manual] Submit forms with various error types
- **Success:** Error messages suggest how to fix the problem
- **Example:** "Password too short. Please enter at least 8 characters."
- **Exception:** Security-sensitive fields (don't reveal password requirements on login form)

#### [UNDERSTAND-304] Error Prevention (Legal, Financial, Data)
- [ ] **Requirement:** For legal/financial transactions, submissions are reversible, checked, or confirmed
- **Level:** [Level AA] [Critical]
- **Test:** [Manual] Test critical transactions
- **Success:** One of: reversible action, data checked before submission, confirmation step with review
- **Examples:** "Review Order" page before purchase, "Undo" option, validation before submission

#### [UNDERSTAND-305] Help
- [ ] **Requirement:** Context-sensitive help available
- **Level:** [Level AAA] [Low]
- **Test:** [Manual] Review complex forms and processes
- **Success:** Help text, tooltips, or links to help available at point of use
- **Examples:** "?" icons with explanations, inline help text, "Learn more" links

#### [UNDERSTAND-306] Error Prevention (All)
- [ ] **Requirement:** All user input requiring submission is checked or confirmed
- **Level:** [Level AAA] [Low]
- **Test:** [Manual] Test all forms
- **Success:** Even simple forms have confirmation or validation
- **Note:** AAA level - extends error prevention to all forms

#### [UNDERSTAND-307] Required Field Identification
- [ ] **Requirement:** Required form fields are clearly marked and programmatically indicated
- **Level:** [Level A] [Critical]
- **Test:** [Manual] + [AT] Review form fields
- **Success:** Required fields have visual indicator (* or "required") and aria-required="true"
- **Example:** `<label>Email <span aria-label="required">*</span></label><input aria-required="true">`

#### [UNDERSTAND-308] Form Validation
- [ ] **Requirement:** Input validation provides clear, specific feedback
- **Level:** [Level A] [High]
- **Test:** [Manual] Test various invalid inputs
- **Success:** Validation messages are specific, not generic
- **Bad Example:** "Invalid input"
- **Good Example:** "Phone number must be 10 digits (###-###-####)"

#### [UNDERSTAND-309] Error Summary
- [ ] **Requirement:** Form errors presented in summary at top of page with links to errors
- **Level:** [Best Practice] [High]
- **Test:** [Manual] Submit form with multiple errors
- **Success:** Error summary appears with count and links to each error
- **Example:** "3 errors found: Email address invalid (jump to field), Password too short (jump to field)"

---

## 4. ROBUST

Content must be robust enough to be interpreted reliably by a wide variety of user agents, including assistive technologies.

### 4.1 Compatible

Maximize compatibility with current and future user agents, including assistive technologies.

#### [ROBUST-101] Parsing / Valid HTML
- [ ] **Requirement:** HTML is well-formed (complete start/end tags, properly nested, unique IDs, no duplicate attributes)
- **Level:** [Level A] [High]
- **Test:** [Auto] W3C HTML Validator (https://validator.w3.org/)
- **Success:** No critical parsing errors
- **Common Issues:** Missing closing tags, duplicate IDs, malformed attributes
- **Note:** WCAG 2.1 deprecated the specific parsing requirement, but valid HTML is still best practice

#### [ROBUST-102] Name, Role, Value
- [ ] **Requirement:** UI components have programmatically determinable name, role, state, and value
- **Level:** [Level A] [Critical]
- **Test:** [AT] Screen reader announces component purpose and state
- **Success:** Screen readers correctly announce what element is and current state
- **Examples:** Button role, current state of checkbox, slider value, expanded/collapsed accordion

#### [ROBUST-103] Status Messages
- [ ] **Requirement:** Status messages presented without receiving focus can be determined by assistive technologies
- **Level:** [Level AA] [High]
- **Test:** [AT] Screen reader announces status updates
- **Success:** Notifications, loading states, success messages announced via ARIA live regions
- **Implementation:** role="status" (polite) or role="alert" (assertive) or aria-live
- **Examples:** "Item added to cart", "Saving...", "3 results found"

#### [ROBUST-104] ARIA Usage - Valid Roles
- [ ] **Requirement:** ARIA roles, states, and properties are used correctly per specification
- **Level:** [Level A] [Critical]
- **Test:** [Auto] axe DevTools, WAVE, or validator
- **Success:** ARIA attributes follow specification, no invalid combinations
- **Common Issues:** role="presentation" on focusable elements, invalid role values

#### [ROBUST-105] ARIA Usage - Required Attributes
- [ ] **Requirement:** ARIA roles have all required attributes
- **Level:** [Level A] [Critical]
- **Test:** [Auto] axe DevTools, WAVE
- **Success:** Roles like checkbox have aria-checked, sliders have aria-valuenow, etc.
- **Example:** `<div role="checkbox" aria-checked="true">` includes required aria-checked

#### [ROBUST-106] ARIA Usage - Valid Values
- [ ] **Requirement:** ARIA attributes have valid values for their type
- **Level:** [Level A] [High]
- **Test:** [Auto] axe DevTools, WAVE
- **Success:** aria-checked="true|false|mixed", aria-expanded="true|false", etc.
- **Common Issues:** aria-hidden="yes" (should be "true"), aria-checked="1" (should be "true")

#### [ROBUST-107] Unique IDs
- [ ] **Requirement:** ID attributes are unique across page
- **Level:** [Level A] [High]
- **Test:** [Auto] HTML Validator, axe DevTools
- **Success:** Every ID appears only once per page
- **Impact:** Breaks label associations, ARIA relationships, anchor links

#### [ROBUST-108] Form Labels
- [ ] **Requirement:** Form inputs have associated labels using for/id or aria-labelledby
- **Level:** [Level A] [Critical]
- **Test:** [Auto] + [AT] Click labels, use screen reader
- **Success:** Clicking label focuses input, screen reader announces label
- **Example:** `<label for="email">Email</label><input id="email">`

#### [ROBUST-109] ARIA Landmark Roles
- [ ] **Requirement:** Page regions use appropriate landmark roles or HTML5 elements
- **Level:** [Best Practice] [High]
- **Test:** [AT] Screen reader landmark navigation
- **Success:** main, navigation, search, banner, contentinfo landmarks present
- **HTML5:** `<main>`, `<nav>`, `<aside>`, `<header>`, `<footer>`

#### [ROBUST-110] Live Regions
- [ ] **Requirement:** Dynamic content updates use ARIA live regions appropriately
- **Level:** [Level AA] [High]
- **Test:** [AT] Screen reader announces dynamic updates
- **Success:** Loading states, search results, form submission feedback announced
- **Levels:** aria-live="polite" (wait for pause), aria-live="assertive" (immediate)

#### [ROBUST-111] Button vs Link Semantics
- [ ] **Requirement:** Buttons and links used semantically correct
- **Level:** [Level A] [High]
- **Test:** [Manual] Review interactive elements
- **Success:** Links navigate (`<a href>`), buttons perform actions (`<button>`)
- **Rule:** If it goes somewhere = link. If it does something = button.

#### [ROBUST-112] Accessible Name Calculation
- [ ] **Requirement:** All interactive elements have accessible names
- **Level:** [Level A] [Critical]
- **Test:** [AT] Screen reader announces meaningful name for every control
- **Success:** No elements announced as "button" or "link" without description
- **Priority:** 1) aria-labelledby, 2) aria-label, 3) visible label, 4) title attribute

---

## 5. ADDITIONAL CONSIDERATIONS

### 5.1 Mobile Accessibility

#### [MOBILE-101] Touch Target Size
- [ ] **Requirement:** Touch targets minimum 44×44 CSS pixels with adequate spacing
- **Level:** [Best Practice] [High]
- **Test:** [Manual] Test on mobile device
- **Success:** Buttons easily tappable without accidentally hitting adjacent elements

#### [MOBILE-102] Orientation Support
- [ ] **Requirement:** App/site works in both portrait and landscape
- **Level:** [Level AA] [High]
- **Test:** [Manual] Rotate device
- **Success:** All functionality available in both orientations

#### [MOBILE-103] Touch Gestures
- [ ] **Requirement:** Complex gestures have simple alternatives
- **Level:** [Level A] [Medium]
- **Test:** [Manual] Test all interactions
- **Success:** No required swipes, pinches, or multi-touch without alternatives

#### [MOBILE-104] Motion and Animation
- [x] **Requirement:** Respects prefers-reduced-motion setting
- **Level:** [Level AA] [Medium]
- **Test:** [Manual] Enable reduced motion on device
- **Success:** Animations reduced or removed

### 5.2 Forms

#### [FORMS-101] Label Association
- [ ] **Requirement:** All form controls have explicit labels
- **Level:** [Level A] [Critical]
- **Test:** [Auto] + [Manual] Click labels, verify focus moves to control
- **Success:** `<label for="id">` associated with control

#### [FORMS-102] Fieldset and Legend
- [ ] **Requirement:** Related form controls grouped with fieldset/legend
- **Level:** [Level A] [High]
- **Test:** [AT] Screen reader announces group label
- **Success:** Radio button groups and checkbox groups use fieldset
- **Example:** `<fieldset><legend>Shipping Method</legend>...</fieldset>`

#### [FORMS-103] Required Fields
- [ ] **Requirement:** Required status indicated visually and programmatically
- **Level:** [Level A] [Critical]
- **Test:** [AT] Screen reader announces "required"
- **Success:** aria-required="true" and visual indicator (* or "required")

#### [FORMS-104] Input Purpose
- [ ] **Requirement:** Autocomplete attributes on personal info fields
- **Level:** [Level AA] [Medium]
- **Test:** [Manual] Check autocomplete attributes
- **Success:** Email, name, phone, address fields have autocomplete
- **Example:** `<input type="email" autocomplete="email">`

#### [FORMS-105] Error Recovery
- [ ] **Requirement:** Failed form submissions preserve user data
- **Level:** [Best Practice] [High]
- **Test:** [Manual] Submit form with errors
- **Success:** All fields retain entered values

### 5.3 Custom Components

#### [CUSTOM-101] Keyboard Interaction Patterns
- [ ] **Requirement:** Custom widgets follow ARIA Authoring Practices (APG) patterns
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Use keyboard with custom components
- **Success:** Tab, Enter, Space, Arrows work as expected per APG
- **Reference:** https://www.w3.org/WAI/ARIA/apg/patterns/

#### [CUSTOM-102] Focus Management
- [ ] **Requirement:** Modals, dialogs trap and restore focus appropriately
- **Level:** [Level A] [Critical]
- **Test:** [Manual] Open modal with keyboard, verify focus trapped
- **Success:** Focus moves to modal on open, cycles within modal, returns to trigger on close

#### [CUSTOM-103] ARIA State Management
- [ ] **Requirement:** Component states reflected in ARIA attributes
- **Level:** [Level A] [Critical]
- **Test:** [AT] Screen reader announces state changes
- **Success:** aria-expanded, aria-selected, aria-checked update dynamically

### 5.4 Content Management

#### [CONTENT-101] PDF Accessibility
- [ ] **Requirement:** PDF documents are tagged and accessible or HTML alternative provided
- **Level:** [Level A] [High]
- **Test:** [AT] Screen reader can read PDF content
- **Success:** PDFs have proper structure, reading order, alt text

#### [CONTENT-102] Document Downloads
- [ ] **Requirement:** File type, size, and language indicated for downloads
- **Level:** [Best Practice] [Medium]
- **Test:** [Manual] Review download links
- **Success:** Link text includes format and size
- **Example:** "Annual Report 2024 (PDF, 3.2 MB)"

#### [CONTENT-103] Office Documents
- [ ] **Requirement:** Word, Excel, PowerPoint documents are accessible
- **Level:** [Best Practice] [High]
- **Test:** [Manual] Use built-in accessibility checkers
- **Success:** Documents have proper structure, alt text, color contrast

### 5.5 Multimedia

#### [MEDIA-101] Video Player Controls
- [ ] **Requirement:** Custom video players have accessible controls
- **Level:** [Level A] [Critical]
- **Test:** [Manual] + [AT] Keyboard navigate player
- **Success:** All controls reachable by keyboard, labeled for screen readers

#### [MEDIA-102] Audio Descriptions
- [ ] **Requirement:** Video with important visual info has audio descriptions
- **Level:** [Level AA] [Medium]
- **Test:** [Manual] Listen to description track
- **Success:** Visual-only content described in audio

#### [MEDIA-103] Transcript Accuracy
- [ ] **Requirement:** Transcripts include all audio and important visual info
- **Level:** [Level A] [High]
- **Test:** [Manual] Compare transcript to content
- **Success:** Transcript complete and accurate with speaker identification

### 5.6 Dynamic Content

#### [DYNAMIC-101] AJAX Updates
- [ ] **Requirement:** AJAX content updates announced to screen readers
- **Level:** [Level AA] [High]
- **Test:** [AT] Trigger AJAX update, verify announcement
- **Success:** aria-live region announces changes

#### [DYNAMIC-102] Infinite Scroll
- [ ] **Requirement:** Infinite scroll has pause mechanism and keyboard access to footer
- **Level:** [Best Practice] [High]
- **Test:** [Manual] Keyboard navigate through infinite scroll
- **Success:** Can reach footer, option to load more explicitly

#### [DYNAMIC-103] Single Page Apps
- [ ] **Requirement:** Route changes update page title and announce to screen readers
- **Level:** [Level AA] [High]
- **Test:** [AT] Navigate between SPA routes
- **Success:** Page title updates, route change announced

---

## Testing Tools Reference

### Automated Testing Tools
- **WAVE** (Web Accessibility Evaluation Tool): https://wave.webaim.org/
- **axe DevTools**: Browser extension for Chrome/Firefox/Edge
- **Lighthouse**: Built into Chrome DevTools
- **Pa11y**: Command-line testing tool
- **HTML Validator**: https://validator.w3.org/
- **Color Contrast Checker**: https://webaim.org/resources/contrastchecker/

### Screen Readers
- **NVDA**: Free, Windows (https://www.nvaccess.org/)
- **JAWS**: Commercial, Windows (https://www.freedomscientific.com/products/software/jaws/)
- **VoiceOver**: Built into macOS and iOS
- **TalkBack**: Built into Android
- **Narrator**: Built into Windows

### Browser Extensions
- **HeadingsMap**: Visualize heading structure
- **Landmarks**: Show ARIA landmarks
- **WCAG Color Contrast Checker**: Check color contrast
- **Accessibility Insights**: Microsoft's accessibility testing extension

### Manual Testing Checklist
1. Keyboard navigation (Tab, Shift+Tab, Enter, Space, Arrows)
2. Screen reader testing (NVDA or VoiceOver)
3. 200% zoom test
4. Color contrast measurement
5. Color blindness simulation
6. Mobile device testing
7. Reduced motion testing

---

## Quick Reference - Critical Issues

These are the most common and impactful accessibility barriers:

1. **Missing alt text on images** [PERCEIVE-102]
2. **Insufficient color contrast** [PERCEIVE-403, 404]
3. **Keyboard inaccessibility** [OPERATE-101]
4. **Missing or incorrect form labels** [ROBUST-108]
5. **No visible focus indicator** [OPERATE-105]
6. **Missing page titles** [OPERATE-402]
7. **Missing heading structure** [PERCEIVE-302]
8. **Missing video captions** [PERCEIVE-203]
9. **Missing ARIA on custom components** [ROBUST-102]
10. **Missing skip navigation link** [OPERATE-401]

---

## Compliance Levels Summary

- **Level A** (Minimum): Basic accessibility features. Failure creates serious barriers.
- **Level AA** (Target): Addresses major barriers. This is the legal standard in most jurisdictions.
- **Level AAA** (Enhanced): Highest level. Not required for full compliance but provides best experience.

**Recommendation:** Aim for **Level AA compliance** as the baseline, incorporate AAA where feasible.

---

## Document Changelog

- **v1.0** (November 2025): Initial comprehensive checklist based on WCAG 2.1 Level AA standards

---

## License and Attribution

This checklist is based on the Web Content Accessibility Guidelines (WCAG) 2.1 published by the W3C Web Accessibility Initiative (WAI). WCAG documentation is available at https://www.w3.org/WAI/WCAG21/quickref/

This document may be freely used and modified for accessibility testing and compliance purposes.
