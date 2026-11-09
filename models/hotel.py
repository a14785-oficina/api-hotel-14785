from con_sql import bd


class HotelModel(bd.Model):
    __tablename__ = 'hotels'
    hotel_id = bd.Column(bd.String(80), primary_key=True)
    name = bd.Column(bd.String(80), nullable=False)  # Database constraint: prevents NULL values; reqparse's required=True instead rejects requests that omit the name argument.
    stars = bd.Column(bd.Float(precision=1))
    daily = bd.Column(bd.Float(precision=2))
    city = bd.Column(bd.String(40))
    
    # Class Constructor (Mapped Class Essential Components - https://docs.sqlalchemy.org/en/21/orm/mapping_styles.html#orm-mapper-configuration-overview)
    def __init__(self, hotel_id, name, stars, daily, city):
        self.hotel_id = hotel_id
        self.name = name
        self.stars = stars
        self.daily = daily
        self.city = city
        
    # Method to return the hotel data in JSON format
    def json(self):
        return {
            "hotel_id": self.hotel_id,
            "name": self.name,
            "stars": self.stars,
            "daily": self.daily,
            "city": self.city
        }
        
    @classmethod
    def find_hotel(cls, id_hotel):
        hotel = cls.query.filter_by(hotel_id=id_hotel).first()  # SELECT * FROM hotels WHERE hotel_id=hotel_id LIMIT 1
        if hotel:
            return hotel
        return None
    
    def save_hotel(self):
        bd.session.add(self)  # Add the hotel to the session
        bd.session.commit()  # Commit the session to save the hotel in the database
        
    def delete_hotel(self):
        bd.session.delete(self)  # Delete the hotel from the session
        bd.session.commit()  # Commit the session to delete the hotel from the database
        
    def update_hotel(self, name_updated, stars_updated, daily_updated, city_updated):
        self.name = name_updated
        self.stars = stars_updated
        self.daily = daily_updated
        self.city = city_updated
        bd.session.commit()  # Commit the session to update the hotel in the database