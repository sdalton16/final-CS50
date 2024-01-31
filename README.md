# MATH!
Built by Sheamus Dalton (Denver, CO) | Fall 2023
## Video Demo:  <https://youtu.be/ovXrPSmzeUo>
## Description:
#### Summary:
Math! is a web-based application using Python, Javascript and SQL. The app offers two game modes to users — 1. Addition & Subtraction! and 2. Multiplication & Division. The app requires users to login and has a leaderboard for both game modes to track the highest scores ('streaks') across all games played by all users.

#### Game Modes:
Both game modes are built with the same general structure and functionality. The app randomly generates problems for the user to solve. The user is presented with 4 randomly-generated solutions (with one problem being the correct answer, of course) and the app evaluates the user's selection for a correct answer. The app tracks a user's correct answer 'streak' during each individual game. During each game, for each consecutive correct answer, the user's current game streak is incremented. If the user answers a problem incorrectly, their current game streak is reset to zero. The user is able to save their game at any time after answering the first problem. When the user saves their game, that game is over and their streak is logged in the app's database.

#### Leaderboard:
Math! has a leaderboard page where the top user streaks for both game modes are displayed. The leaderboards are ordered starting with the higest score and each line in the leaderboard includes the user's username, streak and the date of their game.

#### Register/Login:
The app requires users to register and to be logged in to play a game. This is required so that the app can track high scores to display on the leaderboard. If a user is not logged in as a registered user, they will only be able to access the login and register pages.

#### Additional detail:
Math! is written in Python and utilizes the Flask framework. To track and store user data, the app utilizes SQLite3. The app has 6 html pages and one CSS stylesheet. The two primary pages 'add_sub' and 'multiply_divide' include Javascript code that creates the game mode functionality. There is code to randomly generate problems, immediately evaluate the user's answer, adjust the display based on the user's streak and save the game by passing the user's current game streak back to the python application where it is saved to the database. Additional functions of the application include requiring a user to register with a unique username, prompting the user to try again if their login attempt is failed and allowing the user to logout.
