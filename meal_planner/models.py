from django.db import models
from django.contrib.auth.models import User

# Food model (dimension)
class Food(models.Model):
    name = models.CharField(max_length=100)
    qty = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    calories = models.FloatField()
    protein = models.FloatField()
    carbs = models.FloatField()
    fat = models.FloatField()
    fiber = models.FloatField(null=True, blank=True)
    sugar = models.FloatField(null=True, blank=True)
    sodium = models.FloatField(null=True, blank=True)
    # Add more nutrients as needed

    def __str__(self):
        return self.name

# Recipe model (dimension/transactional)
class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    foods = models.ManyToManyField(Food, through='RecipeFood')
    instructions = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # Optionally add tags, cuisine, etc.

    def __str__(self):
        return self.name

# Through model for Recipe and Food (quantities)
class RecipeFood(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Quantity in grams or units")

# MealPlan model (fact/transactional)
class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=[('breakfast','Breakfast'),('lunch','Lunch'),('dinner','Dinner'),('snack','Snack')])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'date', 'meal_type')

# UserPreference model
class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dietary_restrictions = models.TextField(blank=True, help_text="Comma-separated restrictions, e.g. gluten-free, vegan")
    liked_recipes = models.ManyToManyField(Recipe, blank=True, related_name='liked_by_users')
    disliked_foods = models.ManyToManyField(Food, blank=True, related_name='disliked_by_users')
    goal = models.CharField(max_length=100, blank=True, help_text="e.g. weight loss, muscle gain")

# UserProgress model
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight_kg = models.FloatField()
    height_cm = models.FloatField()
    body_fat_percent = models.FloatField(null=True, blank=True)
    muscle_mass_kg = models.FloatField(null=True, blank=True)
    bmi = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'date')