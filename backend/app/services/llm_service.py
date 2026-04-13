import json
import re
from typing import Any

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


def extract_json(text):
    try:
        # Try direct JSON
        return json.loads(text)
    except:
        pass

    # Try to extract JSON block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    print(" JSON extraction failed. Raw output:", text)
    return {}


def safe_parse_json(raw: str):
    try:
        return json.loads(raw)
    except Exception:
        pass

    try:
        start = raw.find("{")
        end = raw.rfind("}")
        if start != -1 and end != -1 and end > start:
            return json.loads(raw[start : end + 1])
    except Exception:
        pass

    return {}


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
        max_new_tokens: int = 256,
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

        if lowered in bad_values:
            return ""

        if "score " in lowered or "[page " in lowered:
            return ""

        if re.fullmatch(r"_+", cleaned):
            return ""

        if len(set(cleaned)) == 1 and len(cleaned) > 5:
            return ""

        return cleaned

    @staticmethod
    def _normalize_list_text(value: str) -> list[str]:
        cleaned = LLMService._clean_text(value)

        if not cleaned:
            return []

        lowered = cleaned.lower()
        if lowered in {"not found", "unknown", "none", "null", "n/a", "parties"}:
            return []

        parts = re.split(r"\s*[,;|\n]\s*", cleaned)
        parts = [p.strip(" -•\t\"'") for p in parts if p.strip(" -•\t\"'")]

        seen = set()
        result = []
        for part in parts:
            key = part.lower()
            if key not in seen and key not in {"parties"}:
                seen.add(key)
                result.append(part)

        return result

    @staticmethod
    def _dedupe_parties(parties: list[str]) -> list[str]:
        cleaned = []
        seen = set()

        for party in parties:
            normalized = party.strip().strip('"').strip("'")
            key = normalized.lower()

            if not normalized:
                continue

            if key in {"parties", "party"}:
                continue

            if key not in seen:
                seen.add(key)
                cleaned.append(normalized)

        return cleaned[:5]

    @classmethod
    def summarize_document(cls, context: str) -> str:
        prompt = f"""
You are a legal document summarization assistant.

Summarize the document in EXACTLY 2 short sentences.

STRICT RULES:
- Each sentence must be short.
- Maximum total length: 45 words.
- Do NOT copy long phrases from the document.
- Do NOT include quotes.
- Focus only on the document purpose and main obligation.
- If governing law or exclusions are clearly present, mention at most one of them briefly.
- Do NOT invent facts.

Context:
{context}
"""
        summary = cls._generate(prompt=prompt, max_new_tokens=60)

        if summary == "NOT_FOUND":
            return "Summary could not be generated."

        summary = cls._clean_text(summary)
        words = summary.split()
        if len(words) > 45:
            summary = " ".join(words[:45]).rstrip() + "..."

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
        answer = cls._generate(prompt=prompt, max_new_tokens=140)

        if answer == "NOT_FOUND":
            return "I could not find the answer in the provided document context."

        return answer

    @classmethod
    def extract_structured_analysis(cls, context: str) -> dict[str, Any]:
        text = cls._clean_text(context)
        lower = text.lower()

        # 1. Detect document type
        if "invention assignment agreement" in lower:
            document_type = "Invention Assignment Agreement"
        elif (
            "non-disclosure agreement" in lower
            or "nondisclosure agreement" in lower
            or "nda" in lower
        ):
            document_type = "NDA"
        elif "confidential" in lower and "disclosure" in lower:
            document_type = "NDA"
        else:
            document_type = "Legal Agreement"

        # 2. Strong rule-based extraction
        parties = []
        effective_date = ""
        governing_law = ""
        term = ""
        return_or_destruction_of_materials = ""

        # Better company extraction for invention assignment agreements
        company_match = re.search(
            r'by\s+and\s+between\s+([A-Z][A-Za-z0-9&,\.\-\s]+?)\s+\("Company"\)',
            text,
            re.IGNORECASE,
        )

        if company_match:
            parties.append(company_match.group(1).strip())

        # Intern detection
        if '"Intern"' in text or '("Intern")' in text or "intern" in lower:
            parties.append("Intern")

        # NDA fallback roles
        if not parties:
            if "disclosing party" in lower:
                parties.append("Disclosing Party")
            if "receiving party" in lower:
                parties.append("Receiving Party")

        # Effective date
        date_match = re.search(
            r"(effective date|dated|entered into as of|made and entered into as of)\s*[:\-]?\s*([A-Za-z0-9,\/\-\s]+)",
            text,
            re.IGNORECASE,
        )
        if date_match:
            candidate = cls._normalize_scalar(date_match.group(2))
            if candidate and "mm/dd" not in candidate.lower():
                effective_date = candidate

        # Governing law
        law_match = re.search(
            r"governed by the laws of\s+([A-Za-z\s]+)",
            text,
            re.IGNORECASE,
        )
        if law_match:
            governing_law = cls._normalize_scalar(law_match.group(1))

        # Term / survival
        term_match = re.search(
            r"(term|survive|survival).{0,120}",
            text,
            re.IGNORECASE,
        )
        if term_match:
            term = cls._normalize_scalar(term_match.group(0))

        # Return / destruction
        return_match = re.search(
            r"(return|destroy).{0,180}(materials|information|documents)",
            text,
            re.IGNORECASE,
        )
        if return_match:
            return_or_destruction_of_materials = cls._normalize_scalar(
                return_match.group(0)
            )

        # 3. LLM fallback for document-specific enrichment
        prompt = f"""
    You are a legal document extraction system.

    Extract structured information from the document.

    Return ONLY valid JSON. Do NOT include any explanation or extra text.

    Required JSON format:

    {{
    "document_type": "",
    "parties": [],
    "effective_date": "",
    "governing_law": "",
    "term": "",
    "assignment_scope": "",
    "work_product_ip": ""
    }}

    Rules:
    - document_type must be one of: NDA, Invention Assignment Agreement, Other
    - parties must be a list of names
    - If not found, return empty string "" or empty list []
    - Output MUST be valid JSON with no text before or after

    Document:
    \"\"\"{text}\"\"\"
    """

        raw = cls._generate(prompt=prompt, max_new_tokens=260)
        print("RAW LLM:", raw)

        parsed = safe_parse_json(raw)
        parsed = parsed if isinstance(parsed, dict) else {}

        assignment_scope = cls._normalize_scalar(
            str(parsed.get("assignment_scope", ""))
        )
        work_product_ip = cls._normalize_scalar(str(parsed.get("work_product_ip", "")))

        if not assignment_scope:
            scope_match = re.search(
                r"(assignment of rights.{0,180}|assign.{0,180}inventions?.{0,180}|inventions?.{0,180}assigned.{0,180})",
                text,
                re.IGNORECASE,
            )
            if scope_match:
                assignment_scope = cls._normalize_scalar(scope_match.group(0))

        if not work_product_ip:
            ip_match = re.search(
                r"(company intellectual property.{0,220}|inventions?.{0,220}|work product.{0,220})",
                text,
                re.IGNORECASE,
            )
            if ip_match:
                work_product_ip = cls._normalize_scalar(ip_match.group(0))

        # Optional override only if LLM returns something usable
        llm_document_type = cls._normalize_scalar(str(parsed.get("document_type", "")))
        if llm_document_type in {"NDA", "Invention Assignment Agreement", "Other"}:
            if llm_document_type == "Other":
                document_type = "Legal Agreement"
            else:
                document_type = llm_document_type

        llm_parties = parsed.get("parties", [])
        if isinstance(llm_parties, list) and llm_parties:
            normalized_llm_parties = cls._dedupe_parties(
                [cls._normalize_scalar(str(p)) for p in llm_parties if str(p).strip()]
            )
            if normalized_llm_parties:
                parties = normalized_llm_parties

        llm_effective_date = cls._normalize_scalar(
            str(parsed.get("effective_date", ""))
        )
        if llm_effective_date and "mm/dd" not in llm_effective_date.lower():
            effective_date = llm_effective_date

        llm_governing_law = cls._normalize_scalar(str(parsed.get("governing_law", "")))
        if llm_governing_law:
            governing_law = llm_governing_law

        llm_term = cls._normalize_scalar(str(parsed.get("term", "")))
        if llm_term:
            term = llm_term

        # --------- FALLBACK: Work Product / IP (RULE-BASED) ---------
        if not work_product_ip:
            ip_match = re.search(
                r"(inventions?.{0,120}|intellectual property.{0,120}|work product.{0,120})",
                text,
                re.IGNORECASE,
            )
            if ip_match:
                work_product_ip = cls._normalize_scalar(ip_match.group(0))

        return {
            "document_type": document_type,
            "parties": cls._dedupe_parties(parties),
            "effective_date": effective_date,
            "term": term,
            "governing_law": governing_law,
            "assignment_scope": assignment_scope,
            "work_product_ip": work_product_ip,
            "return_or_destruction_of_materials": return_or_destruction_of_materials,
            "confidential_information_definition": "",
            "permitted_use": "",
            "non_disclosure_obligations": "",
            "exclusions": "",
            "third_party_disclosure_rules": "",
            "termination": "",
            "survival_clause": "",
            "risks": [],
        }
