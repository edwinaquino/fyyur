Fyyur App
-----

### Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner.

### Overview

This app is nearly complete. It is only missing one thing… real data! The views and controllers are defined in this application, it contains the models and model interactions to be able to store retrieve, and update data from a PostgreSQL database. Upon successful installation, you will have a fully functioning site that is at least capable of doing the following, if not more, using a PostgreSQL database:

* creating new venues, artists, and creating new shows.
* searching for venues and artists.
* learning more about a specific artist or venue.

If you would like Fyyur to be the next new platform that artists and musical venues can use to find each other, and discover new music shows. You can make that happen!

### Tech Stack

The tech stack will include:

* **SQLAlchemy ORM** to be our ORM library of choice
* **PostgreSQL** as our database of choice
* **Python3** and **Flask** as our server language and server framework
* **Flask-Migrate** for creating and running schema migrations
* **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for our website's frontend

### Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app. 
                    "python app.py" to run after installing dependences
  ├── config.py *** Database URLs, CSRF generation, etc
  ├── models.py Includes your SQLAlchemy models used by the app.py
  ├── error.log  
  ├── forms.py *** Your forms
  ├── requirements.txt *** The dependencies we need to install with "pip3 install -r requirements.txt"
  ├── static
  │   ├── css 
  │   ├── font
  │   ├── ico
  │   ├── img
  │   └── js
  └── templates
      ├── errors
      ├── forms
      ├── layouts
      └── pages
  ```

Overall:
* Models are located in the `models.py` file and imported to `app.py`.
* Controllers are located in `app.py`.
* The web frontend is located in `templates/`, which builds static assets deployed to the web server at `static/`.
* Web forms for creating data are located in `form.py`


Highlight folders:
* `templates/pages` -- Defines the pages that are rendered to the site. These templates render views based on data passed into the template’s view, in the controllers defined in `app.py`. These pages successfully represent the data to the user, and are already defined for you.
* `templates/layouts` -- Defines the layout that a page can be contained in to define footer and header code for a given page.
* `templates/forms` -- Defines the forms used to create new artists, shows, and venues.
* `app.py` -- Defines routes that match the user’s URL, and controllers which handle data and renders views to the user. This is the main file you will be working on to connect to and manipulate the database and render views with data to the user, based on the URL.
* Models in `app.py` -- (Missing functionality.) Defines the data models that set up the database tables.
* `models.py` -- Defines the SQLAlchemy classes to connect to a PostgreSQL database.
* `config.py` -- Stores configuration variables and instructions, separate from the main application code. This is where you will need to connect to the database.


Instructions
-----

1. Understand the Project Structure (explained above) and where important files are located.
2. Build and run local development following the Development Setup steps below.
3. This application pulls data form a PostgreSQL database and needs to connect to a real database and talk to a real backend.
3. The following are the files you will need to modify to adjust to your specific platform:

  1. Connect to a database in `config.py`. Provide a username, password and database name.
  2. Using SQLAlchemy, set up normalized models for the objects we support in our web app in the Models section of `app.py`. after a successful connection, add new Venues, Artists and Shows, then check out the  pages provided at /artists/1, /venues/1, and /shows/1 for examples of the data we want to model, using all of the learned best practices in database schema design.
  3. Contains form submissions for creating new Venues, Artists, and Shows. There is proper constraints, powering the `/create` endpoints that serve the create form templates, to avoid duplicate or nonsensical form submissions. Submitting a form creates proper new records in the database.
  4. Contains controllers for listing venues, artists, and shows. Note the structure of the mock data used.
  5. Contains search, powering the `/search` endpoints that serve the application's search functionalities.
  6. Serve venue and artist detail pages, powering the `<venue|artist>/<id>` endpoints that power the detail pages.


Performance Criteria
-----

1. The web app successfully connects to a PostgreSQL database. A local connection to a database on your local computer is fine.
2. There is no use of mock data throughout the app.
3. The application uses real data from a real backend server, with real search functionality. For example:
  * when a user submits a new artist record, the user is be able to see it populate in /artists, as well as search for the artist by name and have the search return results.
  * Users will be able to go to the URL `/artist/<artist-id>` to visit a particular artist’s page using a unique ID per artist, and see real data about that particular artist.
  * Venues will continue to be displayed in groups by city and state.
  * Search is allowed to be partial string matching and case-insensitive.
  * Past shows versus Upcoming shows are distinguished in Venue and Artist pages.
  * A user is able to click on the venue for an upcoming show in the Artist's page, and on that Venue's page, see the same show in the Venue Page's upcoming shows section.
4. As a fellow developer on this application, you will be able to run `flask db migrate`, and have your local database be populated with the right tables to run this application and have it interact with your local postgres server, serving the application's needs completely with real data you can seed your local database with.
  * The models is completed (see TODOs in the `Models` section of `app.py`) and model the objects used throughout Fyyur.
  * The right _type_ of relationship and parent-child dynamics between models is accurately identified and fit the needs of this particular application.
  * The relationship between the models is accurately configured, and referential integrity amongst the models is preserved.
  * `flask db migrate`  works and populates your local postgres database with properly configured tables for this application's objects, including proper columns, column data types, constraints, defaults, and relationships that completely satisfies the needs of this application. The proper type of relationship between venues, artists, and shows is configured.


Best of luck deploying and enjoying this app!

### Development Setup

First, [install Flask](http://flask.pocoo.org/docs/1.0/installation/#install-flask) if you haven't already.

  ```
  $ cd ~
  $ sudo pip3 install Flask
  ```

To start and run the local development server,

1. Clone this repo
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ git clone [PATH TO THIS REPO]
  ```

2. Initialize and activate a virtualenv:
  ```
  $ cd YOUR_PROJECT_DIRECTORY_PATH/
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  or
  $ pip3 install -r requirements.txt
  ```

4. Run the development server:
  ```
  $ export FLASK_APP=myapp
  $ export FLASK_ENV=development # enables debug mode
  $ python3 app.py
  or
  $ python app.py
  ```

5. Navigate to Home page [http://localhost:5000](http://localhost:5000)
