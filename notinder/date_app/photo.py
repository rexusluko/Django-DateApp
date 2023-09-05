from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import uuid

def save_photo_to_minio(photo):
    unique_filename = str(uuid.uuid4())
    file_content = ContentFile(photo.read())
    default_storage.save(unique_filename, file_content)
    return unique_filename

def load_photo_from_minio(photo_path):
    return default_storage.open(photo_path).read()
