from datetime import date, datetime

from paysure.lib.database import Database
from paysure.lib.file import File
from paysure.lib.weather_prediction.actions import GetWeatherInformation
from paysure.lib.weather_prediction.weather_prediction import DummyWeatherModel
from paysure.lib.xml import XML


class Core:
    def __init__(self, db_name: str = 'database.db'):
        self.db = Database(db_name)

    @staticmethod
    def handle_payment(payment_message_request_xml: str):
        # TODO: check xml validity

        accept: str = File("resources/response_accept.xml").get_content()  # TODO: error handling; don't load every time
        decline: str = File("resources/response_decline.xml").get_content()

        # TODO: load from db?
        money_on_account: float = 100.0
        transaction_amount: int = 0

        # TODO: set default values

        # TODO: load all data from xml
        xml: XML = XML(payment_message_request_xml)

        try:
            request_amount: int = int(xml.get_from_xml("Amount"))

            city: str = xml.get_from_xml("Merchant_City")

            transaction_time_str: str = xml.get_from_xml("Transaction_Time")
            transaction_time_datetime: datetime = datetime.strptime(transaction_time_str.split(",")[0], "%Y-%m-%dT%H:%M:%S")  # TODO: don't cut off date
            transaction_time_date: date = transaction_time_datetime.date()

            weather: dict = DummyWeatherModel().get_weather(transaction_time_date, city)  # TODO: use actions

            clouds: bool = weather['clouds']

            temperature: int = weather['temperature']

            weather_direction: str = weather['wind_direction']

        except (ValueError, TypeError):
            return "", 400

        # TODO: checks; sort; load reasons and const from config
        if request_amount > money_on_account:
            return decline.replace("{reason}", "InsufficientFunds"), 400

        if clouds == "SUNNY" and transaction_amount < 2 or transaction_amount < 1:
            return decline.replace("{reason}", "TransactionCountOverLimit"), 400

        if request_amount > 150:
            return decline.replace("{reason}", "TransactionAmountOverLimit"), 400

        if clouds == 'RAINING':
            return decline.replace("{reason}", "ItsRaining"), 400

        if temperature < 10 and request_amount > 150/2:
            return decline.replace("{reason}", "None"), 400

        # TODO: save transaction and other db data
        if weather_direction == "S":
            pass  # TODO: charge account of bank instead of costumer

        return accept, 200
