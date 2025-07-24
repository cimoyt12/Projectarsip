from rest_framework import serializers
from .models import Arsip

class ArsipSerializer(serializers.ModelSerializer):
    ukuran_mb = serializers.SerializerMethodField()
    
    class Meta:
        model = Arsip
        fields = '__all__'
    
    def get_ukuran_mb(self, obj):
        return obj.get_ukuran_mb()