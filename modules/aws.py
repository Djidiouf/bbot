__author__ = 'Djidiouf'

# Python built-in modules
import configparser
import os
import json

# Third-party modules
import boto3
from botocore.exceptions import ClientError

# Project modules
import modules.connection


class MyExceptionAWSInProgress(Exception):
    """Raise for my specific kind of exception"""
    pass

def lambda_run(i_args):
    results = "Not implemented"
    return results


def asg_desired_capacity(i_string):
    tuple_string = i_string.partition(' ')
    requested_server = tuple_string[0]
    requested_capacity = tuple_string[2]

    # Read config
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'config.cfg'))  # Absolute path is better

    # Establish real server name
    if requested_server == "teamspeak":
        requested_server = config['aws']['teamspeak_asg']
    else:
        results = "Error: The value %s is invalid" % (requested_server)
        return results

    # Establish requested capacity
    if requested_capacity == 'on' or requested_capacity == 'up' or requested_capacity == '1':
        requested_capacity = 1
    elif requested_capacity == 'off' or requested_capacity == 'down' or requested_capacity == '0':
        requested_capacity = 0
    else:
        results = "Error: The value %s is invalid" % (requested_capacity)
        return results

    # Run command
    client = boto3.client('autoscaling')
    try:
        results = client.set_desired_capacity(
            AutoScalingGroupName=requested_server,
            DesiredCapacity=requested_capacity,
            HonorCooldown=True,
        )
        print(results)
        if results['ResponseMetadata']['HTTPStatusCode'] == 200:
            results = "A request to change the %s desired capacity to %s has been issued" % (requested_server, requested_capacity)
            return results
        else:
            results = "Error: Unexpected"
            return results

    except ClientError as e:
        print(e.response['Error']['Code'])
        if e.response['Error']['Code'] == 'ScalingActivityInProgress':
            raise MyExceptionAWSInProgress("A Scaling activity is already in progress for %s" % requested_server)
        else:
            raise e


def aws(i_string):
    tuple_string = i_string.partition(' ')
    sub_cmd = tuple_string[0]
    sub_arg = tuple_string[2]

    if sub_cmd == "asg":
        aws_results = asg_desired_capacity(sub_arg)
        return aws_results
    elif sub_cmd == "lambda":
        aws_results = lambda_run(sub_arg)
        return aws_results


def main(i_string, i_medium, i_alias=None):
    try:
        aws_results = aws(i_string.lower())
        modules.connection.send_message("%s" % aws_results, i_medium, i_alias)

    except MyExceptionAWSInProgress as e:
        modules.connection.send_message("%s" % e.args, i_medium, i_alias)
        return
