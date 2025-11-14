import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# make sure the queue exists
# channel.queue_declare(queue='hello')

rmq_analyzer_task_message_json = """{
    "id": "task_12345",
    "task": "analyze_code_quality",
    "kwargs": {
      "run_id": "run_67890",
      "status": {
        "code": 200,
        "hmessage": "Analysis completed successfully",
        "err": ""
      },
      "check_seq": "seq_001",
      "report": {
        "issues": [
          {
            "issue_code": "W001",
            "issue_text": "Unused variable found",
            "location": {
              "path": "/src/main.py",
              "position": {
                "begin": {
                  "line": 15,
                  "column": 4
                },
                "end": {
                  "line": 15,
                  "column": 12
                }
              }
            },
            "processed_data": {
              "source_code": {
                "rendered": ["dmFyIHVudXNlZF92YXJpYWJsZSA9IDEwOw=="]
              }
            },
            "identifier": "unused_var_main_15"
          }
        ],
        "metrics": [
          {
            "metric_code": "M001",
            "namespace": [
              {
                "key": "complexity",
                "value": "low",
                "metadata": {
                  "score": 2.5
                }
              }
            ]
          }
        ],
        "is_passed": true,
        "errors": [],
        "file_meta": {
          "if_all": false,
          "deleted": [],
          "renamed": [],
          "modified": ["src/main.py"],
          "added": [],
          "diff_meta": {
            "src/main.py": {
              "additions": [[15, 18], [22, 24]],
              "deletions": [[10, 12]]
            }
          },
          "pr_diff_meta": null
        },
        "extra_data": {
          "analysis_duration": "2.5s",
          "tool_version": "1.0.0"
        }
      },
      "report_object": "5adf3866-844b-4ba9-a7a8-aadebdf60c43/1/20250917-092848-8fa8015f"
    },
    "retries": 0
  }"""
msg = """
{
  "id": "5b64b502-acee-4ce3-a05b-e0853798bd8d",
  "task": "01999e7a-bf77-7962-b7f8-5023c3e00fe6-enki-grpc",
  "kwargs": {
    "flow_id": "01999e7a-bf77-7962-b7f8-5023c3e00fe6",
    "flow_type": "detached_repository_analysis",
    "status": {
      "code": 2000,
      "hmessage": "Detached run completed successfully",
      "err": ""
    }
  },
  "retries": 1
}
"""
msg2 = """
{
"id": "5b64b502-acee-4ce3-a05b-e0853798bd8d",
  "task": "01999e7a-bf77-7962-b7f8-5023c3e00fe6-enki-grpc",
  "kwargs": "KLUv/WBKBG0ZAGY6oiQgcfPz+dDtfD+G23+SkmbXk4kFHsYmS1lShET6+F8NAQQB5AGgAKkAiQCOQxQKV576R/+8Pw9HJkdPifzjTAp9fXh+rWyJCFT+UqsTUcjy9Hl+Ui++Riz6J80IdDCU/sbzXGb3pQJUmAJUHAzKDYyEa33KhBHYXUbAvEN9iTiq7kQqF8pwEDBVQjnDoi1U0jgWlW+Wmm97JunmN+lJ2MSFr/HtbyB/jDGtReWIEWDWNmsrsZjYNdGtbNyUrIGTX9O6fb/4DAHjDsMR0fn7NKeKkKeXiCsSByJGCKlPHYtGwkQE5CNGiC6eRhgUXVhBBUSVC9TN3w4G/SoZoLAzsCxgg0bVkTyFPOxElfenB07tXihcUwYMEI0BxEPDFhwcFiCUSeRQSPIYNAuNRIFUzu3falSD6m2TdlNTqx6PR1OduvFwhRuM9+abXqBq+fcHBeqB6lj4HwkESQZewhSK6uNBUC1RNGH6KyQU4Yg9wjTSeHd2Zs45fMx9k65ji4yxSoy1dc1sv189Bn/G5smf2WTvfVpv2L688ZrL3/Ndd/xKOufmHmPonvv569Va6bygWidXOVu5Ma2arbG5Sv1Lz5l9LW5MJgVZ6k5pbnuMydt/5OcX3UxypZVLrf4XJ/znsJtj67nluuM3fG9l4sRxRneTn2MyJtbsolRxJW4BHUvA1HdoxEQVmkAqfedn8O/Ucc7Z0DlK2Erx7GUp56vW831UKnpqSi5c66rbcuwyuYeMP6Ynl2qPoVpeG3uu15SCcpPqpl7yW/BZ9P5NzLUZZXzWul8u9zIo/fGqdethO0tPDrbo5mtuyukik+2twTndPZUWR7kmbHBJ99p9ny+4PK6XXMGXpCdWAUUoIELDKDMPcnTQMMoqsqX1f4sBphNSawiFsxkvVeMxIc0r/p2N4QUVCMYUX6C6f6tAhRVpsqj7BOEGwzVoT9zJSzjWNMKDaSAYsfYFwvoTAxLokE8gyQzYdCyW7R2Rj7pXPfIPilcOMrxst3xgCl6WPn0CaI1pFBm0+5s2ae+f4eGl9SkrclvMrB83GPTO/9jwq23rzBV8T245sLxXJObMHg==",
  "retries": 1
}
"""

