from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PartialUpdateMixin(ModelViewSet):
    def update(self, request, *args, **kwargs):
        return super(PartialUpdateMixin, self).update(request, partial=True)
