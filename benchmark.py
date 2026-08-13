"""
benchmark.py — DeepEval RAG Evaluation & RBAC Security Testing.
Judge: Groq SDK (llama-3.3-70b-versatile) with native JSON mode.
"""
from __future__ import annotations
import json
from pathlib import Path

from groq import Groq, AsyncGroq
from deepeval import evaluate
from deepeval.evaluate.configs import AsyncConfig
from deepeval.metrics import (
    AnswerRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
    FaithfulnessMetric,
)
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase

from src.config import GROQ_API_KEY
from src.rag_engine import query_rag_chain_with_sources

JUDGE_MODEL  = "openai/gpt-oss-120b"
QA_JSON_PATH = Path(__file__).resolve().parent / "QA.json"


class GroqEvalLLM(DeepEvalBaseLLM):
    """DeepEval judge using the official Groq SDK with native JSON mode."""

    def __init__(self, model_name: str = JUDGE_MODEL):
        self.model_name = model_name
        self._client = Groq(api_key=GROQ_API_KEY)
        self._async_client = AsyncGroq(api_key=GROQ_API_KEY)

    def load_model(self):
        return self._client

    def get_model_name(self) -> str:
        return self.model_name

    def generate(self, prompt: str) -> str:
        res = self._client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0,
        )
        return res.choices[0].message.content or "{}"

    async def a_generate(self, prompt: str) -> str:
        res = await self._async_client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0,
        )
        return res.choices[0].message.content or "{}"


def load_qa_dataset() -> list[dict]:
    path = QA_JSON_PATH if QA_JSON_PATH.exists() else Path(__file__).resolve().parent / "data" / "QA.json"
    if not path.exists():
        raise FileNotFoundError(f"QA dataset not found at {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_benchmark(num_questions: int = 50, test_isolation: bool = True):
    qa_data    = load_qa_dataset()
    eval_items = qa_data[:num_questions]

    judge = GroqEvalLLM()

    faithfulness_metric = FaithfulnessMetric(model=judge, threshold=0.5, verbose_mode=False)
    relevancy_metric    = AnswerRelevancyMetric(model=judge, threshold=0.5, verbose_mode=False)
    precision_metric    = ContextualPrecisionMetric(model=judge, threshold=0.5, verbose_mode=False)
    recall_metric       = ContextualRecallMetric(model=judge, threshold=0.5, verbose_mode=False)

    all_test_cases:    list[LLMTestCase] = []
    isolation_results: list[dict]        = []

    for idx, item in enumerate(eval_items, 1):
        question        = item["question"]
        expected_output = item.get("expected_output", "")
        role            = item.get("target_role", "admin")
        source_doc      = item.get("source_doc", "")

        # ── 1. Authorized RAG query ───────────────────────────────────────────
        res            = query_rag_chain_with_sources(question=question, user_role=role, k=3)
        actual_output  = res["answer"]
        context_chunks = [doc.page_content for doc in res["docs"]]

        print(f"[{idx}/{len(eval_items)}] ✅ Authorized [{role}] Q: {question[:50]}...")

        all_test_cases.append(LLMTestCase(
            input=question,
            actual_output=actual_output,
            expected_output=expected_output,
            retrieval_context=context_chunks,
        ))

        # ── 2. RBAC Security / Isolation Test ─────────────────────────────────
        if test_isolation and role != "employee":
            unauth_res  = query_rag_chain_with_sources(question=question, user_role="employee", k=3)
            doc_leaked  = any(source_doc in d.metadata.get("source", "") for d in unauth_res["docs"]) if source_doc else False
            isolation_results.append({"question": question, "passed": not doc_leaked})

    # ── 3. DeepEval evaluation (3 parallel test cases) ────────────────────────
    evaluate(
        test_cases=all_test_cases,
        metrics=[faithfulness_metric, relevancy_metric, precision_metric, recall_metric],
        async_config=AsyncConfig(
            throttle_value=1,
            max_concurrent=3,
        ),
    )

    # ── 4. RBAC Isolation Summary ─────────────────────────────────────────────
    if isolation_results:
        iso_passed_count = sum(1 for r in isolation_results if r["passed"])
        iso_total        = len(isolation_results)
        print(f"\n🛡️  RBAC ISOLATION: {iso_passed_count}/{iso_total} PASSED ({iso_passed_count / iso_total * 100:.1f}%)")


if __name__ == "__main__":
    import sys
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    run_benchmark(num_questions=count)
