from django.core.files.storage import default_storage


def load_photo_from_minio(photo_path):
    return default_storage.open(photo_path).read()
