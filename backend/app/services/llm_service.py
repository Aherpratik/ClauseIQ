import json
import re
from typing import Any

import requests


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
    _base_url = "http://localhost:11434/api/generate"
    _model_name = "mistral"

    @classmethod
    def _generate(
        cls,
        prompt: str,
        max_new_tokens: int = 256,
    ) -> str:
        try:
            response = requests.post(
                cls._base_url,
                json={
                    "model": cls._model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": max_new_tokens,
                        "temperature": 0.1,
                    },
                },
                timeout=120,
            )
            response.raise_for_status()

            data = response.json()
            text = data.get("response", "").strip()

            print("\n\n===== RAW MODEL OUTPUT =====")
            print(text)
            print("================================\n\n")

            if not text:
                return "NOT_FOUND"

            return text

        except Exception as e:
            print("Ollama request failed:", str(e))
            return "NOT_FOUND"

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

Summarize the document in exactly 2 short sentences.
Keep it concise and factual.
Do not invent information.
Do not use bullet points.

Context:
{context}

Answer:
"""
        summary = cls._generate(prompt=prompt, max_new_tokens=80)

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
You are a legal document question answering assistant.

Use only the context below to answer the question.

If the answer is not present in the context, respond exactly with:
I could not find the answer in the provided document context.

Context:
{context}

Question:
{question}

Answer:
"""
        answer = cls._generate(prompt=prompt, max_new_tokens=120)

        if answer == "NOT_FOUND":
            return "I could not find the answer in the provided document context."

        if answer.strip().lower() in {"do not guess", "answer:", "[]"}:
            return "I could not find the answer in the provided document context."

        return answer.strip()

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
        elif "appointment" in lower or "employment" in lower:
            document_type = "Employment Agreement"
        elif "confidential" in lower and "disclosure" in lower:
            document_type = "NDA"
        else:
            document_type = "Legal Agreement"

        # 2. Rule-based extraction first
        parties = []
        effective_date = ""
        governing_law = ""
        term = ""
        return_or_destruction_of_materials = ""

        company_match = re.search(
            r"([A-Z][A-Za-z0-9&.,\s]+?(?:Private Limited|Ltd|LLC|Inc))",
            text,
        )
        if company_match:
            parties.append(company_match.group(1).strip())

        name_match = re.search(
            r"(?:Mr\.|Ms\.|Mrs\.|Dr\.)?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)",
            text,
        )
        if name_match:
            candidate_name = cls._normalize_scalar(name_match.group(1))
            if candidate_name and candidate_name not in parties:
                parties.append(candidate_name)

        if '"Intern"' in text or '("Intern")' in text or "intern" in lower:
            parties.append("Intern")

        if not parties:
            if "disclosing party" in lower:
                parties.append("Disclosing Party")
            if "receiving party" in lower:
                parties.append("Receiving Party")

        date_match = re.search(
            r"(effective date|dated|entered into as of|made and entered into as of|commences on)\s*[:\-]?\s*([A-Za-z0-9,\/\-\s]+)",
            text,
            re.IGNORECASE,
        )
        if date_match:
            candidate = cls._normalize_scalar(date_match.group(2))
            if candidate and "mm/dd" not in candidate.lower():
                effective_date = candidate

                effective_date = re.sub(r"\s*,\s*", ", ", effective_date)

        law_match = re.search(
            r"(governed by|laws of|jurisdiction of)\s+([A-Za-z\s,]+)",
            text,
            re.IGNORECASE,
        )
        if law_match:
            governing_law = cls._normalize_scalar(law_match.group(1))

        term_match = re.search(
            r"(period of|term of|duration of).{0,80}",
            text,
            re.IGNORECASE,
        )
        if term_match:
            term = cls._normalize_scalar(term_match.group(0))

        return_match = re.search(
            r"(return|destroy).{0,180}(materials|information|documents)",
            text,
            re.IGNORECASE,
        )
        if return_match:
            return_or_destruction_of_materials = cls._normalize_scalar(
                return_match.group(0)
            )

        # 3. Mistral structured fallback
        prompt = f"""
You are a legal document extraction system.

Return only valid JSON.
Do not include markdown.
Do not include explanation text.

Use this exact JSON structure:
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
- document_type must be one of: NDA, Invention Assignment Agreement, Employment Agreement, Legal Agreement
- parties must be a JSON array of short names only
- if a field is missing, return "" or []
- do not return a Python list
- do not return prose before or after JSON

Document:
\"\"\"{text}\"\"\"
"""
        raw = cls._generate(prompt=prompt, max_new_tokens=220)
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
                r"(company intellectual property.{0,220}|inventions?.{0,220}|work product.{0,220}|intellectual property.{0,220})",
                text,
                re.IGNORECASE,
            )
            if ip_match:
                work_product_ip = cls._normalize_scalar(ip_match.group(0))

        llm_document_type = cls._normalize_scalar(str(parsed.get("document_type", "")))
        if llm_document_type in {
            "NDA",
            "Invention Assignment Agreement",
            "Employment Agreement",
            "Legal Agreement",
        }:
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

        # 4. Generic risk detection
        risks = []

        if not parties:
            risks.append("Parties are not clearly identified.")
        if not effective_date:
            risks.append("Effective date is not clearly identified.")
        if not governing_law:
            risks.append("Governing law is not clearly identified.")
        if not term:
            risks.append("Term or duration is not clearly identified.")
        if "termination" not in lower and "terminate" not in lower:
            risks.append("Termination terms are not clearly identified.")

        if (
            "sign" not in lower
            and "signature" not in lower
            and "accepted" not in lower
            and "acceptance" not in lower
        ):
            risks.append("Signature or acceptance language is not clearly identified.")

        if "____" in text or "___" in text or "(mm/dd/yy)" in lower:
            risks.append("Document appears to contain unfilled placeholders.")

        obligation_markers = [
            "shall",
            "must",
            "agree to",
            "agrees to",
            "responsible for",
        ]
        if not any(marker in lower for marker in obligation_markers):
            risks.append("Key obligations are not clearly stated.")

        payment_context_markers = [
            "salary",
            "compensation",
            "payment",
            "ctc",
            "remuneration",
            "wages",
            "bonus",
        ]
        if any(marker in lower for marker in payment_context_markers):
            if not re.search(
                r"(salary|compensation|ctc|remuneration|wages).{0,80}(\d|\$|rs|inr)",
                lower,
            ):
                risks.append(
                    "Payment or compensation terms may not be clearly specified."
                )

        ip_markers = [
            "intellectual property",
            "inventions",
            "assignment",
            "ownership",
            "work product",
            "proprietary",
        ]
        if any(marker in lower for marker in ip_markers):
            if not assignment_scope and not work_product_ip:
                risks.append(
                    "Intellectual property or ownership scope is not clearly identified."
                )

        formatted_risks = []
        for r in list(dict.fromkeys(risks))[:6]:
            severity = "low"

            if any(
                word in r.lower()
                for word in ["missing", "not clearly", "not identified"]
            ):
                severity = "medium"

            if any(
                word in r.lower()
                for word in ["missing governing law", "missing parties"]
            ):
                severity = "high"

            formatted_risks.append(
                {
                    "title": r,
                    "description": r,
                    "severity": severity,
                }
            )

        clauses = []
        text_lower = lower

        if "confidential" in text_lower:
            clauses.append("Confidentiality")
        if "termination" in text_lower:
            clauses.append("Termination")
        if "payment" in text_lower or "salary" in text_lower:
            clauses.append("Compensation")
        if "law" in text_lower or "jurisdiction" in text_lower:
            clauses.append("Governing Law")
        if "liability" in text_lower:
            clauses.append("Liability")
        if "agreement" in text_lower and len(clauses) == 0:
            clauses.append("General Terms")
        if not clauses:
            clauses = ["General Clause"]

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
            "risks": formatted_risks,
            "clauses": clauses,
        }
