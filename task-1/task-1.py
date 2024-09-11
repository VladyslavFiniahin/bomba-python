class Animal:
    def __init__(self, type, name, age):
        self.type = type
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.type} - {self.name}, {self.age} років"

class Ssavec(Animal):
    def __init__(self, name, age, predatory):
        super().__init__("Ссавець", name, age)
        self.predatory = predatory

    def __str__(self):
        return f"{super().__str__()}, хижак: {self.predatory}"

class Bird(Animal):
    def __init__(self, name, age, wing):
        super().__init__("Птах", name, age)
        self.wing = wing

    def __str__(self):
        return f"{super().__str__()}, крило: {self.wing} м"

class Reptile(Animal):
    def __init__(self, name, age, typereptile):
        super().__init__("Рептилія", name, age)
        self.typereptile = typereptile

    def __str__(self):
        return f"{super().__str__()}, тип луски: {self.typereptile}"

class Zoo:
    def __init__(self):
        self.animals = []

    def add_animal(self, animal):
        self.animals.append(animal)

    def sort_by_type(self):
        sorted = {}
        for animal in self.animals:
            if animal.type not in sorted:
                sorted[animal.type] = []
            sorted[animal.type].append(animal)
        return sorted

    def give_report(self):
        report = "Звіт про склад зоопарку:\n"
        for type, animals in self.sort_by_type().items():
            report += f"\nВид: {type}\n"
            for animal in animals:
                report += f"  - {animal}\n"
        return report

zoo = Zoo()
zoo.add_animal(Ssavec("Лев", 5, "так"))
zoo.add_animal(Bird("Орел", 3, 4.2))
zoo.add_animal(Reptile("Крокодил", 12, "кератинова луска"))
zoo.add_animal(Ssavec("Слон", 10, "ні"))

print(zoo.give_report())