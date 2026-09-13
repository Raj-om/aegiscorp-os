# Free LLM API Providers & Ecosystem References for AegisCorp OS

AegisCorp OS is architected with a provider-neutral adapter layer (`aegiscorp/agents/llm.py`). While it ships with a zero-dependency offline deterministic simulation engine, you can connect live frontier LLMs at zero cost using free-tier providers.

---

## 🌟 Curated Free LLM API Directories

For up-to-date links to obtain your own free API keys, rate limits, and OpenAI-compatible endpoint URLs:

1. **[awesome-freellm-apis](https://github.com/cloudcommunity/awesome-free-llm-apis)** (Best Overall)
   - 480+ free LLM APIs across 31+ providers.
   - Refreshed daily with model IDs, rate limits, and OpenAI-compatible base URLs.
2. **[awesome-free-llm-apis](https://github.com/free-llm-apis/awesome-free-llm-apis)**
   - Curated list covering GitHub Models, Groq, OpenRouter, NVIDIA NIM, Hugging Face, and Cloudflare Workers AI.
3. **[awesome-free-llm-apis (amardeeplakshkar)](https://github.com/amardeeplakshkar/awesome-free-llm-apis)**
   - Focuses on permanently free APIs with documented SDK compatibility.
4. **Free-LLM**
   - Directory covering free/trial endpoints for Mistral, Together AI, Cerebras, and Fireworks.

> [!CAUTION]
> These repositories provide direct portal links to register for your own free developer keys. Never commit your private API keys or tokens to GitHub or public repositories.

---

## 🚀 Quick Setup with Top Free Providers

AegisCorp OS includes native presets for the fastest free-tier LLM providers. Set your preferred provider in `.env`:

### 1. Groq (Ultra-Fast Inference — Free Tier)
- **Get Key**: [console.groq.com/keys](https://console.groq.com/keys)
- **Models**: `llama-3.3-70b-versatile`, `deepseek-r1-distill-llama-70b`, `mixtral-8x7b-32768`
- **Config in `.env`**:
  ```env
  DEFAULT_LLM_PROVIDER=groq
  GROQ_API_KEY=gsk_your_groq_api_key
  ```

### 2. OpenRouter (Free Frontier Models)
- **Get Key**: [openrouter.ai/keys](https://openrouter.ai/keys)
- **Models**: `meta-llama/llama-3.3-70b-instruct:free`, `google/gemini-2.0-flash-exp:free`, `deepseek/deepseek-chat:free`
- **Config in `.env`**:
  ```env
  DEFAULT_LLM_PROVIDER=openrouter
  OPENROUTER_API_KEY=sk-or-v1-your_openrouter_key
  ```

### 3. GitHub Models (Free GPT-4o, Claude 3.5, Llama 3.3)
- **Get Key**: Use any GitHub Personal Access Token (PAT) with `read:packages` or standard access at [github.com/settings/tokens](https://github.com/settings/tokens).
- **Config in `.env`**:
  ```env
  DEFAULT_LLM_PROVIDER=github_models
  GITHUB_TOKEN=ghp_your_github_token
  ```

### 4. Cerebras (Lightning-Fast Llama 3.1 70B)
- **Get Key**: [cloud.cerebras.ai](https://cloud.cerebras.ai)
- **Config in `.env`**:
  ```env
  DEFAULT_LLM_PROVIDER=cerebras
  CEREBRAS_API_KEY=csk_your_cerebras_key
  ```

### 5. Google Gemini (Generative Language Free Tier)
- **Get Key**: [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
- **Config in `.env`**:
  ```env
  DEFAULT_LLM_PROVIDER=gemini
  GEMINI_API_KEY=AIzaSy_your_gemini_key
  ```

### 6. Local Offline (Ollama — Zero External Calls)
- **Download**: [ollama.com](https://ollama.com) (`ollama run llama3.2`)
- **Config in `.env`**:
  ```env
  DEFAULT_LLM_PROVIDER=ollama
  OLLAMA_BASE_URL=http://localhost:11434
  OLLAMA_MODEL=llama3.2
  ```

---

## 💡 AI Applications & Multi-Agent Architecture Reference

To explore and benchmark multi-agent capabilities, MCP tooling, and RAG architectures that pair with AegisCorp OS:

⭐ **[Shubhamsaboo/awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps)**
- Over 100+ runnable AI applications covering:
  - 🤖 Autonomous AI Agents
  - 👥 Multi-agent collaborative squads
  - 🔌 Model Context Protocol (MCP) servers and tools
  - 📚 Retrieval-Augmented Generation (RAG) pipelines
  - 🎙️ Real-time voice agents
  - 🧠 Agent cognitive skills & prompt engineering patterns
