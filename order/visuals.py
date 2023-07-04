class Order:
    def __init__(self, receiver_name, receiver_surname, receiver_number, origin, destination, date_until,
                 delivery_type) -> None:
        self.receiver_name = receiver_name
        self.receiver_surname = receiver_surname
        self.receiver_number = receiver_number
        self.origin = origin
        self.destination = destination
        self.date_until = date_until
        self.delivery_type = delivery_type


class FirstOrder(Order):
    def __init__(self, receiver_name, receiver_surname, receiver_number, origin, destination, date_until, delivery_type,
                 car_type) -> None:
        super().__init__(receiver_name, receiver_surname, receiver_number, origin, destination, date_until,
                         delivery_type)
        self.car_type = car_type


class SecondOrder(Order):
    def __init__(self, receiver_name, receiver_surname, receiver_number, origin, destination, date_until, delivery_type
                 , cargo_type, weight, volume) -> None:
        super().__init__(receiver_name, receiver_surname, receiver_number, origin, destination, date_until,
                         delivery_type)
        self.cargo_type = cargo_type
        self.weight = weight
        self.volume = volume
