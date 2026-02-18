"""Real article summarization service using T5 transformer model"""
import logging
from typing import List, Optional
from ..core.exceptions import SummarizationError
from ..core.error_handler import handle_errors

logger = logging.getLogger(__name__)

# Lazy loading of heavy ML imports
_model = None
_tokenizer = None


def _load_model(model_name: str = "t5-small", use_gpu: bool = False):
    """Lazy-load the T5 model and tokenizer"""
    global _model, _tokenizer

    if _model is not None and _tokenizer is not None:
        return _model, _tokenizer

    try:
        from transformers import T5ForConditionalGeneration, T5Tokenizer
        import torch

        logger.info(f"Loading summarization model: {model_name}")
        _tokenizer = T5Tokenizer.from_pretrained(model_name, legacy=True)
        _model = T5ForConditionalGeneration.from_pretrained(model_name)

        if use_gpu and torch.cuda.is_available():
            _model = _model.to("cuda")
            logger.info("Summarizer using GPU")
        else:
            logger.info("Summarizer using CPU")

        _model.eval()
        logger.info(f"Model {model_name} loaded successfully")
        return _model, _tokenizer

    except Exception as e:
        logger.error(f"Failed to load model {model_name}: {e}")
        raise SummarizationError(f"Model loading failed: {e}")


class Summarizer:
    """
    Production article summarization service using T5 transformer.
    Falls back to extractive summarization if model loading fails.
    """

    def __init__(self, model_name: str = "t5-small", max_length: int = 150,
                 use_gpu: bool = False, num_beams: int = 4):
        self.model_name = model_name
        self.max_length = max_length
        self.use_gpu = use_gpu
        self.num_beams = num_beams
        self.max_input_tokens = 512
        self._model_loaded = False
        logger.info(f"Summarizer initialized (model={model_name}, max_length={max_length})")

    def _ensure_model(self):
        """Ensure model is loaded"""
        if not self._model_loaded:
            try:
                _load_model(self.model_name, self.use_gpu)
                self._model_loaded = True
            except Exception as e:
                logger.warning(f"Model not available, will use extractive fallback: {e}")

    def _preprocess(self, content: str) -> str:
        """Preprocess content for T5 model"""
        from bs4 import BeautifulSoup
        import re

        # Strip HTML
        try:
            soup = BeautifulSoup(content, "html.parser")
            content = soup.get_text(separator=" ", strip=True)
        except Exception:
            pass

        # Normalize whitespace
        content = re.sub(r'\s+', ' ', content).strip()

        # Add T5 task prefix
        return f"summarize: {content}"

    @handle_errors
    def summarize(self, content: str) -> str:
        """
        Generate summary of article content using T5 model.
        Falls back to extractive summarization on failure.

        Args:
            content: Article content

        Returns:
            Summary text
        """
        if not content:
            return ""

        words = content.split()

        # If content is shorter than max length, return as is
        if len(words) <= self.max_length:
            return content

        # Try AI-powered summarization
        self._ensure_model()

        if self._model_loaded and _model is not None and _tokenizer is not None:
            try:
                return self._ai_summarize(content)
            except Exception as e:
                logger.warning(f"AI summarization failed, using extractive fallback: {e}")

        # Fallback: extractive summarization
        return self._extractive_summarize(content)

    def _ai_summarize(self, content: str) -> str:
        """Summarize using T5 model"""
        import torch

        preprocessed = self._preprocess(content)

        # Tokenize with truncation for long articles
        inputs = _tokenizer(
            preprocessed,
            return_tensors="pt",
            max_length=self.max_input_tokens,
            truncation=True,
            padding=True,
        )

        if self.use_gpu and torch.cuda.is_available():
            inputs = {k: v.to("cuda") for k, v in inputs.items()}

        # Generate summary
        with torch.no_grad():
            summary_ids = _model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_length=self.max_length,
                min_length=30,
                num_beams=self.num_beams,
                length_penalty=2.0,
                early_stopping=True,
                no_repeat_ngram_size=3,
            )

        summary = _tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        # Ensure word count limit
        summary_words = summary.split()
        if len(summary_words) > self.max_length:
            summary = " ".join(summary_words[:self.max_length])
            if not summary.endswith('.'):
                summary += '.'

        logger.debug(f"AI summary: {len(summary_words)} words from {len(content.split())} words")
        return summary

    def _extractive_summarize(self, content: str) -> str:
        """Fallback extractive summarization - takes first N sentences up to word limit"""
        sentences = content.replace('\n', ' ').split('. ')
        summary_words = []
        word_count = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            words = sentence.split()
            if word_count + len(words) <= self.max_length:
                summary_words.extend(words)
                word_count += len(words)
            else:
                break

        summary = ' '.join(summary_words)
        if summary and not summary.endswith('.'):
            summary += '.'

        logger.debug(f"Extractive summary: {word_count} words from {len(content.split())} words")
        return summary

    @handle_errors
    def batch_summarize(self, contents: List[str]) -> List[str]:
        """
        Summarize multiple articles.

        Args:
            contents: List of article contents

        Returns:
            List of summaries
        """
        logger.info(f"Batch summarizing {len(contents)} articles")
        summaries = []

        self._ensure_model()

        if self._model_loaded and _model is not None and _tokenizer is not None:
            # Process in batches for efficiency
            batch_size = 8
            for i in range(0, len(contents), batch_size):
                batch = contents[i:i + batch_size]
                for content in batch:
                    try:
                        summary = self.summarize(content)
                        summaries.append(summary)
                    except Exception as e:
                        logger.warning(f"Batch item failed: {e}")
                        summaries.append(self._extractive_summarize(content))
        else:
            # Use extractive fallback for all
            for content in contents:
                summaries.append(self._extractive_summarize(content))

        return summaries
