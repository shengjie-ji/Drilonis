# Introduction 

### Globals
default daily_action_points = 2
default daily_expended_points = 0
default current_visitor = None
default visitor_decision = None
default visitor_dialogue = ""
default inspected_items = []
default duelist_one = None
default duelist_two = None

define n = Character("Narrator")
define gc = Character("Guard Captain", color="#ADD8E6", what_color="#ADD8E6") # Light Blue
define e  = Character("Edgar", color="#FFA07A", what_color="#FFA07A")          # Light Salmon                                                   # Narrator, no name displayed
define g  = Character("Guard", color="#90EE90", what_color="#90EE90")          # Light Green
define g2 = Character("Guard 2")  

default fur_merchant = None
default yojimbo = None

init python:
    ### Character ------------------------------------------------------------------------
    class PlayerCharacter:
        def __init__(self, name, inventory, **kwargs):
            self.name = name,
            self.inventory = inventory

    class VisitorCharacter:
        def __init__(self, id, name, inventory, **kwargs):
            self.id           = id
            self.name         = name
            self.character    = Character(name, **kwargs)
            self.inventory    = inventory
            self.status       = 'Alive' # Alive, Dead
            self.relationship = 'Neutral' # Friendly, Neutral, Enemy

        def auto_chat(self, event_type, character_lines, interjection=None):
            import math

            if event_type == 'Inspection':
                
                for character_line in character_lines:
                    
                    if visitor_decision is not None:
                        break

                    line_pause = 0.5 + (math.ceil(len(character_line) / 3) * 0.1)
                    character_line = character_line + "{w=%s}{nw}" % line_pause
                    self.character(character_line)
                    renpy.pause(2.0)

                    if interjection:
                            interjection(idx)
            

            if event_type == 'Combat':
                
                for character_line in character_lines:
                    
                    if visitor_decision is not None:
                        break

                    line_pause = 0.25 + (math.ceil(len(character_line) / 4) * 0.1)
                    character_line = character_line + "{w=%s}{nw}" % line_pause
                    self.character(character_line)
                    renpy.pause(2.0)
            
                if interjection:
                        interjection(idx)


            return

### Item Inspection ------------------------------------------------------------------

    def perform_inspection(items):

        inspected_items.clear()
        res = []

        if not items:
            res = ["Nothing was Found..."]
            return res

        for item, amount in items.items():
           current_item = f"{item} ({amount})"
           res.append(current_item)

        return res

### Screen for Inspection Mode

screen visitor_screening:
    tag documents

    frame:
        xalign 0.5
        yalign 0.25
        vbox:
            spacing 15
            text "Name: [current_visitor.name]"

            vbox:
                for line in inspected_items_display:
                    text line
            text "A guard looks your way: What's your call?"

            hbox:
                spacing 30
                textbutton "Approve" action [SetVariable("visitor_decision", "Approve"), Return()]
                textbutton "Deny" action [SetVariable("visitor_decision", "Deny"), Return()]
                textbutton "Apprehend" action [SetVariable("visitor_decision", "Apprehend"), Return()]  

    # Bottom-style dialogue display
    frame:
        style "say_window"
        xalign 0.5
        yalign 0.70
        xfill True
        yminimum 150

        text "[visitor_dialogue]" style "say_dialogue" xalign 0.5 yalign 1.0

screen duel:

    # add 'bg combat'

    fixed:
        xysize (config.screen_width, config.screen_height)

        add duelist_one:
            xpos 0.25
            ypos 0.5
            xanchor 0.5
            yanchor 0.5

        add duelist_two:
            xpos 0.75
            ypos 0.5
            xanchor 0.5
            yanchor 0.5

