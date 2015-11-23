from rest_framework.viewsets import ModelViewSet


class BaseModelViewSet(ModelViewSet):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
