from rest_framework import serializers


class DataCenterSerializer(serializers.Serializer):
    name = serializers.CharField()
    servers = serializers.IntegerField()

    def validate_servers(self, obj):
        if obj <= 0:
            raise serializers.ValidationError("servers must be greater than 0")
        return obj


class DevOpsSerializer(serializers.Serializer):
    DM_capacity = serializers.IntegerField()
    DE_capacity = serializers.IntegerField()
    data_centers = DataCenterSerializer(many=True)

    def validate_DM_capacity(self, obj):
        if obj <= 0:
            raise serializers.ValidationError("DM_capacity must be greater than 0")
        return obj

    def validate_DE_capacity(self, obj):
        if obj <= 0:
            raise serializers.ValidationError("DE_capacity must be greater than 0")
        return obj

    def validate_data_centers(self, obj):
        if len(obj) == 0:
            raise serializers.ValidationError("data_centers length must be greater than 0")
        return obj
