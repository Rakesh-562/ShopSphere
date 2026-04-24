import pika
import json
import logging

logger = logging.getLogger(__name__)

def publish_order_event(order):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )
        channel = connection.channel()

        # Defining a topic exchange as per D6/D8 architecture
        channel.exchange_declare(exchange='shopsphere_events', exchange_type='topic')

        message = {
            "order_id": order.id,
            "status": "created",
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                }
                for item in order.items.all()
            ],
        }

        # Publishing to 'order.created' topic
        channel.basic_publish(
            exchange='shopsphere_events',
            routing_key='order.created',
            body=json.dumps(message)
        )
        
        logger.info(f"Published order.created for Order {order.id}")
        connection.close()
    except pika.exceptions.AMQPConnectionError:
        logger.error("RabbitMQ is not running. Could not publish order event.")