### GAME START --------------------------------------------------------------------------- 
label start:

    $ pc = PlayerCharacter(
        name="Edgar",
        inventory = {'Sword': 1, 'Light Armor Set (Iron)': 1, 'Healing Potion': 10},
        )

    n "Welcome, to the kingdom of 'Albenora'."
    n "The year is 1400, in the remote hold of 'Drilonis', a bridge exists over a mighty river."
    n "Two generations ago, a warrior from a roaming 'Vlach' mercenary band from the family of 'Kastrioti' distinguished himself."
    n "'The King' personally awarded him a small hold, which became known as Driolonis."
    n "That warrior was your Grandfather, and at the ripe age of 67, he passed away, leaving the hold to your father, Ardian."
    n "The hold oversaw a bridge that connected two sides of a trade route that saw few visitors."
    n "Together with a small retinue of servants and guards, you supervise the bridge and the surrounding route for brigands and the odd con man."
    n "There were other exceptions to the lull, such as the 'Eel Festival' in the coastal town of Vranisht."
    n "But the bridge is actually just one of the trade routes that traverse all around the kingdom of Albenora. And an out of the way one at that."
    n "To get to the the neighorbing capital of Floki, the Kings Road would save any reasonable traveler 6 days each way."
    n "But a modest income and stories of your heroic grandfather's hard fought achievements earned this keep, and so it shall."
    n "As the lord of the hold, entrusted to his heirs by your grandfather,"
    n "your father oversees the land on behalf of the King, Bardhyl II."
    n "Until recently, your family was able to maintain this position, dealing with the odd rude customer or some bandits."
    n "but recently, things have changed."
    n "In recent months, the air in Albenora has grown heavier."
    n "Traders now travel in caravans, guarded and grim, their wagons bearing fewer goods and more weapons."
    n "Rumors echo through the marketplace—of towns burned, children conscripted, and nobles vanishing overnight."
    n "You begin to see fewer familiar faces and more strangers cloaked in foreign colors."
    n "Some peasants have fled to the keep, seeking shelter, claiming their villages were raided by armored men who bore no banners."   
    n "King Durhan of the neighboring kingdom of Indica has for the past year been engaged in a brewing conflict, one that is surprisingly brutal"
    n "Neither King has intended this level of escalation, but when Durhan enlisted the Grey Company as mercenaries, paid with the spoils of villages and and even some merchants along the Rruga e Mbretit, or the King's Road."
    n "This lead to a equal response by Bardhyl. But what was once a defensive campaign became a proxy war when Bardhyl hired the Legions to push the invading forces back."      
    n "A year into the conflict, Drilonis has been largely unaffected, but is only a matter of time. Until what, we shall see..."
    n "But enough of that, a trader approaches; with a large burlap hoisted on his back and no companions, the Lord father is probably not needed to handle this."
    n "Why don\'t we give it a try?"
    jump tutorial


label tutorial:
    
    $ inspection_completed = False 
    $ visitor_decision = None
    $ inspected_items = []
    $ inspected_items_display = []

    $ fur_merchant = VisitorCharacter(
        id=1,
        name="Reresh",
        inventory = {'Direwolf Pelt': 10, 'Hunting Sword': 2, 'Trade Contract': 1},
        )

    $ current_visitor = fur_merchant
    $ inspected_items = perform_inspection(current_visitor.inventory)

    show screen visitor_screening

    python:
        for item in inspected_items:
            
            if visitor_decision is not None:
                break

            inspected_items_display.append(item)
            renpy.pause(2.0)

    $ fur_merchant_inspection_lines = [
            "These are some nice pelts, take a good look at those in the front: its direwolf pelts.",
            "Oh, what is the sword for? Well its a hunting sword so for removing the pelt if need be.",
            "You would be surprised the discounts I get when I simply have to remove the pelt myself.",
            "This contract is with the merchant of Brigje, I'm hoping to get a chance to try some eel.",
            "Have you good sirs been to the festival? I have heard on in since I began as a merchant but this is my first chance.",
            "The King's Road was always the best way to conduct my routes, but with the recent changes...",
            "A peer of mine lost 50 lbs of iron by some brigands, and to think we call that lucky in todays age!",
            "I suppose it is not so bad, I finally get a chance to try some eel, I hoped to bring back some for the missus.",
            "Are you lads almost finished? I admit I have little to show and less to offer you gentleman."
    ]

    $ fur_merchant_combat_lines = [
            "No sir, please, why are you doing this?",
            "Please spare me I have a family to provide for!",
            "Look I am surrendering please have mercy on this poor merchant, good Lord."
    ]

    $ fur_merchant.auto_chat('Inspection', fur_merchant_inspection_lines)

    $ inspection_completed = True

    if visitor_decision == 'Approve':

        hide screen visitor_screening
        jump approval

    if visitor_decision == 'Deny':

        hide screen visitor_screening
        jump deny

    if visitor_decision == 'Apprehend':

        hide screen visitor_screening
        jump combat

    pause

label approval:

    n "Everything seems to be in order."
    jump act_one

label deny:

    n "Everything seems to be not in order."
    jump act_one

label combat:

    n "TODO: Make Combat System that is cool and fun." 
    jump act_one

label act_one:

    n "Now that we got through the basics, do you feel confident in the mechanics so far?"

label random_encounter:

    n "TODO: Create System to select a random encounter"


