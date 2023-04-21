import requests
from assertpy import assert_that
from uuid import uuid4
from constants.configs import TRELLO_TOKEN
from constants.configs import TRELLO_API_KEY
from constants.configs import ORGANIZATION_ID
from test_boadrds_integration import create_new_board
from test_boadrds_integration import delete_board_by_id


# =============== Test ===============
def test_create_new_card_on_board():
    # Arrange
    board_id = create_new_board()
    list_id = create_new_list(board_id=board_id)
    card_name = f"Automation {uuid4()}"
    # Act
    card = create_new_card(list_id=list_id, card_name=card_name)
    card_json = card.json()

    # Assert
    assert_that(card.status_code).is_equal_to(200)
    assert_that(card_json['name']).is_equal_to(card_name)

    delete_board_by_id(board_id)


# =============== Helpers ===============

def get_cards_in_a_list():
    pass


def create_new_list(board_id, name=f"List {uuid4()}"):
    url = "https://api.trello.com/1/lists"
    headers = {
        "Accept": "application/json"
    }
    query = {
        'name': name,
        'idBoard': board_id,
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    response = requests.post(url=url, headers=headers, params=query).json()
    return response['id']


def create_new_card(list_id, card_name):
    url = "https://api.trello.com/1/cards"
    headers = {
        "Accept": "application/json"
    }
    query = {
        'idList': list_id,
        'name': card_name,
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    response = requests.post(url=url, params=query, headers=headers)
    return response
