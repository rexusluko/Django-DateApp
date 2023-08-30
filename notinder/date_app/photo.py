import uuid

from minio import Minio

base_url = 'minio:9000'
minio_client = Minio(
    base_url,
    access_key='admin',
    secret_key='password',
    secure=False
)
bucket = 'photo'


def save_photo_to_minio(photo):
    unique_filename = str(uuid.uuid4())
    minio_client.put_object(bucket, unique_filename, photo, len(photo), content_type='image/png')
    return unique_filename


def load_photo_from_minio(photo_path):
    photo = minio_client.get_object(bucket, photo_path)
    return photo.data
