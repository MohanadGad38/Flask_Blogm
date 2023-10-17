from flaskblog import create_app

app=create_app()
# debug mode
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')




