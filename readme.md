# Nebula AI - Kaggle Capstone Project 🚀

> **A real-time, cross-platform voice AI assistant that sees, hears, understands, and actively controls your digital life.**

Welcome to the **Nebula AI** repository, submitted as part of the **Kaggle 5-Day AI Agents Intensive** capstone project. This project is a highly capable **Concierge Agent**, acting as an autonomous personal assistant that bridges the gap between natural human intent and complex real-world task execution.

---

## 🌟 Overview & Capabilities

Nebula AI is designed to be the ultimate personal concierge. It is capable of much more than just answering questions—it is built to *take action*. 

### ✨ Highlight Features:
- **🍔 Automated Food Ordering:** Feeling hungry? Just tell Nebula AI, and it will autonomously navigate to Swiggy using Playwright to order your favorite meals.
- **✈️ Flight Booking:** Tell it your destination and dates, and the agent will browse the web to find and book flight tickets for you.
- **📅 Daily Routine Generation:** It can intelligently design, organize, and manage your daily schedule and routines based on your preferences.
- **🧠 Absolute Memory:** Nebula AI remembers everything you tell it. It retains context about your life, your ongoing projects, and your specific tastes across multiple sessions.
- **💻 Autonomous Coder:** Ask it to write code, debug issues, or architect software. It can generate clean, functional code right in front of your eyes.
- **🌍 Multi-Lingual Voice Interactions:** Speak naturally in almost any language. The agent understands you instantly and replies with ultra-low latency text-to-speech.
- **👁️ Object & Environment Scanning:** Hold any object up to your webcam, and Nebula AI will instantly scan it, recognize it, and tell you exactly what you are holding.
- **🎵 Music & Entertainment:** Ask the agent to play your favorite songs or videos, and it will handle the web navigation and playback for you.

---

## 🏗️ Architecture & Agent Workflow

Nebula AI is engineered for total autonomy, heavily relying on the **Google Gemini** multimodal models as its core brain.

### The Agentic Workflow
The system operates on an advanced **Observe-Plan-Act** workflow, designed to handle multi-step reasoning:

1. **Perception (Observation):** The agent continuously takes in multimodal inputs. This includes real-time audio transcripts from your voice, screenshots of your current desktop, physical environment data from the webcam, and dropped files.
2. **Cognition (Planning):** The core Gemini-powered planner evaluates the request against current observations. It breaks complex tasks (e.g., "Book a flight to Tokyo") into sequential, logical steps. 
3. **Execution (Action):** The agent delegates sub-tasks to specialized **Action Handlers**. It executes Python scripts, runs terminal commands, or launches browser sessions using Playwright to interact with dynamic web applications.
4. **Validation (Feedback Loop):** After taking an action, the agent re-observes the screen or terminal output to ensure the action succeeded before moving to the next step.

### System Modules
- **Agent Core (`/agent`)**: The central decision-making hub that handles the planning logic, error recovery, and task queuing.
- **Memory Module (`/memory`)**: Features a localized persistent memory database. It constantly updates a "Long-Term" state profile about the user, allowing the agent to reference past conversations or preferences securely without leaking data.
- **Action Suite (`/actions`)**: A robust library of tools including computer control, web search, UI interaction, code execution, and autonomous web browsing.
- **Adaptive UI (`ui.py`)**: A responsive, semi-transparent heads-up display built with PyQt6 that blends seamlessly into the user's OS workspace.

---

## 🛠️ Installation & Quick Start

```bash
# Clone the repository
git clone https://github.com/Sk-Naim/Nebula_AI_Assistant.git
cd Kaggle-Capstone-Project

# Install dependencies
pip install -r requirements.txt
playwright install

# Run the agent
python main.py
```

*Note: Requires a free Gemini API Key. Set your key securely in `config/api_keys.json` before running.*

---

## 🎯 Capstone Project Context
Developed for the **Kaggle 5-Day AI Agents Intensive**. Nebula AI demonstrates the real-world usefulness of autonomous agents by serving as an advanced personal assistant that goes beyond simple chatbots, actively manipulating the desktop environment and web browsers to complete real work safely and efficiently.

---
*Developed and Engineered by **Sk Naim**.*
