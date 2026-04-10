from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import json


class LLMService:
    _tokenizer = None
    _model = None

    @classmethod
    def load_model(cls):
        if cls._tokenizer is None or cls._model is None:
            model_name = "google/flan-t5-base"
            cls._tokenizer = AutoTokenizer.from_pretrained(model_name)
            cls._model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    @classmethod
    def answer_question(cls, question: str, context: str) -> str:
        cls.load_model()

        prompt = f"""
You are an Intelligent document analysis assistant.

Use Only the provided context to answer the question.
you may summarize or infer from the context, but do not invent facts.

Answer the user's question clearly and concisely in 2-4 sentences

If the answer is not present in the context or context is insufficient, say:

"I could not find the answer in the provided document context."



Question:
{question}

context:
{context}
"""
        input = cls._tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        )

        outputs = cls._model.generate(
            **input,
            max_new_tokens=160,
            do_sample=False,
        )

        response = cls._tokenizer.decode(outputs[0], skip_special_tokens=True)

        return response.strip()

    @classmethod
    def extract_structured_analysis(cls, context: str) -> dict:
        cls.load_model()

        prompt = f"""
You are a legal document analysis assistant.

Using ONLY the context below, extract the following NDA-related fields.
If a field is missing, use an empty string.
If parties are missing, return an empty list.
If risks are missing, return an empty list.

Return ONLY valid JSON with this exact structure:

{{
  "document_type": "NDA",
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

        inputs = cls._tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=1024,
        )

        outputs = cls._model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
        )

        raw_output = cls._tokenizer.decode(outputs[0], skip_special_tokens=True).strip()

        try:
            return json.loads(raw_output)
        except Exception:
            return {
                "document_type": "NDA",
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
                "raw_output": raw_output,
            }
