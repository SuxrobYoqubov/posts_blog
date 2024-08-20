from django.urls import path
from post.views import PostView, PostDetailView,AddCommentView, \
PostCategoryView, PostCreateView, MessageView

app_name = "post"

urlpatterns = [
    path("", PostView.as_view(), name='list'),
    path("create/", PostCreateView.as_view(), name = "create"),
    path("<int:id>/category/", PostCategoryView.as_view(), name = "category"),
    path("<int:id>/comment/", AddCommentView.as_view(), name = "comment"),
    path("<int:id>/post/", PostDetailView.as_view(), name = "detail"),
    path("message/", MessageView.as_view(), name = "message"),
]
