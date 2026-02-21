from django import forms
from .models import MiendDietParameters, Food

class CategorySelectForm(forms.Form):
    category = forms.ModelChoiceField(queryset=MiendDietParameters.objects.all(), label="Select MIND Diet Category")

class FoodSelectForm(forms.Form):
    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)
        super().__init__(*args, **kwargs)
        self.category = category
        foods = Food.objects.filter(category=category)
        param = MiendDietParameters.objects.get(category=category)
        self.servings_limit = param.servings_per_week

        for food in foods:
            self.fields[f'food_{food.id}'] = forms.IntegerField(
                label=f"{food.name} ({food.serving_unit})",
                min_value=0,
                initial=0,
                required=False
            )
        self.helper_text = f"Distribute a total of {param.servings_per_week} servings (or more) among these foods."


    def clean(self):
        cleaned_data = super().clean()
        total = sum([v or 0 for k, v in cleaned_data.items() if k.startswith('food_')])
        if total < self.servings_limit:
            raise forms.ValidationError(f"You have selected {total} servings, which is less than the required {self.servings_limit} servings for this category.")
        return cleaned_data
