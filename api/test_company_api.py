import json
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
class BasicCompanyAPiTestCase(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("api:companies-list")

    def tearDown(self) -> None:
        pass


class TestListCompanies(BasicCompanyAPiTestCase):

    def test_get_companies_list_should_succeed(self) -> None:
        response = self.client.get(self.companies_url)
        data = json.loads(response.content)['data']
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(data, [])


class TestPostCompanies(BasicCompanyAPiTestCase):

    def test_create_company(self) -> None:
        response = self.client.post(path=self.companies_url,
                                    data={
                                        "name": "comapany name",
                                        "location": "berlin"
                                    })
        self.assertEqual(response.status_code, 201)
        response_content = response.json()
        self.assertEqual(
            response_content.get('data').get("name"), "comapany name")
        self.assertEqual(response_content.get('data').get("location"), "berlin")

    def test_create_company_without_arguments_should_fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        response_content = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response_content.get('errors').get('name'),
            ["This field is required."])

    def test_create_company_with_empty_name_should_fail(self):
        response = self.client.post(
            path=self.companies_url,
            data={"name": ""},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("This field may not be blank.", str(response.content))


class TestRetrieveCompany(BasicCompanyAPiTestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.pk = None

    def get_url(self):
        return reverse("api:companies-detail", kwargs={'pk': self.pk})

    def test_retreive_one_company_should_succeed(self) -> None:
        self.pk = 1
        response = self.client.get(self.get_url())
        data = json.loads(response.content)['data']
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(data, {})
        self.assertNotEqual(data, [])
        self.assertEquals(data.get('id'), self.pk)

    def test_retreive_one_company_with_non_existent_id_should_fail(self):
        self.pk = 1111111111111
        response = self.client.get(self.get_url())
        self.assertEqual(response.status_code, 404)
        self.assertIn("A Company with this id does not exist",
                      str(response.content))
