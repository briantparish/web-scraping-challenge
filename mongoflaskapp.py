import pymongo
import scrape_mars
from flask import Flask, render_template

app = Flask(__name__)

conn = 'mongodb://localhost:27017/mars_info'
client = pymongo.MongoClient(conn)

# Define the 'mars_info' database in Mongo
db = client.mars_info
# Define collection 'mars'
col = db.mars

mars_info = scrape_mars.scrape()
col.insert_one(mars_info)

# Set route
@app.route('/scrape')
def scrape():
   
    mars_data = col.find_one()

    # Return the template with the teams list passed in
    return render_template('scrape.html', mars=mars_data)


if __name__ == "__main__":
    app.run(debug=True)
