
from django.contrib import admin
from .models import Food, UserMealPlan, AgentMemory, MiendDietParameters
from import_export.admin import ImportExportModelAdmin



@admin.register(MiendDietParameters)
class MiendDietParametersAdmin(ImportExportModelAdmin):
    list_display = ("category", "servings_per_week")
    search_fields = ("category",)
	
@admin.register(Food)
class FoodAdmin(ImportExportModelAdmin):
	list_display = ("name", "category", "serving_unit", "one_serving_qty")
	search_fields = ("name", "category")

@admin.register(UserMealPlan)
class MealPlanAdmin(admin.ModelAdmin):
	list_display = ("user", "is_active", "meal_plan_name", "meal_plan", "created_at")
	list_filter = ("user",)

@admin.register(AgentMemory)
class AgentMemoryAdmin(admin.ModelAdmin):
	list_display = ("user", "memory_type", "importance", "active", "created_at", "last_accessed")
	search_fields = ("user__username", "memory_type", "content")
