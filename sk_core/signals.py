
def set_child_models_attrs(sender, models, attrs, **kwargs):
    for attr in attrs:
        value = getattr(kwargs['instance'], attr)
        for model in models:
            instances = model.objects.filter(map=kwargs['instance'])
            for instance in instances:
                setattr(instance, attr, value)
                instance.save()
