# Algorithm Intelligence Workbench
### *An Interactive Algorithm Research & Analysis Environment*

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Dependencies](https://img.shields.io/badge/Dependencies-Zero%20External-brightgreen.svg)]()
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

The **Algorithm Intelligence Workbench** is a desktop computational laboratory engineered for algorithmic analysis, step-level mechanical visualization, invariant tracking, and empirical performance benchmarking of comparison-based sorting algorithms, centered on **Insertion Sort**.

Built with pure standard Python (`tkinter`), the workbench requires zero third-party packages or environment setups: open the workspace and execute immediately.

---

## Key Highlights

- **Elite Dark Analytics Visual Identity:** Deep navy (`#172638`) surrounding near-black (`#05090D`) technical work surfaces with high-precision electric turquoise (`#20E6D0`) and cyan highlights, plus an academic light theme.
- **Mission-Control Telemetry Ribbon:** Real-time 8-metric telemetry strip displaying active Comparisons, Shifts, Array Accesses, Wall Time, Pass Progress, Dimension N, Sorted Invariant, and Execution Phase.
- **Synchronized Execution & Pseudocode Highlighting:** Real-time synchronization between the visual canvas, active line in CLRS-style pseudocode, and inductive loop invariants.
- **Granular Execution Engine:**
  - **Auto-Run:** Real-time 60 FPS animation with dynamic speed slider (600 ms down to 20 ms).
  - **Step Forward (Next Op):** Advance execution by exactly one atomic operation (comparison, rightward shift, or key insertion) for classroom demonstration and step-by-step formal analysis.
  - **Pause / Resume / Reset:** Complete non-destructive state persistence.
- **Empirical Benchmark Suite (Non-Animated):** A dedicated headless measurement laboratory measuring exact wall-clock latency (nanoseconds), comparisons, and data shifts across input dimensions ($N = 50$ to $N = 2000+$) and distributions (Random, Sorted Best-Case, Reversed Worst-Case, Nearly Sorted). Includes an interactive empirical scaling canvas and CSV export.
- **Formal Invariant & Complexity Theory:** Built-in interactive ledger detailing the mathematical induction proof of correctness (Initialization, Maintenance, Termination), stability preservation, and $O(1)$ spatial invariants.
- **Reproducibility & Custom Arrays:** Configurable PRNG seeds, five distribution presets, and custom array entry dialog with instant syntax validation.
- **Audit & Telemetry Export:** Export raw execution traces as JSON, benchmark data as CSV, and comprehensive research audit reports as Markdown.

---

## Laboratory Architecture

```
Algorithm Intelligence Workbench
│
├── 1. Algorithm Visualizer & Step Lab
│   ├── Interpolated 60 FPS Canvas with Lifted Floating Key & Target Slot
│   ├── Invariant Subarray Divider (Sorted A[0..i-1] vs Unsorted A[i..n-1])
│   ├── Inversion Counter Telemetry
│   ├── Synchronized CLRS Pseudocode Display
│   ├── 4-Line Chronological Operation History & Fading Narrative
│   └── Real-Time Metrics (Comparisons, Shifts, Array Accesses, Elapsed Time)
│
├── 2. Empirical Benchmark Laboratory
│   ├── Headless Pure Algorithmic Execution Engine
│   ├── Metric Tracking: Latency (µs), Comparisons, Shifts, Memory Reads/Writes
│   ├── Empirical Growth Ratio Calculation (T(2N)/T(N))
│   ├── Real-Time Tabular Results Grid
│   └── Vector Asymptotic Scaling Curves vs O(N) and O(N²) Bounds
│
└── 3. Invariant Proof & Complexity Theory
    ├── Mathematical Proof of Correctness (Initialization, Maintenance, Termination)
    ├── Stability Invariant Preservation Proof
    ├── Spatial Memory Bounds Proof
    └── Research Audit Report Generator
```

---

## Quickstart

### Prerequisites

Python 3.8 or newer with standard `tkinter` support (included by default in official python.org installers for Windows and macOS).

*On Linux (Debian/Ubuntu):*
```bash
sudo apt install python3-tk
```

*On Linux (Fedora):*
```bash
sudo dnf install python3-tkinter
```

### Launching the Workbench

Execute either entry point:

```bash
# Master Workbench Entry Point
python algorithm_workbench.py

# Seamless Backward-Compatible Visualizer Entry Point
python insertion_sort_visualizer.py
```

### Running Automated Verification Suite

Run the unit test suite verifying theoretical bounds, algorithm stability, edge cases, and distribution generators:

```bash
python test_algorithm_workbench.py
```

---

## Interactive Controls & Shortcuts

| Action | Control / Key | Description |
|---|---|---|
| **Auto-Run** | Button / <kbd>Space</kbd> | Starts continuous animated sorting at selected speed |
| **Step Forward** | Button / <kbd>S</kbd> | Advances execution by exactly one atomic operation |
| **Pause / Resume** | Button / <kbd>Space</kbd> | Toggles pause state without losing current generator context |
| **Reset** | Button / <kbd>R</kbd> | Restores original untouched array and resets all telemetry |
| **Generate** | Button | Generates a new array according to active distribution preset |
| **Theme Toggle** | Button | Switches between Obsidian Dark and Studio Light modes |
| **Custom Array** | Button | Opens modal to input arbitrary comma-separated integers |
| **PRNG Seed** | Entry + Apply | Sets deterministic seed for scientific reproducibility |

---

## The Insertion Sort Invariant & Theory

### CLRS Invariant Formulation
> **Loop Invariant:** At the start of each iteration of the outer loop (index $i$), the subarray $A[0 .. i-1]$ consists of the elements originally in $A[0 .. i-1]$, but in strictly sorted order.

1. **Initialization (Base Case):**
   Prior to the first iteration ($i = 1$), the subarray contains only $A[0]$, which is trivially sorted.
2. **Maintenance (Inductive Step):**
   The inner `while` loop shifts elements $A[j] > key$ one position rightward, maintaining sorted order and opening slot $j + 1$. Dropping $key$ into slot $j + 1$ extends the sorted subarray to $A[0 .. i]$.
3. **Termination:**
   The outer loop terminates when $i = n$. By substitution into the invariant, subarray $A[0 .. n-1]$ contains all original elements in sorted order.

### Complexity Matrix

| Metric | Best Case (Sorted) | Average Case (Random) | Worst Case (Reversed) |
|---|---|---|---|
| **Comparisons** | $n - 1$ | $\approx \frac{n(n - 1)}{4}$ | $\frac{n(n - 1)}{2}$ |
| **Shifts (Writes)** | $0$ | $\approx \frac{n(n - 1)}{4}$ | $\frac{n(n - 1)}{2}$ |
| **Time Complexity** | $O(n)$ | $O(n^2)$ | $O(n^2)$ |
| **Auxiliary Space** | $O(1)$ (In-Place) | $O(1)$ (In-Place) | $O(1)$ (In-Place) |
| **Stability** | Stable | Stable | Stable |

---

## Export Formats

1. **Execution Trace (`.json`):** Comprehensive step-by-step audit record including operation type, active pseudocode line, timestamps, and live array snapshots.
2. **Benchmark Results (`.csv`):** Tabular export containing distribution, dimension ($N$), execution latency, comparisons, shifts, and asymptotic growth ratios.
3. **Research Audit Report (`.md`):** Formatted Markdown document summarizing session parameters, theoretical proofs, and empirical performance metrics.

---

## License

MIT License. Open source and free for educational, research, and production use.
