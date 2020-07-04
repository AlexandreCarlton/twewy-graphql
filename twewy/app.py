from flask import Flask
from flask_graphql import GraphQLView

from twewy.database import init_db, db_session
from twewy.schema import schema

app = Flask(__name__)
app.debug = True
app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql",
                                  schema=schema,
                                  graphiql=True))

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
