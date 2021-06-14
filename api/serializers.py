from rest_framework.serializers import ModelSerializer, CharField
from .models import Exchange, UserAccess

class ExchangeSerializer(ModelSerializer):
    origin = CharField(source='get_origin_display')

    class Meta:
        model = Exchange
        fields = ('id', 'origin', 'value', 'created')
        ref_name = 'Exchange'


class UserAccessSerializer(ModelSerializer):
    
    class Meta:
        model = UserAccess
        fields = ('id', 'user', 'created')
        ref_name = 'UserAccess'

