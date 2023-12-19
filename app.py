import pyxel

game_started = False
max_snake_length = 0

def on_quit():
    global max_snake_length
    print(f"La taille maximale du serpent atteinte était : {max_snake_length}")

arrow_keys = [
    pyxel.KEY_UP, 
    pyxel.KEY_DOWN, 
    pyxel.KEY_LEFT, 
    pyxel.KEY_RIGHT
]

snake_geometry = []
snake_direction = []
fruit = []

# Demander à l'utilisateur la vitesse désirée
user_speed_input = input(f"Entrez la vitesse du serpent (par défaut est 10): ")

# Convertir la valeur en entier
try:
    user_speed = int(user_speed_input)
except ValueError:
    print("Veuillez entrer un nombre valide. La vitesse par défaut de 10 sera utilisée.")
    user_speed = 10

# Initialisation des rochers
rocks = []
for i in range(30):
    for j in range(30):
        if (i+j) % 5 == 0 and (i-j) % 11 == 0:
            rocks.append([i, j])

# Ajouter ces lignes pour afficher le nombre initial de rochers
initial_num_rocks = len(rocks)
print(f"Il y a initialement {initial_num_rocks} rochers.")

# Demander à l'utilisateur s'il veut ajouter ou enlever des rochers, et combien
user_choice = input("Voulez-vous ajouter (nombre positif) ou enlever (nombre négatif) des rochers? Combien? ")

def spawn_new_fruit():
    global fruit
    while True:
        fruit = [pyxel.rndi(0, 29), pyxel.rndi(0, 29)]
        if fruit not in snake_geometry and fruit not in rocks:
            break

def is_occupied(position):
    return position in snake_geometry or position == fruit # Définit les cases occupées par un rochet ou un fruit, dans le but de ne pas rajouter ceux_ci dans ces positions

# Fonction pour enlever des rochers en fonction de la réponse de l'utilisateur
def remove_random_rockers(num_rocks):
    if len(rocks) >= -num_rocks:
        indices_to_remove = [pyxel.rndi(0, len(rocks) - 1) for _ in range(abs(num_rocks))]
        indices_to_remove.sort(reverse=True)  # Supprimer en ordre décroissant pour éviter de changer l'ordre de la liste
        for index in indices_to_remove:
            rocks.pop(index)

# Fonction pour ajouter des rochers en fonction de la réponse de l'utilisateur
def add_rocks(num_rocks):
    for _ in range(num_rocks):
        new_rocker = [pyxel.rndi(0, 29), pyxel.rndi(0, 29)]

        # Vérifier si la nouvelle position est occupée, si oui, réessayer jusqu'à trouver une position libre
        while is_occupied(new_rocker) or new_rocker in snake_geometry:
            new_rocker = [pyxel.rndi(0, 29), pyxel.rndi(0, 29)]

        rocks.append(new_rocker)

def update(): # Dynamique du jeu
    global snake_geometry, snake_direction, game_started, max_snake_length
    if not game_started:
        # Vérifier si l'utilisateur a cliqué pour commencer le jeu
        if pyxel.btnp(pyxel.KEY_SPACE):
            game_started = True
            snake_geometry = [
                [10, 16], 
                [11, 16]] # initialise la position du serpent
            spawn_new_fruit() # initialise la position du fruit
            try:
                num_rocks = int(user_choice)
                if num_rocks > 0:
                    add_rocks(num_rocks)
                elif num_rocks < 0:
                    remove_random_rockers(num_rocks)
            except ValueError:
                print("Veuillez entrer un nombre valide.")
            snake_direction = [1, 0] # initialise la direction du serpent vers la droite
    else : 
        if pyxel.btnp(pyxel.KEY_Q):
            print(on_quit())
            pyxel.quit() # imprime le score si on quitte le jeu avec Q
        arrow_keys_pressed = []
        for key in arrow_keys:
            if pyxel.btnp(key):
                arrow_keys_pressed.append(key)
        for key in arrow_keys_pressed: # pour le mouvement du snake : haut/bas/droite/gauche
            if key == pyxel.KEY_UP:
                snake_direction = [0, -1] # Déplacement vers le haut
            elif key == pyxel.KEY_DOWN:
                snake_direction = [0, 1] # Déplacement vers le bas
            elif key == pyxel.KEY_LEFT:
                snake_direction = [-1, 0] # Déplacement vers la gauche
            elif key == pyxel.KEY_RIGHT:
                snake_direction = [1, 0] # Déplacement vers la droite
        snake_head = snake_geometry[-1] # Obtient la position de la tête du serpent
        new_snake_head = [
            snake_head[0] + snake_direction[0],
            snake_head[1] + snake_direction[1],
        ] # Calcule la nouvelle position de la tête du serpent en fonction de sa direction
        if (
            new_snake_head in rocks
            or (
            new_snake_head[0] < 0
            or new_snake_head[0] > 29
            or new_snake_head[1] < 0
            or new_snake_head[1] > 29
            )
        ):
            print(f"La taille maximale du serpent atteinte était : {max_snake_length}")
            pyxel.quit() # quitte le jeu si le serpent atteint un bord ou une pierre, en imprimant le score
        elif (new_snake_head in snake_geometry
        ) :
            snake_geometry = snake_geometry[1:-1] + [snake_head] # réduit la taille du serpent si demi-tour ou collision avec lui même, interdit
        elif new_snake_head == fruit:
            snake_geometry = snake_geometry + [new_snake_head]
            spawn_new_fruit() # ajoute un élément au snake s'il rencontre un fruit
        else:
            snake_geometry = snake_geometry[1:] + [new_snake_head]
            if len(snake_geometry) > max_snake_length:
                max_snake_length = len(snake_geometry)  # Met à jour la taille maximale

def draw(): # Pour les graphismes
    global game_started
    if not game_started: # Graphismes page d'accueil
        pyxel.cls(0)
        color = pyxel.frame_count % 16
        pyxel.text(2, 2, "Snake!", color) 
        pyxel.text(2, 10, "Press", pyxel.frame_count % 16)
        pyxel.text(2, 18, "space", pyxel.frame_count % 16)
    else : # Graphismes du jeu
        pyxel.cls(7)
        pyxel.pset(fruit[0], fruit[1], 8) # Dessine le fruit
        for x, y in rocks:
            pyxel.pset(x, y, 0) # Dessine les rocks en noirs
        for x, y in snake_geometry[:-1]:
            pyxel.pset(x, y, 3) # Dessine le corps du serpent en vert foncé
        snake_head = snake_geometry[-1]
        pyxel.pset(snake_head[0], snake_head[1], 11) # Dessine la tête du serpent en vers clair

pyxel.init(30,30, fps = user_speed)
pyxel.run (update,draw)