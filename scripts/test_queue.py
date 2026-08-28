from app.workers.ingestion_worker import test_job
from app.workers.queue import ingestion_queue

job = ingestion_queue.enqueue(
    test_job,
    "Repo Intelligence",
)

print(f"Queued job: {job.id}")
