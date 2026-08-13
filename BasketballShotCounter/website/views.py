from flask import Blueprint, render_template, request 
from . import db 
from .models import UserStats 
from flask_login import login_required,  current_user 
from .shot_tracker import shot_counter 
 
views = Blueprint('views', __name__) #creates a blueprint for views routes 
 
#each @auth.route() gives the url for that page 
#function defines what happens when the user goes to that page 
 
@views.route('/', methods = ['GET','POST'])  
@login_required 
 
def homepage(): 
 
    #variable that stores the recent videos statistics 
    new_stats = UserStats.query.filter_by(user=current_user.id).order_by(UserStats.id.desc()).first() 
    processing_error = None 
     
    if request.method == 'POST':   
 
        #gets the shot type selected by the user 
        shot_type = request.form.get('shot_type') 
        #gets the video file uploaded by the user 
        video = request.files.get('video') 
         
        #where the uploaded file will be stored 
        file_path = "E:/NEAPROJECT/Code/WEBSITE/website/videos/" + video.filename 
 
        #saves the video in a local folder called 'videos' 
        video.save(file_path) 
 
        #runs shot_counter program on uploaded file and gets the output dictionary 
        stats = shot_counter(file_path) 
 
        #if the shot tracker produces an error 
        if "error" in stats: 
            processing_error = stats["error"] 
        #shot tracker has successfully processed the video 
        else: 
            shot_count = stats["shot_count"] #gets the value in the 'shot_count' key  
            make_count = stats["make_count"] #gets the value in the 'make_count' key  
            field_goal = stats["FG"] #gets the value in the 'field_goal' key  
       
            #creates a new object with the most recent videos' shot statistics 
            new_stats = UserStats(user = current_user.id, shot_type = shot_type, shot_count = shot_count, make_count = make_count, field_goal = field_goal) 
 
            #adds the new stats to the database 
            db.session.add(new_stats) 
            db.session.commit() 
 
    #shot type chosen in drop down list in the all-time analytics box 
    alltime_shot_type = request.args.get('alltime_shot_type') 
 
    #variable that stores the users all-time statistics 
    alltime_stats = None 
 
    #variable that stores the users all time nba comparison 
    alltime_nba_comparison = "" 
 
    #if a shot type is chosen in the alltime analytics box 
    if alltime_shot_type: 
 
        #gets all of the stats for the selected shot type and the users id 
        total_stats = UserStats.query.filter_by(shot_type = alltime_shot_type, user = current_user.id).all() 
 
        #gets the total of all of the shot attempts and makes under the chosen shot type 
        total_shot_attempts = sum(stat.shot_count for stat in total_stats) 
        total_shot_makes = sum(stat.make_count for stat in total_stats) 
 
        #to stop it from dividing by 0 
        if total_shot_attempts == 0: 
            alltime_field_goal = 0 
        else: 
            #calculates the all time field goal percentage and rounds it to 2 decimal places 
            alltime_field_goal = round((total_shot_makes/total_shot_attempts)*100, 2)      
 
        #finds the users all time nba comparison 
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
   
 
        #stores the all time stats under the chosen shot type as a dictionary 
        alltime_stats = {'total_shot_attempts': total_shot_attempts, 'total_shot_makes': total_shot_makes, 'alltime_field_goal': alltime_field_goal, 'alltime_nba_comparison': alltime_nba_comparison} 
 
 
    #if new_stats exists 
    if new_stats: 
        #finds the users current nba comparison 
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
 