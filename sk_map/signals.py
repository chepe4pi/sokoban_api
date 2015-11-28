from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Map, Wall, Box, Point, Men

models = [Wall, Box, Point, Men]
attrs = ['owner', 'public']


@receiver(post_save, sender=Map, dispatch_uid='set_attributes_to_aggrigable_models')
def handler(sender, **kwargs):
    print('got')
    for attr in attrs:
        value = getattr(kwargs['instance'], attr)
        for model in models:
            instances = model.objects.filter(map=kwargs['instance'])
            for instance in instances:
                setattr(instance, attr, value)
                instance.save()
