from django.db.models.signals import post_delete
from django.dispatch import receiver

from kreddb import models


# TODO Если в этом методе будет ошибка, транзакция будет откачена!!!
@receiver(post_delete, sender=models.GenerationImage)
def generation_image_post_delete(instance: models.GenerationImage, **kwargs):
    storage, path = instance.image.storage, instance.image.path
    storage.delete(path)
    original_path = path.rsplit('.')
    for sz, _ in models.IMAGE_SIZES.items():
        storage.delete(original_path[0] + '_' + sz + '.' + original_path[1])
