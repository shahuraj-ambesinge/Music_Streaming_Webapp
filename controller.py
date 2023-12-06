from flask import Flask, render_template, session, request, redirect
from main import app,db
from werkzeug.utils import secure_filename
from model import *
import os



#Allowed set of file format
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'mp3'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#User---------------------------------------------------------------------------------------------------------------
#User---------------------------------------------------------------------------------------------------------------
#User--------------------------------------------------------------------------------------------------------------

@app.route('/')
@app.route('/home')
def start():
    if 'user_id' in session:
        song_data = Song.query.all()
        return render_template('index.html', songs = song_data)
    else:
        return redirect('/signin')
    
@app.route('/signin')
def sign_in():
    return render_template('signin.html')


@app.route('/signup')
def sign_up():
    return render_template('signup.html')

@app.route('/login-action', methods=['POST'])
def login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    users = User.query.filter_by(email=email, password=password)
    check = []
    for user in users:
        check.append(user)
    if len(check)>=1:
        session['user_id'] = check[0].id
        return redirect('/')
    else:
        return redirect('/signin')


@app.route('/signup-action', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        print(username, email, password)
        update_user = User(fullname=username, email=email, password=password)
        db.session.add(update_user)
        db.session.flush()
    except Exception as error:
        return "{}".format(error), "user is not registered"
    else:
        db.session.commit()
        return redirect('/signin')
    
    
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/signin')


@app.route('/music_player/<int:id>')
def music_player(id):
    if 'user_id' in session:
        song_ID = id
        song_data = Song.query.filter_by(song_ID = song_ID)


        rating_check = Rating.query.filter_by(song_ID=song_ID).all()
        rating_sum = sum(rating.rating for rating in rating_check)
        rating_count = len(rating_check)
        if rating_count == 0:
            rating_avg =0
        else:
            rating_avg = round((rating_sum/rating_count), 1)
            

        user_ID = session['user_id']
        playlist_data = Playlist.query.filter_by(user_ID=user_ID)
        if not playlist_data:
            return render_template('music_player.html',  song_dictionary = song_data[0], rating_count=rating_count, rating_avg=rating_avg)
        
        return render_template('music_player.html', song_dictionary = song_data[0], playlist_list=playlist_data, rating_avg=rating_avg, rating_count=rating_count)
    else:
        return redirect('/signin')


@app.route('/action_rating_upload', methods=['POST'])
def action_handle_rating():
    if 'user_id' in session:
        try:
            rating = request.form.get('inlineRadioOptions')
            song_ID = request.form.get('song_ID')
            user_ID = session['user_id']
            check = Rating.query.filter_by(user_ID=user_ID, song_ID=song_ID).first()
            if check:
                check.rating = rating
            #-------------------------------------------------- no rating (song and user)-----------
            else:
                upload_rating = Rating(song_ID=song_ID, user_ID=user_ID, rating=rating)
                db.session.add(upload_rating)
                db.session.flush()


        except Exception as error:
            
            return "{}".format(error), "creator is not registered"

        else:
            db.session.commit()
            return redirect(f'/music_player/{song_ID}')

    else:
        return redirect('/signnin')
    

@app.route('/create_playlist_action', methods=['POST'])
def create_playlist():
    if 'user_id' in session:
        try:
            song_ID = request.form.get('song_id')
            playlist_name = request.form.get('playlistName')
            user_ID = session['user_id']
            create_playlist = Playlist(playlist_name=playlist_name, user_ID=user_ID, song_ID=song_ID)
            db.session.add(create_playlist)
            db.session.flush()

        except Exception as error:
            return "{}".format(error), "playlist not created"
        
        else:
            db.session.commit()
            return redirect(f'/music_player/{song_ID}')
    else:
        return redirect('/signin')



@app.route('/add_to_playlist_action', methods=['POST'])
def add_to_playlist_action():
    if 'user_id' in session:
        try:
            playlist_name = request.form.get('playlist_name')
            song_ID = request.form.get('song_id')
            user_ID = session['user_id']
            print(playlist_name, song_ID, user_ID)
            add_to_playlist = Playlist.query.filter_by(user_ID=user_ID, song_ID=song_ID, playlist_name=playlist_name).first()
            db.session.add(add_to_playlist)
            db.session.flush()

        except Exception as error:
            return "{}".format(error)
        
        else:
            db.session.commit()
            return redirect(f'/music_player/{song_ID}')
        
    else:
        return redirect('/signin')




#Admin-----------------------------------------------------------------------------------------------------------
#Admin-------------------------------------------------------------------------------------------------------------
#Admin--------------------------------------------------------------------------------------------------------------


@app.route('/admin_home')
def admin_start():
    if 'admin_id' in session:
        return render_template('admin_index.html')
    else:
        return redirect('/admin_signin')
    
@app.route('/admin_signin')
def admin_sign_in():
    return render_template('admin_signin.html')

@app.route('/admin_signup')
def admin_sign_up():
    return render_template('admin_signup.html')

@app.route('/admin-login-action', methods=['POST'])
def admin_login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    admins = Admin.query.filter_by(email=email, password=password)
    check = []
    for admin in admins:
        check.append(admin)
    if len(check)>=1:
        session['admin_id'] = check[0].admin_id
        return redirect('/admin_home')
    else:
        return redirect('/admin_signin')
    
    
@app.route('/admin-signup-action', methods=['POST'])
def admin_register():
    try:
        admin_name = request.form.get('admin_name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        update_admin = Admin(admin_name=admin_name, email=email, password=password, gender=gender)
        db.session.add(update_admin)
        db.session.flush()
    except Exception as error:
        return "{}".format(error), "admin is not registered"
    else:
        db.session.commit()
        return redirect('/admin_signin')
    
@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_id')
    return redirect('/admin_signin')




#Creator
#Creator---------------------------------------------------------------------------------------------------------------------------------------------------------
#Creator


@app.route('/creator_home')
def creator_start():
    if 'creator_id' in session:
        creator_ID = session['creator_id']
        album_list = Album.query.filter_by(creator_ID=creator_ID)
        return render_template('creator_index.html', album_list = album_list)
    else:
        return redirect('/creator_signin')
    

@app.route('/creator_signin')
def creator_sign_in():
    return render_template('creator_signin.html')


@app.route('/creator_signup')
def creator_sign_up():
    return render_template('creator_signup.html')


@app.route('/creator-login-action', methods=['POST'])
def creator_login_action():
    email = request.form.get('email')
    password = request.form.get('password')
    creators = Creator.query.filter_by(email=email, password=password)
    check = []
    for creator in creators:
        check.append(creator)
    if len(check)>=1:
        session['creator_id'] = check[0].creator_id
        return redirect('/creator_home')
    else:
        return redirect('/creator_signin')
    
    
@app.route('/creator-signup-action', methods=['POST'])
def creator_register():
    try:
        creator_name = request.form.get('creator_name')
        email = request.form.get('email')
        password = request.form.get('password')
        gender = request.form.get('gender')
        update_creator = Creator(creator_name=creator_name, email=email, password=password, gender=gender)
        db.session.add(update_creator)
        db.session.flush()
    except Exception as error:
        return "{}".format(error), "creator is not registered"
    else:
        db.session.commit()
        return redirect('/creator_signin')
   
@app.route('/creator_logout')
def creator_logout():
    session.pop('creator_id')
    return redirect('/creator_signin')


    
@app.route('/user-creator-login-action', methods = ['POST'])
def user_creator_login_action():
    if 'user_id' in session:
        try:
            gender = request.form.get('gender')
            password = request.form.get('password')
            user_creator = User.query.filter_by(id = session['user_id']).first()
            creator_name = user_creator.fullname
            email = user_creator.email
            update_user_creator = Creator(creator_name=creator_name, email=email, password=password, gender=gender)
            db.session.add(update_user_creator)
            db.session.flush()

        except Exception as error:
            return "{}".format(error), "employee is already registered"
        else:
            db.session.commit()
            session.pop('user_id')
            return redirect('/creator_signin')     
        
    else:
        return redirect('/signin')


@app.route('/user_creator')
def user_creator():
    if 'user_id' in session:
        return render_template('user_creator.html')
    else:
        return redirect('/signin')
    


@app.route('/profile')
def profile():
   if 'user_id' in session:
       return render_template('base_profile.html')
   else:
       return redirect('/signin')

  
@app.route('/creator_profile')
def creator_profile():
   if 'creator_id' in session:
       c_id = int(session['creator_id'])
       creator_data = Creator.query.filter_by(creator_id=c_id)
       return render_template('creator_profile.html', creator_dictionary=creator_data[0], type='Creator')
   else:
       return redirect('/creator_signin')
   

@app.route('/user_profile')
def user_profile():
   if 'user_id' in session:
       u_id = int(session['user_id'])
       user_data = User.query.filter_by(id=u_id)
       return render_template('user_profile.html', user_dictionary=user_data[0], type='user')
   else:
       return redirect('/user_signin')
   

@app.route('/song_details')
def playlist_action():
    song_ID = 3
    song_data = Song.query.filter_by(song_ID = song_ID)
    return render_template('song_details.html', song_dictionary = song_data[0])

@app.route('/song_upload')
def song_upload():
    if 'creator_id' in session:
        return render_template('song_upload.html')
    else:
        return redirect('/creator_signin')

@app.route('/song_upload_action', methods=['POST'])
def song_upload_action():
    if 'creator_id' in session:
        try:
            song_name = request.form.get('song_name')
            genre = request.form.get('genre')
            artist = request.form.get('artist')
            lyrics = request.form.get('lyrics')
            duration = request.form.get('duration')
            album = request.form.get('album')
            creator_ID = session['creator_id']
            print(creator_ID)
            filename=None
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            upload_song = Song(song_name=song_name, genre = genre,file_name=filename, artist = artist, lyrics = lyrics, duration = duration, album = album, creator_ID=creator_ID)
            db.session.add(upload_song)
            db.session.flush()
        except Exception as error:
            return "{}".format(error), "creator is not registered"
        else:
            db.session.commit()
            return redirect('/creator_home')
    else:
        return redirect('/creator_home')



    

# loading all songs in creater login
@app.route('/album/<int:id>')
def load_album(id):
    if 'creator_id' in session:
        songs = Song.query.filter_by(creator_ID=session['creator_id'], album_ID = id)
        return render_template('album.html', songs_list=songs)
    else:
        return redirect('/creator_signin')
    

#play song in creator album
@app.route('/creator_music_player/<int:id>')
def creator_music_player(id):
    if 'creator_id' in session:
        song_ID = id
        song_data = Song.query.filter_by(song_ID = song_ID)
        return render_template('creator_music_player.html', song_dictionary = song_data[0])
    else:
        return redirect('/creator_signin')
    

@app.route('/creator_list_all_songs')
def creator_list_all_songs():
    if 'creator_id' in session:
        songs_list = Song.query.all()
        return render_template('creator_song_list.html', songs=songs_list)
    else:
        return redirect('/creator_signin')
    


