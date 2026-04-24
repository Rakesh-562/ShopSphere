import pika
import json

def reduce_stock(product_id, quantity):
    # replace this with your DB logic
    print(f"Reducing stock for product {product_id} by {quantity}")

def callback(ch, method, properties, body):
    event = json.loads(body)

    print("Received event:", event)

    for item in event["items"]:
        product_id = item["product_id"]
        qty = item["quantity"]

        reduce_stock(product_id, qty)

def start_consumer():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
    except pika.exceptions.AMQPConnectionError as exc:
        print("RabbitMQ is not running on localhost:5672 or refused the connection.")
        raise exc

    channel = connection.channel()

    channel.exchange_declare(exchange='shopsphere_events', exchange_type='topic')
    channel.queue_declare(queue='order_created')
    channel.queue_bind(
        exchange='shopsphere_events',
        queue='order_created',
        routing_key='order.created',
    )

    channel.basic_consume(
        queue='order_created',
        on_message_callback=callback,
        auto_ack=True
    )

    print("Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
