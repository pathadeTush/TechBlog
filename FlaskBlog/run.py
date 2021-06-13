from flaskblog import create_app
# create_app() is a function defined in __init__.py file. which create app object and return it. 
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
