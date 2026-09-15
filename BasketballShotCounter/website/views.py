from flask import Blueprint, render_template, request
from . import db
from .models import UserStats
from flask_login import login_required,  current_user
from .shot_tracker import shot_counter
from pathlib import Path

views = Blueprint('views', __name__) 


@views.route('/', methods = ['GET','POST']) 
@login_required

def homepage():

    new_stats = UserStats.query.filter_by(user=current_user.id).order_by(UserStats.id.desc()).first()
    processing_error = None
    
    if request.method == 'POST':  

        shot_type = request.form.get('shot_type')
        
        video = request.files.get('video')
        

        video_folder = Path(__file__).parent / "videos"
        video_folder.mkdir(exist_ok=True)
        file_path = str(video_folder / video.filename)

        video.save(file_path)

        #runs shot_counter program on uploaded file and gets the output dictionary
        stats = shot_counter(file_path)

        
        if "error" in stats:
            processing_error = stats["error"]
        
        else:
            shot_count = stats["shot_count"] 
            make_count = stats["make_count"] 
            field_goal = stats["FG"] 
      
            
            new_stats = UserStats(user = current_user.id, shot_type = shot_type, shot_count = shot_count, make_count = make_count, field_goal = field_goal)

            db.session.add(new_stats)
            db.session.commit()

    #shot type chosen in drop down list in the all-time analytics box
    alltime_shot_type = request.args.get('alltime_shot_type')

    
    alltime_stats = None
    alltime_nba_comparison = ""

    
    if alltime_shot_type:

        total_stats = UserStats.query.filter_by(shot_type = alltime_shot_type, user = current_user.id).all()

        #gets the total of all of the shot attempts and makes under the chosen shot type
        total_shot_attempts = sum(stat.shot_count for stat in total_stats)
        total_shot_makes = sum(stat.make_count for stat in total_stats)

        if total_shot_attempts == 0:
            alltime_field_goal = 0
        else:
            
            alltime_field_goal = round((total_shot_makes/total_shot_attempts)*100, 2)     

        if alltime_field_goal == 0:
            alltime_nba_comparison = "No one!"
        elif alltime_field_goal < 30:
            alltime_nba_comparison = "Dejounte Murray"
        elif alltime_field_goal < 50:
            alltime_nba_comparison = "LeBron James"
        elif alltime_field_goal < 70:
            alltime_nba_comparison = "Kevin Durant"
        else:
            alltime_nba_comparison = "Wilt Chamberlain"
  

        alltime_stats = {'total_shot_attempts': total_shot_attempts, 'total_shot_makes': total_shot_makes, 'alltime_field_goal': alltime_field_goal, 'alltime_nba_comparison': alltime_nba_comparison}


    
    if new_stats:
        
        if new_stats.field_goal == 0:
            nba_comparison = "No one!"
        elif new_stats.field_goal < 30:
            nba_comparison = "Dejounte Murray"
        elif new_stats.field_goal < 50:
            nba_comparison = "LeBron James"
        elif new_stats.field_goal < 70:
            nba_comparison = "Kevin Durant"
        else:
            nba_comparison = "Wilt Chamberlain"
    else:
        nba_comparison = None
        

    return render_template("homepage.html", user = current_user, new_stats = new_stats, alltime_stats = alltime_stats, alltime_shot_type = alltime_shot_type, nba_comparison = nba_comparison, alltime_nba_comparison = alltime_nba_comparison, processing_error = processing_error)

