__author__ = 'Djidiouf'

# Python built-in modules
import configparser
import os

# Third-party modules
import boto3
from botocore.exceptions import ClientError

# Project modules
import modules.connection


# Read config
config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better


def receive_message():
    sqs = boto3.resource('sqs')

    # Get the queue
    queue = sqs.get_queue_by_name(QueueName=config['aws']['sqs_queue'])

    # Process messages by printing out body and optional author name
    messages = queue.receive_messages(MessageAttributeNames=['Author'], MaxNumberOfMessages=10, WaitTimeSeconds=0)

    for message in messages:
        # Get the custom author message attribute if it was set
        author_text = 'None'
        if message.message_attributes is not None:
            author_name = message.message_attributes.get('Author').get('StringValue')
            if author_name:
                author_text = '{0}'.format(author_name)

        # Print out the body and author (if set)
        current_message = message.body.splitlines() # Split string when \n \r\n is detected
        for line in current_message:
            # print('[{0}]: {1}'.format(author_text, line))
            modules.connection.send_message('[{0}]: {1}'.format(author_text, line))

        # Let the queue know that the message is processed
        message.delete()


def main():
    receive_message()
