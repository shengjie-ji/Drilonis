init -98 python:
  # Using Composition
  class VisitorCharacter:
      def __init__(self, id, name, inventory, dialogue_lines, **kwargs):
          self.id = id
          self.name = name
          self.character = Character(name, **kwargs)
          self.inventory = inventory 
          self.dialogue_lines = dialogue_lines

### Characters

### 001: Fur Merchant
define fur_merchant = VisitorCharacter(
    id = 1,
    name = 'Rreresh',
    inventory = {'Hunting Sword': 2, 'Trade Contract': 1},
    dialogue_lines = {
    "Inspection": [
    "These are some nice pelts, take a good look at those in the front: its direwolf pelts.",
    "Oh, what is the sword for? Well its a hunting sword so for removing the pelt if need be.",
    "You would be surprised the discounts I get when I simply have to remove the pelt myself.",
    "This contract is with the merchant of Brigje, I'm hoping to get a chance to try some eel."
    ],
    "Combat": [
    "No sir, please, why are you doing this?",
    "Please spare me I have a family to provide for!",
    "Look I am surrendering please have mercy on this poor merchant, good Lord." 
    ]
    },
)

### 002: Yojimbo, the Wandering Samurai
define yojimbo = VisitorCharacter(
    id    = 2,
    name  = "Yojimbo",
    inventory = {'Old Eastern Sword': 1},
    dialogue_lines = {}
)