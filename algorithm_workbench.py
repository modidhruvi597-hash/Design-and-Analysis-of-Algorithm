#!/usr/bin/env python3
"""
ALGORITHM INTELLIGENCE WORKBENCH
An Interactive Algorithm Research & Analysis Environment
=========================================================

An enterprise-grade computational research environment for algorithmic analysis,
real-time step execution, invariant verification, and empirical benchmarking of
Insertion Sort.

Platform: Pure Python 3.8+ with standard tkinter (zero third-party dependencies).
Architecture: Scientific workstation UI, high-DPI responsive, signature graphite/midnight theme.
"""

import csv
import json
import math
import os
import random
import sys
import time
import traceback
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Tuple

try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
    import tkinter.font as tkfont
except ImportError:
    sys.exit(
        "tkinter is required to run the Algorithm Intelligence Workbench.\n"
        "  Ubuntu/Debian: sudo apt install python3-tk\n"
        "  Fedora:        sudo dnf install python3-tkinter\n"
        "  Windows/macOS: Reinstall Python from python.org with tcl/tk enabled."
    )

# =============================================================================
# 1. ARCHITECTURAL CONSTANTS & SIGNATURE DESIGN TOKENS
# =============================================================================

APP_TITLE = "Algorithm Intelligence"
APP_SUBTITLE = "Interactive Computational Complexity, Step Execution & Empirical Analysis Laboratory"
SETTINGS_FILE = Path.home() / ".algorithm_intelligence_workbench.json"

MIN_SIZE, MAX_SIZE, DEFAULT_SIZE = 10, 50, 24
MIN_VALUE, MAX_VALUE = 5, 100
DEFAULT_SPEED = 32
LIFT_HEIGHT = 28

# Execution States
IDLE = "idle"
SORTING = "sorting"
PAUSED = "paused"
COMPLETED = "completed"
BENCHMARKING = "benchmarking"

# Semantic Color Palette (Elite Dark Analytics & High Contrast)
COLORS = {
    "normal":   "#36BCEB",   # Secondary Cyan        - Unsorted Partition
    "sorted":   "#10B981",   # Restrained Emerald    - Sorted Subarray Invariant
    "compare":  "#F59E0B",   # Warm Amber            - Active Key Comparison
    "shift":    "#F43F5E",   # Coral / Muted Red     - Rightward Element Shift
    "key":      "#8B5CF6",   # Electric Violet       - Extracted Key Element
    "target":   "#F97316",   # Technical Orange      - Insertion Slot Marker
    "accent":   "#20E6D0",   # Primary Turquoise     - Action Hero Highlight
    "teal":     "#12BFAF",   # Secondary Teal
    "cyan":     "#36BCEB",   # Secondary Cyan
    "success":  "#10B981",   # Emerald Success
    "error":    "#EF4444",   # Error
    "neutral":  "#64748B",   # Cool Slate
}
ACTIVE_STATES = ("key", "compare", "shift", "target")

STATE_COLORS = {
    IDLE: COLORS["normal"],
    SORTING: COLORS["accent"],
    PAUSED: COLORS["compare"],
    COMPLETED: COLORS["sorted"],
    BENCHMARKING: COLORS["cyan"],
}
STATE_TEXT = {
    IDLE: "READY",
    SORTING: "SORTING",
    PAUSED: "PAUSED",
    COMPLETED: "COMPLETED",
    BENCHMARKING: "BENCHMARKING",
}

# Signature Design System (Elite Dark Scientific Analytics Suite)
THEMES = {
    "dark": {
        "bg": "#172638",           # Outer application background
        "workspace": "#05090D",    # Main workspace background
        "card": "#080E14",         # Primary content surface
        "card2": "#0B1117",        # Secondary card surface
        "card3": "#101922",        # Elevated interactive surface
        "hover": "#14212B",        # Hover surface
        "border": "#1D2A35",       # Main border
        "line": "#17232D",         # Subtle divider
        "border_active": "#1A5A5F",# Restrained darker turquoise border
        "ink": "#F2F6F8",          # Primary text
        "soft": "#A4B1BD",         # Secondary text
        "muted": "#8795A3",        # Muted metadata
        "disabled": "#4C5A67",     # Subdued neutral
        "chart": "#05090D",        # Plotting surface (near-black)
        "grid_line": "#0E1822",    # Low-contrast grid line
        "grid_guide": "#17232D",   # Reference guide lines
        "track": "#101922",        # Slider / Progress track
        "code_bg": "#05090D",      # Monospace terminal background
        "code_hl": "#0A252E",      # Active code line highlight (dark teal tint)
        "code_num": "#4C5A67",     # Line number
        "accent": "#20E6D0",       # Primary turquoise
        "accent_secondary": "#12BFAF", # Secondary teal
        "accent_cyan": "#36BCEB",  # Secondary cyan
        "accent_bg": "#083238",    # Active selection background (restrained dark teal)
        "sorted": "#10B981",       # Restrained emerald
        "normal": "#36BCEB",       # Unsorted partition (cyan family)
        "key": "#8B5CF6",          # Electric violet
        "compare": "#F59E0B",      # Warm amber
        "shift": "#F43F5E",        # Coral / muted red
        "target": "#F97316",       # Technical orange
        "cyan": "#36BCEB",         # Secondary cyan
        "success": "#10B981",      # Emerald success
        "glow": 0.20,
    },
    "light": {
        "bg": "#E8ECEF",           # Soft Technical Off-White Shell
        "workspace": "#F4F7F9",    # Light Workspace
        "card": "#FFFFFF",         # Pure White Work Surface
        "card2": "#EDF2F6",        # Soft Slate Differentiated Surface
        "card3": "#E2E8F0",        # Elevated Surface
        "hover": "#DBE4EC",        # Hover Surface
        "border": "#CBD5E1",       # Crisp Separator Border
        "line": "#E2E8F0",         # Subtle Separators
        "border_active": "#12BFAF",# Active Border
        "ink": "#0F172A",          # Deep Charcoal Primary Text
        "soft": "#475569",         # Muted Slate Secondary Text
        "muted": "#64748B",        # Dim Axis / Tick Text
        "disabled": "#94A3B8",     # Disabled Text
        "chart": "#FFFFFF",        # Plotting Surface
        "grid_line": "#F1F5F9",    # Blueprint Grid
        "grid_guide": "#E2E8F0",   # Reference Guide Lines
        "track": "#E2E8F0",        # Slider / Progress Track
        "code_bg": "#F8FAFC",      # Monospace Terminal Background
        "code_hl": "#E0F7F6",      # Active Code Line Highlight
        "code_num": "#94A3B8",     # Line Number
        "accent": "#0D9488",       # Primary Teal
        "accent_secondary": "#0F766E",
        "accent_cyan": "#0284C7",
        "accent_bg": "#CCFBF1",    # Active Selection Tint
        "sorted": "#059669",
        "normal": "#0284C7",
        "key": "#7C3AED",
        "compare": "#D97706",
        "shift": "#E11D48",
        "target": "#EA580C",
        "cyan": "#0284C7",
        "success": "#059669",
        "glow": 0.08,
    },
}

UI_SCALE = 1.0


def px(value: float) -> int:
    return int(round(value * UI_SCALE))


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def hex_to_rgb(color: str) -> Tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: Tuple[float, float, float]) -> str:
    return "#%02x%02x%02x" % tuple(clamp(int(round(v)), 0, 255) for v in rgb)


def mix(color_a: str, color_b: str, t: float) -> str:
    t = clamp(t, 0.0, 1.0)
    a, b = hex_to_rgb(color_a), hex_to_rgb(color_b)
    return rgb_to_hex(tuple(a[i] + (b[i] - a[i]) * t for i in range(3)))


COLOR_RGB = {name: hex_to_rgb(code) for name, code in COLORS.items()}


def round_points(x1: float, y1: float, x2: float, y2: float, r: float) -> List[float]:
    r = max(1.0, min(r, (x2 - x1) / 2.0, (y2 - y1) / 2.0))
    return [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1
    ]


def round_rect(canvas: tk.Canvas, x1: float, y1: float, x2: float, y2: float, r: float, **kwargs) -> int:
    return canvas.create_polygon(round_points(x1, y1, x2, y2, r), smooth=True, **kwargs)


def pick_font(root: tk.Tk, candidates: Tuple[str, ...], fallback: str = "TkDefaultFont") -> str:
    installed = set(tkfont.families(root))
    for name in candidates:
        if name in installed:
            return name
    return fallback


def load_settings() -> Dict[str, Any]:
    try:
        return json.loads(SETTINGS_FILE.read_text())
    except (OSError, ValueError):
        return {}


def save_settings(data: Dict[str, Any]) -> None:
    try:
        current = load_settings()
        current.update(data)
        SETTINGS_FILE.write_text(json.dumps(current, indent=2))
    except OSError:
        pass


# =============================================================================
# 2. CORE ALGORITHM & HEADLESS BENCHMARK ENGINE
# =============================================================================

@dataclass
class BenchmarkResult:
    distribution: str
    size: int
    elapsed_us: float
    comparisons: int
    shifts: int
    accesses: int
    theoretical_comparisons: float
    growth_ratio: Optional[float] = None