msg3 = b"KLUv/WBKBG0ZAGY6oiQgcfPz+dDtfD+G23+SkmbXk4kFHsYmS1lShET6+F8NAQQB5AGgAKkAiQCOQxQKV576R/+8Pw9HJkdPifzjTAp9fXh+rWyJCFT+UqsTUcjy9Hl+Ui++Riz6J80IdDCU/sbzXGb3pQJUmAJUHAzKDYyEa33KhBHYXUbAvEN9iTiq7kQqF8pwEDBVQjnDoi1U0jgWlW+Wmm97JunmN+lJ2MSFr/HtbyB/jDGtReWIEWDWNmsrsZjYNdGtbNyUrIGTX9O6fb/4DAHjDsMR0fn7NKeKkKeXiCsSByJGCKlPHYtGwkQE5CNGiC6eRhgUXVhBBUSVC9TN3w4G/SoZoLAzsCxgg0bVkTyFPOxElfenB07tXihcUwYMEI0BxEPDFhwcFiCUSeRQSPIYNAuNRIFUzu3falSD6m2TdlNTqx6PR1OduvFwhRuM9+abXqBq+fcHBeqB6lj4HwkESQZewhSK6uNBUC1RNGH6KyQU4Yg9wjTSeHd2Zs45fMx9k65ji4yxSoy1dc1sv189Bn/G5smf2WTvfVpv2L688ZrL3/Ndd/xKOufmHmPonvv569Va6bygWidXOVu5Ma2arbG5Sv1Lz5l9LW5MJgVZ6k5pbnuMydt/5OcX3UxypZVLrf4XJ/znsJtj67nluuM3fG9l4sRxRneTn2MyJtbsolRxJW4BHUvA1HdoxEQVmkAqfedn8O/Ucc7Z0DlK2Erx7GUp56vW831UKnpqSi5c66rbcuwyuYeMP6Ynl2qPoVpeG3uu15SCcpPqpl7yW/BZ9P5NzLUZZXzWul8u9zIo/fGqdethO0tPDrbo5mtuyukik+2twTndPZUWR7kmbHBJ99p9ny+4PK6XXMGXpCdWAUUoIELDKDMPcnTQMMoqsqX1f4sBphNSawiFsxkvVeMxIc0r/p2N4QUVCMYUX6C6f6tAhRVpsqj7BOEGwzVoT9zJSzjWNMKDaSAYsfYFwvoTAxLokE8gyQzYdCyW7R2Rj7pXPfIPilcOMrxst3xgCl6WPn0CaI1pFBm0+5s2ae+f4eGl9SkrclvMrB83GPTO/9jwq23rzBV8T245sLxXJObMHg=="
# for i in range(10):
channel.basic_publish(
    exchange="", routing_key="enki-tmp-q-default-session-id", body=msg3
)
print(f" [x] sent 'message'")

connection.close()
