# Reveal.js Site Map

Use this as the feature inventory for Reveal.js deck work. The source pages are the official docs at `https://revealjs.com/`.

## Getting Started

- [Installation](https://revealjs.com/installation/): choose basic browser-only setup, full npm setup, development server port, or npm package usage.
- [Markup](https://revealjs.com/markup/): core structure is `.reveal > .slides > section`; nested `section` creates vertical slides; slide state classes support styling.
- [Markdown](https://revealjs.com/markdown/): `data-markdown` slides, external Markdown files, horizontal/vertical separators, element attributes, slide attributes, syntax highlighting, line number offset, and marked configuration.
- [React](https://revealjs.com/react/): official `@revealjs/react` wrapper for component-authored decks; use only when React is already part of the project or specifically requested.
- [React manual setup](https://revealjs.com/react-legacy/): legacy/manual initialization guidance; avoid for new React decks unless maintaining old code.

## Content Features

- [Backgrounds](https://revealjs.com/backgrounds/): color, gradient, image, video, iframe, background transitions, and parallax backgrounds via `data-background*` attributes.
- [Media](https://revealjs.com/media/): autoplay, lazy loading, iframe behavior, iframe postMessage, automatic pause/resume, and `data-prevent-swipe` for touch-heavy content.
- [Lightbox](https://revealjs.com/lightbox/): image, video, iframe, and arbitrary-element lightboxes through `data-preview-image`, `data-preview-video`, and related attributes.
- [Code](https://revealjs.com/code/): Highlight.js plugin, syntax themes, line numbers, line highlights, step-by-step highlights, language selection, HTML escaping, and manual highlighting.
- [Math](https://revealjs.com/math/): KaTeX and MathJax support through the math plugin; pick one typesetter and load only what the deck needs.
- [Fragments](https://revealjs.com/fragments/): incremental reveals, custom fragment styles, nested fragments, explicit `data-fragment-index`, and fragment events.
- [Links](https://revealjs.com/links/): internal slide IDs, numbered links, relative navigation buttons, and lightbox links.
- [Layout](https://revealjs.com/layout/): `r-stack`, fit text, stretch, and frame helpers. Use these for slide mechanics, not as a substitute for a theme grid.
- [Slide Visibility](https://revealjs.com/slide-visibility/): `data-visibility="hidden"` removes slides; `data-visibility="uncounted"` keeps optional slides out of progress and slide numbering.

## Customization

- [Themes](https://revealjs.com/themes/): built-in theme stylesheets and CSS custom properties. Use a theme stylesheet plus overrides for deck-specific identity.
- [Transitions](https://revealjs.com/transitions/): global and per-slide transitions, separate in/out transitions, transition speed, and background transitions.
- [Config Options](https://revealjs.com/config/): initialization options for layout, controls, navigation, progress, history/hash, interaction, fragments, media, view modes, and plugins.
- [Presentation Size](https://revealjs.com/presentation-size/): `width`, `height`, `margin`, `minScale`, and `maxScale` determine the design canvas and scaling behavior.

## Presentation Features

- [Vertical Slides](https://revealjs.com/vertical-slides/): nested stacks. Use for optional depth, demos, or drill-downs; do not hide core narrative vertically.
- [Auto-Animate](https://revealjs.com/auto-animate/): smooth transitions between similar elements across adjacent slides. Use for evolving diagrams, comparisons, and progressive UI states.
- [Auto-Slide](https://revealjs.com/auto-slide/): timed navigation for kiosk, looping demos, and unattended decks.
- [Speaker View](https://revealjs.com/speaker-view/): presenter notes, current/next slide, timer, and speaker-only controls through the Notes plugin.
- [Scroll View](https://revealjs.com/scroll-view/): document-like presentation mode for long reading surfaces and articles.
- [Slide Numbers](https://revealjs.com/slide-numbers/): display modes and context controls for slide numbers.
- [Jump to Slide](https://revealjs.com/jump-to-slide/): keyboard shortcut to jump by number or slide ID; disable for locked-down kiosks.
- [Touch Navigation](https://revealjs.com/touch-navigation/): swipe navigation and `touch: false` for disabling it.
- [PDF Export](https://revealjs.com/pdf-export/): Chrome/Chromium print route, speaker notes, page numbers, page size, and separate pages for fragments.
- [Overview Mode](https://revealjs.com/overview/): `ESC`/`O` overview and API/events for overview state.
- [Fullscreen Mode](https://revealjs.com/fullscreen/): `F` keyboard fullscreen support.

## API And Plugins

- [Initialization](https://revealjs.com/initialization/): global `Reveal.initialize`, multiple presentation instances, ES module usage, and destroy/uninitialize behavior.
- [API Methods](https://revealjs.com/api/): navigation, fragments, slide queries, state, modes, DOM elements, sync, layout, and configuration methods.
- [Events](https://revealjs.com/events/): ready, slide changed, transition end, resize, and feature-specific events.
- [Keyboard](https://revealjs.com/keyboard/): config-level keyboard overrides plus runtime `addKeyBinding` and `removeKeyBinding`.
- [Presentation State](https://revealjs.com/presentation-state/): `getState` and `setState` for restoring navigation, fragments, pause, and overview state.
- [postMessage](https://revealjs.com/postmessage/): control decks inside another window or iframe and receive bubbled events/callbacks.
- [Using Plugins](https://revealjs.com/plugins/): register built-in or third-party plugins through the config `plugins` array.
- [Creating a Plugin](https://revealjs.com/creating-plugins/): plugin object shape, plugin registration, async plugins, and deck instance access.
- [Multiplex](https://revealjs.com/multiplex/): audience devices follow a master deck through the separate multiplex plugin.

## Feature Selection Heuristic

- Use **fragments** for explanation order.
- Use **vertical slides** for optional depth.
- Use **auto-animate** for changing state across related slides.
- Use **backgrounds** for context or media-heavy moments.
- Use **speaker notes** for delivery, caveats, and transitions.
- Use **uncounted appendix slides** for backup material.
- Use **scroll view** for reading; use slide view for live talks.
- Use **postMessage** only when embedding or remotely controlling a deck.
