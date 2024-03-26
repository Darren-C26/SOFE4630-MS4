from google.cloud import pubsub_v1
import json

# Configure Pub/Sub settings
project_id = "your-project-id"
subscription_id = "filter-subscription"
topic_id = "filtered_meter_readings"
credentials_path = "credentials.json"

subscriber = pubsub_v1.SubscriberClient.from_service_account_file(credentials_path)
topic_path = subscriber.topic_path(project_id, topic_id)
subscription_path = subscriber.subscription_path(project_id, subscription_id)

# Callback function to handle incoming messages
def callback(message):
    data = json.loads(message.data.decode("utf-8"))
    if all(val is not None for val in data.values()):
        # Publish filtered message to new topic
        publisher = pubsub_v1.PublisherClient.from_service_account_file(credentials_path)
        filtered_message = json.dumps(data)
        publisher.publish(topic_path, filtered_message.encode("utf-8"))
        message.ack()

# Subscribe to the original topic
subscriber.subscribe(subscription_path, callback=callback)
