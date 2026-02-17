
from django.contrib import admin
from .models import Food, Recipe, RecipeFood, MealPlan, UserPreference, UserProgress

class RecipeFoodInline(admin.TabularInline):
	model = RecipeFood
	extra = 1

@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "calories", "protein", "carbs", "fat")
	search_fields = ("name", "category")

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
	list_display = ("name", "created_by")
	search_fields = ("name",)
	inlines = [RecipeFoodInline]

@admin.register(MealPlan)
class MealPlanAdmin(admin.ModelAdmin):
	list_display = ("user", "date", "meal_type", "recipe")
	list_filter = ("meal_type", "date", "user")

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
	list_display = ("user", "goal")
	search_fields = ("user__username", "goal")

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
	list_display = ("user", "date", "weight_kg", "bmi")
	list_filter = ("user", "date")
