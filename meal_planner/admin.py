
from django.contrib import admin
from .models import Food, Meal, MealFood, MealPlan, AgentMemory, MiendDietParameters
from import_export.admin import ImportExportModelAdmin



@admin.register(MiendDietParameters)
class MiendDietParametersAdmin(ImportExportModelAdmin):
    list_display = ("category", "servings_per_week")
    search_fields = ("category",)
	
@admin.register(MealFood)
class MealFoodAdmin(admin.ModelAdmin):
	list_display = ("meal", "food", "quantity")
	search_fields = ("meal__name", "food__name")

class MealFoodInline(admin.TabularInline):
	model = MealFood
	extra = 1

@admin.register(Food)
class FoodAdmin(ImportExportModelAdmin):
	list_display = ("name", "category", "serving_unit", "one_serving_qty")
	search_fields = ("name", "category")
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
	list_display = ("name", "created_by")
	search_fields = ("name",)
	inlines = [MealFoodInline]

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
	list_display = ("user", "date", "meal_type", "meal")
	list_filter = ("meal_type", "date", "user")


@admin.register(AgentMemory)
class AgentMemoryAdmin(admin.ModelAdmin):
	list_display = ("user", "memory_type", "importance", "active", "created_at", "last_accessed")
	search_fields = ("user__username", "memory_type", "content")
