# Pokemon Party Builder Dashboard

Jackson Hammond

[Link to this repository](https://github.com/jbhammon/si507_final_project)

---

## Project Description

This project is be a dashboard for users to build their Pokemon parties. The project will allow users to build parties of six pokemon for the traditional Pokemon RPG games. They can pick Pokemon based on the specific game they’re playing, and the dashboard will help them visualize how strong their party is and which types they will have trouble fighting. There will be a route for building a team one Pokemon at time. There will be another route that let’s the user view detailed information about the Pokemon they’ve added to their team.  

## How to run

1. First, you should fork this repository and clone it locally for yourself.
2. Second, you should install all requirements with `pip install -r requirements.txt`
3. Third, run `python SI507_project_tools.py runserver` from the command line in the directory you cloned this repo into.

## How to use

1. A user can create their first party on the home page by entering a name and the game they're creating it for.
2. After they submit the form a link to edit that team will be available for the user.
3. After clicking on a party a user can search for Pokemon to add to their party.
4. Users can search for Pokemon in the given form, and then see them added to the party.
5. The dashboard will then display for the user various helpful information about the team they've created.

## Routes in this application
- `/` -> this is the home page, where users see the parties they've created, and have a form available to create new ones
- `/built_team/<teamname>` -> this route has a form for user input to add pokemon to a party they've already created called <teamname>
- `/details/<pokemon>` -> this route is where users can see details about Pokemon they've added to a party

## How to run tests
1. First, at the command line run `python SI507_project_tests.py` in the directory you cloned this repo into.
2. Results of the test should print to the terminal, and the tests that passed and failed will be visible.

## In this repository:
- templates
  - index.html
  - pokemon.html
  - view_team.html
- data
  - Games.csv
  - Pokemon.csv
- .gitignore
- requirements.txt
- DB Diagram.png
- README.md
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
- [ ] Includes a `requirements.txt` file containing all required modules to run program
- [x] Includes a clear and readable README.md that follows this template
- [ ] Includes a sample .sqlite/.db file
- [ ] Includes a diagram of your database schema
- [ ] Includes EVERY file needed in order to run the project
- [ ] Includes screenshots and/or clear descriptions of what your project should look like when it is working

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
- [ ] Inclusion of JavaScript files in the application
- [x] Links in the views of Flask application page/s
- [ ] Relevant use of `itertools` and/or `collections`
- [ ] Sourcing of data using web scraping
- [ ] Sourcing of data using web REST API requests
- [x] Sourcing of data using user input and/or a downloaded .csv or .json dataset
- [ ] Caching of data you continually retrieve from the internet in some way

### Submission
- [ ] I included a link to my GitHub repository with the correct permissions on Canvas! (Did you though? Did you actually? Are you sure you didn't forget?)
- [ ] I included a summary of my project and how I thought it went **in my Canvas submission**!
