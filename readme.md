# 🤖 AI Sales Agent (WhatsApp)

A production-ready AI Sales Assistant built with **FastAPI**, **LangChain**, and **Llama 3 (via Groq)**. This agent is designed to qualify leads, manage conversation state, and handle real-time WhatsApp webhooks.

![Status](https://img.shields.io/badge/Status-Development-green) ![Python](https://img.shields.io/badge/Python-3.10-blue) ![AI](https://img.shields.io/badge/Model-Llama3--70B-orange)

## 🚀 Features

* **Automated Conversations:** Handles inbound messages from WhatsApp/Messenger 24/7.
* **Natural Language Processing:** Uses LLMs to understand customer intent and context.
* **Lead Qualification:** Ask specific questions to determine if a user is a potential buyer.
* **FastAPI Webhook:** High-performance, asynchronous server to receive real-time updates from Meta.

## 🛠️ Tech Stack

* **Language:** Python 3.10
* **Framework:** FastAPI
* **Server:** Uvicorn
* **Environment Management:** Miniconda
* **APIs:** Meta Graph API (WhatsApp/Messenger), OpenAI / Groq

## 📦 Installation & Setup

### 1. Prerequisites
Before you begin, ensure you have **Miniconda** installed.
* Download and install it from [here](https://docs.anaconda.com/free/miniconda/#quick-command-line-install).

### 2. Clone the Repository
Download the project code and enter the directory:

```bash
git clone <your-repo-url>
cd <your-project-folder>