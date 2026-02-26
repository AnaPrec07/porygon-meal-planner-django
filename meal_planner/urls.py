from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodViewSet, AgentMemoryViewSet, UserViewSet, RegisterUserView, ai_chatbot, landing_page, test_mindy_agent
from .wizard_views import MindDietWizardView, ShoppingListView, DownloadShoppingListPDFView

router = DefaultRouter()
router.register(r'foods', FoodViewSet)
router.register(r'agentmemories', AgentMemoryViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('shopping-list/', ShoppingListView.as_view(), name='shopping_list'),
    path('mind-diet-wizard/', MindDietWizardView.as_view(), name='mind_diet_wizard'),
    path('download-shopping-list-pdf/', DownloadShoppingListPDFView.as_view(), name='download_shopping_list_pdf'),
    path('api/', include(router.urls)),
    path('api/register/', RegisterUserView.as_view(), name='register'),
    path('api/auth/', include('rest_framework.urls')),  # login/logout for browsable API
    path('api/token-auth/', __import__('rest_framework.authtoken.views').authtoken.views.obtain_auth_token, name='api_token_auth'),
    path('api/ai-chatbot/', ai_chatbot, name='ai_chatbot'),
    path('generate-agent-meal-plan/', test_mindy_agent, name='generate_agent_meal_plan'),
]
