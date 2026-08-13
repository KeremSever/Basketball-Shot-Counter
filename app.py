from website import create_app 
 
app = create_app() #initialises flask app 
 
if __name__ == '__main__': #runs the flask app  
    app.run(debug=True) 
 