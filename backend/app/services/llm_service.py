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

        response = cls._tokenizer.decode(outputs[0], skip_special_tokens=True)
        print("\n\n===== RAW MODEL OUTPUT =====")
        print(response)
        print("================================\n\n")
        return response.strip()

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
        }
        return "" if lowered in bad_values else cleaned

    @staticmethod
    def _normalize_list_text(value: str) -> list[str]:
        cleaned = LLMService._clean_text(value)

        if not cleaned:
            return []

        lowered = cleaned.lower()
        if lowered in {"not found", "unknown", "none", "null", "n/a"}:
            return []

        parts = re.split(r"\s*[,;|\n]\s*", cleaned)
        parts = [p.strip(" -•\t") for p in parts if p.strip(" -•\t")]

        seen = set()
        result = []
        for part in parts:
            key = part.lower()
            if key not in seen:
                seen.add(key)
                result.append(part)

        return result

    @classmethod
    def summarize_document(cls, context: str) -> str:
        prompt = f"""
You are a legal document summarization assistant.

Summarize the document using ONLY the provided context.

Requirements:
- Write 4 to 6 concise bullet points.
- Focus on the document purpose, core obligations, exclusions, term, and governing law if present.
- Do not invent facts.
- If the context is insufficient, say that the summary is limited.

Context:
{context}
"""
        return cls._generate(prompt=prompt, max_new_tokens=180)

    @classmethod
    def answer_question(cls, question: str, context: str) -> str:

        prompt = f"""
You are a legal document question-answering assistant.

Answer the question using ONLY the provided context.
Do NOT invent facts.
Do NOT rely on outside knowledge.
If the answer is not clearly present in the context, respond exactly with:
I could not find the answer in the provided document context.

Requirements:
- Answer in 1 to 3 sentences.
- Prefer precise language from the document.
- Be direct and factual.

Question:
{question}

context:
{context}
"""
        return cls._generate(prompt=prompt, max_new_tokens=120)

    @classmethod
    def extract_field(cls, field_name: str, instructions: str, context: str) -> str:
        prompt = f"""
You are a legal document extraction assistant.

Extract ONLY the field requested below using ONLY the provided context.

Field:
{field_name}

Instructions:
{instructions}

Rules:
- Return only the extracted value.
- Do not return labels.
- Do not explain.
- If the field is missing or unclear, return exactly:
NOT_FOUND

Context:
{context}
"""
        raw = cls._generate(prompt=prompt, max_new_tokens=80)
        return cls._normalize_scalar("" if raw == "NOT_FOUND" else raw)

    @classmethod
    def extract_list_field(
        cls,
        field_name: str,
        instructions: str,
        context: str,
    ) -> list[str]:
        prompt = f"""
You are a legal document extraction assistant.

Extract ONLY the requested list field using ONLY the provided context.

Field:
{field_name}

Instructions:
{instructions}

Rules:
- Return a comma-separated list only.
- Do not return labels.
- Do not explain.
- If nothing is found, return exactly:
NOT_FOUND

Context:
{context}
"""
        raw = cls._generate(prompt=prompt, max_new_tokens=80)
        if raw == "NOT_FOUND":
            return []
        return cls._normalize_list_text(raw)

    @classmethod
    def extract_risks(cls, context: str) -> list[dict[str, Any]]:
        prompt = f"""
You are a legal risk review assistant.

Using ONLY the provided context, identify up to 3 meaningful risks or review flags.

Return ONLY valid JSON as an array with this exact structure:
[
  {{
    "title": "short risk title",
    "severity": "high|medium|low",
    "description": "brief explanation",
    "recommendation": "brief recommendation"
  }}
]

Rules:
- If no clear risks are present, return [].
- Do not include markdown.
- Do not include any text outside JSON.

Context:
{context}
"""
        raw = cls._generate(prompt=prompt, max_new_tokens=220)

        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                normalized = []
                for item in parsed:
                    if not isinstance(item, dict):
                        continue
                    normalized.append(
                        {
                            "title": cls._normalize_scalar(str(item.get("title", ""))),
                            "severity": cls._normalize_scalar(
                                str(item.get("severity", ""))
                            ).lower()
                            or "low",
                            "description": cls._normalize_scalar(
                                str(item.get("description", ""))
                            ),
                            "recommendation": cls._normalize_scalar(
                                str(item.get("recommendation", ""))
                            ),
                        }
                    )
                return normalized
        except Exception:
            pass

        return []

    @classmethod
    def extract_structured_analysis(cls, context: str) -> dict[str, Any]:

        document_type = cls.extract_field(
            field_name="document_type",
            instructions=(
                "Identify the document type. "
                "If it is a non-disclosure agreement, return NDA. "
                "Otherwise return the most specific document type found."
            ),
            context=context,
        )

        parties = cls.extract_list_field(
            field_name="parties",
            instructions=(
                "Extract the names of the parties to the agreement. "
                "If exact legal names are not present, return the role names if clearly used."
            ),
            context=context,
        )

        effective_date = cls.extract_field(
            field_name="effective_date",
            instructions="Extract the effective date of the agreement.",
            context=context,
        )

        term = cls.extract_field(
            field_name="term",
            instructions="Extract the stated term or duration of the agreement.",
            context=context,
        )

        confidential_information_definition = cls.extract_field(
            field_name="confidential_information_definition",
            instructions=(
                "Extract the clause or sentence defining confidential information."
            ),
            context=context,
        )

        permitted_use = cls.extract_field(
            field_name="permitted_use",
            instructions=(
                "Extract how the receiving party is permitted to use confidential information."
            ),
            context=context,
        )

        non_disclosure_obligations = cls.extract_field(
            field_name="non_disclosure_obligations",
            instructions=(
                "Extract the main non-disclosure or protection obligations of the receiving party."
            ),
            context=context,
        )

        exclusions = cls.extract_field(
            field_name="exclusions",
            instructions=(
                "Extract the exclusions or exceptions to confidential information."
            ),
            context=context,
        )

        third_party_disclosure_rules = cls.extract_field(
            field_name="third_party_disclosure_rules",
            instructions=(
                "Extract rules about disclosure to third parties, affiliates, advisors, or required disclosures."
            ),
            context=context,
        )

        return_or_destruction_of_materials = cls.extract_field(
            field_name="return_or_destruction_of_materials",
            instructions=(
                "Extract any return, destruction, or deletion obligations for confidential materials."
            ),
            context=context,
        )

        termination = cls.extract_field(
            field_name="termination",
            instructions="Extract any termination clause or termination conditions.",
            context=context,
        )

        governing_law = cls.extract_field(
            field_name="governing_law",
            instructions="Extract the governing law or jurisdiction clause.",
            context=context,
        )

        survival_clause = cls.extract_field(
            field_name="survival_clause",
            instructions=(
                "Extract any survival clause or confidentiality survival period."
            ),
            context=context,
        )

        risks = cls.extract_risks(context)

        return {
            "document_type": document_type,
            "parties": parties,
            "effective_date": effective_date,
            "term": term,
            "confidential_information_definition": confidential_information_definition,
            "permitted_use": permitted_use,
            "non_disclosure_obligations": non_disclosure_obligations,
            "exclusions": exclusions,
            "third_party_disclosure_rules": third_party_disclosure_rules,
            "return_or_destruction_of_materials": return_or_destruction_of_materials,
            "termination": termination,
            "governing_law": governing_law,
            "survival_clause": survival_clause,
            "risks": risks,
        }
