from rest_framework import serializers


class DataCenterSerializer(serializers.Serializer):
    name = serializers.CharField()
    servers = serializers.IntegerField(min_value=1)

class DevOpsSerializer(serializers.Serializer):
    DM_capacity = serializers.IntegerField(min_value=1)
    DE_capacity = serializers.IntegerField(min_value=1)
    data_centers = DataCenterSerializer(many=True, allow_empty=False)