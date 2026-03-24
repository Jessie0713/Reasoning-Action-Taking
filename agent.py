# agent.py
import os
import re
import requests
from typing import Optional

from tools import SearchTool


class ReActAgent:
    def __init__(self, model: str = "gpt-4o-mini", max_steps: int = 5):
        self.model = model
        self.max_steps = max_steps
        self.search_tool = SearchTool()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        if not self.openai_api_key:
            raise ValueError("Missing OPENAI_API_KEY in environment variables.")

        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        return """
You are a general-purpose ReAct agent.

You must solve user questions using this format:

Thought: think about what to do next
Action: Search[search query]
Observation: result from the tool
... (repeat as needed)
Final Answer: the final answer to the user

Rules:
1. The only allowed tool action is:
   Action: Search[query]
2. Never invent an Observation.
3. After producing an Action, stop. The environment will execute it and return an Observation.
4. If the search result is poor, empty, or irrelevant, reflect and try a better search query.
5. Break multi-step problems into smaller parts.
6. If you already have enough facts or numbers, DO NOT output another action.
7. If you already have enough facts or numbers, directly output:
   Final Answer: ...
8. Never output actions like Calculate, Compute, Lookup, or anything except Search[...].

Example:
User: What fraction of Germany's population is France's population?
Thought: I should first find Germany's population.
Action: Search[Germany current population]

Observation: Germany population is about 84 million.

Thought: Now I need France's population.
Action: Search[France current population]

Observation: France population is about 68 million.

Thought: I now have both numbers, so I can compute the fraction directly.
Final Answer: France's population is about 68/84 ≈ 0.81, or about 81% of Germany's population.
"""

    def _call_llm(self, messages) -> str:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "stop": ["Observation:"]
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    def _parse_action(self, text: str) -> Optional[str]:
        match = re.search(r"Action:\s*Search\[(.*?)\]", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _parse_final_answer(self, text: str) -> Optional[str]:
        match = re.search(r"Final Answer:\s*(.*)", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def execute(self, query: str) -> str:
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": query}
        ]

        print("=" * 80)
        print(f"USER QUESTION: {query}")
        print("=" * 80)

        for step in range(1, self.max_steps + 1):
            print(f"\n--- Step {step} ---")

            try:
                llm_output = self._call_llm(messages)
            except Exception as e:
                error_msg = f"LLM API error: {str(e)}"
                print(error_msg)
                return error_msg

            print(llm_output)
            messages.append({"role": "assistant", "content": llm_output})

            final_answer = self._parse_final_answer(llm_output)
            if final_answer:
                return final_answer

            action_query = self._parse_action(llm_output)
            if action_query:
                observation = self.search_tool.search(action_query)
                observation_text = f"Observation: {observation}"
                print(observation_text)
                messages.append({"role": "user", "content": observation_text})
            else:
                fail_msg = "No valid Action or Final Answer found. Stopping."
                print(fail_msg)
                return fail_msg

        return "Reached max steps without final answer."