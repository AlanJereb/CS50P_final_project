import pytest
from project import is_game_finished, restart, quit, Game
from data.words import words_five_letters, words_six_letters
from unittest.mock import MagicMock, patch, PropertyMock


def test_is_game_finished():
    game = Game()
    game.failures = 10
    assert game.is_game_finished() == True
    game.failures = 0
    game.guessed_letters = [["p", "a", "s", "s", "y"]]
    game.word = "passy"
    assert game.is_game_finished() == True
    game.guessed_letters = [["p", "a", "s", "s", ""]]
    game.word = "passy"
    assert game.is_game_finished() == False

def test_restart():
    game = Game()
    game.game_screen = 1
    game.used_letters = ["a"]
    game.failures = 5
    game.game_mode = "1"
    game.restart()
    assert game.game_screen == 0
    assert game.used_letters == []
    assert game.failures == 0
    assert game.game_mode == "0"

def test_quit():
    game = Game()
    with pytest.raises(SystemExit) as sys_exit:
        game.quit()


# Game class tests below

def test_variable_separator_length():
    game = Game()
    # Getter
    assert game.separator_length == 40
    # Setter
    game.separator_length = 20
    assert game.separator_length == 20

def test_variable_game_screen():
    game = Game()
    # Getter
    assert game.game_screen == 0
    # Setter
    game.game_screen = 10
    assert game.game_screen == 10

def test_variable_game_mode():
    game = Game()
    # Getter
    assert game.game_mode == "0"
    # Setter
    game.game_mode = "10"
    assert game.game_mode == "10"

def test_variable_guessed_letters():
    game = Game()
    # Getter
    assert game.guessed_letters == []
    # Setter
    game.guessed_letters = [["f", "o", "o"]]
    assert game.guessed_letters == ["f", "o", "o"]
    # Setter - # set a letter at a specific index
    game.guessed_letters = ["b", 0]
    assert game.guessed_letters == ["b", "o", "o"]

def test_variable_used_letters():
    game = Game()
    # Getter
    assert game.used_letters == []
    # Setter
    game.used_letters = [["f", "o", "o"]]
    assert game.used_letters == ["f", "o", "o"]
    # Setter - append
    game.used_letters = ["b", True]
    assert game.used_letters == ["f", "o", "o", "b"]

def test_variable_word():
    game = Game()
    # Getter
    assert game.word == ""
    # Setter
    game.word = "1"
    assert game.word in [word.upper() for word in words_five_letters]
    game.word = "2"
    assert game.word in [word.upper() for word in words_six_letters]

def test_failures():
    game = Game()
    # Getter
    assert game.failures == 0
    # Setter
    game.failures = 5
    assert game.failures == 5

def test_already_used_letter():
    game = Game()
    # Getter
    assert game.already_used_letter == ""
    # Setter
    game.already_used_letter = "a"
    assert game.already_used_letter == "a"

def test_game_logic(monkeypatch):
    game = Game()
    # Mocks
    game.start_game = MagicMock()
    user_inputs = iter(["invalid", "1", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "no"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    game.main_game = MagicMock()
    game.quit = MagicMock()
    with patch.object(type(game), 'word', new_callable=PropertyMock) as mock_word:
        mock_word.return_value = "AAAAA"
        # Tests
        assert game.game_screen == 0
        game.run_game()
        assert game.start_game.called
        assert game.game_screen == 1
        # Screen two
        assert game.main_game.called
        assert game.failures == 10
        assert game.used_letters == ["B", "C", "D", "E", "F", "G", "H", "I", "J", "K"]
        assert game.quit.called


# clear_terminal not tested, as it contains none of my own code, just packages

def test_user_has_failed():
    game = Game()
    game.failures = 10
    assert game.user_has_failed() == True
    game.failures = 9
    assert game.user_has_failed() == False


def test_user_has_won():
    game = Game()
    game.word = "fail"
    game.guessed_letters = [["f", "a", "i", "k"]]
    assert game.user_has_won() == False
    game.guessed_letters = ["l", 3]
    assert game.user_has_won() == True


# All print functions not tested as print is a package
