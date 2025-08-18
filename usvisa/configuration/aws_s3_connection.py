import os
import boto3

from usvisa.constants import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION

class S3Client:
    s3_client = None
    s3_resource = None

    def __init__(self, region_name = AWS_REGION):
        """
        Initialize the S3 client and resource with the provided AWS credentials and region.
        """
        if S3Client.s3_resource == None or S3Client.s3_client == None:
            __access_key_id = os.getenv(AWS_ACCESS_KEY_ID, )
            __secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY)

            if __access_key_id is None:
                raise Exception(f"Environment variable: {AWS_ACCESS_KEY_ID} is not not set.")
            if __secret_access_key is None:
                raise Exception(f"Environment variable: {AWS_SECRET_ACCESS_KEY} is not set.")
            
            # Initialize the S3 client and resource with the provided credentials
            # S3 client is used for operations like uploading files
            S3Client.s3_resource = boto3.resource('s3',
                                                  aws_access_key_id = __access_key_id,
                                                  aws_secret_access_key = __secret_access_key, 
                                                  region_name = region_name)
            # S3 resource is used for operations like listing buckets
            S3Client.s3_client = boto3.client('s3',
                                              aws_access_key_id = __access_key_id,
                                              aws_secret_access_key = __secret_access_key, 
                                              region_name = region_name)
            
        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client
