import tempfile

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils.crypto import get_random_string
from PIL import Image
from rest_framework import status
from rest_framework.test import APIClient

from users.models import TierList, Tier

def create_client(**params):

    defaults = {
        "email": "mail_" + get_random_string(length=10) + "@example.com",
        "password": "password_123",
    }
    defaults.update(**params)
    user = get_user_model().objects.create_user(**defaults)
    user_client = APIClient()
    user_client.force_authenticate(user)
    return user_client


class ImageUploadTests(TestCase):
    def setUp(self):
        self.user_premium = create_client(**{"tier": TierList.PREMIUM})
        self.user_enterprise = create_client(**{"tier": TierList.ENTERPRISE})
        self.user_basic = create_client()
        custom_tier_1 = Tier.objects.create(
            **{
                "thumbnail_sizes": [100, 900],
                "original_file_access": False,
                "binary_file_access": False,
            }
        )
        self.user_custom_1 = create_client(
            **{"tier": TierList.CUSTOM, "custom_tier": custom_tier_1}
        )
        custom_tier_2 = Tier.objects.create(
            **{
                "thumbnail_sizes": [250, 100, 300, 400],
                "original_file_access": True,
                "binary_file_access": True,
            }
        )
        self.user_custom_2 = create_client(
            **{"tier": TierList.CUSTOM, "custom_tier": custom_tier_2}
        )
        self.url = reverse("images:image-list")

    def test_upload_image_basic_user(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"file": image_file, "binary_expiration_time": ""}
            res = self.user_basic.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(200, res.data["thumbnail_urls"])
        self.assertNotIn("file", res.data)
        self.assertNotIn(400, res.data["thumbnail_urls"])

    def test_wrong_upload_image_basic_user(self):

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"file": image_file, "binary_expiration_time": "333"}
            res = self.user_basic.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_image_premium_user(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"file": image_file, "binary_expiration_time": ""}
            res = self.user_premium.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("file", res.data)
        self.assertIn(200, res.data["thumbnail_urls"])
        self.assertIn(400, res.data["thumbnail_urls"])

    def test_wrong_upload_image_premium_user(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"file": image_file, "binary_expiration_time": "333"}
            res = self.user_premium.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_image_enterprise_user(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"file": image_file, "binary_expiration_time": "333"}
            res = self.user_enterprise.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(res.data["image_binary"])
        self.assertIn("file", res.data)
        self.assertIn(200, res.data["thumbnail_urls"])
        self.assertIn(400, res.data["thumbnail_urls"])


    def test_upload_image_custom_user_1(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"file": image_file, "binary_expiration_time": ""}
            res = self.user_custom_1.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn(100, res.data["thumbnail_urls"])
        self.assertIn(900, res.data["thumbnail_urls"])
        self.assertNotIn("file", res.data)

    def test_wrong_upload_image_custom_user_1(self):

        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"file": image_file, "binary_expiration_time": "333"}
            res = self.user_custom_1.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_upload_image_custom_user_2(self):
        with tempfile.NamedTemporaryFile(suffix=".jpg") as image_file:
            img = Image.new("RGB", (10, 10))
            img.save(image_file, format="JPEG")
            image_file.seek(0)
            payload = {"file": image_file, "binary_expiration_time": "333"}
            res = self.user_custom_2.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(res.data["image_binary"])
        self.assertIn("file", res.data)
        self.assertIn(250, res.data["thumbnail_urls"])
        self.assertIn(100, res.data["thumbnail_urls"])
        self.assertIn(300, res.data["thumbnail_urls"])
        self.assertIn(400, res.data["thumbnail_urls"])


