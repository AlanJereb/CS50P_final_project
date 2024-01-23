# HANGMAN - the game
#### Video Demo: https://www.youtube.com/watch?v=OJfoCAhXnzY
#### Description:
This is my final project for the CS50P class.
I've coded a CLI-only Hangman game.

### Game description:
The game follows standard hangman game rules:
- You have 10 wrong tries to try to guess the word letter-by-letter
- You cannot repeat already guessed letters
- If you correctly guess the letter, it does not count towards your total of 10 tries
- If you reach 10 failed tries the game ends and you lose
- If you guess the word before reaching 10 tries you win

The game has two modes:
- Normal mode | 5-letter random English word
- Hard mode | 6-letter random English word

As per standard hangman game, for each unsuccessfull try, a part of hangman is drawn. If you reach 10 failed
tries a full picture will be drawn.

After completing the game (winning or losing), you have an option to start another game or quit the program.

### Code structure:
`project.py` - as per guidelines consists of a main function and three functions on the same level, needing for testing. I have however, for state-keeping reasons initialized and kept all of my game inside a Game class, which is in the same file. I wanted to avoid using global variables.

The three required functions that are on the same indentation level as the main function, implement calls to Game class methods, so that requirements are fullfiled. But I must point out, that also all Class methods were thoroughly tested.

`test_project.py` - contains all the tests of the project

`requirements.txt` - contains all package dependencies and their versions used in the project

`data/words.py` - contains two lists of five-letter and six-letter English words used when picking ingame modes

`components/separators.py` - contains functions used to draw hangman game inside the CLI

`components/stages.py` - contains stages of each of the wrong guess drawings for the hangman game
Stages are on purpose not following DRY principle, so they are easier to mantain and easier to review. If this was a bigger app, where performance would be critical, these stages + start screen drawings could be optimised.

### Game code walkthough:
As already mentioned beforehand, class `Game` encapsulates the whole game logic.
Here is the breakdown of key methods and their properties:
 - `__init__`: This method initializes game related variables which are used both for rendering CLI game building blocks and for game logic.
 - **Getters and Setters**: I've used these properties, to both "prevent" direct manipulation with __init__ initialized state variables and to control the way of how these variables should be updated and retrieved.
 - `run_game`: This is how you start the game. It uses a `while True` loop and `input` functions to stop and wait on each of the loop's iterations. It controls the whole flow of the game logic by running other methods like `start_game` and `main_game`. It is also responsible for most of the state variable changes.
 - `start_game`: Shows the initial CLI screen users sees when starting the game. On this screen user is prompted to select the game difficulty. Based on the selection, `run_game` method sets the a random `word` to guess and guides user on to the main game screen. Otherwise this method has no special logic, it is just responsible for game drawing.
 - `main_game`: Show the main game CLI screen, which through `run_game` tracks already used letters, correct user guesses, and draws stages of the hangman painting for each of the 10 failed attempts. After 10 failed attempts or successfull game completion, user is prompted for a game restart, which transfers player back on to the initial screen, or to terminate the game, which exits the program. Otherwise this method has no special logic, it is just responsible for game drawing.
 - `clear_terminal`: The method is used to clear all of the terminal contents, and thus give an illusion of "animation" when different page stages are rerendered inside in `main_game` portion of the `run_game`
 - `restart`: Method sets variables to the default values, so that the `run_game` while loop puts player back on to the `start_game` screen
 - `quit`: Method prints a message that it is quitting and quits the program
 - `is_game_finished`: A helper method to determine if the game has ended (user has won or lost)
 - `user_has_failed`: A helper method to determine if the user has lost
 - `user_has_won`: A helper method to determine is the user has won
 - `empty_space`: A method used for CLI rendering to prevent repetition - DRY. Even if a lot more code could still be made less repetitive.

This section overviews the main logic of how the game works.

### Future plans:
I plan to add a file which will save game stats:
- number of games
- number of lost games
- number of won games

Using data from the file, CLI render will be updated with game statistics as user finishes games.

### Conclustion:
Even though I already program professionaly, and didn't have much expectations of CS50P course, I must say I was positively surprised. I learned a lot more than I could have imagined. The devil is in the details.
Thank you for your time and reading through this readme file.
