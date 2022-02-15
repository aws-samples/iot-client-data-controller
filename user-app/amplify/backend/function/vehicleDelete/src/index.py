# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import boto3

def handler(event, context):
    print('received event:')
    print(event)
  
    client = boto3.client('iot')
    
    cognito_id = event["requestContext"]["identity"]["cognitoIdentityId"]
    vin_number = event["queryStringParameters"]["vin"]

    length = len(cognito_id)
    cognito_id_short = cognito_id[length - 12 :]
    policy_name = 'pol-' + cognito_id_short + '-' + vin_number

    print("Detach policy...")
    client.detach_policy(
        policyName=policy_name,
        target=cognito_id
    )
    print("Policy detached.")

    print("Delete policy...")
    client.delete_policy(
        policyName=policy_name
    )
    print("Policy deleted.")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps('Vehicle deleted')
    }