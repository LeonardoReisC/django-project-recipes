from django.urls import include, path
from rest_framework.routers import SimpleRouter

from authors.views.api import AuthorAPIV2ViewSet

from . import views

app_name = 'authors'

authors_api_v2_router = SimpleRouter()
authors_api_v2_router.register(
    'api/v2',
    AuthorAPIV2ViewSet,
    basename='authors-api-v2'
)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/create/', views.login_create, name='login_create'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path(
        'dashboard/recipe/create/',
        views.DashboardRecipe.as_view(),
        name='dashboard_recipe_create'
    ),
    path(
        'dashboard/recipe/delete/',
        views.DashboardRecipeDelete.as_view(),
        name='dashboard_recipe_delete'
    ),
    path(
        'dashboard/recipe/<int:id>/edit/',
        views.DashboardRecipe.as_view(),
        name='dashboard_recipe_edit'
    ),
    path(
        'profile/<int:id>/',
        views.ProfileView.as_view(),
        name='profile'
    ),
    path('', include(authors_api_v2_router.urls))
]
