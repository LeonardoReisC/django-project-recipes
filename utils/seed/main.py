import os
import shutil
import sys
from pathlib import Path

import django
from django.conf import settings

DJANGO_BASE_DIR = Path(__file__).parent.parent.parent

sys.path.append(str(DJANGO_BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

if __name__ == '__main__':

    from django.contrib.auth.models import User
    from django.utils.text import slugify

    from authors.models import Profile
    from recipes.models import Category, Recipe
    from tag.models import Tag
    from utils.environment import get_env_variable
    from utils.seed.data import CATEGORIES, data

    USERNAME = get_env_variable('DATABASE_USER')
    FIRST_NAME = USERNAME
    EMAIL = slugify(USERNAME) + '@email.com'
    PASSWORD = get_env_variable('DATABASE_PASSWORD')

    # Create administrator
    user = User.objects.create_superuser(
        USERNAME,
        EMAIL,
        PASSWORD,
        first_name=FIRST_NAME
    )
    user_profile = Profile.objects.get(author__id=user.id)
    user_profile.bio = (
        "I love cooking and sharing my recipes with others. It brings me so "
        "much joy to see people enjoy the dishes I create."
    )
    user_profile.save()

    # Create initial categories
    categories_objs = [Category.objects.create(name=c) for c in CATEGORIES]

    recipes_cover_path = settings.MEDIA_ROOT / 'recipes/covers'
    os.makedirs(recipes_cover_path)

    # Create recipes
    for recipe_data in data:
        tags = []
        for tag in recipe_data['tags']:
            tag = Tag.objects.get_or_create(name=tag)[0]
            tags.append(tag)

        initial_path = DJANGO_BASE_DIR / Path(recipe_data['cover'])
        new_path = recipes_cover_path / initial_path.name
        recipe_data['cover'] = str(new_path)
        shutil.copy(initial_path, new_path)

        recipe_category = categories_objs[recipe_data['category']]
        recipe_data = {
            **recipe_data,
            "is_published": True,
            "category": recipe_category,
            "author": user,
        }
        recipe_data.pop('tags')
        recipe = Recipe(**recipe_data)

        recipe.save()
        recipe.tags.set(tags)
