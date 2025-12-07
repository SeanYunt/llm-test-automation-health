def log_message(message: str) -> None:
    print(f"[LOG] {message}")

def format_results(results: dict) -> str:
    formatted = "\n".join(f"{key}: {value}" for key, value in results.items())
    return formatted