label yojimbo_introduction_event:
    "A strange report reaches your ears..."

    gc "Sir, we have an odd case for you, there's a....well he's a swordsman but he moves like no one's ever seen."
    e "Oh? I never heard that report before, are there casualties?"

    n "You start walking faster towards the bridge, the guard starts moving faster to follow your pace."

    gc "Well, maybe one."
    e "What, we should stop him right away, is he captured or dead?"
    gc "Well... he is captured, but he didn't hurt anyone."

    menu:
        "So what was he swinging his fucking sword at? The air?":
            e "So what was he swinging his fucking sword at? The air?"
            gc "Yes, sir."
            n "You do such an abrupt stop and start that the guard almost trips on his own feet."
            e "You take me for a fool? Or am I speaking to one?"
            gc "No sir, please let us get to the entrance and I can explain."
            e "Of that we can both be assured."

        "No casualties? That's... unusual for a swordsman.":
            e "No casualties? That's... unusual for a swordsman."
            gc "Indeed, sir. It's quite perplexing. He seemed to be fighting shadows, or perhaps just practicing in a very... spirited manner."
            e "Practicing? On the other side of the bridge? What was he thinking?"
            gc "We're not entirely sure, sir. He was certainly drawing a crowd, and causing some minor panic with his erratic movements."
            e "Panic without injury. Interesting. Lead the way."

    n "At the gate you see what looks to be a foreign man laying on the ground. His hair has a black sleekness you rarely see on a man."
    n "Wrapped up in a ponytail, his robes looked odd, but were very similar to a traveler's cloak."

    $ yojimbo = VisitorCharacter(
        id=2,
        name="Yojimbo",
        inventory = {'Old Eastern Sword': 1, 'Strange Food Item': 5, 'Short Sword': 1}
        )
  
    yojimbo "Hail Sir, is that the proper greeting? I come from a far away land and request a duel with a warrior!"
    n "The man's loud voice was in stark contrast to his modest clothing."

    menu:
        "You may find a match in me!":
            n "This mans challenge seems intriguing; it is probably best not to engage, but your curiosity wins over your caution"
            pc "You may find me an equal match! But first where do you hail from, soldier?"
        "Apprehend the weirdo":
            pc "That is not going to happen, a man swinging a sword around in my domain is in no position to make demands, seize him and confiscate his sword."

    # Second set of dialogue options for Edgar at the gate
    menu:
        "Did you manage to restrain him?":
            e "Did you manage to restrain him?"
            g "We were just about to, sir. Some of the younger guards were scared of the moves he showed us,"
            g "but we took away his strange sword while he was unconscious, and we were just about to throw him in a dungeon"
            g "and notify you."

        "What a bizarre sight. Captain what is the situation?":
            e "What a bizarre sight. Captain what is the situation?"
            g "We're not entirely sure, sir. This dirty swordsman was moving like a whirlwind, I never seen someone swing in the air so accurately."
            g "We managed to subdue him when he finally collapsed from exhaustion. Well, more like he tired himself out in a couple seconds."
            n "Another guard chimed in"
            g2 "He had a strange sword, but we've confiscated it."
            g "We were just about to toss him in a cell and alert you, sir."

    n "You nod, contemplating the strange circumstances of the 'Dirty Swordsman'."
    
    menu:
        "Alright, have him held for now. I want to question him personally when he wakes.":
            g "Yes sir"
            g2 "Yes sir"
            #$ persistent.swordsman_imprison_day = current_day

        "Well at least make sure he gets fed first, I need him alive for questioning.":
            g "Yes sir"
            g2 "Yes sir"
            #$ persistent.swordsman_imprison_day = current_day
 
        "Make sure you rough him up a bit, I don't want him to attack me when I question him.":
            g "Yes sir"
            g2 "Yes sir"
            #$ gs.yojimbo_imprisioned_date      = current_day
            #$ gs.yojimbo_imprisioned_day_count = 1    
     
    n "You make a mental note that you should check in on the Dirty Swordsman, if only out of curiosity."   

label inspection:

    n "TODO: Base this off the tutorial"

label interrogate_yojimbo:

    n "You enter the tower where the Dirty Swordsman is held."
    n "There was little need in times past for a proper dungeon, so a little room was set aside for this man."
    n "The guard's common area was next door, so there was no real need to post guards or even to lock the man in."
    n "Without his sword the man was hardly any threat, and he even spoke the common tounge. He only ever made one request, to speak to the Lord of the Estate."
    n "As the acting Lord, you decided to give him his request, but honestly speaking you are curious about this man, who clearly hails from a land beyond the bounds of Albenora and Drilonis."
    n "What would you like to ask him first?"

    menu:
        "Where did you learn your swordplay?":
            pc "Where did you learn your swordplay?"

        "What were you thinking causing such a ruckus with a naked weapon?":
            pc "What were you thinking causing such a ruckus with a naked weapon?"

        "Are you a spy? Who are you working for?":
            pc "Are you a spy? Who are you working for?"
