class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
    def drive(self ,distance):
        self.distance = distance
        return distance
    def display(self):
        return f"Make: {self.make}, Model: {self.model}, Year: {self.year}, Distance: {self.distance} km "
class ElectricCar(Car):
    def __init__(self, make, model, year, battery_capacity):
        super().__init__(make, model, year)
        self.battery_capacity = battery_capacity
    def drive(self, distance):
        super().drive(distance)
    def display(self):
        dis = super().display() 
        return dis + f"Battery Capacity: {self.battery_capacity} kWh"
        
car_1 = Car("Toyota", "Corolla", "2000")
car_1.drive(50)
print(car_1.display())
car_2 = ElectricCar("Tesla", "Model S", "2022", "100")
car_2.drive(70)
print(car_2.display())