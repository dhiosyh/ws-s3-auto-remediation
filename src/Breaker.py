import boto3
import json
import time

def lambda_handler(event, context):
    BUCKET_NAME = 'data-rahasia-kelompokku-123'
    s3 = boto3.client('s3')
    
    try:
        # 1. Matikan semua "Block Public Access"
        s3.put_public_access_block(
            Bucket=BUCKET_NAME,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False, 'IgnorePublicAcls': False,
                'BlockPublicPolicy': False, 'RestrictPublicBuckets': False
            }
        )
        time.sleep(2)
        
        # 2. Pasang Policy "Public Read" (Simulasi Kebocoran)
        public_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": "*",
                "Action": "s3:GetObject",
                "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
            }]
        }
        s3.put_bucket_policy(Bucket=BUCKET_NAME, Policy=json.dumps(public_policy))
        return {'statusCode': 200, 'body': json.dumps('Celah Keamanan Terbuka!')}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}