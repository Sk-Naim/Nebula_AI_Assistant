# Nebula AI - Kaggle Capstone Project 🚀

> **A real-time, cross-platform voice AI assistant that sees, hears, understands, and controls your computer.**

Welcome to the **Nebula AI** repository, submitted as part of the **Kaggle 5-Day AI Agents Intensive** capstone project. This project fits into the **Concierge Agents** and **Freestyle Track**, acting as an autonomous personal assistant that bridges the gap between natural human intent and complex operating system tasks.

---

## 🌟 Overview & Working Principle

Nebula AI operates on a **continuous observation-action loop**. It acts as a bridge between the physical world (via camera and microphone), the digital operating system, and a Large Language Model (Google Gemini API).

**The Working Principle:**
1. **Perception**: The agent actively listens to your voice commands and can "see" your screen and physical environment through the camera in real-time.
2. **Cognition**: Using the Gemini API, it processes multimodal inputs (audio transcripts, screenshots, dragged-and-dropped files). The reasoning engine parses intent and formulates a plan.
3. **Execution**: The agent converts its plan into discrete tool calls (Action Handlers). It can simulate keyboard typing, execute terminal commands, browse the web via Playwright, or manipulate local files.
4. **Memory**: Short-term conversation history and long-term user preferences are retained, allowing the agent to continuously learn and adapt to your workflow over time.

---

## ✨ Comprehensive Features

- **🎙️ Real-Time Voice Interaction**: Speak naturally in any language with ultra-low latency voice-to-text and text-to-speech pipelines.
- **👁️ Visual Awareness**: Real-time screen processing allows the agent to "see" your workspace, acting on visual context, UI elements, and even webcam feeds.
- **🤖 Autonomous Task Execution**: High-level planning for multi-step goals. The agent can browse the web using Playwright, manipulate files, and execute terminal commands without human intervention.
- **🧠 Persistent Memory**: Retains deep context of your ongoing projects, coding preferences, and personal workflows across sessions.
- **🎨 Adaptive UI HUD**: A responsive, semi-transparent heads-up display (HUD) that blends seamlessly with your desktop environment, mimicking native OS integrations.
- **⌨️ Hybrid Input**: Switch smoothly between typing text commands in the terminal and speaking out loud.
- **📂 Document & File Handling**: Drag and drop PDFs, source code, or images directly into the assistant interface for instant summarization, analysis, or editing.
- **🌐 Cross-Platform Capability**: Architected to run cleanly on macOS, Windows, and Linux.

---

## 🏗️ Architecture Breakdown

Nebula AI is engineered for total autonomy with a modular, highly decoupled architecture:

1. **Core Engine (`/core`)**: Manages the main event loop, connecting inputs to the Gemini API. It handles token limits, prompting, and routes logic to action handlers.
2. **Action Handlers (`/actions`)**: A suite of tools the agent can invoke to interact with the system. This includes OS-level bash commands, Python scripting, and opening local applications.
3. **Agent Logic (`/agent`)**: The decision-making layer that breaks down complex user prompts into executable tool calls and multi-step plans.
4. **Memory Module (`/memory`)**: Handles storing context in localized JSON databases to persist memory securely on your own device.
5. **Web Automation**: Uses Playwright to autonomously navigate the web, scrape information, read documentation, and interact with complex web applications on behalf of the user.
6. **UI Layer (`ui.py`)**: Built with PyQt6, providing a highly customizable and resizable cross-platform overlay interface.

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
Developed for the **Kaggle 5-Day AI Agents Intensive**. Nebula AI demonstrates the real-world usefulness of autonomous agents by serving as an advanced personal assistant that goes beyond simple chatbots, actively manipulating the desktop environment to complete real work safely and efficiently.

---
*Developed and Engineered by **Sk Naim**.*
