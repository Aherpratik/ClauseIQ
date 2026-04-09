from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


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
You are a careful document analysis assistant.

Answer the user's question using ONLY the provided context.
If the answer is not present in the context, say:

"I could not find the answer in the provided document context."

Be Concise, accurate and grounded. 

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
            max_new_tokens=128,
            do_sample=False,
        )

        response = cls._tokenizer.decode(outputs[0], skip_special_tokens=True)

        return response.strip()
