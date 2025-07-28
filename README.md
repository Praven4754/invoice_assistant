# 🚀 Invoice Assistant System using LangGraph
This project leverages [LangGraph](https://github.com/langchain-ai/langgraph), [LangChain](https://www.langchain.com/), and OpenAI models to create an intelligent toolchain with document generation, memory, messaging, and email functionality — all wrapped in a user-friendly [Gradio](https://gradio.app/) interface.


## 📦 Requirements

This project uses `uv` as the package manager.

### 🔧 Prerequisites

* uv installed - Install uv with standalone installer:
* macOS and Linux:
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh:
  ```

  Windows:
  ```bash
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```


## 🔌 Installation

1. **Clone the repository**

2. **Install dependencies:**

   ```bash
   uv sync
   ```

3. **Set up your environment variables:**

   Create a `.env` file in the same directory as the app.py:

   ```env
   GOOGLE_API_KEY = <your_google_api_key>
   SENDGRID_API_KEY = <your_sendgrid_api_key>
   FROM_EMAIL = <your_verified_mail_for_sendgrid>
   TO_EMAIL = <any_email>
   ```
   Note: FROM_EMAIL should be the one you verified in the Sendgrid with your API


## 📂 Project Structure

```
.
├── app.py                   # Main entry point
├── llm.py                   # LLM setup (e.g., ChatOpenAI or tool integrations)
├── tools.py                 # Any custom tools (e.g., docx generation, email)
├── state.py
├── nodes.py
├── timesheet_<month>.xlsx
├── invoice_<month>.docx     # Will be auto gnerated
├── .env                     # API keys (not tracked by Git)
├── requirements.txt
└── README.md
```

## 🚀 Running the App

Once dependencies are installed and `.env` is configured:

```bash
uv run app.py
```

This will launch your application using `uv`’s virtual environment.



## 📘 Notes

* This project uses:

  * `LangGraph` for stateful graph execution
  * `LangChain` for LLM interactions
  * `Gradio` for UI
  * `python-docx` for generating Word documents
  * `SendGrid` for sending emails

* Additional tools and modules are modularized (e.g., in `llm.py`, etc.) for better scalability.

---

## 🧪 Development & Debugging

* If adding new packages, use:

  ```bash
  uv pip install <package-name>
  ```

  Then regenerate `requirements.txt`:

  ```bash
  uv pip freeze > requirements.txt
  ```

