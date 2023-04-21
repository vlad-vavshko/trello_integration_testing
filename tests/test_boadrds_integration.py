import requests
from assertpy import assert_that
from uuid import uuid4
# from chapters.api_testing_python.trello_integration_testing.constants.configs import TRELLO_TOKEN
# from chapters.api_testing_python.trello_integration_testing.constants.configs import TRELLO_API_KEY
# from chapters.api_testing_python.trello_integration_testing.constants.configs import ORGANIZATION_ID
from constants.configs import TRELLO_TOKEN
from constants.configs import TRELLO_API_KEY
from constants.configs import ORGANIZATION_ID

# =============== Test ===============
def test_create_board():
    # Arrange | Act
    board_id = create_new_board()
    board = list(get_board_by_id(board_id))

    # Assert
    assert_that(board_id).is_not_empty()
    assert_that(board).is_not_empty()
    delete_board_by_id(board_id)


def test_get_a_board():
    # Arrange / Act
    board_id = create_new_board()
    board = list(get_board_by_id(board_id))

    # Assert
    assert_that(board).is_not_empty()
    delete_board_by_id(board_id)


def test_get_all_open_boards():
    # Arrange
    first_board = create_new_board()
    second_board = create_new_board()

    # Act
    all_open_boards = list(filter(lambda b: b['closed'] == False, get_boards_for_organization().json()))

    # Assert
    assert_that(all_open_boards).is_not_empty()
    for board in all_open_boards:
        assert_that(board['closed']).is_false()

    delete_board_by_id(first_board)
    delete_board_by_id(second_board)


def test_update_a_board():
    # Arrange
    board_id = create_new_board()
    url = f"https://api.trello.com/1/boards/{board_id}"
    headers = {
        "Accept": "application/json"
    }
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'name': f'Updated {str(uuid4())}',
        'desc': 'Board updated for Automation Testing by Vlad Vavshko',

    }
    # Act
    response = requests.put(url=url, params=query, headers=headers)
    update_board = get_board_by_id(board_id).json()

    # Assert
    assert_that(response.status_code).is_equal_to(200)
    assert_that(update_board['name']).contains('Updated')
    assert_that(update_board['desc']).contains('Vlad Vavshko')

    delete_board_by_id(board_id)


def test_create_label_on_a_board():
    # Arrange
    board_id = create_new_board()
    url = f"https://api.trello.com/1/boards/{board_id}/labels"
    label_name = f'Label {uuid4()}'
    headers = {
        "Accept": "application/json"
    }
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN,
        'name': label_name,
        'color': 'red',
    }
    # Act
    response = requests.post(url=url, headers=headers, params=query)

    board_labels = list(filter(lambda l:l['name']==label_name, get_labels_on_board(board_id).json()))

    # Assert
    assert_that(response.status_code).is_equal_to(200)
    assert_that(board_labels).is_not_empty()

    delete_board_by_id(board_id)

# =============== Helpers ===============
# Return ID of created board
def create_new_board(board_name=f'Board {str(uuid4())}'):
    url = "https://api.trello.com/1/boards/"
    query = {
        'name': board_name,
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    response = requests.post(url=url, params=query)
    assert_that(response.status_code).is_equal_to(200)
    return response.json()['id']


# Return response of GET request
def get_board_by_id(id):
    url = f"https://api.trello.com/1/boards/{id}"
    headers = {
        "Accept": "application/json"
    }
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    response = requests.get(url=url, headers=headers, params=query)
    # print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
    return response


# Return status code of DELETE request (200 - Success)
def delete_board_by_id(id):
    url = f"https://api.trello.com/1/boards/{id}"
    headers = {
        "Accept": "application/json"
    }
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    response = requests.delete(url=url, params=query, headers=headers)
    return response.status_code


# Return response
def get_boards_for_organization(organization_id=ORGANIZATION_ID):
    url = f"https://api.trello.com/1/organizations/{organization_id}/boards"
    headers = {
        "Accept": "application/json"
    }
    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }

    response = requests.get(url=url, headers=headers, params=query)
    # print(response.content)
    return response


def get_labels_on_board(id):
    url = f"https://api.trello.com/1/boards/{id}/labels"

    query = {
        'key': TRELLO_API_KEY,
        'token': TRELLO_TOKEN
    }
    headers = {
        "Accept": "application/json"
    }

    response = requests.get(url=url, headers=headers, params=query)
    return response
