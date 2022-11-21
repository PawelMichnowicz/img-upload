from django.urls import include, path
from rest_framework import routers

from .views import BinaryImageApi, ImageApi

app_name = "images"

router = routers.SimpleRouter()
router.register("images", ImageApi)


urlpatterns = [
    path("", include(router.urls)),
    path(
        "binary-image/<int:pk>/<int:expiration>",
        BinaryImageApi.as_view(),
        name="binary_image",
    ),
]
