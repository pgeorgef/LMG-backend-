from builtins import list, range

from flask import Flask, jsonify, make_response
from flask_cors import CORS

import imageio
app = Flask(__name__)
CORS(app)

@app.route("/gifmaker/<string:letters>", methods=['GET'])
def gifmaker(letters):
    images = []

    letters = list(letters.lower())
    for letter in letters:
        for i in range(0,9):
            images.append(imageio.imread('C:\Users\Andreea\Desktop\gifmaker\gifmakerdata\\' + letter + '.jpg'))

    imageio.mimsave('johnny.gif', images)

    return make_response(jsonify('worked'), 200)


if __name__ == '__main__':
    app.run()
