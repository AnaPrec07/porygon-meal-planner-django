from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Food

class FoodModelTest(TestCase):
	def test_create_food(self):
		food = Food.objects.create(name="Apple", category="Fruit", calories=52, protein=0.3, carbs=14, fat=0.2)
		self.assertEqual(food.name, "Apple")
		self.assertEqual(food.category, "Fruit")

class FoodAPITest(TestCase):
	def setUp(self):
		self.client = APIClient()
		self.food_data = {"name": "Banana", "category": "Fruit", "calories": 89, "protein": 1.1, "carbs": 23, "fat": 0.3}

	def test_create_food_api(self):
		response = self.client.post(reverse('food-list'), self.food_data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Should require auth
