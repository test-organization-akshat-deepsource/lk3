import pika
import json
import logging
from typing import Dict
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class RMQModelUsage(BaseModel):
    input: float
    cached_input: float
    output: float


class RMQUsageTaskMessage(BaseModel):
    id: str
    task: str
    kwargs: Dict[str, RMQModelUsage]
    retries: int


class RMQUsageConsumer:
    def __init__(self, exchange: str, routing_key: str, queue: str):
        self.exchange = exchange
        self.routing_key = routing_key
        self.queue = queue
        self._connection = None
        self._channel = None

    def connect(self):
        self._connection = pika.BlockingConnection()
        self._channel = self._connection.channel()

        # Declare exchange and queue
        self._channel.exchange_declare(exchange=self.exchange, exchange_type="direct")
        self._channel.queue_declare(queue=self.queue)
        self._channel.queue_bind(
            exchange=self.exchange, queue=self.queue, routing_key=self.routing_key
        )

    def callback(self, ch, method, properties, body):
        try:
            # Parse the message
            message_data = json.loads(body)
            usage_message = RMQUsageTaskMessage(**message_data)

            print(f"\n=== CONSUMED MESSAGE ===")
            print(f"Raw body: {body.decode()}")
            print(f"Task: {usage_message.task}")
            print(f"ID: {usage_message.id}")
            print(f"Retries: {usage_message.retries}")

            logger.info(
                f"Received usage data for task {usage_message.task} with ID {usage_message.id}"
            )

            # Process the usage data
            for model_name, usage_data in usage_message.kwargs.items():
                print(f"Model: {model_name}")
                print(f"  Input tokens: {usage_data.input}")
                print(f"  Cached input tokens: {usage_data.cached_input}")
                print(f"  Output tokens: {usage_data.output}")

                logger.info(f"Model: {model_name}")
                logger.info(f"  Input tokens: {usage_data.input}")
                logger.info(f"  Cached input tokens: {usage_data.cached_input}")
                logger.info(f"  Output tokens: {usage_data.output}")

                # Add your processing logic here
                # e.g., store in database, aggregate metrics, etc.

            print(f"=========================\n")

            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        except Exception as e:
            print(f"ERROR: Failed to process message: {e}")
            logger.error(f"Error processing message: {e}")
            # Reject the message and don't requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

    def start_consuming(self):
        self.connect()
        self._channel.basic_consume(queue=self.queue, on_message_callback=self.callback)

        logger.info("Starting to consume messages. To exit press CTRL+C")
        try:
            self._channel.start_consuming()
        except KeyboardInterrupt:
            self._channel.stop_consuming()
            self._connection.close()


if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    # Configure these based on your settings
    EXCHANGE = "exchange"
    ROUTING_KEY = "key"
    QUEUE = "queue"

    consumer = RMQUsageConsumer(EXCHANGE, ROUTING_KEY, QUEUE)
    consumer.start_consuming()
