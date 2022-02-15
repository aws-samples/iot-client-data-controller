# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import json
import os

def handler(event, context):

    client = boto3.client('iot')

    runtime_region = os.environ['AWS_REGION']
    runtime_account_id = context.invoked_function_arn.split(":")[4]

    # input start
    cognito_id = event["requestContext"]["identity"]["cognitoIdentityId"]
    vin_number = event["queryStringParameters"]["vin"]
    # input end

    length = len(cognito_id)
    cognito_id_short = cognito_id[length - 12 :]
    policy_name = 'pol-' + cognito_id_short + '-' + vin_number

    # subscribe  $aws/things/" + this.vin_number + "/shadow/name/" + this.vin_number + "/get
    # publish    $aws/things/" + vin + "/shadow/name/" + vin + "/get/accepted
    # publish    $aws/things/" + this.vin_number + "/shadow/name/" + this.vin_number + "/update
    policy_json = {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Action": "iot:Connect",
        "Resource": "arn:aws:iot:" + runtime_region + ":" + runtime_account_id + ":*",
        "Effect": "Allow"
        },
        {
        "Action": "iot:Subscribe",
        "Resource": "arn:aws:iot:" + runtime_region + ":" + runtime_account_id + ":topicfilter/$aws/things/" + vin_number + "/shadow/name/" + vin_number + "/*",
        "Effect": "Allow"
        },
        {
        "Action": "iot:Publish",
        "Resource": "arn:aws:iot:" + runtime_region + ":" + runtime_account_id + ":topic/$aws/things/" + vin_number + "/shadow/name/" + vin_number + "/*",
        "Effect": "Allow"
        },
        {
        "Action": "iot:Receive",
        "Resource": "arn:aws:iot:" + runtime_region + ":" + runtime_account_id + ":topic/$aws/things/" + vin_number + "/shadow/name/" + vin_number + "/*",
        "Effect": "Allow"
        }
    ]
    }

    # create policy
    print("Create policy...")
    policy = client.create_policy(
        policyName=policy_name,
        policyDocument=json.dumps(policy_json)
    )
    print("Policy created.")

    # attach policy
    print("Attach policy...")
    response = client.attach_policy(
        policyName=policy_name,
        target=cognito_id
    )
    print("Policy attached.")
  
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Vehicle created')
    }