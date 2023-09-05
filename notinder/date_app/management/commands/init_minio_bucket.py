from django.core.management.base import BaseCommand
import boto3
from decouple import config

class Command(BaseCommand):
    help = 'Create a Minio bucket if it does not exist'

    def handle(self, *args, **kwargs):
        minio_access_key = config('MINIO_ROOT_USER')
        minio_secret_key = config('MINIO_ROOT_PASSWORD')

        minio_client = boto3.client('s3',
            endpoint_url='http://minio:9000',  # URL-адрес Minio-сервера и порт.
            aws_access_key_id=minio_access_key,
            aws_secret_access_key=minio_secret_key,
        )

        bucket_name = 'photo'

        if not minio_client.list_buckets()['Buckets']:
            minio_client.create_bucket(Bucket=bucket_name)

        self.stdout.write(self.style.SUCCESS(f'Bucket "{bucket_name}" created successfully.'))