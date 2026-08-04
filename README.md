# 💎 Wall Jewels — Luxury Wallpaper World

> **Next-Generation Static Web Experience** for Wall Jewels, Chennai's premier provider of custom wallpapers, 3D murals, divine pooja motifs, vertical gardens, and specialty flooring.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Architecture](#-project-architecture)
- [Quick Start \& Execution Commands](#-quick-start--execution-commands)
  - [Method 1: Python HTTP Server (Recommended)](#method-1-python-http-server-recommended)
  - [Method 2: Node.js / npx](#method-2-nodejs--npx)
  - [Method 3: VS Code Live Server Extension](#method-3-vs-code-live-server-extension)
  - [Method 4: PHP Built-in Server](#method-4-php-built-in-server)
  - [Method 5: Direct Browser Access](#method-5-direct-browser-access)
- [Configuration \& Customization (Phase 2)](#-configuration--customization-phase-2)
  - [Adding Custom Photography](#adding-custom-photography)
  - [Tuning Coverflow Deck Geometry](#tuning-coverflow-deck-geometry)
  - [Customizing Background Shaders](#customizing-background-shaders)
- [Deployment Guide](#-deployment-guide)
- [Showroom \& Contact Details](#-showroom--contact-details)
- [License \& Credits](#-license--credits)

---

## 🌟 Overview

The **Wall Jewels** web platform is designed to provide an opulent, immersive showcase for premium wall coverings and interior solutions. Engineered with zero external npm dependencies or heavy JavaScript frameworks, it delivers instant page loads, smooth 60fps animations, and a rich visual aesthetic across desktop and mobile devices.

### Highlights
- ⚡ **Zero-Build Architecture**: Pure HTML5, CSS3, and modern ES6 JavaScript. No compilation or bundler step required.
- 🎨 **WebGL Ambient Canvas**: Custom WebGL shader engine featuring 5 interactive visual modes.
- 🎠 **3D Coverflow Arc Carousel**: GPU-accelerated 3D carousel with hardware-accelerated transforms.
- 🌓 **Adaptive Theme Engine**: Built-in Light/Dark mode supporting system preferences and persistent user overrides.
- ♿ **WCAG AA Compliant**: Rigorously tested text contrast ratios (≥ 14.8:1 body contrast), keyboard navigation, and reduced-motion modes.

---

## ✨ Key Features

### 1. 3D Coverflow Showcase Deck
Located on the landing page (`index.html`), the coverflow carousel fans out featured wallpaper collections in an arc.
- **Hardware-Accelerated**: Every card operates from a unified absolute origin using CSS `transform` and `z-index`, avoiding browser layout reflows during slides.
- **Multi-Input Controls**: Supports directional navigation arrows, interactive pagination dots, direct card clicking, keyboard arrow keys, mouse dragging, and touch swipe gestures.
- **Smart Pause**: Autoplay cycles every 4.6 seconds and automatically pauses on user interaction or hover.

### 2. Interactive WebGL Background Shader Engine
A low-impact, downscaled ambient shader layer rendered behind the UI (`assets/js/background.js`):
- **5 Procedural Modes**:
  - `Plasma`: Slow, molten organic drift (Default).
  - `Silk`: Quiet, flowing horizontal fabric bands.
  - `Aurora`: Soft, serene drifting color clouds.
  - `Damask`: Living wallpaper repeat pattern on a half-drop grid.
  - `Marble`: Veined stone pattern mimicking real Calacatta marble.
  - `Off`: Minimalist pure CSS gradient wash fallback.
- **Performance Optimized**: Renders at `0.5×` resolution with bicubic upscaling to minimize GPU utilization. Automatically pauses when the browser tab is hidden or when `prefers-reduced-motion` is active.

### 3. Comprehensive Collection Explorer
The collection browser (`collection.html`) allows users to filter wall jewel offerings by:
- **Rooms**: Living Room, Bedroom, Pooja Room, Kids & Nursery, Office, School & Campus, Balcony & Outdoor, Flooring.
- **Themes**: 3D & Depth, Indian Deities, Nature & Landscape, Animal Kingdom, Beach & Coastal, Outer Space, Marble & Texture, Floral & Botanical, Superheroes & Cartoons, Custom Photographs.

---

## 🛠️ Technology Stack

| Layer | Technologies |
| :--- | :--- |
| **Markup** | HTML5 (Semantic Structure, Accessible ARIA standards) |
| **Styling** | Modern Vanilla CSS3 (Custom Properties / Design Tokens, Flexbox, Grid, Glassmorphism) |
| **Logic** | Vanilla JavaScript (ES6+ Modules, WebGL API, LocalStorage State) |
| **Build Tools** | *None required* (Runs natively in any web environment) |

---

## 📁 Project Architecture

```
Walljewels/
├── index.html            # Primary landing page & flagship collection showcase
├── collection.html       # Dynamic, filterable collection browser page
├── assets/
│   ├── css/
│   │   └── styles.css    # Unified design system, CSS variables & layouts
│   └── js/
│       ├── data.js       # Central data store (Collection, Rooms, Themes)
│       ├── app.js        # Core UI logic, carousel deck & filter handlers
│       └── background.js # WebGL ambient shader engine & theme syncer
├── .claude/
│   └── launch.json       # Project launcher metadata
└── README.md             # Project documentation
```

---

## 🚀 Quick Start & Execution Commands

Because Wall Jewels uses native HTTP standards (including ES modules and dynamic fetch calls), **it must be served over a local HTTP/HTTPS web server** rather than opened directly via `file://`.

Below are commands to execute and run the project locally across different environments:

### Method 1: Python HTTP Server (Recommended)

If Python is installed on your system, execute one of the following commands in your terminal:

```bash
# Python 3.x (Standard)
python -m http.server 5178

# Alternatively with python3 command
python3 -m http.server 5178
```
Then open your browser and navigate to: **`http://localhost:5178`**

---

### Method 2: Node.js / npx

If Node.js is installed on your machine, you can run a local server instantly without installing global dependencies:

```bash
# Option A: Using 'serve'
npx serve . -p 5178

# Option B: Using 'http-server'
npx http-server -p 5178
```
Then open your browser and navigate to: **`http://localhost:5178`**

---

### Method 3: VS Code Live Server Extension

If you are using Visual Studio Code or Cursor:
1. Open the project folder in VS Code.
2. Install the **Live Server** extension (`daybreak.live-server` or `ritwickdey.LiveServer`).
3. Right-click `index.html` in the file explorer and select **"Open with Live Server"**.
4. The site will open automatically in your browser at `http://127.0.0.1:5500`.

---

### Method 4: PHP Built-in Server

If PHP is available on your machine:

```bash
php -S localhost:5178
```
Then open your browser and navigate to: **`http://localhost:5178`**

---

### Method 5: Direct Browser Access

While an HTTP server is recommended for hash routing and WebGL shader support, you can preview static page structures directly:
- Double-click `index.html` or drag `index.html` into Google Chrome, Microsoft Edge, or Firefox.

---

## ⚙️ Configuration & Customization (Phase 2)

### Adding Custom Photography
All catalog items are defined inside `assets/js/data.js`. To add or replace wallpaper imagery:

1. Place high-resolution photos into `assets/img/collection/`.
2. Update the `img` path in `assets/js/data.js`:

```javascript
{
  t: 'Calacatta Gold',
  room: 'living',
  theme: 'texture',
  blurb: 'Book-matched marble veining, printed seamless across the full wall.',
  img: 'assets/img/collection/calacatta-gold.jpg', // ← Update your image path here
  tone: ['#EDE6DA', '#BFA46F'],
  tag: 'Bestseller'
}
```

*Note: If `img: null` is set, the application automatically renders a woven fallback swatch using the two colors specified in `tone`.*

---

### Tuning Coverflow Deck Geometry
To adjust the 3D coverflow card spacing, card dimensions, or rotation angles, modify the CSS variables in `assets/css/styles.css` (Section 22):

```css
.deck {
  --card-w: 320px;  /* Width of individual cards */
  --card-h: 460px;  /* Height of individual cards */
  --step: 110px;    /* Horizontal offset gap between cards */
  --tilt: 18deg;    /* 3D Y-axis rotation angle for side cards */
}
```

---

### Customizing Background Shaders
Shader opacity and intensity can be tuned in `assets/css/styles.css`:

```css
:root {
  --plasma-op: 0.88; /* Light theme shader opacity */
}
[data-theme="dark"] {
  --plasma-op: 0.82; /* Dark theme shader opacity */
}
```

To adjust specific shader gain levels or color palettes, edit the `MODES` object inside `assets/js/background.js`.

---

## 📦 Deployment Guide

### Automated Production Deployment (Hostinger & GitHub Actions)

This repository is equipped with an automated **GitHub Actions Workflow** ([`.github/workflows/deploy-production.yml`](file:///c:/Users/user/Desktop/UMP%202/Walljewels/Walljewels/.github/workflows/deploy-production.yml)).

- **Trigger**: Every push to the `main` branch.
- **Action**: Automatically syncs production-ready static files into the **`production`** branch.
- **Hostinger Integration**: Connect your Hostinger hPanel Git Deployment to track the **`production`** branch with Auto-Deployment enabled. Any push to `main` will automatically build and update your live Hostinger website.

### Alternative Static Hosting Options

- **Hostinger (Git Deployment)**: Point Hostinger Git deployment directly to the `production` branch.
- **Netlify**: Connect the Git repository (Publish directory: `./`).
- **Vercel**: Import the repository as a Static Site (Build command: *None*, Output directory: `./`).
- **Cloudflare Pages / GitHub Pages**: Set branch to `production` or `main`.


---

## 📍 Showroom & Contact Details

- **Email**: `info@walljewels.com`
- **Phone / Showroom Enquiries**: `+91 98400 64205 / 06 / 07`
- **WhatsApp & Custom Orders**: `+91 9677042903`
- **Headquarters**: Parry's Flagship Showroom (5,000 sq. ft.), Chennai, Tamil Nadu, India.

---

## 📄 License & Credits

- © **Wall Jewels Wallpaper World**. All rights reserved.
- Designed & Developed for Wall Jewels.
