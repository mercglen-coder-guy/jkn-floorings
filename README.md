# JKN Flooring - Architectural Surface Platform

JKN Flooring is a maturely minimal, highly polished architectural flooring platform built for custom residential contractors, builders, and homeowners across Toronto and the Greater Toronto Area (GTA). 

The platform is engineered using a high-performance **Litestar** (Python) backend and integrated with **Google's Gemini Vision AI** to deliver instant style identification and subfloor layout estimates directly from inspiration photos.

---

## Key Features

1. **Architectural Editorial Grid**: An asymmetrical hero landing zone featuring refined visual hierarchy, classy brand tag frames, and elegant call-to-action systems.
2. **Gemini Vision AI Estimator (`/api/vision`)**: A standalone visual assessment tool. Users upload a room style photo, and the backend instantly identifies the material (hardwood, vinyl, or stone tile), maps technical subfloor specifications, and outputs GTA-specific labor and material cost estimates.
3. **AI Concierge Chatbot (`/api/chat`)**: A slide-out, glassmorphic assistant panel (opens via navigation search, sparkles button, or the `⌘K` keyboard shortcut). Driven by semantic routing, the concierge resolves technical material specifications, warranty questions, and GTA installation rates.
4. **Before/After Split Slider**: An interactive horizontal drag-to-compare widget. Reveals subfloor grid preparation versus the finished natural oak wide-plank hardwood.
5. **Classy Estimation Pipeline (`/api/quote`)**: An AJAX-driven quote form with fine-border focus animations, communicating seamlessly with Litestar dataclass models for robust validation.

---

## Directory Structure

```text
JKN-Floorings/
│
├── Home.py               # Main Litestar backend application (handlers, API routes, configurations)
├── requirements.txt      # Project dependencies (Litestar, Jinja2, Uvicorn, etc.)
├── .gitignore            # Clean git exclusion rules (ignores virtual environment and cache)
│
├── Templates/            # Jinja2 Layout Templates
│   ├── base.html         # Base structural shell, Tailwind CSS configs, Lucide, and AI Concierge UI
│   └── home.html         # Hero sections, Vision AI, Before/After Slider, and Contact Form
│
├── static/               # Serviced static assets
│   ├── css/
│   │   └── styles.css    # Legacy layout rules (archived)
│   └── images/
│       ├── hero_flooring.png    # High-resolution Natural Oak Showcase
│       └── craftsmanship.png    # High-resolution Subfloor Grid Prep
│
└── Dependencies/         # Python 3.14 Virtual Environment (git-ignored)
```

---

## Technical Stack

- **Backend Framework**: [Litestar](https://litestar.dev/) - A powerful, lightweight, asynchronous ASGI python framework.
- **Server**: [Uvicorn](https://www.uvicorn.org/) - ASGI web server implementation.
- **Templating**: [Jinja2](https://jinja.palletsprojects.com/) - Modern designer-friendly templating engine.
- **Styling**: [Tailwind CSS v3](https://tailwindcss.com/) - Class-based atomic CSS utility.
- **Typography**: Paired Outfit (Editorial Headings) & Plus Jakarta Sans (Body Text) via Google Fonts.
- **Icons**: Lucide Icons.

---

## Local Setup & Run Guide

### 1. Prerequisites
Ensure you have Python 3.14+ installed on your host system.

### 2. Install Dependencies
Run the following from the repository root:
```bash
./Dependencies/bin/pip install -r requirements.txt
```

### 3. Launch Development Server
Launch the application locally with WatchFiles live-reload active:
```bash
./Dependencies/bin/python -m uvicorn Home:app --host 0.0.0.0 --port 8000 --reload
```

- **Local Machine Access**: `http://127.0.0.1:8000`
- **Local WiFi Network Access**: `http://<your-wifi-ip-address>:8000`

---

## GitHub Deployment Preparation

This repository is **completely ready for GitHub pushing**:
* All environment directories (`Dependencies/`), temporary caches (`__pycache__/`), and system files are fully excluded in the root `.gitignore`.
* Critical credentials or keys should be loaded via `.env` (a standard security pattern if you integrate live Gemini production APIs).
* Accessibility landmarks, descriptive alt tags, and unique DOM test elements (`id="..."`) are incorporated throughout the HTML source code.
