from rest_framework import serializers


class StatsDailyPointSerializer(serializers.Serializer):
    date = serializers.DateField()
    count = serializers.IntegerField()

class StatsMonthlyPointSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    count = serializers.IntegerField()

class StatsDailyDomainSerializer(serializers.Serializer):
    domain = serializers.CharField()
    series = StatsDailyPointSerializer(many=True)

class StatsMonthlyDomainSerializer(serializers.Serializer):
    domain = serializers.CharField()
    series = StatsMonthlyPointSerializer(many=True)

class StatsDailySerializer(serializers.Serializer):
    userId = serializers.CharField()
    byDomain = StatsDailyDomainSerializer(many=True)
    monthlyByDomain = StatsMonthlyDomainSerializer(
        many=True,
        required=False,
        allow_null=True
    )

class StatsMonthlySerializer(serializers.Serializer):
    userId = serializers.CharField()
    monthlyByDomain = StatsMonthlyDomainSerializer(many=True)

class StatsChartDomainField(serializers.Serializer):
    userId = serializers.CharField()
    votes = serializers.ListField(child=StatsDailyPointSerializer())

class StatsChartSerializer(serializers.Serializer):
    domain = serializers.CharField()
    users = serializers.ListField(child=StatsChartDomainField())
