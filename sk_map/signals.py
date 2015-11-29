from django.db.models.signals import post_save
from .models import Map, Wall, Box, Point, Men
from sk_core.signals import set_child_models_attrs
from django.db.models.signals import post_save
from functools import partial


models = [Wall, Box, Point, Men]
attrs = ['owner', 'public']
sender = Map

post_save.connect(receiver=partial(set_child_models_attrs, models=models, attrs=attrs),\
                          sender=Map, dispatch_uid='set_child_models_attrs', weak=False)
