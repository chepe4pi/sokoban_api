from sk_core.serializer import BaseModelSerializer
from ..models import Skins


class SkinSerializer(BaseModelSerializer):

    class Meta:
        model = Skins
        fields = '__all__'
