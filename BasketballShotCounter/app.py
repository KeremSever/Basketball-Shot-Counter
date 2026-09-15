from website import create_app

app = create_app() #initialises flask app

if __name__ == '__main__': 
    app.run(debug=True)


