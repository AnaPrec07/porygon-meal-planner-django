from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy
from .forms import CategorySelectForm, FoodSelectForm
from .models import MiendDietParameters, Food, Meal, MealPlan
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


class MindDietWizardView(LoginRequiredMixin, FormView):
    template_name = 'meal_planner/mind_diet_wizard.html'
    form_class = CategorySelectForm
    success_url = reverse_lazy('mind_diet_wizard')
    http_method_names = ['get', 'post']

    def get(self, request, *args, **kwargs):
        if request.GET.get('restart'):
            request.session['wizard_step'] = 0
            request.session['selected_foods'] = {}
            return HttpResponseRedirect(reverse_lazy('mind_diet_wizard'))
        step = request.session.get('wizard_step', 0)

        selected_categories = request.session.get('selected_categories', [])
        selected_foods = request.session.get('selected_foods', {})
        categories = list(MiendDietParameters.objects.values_list('category', flat=True))
        if step < len(categories):
            category = categories[step]
            form = FoodSelectForm(category=category)
            # Get weekly servings for this category
            param = MiendDietParameters.objects.get(category=category)
            servings = param.servings_per_week
            return self.render_to_response(self.get_context_data(form=form, category=category, step=step, categories=categories, servings=servings))
        else:
            # Generate meal plan
            new_dict = {}
            for category, foods in selected_foods.items():
                new_foods = {}
                for food_id, qty in foods.items():
                    food_obj = Food.objects.get(id=food_id)
                    new_foods[food_obj.name] = qty
                new_dict[category] = new_foods
            meal_plan = self.generate_meal_plan(request.user, new_dict)
            # meal_plan = self.generate_meal_plan(request.user, selected_foods)
            return TemplateView.as_view(template_name='meal_planner/meal_plan_result.html')(request, meal_plan=meal_plan)

    def post(self, request, *args, **kwargs):
        step = request.session.get('wizard_step', 0)
        selected_categories = request.session.get('selected_categories', [])
        selected_foods = request.session.get('selected_foods', {})
        categories = list(MiendDietParameters.objects.values_list('category', flat=True))
        if step < len(categories):
            category = categories[step]
            form = FoodSelectForm(request.POST, category=category)
            if form.is_valid():
                food_quantities = {k.replace('food_', ''): v for k, v in form.cleaned_data.items() if k.startswith('food_') and v > 0}
                selected_foods[category] = food_quantities
                request.session['selected_foods'] = selected_foods
                request.session['wizard_step'] = step + 1
                return HttpResponseRedirect(reverse_lazy('mind_diet_wizard'))
            else:
                return self.render_to_response(self.get_context_data(form=form, category=category, step=step, categories=categories))
        else:
            return HttpResponse("Hello, World!") #HttpResponseRedirect(reverse_lazy('mind_diet_wizard'))

    def generate_meal_plan(self, user, selected_foods):
        # Placeholder: implement logic to generate meal plan using selected_foods
        # For now, just return selected_foods
        return {'selected_foods': selected_foods}
