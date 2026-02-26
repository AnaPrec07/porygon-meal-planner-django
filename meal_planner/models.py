from django.db import models
from django.contrib.auth.models import User

# Food model (dimension)
class Food(models.Model):
    name = models.CharField(max_length=100)
    one_serving_qty = models.FloatField()
    serving_unit = models.CharField(max_length=50)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# MealPlan model (fact/transactional)
class UserMealPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField()
    meal_plan_name = models.CharField(max_length=100)
    meal_plan = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

class MiendDietParameters(models.Model):
    category = models.CharField(max_length=100, unique=True)
    servings_per_week = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.category} ({self.servings_per_week} servings/week)"

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
