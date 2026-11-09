from flask_restful import Resource, reqparse
from models import hotel
from models.hotel import HotelModel

# hotels = [
#     { "hotel_id": "paradise", "name": "Paradise Hotel", "stars": 4.7, "daily": 123.99, "city": "Porto" },
#     { "hotel_id": "fukui", "name": "Fukui Hotel", "stars": 4.3, "daily": 199.99, "city": "Viena" },
#     { "hotel_id": "aqua", "name": "Aqua Hotel", "stars": 4.5, "daily": 149.99, "city": "Lisbon" },
# ]

# List all hotels
class Hotels(Resource):
    def get(self):
        return {"hotels": [hotel.json() for hotel in HotelModel.query.all()]}  # SELECT * FROM hotels


# List, insert, update and delete a hotel in specific
class Hotel(Resource):
    args = reqparse.RequestParser()
    args.add_argument(
        "name", type=str, required=True, help="The field 'name' cannot be left blank!")
    args.add_argument(
        "stars",
        type=float,
        required=True,
        help="The field 'stars' cannot be left blank!",
    )
    args.add_argument(
        "daily",
        type=float,
        required=True,
        help="The field 'daily' cannot be left blank!",
    )
    args.add_argument(
        "city", type=str, required=True, help="The field 'city' cannot be left blank!"
    )

    def get(self, id_hotel):
        hotel_found = HotelModel.find_hotel(id_hotel)
        if hotel_found:
            return hotel_found.json(), 200  # OK
        return {"message": "Hotel was not found!"}, 404  # Not Found

    def post(self, id_hotel):
        data = Hotel.args.parse_args()  # Dictionary with the data sent in the request
        hotel_found = HotelModel.find_hotel(id_hotel)
        if hotel_found:
            return {"message": f"Hotel '{id_hotel}' already exists!"}, 404  # Not Found
        new_hotel = HotelModel(hotel_id=id_hotel, **data)
        new_hotel.save_hotel()
        return new_hotel.json(), 200  # Created

    def put(self, id_hotel):
        data = Hotel.args.parse_args()  # Dictionary with the data sent in the request
        hotel_found = HotelModel.find_hotel(id_hotel)
        if hotel_found:
            hotel_updated = HotelModel(id_hotel, **data)
            hotel_updated.update_hotel(**data)
            hotel_updated.save_hotel()
            return hotel_updated.json(), 200  # OK
        new_hotel = {"hotel_id": id_hotel, **data}
        hotels.append(new_hotel)
        return new_hotel.json(), 201  # Created


    def delete(self, id_hotel) -> dict[str, str]:
        """Delete the hotel with the specified ID."""
        hotel_found = HotelModel.find_hotel(id_hotel)
        if hotel_found:
            hotel_found.delete_hotel()
            return {"message": f"{str(id_hotel).capitalize()} Hotel has been deleted!"}
        return {"message": "Hotel not found!"}, 404  # Not Found
