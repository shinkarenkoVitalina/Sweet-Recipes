from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPage.as_view() , name='main'),
    path('auth', views.LoginUserView.as_view(), name='auth'),
    path('registration', views.RegUserView.as_view(), name='reg'),
    path('profile/<int:pk>', views.ProfilePageView.as_view(), name='profile'),
    path('fav_recipe/<int:pk>', views.FavRecipePageView.as_view(), name='fav_recipe'),
    path('create_recipe', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('category/<int:cat_id>', views.CatPage.as_view(), name='category'),
    path('recipe/<int:pk>', views.RecipePage.as_view(), name='recipe'),
    path('recipe/<int:pk>/add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('recipe/<int:pk>/delete_favorites/', views.delete_favorites, name='delete_favorites'),
    path('recipe/<int:pk>/delete_recipe/', views.delete_recipe, name='delete_recipe'),
    path('logout', views.user_logout, name='logout')
]
