import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

# Create Flask app
app = Flask(__name__)

# Load the pickle model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/")
def Home():
    return render_template("index.html")

@app.route("/predict", methods = ["POST"])
def predict():

    # To store one-hot values
    temp_length_total = []
    temp_width_total = []
    temp_height_total = []

    for i in range(1, 6):
        print("Defect: " + str(i))
        # Length Direction
        temp_length_single = [0, 0, 0, 0, 0]
        loc_length = request.form.get("def"+str(i)+"_loc_len")
        print("Length:" + str(loc_length))
        if loc_length == "H":
            temp_length_single[0] = 1
        elif loc_length == "T":
            temp_length_single[1] = 1
        elif loc_length == "V":
            temp_length_single[2] = 1
        elif loc_length == "U":
            temp_length_single[3] = 1
        else:
            temp_length_single[4] = 1
        print("temp_length_single:")
        print(temp_length_single)
        temp_length_total.append(temp_length_single)
        print("temp_length_total:")
        print(temp_length_total)

        # Width Direction
        temp_width_single = [0, 0, 0, 0, 0, 0, 0]
        loc_width = request.form.get("def"+str(i)+"_loc_width")
        print("Width:" + str(loc_width))
        if loc_width == "C":
            temp_width_single[0] = 1
        elif loc_width == "F":
            temp_width_single[1] = 1
        elif loc_width == "A":
            temp_width_single[2] = 1
        elif loc_width == "W":
            temp_width_single[3] = 1
        elif loc_width == "D":
            temp_width_single[4] = 1
        elif loc_width == "X":
            temp_width_single[5] = 1
        else:
            temp_width_single[6] = 1
        print("temp_width_single:")
        print(temp_width_single)
        temp_width_total.append(temp_width_single)
        print("temp_width_total:")
        print(temp_width_total)

        # Height Direction
        temp_height_single = [0, 0, 0]
        loc_height = request.form.get("def"+str(i)+"_loc_height")
        print("Height:" + str(loc_height))
        if loc_height == "D":
            temp_height_single[0] = 1
        elif loc_height == "T":
            temp_height_single[1] = 1
        else:
            temp_height_single[2] = 1
        print("temp_height_single:")
        print(temp_height_single)
        temp_height_total.append(temp_height_single)
        print("temp_height_total:")
        print(temp_height_total)

    prediction_input = []
    for i in range(1, 6):
        prediction_input.append(float(request.form.get("def"+str(i)+"_rate")) / 2)
        prediction_input.append(float(request.form.get("def"+str(i)+"_area")) / 100)


    for i in range(0, 5):
        for j in temp_length_total[i]:
            prediction_input.append(j)

        for j in temp_width_total[i]:
            prediction_input.append(j)

        for j in temp_height_total[i]:
            prediction_input.append(j)


    features = np.array(prediction_input).reshape((1,85))
    #print(features)
    prediction = model.predict(features)
    prediction_y = prediction.argmax(axis=-1)


    return render_template("index.html", prediction_text = "Grade {}".format(prediction_y[0] + 1))

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=5002, debug=True)
