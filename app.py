#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
# used to format date time
import dateutil.parser
import babel

#Suggestion: You can shorten the length of this line of code like this:
from flask import (
  Flask, 
  render_template, 
  request, 
  Response, 
  flash, 
  redirect, 
  url_for
)

import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from forms import *
import sys
from sqlalchemy import exc


#Required: Move the models to a separate file, for example, models.py, so that the code is cleaner and loosely coupled.

from models import *
# Import everything from models.py, you can comment two lines below:
#app = Flask(__name__)
##db.init_app(app)


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
# Config
# are found in ./models.py

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
# Models are found in ./models.py



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------


@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.

  data = []
  
  # Query All venues
  venues = Venue.query.all()

  # Use set to avoid any duplicates
  places = set()

  for venue in venues:
    places.add((venue.city, venue.state))

  for place in places:
    data.append({
        "city": place[0],
        "state": place[1],
        "venues": []
    })

  for venue in venues:
    num_upcoming_shows = 0

    shows = Show.query.filter_by(venue_id=venue.id).all()

    # get current date to filter num_upcoming_shows
    timeNow = datetime.now()

    for show in shows:
      if show.start_time > timeNow:
          num_upcoming_shows += 1

    for venue_place in data:
      if venue.state == venue_place['state'] and venue.city == venue_place['city']:
        venue_place['venues'].append({
            "id": venue.id,"name": venue.name,"num_upcoming_shows": num_upcoming_shows
        })
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # Declare searched keyword
  search_term = request.form.get('search_term', '')
  result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  response={"count": result.count(),"data": result}
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
  venue = Venue.query.get(venue_id)
  shows = Show.query.filter_by(venue_id=venue_id).all()
  #REQUIRED: It is necessary to implement JOIN here. The rubric requires JOIN in two points only:
  past_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
    filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time < datetime.now()
    ).\
    all()
    
  upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
    filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time > datetime.now()
    ).\
    all()
    
  data = {
    "id": venue.id,"name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link": venue.image_link,
        'past_shows': [{
            'artist_id': artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in past_shows],
        'upcoming_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
  }

  return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  try:
    # get form data and create 
    form = VenueForm()
    venue = Venue(name=form.name.data, 
                  genres=form.genres.data, 
                  address=form.address.data,
                  city=form.city.data, 
                  state=form.state.data,
                  phone=form.phone.data,
                  image_link=form.image_link.data,
                  facebook_link=form.facebook_link.data,
                  website=form.website.data,
                  seeking_talent=form.seeking_talent.data,
                  seeking_description=form.seeking_description.data
    )          
    db.session.add(venue)
    db.session.commit()
    flash('[OK] Venue ' + request.form['name'] + ' was added successfully.')
  except :
    #https://stackoverflow.com/questions/2136739/error-handling-in-sqlalchemy
    # catches errors
    db.session.rollback()
    #flash(sys.exc_info())
    flash( sys.exc_info())
  finally:
    # close session
    db.session.close()
  return render_template('pages/home.html')
  
@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    # Get venue by ID
    venue = Venue.query.get(venue_id)
    venue_name = venue.name
    db.session.delete(venue)
    db.session.commit()
    flash('[OK] Venue ' + venue_name + ' was deleted successfully.')
  except:
    flash('[ERROR] Venue ' + venue_name + ' was not deleted.')
    db.session.rollback()
  finally:
    db.session.close()
    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    data = db.session.query(Artist).all()
    return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term', '')

  # filter artists results by case insensitive search
  result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))

  response={
    "count": result.count(),"data": result
  }

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))



