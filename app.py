from flask import Flask, request, jsonify, url_for, Response , render_template
from pymongo import MongoClient
import gridfs
import shortuuid

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://img-api:loniko0908@img-api.7dicg.mongodb.net/?retryWrites=true&w=majority&appName=IMG-API")
db = client['image_hosting']
fs = gridfs.GridFS(db)  # Create a GridFS object for storing files
images_collection = db['images']

# Home route
@app.route('/')
def home():
    images = images_collection.find({})
    return render_template('index.html', images=images)

# Upload image API
@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.files['image']
    short_url = shortuuid.uuid()
    
    # Save the image file in MongoDB using GridFS
    image_id = fs.put(image.read(), filename=image.filename, content_type=image.content_type)

    # Store image metadata, including GridFS ID and short URL
    image_data = {
        'filename': image.filename,
        'short_url': short_url,
        'image_id': image_id,
        'content_type': image.content_type
    }
    images_collection.insert_one(image_data)

    # Generate a proper URL for accessing the image
    image_url = url_for('get_image', short_url=short_url, _external=True)
    return jsonify({'image_url': image_url}), 201

# Serve image by short URL
@app.route('/img/<short_url>')
def get_image(short_url):
    image = images_collection.find_one({'short_url': short_url})
    if image:
        # Retrieve the image file from MongoDB GridFS
        image_file = fs.get(image['image_id'])
        return Response(image_file.read(), mimetype=image['content_type'])
    return jsonify({'error': 'Image not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
