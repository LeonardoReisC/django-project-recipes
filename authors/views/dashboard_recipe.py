from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View

from authors.forms.recipe_form import RecipeForm
from recipes.models import Recipe


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(View):

    def get(self, request, id=None):
        recipe = self.get_recipe(id)
        form = RecipeForm(instance=recipe)
        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = RecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe,
        )

        if form.is_valid():
            recipe = form.save(commit=False)

            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.save()

            messages.success(request, 'Done.')
            return redirect('authors:dashboard')

        return self.render_recipe(form)

    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = get_object_or_404(
                Recipe,
                is_published=False,
                author=self.request.user,
                pk=id
            )

        return recipe

    def render_recipe(self, form):
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context={
                'form': form,
            }
        )


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def post(self, *args, **kwargs):
        recipe = self.get_recipe(self.request.POST.get('id'))
        recipe.delete()
        messages.success(self.request, 'Deleted.')
        return redirect('authors:dashboard')
