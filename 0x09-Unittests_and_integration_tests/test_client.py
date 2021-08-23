#!/usr/bin/env python3
""" test for client module """
import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient
from parameterized import parameterized


class TestGithubOrgClient(unittest.TestCase):
    """ Class for testing """
    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_org):
        """ Test function for client.get_json """
        client = GithubOrgClient(org_name)
        client.org()
        mock_org.assert_called_once()

    @patch('client.GithubOrgClient.org')
    def test_public_repos_url(self, mock_org):
        """ test for public_repos_url """
        mock_org.return_value = {'repos_url': True}
        client = GithubOrgClient('fake_org')
        self.assertEqual(mock_org.return_value, client.org())

    @patch('client.get_json', return_value=[{'name': 'public_one'}])
    @patch(
            'client.GithubOrgClient._public_repos_url',
            new_callable=PropertyMock,
            return_value='https://api.github.com/'
        )
    def test_public_repos(self, mock_public, mock_get):
        """ function that test public repos """
        client = GithubOrgClient('google')
        repos = client.public_repos()
        self.assertEqual(repos, ['public_one'])
        mock_get.assert_called_once()
        mock_public.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """ Test function for client.GithubOrgClient.has_license """
        new_client = GithubOrgClient("new_org")
        self.assertEqual(new_client.has_license(repo, license_key), expected)
