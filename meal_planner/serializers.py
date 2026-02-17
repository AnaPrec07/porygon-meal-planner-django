from rest_framework import serializers
from .models import Food, Recipe, RecipeFood, MealPlan, UserPreference, UserProgress
from django.contrib.auth.models import User

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class RecipeFoodSerializer(serializers.ModelSerializer):
    food = FoodSerializer(read_only=True)
    food_id = serializers.PrimaryKeyRelatedField(queryset=Food.objects.all(), source='food', write_only=True)

    class Meta:
        model = RecipeFood
        fields = ['id', 'food', 'food_id', 'quantity']

class RecipeSerializer(serializers.ModelSerializer):
    foods = RecipeFoodSerializer(source='recipefood_set', many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = ['id', 'name', 'description', 'instructions', 'created_by', 'foods']

class MealPlanSerializer(serializers.ModelSerializer):
    recipe = RecipeSerializer(read_only=True)
    recipe_id = serializers.PrimaryKeyRelatedField(queryset=Recipe.objects.all(), source='recipe', write_only=True)
    class Meta:
        model = MealPlan
        fields = ['id', 'user', 'date', 'meal_type', 'recipe', 'recipe_id']

class UserPreferenceSerializer(serializers.ModelSerializer):
    liked_recipes = RecipeSerializer(many=True, read_only=True)
    disliked_foods = FoodSerializer(many=True, read_only=True)
    class Meta:
        model = UserPreference
        fields = ['id', 'user', 'dietary_restrictions', 'liked_recipes', 'disliked_foods', 'goal']

class UserProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProgress
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
