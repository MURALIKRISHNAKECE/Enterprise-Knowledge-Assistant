from logger import logger


def run_ragas_evaluation(question: str, answer: str, contexts: list):
    """
    Simplified evaluation using heuristic metrics.
    Full RAGAS evaluation skipped due to LangChain compatibility issues.
    """
    try:
        # Context coverage — how many context chunks contain words from the answer
        answer_words = set(answer.lower().split())
        coverage_scores = []
        for ctx in contexts:
            ctx_words = set(ctx.lower().split())
            overlap = len(answer_words & ctx_words) / max(len(answer_words), 1)
            coverage_scores.append(overlap)

        faithfulness = round(max(coverage_scores) if coverage_scores else 0.0, 4)

        # Answer relevancy — overlap between question and answer words
        question_words = set(question.lower().split())
        relevancy = len(question_words & answer_words) / max(len(question_words), 1)
        answer_relevancy = round(min(relevancy * 2, 1.0), 4)

        # Context precision — average coverage across all contexts
        context_precision = round(
            sum(coverage_scores) / len(coverage_scores) if coverage_scores else 0.0, 4
        )

        scores = {
            "faithfulness": faithfulness,
            "answer_relevancy": answer_relevancy,
            "context_precision": context_precision,
        }

        logger.info(f"Evaluation scores: {scores}")
        return scores

    except Exception as e:
        logger.exception("Evaluation failed")
        return {
            "faithfulness": None,
            "answer_relevancy": None,
            "context_precision": None,
            "error": str(e)
        }