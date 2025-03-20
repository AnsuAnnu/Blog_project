
from django.urls import path,include
from .import views
from .views import (PostListView, PostCreateView, PostUpdateView,
					PostDeleteView, PostDetailView,add_comment, update_comment, delete_comment
)


urlpatterns = [
    # path('',views.Home,name='blog_home'),
	 path('about/', views.About, name='about'),

	path('', PostListView.as_view(), name="blog-home"),
	path('post-new/', PostCreateView.as_view(), name="blog-new"),
	path('post/<int:pk>/', PostDetailView.as_view(), name="blog-detail"),
	path('post/<int:pk>/update', PostUpdateView.as_view(), name="blog-update"),
	path('post/<int:pk>/delete', PostDeleteView.as_view(), name="blog-delete"),
	path("post/<int:post_id>/comment/", add_comment, name="add-comment"),
	path("comment/<int:comment_id>/update/", update_comment, name="update-comment"),
	path("comment/<int:comment_id>/delete/", delete_comment, name="delete-comment"),

]
