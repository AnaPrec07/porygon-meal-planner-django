from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodViewSet, RecipeViewSet, MealPlanViewSet, UserPreferenceViewSet, UserProgressViewSet, UserViewSet, RegisterUserView, ai_chatbot, accept_recipe, user_progress, user_mealplans, landing_page

router = DefaultRouter()
router.register(r'foods', FoodViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'mealplans', MealPlanViewSet)
router.register(r'userpreferences', UserPreferenceViewSet)
router.register(r'userprogress', UserProgressViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
	path('', landing_page, name='landing_page'),
	path('api/', include(router.urls)),
	path('api/register/', RegisterUserView.as_view(), name='register'),
	path('api/auth/', include('rest_framework.urls')),  # login/logout for browsable API
	path('api/token-auth/', __import__('rest_framework.authtoken.views').authtoken.views.obtain_auth_token, name='api_token_auth'),
	path('api/ai-chatbot/', ai_chatbot, name='ai_chatbot'),
	path('api/accept-recipe/', accept_recipe, name='accept_recipe'),
	path('api/user-progress/', user_progress, name='user_progress'),
	path('api/user-mealplans/', user_mealplans, name='user_mealplans'),
]
