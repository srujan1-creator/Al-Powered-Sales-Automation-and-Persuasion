# Aura - AI-Powered Sales Automation & Persuasion

Aura is a high-performance, dynamic AI Sales Representative designed for the **Google Prompt Wars** challenge. It simulates a sophisticated B2B sales conversation for an "Enterprise AI Productivity Suite."

## 🎯 Chosen Vertical
**B2B Enterprise SaaS Sales Assistant**

## 💡 Approach and Logic
Aura is built on a multi-layered AI architecture designed to maximize conversion probability through intelligent interaction:

1.  **Context-Aware Initialization**: Unlike static chatbots, Aura begins by capturing organizational context (size, industry, pain points). This context is injected into the AI's "system instructions" to ensure every pitch is tailored to the lead's specific business environment.
2.  **Dynamic Persuasion Engine**: Aura uses the **Gemini 2.0 Flash** model integrated with **Google Search Grounding**. This allows the assistant to pull real-time industry trends and competitor data into the conversation, providing a "Sales Engineer" level of technical depth.
3.  **SPIN Selling Framework**: The AI is prompted to subtly follow the SPIN (Situation, Problem, Implication, Need-payoff) framework, moving from identifying challenges to demonstrating value.
4.  **Real-Time Lead Scoring**: Every message from the user is analyzed by a secondary AI process that calculates a "Lead Score" (0-100). This score is persisted in the database and determines the level of "persuasion intensity" applied in subsequent responses.

## 🚀 How the Solution Works
-   **Frontend**: A premium, accessible React interface with glassmorphism design. It communicates with the backend via an authenticated REST API.
-   **Backend**: A robust FastAPI application that manages conversation state, persists messages in SQLite, and handles the orchestration between the user and the Gemini AI.
-   **Security**: Implementation of `X-API-Key` headers for all requests and GZip compression for high-speed delivery.
-   **Accessibility**: Fully compliant with ARIA standards, keyboard-navigable, and optimized for screen readers.

## 🛠️ Google Services Integration
Aura deeply integrates Google's latest technologies:
-   **Google Gemini 2.0 Flash**: Powers the core reasoning and chat capabilities.
-   **Google Search Grounding**: Enables Aura to verify facts and fetch real-time market trends during a sale.
-   **Google Fonts**: Uses 'Inter' and 'Outfit' for a high-end, professional typography system.

## 📝 Assumptions Made
-   **Demo Focus**: The lead score is an analytical estimation based on sentiment and conversion signals in the text history.
-   **Environment**: The system assumes a `.env` file is present with a valid `GEMINI_API_KEY`.
-   **Database**: SQLite is utilized to maintain a zero-configuration footprint and ensure the total project size remains well under 10MB.

## 🔧 Setup & Submission
-   **Tests**: A unified test runner is provided (`.\run_tests.ps1`) to verify both Backend and Frontend integrity.
-   **Single Branch**: All code is maintained on the `main` branch for straightforward submission.

---
**Developed for the Google Prompt Wars Challenge.**
