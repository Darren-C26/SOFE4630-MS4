from google.cloud import pubsub_v1
import json

# Configure Pub/Sub settings
project_id = "your-project-id"
subscription_id = "convert-subscription"
topic_id = "converted_meter_readings"
credentials_path = "credentials.json"

subscriber = pubsub_v1.SubscriberClient.from_service_account_file(credentials_path)
topic_path = subscriber.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)


# Callback function to handle incoming messages
def callback(message):
    data = json.loads(message.data.decode("utf-8"))
    data['Pressure_psi'] = data['pressure'] / 6.895
    data['Temperature_F'] = data['temperature'] * 1.8 + 32
    converted_message = json.dumps(data)

    # Publish converted message to new topic
    publisher = pubsub_v1.PublisherClient.from_service_account_file(credentials_path)
    publisher.publish(topic_path, converted_message.encode("utf-8"))
    message.ack()


# Subscribe to the filtered topic
subscriber.subscribe(subscription_path, callback=callback)
