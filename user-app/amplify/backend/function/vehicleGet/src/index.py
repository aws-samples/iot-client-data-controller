# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import json
import boto3

def handler(event, context):
    client = boto3.client('iot')

    cognito_id = event["requestContext"]["identity"]["cognitoIdentityId"]
    print(cognito_id)
    response=client.list_principal_policies(
        principal=cognito_id
    )

    vin_numbers = []
    for policy in response['policies']:
        policy_name = policy['policyName']
        length = len(policy_name)
        vin_number = policy_name[length - 17 :]
        vin_numbers.append(vin_number)

    print(vin_numbers)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': '*',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(vin_numbers)
    }