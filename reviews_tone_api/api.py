from flask import Flask, request
from reviews_tone_api.hotels_avg_tone import get_avg_tones
from reviews_tone_api.index import Hotels_Index

app = Flask(__name__)

hotels_index = Hotels_Index()
hotels_index.initialize_es()

@app.route("/avg_tone/<hotel_name>", methods=["GET", "POST"])
def avg_tone(hotel_name):
    try:
        #hotel_name= request.args.get("hotel_name")
        response = get_avg_tones(hotel_name)
        return {"average_tones" : response}
    except Exception as e:
        print(e)

@app.route("/index_hotel", defaults={'hotel_name': None}, methods=["GET", "POST"])
@app.route("/index_hotel/<hotel_name>", methods=["GET", "POST"])
def index_hotel(hotel_name):
    if hotel_name is not None:
        try:
            hotels_index.create_index(hotel_name)
            return {"message":"Index created successfuly for the given hotel."}
        except Exception as e:
            print(e)
            return {"message":"Failure"}
    else:
        try:
            hotels_index.create_index() # index all hotels
            return {"message":"Index created successfuly of all hotels."}
        except Exception as e:
            print(e)
            return {"message":"Failure"}

if __name__ == '__main__':
    app.run(debug=True)