import pykka

class ParseActor(pykka.ThreadingActor):
    def on_receive(self, message):
        data = message.get('data')
        if data and 'flights' in data:
            parsed_data = self.parse_data(data)
            return parsed_data
        else:
            return {'error': 'Invalid data format'}

    def parse_data(self, data):
        parsed_data = []
        for flight in data:
            parsed_data.append({
                'airline': flight.get('airline', 'Unknown'),
                'price': flight.get('price', 'N/A'),
                'departure_time': flight.get('departure_time', 'N/A'),
                'arrival_time': flight.get('arrival_time', 'N/A'),
                'stops': flight.get('stops', 'N/A')
            })
        return parsed_data
