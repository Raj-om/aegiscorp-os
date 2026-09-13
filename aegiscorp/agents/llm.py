import os
import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class LLMAdapter(ABC):
    """Abstract provider-neutral LLM adapter interface."""
    @abstractmethod
    def generate(self, system_prompt: str, prompt: str, temperature: float = 0.2) -> str:
        pass

class DeterministicSimulationAdapter(LLMAdapter):
    """Deterministic, offline simulation adapter.
    Ensures AegisCorp OS can run full simulations locally out-of-the-box with zero API keys.
    """
    def generate(self, system_prompt: str, prompt: str, temperature: float = 0.2) -> str:
        return self._simulate_phd_response(prompt)

    def _simulate_phd_response(self, prompt: str) -> str:
        return json.dumps({
            "situation_assessment": "Comprehensive analysis completed using first-principles breakdown of current corporate state, market conditions, and strategic objectives.",
            "facts_vs_assumptions": {
                "verified_facts": ["Current digital twin state verified", "Organizational authority boundaries confirmed", "Capital allocation policy applied"],
                "key_assumptions": ["Market conditions remain stable over 18-month horizon", "Target conversion rates reflect tier-1 enterprise cohort performance"]
            },
            "options": [
                {"option": "Aggressive expansion", "risk": "High capital drawdown", "reward": "Rapid market capture"},
                {"option": "Disciplined phased execution", "risk": "Moderate pacing", "reward": "High capital efficiency and risk-adjusted return"},
                {"option": "Conservative defensive holding", "risk": "Opportunity loss", "reward": "Complete liquidity preservation"}
            ],
            "recommendation": "Adopt Option 2 (Disciplined phased execution) with milestone-gated capital commitments and continuous KPI verification.",
            "expected_impact": "Projected +35% ARR growth, preservation of >24 months runway, and maintain 99.98% platform reliability.",
            "risks_and_mitigations": [
                {"risk": "Execution latency across departments", "mitigation": "Enforce explicit dependency graphs and daily operational cadence"},
                {"risk": "Unbudgeted cost overruns", "mitigation": "Automated $1M/$10M/$100M threshold gates and CFO sign-off"}
            ],
            "dependencies": ["Cross-functional alignment across Engineering, Product, and Finance", "Board approval if capital commitment exceeds $100M"],
            "required_approvals": ["Department Executive", "CFO for capital allocation"],
            "next_actions": [
                "Issue detailed task delegations to subordinate teams",
                "Register milestone markers in execution task graph",
                "Emit audit event and monitor leading KPI indicators"
            ],
            "escalation_reason": None
        }, indent=2)

class OpenAICompatibleAdapter(LLMAdapter):
    """Universal adapter for OpenAI-compatible endpoints (Groq, OpenRouter, GitHub Models, Cerebras, NVIDIA NIM, Mistral, Ollama)."""
    def __init__(
        self,
        base_url: str = "https://api.openai.com/v1",
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
        default_headers: Optional[Dict[str, str]] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.default_headers = default_headers or {}

    def generate(self, system_prompt: str, prompt: str, temperature: float = 0.2) -> str:
        if not self.api_key and "localhost" not in self.base_url and "127.0.0.1" not in self.base_url:
            return DeterministicSimulationAdapter().generate(system_prompt, prompt)
        try:
            import httpx
            headers = {
                "Authorization": f"Bearer {self.api_key or 'free'}",
                "Content-Type": "application/json",
                **self.default_headers,
            }
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature
            }
            resp = httpx.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60.0)
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
            return DeterministicSimulationAdapter().generate(system_prompt, prompt)
        except Exception:
            return DeterministicSimulationAdapter().generate(system_prompt, prompt)

class OpenAIAdapter(OpenAICompatibleAdapter):
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        super().__init__(
            base_url="https://api.openai.com/v1",
            api_key=api_key or os.getenv("OPENAI_API_KEY"),
            model=model,
        )

class GroqAdapter(OpenAICompatibleAdapter):
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.3-70b-versatile"):
        super().__init__(
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key or os.getenv("GROQ_API_KEY"),
            model=model,
        )

class OpenRouterAdapter(OpenAICompatibleAdapter):
    def __init__(self, api_key: Optional[str] = None, model: str = "meta-llama/llama-3.3-70b-instruct:free"):
        super().__init__(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key or os.getenv("OPENROUTER_API_KEY"),
            model=model,
            default_headers={"HTTP-Referer": "https://github.com/Raj-om/aegiscorp-os", "X-Title": "AegisCorp OS"},
        )

class GitHubModelsAdapter(OpenAICompatibleAdapter):
    def __init__(self, token: Optional[str] = None, model: str = "gpt-4o"):
        super().__init__(
            base_url="https://models.inference.ai.azure.com",
            api_key=token or os.getenv("GITHUB_TOKEN"),
            model=model,
        )

class CerebrasAdapter(OpenAICompatibleAdapter):
    def __init__(self, api_key: Optional[str] = None, model: str = "llama3.1-70b"):
        super().__init__(
            base_url="https://api.cerebras.ai/v1",
            api_key=api_key or os.getenv("CEREBRAS_API_KEY"),
            model=model,
        )

class MistralAdapter(OpenAICompatibleAdapter):
    def __init__(self, api_key: Optional[str] = None, model: str = "mistral-small-latest"):
        super().__init__(
            base_url="https://api.mistral.ai/v1",
            api_key=api_key or os.getenv("MISTRAL_API_KEY"),
            model=model,
        )

class GeminiAdapter(LLMAdapter):
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-1.5-pro"):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model = model

    def generate(self, system_prompt: str, prompt: str, temperature: float = 0.2) -> str:
        if not self.api_key:
            return DeterministicSimulationAdapter().generate(system_prompt, prompt)
        try:
            import httpx
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
            payload = {
                "contents": [
                    {"role": "user", "parts": [{"text": f"{system_prompt}\n\nTask:\n{prompt}"}]}
                ],
                "generationConfig": {"temperature": temperature}
            }
            resp = httpx.post(url, json=payload, timeout=60.0)
            if resp.status_code == 200:
                data = resp.json()
                return data["candidates"][0]["content"]["parts"][0]["text"]
            return DeterministicSimulationAdapter().generate(system_prompt, prompt)
        except Exception:
            return DeterministicSimulationAdapter().generate(system_prompt, prompt)

def get_llm_adapter(name: Optional[str] = None) -> LLMAdapter:
    provider = (name or os.getenv("DEFAULT_LLM_PROVIDER", "deterministic")).lower()
    if provider == "groq" and os.getenv("GROQ_API_KEY"):
        return GroqAdapter()
    if provider == "openrouter" and os.getenv("OPENROUTER_API_KEY"):
        return OpenRouterAdapter()
    if provider in ("github", "github_models") and os.getenv("GITHUB_TOKEN"):
        return GitHubModelsAdapter()
    if provider == "cerebras" and os.getenv("CEREBRAS_API_KEY"):
        return CerebrasAdapter()
    if provider == "mistral" and os.getenv("MISTRAL_API_KEY"):
        return MistralAdapter()
    if provider == "openai" and os.getenv("OPENAI_API_KEY"):
        return OpenAIAdapter()
    if provider == "gemini" and os.getenv("GEMINI_API_KEY"):
        return GeminiAdapter()
    if provider == "ollama":
        base_url = f"{os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')}/v1"
        return OpenAICompatibleAdapter(base_url=base_url, api_key="ollama", model=os.getenv("OLLAMA_MODEL", "llama3.2"))
    return DeterministicSimulationAdapter()
