def test_job(name: str) -> str:
    print(f"[WORKER] Hello, {name}!", flush=True)

    return f"Processed {name}"
