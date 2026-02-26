from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from meal_planner.agent.agent import ask_mindy_for_meal_plan
import json
import re
import json
from .models import UserMealPlan
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from .models import Food, UserMealPlan, AgentMemory
from .serializers import FoodSerializer, AgentMemorySerializer
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

class AgentMemoryViewSet(viewsets.ModelViewSet):
	queryset = AgentMemory.objects.all()
	serializer_class = AgentMemorySerializer
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
	
def test_mindy_agent(request):
	# Example selected foods; in practice, get this from request.GET or request.POST
	user = request.user if request.user.is_authenticated else None

	if request.method == "POST":
		action = request.POST.get("action")
		if action == "accept":
			meal_plan_data = request.session.get("meal_plan_data")

			# Save to UserMealPlan
			meal_plan_name = request.POST.get("meal_plan_name") or "AI Meal Plan"
			UserMealPlan.objects.create(
				user=user,
				is_active=True,
				meal_plan_name=meal_plan_name,
				meal_plan=meal_plan_data
			)
			return render(request, "meal_planner/agent_meal_plan.html", {"meal_plan": meal_plan_data, "message": "Meal plan saved!"})
		else:
			selected_foods = request.POST.getlist("foods")
			meal_plan_data = ask_mindy_for_meal_plan(selected_foods)
			request.session["meal_plan_data"] = meal_plan_data if isinstance(meal_plan_data, dict) else json.loads(meal_plan_data)
			return render(request, "meal_planner/agent_meal_plan.html", {"meal_plan": meal_plan_data})
	else:
		selected_foods = request.POST.getlist("foods")
		meal_plan_data = ask_mindy_for_meal_plan(selected_foods)
		request.session["meal_plan_data"] = meal_plan_data if isinstance(meal_plan_data, dict) else json.loads(meal_plan_data)

		return render(request, "meal_planner/agent_meal_plan.html", {"meal_plan": meal_plan_data})