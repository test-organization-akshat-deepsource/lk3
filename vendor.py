import json
import pika
import zstandard as zstd
from enki_v2.config import settings

message_payload = {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "task": "analysis_task",
    "retries": 0,
    "kwargs": {
        "run_id": "analysis-run-12345",
        "status": {
            "code": 200,
            "hmessage": "Analysis completed successfully",
            "err": "",
        },
        "check_seq": "cxx",
        "report": {
            "issues": [
                {
                    "issue_code": "SEC-001",
                    "issue_text": "Potential SQL injection vulnerability",
                    "location": {
                        "path": "app/models.py",
                        "position": {
                            "begin": {"line": 25, "column": 5},
                            "end": {"line": 27, "column": 30},
                        },
                    },
                    "processed_data": None,
                    "identifier": "sec-001",
                }
            ],
            "metrics": None,
            "is_passed": False,
            "errors": None,
            "file_meta": {
                "if_all": False,
                "deleted": [],
                "renamed": [],
                "modified": ["app/models.py"],
                "added": [],
                "diff_meta": None,
                "pr_diff_meta": None,
            },
            "extra_data": None,
        },
        "report_object": "",
    },
}

compressor = zstd.ZstdCompressor()
json_str = json.dumps(message_payload)
compressed_body = compressor.compress(json_str.encode("utf-8"))

connection = pika.BlockingConnection(pika.URLParameters(settings.rmq_url))
channel = connection.channel()
# channel.exchange_declare(exchange=settings.rmq_exchange, exchange_type='direct')

routing_key = f"enki-tmp-q-{settings.session_id}"
channel.basic_publish(
    exchange=settings.rmq_exchange, routing_key=routing_key, body=compressed_body
)

print(f"Compressed message published to {routing_key}")
connection.close()
