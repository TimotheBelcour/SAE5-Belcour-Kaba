import os
from unittest import mock

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse


class PageAccueilTests(TestCase):
    def test_la_page_d_accueil_repond(self):
        reponse = self.client.get(reverse("accueil:index"))

        self.assertEqual(reponse.status_code, 200)
        self.assertTemplateUsed(reponse, "accueil/index.html")
        self.assertContains(reponse, "Jardins de Cocagne")

    def test_la_page_d_administration_demande_une_connexion(self):
        reponse = self.client.get("/admin/")

        self.assertRedirects(reponse, "/admin/login/?next=/admin/")


class CompteAdministrateurTests(TestCase):
    """Le compte admin / sae5 imposé est créé à partir de variables d'environnement."""

    @mock.patch.dict(
        os.environ,
        {
            "DJANGO_SUPERUSER_USERNAME": "admin",
            "DJANGO_SUPERUSER_PASSWORD": "sae5",
            "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
        },
    )
    def test_creation_du_compte_admin_sans_saisie(self):
        call_command("createsuperuser", interactive=False, verbosity=0)

        admin = get_user_model().objects.get(username="admin")
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password("sae5"))
        self.assertTrue(self.client.login(username="admin", password="sae5"))
