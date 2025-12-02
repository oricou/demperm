from rest_framework import serializers


class StatsDailyField(serializers.Serializer):
    date = serializers.DateField()
    count = serializers.IntegerField()

class StatsDailySerializer(serializers.Serializer):
    userId = serializers.UUIDField()
    daily = serializers.ListField(child=StatsDailyField())
    delta = serializers.IntegerField()

class StatsMonthlyField(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    count = serializers.IntegerField()

class StatsMonthlySerializer(serializers.Serializer):
    userId = serializers.UUIDField()
    monthly = serializers.ListField(child=StatsMonthlyField())
    delta = serializers.IntegerField()


class StatsChartDomainField(serializers.Serializer):
    userId = serializers.UUIDField()
    votes = serializers.ListField(child=StatsDailyField())

class StatsChartSerializer(serializers.Serializer):
    domain = serializers.CharField()
    users = serializers.ListField(child=StatsChartDomainField())
