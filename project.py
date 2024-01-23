import os
import platform
import sys
import random
from data.words import words_five_letters, words_six_letters
from components.separators import center_text, draw_separator
import components.stages as stage


class Game:
    def __init__(self):
        self.separator_length = 40
        self.game_screen = 0
        self.game_mode = "0"
        self.guessed_letters = []
        self.used_letters = []
        self.word = ""
        self.failures = 0
        self.already_used_letter = ""

    # ##############################
    # # Getters & Setters
    # ##############################

    @property
    def game_screen(self):
        return self._game_screen

    @game_screen.setter
    def game_screen(self, n):
        self._game_screen = n


    @property
    def game_mode(self):
        return self._game_mode

    @game_mode.setter
    def game_mode(self, n):
        self._game_mode = n


    @property
    def guessed_letters(self):
        return self._guessed_letters

    @guessed_letters.setter
    def guessed_letters(self, new_values):
        if len(new_values) == 2 and 0 <= new_values[1] < len(self.guessed_letters):
            self._guessed_letters[new_values[1]] = new_values[0]
        elif len(new_values) == 1:
            self._guessed_letters = new_values[0]
        else:
            self._guessed_letters = []


    @property
    def used_letters(self):
        return self._used_letters

    @used_letters.setter
    def used_letters(self, new_values):
        if len(new_values) == 2 and new_values[1]:
            self._used_letters.append(new_values[0])
        elif len(new_values) == 1:
            self._used_letters = new_values[0]
        else:
            self._used_letters = []


    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, n):
        if n == "1":
            self._word = random.choice(words_five_letters).upper()
        elif n == "2":
            self._word = random.choice(words_six_letters).upper()
        else:
            self._word = n # for testing purposes


    @property
    def failures(self):
        return self._failures

    @failures.setter
    def failures(self, n):
        self._failures = n


    @property
    def already_used_letter(self):
        return self._already_used_letter

    @already_used_letter.setter
    def already_used_letter(self, n):
        self._already_used_letter = n


    ##############################
    # Methods
    ##############################

    """
    Game logic
    """
    def run_game(self):
        self.clear_terminal()
        while self.game_screen <= 1:
            if self.game_screen == 0:
                self.start_game()
                while self.game_mode != "1" and self.game_mode != "2":
                    user_input = input("Mode: ")
                    self.game_mode = user_input
                self.word = user_input
                self.guessed_letters = [[" " for _ in range(len(self.word))]]
                self.game_screen = 1
            elif self.game_screen == 1:
                self.clear_terminal()
                self.main_game()
                if self.is_game_finished():
                    user_input = input("Decision: ").upper()
                else:
                    user_input = input("Guess a letter: ").upper()
                self.already_used_letter = ""
                if len(user_input) == 1 and user_input.isalpha():
                    ###
                    ## check if hit, miss, or repeat guess
                    # hit
                    if user_input in self.word and user_input not in self.used_letters:
                        indexes_of_hit = [index for index, char in enumerate(self.word) if char == user_input]
                        for index in indexes_of_hit:
                            self.guessed_letters = [user_input, index]
                    # repeat
                    elif user_input in self.used_letters:
                        self.already_used_letter = user_input
                    # miss
                    else:
                        self.failures = self.failures + 1
                    ###
                    # add to used letters list
                    if user_input not in self.used_letters:
                        self.used_letters = [user_input, True]
                elif user_input == "YES":
                    self.restart()
                elif user_input == "NO":
                    self.quit()
                    break


    """
    This is the first screen of the game, where user is presented with options:
    - [1] - Normal mode (5-letter words)
    - [2] - hard mode (6-letter words)

    It contains only the render logic
    """
    def start_game(self):
        draw_separator(self.separator_length)
        draw_separator(self.separator_length)
        self.empty_space()
        self.empty_space()
        self.empty_space()
        center_text(text="HANGMAN", length=self.separator_length, draw_border=True, double_border=True)
        self.empty_space()
        self.empty_space()
        self.empty_space()
        draw_separator(self.separator_length)
        draw_separator(self.separator_length)
        self.empty_space()
        center_text(text="Enter mode to start the game", length=self.separator_length, draw_border=True)
        center_text(text="[1] - Normal mode", length=self.separator_length, draw_border=True)
        center_text(text="[2] - Hard mode", length=self.separator_length, draw_border=True)
        self.empty_space()
        draw_separator(self.separator_length)
        print("2023 - Alan Jereb".rjust(self.separator_length))
        center_text(text="", length=self.separator_length)


    """
    This is the second and last screen of the game.
    It draws the hangman drawing based on the number of total failures.

    If you complete the game before 10 failures, it prints you: 'You win!, otherwise it prints you 'You lose!'
    After completing the game, it show you the option:
    - To play another game type: yes
    - To quit the game type: no

    It contains only the render logic
    """
    def main_game(self):
        draw_separator(self.separator_length)
        self.empty_space()

        stage_functions = [stage.zero, stage.one, stage.two, stage.three, stage.four, stage.five, stage.six,
                           stage.seven, stage.eight, stage.nine, stage.ten]

        if 0 <= self.failures <= 10:
            stage_functions[self.failures](self.separator_length)

        self.empty_space()
        self.empty_space()
        if self.user_has_won():
            center_text(text="You win!", length=self.separator_length, draw_border=True, double_border=True)
        elif self.user_has_failed():
            center_text(text="You lose!", length=self.separator_length, draw_border=True, double_border=True)
        self.empty_space()
        if not self.user_has_failed():
            center_text(text=("  ".join(self.guessed_letters)), length=self.separator_length, draw_border=True, double_border=True)
            center_text(text=("__ " * len(self.word)), length=self.separator_length, draw_border=True, double_border=True)
        else:
            center_text(text=self.word, length=self.separator_length, draw_border=True, double_border=True)
        self.empty_space()
        draw_separator(self.separator_length)
        if self.is_game_finished():
            center_text(text="To play another game type: yes", length=self.separator_length, draw_border=True)
            center_text(text="To quit the game type: no", length=self.separator_length, draw_border=True)
        else:
            center_text(text="Used letters:", length=self.separator_length, draw_border=True)
            center_text(text=", ".join(self.used_letters[0:9]), length=self.separator_length, draw_border=True)
            center_text(text=", ".join(self.used_letters[9:]), length=self.separator_length, draw_border=True)
        draw_separator(self.separator_length)
        if len(self.already_used_letter):
            print("You have already used letter", self.already_used_letter ,"!")
        else:
            center_text(text="", length=self.separator_length)
        center_text(text="", length=self.separator_length)


    """
    Clears CLI terminal, so that it gives a feeling of 'animation' when pages are rerendering
    """
    def clear_terminal(self):
        if platform == "Windows":
            os.system("cls")
        else:
            os.system("clear")


    """
    Resets game to default screen
    """
    def restart(self):
        self.clear_terminal()
        self.game_screen = 0
        self.used_letters = []
        self.failures = 0
        self.game_mode = "0"


    """
    Quits game
    """
    def quit(self):
        print("Quitting...")
        sys.exit()


    """ Helpers """
    def is_game_finished(self):
        return self.failures == 10 or "".join(self.guessed_letters) == self.word


    def user_has_failed(self):
        return self.failures == 10


    def user_has_won(self):
        return "".join(self.guessed_letters) == self.word

    # draws empty space in the game CLI
    def empty_space(self):
        return center_text(text="", length=self.separator_length, draw_border=True, double_border=True)
    ##############################

game = Game()

###############################
# Helpers - reimplementing them, to satisfy project requirements,
# as game logic should be in the game class, not scattered here.
# I have however also tested the functions inside the Game class
###############################

def is_game_finished():
    return game.is_game_finished()

def restart():
    return game.restart()

def quit():
    return game.quit()

###############################


def main():
    game.run_game()


if __name__ == "__main__":
    main()
