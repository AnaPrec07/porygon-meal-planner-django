from rest_framework import serializers
from .models import Food, UserMealPlan, AgentMemory
from django.contrib.auth.models import User

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class AgentMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentMemory
        fields = ['id', 'user', 'memory_type', 'content', 'json_payload', 'importance', 'created_at', 'last_accessed', 'active']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
