from rest_framework import serializers
from .models import Food, Meal, MealFood, MealPlan, AgentMemory
from django.contrib.auth.models import User

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class MealFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    food_id = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all(), source='food', write_only=True)

    class Meta:
        model = MealFood
        fields = ['id', 'food', 'food_id', 'quantity']

class MealSerializer(serializers.ModelSerializer):
    foods = MealFoodSerializer(source='mealfood_set', many=True, read_only=True)
    class Meta:
        model = Meal
        fields = ['id', 'name', 'description', 'instructions', 'created_by', 'foods']

class MealPlanSerializer(serializers.ModelSerializer):
    meal = MealSerializer(read_only=True)
    meal_id = serializers.PrimaryKeyRelatedField(queryset=Meal.objects.all(), source='meal', write_only=True)
    class Meta:
        model = MealPlan
        fields = ['id', 'user', 'date', 'meal_type', 'meal', 'meal_id']


class AgentMemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentMemory
        fields = ['id', 'user', 'memory_type', 'content', 'json_payload', 'importance', 'created_at', 'last_accessed', 'active']



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