@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id
      #venue = Venue.query.get(venue_id)
      
        #venue = Venue.query.get(venue_id)
        getArtistData = db.session.query(Artist).get(artist_id)
        #shows = Show.query.filter_by(artist_id=artist_id).all()


        #Begin new objects
        
        #REQUIRED: It is necessary to implement JOIN here. The rubric requires JOIN in two points only:
        past_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
          filter(
              Show.venue_id == Venue.id,
              Show.artist_id == artist_id,
              Show.start_time < datetime.now()
          ).\
          all()
          
        upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
          filter(
              Show.venue_id == Venue.id,
              Show.artist_id == artist_id,
              Show.start_time > datetime.now()
          ).\
          all()        


        data = {
                  "id": getArtistData.id,
                  "name": getArtistData.name,
                  "genres": getArtistData.genres,
                  "city": getArtistData.city,
                  "state": getArtistData.state,
                  "phone": getArtistData.phone,
                  "website": getArtistData.website,
                  "facebook_link": getArtistData.facebook_link,
                  "seeking_venue": getArtistData.seeking_venue,
                  "seeking_description": getArtistData.seeking_description,
                  "image_link": getArtistData.image_link,
                  

              'past_shows': [{
                  'artist_id': artist.id,
                  "artist_name": artist.name,
                  "artist_image_link": artist.image_link,
                  "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
              } for artist, show in past_shows],
              'upcoming_shows': [{
                  'artist_id': artist.id,
                  'artist_name': artist.name,
                  'artist_image_link': artist.image_link,
                  'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
              } for artist, show in upcoming_shows],
              'past_shows_count': len(past_shows),
              'upcoming_shows_count': len(upcoming_shows)
        }       
        
 
        return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>
  #return render_template('forms/edit_artist.html', form=form, artist=artist_data)
  form = ArtistForm()
  artist = Artist.query.get(artist_id)
  if artist: 
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.website.data = artist.website
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description
    
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
  try:
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    artist.name = form.name.data
    artist.name = form.name.data
    artist.phone = form.phone.data
    artist.state = form.state.data
    artist.city = form.city.data
    artist.genres = form.genres.data
    artist.image_link = form.image_link.data
    artist.facebook_link = form.facebook_link.data
    artist.website = form.website.data
    artist.seeking_venue = form.seeking_venue.data
    artist.seeking_description = form.seeking_description.data
       
    db.session.commit()
    flash('[OK] Artist ' + request.form['name'] + ' was updated successfully.')
  except:
    db.session.rolback()
    flash('[ERROR] Artist details was not updated due to errors.')
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)

  #do if venue is found
  if venue: 
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.address.data = venue.address
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website.data = venue.website
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
  try:
    form = VenueForm()
    venue = Venue.query.get(venue_id)
    
    name = form.name.data
    venue.name = name
    
    venue.genres = form.genres.data
    venue.city = form.city.data
    venue.state = form.state.data
    venue.address = form.address.data
    venue.phone = form.phone.data
    venue.facebook_link = form.facebook_link.data
    venue.website = form.website.data
    venue.image_link = form.image_link.data
    venue.seeking_talent = form.seeking_talent.data
    venue.seeking_description = form.seeking_description.data

    db.session.commit()
    flash('[OK] Venue ' + name + ' was updated successfully')
  except:
    db.session.rollback()
    flash('[ERROR] An error occured while trying to update Venue')
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new Venue record in the db, instead

    try:
        # SUCCESS
        form = ArtistForm()
        # TODO: modify data to be the data object returned from db insertion
        newArtist = Artist(name=form.name.data,
                           city=form.city.data,
                           state=form.city.data,
                           phone=form.phone.data,
                           genres=form.genres.data,
                           image_link=form.image_link.data,
                           facebook_link=form.facebook_link.data, 
                           website=form.website.data, 
                           seeking_venue=form.seeking_venue.data, 
                           seeking_description=form.seeking_description.data
                           )
        # TODO: insert form data as a new Venue record in the db, instea
        db.session.add(newArtist)
        db.session.commit()
        # Show successful message
        flash('[OK] Congratulations! Artist ' + request.form['name'] + ' was successfully added!')
    except:
        # FAIL
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        db.session.rollback()
        flash('[ERROR] Artist ' + request.form['name'] + ' could not be added.')
    finally:
        # END SESSION
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------


@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
  shows = Show.query.order_by(db.desc(Show.start_time))
  data = []

  for show in shows:
    data.append({
        "venue_id": show.venue_id,"venue_name": show.venue.name,"artist_id": show.artist_id,"artist_name": show.artist.name,"artist_image_link": show.artist.image_link,"start_time": format_datetime(str(show.start_time))
    })

  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead

    # on successful db insert, flash success
 
  try:
    show = Show(artist_id=request.form['artist_id'], 
                venue_id=request.form['venue_id'],
                start_time=request.form['start_time']
                )

    db.session.add(show)
    db.session.commit()

    flash('[OK] Congratulations! Show was successfully added!')
  except:
    db.session.rollback()
    
    flash('[ERROR] We detected an error. Show was NOT added.')
  finally:
    db.session.close()

  

    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
