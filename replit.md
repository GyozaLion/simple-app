# Logic Gate Signal Visualizer

## Overview

This is an interactive educational web application built with Streamlit that visualizes the behavior of three-input logic gates. The application allows users to configure input signal patterns and frequencies, then observe how different logic gates (AND, OR, NAND, NOR, XOR) process these signals in real-time. The visualization helps users understand digital logic concepts through dynamic signal waveform displays.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture

**Technology Choice: Streamlit**
- **Rationale**: Streamlit was chosen for its rapid prototyping capabilities and built-in interactive widgets, eliminating the need for separate frontend/backend development
- **Pros**: Zero HTML/CSS/JS required, automatic UI generation, hot-reloading for development
- **Cons**: Limited customization compared to traditional web frameworks, locked into Streamlit's layout system

**Layout Pattern: Sidebar + Main Content**
- Sidebar contains all user input controls (signal configuration, gate type selection)
- Main content area displays the generated signal visualizations
- Wide layout mode (`layout="wide"`) maximizes visualization space

### Signal Processing Architecture

**Signal Generation Approach: NumPy Array-based**
- Signals represented as discrete-time arrays using NumPy
- Time domain sampled at regular intervals over configurable duration
- Pattern generation functions create different signal types:
  - Clock Pulse: Periodic square wave using sinusoidal zero-crossing
  - Constant High/Low: Static signal states
  - Half Duration High: Step function at midpoint

**Logic Gate Implementation**
- Pure functional approach using NumPy logical operations
- Three-input gates implemented by chaining binary operations
- Direct boolean-to-float conversion for visualization compatibility
- Supported gates: AND, OR, NAND, NOR, XOR (incomplete in current codebase)

### Visualization Architecture

**Library: Matplotlib**
- **Rationale**: Industry-standard plotting library with extensive signal visualization capabilities
- **Integration**: Plots rendered in-memory and displayed via Streamlit
- **Alternatives Considered**: Plotly (more interactive but heavier), Altair (declarative but less flexible)

**Rendering Strategy**
- Static matplotlib figures generated on-demand based on user input
- Streamlit handles display refresh when configuration changes
- No client-side visualization state management required

### Application State Management

**Approach: Streamlit Session State (Implicit)**
- Widget values automatically managed by Streamlit
- No explicit session state required for current functionality
- Reactive programming model: UI changes trigger full script re-execution
- Signal regeneration on every parameter change (acceptable for small datasets)

## External Dependencies

### Core Libraries

**Streamlit (Web Framework)**
- Purpose: Application framework and UI rendering
- Provides: Web server, widget system, layout management, auto-refresh

**NumPy (Numerical Computing)**
- Purpose: Signal array generation and logical operations
- Provides: Efficient array operations, mathematical functions, boolean logic

**Matplotlib (Visualization)**
- Purpose: Signal waveform plotting
- Provides: 2D plotting, figure management, customization options

### Development Tools

**Python 3.x Runtime**
- Required for all dependencies
- No specific version constraints identified in current codebase

### Notable Absences

- No database integration (application is stateless)
- No external API calls
- No authentication/authorization system
- No persistent data storage
- No third-party cloud services

### Asset Dependencies

**Attached Assets**
- Contains reference Python code for signal visualization patterns
- Appears to be documentation/example code rather than runtime dependency
- Shows original implementation concepts using matplotlib subplots