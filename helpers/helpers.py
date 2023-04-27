import requests
from uuid import uuid4
from assertpy import assert_that


# Helpers to interact with the boards
class Boards:
    def __init__(self, TRELLO_TOKEN, TRELLO_API_KEY, ORGANIZATION_ID):
        self.TRELLO_TOKEN = TRELLO_TOKEN
        self.TRELLO_API_KEY = TRELLO_API_KEY
        self.ORGANIZATION_ID = ORGANIZATION_ID

    # Return ID of created board
    def create_new_board(self, board_name=f'Board {str(uuid4())}'):
        url = "https://api.trello.com/1/boards/"
        query = {
            'name': board_name,
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN
        }
        response = requests.post(url=url, params=query)
        assert_that(response.status_code).is_equal_to(200)
        return response.json()['id']

    # Return response of GET request
    def get_board_by_id(self, id):
        url = f"https://api.trello.com/1/boards/{id}"
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN
        }
        response = requests.get(url=url, headers=headers, params=query)
        # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
        return response

    # Return status code of DELETE request (200 - Success)
    def delete_board_by_id(self, id):
        url = f"https://api.trello.com/1/boards/{id}"
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN
        }
        response = requests.delete(url=url, params=query, headers=headers)
        return response.status_code

    # Return response
    def get_boards_for_organization(self):
        organization_id = self.ORGANIZATION_ID
        url = f"https://api.trello.com/1/organizations/{organization_id}/boards"
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN
        }

        response = requests.get(url=url, headers=headers, params=query)
        # print(response.content)
        return response

    def get_labels_on_board(self, id):
        url = f"https://api.trello.com/1/boards/{id}/labels"

        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN
        }
        headers = {
            "Accept": "application/json"
        }

        response = requests.get(url=url, headers=headers, params=query)
        return response


# Helpers to interact with the cards
class Cards:
    def __init__(self, TRELLO_TOKEN, TRELLO_API_KEY, ORGANIZATION_ID):
        self.TRELLO_TOKEN = TRELLO_TOKEN
        self.TRELLO_API_KEY = TRELLO_API_KEY
        self.ORGANIZATION_ID = ORGANIZATION_ID

    # Return ID of list
    def create_new_list(self, board_id, name=f"List {uuid4()}"):
        url = "https://api.trello.com/1/lists"
        headers = {
            "Accept": "application/json"
        }
        query = {
            'name': name,
            'idBoard': board_id,
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN
        }
        response = requests.post(url=url, headers=headers, params=query).json()
        return response['id']

    # Return response of POST request
    def create_new_card(self, list_id, card_name):
        url = "https://api.trello.com/1/cards"
        headers = {
            "Accept": "application/json"
        }
        query = {
            'idList': list_id,
            'name': card_name,
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN
        }
        response = requests.post(url=url, params=query, headers=headers)
        return response

    # Return response of PUT request
    def card_update(self, card_id):
        url = f"https://api.trello.com/1/cards/{card_id}"
        headers = {
            "Accept": "application/json"
        }
        query = {
            'key': self.TRELLO_API_KEY,
            'token': self.TRELLO_TOKEN,
            'name': f"Updated {uuid4()}",
            'desc': "Updated card with Automation script",

        }
        response = requests.put(url=url, headers=headers, params=query)
        return response
