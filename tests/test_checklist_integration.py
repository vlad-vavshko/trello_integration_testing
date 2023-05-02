import pytest
from assertpy import assert_that
from uuid import uuid4
from constants.configs import TRELLO_TOKEN
from constants.configs import TRELLO_API_KEY
from constants.configs import ORGANIZATION_ID
from helpers.helpers import Cards
from helpers.helpers import Boards
from helpers.helpers import Checklists
import random

# Init
boards = Boards(TRELLO_TOKEN, TRELLO_API_KEY, ORGANIZATION_ID)
cards = Cards(TRELLO_TOKEN, TRELLO_API_KEY, ORGANIZATION_ID)
checklists = Checklists(TRELLO_TOKEN, TRELLO_API_KEY, ORGANIZATION_ID)


def test_create_checklist_for_card():
    # Arrange
    board_id = boards.create_new_board()
    list_id = cards.create_new_list(board_id=board_id)
    card_name = f"Automation {uuid4()}"

    card = cards.create_new_card(list_id=list_id, card_name=card_name)
    assert_that(card.status_code).is_equal_to(200)
    card_id = card.json()['id']
    # Act
    checklist_response = checklists.create_checklist(card_id=card_id)

    # Assert
    assert_that(checklist_response.status_code).is_equal_to(200)
    assert_that(checklist_response.json()['idBoard']).is_equal_to(board_id)
    assert_that(checklist_response.json()['idCard']).is_equal_to(card_id)
    boards.delete_board_by_id(board_id)


def test_update_checklist_on_card():
    # Arrange
    board_id = boards.create_new_board()
    list_id = cards.create_new_list(board_id=board_id)
    card_name = f"Automation {uuid4()}"

    card = cards.create_new_card(list_id=list_id, card_name=card_name)
    assert_that(card.status_code).is_equal_to(200)
    card_id = card.json()['id']
    # Act
    # Update name
    new_checklist = checklists.create_checklist(card_id=card_id)
    assert_that(new_checklist.status_code).is_equal_to(200)
    checklist_id = new_checklist.json()['id']
    upd_checklist = checklists.update_checklist(checklist_id)
    assert_that(upd_checklist.status_code).is_equal_to(200)
    # Add random amount of checkitems to checklist
    checkitems_amount = random.randint(1, 5)
    for i in range(0, checkitems_amount):
        checklists.add_checkitem_to_checklist(checklist_id, is_checked=random.choice(['true', 'false']))

    number_of_checkitems_in_chekclist = len(list(checklists.get_checkitems(checklist_id=checklist_id).json()))

    # Assert
    assert_that(number_of_checkitems_in_chekclist).is_equal_to(checkitems_amount)
    assert_that(upd_checklist.json()['name']).contains("Updated")
    boards.delete_board_by_id(board_id)


def test_delete_checklist_from_card():
    # Arrange
    board_id = boards.create_new_board()
    list_id = cards.create_new_list(board_id=board_id)
    card_name = f"Automation {uuid4()}"

    card = cards.create_new_card(list_id=list_id, card_name=card_name)
    assert_that(card.status_code).is_equal_to(200)
    card_id = card.json()['id']
    # Act
    new_checklist = checklists.create_checklist(card_id=card_id).json()
    checklist_on_card = cards.get_checklist_on_card(card_id=card_id).json()
    assert_that(checklist_on_card[0]['id']).is_equal_to(new_checklist['id'])

    delete_status_code = checklists.delete_checklist_by_id(new_checklist['id'])

    # Assert
    assert_that(delete_status_code).is_equal_to(200)
    checklist_on_card = list(cards.get_checklist_on_card(card_id=card_id).json())
    print(checklist_on_card)
    assert_that(checklist_on_card).is_empty()



    boards.delete_board_by_id(board_id)
def test_get_checklist():
    # Arrange
    board_id = boards.create_new_board()
    list_id = cards.create_new_list(board_id=board_id)
    card_name = f"Automation {uuid4()}"

    card = cards.create_new_card(list_id=list_id, card_name=card_name)
    assert_that(card.status_code).is_equal_to(200)
    card_id = card.json()['id']
    # Act
    new_checklist = checklists.create_checklist(card_id=card_id).json()
    checklist_on_card = cards.get_checklist_on_card(card_id=card_id).json()

    # Assert
    assert_that(checklist_on_card[0]['id']).is_equal_to(new_checklist['id'])

