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

# Meal model (dimension/transactional)
class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # Optionally add tags, cuisine, etc.

    def __str__(self):
        return self.name

# Through model for Meal and Food (quantities)
class MealFood(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    quantity = models.FloatField(help_text="Quantity in grams or units")

# MealPlan model (fact/transactional)
class MealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    meal_type = models.CharField(max_length=20, choices=[('breakfast','Breakfast'),('lunch','Lunch'),('dinner','Dinner'),('snack','Snack')])
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'date', 'meal_type')

class AgentMemory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    memory_type = models.CharField(
        max_length=50,
        choices=[
            ("preference", "Preference"),
            ("goal", "Goal"),
            ("fact", "Fact"),
            ("event", "Event"),
            ("progress", "Progress"),
        ],
    )
    content = models.TextField()
    json_payload = models.TextField()
    importance = models.FloatField()
    created_at = models.DateTimeField()
    last_accessed = models.DateTimeField()
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "dataset.agent_memory"
