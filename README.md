# Pokemon Party Builder Dashboard

Jackson Hammond

[Link to this repository](https://github.com/jbhammon/si507_final_project)

---

## Project Description

This project is be a dashboard for users to build their Pokemon parties. The project will allow users to build parties of six pokemon for the traditional Pokemon RPG games. They can pick Pokemon based on the specific game they’re playing, and the dashboard will help them visualize how strong their party is and which types they will have trouble fighting. There will be a route for building a party one Pokemon at time. There will be another route that let’s the user view detailed information about the Pokemon they’ve added to their party.  

## How to run

1. First, you should fork this repository and clone it locally for yourself.
2. Second, you should install all requirements with `pip install -r requirements.txt`
3. Third, run `python app.py runserver` from the command line in the directory you cloned this repo into.
4. You can find the homepage of the app at http://localhost:5000/
5. This repo has an example database file for reference (SAMPLE_database_file.db), but the app will create a database file called pokemon_dashboard.db

## How to use

### IF YOU HAVE NO IDEA HOW POKEMON WORKS SEE THE END OF THIS SECTION FOR SPECIFIC STEPS YOU CAN FOLLOW TO USE THIS APP

1. A user can create their first party on the home page by typing a name and selecting the game they're creating it for. They can also choose an existing party (if there are any in the database) to edit by clicking its name.
2. After they submit the form a link to edit that party will be available for the user at the top of the page.
![Homepage](/readme_screenshots/homepage.png)
3. After clicking on a party a user can search for Pokemon to add to their party.
![Build party](/readme_screenshots/build_party_empty.png)
4. Users can search for Pokemon in the given form by their name, and then see them added to the party.
![Build party](/readme_screenshots/build_party.png)
5. Users will be told if the Pokemon they tried to add doesn't exist in the database or if it's not available in the game they chose when they created the party. The Pokemon will not be added, and they'll be presented with the form again.
![Build party](/readme_screenshots/error message one.png)
![Build party](/readme_screenshots/error message two.png)
5. The dashboard will then display for the user which types their party has no resistance to. For example, if there is no Pokemon in the party that has a resistance to (i.e. takes less damage from) Ice-type attacks, then "Ice" will be shown in the list for the user.
![Build party](/readme_screenshots/build_party_full.png)

### I don't know pokemon at all, what should I do?
1. Once you've started the app and navigated to http://localhost:5000/ click the link at the bottom to refresh the database.
2. Navigate back to the home page.
3. Type in a name for a new party, like "I'm New to Pokemon".
4. Select the "Gold Version" option in the "Game" selection section of the form.
5. Submit the form, and then click the link for the new party you just created.
6. Time to add some pokemon to the party. Notice while you add each that the list of "types this party has no resistance to" gets shorter. Search for these six pokemon: Feraligatr, Ampharos, Lugia, Gengar, Steelix, and Pidgeot. That's the party I used in the first ever Pokemon game I played, and it should only be missing a resistance to Dark-type moves.
7. Other potential options to add: Sudowoodo, Golem, Magmar, Rapidash
8. Palkia is from a future generation. If you chose "Gold Version" correctly when you created this party, you should be told you can't add that Pokemon to this party.
9. Any random string should tell you to check your spelling because that pokemon isn't in the database.
10. Click on the name of any of the Pokemon currently in the party. You'll be shown their types and overall stats.

## Routes in this application
- `/` -> this is the home page, where users see the parties they've created, and have a form available to create new ones
- `/build_team/<teamname>` -> this route has a form for user input to add Pokemon to a party they've already created called <teamname>
- `/details/<pokemon>` -> this route is where users can see details about Pokemon they've added to a party
- `/delete/<teamname>/<pokemon>` -> users are sent to this route when they remove a Pokemon from a party. It manages the data changes involved with dropping the row from the database. Users don't see anything displayed for them here, but are instead redirected to the `/built_team/<teamname>` route.
- '/db_refresh' -> Users are given a link to this route from the home page. By navigating here users are able to refresh the database. All the tables are dropped and created again, and the "Game" and "Pokemon" tables are filled in from the appropriate .csv files in the `/data` directory. All the parties users have created will be gone, and they're able to start again fresh.

## How to run tests
1. First, at the command line run `python SI507_project_tests.py` in the directory you cloned this repo into.
2. Results of the test should print to the terminal, and the tests that passed and failed will be visible.

## In this repository:
- data
  - Games.csv
  - Pokemon.csv
- readme_screenshots
  - Various screenshots of the app running that are linked above
- static
  - js
    - lib
    - main_scripts.js
- templates
  - index.html
  - pokemon.html
  - refresh.html
  - view_team.html
- .gitignore
- DB Diagram.png
- SAMPLE_database_file.db
- README.md
- requirements.txt
- SI507project_tests.py
- SI507project_tools.py

---
## Code Requirements for Grading
Please check the requirements you have accomplished in your code as demonstrated.
- [x] This is a completed requirement.
- [ ] This is an incomplete requirement.

Below is a list of the requirements listed in the rubric for you to copy and paste.  See rubric on Canvas for more details.

### General
- [x] Project is submitted as a Github repository
- [x] Project includes a working Flask application that runs locally on a computer
- [x] Project includes at least 1 test suite file with reasonable tests in it.
- [x] Includes a `requirements.txt` file containing all required modules to run program
- [x] Includes a clear and readable README.md that follows this template
- [x] Includes a sample .sqlite/.db file
- [x] Includes a diagram of your database schema
- [x] Includes EVERY file needed in order to run the project
- [x] Includes screenshots and/or clear descriptions of what your project should look like when it is working

### Flask Application
- [x] Includes at least 3 different routes
- [x] View/s a user can see when the application runs that are understandable/legible for someone who has NOT taken this course
- [x] Interactions with a database that has at least 2 tables
- [x] At least 1 relationship between 2 tables in database
- [x] Information stored in the database is viewed or interacted with in some way

### Additional Components (at least 6 required)
- [ ] Use of a new module
- [ ] Use of a second new module
- [ ] Object definitions using inheritance (indicate if this counts for 2 or 3 of the six requirements in a parenthetical)
- [x] A many-to-many relationship in your database structure
- [x] At least one form in your Flask application
- [x] Templating in your Flask application
- [x] Inclusion of JavaScript files in the application
- [x] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [ ] Sourcing of data using web scraping
- [ ] Sourcing of data using web REST API requests
- [x] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [ ] Caching of data you continually retrieve from the internet in some way

### Submission
- [x] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [x] I included a summary of my project and how I thought it went **in my Canvas submission**!
