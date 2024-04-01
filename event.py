# The event that the lambda function receives from the SQS queue is as follows:
import json

event = {'Records': [
    {'messageId': 'f515e061-555f-4d0a-8a67-0807d4dfa833', 
     'receiptHandle': 'AQEBf3QYg0TmSFJd5HBZdbzUcTG2E3zLHMA5kIdY47F5P6M2YjHEuRTG++z/wsje8XhXjp7JUxgKL3Z1+kxPlcTiESZojSxreZx0qkQ1ounpWSHXhpZ7TBreKW/So/ezlsudfZ0L7qpnHvy6WxDYBL3MAezNBf2NdzDP+fQ995vweiw1wfIYrR29A0bKaG0Z7LS5+tSBPEbZfpldJfYLz3wVGf55kKsdfV9Rdqk0r45B3XCzx8vDxLO/fde+gpmbcdbN7XSmPqtaE13uD+dgYE497f2avfx0TWXfpGDtVXGWDjRDvdpyLAC22f6ohhKWPtENE+8Tqw55hLJOskCgPrdWQ36uWxv0Ctjg+6hBsvUrcysi8bKp/i1wCE1TF672mvpZiKwoIsaT7tJNyqiNUQDXaA==', 
     
     'body': '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-east-1","eventTime":"2024-03-30T18:59:47.899Z","eventName":"ObjectCreated:Put","userIdentity":{"principalId":"AWS:AROAXRV4O6ILBWVXIUVVX:i-0a4396d900b746df6"},"requestParameters":{"sourceIPAddress":"34.227.151.244"},"responseElements":{"x-amz-request-id":"269CZ0RBW38RCGSS","x-amz-id-2":"Ou5LA6PpMc0Ai/OhqHGgAWlndCjC0A7A3+jUGJVpLXxMcOAPRkdnuyDJig6Xd/UHeN6kmJfn8B989C9zSySFK4GU6r4JH74R"},"s3":{"s3SchemaVersion":"1.0","configurationId":"SQS_Notif","bucket":{"name":"mybucket-s2038770","ownerIdentity":{"principalId":"A2JT9LIIOSN8JZ"},"arn":"arn:aws:s3:::mybucket-s2038770"},"object":{"key":"IMG_20240212_151946.jpg","size":233274,"eTag":"331cb3fcb77ef34354967294b045ed61","versionId":"Usb5DvMuLNMwVqA9KzwL3.LXz4ZT4bwd","sequencer":"0066086123CEA364EE"}}}]}', 'attributes': {'ApproximateReceiveCount': '2', 'SentTimestamp': '1711825189037', 'SenderId': 'AROA4R74ZO52XAB5OD7T4:S3-PROD-END', 'ApproximateFirstReceiveTimestamp': '1711825489037'}, 'messageAttributes': {}, 'md5OfBody': 'f34fefb17623083c6cb1784767eaac1e', 'eventSource': 'aws:sqs', 'eventSourceARN': 'arn:aws:sqs:us-east-1:519012545046:MyQueueS2038770', 'awsRegion': 'us-east-1'}
    ]}

event2 = {'Records': [
    {'eventID': 'b3296fb1b2d614db0bc56095146c26ea', 
     'eventName': 'INSERT', 
     'eventVersion': '1.1', 
     'eventSource': 'aws:dynamodb', 
     'awsRegion': 'us-east-1', 
     'dynamodb': {
         'ApproximateCreationDateTime': 1711898292.0, 
         'Keys': {'imageName': {'S': 'IMG_20240212_152041.jpg'}}, 
         'NewImage': {'imageName': {'S': 'IMG_20240212_152041.jpg'}, 
                      'image_bucket': {'S': 'mybucket-s2038770'}, 
                      'sourceIP': {'S': '3.82.231.166'}, 
                      'eventTime': {'S': '2024-03-31T15:13:09.491Z'}, 
                      'text_values': {'L': [{'S': '6585'}, {'S': 'OC 11'}, {'S': '6585'}, {'S': 'OC'}, {'S': '11'}]}, 
                      'eventName': {'S': 'ObjectCreated:Put'}, 
                      'label_confidence_scores': {'L': [{'S': '99.9998550415039'}, {'S': '99.9998550415039'}, {'S': '99.9998550415039'}, {'S': '99.50138854980469'}]}, 
                      'label_names': {'L': [{'S': 'Bumper'}, {'S': 'Transportation'}, {'S': 'Vehicle'}, {'S': 'Car'}]}, 
                      'text_confidence_scores': {'L': [{'S': '64.14270782470703'}, {'S': '94.07811737060547'}, {'S': '64.14270782470703'}, {'S': '88.77405548095703'}, {'S': '99.38217163085938'}]}
                      }, 
                      'SequenceNumber': '118400000000079043905270', 
                      'SizeBytes': 466, 
                      'StreamViewType': 'NEW_AND_OLD_IMAGES'
        }, 
        'eventSourceARN': 'arn:aws:dynamodb:us-east-1:519012545046:table/entryTableS2038770/stream/2024-03-31T15:14:36.333'}
        ]}

image_name = event2['Records'][0]['dynamodb']['NewImage']['imageName']['S']