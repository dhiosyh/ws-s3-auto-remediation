import boto3
import json

def lambda_handler(event, context):
    BUCKET_NAME = 'data-rahasia-kelompokku-123'
    s3 = boto3.client('s3')
    
    try:
        # 1. Pasang kembali gembok "Block Public Access"
        s3.put_public_access_block(
            Bucket=BUCKET_NAME,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True, 'IgnorePublicAcls': True,
                'BlockPublicPolicy': True, 'RestrictPublicBuckets': True
            }
        )
        # 2. Hapus Bucket Policy yang membocorkan data
        s3.delete_bucket_policy(Bucket=BUCKET_NAME)
        return {'statusCode': 200, 'body': json.dumps('Keamanan dipulihkan!')}
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps(str(e))}