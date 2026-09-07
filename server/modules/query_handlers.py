import time
from logger import logger


def query_chain(chain, user_input: str):
    try:
        logger.debug(f"Running chain for input: {user_input}")

        start_time = time.time()
        result = chain.invoke({"query": user_input})
        end_time = time.time()

        latency = round(end_time - start_time, 3)

        # Token usage
        token_usage = result.get("token_usage", {})
        prompt_tokens = token_usage.get("prompt_tokens", 0)
        completion_tokens = token_usage.get("completion_tokens", 0)
        total_tokens = token_usage.get("total_tokens", 0)

        # Cost estimate (Groq gpt-oss-20b pricing ~$0.00027 per 1K tokens)
        cost_usd = round((total_tokens / 1000) * 0.00027, 6)

        response = {
            "response": result["result"],
            "sources": [doc.metadata.get("source", "") for doc in result["source_documents"]],
            "metrics": {
                "latency_seconds": latency,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": total_tokens,
                "estimated_cost_usd": cost_usd
            }
        }

        logger.info(f"Latency: {latency}s | Tokens: {total_tokens} | Cost: ${cost_usd}")
        logger.debug(f"Chain response: {response}")
        return response

    except Exception as e:
        logger.exception("Error on query chain")
        raise