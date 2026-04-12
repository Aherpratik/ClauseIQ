from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json
import re
from typing import Any


class LLMService:
    _tokenizer = None
    _model = None
    _model_name = "google/flan-t5-large"

    @classmethod
    def load_model(cls):
        if cls._tokenizer is None or cls._model is None:
            cls._tokenizer = AutoTokenizer.from_pretrained(cls._model_name)
            cls._model = AutoModelForSeq2SeqLM.from_pretrained(cls._model_name)

    @classmethod
    def _generate(
        cls,
        prompt: str,
        max_input_tokens: int = 1024,
        max_new_tokens: int = 128,
    ) -> str:
        cls.load_model()

        inputs = cls._tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=max_input_tokens,
        )

        outputs = cls._model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=False,
        )

        response = cls._tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        print("\n\n===== RAW MODEL OUTPUT =====")
        print(response)
        print("================================\n\n")

        if not response:
            return "NOT_FOUND"

        return response

    @staticmethod
    def _clean_text(value: str) -> str:
        if not value:
            return ""
        return re.sub(r"\s+", " ", value).strip()

    @staticmethod
    def _normalize_scalar(value: str) -> str:
        cleaned = LLMService._clean_text(value)
        lowered = cleaned.lower()

        bad_values = {
            "",
            "not found",
            "unknown",
            "n/a",
            "none",
            "null",
            "not specified",
            "not provided",
            "not mentioned",
            "effective_date",
            "term",
            "governing_law",
            "non_disclosure_obligations",
            "third_party_disclosure_rules",
            "parties",
            "document_type",
        }

        # remove obvious metadata junk
        if "score " in lowered or "[page " in lowered:
            return ""

        # remove long underscore placeholders
        if re.fullmatch(r"_+", cleaned):
            return ""

        return "" if lowered in bad_values else cleaned

    @staticmethod
    def _normalize_list_text(value: str) -> list[str]:
        cleaned = LLMService._clean_text(value)

        if not cleaned:
            return []

        lowered = cleaned.lower()
        if lowered in {"not found", "unknown", "none", "null", "n/a", "parties"}:
            return []

        parts = re.split(r"\s*[,;|\n]\s*", cleaned)
        parts = [p.strip(" -•\t") for p in parts if p.strip(" -•\t")]

        seen = set()
        result = []
        for part in parts:
            key = part.lower()
            if key not in seen and key not in {"parties"}:
                seen.add(key)
                result.append(part)

        return result

    @classmethod
    def summarize_document(cls, context: str) -> str:
        prompt = f"""
You are a legal document summarization assistant.

Using ONLY the provided context, write a concise summary in 4 bullet points.

Rules:
- Focus on document purpose, parties, confidentiality obligations, exclusions, and governing law if present.
- Do not copy the document verbatim.
- Do not repeat the same phrase.
- Do not invent facts.
- If a field is missing, simply omit it.

Context:
{context}
"""
        summary = cls._generate(prompt=prompt, max_new_tokens=180)

        if summary == "NOT_FOUND":
            return "Summary could not be generated."

        return summary

    @classmethod
    def answer_question(cls, question: str, context: str) -> str:
        prompt = f"""
You are a legal document question-answering assistant.

Answer the question using ONLY the provided context.

Rules:
- Do not invent facts.
- Do not use outside knowledge.
- Keep the answer to 1 to 3 sentences.
- If the answer is not clearly present, return exactly:
I could not find the answer in the provided document context.

Question:
{question}

Context:
{context}
"""
        answer = cls._generate(prompt=prompt, max_new_tokens=120)

        if answer == "NOT_FOUND":
            return "I could not find the answer in the provided document context."

        return answer

    @classmethod
    def extract_structured_analysis(cls, context: str) -> dict[str, Any]:
        """
        Use ONE structured extraction call instead of many field-by-field calls.
        This is more stable than the previous version.
        """

        prompt = f"""
You are a legal document analysis assistant.

Using ONLY the context below, extract structured information from the agreement.

STRICT RULES:
- Return ONLY valid JSON.
- Do NOT include markdown.
- Do NOT include explanations.
- Do NOT return field names as values.
- If a value is missing, return an empty string.
- For parties, return a JSON array.
- For risks, return a JSON array of strings.

Return this exact JSON structure:

{{
  "document_type": "",
  "parties": [],
  "effective_date": "",
  "term": "",
  "confidential_information_definition": "",
  "permitted_use": "",
  "non_disclosure_obligations": "",
  "exclusions": "",
  "third_party_disclosure_rules": "",
  "return_or_destruction_of_materials": "",
  "termination": "",
  "governing_law": "",
  "survival_clause": "",
  "risks": []
}}

Context:
{context}
"""

        raw = cls._generate(prompt=prompt, max_new_tokens=300)

        try:
            parsed = json.loads(raw)

            return {
                "document_type": cls._normalize_scalar(
                    str(parsed.get("document_type", ""))
                ),
                "parties": cls._normalize_list_text(
                    ", ".join(parsed.get("parties", []))
                    if isinstance(parsed.get("parties", []), list)
                    else str(parsed.get("parties", ""))
                ),
                "effective_date": cls._normalize_scalar(
                    str(parsed.get("effective_date", ""))
                ),
                "term": cls._normalize_scalar(str(parsed.get("term", ""))),
                "confidential_information_definition": cls._normalize_scalar(
                    str(parsed.get("confidential_information_definition", ""))
                ),
                "permitted_use": cls._normalize_scalar(
                    str(parsed.get("permitted_use", ""))
                ),
                "non_disclosure_obligations": cls._normalize_scalar(
                    str(parsed.get("non_disclosure_obligations", ""))
                ),
                "exclusions": cls._normalize_scalar(str(parsed.get("exclusions", ""))),
                "third_party_disclosure_rules": cls._normalize_scalar(
                    str(parsed.get("third_party_disclosure_rules", ""))
                ),
                "return_or_destruction_of_materials": cls._normalize_scalar(
                    str(parsed.get("return_or_destruction_of_materials", ""))
                ),
                "termination": cls._normalize_scalar(
                    str(parsed.get("termination", ""))
                ),
                "governing_law": cls._normalize_scalar(
                    str(parsed.get("governing_law", ""))
                ),
                "survival_clause": cls._normalize_scalar(
                    str(parsed.get("survival_clause", ""))
                ),
                "risks": (
                    [r for r in parsed.get("risks", []) if isinstance(r, str)]
                    if isinstance(parsed.get("risks", []), list)
                    else []
                ),
            }

        except Exception:
            return {
                "document_type": "",
                "parties": [],
                "effective_date": "",
                "term": "",
                "confidential_information_definition": "",
                "permitted_use": "",
                "non_disclosure_obligations": "",
                "exclusions": "",
                "third_party_disclosure_rules": "",
                "return_or_destruction_of_materials": "",
                "termination": "",
                "governing_law": "",
                "survival_clause": "",
                "risks": [],
            }
