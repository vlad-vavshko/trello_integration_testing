from assertpy import assert_that
from uuid import uuid4
from constants.configs import TRELLO_TOKEN
from constants.configs import TRELLO_API_KEY
from constants.configs import ORGANIZATION_ID
from helpers.helpers import Boards
from helpers.helpers import Cards

# Init
boards = Boards(TRELLO_TOKEN, TRELLO_API_KEY, ORGANIZATION_ID)
cards = Cards(TRELLO_TOKEN, TRELLO_API_KEY, ORGANIZATION_ID)


# =============== Test ===============
def test_create_new_card_on_board():
    # Arrange
    board_id = boards.create_new_board()
    list_id = cards.create_new_list(board_id=board_id)
    card_name = f"Automation {uuid4()}"
    # Act
    card = cards.create_new_card(list_id=list_id, card_name=card_name)
    card_json = card.json()

    # Assert
    assert_that(card.status_code).is_equal_to(200)
    assert_that(card_json['name']).is_equal_to(card_name)

    boards.delete_board_by_id(board_id)


def test_update_card_on_board():
    # Arrange
    board_id = boards.create_new_board()
    list_id = cards.create_new_list(board_id=board_id)
    card_name = f"Automation {uuid4()}"
    card_id = cards.create_new_card(list_id=list_id, card_name=card_name).json()['id']

    # Act
    updated_card = cards.card_update(card_id)
    upd_card_json = updated_card.json()

    # Assert
    assert_that(updated_card.status_code).is_equal_to(200)
    assert_that(upd_card_json['desc']).contains('Updated')

    boards.delete_board_by_id(board_id)


def test_delete_card_from_board():
    pass


def test_move_card_between_list():
    pass
