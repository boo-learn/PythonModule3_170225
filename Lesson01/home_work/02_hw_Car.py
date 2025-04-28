class Car:
    def __init__(self, capacity, gas_per_km, gas=0):
        self.gas = gas  # сколько бензина в баке
        self.capacity = capacity  # вместимость бака
        self.gas_per_km = gas_per_km  # расход топлива на **один** километр
        self.mileage = 0

    def fill(self, liters):
        if self.gas + liters > self.capacity:
            print(f"Бак переполнен на {(self.gas + liters) - self.capacity} литров")
            self.gas = self.capacity
        else:
            self.gas += liters

    def ride(self, distance):
        possible_dist = self.gas / self.gas_per_km  # расстояние на которое хватит топлива
        if possible_dist >= distance:
            self.mileage += distance
            self.gas -= distance * self.gas_per_km
        else: # не хватает топлива
            self.mileage += possible_dist
            self.gas = 0


car = Car(100, 1)

# тесты на fill()
car.fill(40)
assert car.gas == 40
car.fill(90)  # 130
assert car.gas == 100
car.fill(20)
assert car.gas == 100


car = Car(capacity=100, gas_per_km=1, gas=40)
# тесты на ride()
car.ride(30)
assert car.mileage == 30
assert car.gas == 10
car.ride(20)
assert car.mileage == 40
assert car.gas == 0