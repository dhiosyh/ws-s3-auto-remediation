import boto3
import json

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    sns_client = boto3.client('sns') # Agen untuk kirim email instan
    
    bucket_name = 'data-rahasia-kelompokku-123'
    # ARN SNS tujuan notifikasi darurat
    sns_topic_arn = 'arn:aws:sns:us-east-1:005445459855:S3-Activity-Notification' 
    
    try:
        # Aksi 1: Membuka gembok S3 (Simulasi Kebocoran Data)
        s3_client.put_public_access_block(
            Bucket=bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
        )
        
        # Aksi 2: Menyebarkan peringatan darurat seketika via SNS
        pesan_darurat = f"PERINGATAN DARURAT: Gembok Public Access pada bucket {bucket_name} telah dimatikan (OFF) oleh Breaker!"
        sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="ALARM: S3 Terbuka Ke Publik!",
            Message=pesan_darurat
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Breaker sukses membuka gembok dan email peringatan telah dikirim!')
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Gagal mengeksekusi: {str(e)}')
        }
