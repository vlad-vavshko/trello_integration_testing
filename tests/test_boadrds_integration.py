import requests
from assertpy import assert_that
from uuid import uuid4
from helpers.helpers import Boards
from constants.configs import TRELLO_TOKEN
from constants.configs import TRELLO_API_KEY
from constants.configs import ORGANIZATION_ID

# Init
boards = Boards(TRELLO_TOKEN, TRELLO_API_KEY, ORGANIZATION_ID)


# =============== Test ===============
def test_create_board():
    # Arrange | Act
    board_id = boards.create_new_board()
    board = list(boards.get_board_by_id(board_id))

    # Assert
    assert_that(board_id).is_not_empty()
    assert_that(board).is_not_empty()
    boards.delete_board_by_id(board_id)


def test_get_a_board():
    # Arrange / Act
    board_id = boards.create_new_board()
    board = list(boards.get_board_by_id(board_id))

    # Assert
    assert_that(board).is_not_empty()
    boards.delete_board_by_id(board_id)


def test_get_all_open_boards():
    # Arrange
    first_board = boards.create_new_board()
    second_board = boards.create_new_board()

    # Act
    all_open_boards = list(filter(lambda b: b['closed'] == False, boards.get_boards_for_organization().json()))

    # Assert
    assert_that(all_open_boards).is_not_empty()
    for board in all_open_boards:
        assert_that(board['closed']).is_false()

    boards.delete_board_by_id(first_board)
    boards.delete_board_by_id(second_board)


def test_update_a_board():
    # Arrange
    board_id = boards.create_new_board()
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
    update_board = boards.get_board_by_id(board_id).json()

    # Assert
    assert_that(response.status_code).is_equal_to(200)
    assert_that(update_board['name']).contains('Updated')
    assert_that(update_board['desc']).contains('Vlad Vavshko')

    boards.delete_board_by_id(board_id)


def test_create_label_on_a_board():
    # Arrange
    board_id = boards.create_new_board()
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

    board_labels = list(filter(lambda l: l['name'] == label_name, boards.get_labels_on_board(board_id).json()))

    # Assert
    assert_that(response.status_code).is_equal_to(200)
    assert_that(board_labels).is_not_empty()

    boards.delete_board_by_id(board_id)
