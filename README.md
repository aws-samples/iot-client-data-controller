# IoT Client Data Controller

## Motivation

This solution could be applied to different industries and use cases, but we are focusing on the concrete example of connected vehicles, with the following reasoning.

The number of connected vehicles will increasing trastically over the next years. These will produce and immense and constant stream of data. The topic of ownership of this data has not reached a conclusion and when it eventually does, regulations will vary by country.
Companies have understood the power and leverage laying in the information stored in their connected vehicle data lakes. There is additional revenue in it and new product features to build. But also the consumers become more aware of their rights in regards to data and privacy and eventually will disapprove that global cooperations make money with the bits and bytes produced by vehicles entirely owned by the consumer, fuelled by electricity paid by them.

Therefore a definite differentiator for a car manufacturer would be to give full ownership and control over his connected vehicle data back to the consumer and include him in the value generation.
Costumers will associate this very positive with the brand, proving that it is customer-centric and can be trusted. Especially the purchase of a car is still emotionally driven and all about identification with a brand image. 

## Solution

The following solution shows how technically a vehicle owner could control the data flow from his vehicles towards the OEM. 
AWS IoT Greengrass v2 will act as gateway in the vehicle and different functionalities will be running as components there. Resulting in these categories: 1/ Diagnostics Trouble Code; 2/ Trip Data; 3/ Telemetry.
In the corresponding connected car app the user can configure which of these categories should share its data to which extent and for which purpose.
Once the data is sent and accepted in AWS IoT Core it can be further processed following for example the [AWS  solution for Connected Vehicles](https://aws.amazon.com/solutions/implementations/aws-connected-vehicle-solution/)

This solution will setting up the following architecture.

![alt text](images/architecture.png?raw=true)

Start with downloading the solution with cloning it from this repository

    git clone https://github.com/aws-samples/iot-client-data-controller
    cd iot-client-data-controller

### User App Setup

The user app frontend is built using Vue.js, connected to a backend running Python functions. We will be using AWS Amplify, to easily get this hosted on cloud and make use of pre-built authentication, etc.

How to get started with AWS Amplify is described [here](https://docs.amplify.aws/start/getting-started/installation/q/integration/vue/). We will start getting Amplify installed and configured using the following commands:

    npm install -g @aws-amplify/cli
    
    amplfiy configure

Once done you can go into the user-app folder and initialize your Amplify instance.

    cd user-app
    amplify init

**Provide the below reponses.**
**Note:** In the below, ensure the selected AWS profile has a default AWS Region specified to determine where the application will be deployed.

? Enter a name for the environment **dev**

? Choose your default editor: **[... your prefered Editor ...]**

? Select the authentication method you want to use: **AWS profile**

? Please choose the profile you want to use: **[Select Preferred AWS Profile]**

You should see the following success messages and can ignore any errors:

✔ Successfully created initial AWS cloud resources for deployments.
✔ Initialized provider successfully.


### Infrastructure Setup

To deploy necessary AWS services like IoT Policies go to the AWS Console and Search for CloudFormation.
Here under Stack click on `Create Stack` and With new resources (standard).

![alt text](images/cloudformation.png?raw=true)

Select `Template is ready`, `Upload a template file` and click `Choose file`. In the openining dialog select *backend > IotCdkStack.template.json* of this repository. Click `Next`, enter any name for the stack, click `Next` twice, acknowledge that Cloudformation is creating IAM resources and `Create stack`.

It will take a few minutes until the stack will show with the status `CREATE_COMPLETE` after which you can proceed.

Once this deployment is complete please run the following AWS CLI command 

    aws lambda add-permission \
    --function-name ConnectedVehicle-AdjustPolicies-Lambda \
    --region <YOUR_REGION> --principal iot.amazonaws.com \
    --source-arn arn:aws:iot:<YOUR_REGION>:<YOUR_ACCOUNT_ID>:rule/ConnectedVehiclePolicyUpdate \
    --source-account <YOUR_ACCOUNT_ID> \
    --statement-id <ANY_RANDOM_NUMBER> --action "lambda:InvokeFunction"

This infrastructure stack contains the following:
1. IoT Policies for Vehicle: which allow a thing to receive MQTT messages from a specific data. Initially when a new vehicle is registered with AWS IoT core, none of these policies is attached to the thing. This will only happen once requested via the user app and only then data can flow through.

2. Lambda function `ConnectedVehicle-AdjustPolicy` to control, which policies are attached to which device and therefore which data will be accepted.

3. The Lambda function requires certain permissions, which are granted via an attached role having the following permissions attached iot:UpdateThingShadow, iot:DetachPolicy, iot:AttachPolicy, iot:ListThingPrincipals

4. IoT Rule `ConnectedVehiclePolicyUpdate` which, detects the updates made to the shadow using the following rule query

    SELECT topic(3) as vin, state.desired FROM '$aws/things/+/shadow/name/+/update/accepted'

This will trigger the lambda function mentioned above and provide the following format of data

    {'vin': '1HGBH41JXMN109186', 'desired': {'trip_bool': False, 'dtc_bool': True, 'telemetry_bool': False}}


### Enable MQTT Messaging for User App

1. In the file *user-app > src > main.js* the following code must be adjusted

    Amplify.addPluggable(new AWSIoTProvider({
      aws_pubsub_region: '[...Region of your AWS IoT Core, e.g. ap-southeast-1...]',
      aws_pubsub_endpoint: 'wss://[...Device data endpoint found in IoT Core > Settings, e.g. a23lushfl3457z-ats.iot.ap-south-1.amazonaws.com...]/mqtt',
    }));

2. Then please navigate to the CloudFormation service and look for a in the main stack `amplify-userapp-dev-XXXXXX`, select it and under the tab `Resources` you will find a resource named `AuthRole` of type `AWS::IAM::Role`. Please click on this Physical ID, which will take you to the IAM service.

Click Attached Policies and add `AWSIoTDataAccess` and `AWSIoTConfigAccess`.


### Publish

Then everything should be pushed from your local machine to the cloud using

    npm install
    amplify push

And eventually host the frontend so it can be access via the internet

    amplify hosting add

? Select the plugin module to execute: **Hosting with Amplify Console**

? Choose a type **Manual deployment**

    amplify publish
    

## Testing the solution

Now that everything is in place to control the incoming data, we can simulate it using a dummy vehicle.

### Adding thing manually

Within IoT Core you can add a Thing manually and assign a named shadow to it. Important is that these should have the exact VIN, which you entered in the app.

![alt text](images/create_thing.png?raw=true)

In the beginning this would not have any policies assigned to it besides `Connect`.

![alt text](images/connect_policy.png?raw=true)

### Using Greengrass

We could also deploy GreengrassV2 to a suitable device and deploy components there. 

Follow the [GreengrassV2 installation](https://docs.aws.amazon.com/greengrass/v2/developerguide/getting-started.html) for example on a Raspberry Pi or an Cloud9 instance. 

During the setup there is one command which triggers the installation of GreengrassV2 on the device and the creation of the respective assets on AWS IoT Hub. Here you will be able to set the thing name (`--thing-name`) and group (`--thing-group-name`) for the device on AWS. In our example a VIN number shall be the name and it should be in the group vehicles. It is also important to keep attached the **Connect** policy via `--thing-policy-name`. So that 

    sudo -E java -Droot="/greengrass/v2" -Dlog.store=FILE \
      -jar ./GreengrassInstaller/lib/Greengrass.jar \
      --aws-region [...region...] \
      --thing-name 1HGBH41JXMN109186 \
      --thing-group-name Vehicles \
      --thing-policy-name Connect \
      --tes-role-name GreengrassV2TokenExchangeRole \
      --tes-role-alias-name GreengrassCoreTokenExchangeRoleAlias \
      --component-default-user ggc_user:ggc_group \
      --provision true \
      --setup-system-service true \
      --deploy-dev-tools true

Back in the AWS console under IoT Core, you will find a thing created, in this example with the name 1HGBH41JXMN109186. If you select it and navigate to `Device Shadows`, click on `Create Shadow`.

![alt text](images/createshadow.png?raw=true)

Select `Named Shadow` and as the Device Shadow name enter the same as the thing name (in this example 1HGBH41JXMN109186).

Here you can [create components](https://docs.aws.amazon.com/greengrass/v2/developerguide/ipc-iot-core-mqtt.html) that simulate the communication with IoT Core.

In the current implementation the following data categories are set up.
| Data content | MQTT topic | Related IoT Policy |
| --- | --- | --- |
| Aggregated trip data | connectedcar/trip/# | PublishTripData |
| Diagnostics trouble codes | connectedcar/dtc/# | PublishDiagnosticsTroubleCodes |
| Telematics data | connectedcar/telemetry/# | PublishTelemetry |

## Outlook

Now the vehicle owner has control over which data is processed further. But it is still up to the platform owner (i.e. automotive OEM), which options are presented to the customer. One aspiring thought is to include the customer into the data value chain. So the vehicle owner could agree for his anonymized data to be published, for which in return a share of data revenue will be paid. Similar approaches already exist for browsers like for example https://gener8ads.com/. This would limit the amount of revenue the OEM would generate with the data, but it would be a real brand differentiator.

### Solution Outline

A possible implementation for this could happen using Web 3.0 frameworks, where ownership and entitlement to use assets are controlled with blockchain technology.

#### Layer 1: Data Lake storing data
As in the AWS Connected Vehicle Solution, this is a combination of S3 buckets and DynamoDB tables, where data is properly partitioned and life-cycle policies are activated to keep the data only as long as defined by the customer.

#### Layer 2: Compute-to-Data environment
On top of this compute layer can be established, which already has the Web 3.0 integrations included. An existing example for this setup can be found with the [Ocean Protocol](https://docs.oceanprotocol.com/tutorials/compute-to-data/).

#### Layer 3: Algorithm
Running on this Compute-to-Data environment, an [algorithm](https://docs.oceanprotocol.com/tutorials/compute-to-data-algorithms/) is running, which turns the stored data into consumable output. 

#### Layer 4: Data Marketplace
Finally through a data marketplace the usage of these algorithms could be published and consumed. All with an underlaying exchange of tokens to facilitate the transactions.


## License Summary

This sample code is made available under the MIT-0 license. See the LICENSE file.

Sample car picture (car.png) taken from Wikipedia under CC BY-SA 4.0 license.
https://en.wikipedia.org/wiki/Lamborghini#/media/File:Lamborghini_Urus_IMG_2640.jpg


