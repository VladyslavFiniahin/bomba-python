import random
import json

class GameObject:                #батьківський клас
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.alive = True

    def update(self):
        pass

    def __str__(self):
        return f"{self.name} at ({self.x}, {self.y})"


class Steve(GameObject):                #нащадок класу gameobject
    def __init__(self, name, x, y, hp):
        super().__init__(name, x, y)
        self.hp = hp
        self.has_sword = False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update(self):
        print(f"{self.name} moves. Position: ({self.x}, {self.y})")


class Enemy(GameObject):            #нащадок класу gameobject
    def update(self):
        print(f"Enemy {self.name} remains at ({self.x}, {self.y})")  # як і заспавнився так і лишається на місці


class Item(GameObject):             #нащадок класу gameobject
    def update(self):
        print(f"Item {self.name} is on the ground. Position: ({self.x}, {self.y})")

#словник який зберігає функції:
event_listeners = {}

def event_listener(event_name):
    def decorator(func):
        if event_name not in event_listeners:
            event_listeners[event_name] = []
        event_listeners[event_name].append(func)
        return func
    return decorator

def trigger_event(event_name, *args, **kwargs):
    if event_name in event_listeners:
        for func in event_listeners[event_name]:
            func(*args, **kwargs)

@event_listener('on_collision')
def handle_collision(obj1, obj2):
    if isinstance(obj1, Steve) and isinstance(obj2, Enemy):
        if not obj1.has_sword:
            print(f"{obj1.name} collided with {obj2.name} and doesn't have a sword! Game Over!")
            obj1.hp = 0
        else:
            print(f"{obj1.name} defeated {obj2.name} with the sword!")
            obj2.alive = False
    elif isinstance(obj1, Steve) and isinstance(obj2, Item) and obj2.name == 'Sword':
        obj1.has_sword = True
        print(f"{obj1.name} picked up the sword!")


def game_loop(objects):
    while True:
        print("\nGame tick:")
        for obj in objects:
            if obj.alive:
                obj.update()

        for i in range(len(objects)):
            for j in range(i + 1, len(objects)):
                if objects[i].x == objects[j].x and objects[i].y == objects[j].y:
                    trigger_event('on_collision', objects[i], objects[j])

        yield objects


def user_input(steve):
    move = input("Enter move (w/a/s/d): ").lower()
    if move == 'w':
        steve.move(0, -1)
    elif move == 's':
        steve.move(0, 1)
    elif move == 'a':
        steve.move(-1, 0)
    elif move == 'd':
        steve.move(1, 0)


def save_game(objects, filename='game_state.json'):
    try:
        with open(filename, 'r') as f:
            data = f.read()
        game_count = data.count("Game")
    except FileNotFoundError:
        game_count = 0

    game_number = game_count + 1

    with open(filename, 'a') as f:
        f.write(f"Game {game_number}:\n")
        for obj_data in [{'name': obj.name, 'x': obj.x, 'y': obj.y, 'hp': getattr(obj, 'hp', None), 'has_sword': getattr(obj, 'has_sword', None), 'alive': obj.alive} for obj in objects]:
            for key, value in obj_data.items():
                f.write(f"{key}: {value}\n")
            f.write("\n")
    print(f"Game {game_number} saved!")


if __name__ == "__main__":
    steve = Steve('Steve', 0, 0, 100)
    
    #спавним ворга і меч у рандомному місці до 5 по x і y
    enemy_x, enemy_y = random.randint(-5, 5), random.randint(-5, 5)
    sword_x, sword_y = random.randint(-5, 5), random.randint(-5, 5)
    enemy = Enemy('Enemy', enemy_x, enemy_y)
    sword = Item('Sword', sword_x, sword_y)

    objects = [steve, enemy, sword]
    loop = game_loop(objects)

    while True:  #ходів безліч
        next(loop)
        user_input(steve)

        if steve.hp <= 0:
            print(f"Game Over! {steve.name} died.")
            break
        elif not enemy.alive:
            print(f"Victoory! {steve.name} has defeated {enemy.name}.")
            break

    save_game(objects)
