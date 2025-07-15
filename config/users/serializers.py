from django.contrib.auth.models import User
from rest_framework import serializers

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    
    class Meta:
        model = User
        fields = ['username','password']
        
    def create(self, validated_data):
        user = User.objects.create_user( #create_user : 자동으로 비밀번호를 해상하여 저장
            username = validated_data['username'],
            password = validated_data['password']
        )
        return user