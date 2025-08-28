class Kaiju:
    def __init__(self, name, max_health):
        self.name = name
        self.health = max_health
        self.max_health = max_health
        self.attacks = self.set_attacks()
        self.damage_multiplier = 1.0
        self.buff_active = False
        self.buff_turns_remaining = 0

    def set_attacks(self):
        #Code Damage Buff for Alpha Call, and charge mechanic for Atomic Breath and Proton Beam
        attack_options = {
            "Godzilla": {"Atomic Breath": 25, "Tail Swipe": 15, "Claw Slash": 15, "Alligator Bite": 15},
            "Mothra": {"Wing Gust": 15, "Silk Wrap": 10, "Blessed Wing": -20, "Holy Sting": 10},
            "MechaGodzilla": {"Proton Beam": 30, "Missiles": 10, "Proton Punch": 15, "Tail Drill": 15},
            "Kong": {"Axe Swing": 15, "Choke Handle": 15, "Jia's Sign": "Damage Buff", "Ape Punch": 10},
            "SpaceGodzilla": {"Crystal Spikes": 20, "Tail Swing": 15, "Flying Headbutt": 15, "Corona Beam": 25},
            "King Ghidorah": {"Gravity Beam": 20, "Triangle Bite": 15, "Alpha Call": "Damage Buff", "Spiked Tails": 15},
            "Rodan": {"Air Slam": 15, "Sonic Boom": 15, "Uranium Heat Beam": 20, "Flame On!": "Damage Buff"}
        }
        return attack_options.get(self.name, {"Basic Attack": 10})  # Default attack if Kaiju not in list

    def is_alive(self):
        return self.health > 0

    def show_attacks(self):
        """ Display available attacks """
        print(f"\n{self.name}'s available attacks:")
        buff_attacks = ["Jia's Sign", "Alpha Call", "Flame On!"]
        for attack, dmg in self.attacks.items():
            if attack in buff_attacks:
                effect = "Damage Buff"
            else:
                effect = f"{'heals' if dmg < 0 else 'deals'} {abs(dmg)}"
            print(f"- {attack} ({effect})")

    def take_damage(self, damage):
        """ Reduce health when attacked """
        self.health -= damage
        if self.health < 0:
            self.health = 0
        print(f"{self.name} takes {damage} damage! Health left: {self.health}")

    def heal(self, heal_amount):
        """ Restore health if an attack has healing effects """
        self.health += heal_amount
        if self.health > self.max_health:
            self.health = self.max_health
        print(f"{self.name} heals for {heal_amount} HP! Current health: {self.health}")

    def do_attack(self, attack_name, target):
        """ Perform an attack on the opponent """
        if attack_name not in self.attacks:
            print(f"{self.name} tries to attack, but doesn't know '{attack_name}'!")
            return

        # Retrieve the attack damage
        base_damage = self.attacks[attack_name]
        
        if attack_name in ["Jia's Sign", "Alpha Call", "Flame On!"]:
            print(f"{self.name} used '{attack_name}'. Their attack increased!")
            self.damage_multiplier = 1.5  # Increase damage output
            self.buff_turns_remaining = 3  # Buff lasts for 3 turns
            return


        # Ensure we only multiply numerical values
        if isinstance(base_damage, (int, float)):  
            damage = base_damage * self.damage_multiplier
        else:
            print(f"{self.name}'s attack increased!")
            return
        if damage > 0:
            print(f"{self.name} uses '{attack_name}', dealing {int(damage)} damage!")
            target.take_damage(int(damage))
        elif damage < 0:
            print(f"{self.name} uses '{attack_name}', and heals {int(-damage)} health! Health Left: {self.health}")
            self.heal(-damage)

        if self.buff_turns_remaining > 0:
            self.buff_turns_remaining -= 1
            if self.buff_turns_remaining == 0:
                self.damage_multiplier = 1.0
                print(f"{self.name}'s damage buff has worn off.")







# Initialize Kaiju Roster
kaiju_roster = {
    "Godzilla": Kaiju("Godzilla", 100),
    "Mothra": Kaiju("Mothra", 80),
    "MechaGodzilla": Kaiju("MechaGodzilla", 100),
    "Kong": Kaiju("Kong", 90),
    "SpaceGodzilla": Kaiju("SpaceGodzilla", 100),
    "King Ghidorah": Kaiju("King Ghidorah", 100),
    "Rodan": Kaiju("Rodan", 90)
}

# Player Selection
print("Choose your Kaiju!\n")
for kaiju_name in kaiju_roster.keys():
    print(f"- {kaiju_name}")

player1_choice = input("Player 1: ").strip()
while player1_choice not in kaiju_roster:
    print("Invalid choice, please select a character.")
    player1_choice = input("Player 1: ").strip()

player2_choice = input("Player 2: ").strip()
while player2_choice not in kaiju_roster:
    print("Invalid choice, please select a character.")
    player2_choice = input("Player 2: ").strip()

player1_kaiju = Kaiju(player1_choice, kaiju_roster[player1_choice].max_health)
player2_kaiju = Kaiju(player2_choice, kaiju_roster[player2_choice].max_health)

print(f"\n{player1_kaiju.name} vs {player2_kaiju.name}")
print("FIGHT!")

# Battle Loop
current_kaiju = player1_kaiju
opponent_kaiju = player2_kaiju

while player1_kaiju.is_alive() and player2_kaiju.is_alive():
    print(f"\nIt's {current_kaiju.name}'s turn!")
    current_kaiju.show_attacks()

    chosen_attack = input("What will you do? ").strip()
    while chosen_attack not in current_kaiju.attacks:
        print("Invalid attack! Choose one from the list above!")
        chosen_attack = input("What will you do? ").strip()

    # Perform attack ONLY ONCE
    current_kaiju.do_attack(chosen_attack, opponent_kaiju)


    # Check if opponent fainted before swapping turns
    if not opponent_kaiju.is_alive():
        break  # Stop battle if one faints

    # Swap turns
    current_kaiju, opponent_kaiju = opponent_kaiju, current_kaiju
# Announce Winner
winner = player1_kaiju if player1_kaiju.is_alive() else player2_kaiju
print(f"\n{winner.name} wins!")