def generate_distribution(dist_type: str, size: int, seed: Optional[int] = None) -> List[int]:
    rng = random.Random(seed) if seed is not None else random.Random()
    dist = dist_type.lower().replace(" ", "_")

    if "sorted" in dist and "nearly" not in dist:
        step = max(1, (MAX_VALUE - MIN_VALUE) // max(1, size))
        return [MIN_VALUE + i * step for i in range(size)]
    elif "reverse" in dist:
        step = max(1, (MAX_VALUE - MIN_VALUE) // max(1, size))
        return [MAX_VALUE - i * step for i in range(size)]
    elif "nearly" in dist:
        arr = [MIN_VALUE + int(i * (MAX_VALUE - MIN_VALUE) / max(1, size)) for i in range(size)]
        swaps = max(1, int(size * 0.08))
        for _ in range(swaps):
            idx = rng.randint(0, size - 2)
            arr[idx], arr[idx + 1] = arr[idx + 1], arr[idx]
        return arr
    elif "duplicate" in dist or "few_unique" in dist:
        palette = [rng.randint(MIN_VALUE + 6, MAX_VALUE - 6) for _ in range(3)]
        return [rng.choice(palette) for _ in range(size)]
    else:
        return [rng.randint(MIN_VALUE, MAX_VALUE) for _ in range(size)]


def count_inversions(arr: List[int]) -> int:
    inversions = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions


def insertion_sort_headless(arr: List[int]) -> Tuple[List[int], Dict[str, Any]]:
    a = list(arr)
    n = len(a)
    comparisons = 0
    shifts = 0
    accesses = 0

    t_start = time.perf_counter_ns()
    for i in range(1, n):
        key = a[i]
        accesses += 1
        j = i - 1
        while j >= 0:
            comparisons += 1
            accesses += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                accesses += 2
                j -= 1
            else:
                break
        a[j + 1] = key
        accesses += 1
    t_end = time.perf_counter_ns()

    elapsed_us = (t_end - t_start) / 1000.0
    return a, {
        "size": n,
        "comparisons": comparisons,
        "shifts": shifts,
        "accesses": accesses,
        "elapsed_us": elapsed_us,
        "elapsed_ms": elapsed_us / 1000.0,
        "is_sorted": a == sorted(arr),
    }


# =============================================================================
# 3. SCIENTIFIC WORKSTATION WIDGETS
# =============================================================================

class ScrollFrame(tk.Frame):
    """Universal vertical scrolling viewport with smooth mouse-wheel handling."""

    def __init__(self, parent: tk.Widget):
        super().__init__(parent, bd=0, highlightthickness=0)
        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, yscrollincrement=px(20))
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.inner = tk.Frame(self.canvas, bd=0, highlightthickness=0)
        self._window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")
        self.inner.bind("<Configure>", self._on_inner_resize)
        self.canvas.bind("<Configure>", self._on_canvas_resize)

        for seq in ("<MouseWheel>", "<Button-4>", "<Button-5>"):
            self.bind_all(seq, self._on_wheel)

    def _on_inner_resize(self, _event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_resize(self, event):
        self.canvas.itemconfigure(self._window, width=event.width)

    def _on_wheel(self, event):
        if self.inner.winfo_reqheight() <= self.canvas.winfo_height():
            return
        if event.num == 4:
            step = -3
        elif event.num == 5:
            step = 3
        elif sys.platform == "darwin":
            step = -event.delta
        else:
            step = -3 if event.delta > 0 else 3
        self.canvas.yview_scroll(step, "units")


class GlowButton(tk.Canvas):
    """
    Precision technical button with automatic font metrics measurement,
    active state indicators, and zero text-clipping guarantees.
    """

    def __init__(
        self,
        parent: tk.Widget,
        text: str,
        command: Any,
        color: str,
        font: Any,
        height: int = 30,
        ghost: bool = False,
        min_width: int = 70,
        is_hero: bool = False,
        is_tab: bool = False,
        is_preset: bool = False,
    ):
        self.text = text
        self.command = command
        self.color = color
        self.font = font
        self.ghost = ghost
        self.is_hero = is_hero
        self.is_tab = is_tab
        self.is_preset = is_preset
        self.is_active_tab = False
        self.is_active_preset = False
        self.enabled = True
        self.hover = False
        self.pressed = False
        self.theme: Optional[Dict[str, Any]] = None

        req_w = self._calculate_required_width(min_width)
        super().__init__(
            parent,
            width=req_w,
            height=px(height),
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )

        self.bind("<Configure>", lambda e: self.redraw())
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _calculate_required_width(self, min_w: int) -> int:
        padding = px(22)
        try:
            measured = self.font.measure(self.text)
        except Exception:
            measured = len(self.text) * px(8)
        return max(px(min_w), measured + padding)

    def set_enabled(self, flag: bool) -> None:
        self.enabled = flag
        self.configure(cursor="hand2" if flag else "arrow")
        self.redraw()

    def set_text(self, text: str) -> None:
        self.text = text
        req_w = self._calculate_required_width(0)
        if req_w > self.winfo_width():
            self.configure(width=req_w)
        self.redraw()

    def set_active_tab(self, flag: bool) -> None:
        self.is_active_tab = flag
        self.redraw()

    def set_active_preset(self, flag: bool) -> None:
        self.is_active_preset = flag
        self.redraw()

    def apply_theme(self, theme: Dict[str, Any]) -> None:
        self.theme = theme
        self.configure(bg=theme["card"] if (self.is_tab or not self.ghost) else theme["bg"])
        self.redraw()

    def _on_enter(self, _event):
        self.hover = True
        self.redraw()

    def _on_leave(self, _event):
        self.hover = self.pressed = False
        self.redraw()

    def _on_press(self, _event):
        if self.enabled:
            self.pressed = True
            self.redraw()

    def _on_release(self, _event):
        was_pressed = self.pressed
        self.pressed = False
        self.redraw()
        if was_pressed and self.hover and self.enabled:
            self.command()

    def redraw(self) -> None:
        self.delete("all")
        th = self.theme
        if th is None:
            return
        w, h = self.winfo_width(), self.winfo_height()
        radius = px(4)
        inset = px(2)

        if self.is_tab:
            # Segmented Rail Navigation Tab with active indicator
            if self.is_active_tab:
                fill = th["accent_bg"]
                border_col = th["border_active"]
                text_color = th["accent"]
                round_rect(self, inset, inset, w - inset, h - inset, radius, fill=fill, outline=border_col)
                # Bottom 2px turquoise indicator line
                self.create_line(inset + px(8), h - inset - 1, w - inset - px(8), h - inset - 1, fill=th["accent"], width=px(2))
            else:
                fill = th["hover"] if self.hover else th["card"]
                border_col = th["border"]
                text_color = th["ink"] if self.hover else th["soft"]
                round_rect(self, inset, inset, w - inset, h - inset, radius, fill=fill, outline=border_col)
        elif self.is_preset:
            # Input Dataset Preset Tab
            if self.is_active_preset:
                fill = th["accent_bg"]
                border_col = th["border_active"]
                text_color = th["accent"]
                round_rect(self, inset, inset, w - inset, h - inset, radius, fill=fill, outline=border_col)
            else:
                fill = th["hover"] if self.hover else th["card3"]
                border_col = th["border"]
                text_color = th["ink"] if self.hover else th["soft"]
                round_rect(self, inset, inset, w - inset, h - inset, radius, fill=fill, outline=border_col)
        elif self.is_hero:
            # Primary Action Button (Solid Turquoise Hero with near-black bold text)
            if not self.enabled:
                fill = th["card3"]
                text_color = th["disabled"]
                round_rect(self, inset, inset, w - inset, h - inset, radius, fill=fill, outline=th["border"])
            elif self.pressed:
                fill = th["accent_secondary"]
                text_color = "#05090D"
                round_rect(self, inset, inset, w - inset, h - inset, radius, fill=fill)
            elif self.hover:
                fill = th["accent_cyan"]
                text_color = "#05090D"
                round_rect(self, inset, inset, w - inset, h - inset, radius, fill=fill)
            else:
                fill = th["accent"]
                text_color = "#05090D"
                round_rect(self, inset, inset, w - inset, h - inset, radius, fill=fill)
        elif self.ghost:
            # Quiet Secondary Button with fine technical outline
            fill = th["hover"] if self.hover else th["card3"]
            if not self.enabled:
                fill = th["card"]
                text_color = th["disabled"]
                round_rect(self, inset, inset, w - inset, h - inset, radius, fill=fill, outline=th["border"])
            else:
                border_col = self.color if self.hover else th["border"]
                text_color = self.color if self.hover else th["ink"]
                round_rect(self, inset, inset, w - inset, h - inset, radius, fill=fill, outline=border_col)
        elif not self.enabled:
            round_rect(
                self, inset, inset, w - inset, h - inset, radius,
                fill=th["card"], outline=th["border"]
            )
            text_color = th["disabled"]
        else:
            # Semantic Control Button (Step, Reset, Pause, Resume, Generate)
            fill = th["hover"] if self.hover else th["card3"]
            border_col = self.color if self.hover else th["border"]
            if self.pressed:
                fill = mix(th["card3"], "#000000", 0.20)
            round_rect(
                self, inset, inset, w - inset, h - inset, radius,
                fill=fill, outline=border_col
            )
            text_color = self.color

        self.create_text(w / 2, h / 2, text=self.text, font=self.font, fill=text_color)


class Slider(tk.Canvas):
    """Precision technical slider with numeric tracking thumb."""

    def __init__(self, parent: tk.Widget, minimum: int, maximum: int, value: int, command: Any = None):
        super().__init__(parent, height=px(22), highlightthickness=0, bd=0, cursor="hand2")
        self.minimum = minimum
        self.maximum = maximum
        self.value = value
        self.command = command
        self.enabled = True
        self.theme: Optional[Dict[str, Any]] = None

        self.bind("<Configure>", lambda e: self.redraw())
        self.bind("<Button-1>", self._drag)
        self.bind("<B1-Motion>", self._drag)

    def get(self) -> int:
        return self.value

    def set(self, value: int) -> None:
        self.value = int(clamp(value, self.minimum, self.maximum))
        self.redraw()

    def set_enabled(self, flag: bool) -> None:
        self.enabled = flag
        self.configure(cursor="hand2" if flag else "arrow")
        self.redraw()

    def apply_theme(self, theme: Dict[str, Any]) -> None:
        self.theme = theme
        self.configure(bg=theme["card3"])
        self.redraw()

    def _fraction(self) -> float:
        return (self.value - self.minimum) / max(1, self.maximum - self.minimum)

    def _drag(self, event: tk.Event) -> None:
        if not self.enabled:
            return
        margin = px(8)
        span = max(1, self.winfo_width() - 2 * margin)
        fraction = clamp((event.x - margin) / span, 0.0, 1.0)
        new_val = int(round(self.minimum + fraction * (self.maximum - self.minimum)))
        if new_val != self.value:
            self.value = new_val
            self.redraw()
            if self.command:
                self.command(new_val)

    def redraw(self) -> None:
        self.delete("all")
        th = self.theme
        if th is None:
            return
        w, h = self.winfo_width(), self.winfo_height()
        margin = px(8)
        cy = h / 2
        x = margin + (w - 2 * margin) * self._fraction()

        fill = th["accent"] if self.enabled else th["disabled"]
        self.create_line(margin, cy, w - margin, cy, width=px(3), capstyle="round", fill=th["track"])
        self.create_line(margin, cy, x, cy, width=px(3), capstyle="round", fill=fill)

        r = px(5)
        if self.enabled:
            self.create_oval(
                x - r - px(2), cy - r - px(2), x + r + px(2), cy + r + px(2),
                fill=th["accent_bg"], outline=""
            )
        self.create_oval(x - r, cy - r, x + r, cy + r, fill="#FFFFFF", outline=fill, width=px(2))


class ProgressBar(tk.Canvas):
    """Vector convergence progress bar."""

    def __init__(self, parent: tk.Widget):
        super().__init__(parent, height=px(10), highlightthickness=0, bd=0)
        self.target = 0.0
        self.shown = 0.0
        self.phase = 0.0
        self.theme: Optional[Dict[str, Any]] = None
        self.bind("<Configure>", lambda e: self.redraw())

    def set_target(self, fraction: float, snap: bool = False) -> None:
        self.target = clamp(fraction, 0.0, 1.0)
        if snap:
            self.shown = self.target
            self.redraw()

    def apply_theme(self, theme: Dict[str, Any]) -> None:
        self.theme = theme
        self.configure(bg=theme["card3"])
        self.redraw()

    def tick(self, dt: float, active: bool) -> None:
        changed = False
        if abs(self.target - self.shown) > 0.0005:
            self.shown += (self.target - self.shown) * (1.0 - math.exp(-dt / 0.12))
            changed = True
        elif self.shown != self.target:
            self.shown = self.target
            changed = True
        if active:
            self.phase = (self.phase + dt * 0.45) % 1.0
            changed = True
        if changed:
            self.redraw()

    def redraw(self) -> None:
        self.delete("all")
        th = self.theme
        if th is None:
            return
        w, h = self.winfo_width(), self.winfo_height()
        top, bottom = px(1), h - px(1)
        round_rect(self, 0, top, w, bottom, px(3), fill=th["track"])

        fill_w = w * self.shown
        if fill_w < 2:
            return
        round_rect(self, 0, top, fill_w, bottom, px(3), fill=th["accent"])


# =============================================================================
# 4. DATA MODEL & BAR ENTITY
# =============================================================================

class Bar:
    """Represents a single visualized element with continuous physical coordinates."""

    def __init__(self, value: int, index: int):
        self.value = value
        self.index = index
        self.state = "normal"
        self.x = self.tx = 0.0
        self.lift = self.tlift = 0.0
        self.h = 10.0
        self.rgb = COLOR_RGB["normal"]
        self.flash = 0.0
        self.glow: Any = None
        self.rect: Any = None
        self.text: Any = None
        self.drawn: Any = None


# =============================================================================
# 5. ALGORITHM INTELLIGENCE WORKBENCH (UNIFIED SUITE)
# =============================================================================

class VisualizerApp:
    """The enterprise desktop workbench environment for algorithm intelligence."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.closing = False

        # Load Settings (Default: Signature Dark Theme)
        settings = load_settings()
        self.theme_name = settings.get("theme", "dark")
        if self.theme_name not in THEMES:
            self.theme_name = "dark"
        self.th = THEMES[self.theme_name]

        # Application State
        self.state = IDLE
        self.current_tab = "visualizer"
        self.values: List[int] = []
        self.original: List[int] = []
        self.bar_objs: List[Bar] = []
        self.bars: List[Bar] = []
        self.stats: Dict[str, Any] = {}
        self.gen: Optional[Generator[float, None, None]] = None
        self.job: Any = None
        self.wave_job: Any = None
        self.run_token = 0
        self.key_bar: Optional[Bar] = None
        self.gap_index: Optional[int] = None
        self.confetti: List[Dict[str, Any]] = []
        self.history_texts: List[str] = []
        self.execution_trace: List[Dict[str, Any]] = []
        self.active_code_line = 1
        self.current_seed: Optional[int] = None
        self.current_preset = "Random"
        self.paused_message = ""
        self.paused_phase = "Starting"

        # Benchmarking State
        self.benchmark_records: List[BenchmarkResult] = []
        self.is_benchmarking = False

        # Timer
        self.timer_started: Optional[float] = None
        self.timer_elapsed = 0.0
        self.last_clock = 0.0

        # Animation Loop
        self.tau = 0.065
        self.last_tick = time.perf_counter()
        self.div_x = 0.0
        self.div_count = 0
        self.ghost_x = 0.0
        self._ghost_visible = False
        self._tag_visible = False
        self._overlay_sig: Any = None

        # Canvas Geometry
        self.W = self.H = 0
        self.pad = self.slot = self.bw = self.base = self.max_h = 0.0
        self.compact = False

        # Registries
        self.w: Dict[str, tk.Widget] = {}
        self.idx_items: List[int] = []
        self._themed: List[Tuple[tk.Widget, Dict[str, str]]] = []
        self._custom: List[Any] = []
        self._hooks: List[Any] = []

        self.build_fonts()
        self.build_ui()
        if hasattr(self, "preset_buttons") and "Random" in self.preset_buttons:
            self.preset_buttons["Random"].set_active_preset(True)
        self.apply_theme()
        self.update_speed()
        self.generate_array()
        self.set_state(IDLE)
        self.bind_keys()
        self.tick()

    # -------------------------------------------------------------------------
    # Typography & Design Token Helpers
    # -------------------------------------------------------------------------
    def build_fonts(self) -> None:
        ui = pick_font(
            self.root,
            ("Segoe UI Variable Text", "Segoe UI", "SF Pro Text", "Helvetica Neue", "Ubuntu", "Arial")
        )
        mono = pick_font(
            self.root,
            ("Cascadia Code", "Cascadia Mono", "Consolas", "SF Mono", "Menlo", "Courier New")
        )

        def make(family: str, size: int, bold: bool = False) -> tkfont.Font:
            return tkfont.Font(root=self.root, family=family, size=-px(size), weight="bold" if bold else "normal")

        self.f = {
            "title": make(ui, 16, True),
            "chip": make(mono, 10, True),
            "h2": make(ui, 13, True),
            "h2big": make(ui, 17, True),
            "body": make(ui, 12),
            "bold": make(ui, 12, True),
            "small": make(ui, 10),
            "tag": make(mono, 9, True),
            "step": make(ui, 13, True),
            "btn": make(ui, 11, True),
            "mono": make(mono, 11),
            "mono_s": make(mono, 10),
            "mono_b": make(mono, 12, True),
            "mono_big": make(mono, 15, True),
            "bar": make(mono, 10, True),
            "idx": make(mono, 9),
            "code": make(mono, 11),
            "code_bold": make(mono, 11, True),
        }

    def reg(self, widget: tk.Widget, **options: str) -> tk.Widget:
        self._themed.append((widget, options))
        return widget

    def frame(self, parent: tk.Widget, bg: str = "card") -> tk.Frame:
        return self.reg(tk.Frame(parent, bd=0, highlightthickness=0), bg=bg)

    def card(self, parent: tk.Widget) -> tk.Frame:
        fr = tk.Frame(parent, bd=0, highlightthickness=1)
        return self.reg(fr, bg="card", highlightbackground="border", highlightcolor="border")

    def tile(self, parent: tk.Widget) -> tk.Frame:
        fr = tk.Frame(parent, bd=0, highlightthickness=1)
        return self.reg(fr, bg="card2", highlightbackground="line", highlightcolor="line")

    def label(self, parent: tk.Widget, text: str = "", font: str = "body", fg: str = "ink", bg: str = "card", **kwargs) -> tk.Label:
        lb = tk.Label(parent, text=text, font=self.f[font], bd=0, **kwargs)
        return self.reg(lb, fg=fg, bg=bg)

    @staticmethod
    def autowrap(label: tk.Label, margin: int) -> None:
        label.bind("<Configure>", lambda e: label.configure(wraplength=max(60, e.width - margin)))

    def apply_theme(self) -> None:
        th = self.th = THEMES[self.theme_name]
        self.root.configure(bg=th["bg"])
        for widget, options in self._themed:
            try:
                resolved = {opt: th.get(key, COLORS.get(key, key)) for opt, key in options.items()}
                widget.configure(**resolved)
            except tk.TclError:
                pass
        for widget in self._custom:
            widget.apply_theme(th)
        self.refresh_chart_theme()
        self.highlight_pseudocode_line(self.active_code_line)
        for hook in self._hooks:
            hook(th)

    # -------------------------------------------------------------------------
    # Layout & Scientific Shell Construction (1366x768 Standard)
    # -------------------------------------------------------------------------
    def build_ui(self) -> None:
        self.root.title(f"{APP_TITLE} // Scientific Research Workbench")

        master_frame = self.frame(self.root, bg="bg")
        master_frame.pack(fill="both", expand=True)

        # Compact Engineering Shell Header (46px)
        self.build_header(master_frame)

        # Scrollable Instrument Workspace
        self.scroll = ScrollFrame(master_frame)
        self.scroll.pack(fill="both", expand=True)
        self.reg(self.scroll, bg="workspace")
        self.reg(self.scroll.canvas, bg="workspace")
        self.reg(self.scroll.inner, bg="workspace")

        self.view_container = self.frame(self.scroll.inner, bg="workspace")
        self.view_container.pack(fill="both", expand=True, padx=px(18), pady=(px(8), px(20)))

        # 3 Dedicated Scientific Labs
        self.view_visualizer = self.frame(self.view_container, bg="workspace")
        self.build_visualizer_tab(self.view_visualizer)

        self.view_benchmark = self.frame(self.view_container, bg="workspace")
        self.build_benchmark_tab(self.view_benchmark)

        self.view_analysis = self.frame(self.view_container, bg="workspace")
        self.build_analysis_tab(self.view_analysis)

        self.switch_tab("visualizer")

    def build_header(self, parent: tk.Widget) -> None:
        header = self.frame(parent, bg="bg")
        header.pack(fill="x", padx=px(18), pady=(px(8), px(4)))

        # Left: Product Wordmark
        left = self.frame(header, bg="bg")
        left.pack(side="left")

        logo_row = self.frame(left, bg="bg")
        logo_row.pack(anchor="w")
        self.label(logo_row, "◈ ", "title", fg="accent", bg="bg").pack(side="left")
        self.label(logo_row, "ALGORITHM INTELLIGENCE", "title", fg="ink", bg="bg").pack(side="left")
        
        chip = tk.Label(
            logo_row, text=" RESEARCH SUITE ", font=self.f["chip"],
            bd=0, padx=px(6), pady=px(1)
        )
        self.reg(chip, bg="card3", fg="accent_secondary")
        chip.pack(side="left", padx=(px(8), 0))

        # Center: Segmented Navigation Rail (No clipped tabs)
        center = self.frame(header, bg="bg")
        center.pack(side="left", expand=True)

        self.tab_buttons: Dict[str, GlowButton] = {}
        tabs = [
            ("visualizer", "∿ Visualizer"),
            ("benchmark", "☷ Benchmark Lab"),
            ("analysis", "⊨ Proof & Complexity"),
        ]

        seg_box = self.frame(center, bg="card")
        seg_box.pack(anchor="center")

        for tab_id, tab_label in tabs:
            btn = GlowButton(
                seg_box,
                tab_label,
                lambda tid=tab_id: self.switch_tab(tid),
                COLORS["accent"],
                self.f["btn"],
                height=28,
                is_tab=True,
                min_width=120,
            )
            btn.pack(side="left", padx=px(2), pady=px(2))
            self._custom.append(btn)
            self.tab_buttons[tab_id] = btn

        # Right: Status Indicator, Theme, Export
        right = self.frame(header, bg="bg")
        right.pack(side="right")

        self.badge = tk.Label(
            right, text="● READY", font=self.f["chip"], bd=0,
            highlightthickness=1, padx=px(10), pady=px(3)
        )
        self.reg(self.badge, bg="card", fg="normal", highlightbackground="border")
        self.badge.pack(side="left", padx=(0, px(6)))

        export_btn = GlowButton(
            right, "↓ Export Audit", self.export_audit_report, COLORS["cyan"],
            self.f["small"], height=28, ghost=True, min_width=85
        )
        export_btn.pack(side="left", padx=(0, px(6)))
        self._custom.append(export_btn)

        self.theme_btn = GlowButton(
            right, "◐ Theme", self.toggle_theme, COLORS["accent"],
            self.f["small"], height=28, ghost=True, min_width=75
        )
        self.theme_btn.pack(side="left")
        self._custom.append(self.theme_btn)

    def switch_tab(self, tab_id: str) -> None:
        self.current_tab = tab_id
        self.view_visualizer.pack_forget()
        self.view_benchmark.pack_forget()
        self.view_analysis.pack_forget()

        if tab_id == "visualizer":
            self.view_visualizer.pack(fill="both", expand=True)
        elif tab_id == "benchmark":
            self.view_benchmark.pack(fill="both", expand=True)
            self.refresh_benchmark_table()
        elif tab_id == "analysis":
            self.view_analysis.pack(fill="both", expand=True)

        for tid, btn in self.tab_buttons.items():
            btn.set_active_tab(tid == tab_id)

    # =========================================================================
    # TAB 1: VISUALIZER & EXECUTION INSTRUMENTS
    # =========================================================================
    def build_visualizer_tab(self, parent: tk.Widget) -> None:
        self.build_telemetry_strip(parent)
        self.build_viz_stage(parent)
        self.build_unified_control_console(parent)
        self.build_inspection_workspace(parent)

    def build_telemetry_strip(self, parent: tk.Widget) -> None:
        strip = self.card(parent)
        strip.pack(fill="x", pady=(px(2), px(4)))

        metrics = [
            ("COMPARISONS", "statComparisons", "0", "ink"),
            ("RIGHT SHIFTS", "statShifts", "0", "ink"),
            ("ARRAY ACCESSES", "statAccesses", "0", "accent"),
            ("WALL TIME", "statTime", "0 ms", "accent_cyan"),
            ("CURRENT PASS", "statPass", "0 of 0", "ink"),
            ("DIMENSION N", "statSize", f"{DEFAULT_SIZE} items", "soft"),
            ("SORTED INVARIANT", "statSorted", f"0 / {DEFAULT_SIZE}", "sorted"),
            ("PHASE", "statPhase", "READY", "accent"),
        ]
        for col, (label_text, key, initial_val, color_role) in enumerate(metrics):
            strip.grid_columnconfigure(col, weight=1, uniform="tel")
            cell = self.frame(strip, bg="card")
            cell.grid(row=0, column=col, sticky="nsew", padx=px(2), pady=px(4))
            if col > 0:
                sep = tk.Frame(cell, width=1, bd=0)
                self.reg(sep, bg="line")
                sep.pack(side="left", fill="y", padx=(0, px(6)))
            inner = self.frame(cell, bg="card")
            inner.pack(side="left", fill="both", expand=True)
            self.label(inner, label_text, "tag", fg="muted", bg="card").pack(anchor="w", padx=px(4), pady=(px(2), 0))
            val_lb = self.label(inner, initial_val, "mono_b", fg=color_role, bg="card")
            val_lb.pack(anchor="w", padx=px(4), pady=(0, px(2)))
            self.w[key] = val_lb

    def build_viz_stage(self, parent: tk.Widget) -> None:
        card = self.card(parent)
        card.pack(fill="x", pady=(px(2), 0))

        # Precision Chart Header
        top = self.frame(card)
        top.pack(fill="x", padx=px(14), pady=(px(8), px(4)))
        
        self.portion_tag(top, COLORS["sorted"], "Sorted Invariant Subarray A[0..i-1]", "sortedTag").pack(side="left")

        center_info = self.frame(top)
        center_info.pack(side="left", expand=True)
        self.w["invCount"] = self.label(center_info, "Inversions remaining: 0", "mono_s", fg="soft")
        self.w["invCount"].pack(anchor="center")

        self.portion_tag(top, COLORS["normal"], "Unsorted Array Domain A[i..n-1]", "unsortedTag").pack(side="right")

        # Scientific Oscilloscope Canvas
        self.chart = tk.Canvas(card, height=px(290), highlightthickness=0, bd=0)
        self.chart.pack(fill="x", padx=px(14))
        self.chart.bind("<Configure>", self.on_chart_resize)
        self.chart.bind("<Button-1>", lambda e: self.hide_completion())
        self.build_chart_items()

        # Integrated Technical Legend Ribbon
        legend = self.frame(card)
        legend.pack(fill="x", padx=px(14), pady=(px(6), px(8)))
        items = [
            ("normal", "Unsorted Element"),
            ("sorted", "Sorted Partition (A[0..i-1])"),
            ("compare", "Active Comparison"),
            ("shift", "Rightward Shift"),
            ("key", "Extracted Key (A[i])"),
            ("target", "Target Slot"),
        ]
        for column, (name, text) in enumerate(items):
            legend.grid_columnconfigure(column, weight=1, uniform="legend")
            cell = self.frame(legend)
            cell.grid(row=0, column=column, sticky="w")
            swatch = tk.Canvas(cell, width=px(10), height=px(10), highlightthickness=0, bd=0)
            self.reg(swatch, bg="card")
            round_rect(swatch, 1, 1, px(10) - 1, px(10) - 1, px(2), fill=COLORS[name])
            swatch.pack(side="left")
            self.label(cell, text, "small", fg="soft").pack(side="left", padx=(px(5), 0))

        self.build_completion()

    def portion_tag(self, parent: tk.Widget, color: str, text: str, key: str) -> tk.Frame:
        box = self.frame(parent)
        dot = tk.Canvas(box, width=px(8), height=px(8), highlightthickness=0, bd=0)
        self.reg(dot, bg="card")
        dot.create_oval(1, 1, px(8) - 1, px(8) - 1, fill=color, outline="")
        dot.pack(side="left")
        self.label(box, text, "small", fg="soft").pack(side="left", padx=(px(5), px(5)))
        self.w[key] = self.label(box, "0 bars", "mono_s")
        self.w[key].pack(side="left")
        return box

    def build_chart_items(self) -> None:
        c = self.chart
        # Invariant Region Shaded Overlays
        self.strip_sorted = c.create_rectangle(0, 0, 0, 0, fill=COLORS["sorted"], outline="")
        self.strip_unsorted = c.create_rectangle(0, 0, 0, 0, fill=COLORS["normal"], outline="")
        self.ghost = c.create_rectangle(
            0, 0, 0, 0, outline=COLORS["target"], width=2, dash=(4, 3), state="hidden"
        )
        self.divider_glow = c.create_line(0, 0, 0, 0, width=px(6), tags="top")
        self.divider = c.create_line(0, 0, 0, 0, width=px(2), fill=COLORS["sorted"], tags="top")
        self.label_sorted = c.create_text(
            0, 0, text="◄ SORTED INVARIANT [0 .. i-1]", anchor="e", font=self.f["tag"], fill=COLORS["sorted"], tags="top"
        )
        self.label_unsorted = c.create_text(
            0, 0, text="UNSORTED DOMAIN [i .. n-1] ►", anchor="w", font=self.f["tag"], fill=COLORS["normal"], tags="top"
        )
        self.tag_bg = c.create_polygon(0, 0, 0, 0, 0, 0, smooth=True, fill=COLORS["key"], outline="", state="hidden", tags="top")
        self.tag_txt = c.create_text(0, 0, text="KEY", font=self.f["tag"], fill="#FFFFFF", state="hidden", tags="top")

    def build_completion(self) -> None:
        box = tk.Frame(self.chart, bd=0, highlightthickness=1)
        self.reg(box, bg="card", highlightbackground="border", highlightcolor="border")
        self.done = box
        self.label(box, "Sorting Completed Successfully", "h2big").pack(padx=px(28), pady=(px(14), px(2)))
        self.label(box, "Inductive invariant proven across all N passes", "small", fg="soft").pack()

        stats = self.frame(box)
        stats.pack(pady=(px(8), px(4)))
        for caption, key in (
            ("Comparisons", "doneComparisons"),
            ("Shifts", "doneShifts"),
            ("Accesses", "doneAccesses"),
            ("Wall Time", "doneTime"),
        ):
            t = self.tile(stats)
            t.pack(side="left", padx=px(3))
            self.label(t, caption, "small", fg="soft", bg="card2").pack(padx=px(10), pady=(px(4), 0))
            self.w[key] = self.label(t, "0", "mono_big", bg="card2")
            self.w[key].pack(padx=px(10), pady=(0, px(4)))

        self.w["doneArray"] = self.label(box, "", "mono_s", fg="soft", justify="center")
        self.w["doneArray"].pack(padx=px(14), pady=(px(4), px(6)))

        btn_row = self.frame(box)
        btn_row.pack(pady=(0, px(12)))

        export_json_btn = GlowButton(
            btn_row, "Export Trace JSON", self.export_trace_json, COLORS["accent"], self.f["small"],
            height=28, ghost=True, min_width=110
        )
        export_json_btn.pack(side="left", padx=px(3))
        self._custom.append(export_json_btn)

        close = GlowButton(
            btn_row, "Dismiss", self.hide_completion, COLORS["key"], self.f["small"],
            height=28, ghost=False, min_width=75
        )
        close.pack(side="left", padx=px(3))
        self._custom.append(close)

    # -------------------------------------------------------------------------
    # Unified Execution Console (Cohesive Technical Command Deck)
    # -------------------------------------------------------------------------
    def build_unified_control_console(self, parent: tk.Widget) -> None:
        card = self.card(parent)
        card.pack(fill="x", pady=(px(6), 0))

        # Row 1: Dataset Presets & Seed Bar
        row1 = self.frame(card)
        row1.pack(fill="x", padx=px(14), pady=(px(8), px(4)))

        self.label(row1, "INPUT DATASET:", "bold", fg="soft").pack(side="left", padx=(0, px(8)))

        presets = [
            ("Random", "Random"),
            ("Sorted (Best)", "Sorted"),
            ("Reversed (Worst)", "Reversed"),
            ("Nearly Sorted", "Nearly Sorted"),
            ("Few Unique", "Few Unique"),
        ]

        self.preset_buttons: Dict[str, GlowButton] = {}
        for p_label, p_type in presets:
            btn = GlowButton(
                row1,
                p_label,
                lambda pt=p_type: self.apply_preset(pt),
                COLORS["accent"],
                self.f["small"],
                height=26,
                is_preset=True,
                min_width=72,
            )
            btn.pack(side="left", padx=px(2))
            self._custom.append(btn)
            self.preset_buttons[p_type] = btn

        custom_btn = GlowButton(
            row1,
            "Custom Array…",
            self.prompt_custom_array,
            COLORS["accent"],
            self.f["small"],
            height=26,
            ghost=True,
            min_width=82,
        )
        custom_btn.pack(side="left", padx=(px(6), px(2)))
        self._custom.append(custom_btn)

        seed_box = self.frame(row1)
        seed_box.pack(side="right")
        self.label(seed_box, "PRNG Seed:", "small", fg="soft").pack(side="left", padx=(0, px(4)))
        self.seed_entry = tk.Entry(
            seed_box, width=6, font=self.f["mono_s"], bd=0, highlightthickness=1, justify="center"
        )
        self.reg(self.seed_entry, bg="card2", fg="ink", highlightbackground="border", highlightcolor="accent")
        self.seed_entry.pack(side="left", padx=(0, px(4)))
        self.seed_entry.bind("<Return>", lambda e: self.apply_seed_from_entry())

        apply_seed_btn = GlowButton(
            seed_box, "Apply", self.apply_seed_from_entry, COLORS["accent"], self.f["small"],
            height=24, ghost=True, min_width=42
        )
        apply_seed_btn.pack(side="left")
        self._custom.append(apply_seed_btn)

        # Hairline Separator
        div_line = tk.Frame(card, height=1, bd=0)
        self.reg(div_line, bg="line")
        div_line.pack(fill="x", padx=px(14), pady=px(3))

        # Row 2: Transport Execution Bar
        row2 = self.frame(card)
        row2.pack(fill="x", padx=px(12), pady=(px(4), px(6)))

        specs = [
            ("▶ Auto-Run", COLORS["accent"], self.start_sorting, "btn_start", True),
            ("⏭ Step Forward", COLORS["cyan"], self.step_forward, "btn_step", False),
            ("⏸ Pause", COLORS["compare"], self.pause_sorting, "btn_pause", False),
            ("▶ Resume", COLORS["key"], self.resume_sorting, "btn_resume", False),
            ("↺ Reset", COLORS["shift"], self.reset_sorting, "btn_reset", False),
            ("⚡ Generate", COLORS["normal"], self.on_generate, "btn_generate", False),
        ]
        for column, (text, color, command, attr, is_hero) in enumerate(specs):
            row2.grid_columnconfigure(column, weight=1, uniform="c_btns")
            btn = GlowButton(row2, text, command, color, self.f["btn"], height=30, is_hero=is_hero)
            btn.grid(row=0, column=column, sticky="ew", padx=px(2))
            self._custom.append(btn)
            setattr(self, attr, btn)

        # Row 3: Parameter Sliders & Convergence Status (3 Columns)
        row3 = self.frame(card, bg="card3")
        row3.pack(fill="x", padx=px(12), pady=(0, px(8)))
        row3.grid_columnconfigure(0, weight=1, uniform="p_cols")
        row3.grid_columnconfigure(1, weight=1, uniform="p_cols")
        row3.grid_columnconfigure(2, weight=1, uniform="p_cols")

        # Col 1: Speed Slider
        s1 = self.frame(row3, bg="card3")
        s1.grid(row=0, column=0, sticky="ew", padx=px(6), pady=px(6))
        h1 = self.frame(s1, bg="card3")
        h1.pack(fill="x")
        self.label(h1, "Speed / Delay", "small", fg="soft", bg="card3").pack(side="left")
        self.w["speedValue"] = self.label(h1, "", "mono_s", bg="card3")
        self.w["speedValue"].pack(side="right")
        self.speed_slider = Slider(s1, 1, 100, DEFAULT_SPEED, lambda v: self.update_speed())
        self.speed_slider.pack(fill="x", pady=(px(2), 0))
        self._custom.append(self.speed_slider)

        # Col 2: Size Slider
        s2 = self.frame(row3, bg="card3")
        s2.grid(row=0, column=1, sticky="ew", padx=px(6), pady=px(6))
        h2 = self.frame(s2, bg="card3")
        h2.pack(fill="x")
        self.label(h2, "Dimension N", "small", fg="soft", bg="card3").pack(side="left")
        self.w["sizeValue"] = self.label(h2, "", "mono_s", bg="card3")
        self.w["sizeValue"].pack(side="right")
        self.size_slider = Slider(s2, MIN_SIZE, MAX_SIZE, DEFAULT_SIZE, lambda v: self.update_array_size())
        self.size_slider.pack(fill="x", pady=(px(2), 0))
        self._custom.append(self.size_slider)

        # Col 3: Pass Convergence
        s3 = self.frame(row3, bg="card3")
        s3.grid(row=0, column=2, sticky="ew", padx=px(6), pady=px(6))
        h3 = self.frame(s3, bg="card3")
        h3.pack(fill="x")
        self.w["progressMeta"] = self.label(h3, "Pass 0 of 0", "small", fg="soft", bg="card3")
        self.w["progressMeta"].pack(side="left")
        self.w["progressPercent"] = self.label(h3, "0%", "mono_b", bg="card3")
        self.w["progressPercent"].pack(side="right")
        self.progress = ProgressBar(s3)
        self.progress.pack(fill="x", pady=(px(4), 0))
        self._custom.append(self.progress)

    def apply_preset(self, preset_name: str) -> None:
        if self.state in (SORTING, PAUSED, BENCHMARKING):
            return
        self.current_preset = preset_name
        for pt, btn in self.preset_buttons.items():
            btn.set_active_preset(pt == preset_name)
        self.cancel_pending()
        size = int(self.size_slider.get())
        seed = int(self.seed_entry.get().strip()) if self.seed_entry.get().strip().isdigit() else None
        self.values = generate_distribution(preset_name, size, seed=seed)
        self.original = list(self.values)
        self.render_array()
        self.reset_stats_and_panels()
        self.set_state(IDLE)
        self.setw("stepMessage", f"Generated '{preset_name}' distribution ({size} elements).")

    def apply_seed_from_entry(self) -> None:
        raw = self.seed_entry.get().strip()
        if raw.isdigit():
            self.current_seed = int(raw)
            self.apply_preset(self.current_preset)
        elif raw == "":
            self.current_seed = None
            self.apply_preset(self.current_preset)
        else:
            messagebox.showwarning("Invalid Seed", "Please enter an integer seed or leave empty.")

    def prompt_custom_array(self) -> None:
        if self.state in (SORTING, PAUSED, BENCHMARKING):
            return
        dialog = tk.Toplevel(self.root)
        dialog.title("Custom Input Array")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg=self.th["bg"])
        dialog.geometry(f"{px(380)}x{px(200)}")

        fr = tk.Frame(dialog, bg=self.th["bg"], padx=px(16), pady=px(14))
        fr.pack(fill="both", expand=True)

        tk.Label(
            fr, text="Custom Array Values (comma-separated):", font=self.f["bold"],
            bg=self.th["bg"], fg=self.th["ink"]
        ).pack(anchor="w")
        tk.Label(
            fr, text="Enter 4 to 60 integers (1 to 100):", font=self.f["small"],
            bg=self.th["bg"], fg=self.th["soft"]
        ).pack(anchor="w", pady=(0, px(6)))

        initial_val = ", ".join(str(v) for v in self.values[:20])
        entry = tk.Entry(fr, font=self.f["mono"], bd=0, highlightthickness=1)
        entry.configure(bg=self.th["card"], fg=self.th["ink"], highlightbackground=self.th["border"])
        entry.insert(0, initial_val)
        entry.pack(fill="x", pady=px(4))
        entry.focus_set()

        err_lb = tk.Label(fr, text="", font=self.f["small"], bg=self.th["bg"], fg=COLORS["shift"])
        err_lb.pack(anchor="w")

        def submit():
            raw = entry.get().replace("[", "").replace("]", "").replace(";", ",")
            parts = [p.strip() for p in raw.split(",") if p.strip()]
            try:
                nums = [int(p) for p in parts]
                if len(nums) < 4:
                    err_lb.configure(text="Please provide at least 4 numbers.")
                    return
                if len(nums) > 60:
                    err_lb.configure(text="Maximum 60 numbers allowed.")
                    return
                if any(n < 1 or n > 150 for n in nums):
                    err_lb.configure(text="Values must be between 1 and 150.")
                    return
            except ValueError:
                err_lb.configure(text="Invalid format. Please enter numbers.")
                return

            dialog.destroy()
            self.cancel_pending()
            self.values = nums
            self.original = list(nums)
            self.size_slider.set(len(nums))
            self.setw("sizeValue", f"{len(nums)} bars")
            self.render_array()
            self.reset_stats_and_panels()
            self.set_state(IDLE)
            self.setw("stepMessage", f"Custom array loaded ({len(nums)} elements). Press Auto-Run or Step.")

        btn_box = tk.Frame(fr, bg=self.th["bg"])
        btn_box.pack(side="bottom", fill="x", pady=(px(8), 0))

        ok_btn = GlowButton(btn_box, "Apply Array", submit, COLORS["sorted"], self.f["btn"], height=28)
        ok_btn.pack(side="right", padx=(px(4), 0))
        ok_btn.apply_theme(self.th)

        cancel_btn = GlowButton(btn_box, "Cancel", dialog.destroy, COLORS["normal"], self.f["btn"], height=28, ghost=True)
        cancel_btn.pack(side="right")
        cancel_btn.apply_theme(self.th)

    # -------------------------------------------------------------------------
    # Live Inspection Workspace (Coordinated Scientific Instruments)
    # -------------------------------------------------------------------------
    def build_inspection_workspace(self, parent: tk.Widget) -> None:
        row = self.frame(parent, bg="bg")
        row.pack(fill="x", pady=(px(6), 0))
        row.grid_columnconfigure(0, weight=6, uniform="insp")
        row.grid_columnconfigure(1, weight=5, uniform="insp")

        # Instrument 1: Real-Time Telemetry & Decision Matrix (Left)
        left_card = self.card(row)
        left_card.grid(row=0, column=0, sticky="nsew", padx=(0, px(4)))
        self.label(left_card, "OPERATION NARRATIVE & DECISION MATRIX", "h2").pack(anchor="w", padx=px(14), pady=(px(8), px(4)))

        # Monospace Operation Ticker
        ticker_box = self.frame(left_card, bg="code_bg")
        ticker_box.pack(fill="x", padx=px(14), pady=(0, px(4)))
        
        self.w["stepMessage"] = self.label(
            ticker_box, "", "mono", fg="accent", bg="code_bg", anchor="w", justify="left",
            padx=px(8), pady=px(6), height=2
        )
        self.w["stepMessage"].pack(fill="x")
        self.autowrap(self.w["stepMessage"], px(24))

        # Algorithmic State Micro-Table
        matrix_box = self.tile(left_card)
        matrix_box.pack(fill="x", padx=px(14), pady=px(3))
        matrix_box.grid_columnconfigure(0, weight=1, uniform="m")
        matrix_box.grid_columnconfigure(1, weight=1, uniform="m")
        matrix_box.grid_columnconfigure(2, weight=2, uniform="m")

        self.edu_cell(matrix_box, "Key A[i]", "eduKey", 0, 0)
        self.edu_cell(matrix_box, "Comparing A[j]", "eduCompare", 0, 1)
        action_lb = self.edu_cell(matrix_box, "Algorithmic Decision", "eduAction", 0, 2, font="bold")
        self.autowrap(action_lb, px(16))

        # Fading 3-Line Operation History
        self.history_labels: List[tk.Label] = []
        for _ in range(3):
            lb = self.label(left_card, "", "mono_s", anchor="w")
            lb.pack(fill="x", padx=px(16), pady=(px(1), 0))
            self.history_labels.append(lb)
        self._hooks.append(self.color_history)

        # Telemetry Metrics Cluster (6 Cells)
        stat_head = self.frame(left_card)
        stat_head.pack(fill="x", padx=px(14), pady=(px(6), px(2)))
        self.label(stat_head, "COMPUTATIONAL COMPLEXITY TELEMETRY", "tag", fg="soft").pack(side="left")

        stat_grid = self.frame(left_card)
        stat_grid.pack(fill="both", expand=True, padx=px(12), pady=(0, px(8)))
        for c in range(3):
            stat_grid.grid_columnconfigure(c, weight=1, uniform="st_cells")

        tiles = [
            ("Comparisons", "statComparisons"),
            ("Right Shifts", "statShifts"),
            ("Array Accesses", "statAccesses"),
            ("Wall Time", "statTime"),
            ("Current Pass", "statPass"),
            ("Theoretical O(n²)", "statTheoretical"),
        ]
        for idx, (caption, key) in enumerate(tiles):
            stat_grid.grid_rowconfigure(idx // 3, weight=1)
            t = self.tile(stat_grid)
            t.grid(row=idx // 3, column=idx % 3, sticky="nsew", padx=px(2), pady=px(2))
            self.label(t, caption, "small", fg="soft", bg="card2").pack(anchor="w", padx=px(6), pady=(px(4), 0))
            self.w[key] = self.label(t, "0", "mono_big", bg="card2", anchor="w")
            self.w[key].pack(fill="x", padx=px(6), pady=(0, px(4)))

        # Instrument 2: Synchronized Pseudocode & Invariant Ledger (Right)
        right_card = self.card(row)
        right_card.grid(row=0, column=1, sticky="nsew", padx=(px(4), 0))
        
        head_r = self.frame(right_card)
        head_r.pack(fill="x", padx=px(14), pady=(px(8), px(4)))
        self.label(head_r, "SYNCHRONIZED CLRS PSEUDOCODE", "h2").pack(side="left")
        self.label(head_r, "ALGORITHM PROOF", "tag", fg="accent").pack(side="right")

        self.code_lines = [
            (1, "for i = 1 to length[A] - 1:"),
            (2, "    key = A[i]"),
            (3, "    j = i - 1"),
            (4, "    while j >= 0 and A[j] > key:"),
            (5, "        A[j + 1] = A[j]    # shift right"),
            (6, "        j = j - 1"),
            (7, "    A[j + 1] = key         # insert key"),
        ]

        code_box = self.frame(right_card, bg="code_bg")
        code_box.pack(fill="x", padx=px(14), pady=px(4))

        self.code_labels: Dict[int, Tuple[tk.Frame, tk.Label, tk.Label, tk.Label]] = {}
        for num, text in self.code_lines:
            line_fr = self.frame(code_box, bg="code_bg")
            line_fr.pack(fill="x", pady=px(1))

            chevron_lb = self.label(line_fr, " ", "mono_s", fg="accent", bg="code_bg", width=2, anchor="center")
            chevron_lb.pack(side="left")

            num_lb = self.label(line_fr, f"{num:2d} ", "mono_s", fg="code_num", bg="code_bg", width=3, anchor="e")
            num_lb.pack(side="left")

            txt_lb = self.label(line_fr, text, "code", fg="ink", bg="code_bg", anchor="w")
            txt_lb.pack(side="left", fill="x", expand=True, padx=(px(4), 0))

            self.code_labels[num] = (line_fr, num_lb, txt_lb, chevron_lb)

        # Formal Invariant Theorem Statement
        inv_box = self.tile(right_card)
        inv_box.pack(fill="x", padx=px(14), pady=px(4))
        self.label(inv_box, "LOOP INVARIANT THEOREM:", "tag", fg="sorted", bg="card2").pack(anchor="w", padx=px(8), pady=(px(4), 0))
        self.w["invText"] = self.label(
            inv_box,
            "At start of iteration i, subarray A[0 .. i-1] contains the original elements in strictly sorted order.",
            "small", fg="ink", bg="card2", anchor="w", justify="left"
        )
        self.w["invText"].pack(fill="x", padx=px(8), pady=(px(1), px(6)))
        self.autowrap(self.w["invText"], px(20))

        # Subarray Partitions Monospace Readout
        part_box = self.frame(right_card)
        part_box.pack(fill="x", padx=px(14), pady=(0, px(8)))

        for title, color, key in (
            ("Sorted Subarray A[0..i-1]:", COLORS["sorted"], "sortedList"),
            ("Unsorted Domain A[i..n-1]:", COLORS["normal"], "unsortedList"),
        ):
            p_head = self.frame(part_box)
            p_head.pack(fill="x", pady=(px(2), 0))
            self.label(p_head, title, "tag", fg="soft").pack(side="left")
            lb = self.label(part_box, "", "mono_s", anchor="w", justify="left")
            lb.pack(fill="x")
            self.autowrap(lb, px(24))
            self.w[key] = lb

    def edu_cell(self, parent: tk.Widget, caption: str, key: str, row: int, column: int, span: int = 1, font: str = "mono_b") -> tk.Label:
        t = self.tile(parent)
        t.grid(row=row, column=column, columnspan=span, sticky="nsew", padx=px(2), pady=px(2))
        self.label(t, caption, "small", fg="soft", bg="card2").pack(anchor="w", padx=px(6), pady=(px(2), 0))
        value = self.label(t, "—", font, bg="card2", anchor="w", justify="left")
        value.pack(fill="x", padx=px(6), pady=(0, px(4)))
        self.w[key] = value
        return value

    def color_history(self, th: Dict[str, Any]) -> None:
        for label, strength in zip(self.history_labels, (0.75, 0.45, 0.25)):
            label.configure(fg=mix(th["card"], th["soft"], strength))

    def highlight_pseudocode_line(self, line_num: int) -> None:
        self.active_code_line = line_num
        th = self.th
        if not hasattr(self, "code_labels") or not th:
            return
        for num, (fr, num_lb, txt_lb, chevron_lb) in self.code_labels.items():
            if num == line_num:
                fr.configure(bg=th["code_hl"])
                chevron_lb.configure(bg=th["code_hl"], fg=th["accent"], text="▶")
                num_lb.configure(bg=th["code_hl"], fg=th["accent"])
                txt_lb.configure(bg=th["code_hl"], fg=th["ink"], font=self.f["code_bold"])
            else:
                fr.configure(bg=th["code_bg"])
                chevron_lb.configure(bg=th["code_bg"], fg=th["code_bg"], text=" ")
                num_lb.configure(bg=th["code_bg"], fg=th["code_num"])
                txt_lb.configure(bg=th["code_bg"], fg=th["soft"], font=self.f["code"])

    # =========================================================================
    # TAB 2: EMPIRICAL BENCHMARK LABORATORY
    # =========================================================================
    def build_benchmark_tab(self, parent: tk.Widget) -> None:
        card = self.card(parent)
        card.pack(fill="x", pady=(px(2), 0))

        head = self.frame(card)
        head.pack(fill="x", padx=px(16), pady=(px(10), px(4)))
        self.label(head, "Empirical Performance & Scaling Benchmark Suite", "h2").pack(side="left")
        self.label(
            head,
            "Direct Headless Execution Engine (Nanosecond Precision)",
            "tag", fg="soft"
        ).pack(side="right")

        desc = self.label(
            card,
            "Headless benchmarking across input dimensions (N) and distributions. "
            "Measures exact operations, wall-clock latency, and empirical growth factors.",
            "body", fg="soft"
        )
        desc.pack(fill="x", padx=px(16), pady=(0, px(8)))
        self.autowrap(desc, px(32))

        ctrl_bar = self.frame(card)
        ctrl_bar.pack(fill="x", padx=px(16), pady=(0, px(10)))

        run_bench_btn = GlowButton(
            ctrl_bar, "▶ Run Benchmark Suite", self.run_empirical_benchmark, COLORS["accent"], self.f["btn"],
            height=30, min_width=140, is_hero=True
        )
        run_bench_btn.pack(side="left", padx=(0, px(6)))
        self._custom.append(run_bench_btn)

        export_csv_btn = GlowButton(
            ctrl_bar, "↓ Export CSV", self.export_benchmark_csv, COLORS["cyan"], self.f["btn"],
            height=30, ghost=True, min_width=90
        )
        export_csv_btn.pack(side="left", padx=(0, px(6)))
        self._custom.append(export_csv_btn)

        clear_btn = GlowButton(
            ctrl_bar, "✕ Clear Data", self.clear_benchmark_data, COLORS["shift"], self.f["btn"],
            height=30, ghost=True, min_width=85
        )
        clear_btn.pack(side="left")
        self._custom.append(clear_btn)

        self.w["benchStatus"] = self.label(ctrl_bar, "Status: Ready", "mono_s", fg="soft")
        self.w["benchStatus"].pack(side="right", padx=px(6))

        # Benchmark Table Card
        table_card = self.card(parent)
        table_card.pack(fill="both", expand=True, pady=(px(6), 0))
        self.label(table_card, "Empirical Measurement Results", "h2").pack(anchor="w", padx=px(16), pady=(px(10), px(4)))

        self.table_frame = self.frame(table_card)
        self.table_frame.pack(fill="x", padx=px(16), pady=(0, px(12)))

        # Scaling Chart Canvas
        chart_card = self.card(parent)
        chart_card.pack(fill="x", pady=(px(6), 0))
        self.label(chart_card, "Empirical Scaling Curve vs Asymptotic Bounds", "h2").pack(anchor="w", padx=px(16), pady=(px(10), px(4)))

        self.bench_chart = tk.Canvas(chart_card, height=px(210), highlightthickness=0, bd=0)
        self.bench_chart.pack(fill="x", padx=px(16), pady=(0, px(12)))
        self.bench_chart.bind("<Configure>", lambda e: self.draw_benchmark_chart())

    def clear_benchmark_data(self) -> None:
        self.benchmark_records.clear()
        self.refresh_benchmark_table()
        self.draw_benchmark_chart()
        self.setw("benchStatus", "Status: Ready (Data Cleared)")

    def run_empirical_benchmark(self) -> None:
        if self.is_benchmarking:
            return
        self.is_benchmarking = True
        self.set_state(BENCHMARKING)
        self.setw("benchStatus", "Status: Benchmarking in progress…")
        self.root.update_idletasks()

        sizes = [50, 100, 250, 500, 1000, 2000]
        distributions = ["Random", "Sorted (Best)", "Reversed (Worst)", "Nearly Sorted"]

        self.benchmark_records.clear()
        prev_records_by_dist: Dict[str, BenchmarkResult] = {}
        for dist in distributions:
            for n in sizes:
                arr = generate_distribution(dist, n, seed=42)
                _, metrics = insertion_sort_headless(arr)
                theoretical = n - 1 if "sorted" in dist.lower() and "nearly" not in dist.lower() else (n * (n - 1)) / 2.0
                growth = None
                if dist in prev_records_by_dist:
                    prev = prev_records_by_dist[dist]
                    if prev.size > 0 and prev.elapsed_us > 0:
                        growth = metrics["elapsed_us"] / prev.elapsed_us

                res = BenchmarkResult(
                    distribution=dist,
                    size=n,
                    elapsed_us=metrics["elapsed_us"],
                    comparisons=metrics["comparisons"],
                    shifts=metrics["shifts"],
                    accesses=metrics["accesses"],
                    theoretical_comparisons=theoretical,
                    growth_ratio=growth,
                )
                self.benchmark_records.append(res)
                prev_records_by_dist[dist] = res

        self.is_benchmarking = False
        self.set_state(IDLE)
        self.setw("benchStatus", f"Status: Completed ({len(self.benchmark_records)} trials)")
        self.refresh_benchmark_table()
        self.draw_benchmark_chart()

    def refresh_benchmark_table(self) -> None:
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        headers = [
            ("Distribution", 16),
            ("Dimension N", 12),
            ("Elapsed Time", 12),
            ("Comparisons", 12),
            ("Shifts", 12),
            ("Accesses", 12),
            ("Theoretical", 14),
            ("Growth Ratio", 12),
        ]

        hdr_row = self.frame(self.table_frame, bg="card2")
        hdr_row.pack(fill="x", pady=px(2))
        for col, width in headers:
            lb = self.label(hdr_row, col, "bold", fg="soft", bg="card2", width=width, anchor="w")
            lb.pack(side="left", padx=px(5), pady=px(4))

        if not self.benchmark_records:
            empty = self.label(
                self.table_frame, "No benchmark data. Click 'Run Benchmark Suite' to execute.",
                "small", fg="soft"
            )
            empty.pack(pady=px(12))
            return

        for idx, rec in enumerate(self.benchmark_records):
            row_bg = "card" if idx % 2 == 0 else "card2"
            row_fr = self.frame(self.table_frame, bg=row_bg)
            row_fr.pack(fill="x", pady=px(1))

            time_str = f"{rec.elapsed_us:.1f} µs" if rec.elapsed_us < 1000 else f"{rec.elapsed_us / 1000.0:.2f} ms"
            growth_str = f"{rec.growth_ratio:.2f}x" if rec.growth_ratio is not None else "—"

            vals = [
                (rec.distribution, 16, "ink"),
                (str(rec.size), 12, "accent"),
                (time_str, 12, "cyan"),
                (f"{rec.comparisons:,}", 12, "compare"),
                (f"{rec.shifts:,}", 12, "shift"),
                (f"{rec.accesses:,}", 12, "soft"),
                (f"{int(rec.theoretical_comparisons):,}", 14, "muted"),
                (growth_str, 12, "sorted"),
            ]
            for val, width, color_key in vals:
                fg_col = self.th.get(color_key, COLORS.get(color_key, self.th["ink"]))
                lb = self.label(row_fr, val, "mono_s", fg=color_key, bg=row_bg, width=width, anchor="w")
                lb.configure(fg=fg_col)
                lb.pack(side="left", padx=px(5), pady=px(3))

    def draw_benchmark_chart(self) -> None:
        c = self.bench_chart
        c.delete("all")
        th = self.th
        if th is None:
            return
        c.configure(bg=th["card2"])

        w = max(300, c.winfo_width())
        h = max(180, c.winfo_height())
        pad_x, pad_y = px(45), px(22)
        plot_w = w - 2 * pad_x
        plot_h = h - 2 * pad_y

        c.create_line(pad_x, h - pad_y, w - pad_x, h - pad_y, fill=th["border"], width=px(1))
        c.create_line(pad_x, pad_y, pad_x, h - pad_y, fill=th["border"], width=px(1))

        c.create_text(w / 2, h - px(7), text="Dimension N", font=self.f["small"], fill=th["soft"])
        c.create_text(px(14), h / 2, text="Time (µs)", font=self.f["small"], fill=th["soft"], angle=90)

        if not self.benchmark_records:
            c.create_text(w / 2, h / 2, text="Run benchmark suite to plot empirical scaling curves", font=self.f["body"], fill=th["soft"])
            return

        max_n = max(r.size for r in self.benchmark_records)
        max_time = max(max(r.elapsed_us for r in self.benchmark_records), 1.0)

        for frac in (0.25, 0.50, 0.75, 1.0):
            y = h - pad_y - frac * plot_h
            c.create_line(pad_x, y, w - pad_x, y, fill=th["line"], dash=(2, 4))
            val_t = frac * max_time
            val_str = f"{val_t:.0f}µs" if val_t < 1000 else f"{val_t/1000:.1f}ms"
            c.create_text(pad_x - px(5), y, text=val_str, font=self.f["idx"], fill=th["muted"], anchor="e")

        by_dist: Dict[str, List[BenchmarkResult]] = {}
        for r in self.benchmark_records:
            by_dist.setdefault(r.distribution, []).append(r)

        palette = {
            "Random": COLORS["cyan"],
            "Sorted (Best)": COLORS["sorted"],
            "Reversed (Worst)": COLORS["shift"],
            "Nearly Sorted": COLORS["compare"],
        }

        legend_x = w - pad_x - px(150)
        legend_y = pad_y + px(6)

        for d_idx, (dist, records) in enumerate(by_dist.items()):
            col = palette.get(dist, COLORS["accent"])
            records.sort(key=lambda r: r.size)
            points = []
            for r in records:
                px_x = pad_x + (r.size / max_n) * plot_w
                px_y = h - pad_y - (r.elapsed_us / max_time) * plot_h
                points.append((px_x, px_y))

            if len(points) > 1:
                flat_pts = [coord for pt in points for coord in pt]
                c.create_line(flat_pts, fill=col, width=px(2), smooth=False)

            for px_x, px_y in points:
                c.create_oval(px_x - px(3), px_y - px(3), px_x + px(3), px_y + px(3), fill=col, outline=th["card2"], width=px(1))

            ly = legend_y + d_idx * px(15)
            c.create_line(legend_x, ly, legend_x + px(10), ly, fill=col, width=px(2))
            c.create_oval(legend_x + px(3), ly - px(3), legend_x + px(7), ly + px(3), fill=col, outline="")
            c.create_text(legend_x + px(15), ly, text=dist, font=self.f["small"], fill=th["ink"], anchor="w")

    # =========================================================================
    # TAB 3: INVARIANT PROOF & COMPLEXITY THEORY
    # =========================================================================
    def build_analysis_tab(self, parent: tk.Widget) -> None:
        card = self.card(parent)
        card.pack(fill="x", pady=(px(2), 0))

        self.label(card, "Formal Mathematical Proof of Correctness (CLRS)", "h2").pack(anchor="w", padx=px(16), pady=(px(10), px(4)))

        lead = self.label(
            card,
            "Insertion sort operates via an inductive incremental mechanism. Correctness is rigorously established "
            "using the loop invariant property over subarray A[0 .. i-1].",
            "body", fg="soft"
        )
        lead.pack(fill="x", padx=px(16), pady=(0, px(8)))
        self.autowrap(lead, px(32))

        proof_grid = self.frame(card)
        proof_grid.pack(fill="x", padx=px(12), pady=(0, px(12)))
        proof_grid.grid_columnconfigure(0, weight=1, uniform="pr")
        proof_grid.grid_columnconfigure(1, weight=1, uniform="pr")
        proof_grid.grid_columnconfigure(2, weight=1, uniform="pr")

        proof_steps = [
            ("1. INITIALIZATION (Base Case)",
             "Prior to iteration i = 1, subarray consists of only A[0]. "
             "A single element is trivially sorted, verifying the base invariant holds."),
            ("2. MAINTENANCE (Induction)",
             "The inner loop shifts elements A[j] > key to the right, preserving their relative sorted order "
             "and opening slot j+1 where key is placed. Subarray A[0 .. i] is therefore strictly sorted."),
            ("3. TERMINATION (Conclusion)",
             "The loop terminates when i = n. By substitution into the invariant, subarray A[0 .. n-1] contains all n original "
             "elements in strictly sorted order."),
        ]
        for col_idx, (p_title, p_body) in enumerate(proof_steps):
            t = self.tile(proof_grid)
            t.grid(row=0, column=col_idx, sticky="nsew", padx=px(3), pady=px(3))
            self.label(t, p_title, "bold", fg="accent", bg="card2").pack(anchor="w", padx=px(8), pady=(px(8), px(3)))
            txt = self.label(t, p_body, "small", fg="soft", bg="card2", anchor="nw", justify="left")
            txt.pack(fill="both", expand=True, padx=px(8), pady=(0, px(8)))
            self.autowrap(txt, px(18))

        card2 = self.card(parent)
        card2.pack(fill="x", pady=(px(8), 0))
        self.label(card2, "Stability & Spatial Invariants", "h2").pack(anchor="w", padx=px(16), pady=(px(10), px(4)))

        grid2 = self.frame(card2)
        grid2.pack(fill="x", padx=px(12), pady=(0, px(12)))
        grid2.grid_columnconfigure(0, weight=1, uniform="p2")
        grid2.grid_columnconfigure(1, weight=1, uniform="p2")

        t_stab = self.tile(grid2)
        t_stab.grid(row=0, column=0, sticky="nsew", padx=px(3), pady=px(3))
        self.label(t_stab, "Algorithmic Stability Invariant", "bold", fg="sorted", bg="card2").pack(anchor="w", padx=px(8), pady=(px(8), px(3)))
        s_txt = self.label(
            t_stab,
            "Insertion sort is strictly stable because shifting occurs only when A[j] > key. "
            "Equal keys (A[j] == key) halt the shift loop, preserving original relative positioning.",
            "small", fg="soft", bg="card2", anchor="nw", justify="left"
        )
        s_txt.pack(fill="both", expand=True, padx=px(8), pady=(0, px(8)))
        self.autowrap(s_txt, px(18))

        t_spat = self.tile(grid2)
        t_spat.grid(row=0, column=1, sticky="nsew", padx=px(3), pady=px(3))
        self.label(t_spat, "Spatial Complexity O(1) Auxiliary", "bold", fg="cyan", bg="card2").pack(anchor="w", padx=px(8), pady=(px(8), px(3)))
        sp_txt = self.label(
            t_spat,
            "Insertion sort is strictly in-place, requiring only O(1) auxiliary variables (key, i, j). "
            "All element movements occur directly within the existing memory allocation.",
            "small", fg="soft", bg="card2", anchor="nw", justify="left"
        )
        sp_txt.pack(fill="both", expand=True, padx=px(8), pady=(0, px(8)))
        self.autowrap(sp_txt, px(18))

        card3 = self.card(parent)
        card3.pack(fill="x", pady=(px(8), 0))
        self.label(card3, "Theoretical Asymptotic Complexity Profile", "h2").pack(anchor="w", padx=px(16), pady=(px(10), px(4)))

        grid3 = self.frame(card3)
        grid3.pack(fill="x", padx=px(12), pady=(0, px(12)))
        grid3.grid_columnconfigure(0, weight=1, uniform="p3")
        grid3.grid_columnconfigure(1, weight=1, uniform="p3")
        grid3.grid_columnconfigure(2, weight=1, uniform="p3")

        cases = [
            ("Best-Case: Ω(n)", "Occurs when array is already sorted. Exactly n - 1 comparisons executed and 0 element shifts. Outer loop iterates n - 1 times with instantaneous inner loop break.", "sorted"),
            ("Average-Case: Θ(n²)", "Expected running time over random permutations. Each key compares against roughly half the preceding sorted partition, resulting in ~ n²/4 comparisons and shifts.", "accent"),
            ("Worst-Case: O(n²)", "Occurs when array is strictly reversed. Every key A[i] must be compared with all i preceding elements and shifted, yielding exactly n(n-1)/2 comparisons and shifts.", "shift"),
        ]
        for col_idx, (c_title, c_desc, c_color) in enumerate(cases):
            t = self.tile(grid3)
            t.grid(row=0, column=col_idx, sticky="nsew", padx=px(3), pady=px(3))
            self.label(t, c_title, "bold", fg=c_color, bg="card2").pack(anchor="w", padx=px(8), pady=(px(8), px(3)))
            c_txt = self.label(t, c_desc, "small", fg="soft", bg="card2", anchor="nw", justify="left")
            c_txt.pack(fill="both", expand=True, padx=px(8), pady=(0, px(8)))
            self.autowrap(c_txt, px(18))

    # -------------------------------------------------------------------------
    # Chart Blueprint Layout & Rendering
    # -------------------------------------------------------------------------
    def generate_array(self, size: Optional[int] = None) -> None:
        size = size or int(self.size_slider.get())
        seed = int(self.seed_entry.get().strip()) if hasattr(self, "seed_entry") and self.seed_entry.get().strip().isdigit() else None
        self.values = generate_distribution(self.current_preset, size, seed=seed)
        self.original = list(self.values)
        self.render_array()
        self.reset_stats_and_panels()

    def render_array(self) -> None:
        c = self.chart
        c.delete("bar")
        c.delete("idx")
        self.bar_objs = []
        for index, value in enumerate(self.values):
            bar = Bar(value, index)
            bar.glow = c.create_rectangle(0, 0, 0, 0, outline="", tags="bar")
            bar.rect = c.create_rectangle(0, 0, 0, 0, outline="", tags="bar")
            bar.text = c.create_text(0, 0, text=str(value), font=self.f["bar"], tags="bar")
            self.bar_objs.append(bar)
        self.bars = list(self.bar_objs)
        self.idx_items = [
            c.create_text(0, 0, text=str(i), font=self.f["idx"], tags="idx", fill=self.th["soft"])
            for i in range(len(self.values))
        ]
        self.key_bar = None
        self.gap_index = None
        self.layout()
        c.tag_raise("top")
        c.tag_raise("confetti")

    def slot_x(self, index: int) -> float:
        return self.pad + index * self.slot + (self.slot - self.bw) / 2.0

    def layout(self) -> None:
        c = self.chart
        self.W = max(320, c.winfo_width())
        self.H = max(200, c.winfo_height())
        self.pad = px(38)  # Leave room for left Y-axis scale markings
        count = max(1, len(self.bar_objs))
        self.slot = (self.W - self.pad - px(16)) / count
        gap = min(px(6), max(1.0, self.slot * 0.16))
        self.bw = max(3.0, self.slot - gap)
        self.base = self.H - px(44)
        self.max_h = max(px(50), self.base - px(64))
        self.compact = self.slot < px(17)

        size = 9 if self.slot < px(22) else 10 if self.slot < px(30) else 11
        self.f["bar"].configure(size=-px(size))

        for bar in self.bar_objs:
            bar.h = max(px(8), bar.value / MAX_VALUE * self.max_h)
            bar.x = bar.tx = self.slot_x(bar.index)
            bar.lift = bar.tlift
            bar.drawn = None
            c.itemconfigure(bar.text, state="hidden" if self.compact else "normal")
        for i, item in enumerate(self.idx_items):
            c.coords(item, self.slot_x(i) + self.bw / 2, self.base + px(20))
            c.itemconfigure(item, state="hidden" if self.compact else "normal")
        self._overlay_sig = None

    def on_chart_resize(self, event: tk.Event) -> None:
        if abs(event.width - self.W) < 2 and abs(event.height - self.H) < 2:
            return
        self.layout()
        self.draw_chart_background()

    def draw_chart_background(self) -> None:
        c = self.chart
        c.delete("bg")
        th = self.th
        W = max(320, c.winfo_width())
        H = max(200, c.winfo_height())

        # Scientific Blueprint Coordinates & Reference Guides
        pad = int(self.pad) if self.pad > 0 else px(38)
        base = self.base if self.base > 0 else (H - px(44))
        max_h = self.max_h if self.max_h > 0 else (base - px(64))
        step_x = max(1, px(40))

        for gx in range(pad, max(pad + 1, int(W - px(10))), step_x):
            c.create_line(gx, px(16), gx, base, fill=th["grid_line"], width=1, tags="bg")

        # Y-Axis Scale Markings & Reference Horizontal Lines (0, 25, 50, 75, 100)
        for pct, val_label in ((1.0, "100"), (0.75, "75"), (0.50, "50"), (0.25, "25"), (0.0, "0")):
            y = base - pct * max_h
            c.create_line(pad - px(4), y, W - px(16), y, fill=th["grid_guide"], dash=(2, 4), tags="bg")
            c.create_text(pad - px(8), y, text=val_label, font=self.f["idx"], fill=th["muted"], anchor="e", tags="bg")

        # Baseline Axis Rule
        c.create_line(pad, base, W - px(16), base, fill=th["border"], width=px(1), tags="bg")
        c.tag_lower("bg")

    def refresh_chart_theme(self) -> None:
        if not hasattr(self, "chart"):
            return
        th = self.th
        self.chart.configure(bg=th["chart"])
        self.chart.itemconfigure(self.divider_glow, fill=mix(th["chart"], th["sorted"], 0.25))
        for item in self.idx_items:
            self.chart.itemconfigure(item, fill=th["soft"])
        for bar in self.bar_objs:
            bar.drawn = None
        self._overlay_sig = None
        self.draw_chart_background()

    def place(self, bar: Bar, index: int, lift: float = 0.0) -> None:
        bar.index = index
        bar.tx = self.slot_x(index)
        bar.tlift = lift

    def clear_bar_states(self) -> None:
        for bar in self.bar_objs:
            bar.state = "normal"
            bar.tlift = 0
            bar.flash = 0.0
        self.key_bar = None
        self.gap_index = None

    # -------------------------------------------------------------------------
    # Animation Tick Loop (~60 FPS)
    # -------------------------------------------------------------------------
    def tick(self) -> None:
        if self.closing:
            return
        now = time.perf_counter()
        dt = min(0.05, now - self.last_tick)
        self.last_tick = now
        try:
            self.animate_bars(dt)
            self.animate_overlay(dt)
            self.update_confetti(dt)
            self.progress.tick(dt, self.state == SORTING)
            if self.state == SORTING and now - self.last_clock > 0.05:
                self.last_clock = now
                self.setw("statTime", "%d ms" % self.elapsed_ms())
        except tk.TclError:
            return
        self.root.after(16, self.tick)

    def animate_bars(self, dt: float) -> None:
        move_alpha = 1.0 - math.exp(-dt / self.tau)
        color_alpha = 1.0 - math.exp(-dt / 0.07)
        for bar in self.bar_objs:
            dx = bar.tx - bar.x
            bar.x = bar.tx if abs(dx) < 0.25 else bar.x + dx * move_alpha
            dl = bar.tlift - bar.lift
            bar.lift = bar.tlift if abs(dl) < 0.25 else bar.lift + dl * move_alpha

            target = COLOR_RGB[bar.state]
            if bar.rgb != target:
                nxt = tuple(bar.rgb[i] + (target[i] - bar.rgb[i]) * color_alpha for i in range(3))
                if max(abs(nxt[i] - target[i]) for i in range(3)) < 1.5:
                    nxt = target
                bar.rgb = nxt
            if bar.flash > 0:
                bar.flash = max(0.0, bar.flash - dt * 3.0)

            signature = (round(bar.x, 1), round(bar.lift, 1), bar.rgb, round(bar.flash, 2), bar.state)
            if signature != bar.drawn:
                bar.drawn = signature
                self.draw_bar(bar)

    def draw_bar(self, bar: Bar) -> None:
        c = self.chart
        rgb = bar.rgb
        if bar.flash > 0:
            rgb = tuple(rgb[i] + (255 - rgb[i]) * 0.55 * bar.flash for i in range(3))
        fill = rgb_to_hex(rgb)
        active = bar.state in ACTIVE_STATES
        left, right = bar.x, bar.x + self.bw
        bottom = self.base - bar.lift
        top = bottom - bar.h
        g = px(2)

        c.coords(bar.glow, left - g, top - g, right + g, bottom + g)
        c.itemconfigure(bar.glow, fill=mix(self.th["chart"], fill, 0.35 if active else 0.12))
        c.coords(bar.rect, left, top, right, bottom)
        c.itemconfigure(bar.rect, fill=fill)
        c.coords(bar.text, left + self.bw / 2, top - px(8))
        c.itemconfigure(bar.text, fill=self.th["ink"] if active else self.th["soft"])

    def animate_overlay(self, dt: float) -> None:
        c = self.chart
        alpha = 1.0 - math.exp(-dt / self.tau)

        target = self.pad + self.div_count * self.slot
        diff = target - self.div_x
        self.div_x = target if abs(diff) < 0.25 else self.div_x + diff * alpha

        kb = self.key_bar
        want_ghost = kb is not None and self.gap_index is not None
        ghost_target = self.slot_x(self.gap_index) if want_ghost else self.ghost_x
        if want_ghost and not self._ghost_visible:
            self.ghost_x = ghost_target
        else:
            gd = ghost_target - self.ghost_x
            self.ghost_x = ghost_target if abs(gd) < 0.25 else self.ghost_x + gd * alpha
        if want_ghost:
            c.coords(self.ghost, self.ghost_x - 1, self.base - kb.h - 1, self.ghost_x + self.bw + 1, self.base)
        if want_ghost != self._ghost_visible:
            c.itemconfigure(self.ghost, state="normal" if want_ghost else "hidden")
            self._ghost_visible = want_ghost

        want_tag = kb is not None and kb.state in ("key", "target")
        if want_tag:
            text = f"KEY {kb.value}"
            half = (self.f["tag"].measure(text) + px(14)) / 2.0
            cx = clamp(kb.x + self.bw / 2, half + 4, self.W - half - 4)
            cy = self.base - kb.lift - kb.h - px(18)
            c.coords(self.tag_bg, *round_points(cx - half, cy - px(7), cx + half, cy + px(7), px(4)))
            c.coords(self.tag_txt, cx, cy)
            c.itemconfigure(self.tag_txt, text=text)
        if want_tag != self._tag_visible:
            state = "normal" if want_tag else "hidden"
            c.itemconfigure(self.tag_bg, state=state)
            c.itemconfigure(self.tag_txt, state=state)
            self._tag_visible = want_tag

        signature = (round(self.div_x, 1), self.W, self.H)
        if signature != self._overlay_sig:
            self._overlay_sig = signature
            x, y1, y2 = self.div_x, px(20), self.base + px(12)
            strip_top, strip_bottom = self.base + px(4), self.base + px(8)
            c.coords(self.strip_sorted, self.pad, strip_top, x, strip_bottom)
            c.coords(self.strip_unsorted, x, strip_top, self.W - px(16), strip_bottom)
            c.coords(self.divider_glow, x, y1, x, y2)
            c.coords(self.divider, x, y1, x, y2)
            c.coords(self.label_sorted, x - px(6), px(10))
            c.coords(self.label_unsorted, x + px(6), px(10))
            c.itemconfigure(self.label_sorted, state="normal" if x - self.pad > px(60) else "hidden")
            c.itemconfigure(self.label_unsorted, state="normal" if (self.W - px(16)) - x > px(80) else "hidden")

    # -------------------------------------------------------------------------
    # State Management & Telemetry
    # -------------------------------------------------------------------------
    def setw(self, key: str, text: Any) -> None:
        if key in self.w:
            label = self.w[key]
            text = str(text)
            if label.cget("text") != text:
                label.configure(text=text)

    def set_state(self, new_state: str) -> None:
        self.state = new_state
        self.badge.configure(text=f"● {STATE_TEXT[new_state]}", fg=STATE_COLORS[new_state])
        busy = new_state in (SORTING, PAUSED, BENCHMARKING)
        self.btn_generate.set_enabled(not busy)
        self.btn_start.set_enabled(not busy)
        self.btn_step.set_enabled(new_state != SORTING)
        self.btn_pause.set_enabled(new_state == SORTING)
        self.btn_resume.set_enabled(new_state == PAUSED)
        self.size_slider.set_enabled(not busy)

    def update_statistics(self) -> None:
        s = self.stats
        n = len(self.values)
        self.setw("statComparisons", f"{s.get('comparisons', 0):,}")
        self.setw("statShifts", f"{s.get('shifts', 0):,}")
        self.setw("statAccesses", f"{s.get('accesses', 0):,}")
        self.setw("statPass", f"{s.get('pass_no', 0)} of {max(1, n - 1)}")
        self.setw("statSize", f"{n} items")
        self.setw("statSorted", f"{s.get('sorted', 0)} / {n}")
        self.setw("statPhase", s.get("phase", "Ready").upper())
        self.setw("statTheoretical", f"{int(n * (n - 1) / 2):,}")
        self.setw("sortedTag", f"{s.get('sorted', 0)} {'bar' if s.get('sorted', 0) == 1 else 'bars'}")
        self.setw("unsortedTag", f"{n - s.get('sorted', 0)} bars")

        inversions = count_inversions(self.values)
        self.setw("invCount", f"Inversions remaining: {inversions}")

    def set_phase(self, phase: str) -> None:
        self.stats["phase"] = phase
        self.setw("statPhase", phase.upper())
        self.update_statistics()

    def update_portion_lists(self) -> None:
        limit = 10

        def show(key: str, numbers: List[int], color: str):
            if not numbers:
                self.w[key].configure(text="(empty)", fg=self.th["soft"])
                return
            shown = "  ".join(f"[{v}]" for v in numbers[:limit])
            if len(numbers) > limit:
                shown += f"  +{len(numbers) - limit} more"
            self.w[key].configure(text=shown, fg=color)

        sorted_count = self.stats.get("sorted", 0)
        show("sortedList", self.values[:sorted_count], self.th["sorted"])
        show("unsortedList", self.values[sorted_count:], self.th["normal"])

    def update_step_message(self, text: str) -> None:
        previous = self.w["stepMessage"].cget("text")
        if previous and previous != text:
            self.history_texts.insert(0, previous)
            del self.history_texts[3:]
            self.refresh_history()
        self.setw("stepMessage", text)

    def refresh_history(self) -> None:
        for i, label in enumerate(self.history_labels):
            label.configure(text=self.history_texts[i] if i < len(self.history_texts) else "")

    def update_progress(self, fraction: float) -> None:
        percent = int(round(clamp(fraction, 0.0, 1.0) * 100))
        self.setw("progressPercent", f"{percent}%")
        self.progress.set_target(fraction)
        self.setw("progressMeta", f"Pass {self.stats.get('pass_no', 0)} of {max(1, len(self.values) - 1)}")

    def elapsed_ms(self) -> float:
        running = time.perf_counter() - self.timer_started if self.timer_started else 0.0
        return (self.timer_elapsed + running) * 1000.0

    def start_timer(self) -> None:
        self.timer_started = time.perf_counter()

    def stop_timer(self) -> None:
        if self.timer_started is not None:
            self.timer_elapsed += time.perf_counter() - self.timer_started
            self.timer_started = None
        self.setw("statTime", "%d ms" % (self.timer_elapsed * 1000))

    def reset_timer(self) -> None:
        self.timer_started = None
        self.timer_elapsed = 0.0
        self.setw("statTime", "0 ms")

    def reset_stats_and_panels(self) -> None:
        self.stats = dict(comparisons=0, shifts=0, accesses=0, pass_no=0, key=None, sorted=0, phase="Ready")
        self.execution_trace.clear()
        self.reset_timer()
        self.hide_completion()
        self.chart.delete("confetti")
        self.confetti = []
        self.history_texts = []
        self.refresh_history()
        self.setw("stepMessage", "System Ready. Press 'Auto-Run' or 'Step Forward' to begin execution.")
        for key in ("eduKey", "eduCompare"):
            self.setw(key, "—")
        self.setw("eduAction", "Awaiting execution trigger")
        self.update_statistics()
        self.update_progress(0)
        self.progress.set_target(0, snap=True)
        self.update_portion_lists()
        self.highlight_pseudocode_line(1)
        self.div_count = 0
        self.div_x = self.pad

    def update_speed(self) -> None:
        delay = self.current_delay()
        self.tau = max(90, delay * 0.75) / 4000.0
        if delay < 80:
            label = "Ultra-Fast"
        elif delay < 180:
            label = "Fast"
        elif delay < 320:
            label = "Medium"
        elif delay < 480:
            label = "Deliberate"
        else:
            label = "Classroom Analysis"
        self.setw("speedValue", f"{label} ({delay} ms)")

    def current_delay(self) -> int:
        return int(round(620 - self.speed_slider.get() * 5.8))

    def update_array_size(self) -> None:
        size = int(self.size_slider.get())
        self.setw("sizeValue", f"{size} bars")
        if self.state in (SORTING, PAUSED, BENCHMARKING):
            return
        self.cancel_pending()
        self.generate_array(size)
        self.set_state(IDLE)
        self.setw("stepMessage", f"Generated new array ({size} bars).")

    # -------------------------------------------------------------------------
    # Visual Highlights
    # -------------------------------------------------------------------------
    def highlight_key(self, bar: Bar) -> None:
        bar.state = "key"
        bar.tlift = px(LIFT_HEIGHT)
        self.key_bar = bar
        for item in (bar.glow, bar.rect, bar.text):
            self.chart.tag_raise(item)
        self.chart.tag_raise("top")
        self.chart.tag_raise("confetti")

    def compare_elements(self, bar: Bar) -> None:
        bar.state = "compare"

    def shift_element(self, bar: Bar, to_index: int) -> None:
        bar.state = "shift"
        self.place(bar, to_index, 0)

    def move_key(self, bar: Bar, index: int) -> None:
        self.place(bar, index, px(LIFT_HEIGHT))

    def insert_key(self, bar: Bar, index: int) -> None:
        self.place(bar, index, 0)

    def mark_sorted(self, count: int) -> None:
        for k in range(count):
            self.bars[k].state = "sorted"
        self.stats["sorted"] = count
        self.div_count = count
        self.update_statistics()
        self.update_portion_lists()

    # -------------------------------------------------------------------------
    # The Insertion Sort Generator (Yields Execution Beats)
    # -------------------------------------------------------------------------
    def insertion_sort(self) -> Generator[float, None, None]:
        n = len(self.values)
        s = self.stats

        self.update_step_message("Initializing Insertion Sort Engine...")
        self.set_phase("Starting")
        self.highlight_pseudocode_line(1)
        yield 1.0

        # Base Case
        self.mark_sorted(1)
        self.update_step_message(f"Base Invariant Established: Subarray A[0..0] ({self.values[0]}) is sorted.")
        self.setw("eduAction", "Subarray A[0..0] satisfies loop invariant")
        self.record_trace("INIT", 1, {"sorted_count": 1, "action": "Base invariant established"})
        yield 1.0

        for i in range(1, n):
            # 1. SELECT KEY
            s["pass_no"] = i
            key = self.values[i]
            key_bar = self.bars[i]
            s["key"] = key
            s["accesses"] += 1
            self.set_phase("Selecting Key")
            self.highlight_pseudocode_line(2)
            self.highlight_key(key_bar)
            self.gap_index = i
            self.setw("eduKey", key)
            self.setw("eduCompare", "—")
            self.setw("eduAction", f"Extract key A[{i}] = {key}")
            self.update_statistics()
            self.update_progress((i - 1) / max(1, n - 1))
            self.update_step_message(f"Pass {i}: Selected key element A[{i}] = {key}")
            self.record_trace("SELECT_KEY", 2, {"pass": i, "key": key, "index": i})
            yield 1.0

            # 2. COMPARE AND SHIFT
            j = i - 1
            self.highlight_pseudocode_line(3)
            self.set_phase("Comparing")
            while j >= 0:
                self.move_key(key_bar, j + 1)
                compared = self.values[j]
                s["comparisons"] += 1
                s["accesses"] += 1
                self.highlight_pseudocode_line(4)
                self.compare_elements(self.bars[j])
                self.setw("eduCompare", compared)
                self.update_statistics()
                self.update_step_message(f"Comparing key {key} with A[{j}] = {compared}")
                self.record_trace("COMPARE", 4, {"key": key, "compared": compared, "j": j})
                yield 1.0

                if compared > key:
                    self.set_phase("Shifting")
                    self.highlight_pseudocode_line(5)
                    self.setw("eduAction", f"{compared} > {key} → Shift {compared} rightward to slot {j+1}")
                    self.update_step_message(f"Shifting {compared} one slot to the right")
                    self.values[j + 1] = self.values[j]
                    moving = self.bars[j]
                    self.bars[j + 1] = moving
                    self.shift_element(moving, j + 1)
                    self.gap_index = j
                    s["shifts"] += 1
                    s["accesses"] += 2
                    self.div_count = i + 1
                    self.update_statistics()
                    self.record_trace("SHIFT", 5, {"shifted_value": compared, "from": j, "to": j + 1})
                    yield 1.0

                    moving.state = "sorted"
                    j -= 1
                    self.highlight_pseudocode_line(6)
                    self.set_phase("Comparing")
                else:
                    self.bars[j].state = "sorted"
                    self.setw("eduAction", f"{compared} ≤ {key} → Invariant position located at slot {j+1}")
                    self.update_step_message(f"{compared} is not greater than {key}. Target slot found.")
                    self.record_trace("HALT_SHIFT", 4, {"reason": f"{compared} <= {key}"})
                    yield 0.8
                    break

            if j < 0:
                self.setw("eduAction", f"Reached index 0: {key} is minimal in A[0..{i}]")
                self.update_step_message(f"Key {key} reached beginning of array")
                yield 0.6

            # 3. INSERT KEY
            position = j + 1
            self.set_phase("Inserting")
            self.highlight_pseudocode_line(7)
            self.gap_index = position
            key_bar.state = "target"
            self.move_key(key_bar, position)
            if position == i:
                self.setw("eduAction", f"Key {key} remains in position {position} (no displacement)")
                self.update_step_message(f"No shift needed: {key} remains in position {position}")
            else:
                self.setw("eduAction", f"Insert key {key} into target slot {position}")
                self.update_step_message(f"Inserted key {key} at slot {position}")
            yield 0.8

            self.values[position] = key
            self.bars[position] = key_bar
            self.insert_key(key_bar, position)
            s["accesses"] += 1
            self.update_statistics()
            self.record_trace("INSERT", 7, {"key": key, "position": position})
            yield 1.0

            # 4. MARK SORTED EXTENSION
            self.key_bar = None
            self.gap_index = None
            self.mark_sorted(i + 1)
            self.set_phase("Pass Complete")
            self.highlight_pseudocode_line(1)
            self.update_progress(i / max(1, n - 1))
            self.update_step_message(f"Pass {i} complete: Invariant holds for subarray A[0..{i}]")
            self.record_trace("PASS_COMPLETE", 1, {"sorted_size": i + 1})
            yield 0.6

        # Done
        s["key"] = None
        self.set_phase("Completed")
        self.mark_sorted(n)
        self.update_progress(1.0)
        self.highlight_pseudocode_line(1)
        self.update_step_message("Array is completely sorted! Subarray invariant holds for all A[0..n-1].")
        for key in ("eduKey", "eduCompare"):
            self.setw(key, "—")
        self.setw("eduAction", "Full induction achieved. All elements in strictly sorted positions.")
        self.record_trace("COMPLETED", 1, {"final_comparisons": s["comparisons"], "final_shifts": s["shifts"]})

    def record_trace(self, event_type: str, line_no: int, payload: Dict[str, Any]) -> None:
        self.execution_trace.append({
            "step": len(self.execution_trace) + 1,
            "type": event_type,
            "code_line": line_no,
            "comparisons": self.stats.get("comparisons", 0),
            "shifts": self.stats.get("shifts", 0),
            "payload": payload,
            "timestamp_ms": round(self.elapsed_ms(), 2),
        })

    # -------------------------------------------------------------------------
    # Execution Flow Controls
    # -------------------------------------------------------------------------
    def cancel_pending(self) -> None:
        self.run_token += 1
        for attr in ("job", "wave_job"):
            job = getattr(self, attr)
            if job is not None:
                try:
                    self.root.after_cancel(job)
                except tk.TclError:
                    pass
                setattr(self, attr, None)
        if self.gen is not None:
            self.gen.close()
            self.gen = None

    def on_generate(self) -> None:
        if self.state in (SORTING, PAUSED, BENCHMARKING):
            return
        self.cancel_pending()
        self.generate_array()
        self.set_state(IDLE)
        self.setw("stepMessage", "New array generated. Press 'Auto-Run' or 'Step Forward'.")

    def start_sorting(self) -> None:
        if self.state in (SORTING, BENCHMARKING):
            return
        if self.state == PAUSED:
            self.resume_sorting()
            return
        self.cancel_pending()
        if self.state == COMPLETED:
            self.values = list(self.original)
            self.render_array()
        else:
            self.clear_bar_states()
        self.reset_stats_and_panels()
        self.gen = self.insertion_sort()
        self.set_state(SORTING)
        self.start_timer()
        self.schedule(0)

    def step_forward(self) -> None:
        if self.state == SORTING:
            self.pause_sorting()
            return
        if self.gen is None or self.state in (IDLE, COMPLETED):
            self.cancel_pending()
            if self.state == COMPLETED:
                self.values = list(self.original)
                self.render_array()
            else:
                self.clear_bar_states()
            self.reset_stats_and_panels()
            self.gen = self.insertion_sort()
            self.set_state(PAUSED)

        self.start_timer()
        try:
            next(self.gen)
            self.stop_timer()
            self.set_state(PAUSED)
        except StopIteration:
            self.finish_sorting()
        except Exception:
            traceback.print_exc()
            self.stop_timer()
            self.set_state(IDLE)
            self.setw("stepMessage", "Algorithm exception. Press Reset.")

    def schedule(self, delay_ms: int) -> None:
        if self.job is not None:
            self.root.after_cancel(self.job)
        token = self.run_token
        self.job = self.root.after(delay_ms, lambda: self.advance(token))

    def advance(self, token: int) -> None:
        self.job = None
        if token != self.run_token or self.state != SORTING or self.gen is None:
            return
        try:
            beats = next(self.gen)
        except StopIteration:
            self.finish_sorting()
            return
        except Exception:
            traceback.print_exc()
            self.stop_timer()
            self.set_state(IDLE)
            self.setw("stepMessage", "Execution error encountered. Resetting state.")
            return
        self.schedule(int(self.current_delay() * beats))

    def pause_sorting(self) -> None:
        if self.state != SORTING:
            return
        if self.job is not None:
            self.root.after_cancel(self.job)
            self.job = None
        self.stop_timer()
        self.paused_message = self.w["stepMessage"].cget("text")
        self.paused_phase = self.stats["phase"]
        self.set_state(PAUSED)
        self.set_phase("Paused")
        self.setw("stepMessage", "Execution paused. Press 'Resume' to continue or 'Step Forward' to advance one op.")

    def resume_sorting(self) -> None:
        if self.state != PAUSED:
            return
        self.set_state(SORTING)
        phase = getattr(self, "paused_phase", "") or self.stats.get("phase", "Comparing")
        msg = getattr(self, "paused_message", "") or "Resuming execution…"
        self.set_phase(phase)
        self.setw("stepMessage", msg)
        self.start_timer()
        self.schedule(0)

    def reset_sorting(self) -> None:
        self.cancel_pending()
        self.values = list(self.original)
        self.render_array()
        self.reset_stats_and_panels()
        self.set_state(IDLE)
        self.setw("stepMessage", "Array restored to initial state. Press 'Auto-Run' or 'Step Forward'.")

    def finish_sorting(self) -> None:
        self.stop_timer()
        self.gen = None
        if self.values != sorted(self.original):
            print("Warning: Array is not sorted!", file=sys.stderr)
        self.set_state(COMPLETED)
        self.update_statistics()
        self.celebrate(self.run_token, 0)

    # -------------------------------------------------------------------------
    # Celebration Animation
    # -------------------------------------------------------------------------
    def celebrate(self, token: int, index: int) -> None:
        if token != self.run_token or self.state != COMPLETED:
            return
        if index < len(self.bars):
            self.bars[index].flash = 1.0
            wait = max(10, int(260 / max(1, len(self.bars))))
            self.wave_job = self.root.after(wait, lambda: self.celebrate(token, index + 1))
        else:
            self.spawn_confetti()
            self.wave_job = self.root.after(350, lambda: self.show_completion_message(token))

    def spawn_confetti(self) -> None:
        c = self.chart
        palette = list(COLORS.values())
        for _ in range(70):
            size = random.uniform(px(3), px(7))
            piece = dict(
                x=random.uniform(0, self.W),
                y=random.uniform(-px(50), -px(5)),
                vx=random.uniform(-px(50), px(50)),
                vy=random.uniform(px(90), px(220)),
                size=size,
                phase=random.uniform(0, 6.28),
                spin=random.uniform(4, 9),
            )
            piece["id"] = c.create_rectangle(0, 0, 0, 0, fill=random.choice(palette), outline="", tags="confetti")
            self.confetti.append(piece)
        c.tag_raise("confetti")

    def update_confetti(self, dt: float) -> None:
        if not self.confetti:
            return
        alive = []
        for p in self.confetti:
            p["vy"] += px(170) * dt
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["phase"] += p["spin"] * dt
            if p["y"] > self.H + 20:
                self.chart.delete(p["id"])
                continue
            half = max(1.0, p["size"] * abs(math.cos(p["phase"]))) / 2.0
            self.chart.coords(p["id"], p["x"] - half, p["y"] - p["size"], p["x"] + half, p["y"] + p["size"])
            alive.append(p)
        self.confetti = alive

    def show_completion_message(self, token: int) -> None:
        if token != self.run_token or self.state != COMPLETED:
            return
        self.setw("doneComparisons", f"{self.stats['comparisons']:,}")
        self.setw("doneShifts", f"{self.stats['shifts']:,}")
        self.setw("doneAccesses", f"{self.stats['accesses']:,}")
        self.setw("doneTime", "%d ms" % (self.timer_elapsed * 1000))
        preview = ", ".join(str(v) for v in self.values[:16])
        if len(self.values) > 16:
            preview += ", …"
        self.setw("doneArray", f"Final Invariant Array: [{preview}]")
        self.done.place(relx=0.5, rely=0.5, anchor="center")

    def hide_completion(self) -> None:
        if hasattr(self, "done"):
            self.done.place_forget()

    # -------------------------------------------------------------------------
    # Theme & Export Handlers
    # -------------------------------------------------------------------------
    def toggle_theme(self) -> None:
        self.theme_name = "light" if self.theme_name == "dark" else "dark"
        self.apply_theme()
        self.update_portion_lists()
        self.draw_benchmark_chart()
        save_settings({"theme": self.theme_name})

    def export_trace_json(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            initialfile=f"algorithm_execution_trace_{int(time.time())}.json"
        )
        if not path:
            return
        payload = {
            "algorithm": "Insertion Sort",
            "workbench": APP_TITLE,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "input_dimension": len(self.original),
            "distribution": self.current_preset,
            "seed": self.current_seed,
            "initial_array": self.original,
            "final_array": self.values,
            "statistics": self.stats,
            "wall_clock_ms": round(self.elapsed_ms(), 2),
            "step_count": len(self.execution_trace),
            "trace": self.execution_trace,
        }
        try:
            Path(path).write_text(json.dumps(payload, indent=2))
            messagebox.showinfo("Export Successful", f"Execution trace saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not write file:\n{e}")

    def export_benchmark_csv(self) -> None:
        if not self.benchmark_records:
            messagebox.showwarning("No Data", "Please execute the benchmark suite first.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            initialfile=f"benchmark_results_{int(time.time())}.csv"
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Distribution", "N", "Elapsed_Microseconds", "Elapsed_Milliseconds",
                    "Comparisons", "Shifts", "Array_Accesses", "Theoretical_Comparisons", "Growth_Ratio"
                ])
                for r in self.benchmark_records:
                    writer.writerow([
                        r.distribution, r.size, r.elapsed_us, r.elapsed_us / 1000.0,
                        r.comparisons, r.shifts, r.accesses, r.theoretical_comparisons,
                        r.growth_ratio if r.growth_ratio is not None else ""
                    ])
            messagebox.showinfo("Export Successful", f"Benchmark CSV saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not write CSV:\n{e}")

    def export_audit_report(self) -> None:
        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown Document", "*.md"), ("Text File", "*.txt")],
            initialfile=f"algorithm_research_audit_{int(time.time())}.md"
        )
        if not path:
            return
        report = [
            f"# {APP_TITLE} — Research Audit Report",
            f"**Generated:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Environment:** Python {sys.version.split()[0]} | Platform: {sys.platform}",
            "",
            "## 1. Algorithm Specification & Complexity Profile",
            "- **Algorithm:** Insertion Sort (In-Place, Comparison-Based)",
            "- **Loop Invariant:** Subarray `A[0 .. i-1]` contains original elements in strictly sorted order",
            "- **Best-Case Complexity:** O(n) Comparisons, 0 Shifts (Already sorted array)",
            "- **Worst-Case Complexity:** O(n²) Comparisons, n(n-1)/2 Shifts (Reversed array)",
            "- **Average-Case Complexity:** O(n²) Comparisons",
            "- **Spatial Complexity:** O(1) Auxiliary Memory (In-Place)",
            "- **Stability:** Strictly Preserved (Halts when `A[j] <= key`)",
            "",
            "## 2. Interactive Session Summary",
            f"- **Active Distribution:** {self.current_preset}",
            f"- **Array Size (N):** {len(self.values)}",
            f"- **Comparisons Executed:** {self.stats.get('comparisons', 0):,}",
            f"- **Shifts Executed:** {self.stats.get('shifts', 0):,}",
            f"- **Array Accesses:** {self.stats.get('accesses', 0):,}",
            f"- **Wall-Clock Time:** {self.elapsed_ms():.2f} ms",
            f"- **Initial Array:** `{self.original[:20]}`",
            f"- **Final Array:** `{self.values[:20]}`",
            "",
            "## 3. Empirical Benchmark Snapshot",
        ]
        if self.benchmark_records:
            report.append("| Distribution | N | Time (µs) | Comparisons | Shifts | Accesses | Theoretical | Growth |")
            report.append("|---|---|---|---|---|---|---|---|")
            for r in self.benchmark_records:
                report.append(
                    f"| {r.distribution} | {r.size} | {r.elapsed_us:.1f} | {r.comparisons:,} | {r.shifts:,} | {r.accesses:,} | {int(r.theoretical_comparisons):,} | {r.growth_ratio or '—'} |"
                )
        else:
            report.append("*(No empirical benchmark runs recorded during this session)*")
        report.append("")
        report.append("---")
        report.append("*Report generated autonomously by the Algorithm Intelligence Workbench.*")

        try:
            Path(path).write_text("\n".join(report), encoding="utf-8")
            messagebox.showinfo("Report Exported", f"Audit report successfully written to:\n{path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"Could not write audit report:\n{e}")

    # -------------------------------------------------------------------------
    # Key Bindings & Window Lifetime
    # -------------------------------------------------------------------------
    def bind_keys(self) -> None:
        self.root.bind("<space>", lambda e: self.toggle_pause())
        self.root.bind("<Key-s>", lambda e: self.step_forward())
        self.root.bind("<Key-S>", lambda e: self.step_forward())
        self.root.bind("<Key-r>", lambda e: self.reset_sorting())
        self.root.bind("<Key-R>", lambda e: self.reset_sorting())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def toggle_pause(self) -> None:
        if self.state == SORTING:
            self.pause_sorting()
        elif self.state == PAUSED:
            self.resume_sorting()
        elif self.state == IDLE:
            self.start_sorting()

    def on_close(self) -> None:
        self.closing = True
        self.run_token += 1
        for job in (self.job, self.wave_job):
            if job is not None:
                try:
                    self.root.after_cancel(job)
                except tk.TclError:
                    pass
        self.root.destroy()


# =============================================================================
# 6. PROGRAM ENTRY POINT
# =============================================================================

def main() -> None:
    global UI_SCALE
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    root = tk.Tk()
    UI_SCALE = clamp(root.winfo_fpixels("1i") / 96.0, 1.0, 2.2)

    screen_w, screen_h = root.winfo_screenwidth(), root.winfo_screenheight()
    width = min(px(1240), screen_w - 40)
    height = min(px(800), screen_h - 60)
    root.geometry(f"{width}x{height}+{(screen_w - width) // 2}+{max(0, (screen_h - height) // 2 - 20)}")
    root.minsize(min(px(960), width), min(px(580), height))

    VisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
