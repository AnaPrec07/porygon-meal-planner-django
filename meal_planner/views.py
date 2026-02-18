from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# Landing page view for Mindy introduction and MIND diet info
def landing_page(request):
	context = {
		'mindy_intro': (
			"Hello! I'm Mindy, your friendly nutritionist specializing in the MIND diet. "
			"I'm here to help you achieve your health goals, stay motivated, and celebrate your milestones. "
			"Together, we'll create meal plans that follow the MIND diet and support your unique journey!"
		),
		'mind_diet_info': (
			"The MIND diet (Mediterranean-DASH Diet Intervention for Neurodegenerative Delay) combines elements of the Mediterranean and DASH diets. "
			"It focuses on foods that support brain health and may reduce the risk of Alzheimer's disease."
		),
		'mind_diet_constitutes': [
			"Green leafy vegetables",
			"Other vegetables",
			"Nuts",
			"Berries (especially blueberries)",
			"Beans",
			"Whole grains",
			"Fish",
			"Poultry",
			"Olive oil",
			"Wine (in moderation)"
		],
		'mind_diet_benefits': [
			"Supports brain health",
			"May lower risk of Alzheimer's and dementia",
			"Promotes heart health",
			"Encourages healthy eating habits"
		],
		'mindy_helps': (
			"Mindy helps you organize your goals, track your progress, and stay motivated. "
			"You'll receive personalized meal plans, encouragement, and support every step of the way!"
		),
	}
	return render(request, 'meal_planner/landing.html', context)
@api_view(['GET', 'PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def user_mealplans(request):
	"""
	GET: Return all MealPlan records for the authenticated user, ordered by date.
	PUT/PATCH: Update a specific MealPlan by id (requires 'id' in data).
	"""
	if request.method == 'GET':
		mealplans = MealPlan.objects.filter(user=request.user).order_by('date')
		serializer = MealPlanSerializer(mealplans, many=True)
		return Response(serializer.data)

	elif request.method in ['PUT', 'PATCH']:
		mealplan_id = request.data.get('id')
		if not mealplan_id:
			return Response({'error': 'MealPlan id required.'}, status=400)
		try:
			mealplan = MealPlan.objects.get(id=mealplan_id, user=request.user)
		except MealPlan.DoesNotExist:
			return Response({'error': 'MealPlan not found.'}, status=404)
		serializer = MealPlanSerializer(mealplan, data=request.data, partial=(request.method=='PATCH'))
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=400)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_progress(request):
	"""
	Returns all UserProgress records for the authenticated user, ordered by date.
	"""
	progress = UserProgress.objects.filter(user=request.user).order_by('date')
	serializer = UserProgressSerializer(progress, many=True)
	return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_recipe(request):
	"""
	Endpoint for user to accept or reject a recipe.
	Expects: {
		'accept': true/false,
		'recipe': {
			'name': str,
			'description': str,
			'instructions': str,
			'foods': [
				{'name': str, 'category': str, 'calories': float, 'protein': float, 'carbs': float, 'fat': float}
			]
		},
		'meal_type': str,  # breakfast/lunch/dinner/snack
		'date': str (YYYY-MM-DD)
	}
	"""
	data = request.data
	if not data.get('accept'):
		return Response({'message': 'Recipe not accepted.'}, status=200)

	recipe_data = data.get('recipe')
	meal_type = data.get('meal_type')
	date = data.get('date')
	if not (recipe_data and meal_type and date):
		return Response({'error': 'Missing required fields.'}, status=400)

	# Save foods if not exist
	food_objs = []
	for food in recipe_data.get('foods', []):
		food_obj, _ = Food.objects.get_or_create(
			name=food['name'],
			defaults={
				'category': food.get('category', ''),
				'calories': food.get('calories', 0),
				'protein': food.get('protein', 0),
				'carbs': food.get('carbs', 0),
				'fat': food.get('fat', 0),
				'fiber': food.get('fiber', 0),
				'sugar': food.get('sugar', 0),
				'sodium': food.get('sodium', 0),
			}
		)
		food_objs.append(food_obj)

	# Save recipe if not exist
	recipe, created = Recipe.objects.get_or_create(
		name=recipe_data['name'],
		defaults={
			'description': recipe_data.get('description', ''),
			'instructions': recipe_data.get('instructions', ''),
			'created_by': request.user
		}
	)
	# If new, add foods to recipe
	if created:
		for food_obj in food_objs:
			RecipeFood.objects.create(recipe=recipe, food=food_obj, quantity=100)  # Default quantity

	# Add to MealPlan
	mealplan, _ = MealPlan.objects.get_or_create(
		user=request.user,
		date=date,
		meal_type=meal_type,
		defaults={'recipe': recipe}
	)
	if not _:
		mealplan.recipe = recipe
		mealplan.save()

	return Response({'message': 'Recipe accepted and added to meal plan.'}, status=201)

from rest_framework import viewsets, permissions
from .models import Food, Recipe, RecipeFood, MealPlan, UserPreference, UserProgress
from .serializers import FoodSerializer, RecipeSerializer, RecipeFoodSerializer, MealPlanSerializer, UserPreferenceSerializer, UserProgressSerializer
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserSerializer

# AI Chatbot endpoint (placeholder)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ai_chatbot(request):
	user_message = request.data.get('message', '')
	# Placeholder: Replace with OpenAI or other AI integration
	if not user_message:
		return Response({'error': 'No message provided.'}, status=400)
	# Example static response
	ai_response = f"AI suggests a healthy meal plan for: '{user_message}' (replace with real AI call)"
	return Response({'response': ai_response})

# Food CRUD
class FoodViewSet(viewsets.ModelViewSet):
	queryset = Food.objects.all()
	serializer_class = FoodSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# Recipe CRUD
class RecipeViewSet(viewsets.ModelViewSet):
	queryset = Recipe.objects.all()
	serializer_class = RecipeSerializer
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# MealPlan CRUD
class MealPlanViewSet(viewsets.ModelViewSet):
	queryset = MealPlan.objects.all()
	serializer_class = MealPlanSerializer
	permission_classes = [permissions.IsAuthenticated]

# UserPreference CRUD
class UserPreferenceViewSet(viewsets.ModelViewSet):
	queryset = UserPreference.objects.all()
	serializer_class = UserPreferenceSerializer
	permission_classes = [permissions.IsAuthenticated]

# UserProgress CRUD
class UserProgressViewSet(viewsets.ModelViewSet):
	queryset = UserProgress.objects.all()
	serializer_class = UserProgressSerializer
	permission_classes = [permissions.IsAuthenticated]

# User CRUD (read-only)
class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

# Registration endpoint
class RegisterUserView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = [permissions.AllowAny]

	def create(self, request, *args, **kwargs):
		response = super().create(request, *args, **kwargs)
		user = User.objects.get(username=request.data['username'])
		token, created = Token.objects.get_or_create(user=user)
		response.data['token'] = token.key
		return response
