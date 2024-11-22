import logging
import argparse
from kafka import KafkaProducer
import json

class BaseProducer:
    # Class-level variable for logging level
    log_level = "ERROR"

    def __init__(self, bootstrap_servers):
        # Ensure CLI args are parsed only once
        if not hasattr(BaseProducer, "_cli_parsed"):
            BaseProducer.parse_cli_args()
            BaseProducer._cli_parsed = True

        # Set up logging
        self.logger = self.setup_logging(BaseProducer.log_level)
        self.logger.info("Initializing Kafka producer...")

        # Initialize Kafka producer
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.logger.info("Kafka producer initialized.")

    @classmethod
    def setup_logging(cls, log_level):
        """Set up logging configuration."""
        logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')
        return logging.getLogger(cls.__name__)

    @classmethod
    def parse_cli_args(cls):
        """Parse CLI arguments for log level."""
        parser = argparse.ArgumentParser(description="Kafka Producer with parameterized logging.")
        parser.add_argument(
            "--log-level", 
            default=cls.log_level, 
            choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], 
            help="Set the logging level (default: ERROR)"
        )
        args = parser.parse_args()
        cls.log_level = args.log_level.upper()

    def send_message(self, topic, data_sources):
        """Send a message to Kafka."""
        try:
            formatted_message = self.format_message(data_sources)
            self.producer.send(topic, value=formatted_message)
            self.producer.flush()
            self.logger.info(f"Message sent to topic '{topic}': {formatted_message}")
        except Exception as e:
            self.logger.error(f"Failed to send message to topic '{topic}': {e}")

    def format_message(self, data_sources):
        """Format a message. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement the 'format_message' method")

    def __del__(self):
        self.logger.info("Closing Kafka producer...")
        self.producer.close()
        self.logger.info("Kafka producer closed.")

class ChildProducer(BaseProducer):
    def format_message(self, data):
        """Format message for 'user_activity'."""
        return data


if __name__ == "__main__":
    BOOTSTRAP_SERVERS = ""

    # Initialize the producer
    cProducer = ChildProducer(BOOTSTRAP_SERVERS)
    data = {
        "user_id": "Hey",
        "action": "login"
    }

    # Send messages
    cProducer.send_message("astaad", data)
    data["action"] = 'logout'
    cProducer.send_message("astaad", data)
