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
define gc = Character("Guard Captain Eos", color="#ADD8E6", what_color="#ADD8E6") # Light Blue
define e  = Character("Edgar", color="#FFA07A", what_color="#FFA07A")          # Light Salmon                                                   # Narrator, no name displayed
define g  = Character("Guard", color="#90EE90", what_color="#90EE90")          # Light Green
define g2 = Character("Guard 2")  
define tax_collector = Character("Ser Jorlen")

default fur_merchant = None
default yojimbo = None

init python:
    ### Story Progression Map

    event_tree = {
    "start": ["beginning"],
    "beginning": ["tutorial"],
    "tutorial": ["tutorial_combat","tutorial_deny","tutorial_approval"],
    "tutorial_combat": ["act_one"],
    "tutorial_approval": ["act_one"],
    "tutorial_deny": ["act_one"],
    "act_one": ["act_two"] 
    }

    ### Character ------------------------------------------------------------------------
    class PlayerCharacter:
        def __init__(self, name, inventory, **kwargs):
            self.name      = name,
            self.inventory = inventory
            self.strength  = kwargs.get("strength", 3),
            self.hp        = kwargs.get("hp", 50)

        def attack(self, target):
            damage     = self.strength
            target.hp -= damage
            target.hp  = max(target.hp, 0) 

            if target.hp == 0:
                target.status = 'Downed'

            renpy.notify(f"{self.name} strikes! {target.name} takes {damage} damage. ({target.hp} HP left)")

    class AllyCharacter:
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

### Screen for Event Tree
#    for label, (x, y) in positions.items():
#        frame:
#            xpos x ypos y
#            textbutton label action Jump(label)

screen event_tree:
    tag menu

    frame:
        xpos 100 ypos 100
        textbutton "start" action Jump("start")

    frame:
        xpos 200 ypos 100
        textbutton "beginning" action Jump("beginning")

    frame:
        xpos 500 ypos 100
        textbutton "tutorial" action Jump("tutorial")

    frame:
        xpos 700 ypos 100
        textbutton "tutorial_approval" action Jump("tutorial_approval")

    frame:
        xpos 700 ypos 300
        textbutton "tutorial_deny" action Jump("tutorial_deny")

    frame:
        xpos 700 ypos 500
        textbutton "tutorial_combat" action Jump("tutorial_combat")

    frame:
        xpos 1000 ypos 300
        textbutton "act_one" action Jump("act_one")

    frame:
        xpos 1200 ypos 300
        textbutton "act_two" action Jump("act_two")

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

    frame:
        xysize (config.screen_width, int(config.screen_height * 0.25))
        ypos int(config.screen_height * 0.75)
        background "#2228"

        hbox:
            spacing 20
            align (0.5, 0.5)

            textbutton "Strike"    action Function(duelist_one.attack, duelist_two)
            textbutton "Detain"    action Function(detain)
            textbutton "Cards"     action Function(use_cards)
            textbutton "Surrender" action Function(surrender)


### GAME START --------------------------------------------------------------------------- 
label start:

    n "Let's get started"
    show screen event_tree

    jump beginning
 
label beginning:

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

    $ captain_eos = AllyCharacter(
        id=3,
        name="Eos",
        inventory = {'Wolf Blade': 1, 'Sigil Shield': 1, 'Wife Given Locket': 1},
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
        jump tutorial_approval

    if visitor_decision == 'Deny':

        hide screen visitor_screening
        jump tutorial_deny

    if visitor_decision == 'Apprehend':

        hide screen visitor_screening
        jump tutorial_combat

    pause

label tutorial_approval:

    n "Everything seems to be in order."
    pc "I think everything is in order."
    jump act_one

label tutorial_deny:

    n "Everything seems to be not in order."
    jump act_one

label tutorial_combat:

    n "TODO: Make Combat System that is cool and fun." 
    jump act_one

label act_one:

    n "Now that we got through the basics, do you feel confident in the mechanics so far?"

label act_two:

    n "This is a placeholder for Act Two."

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
            pc "Have at you!"

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
            n "The man did not even look in your general direction. If anything his crossed arms and huffier attitude seemed similar to a petulant child."
            n "Oh wow there goes the chin, right into the air."
            n "What's wrong, sir, surely you didn't come all the way here to sit in this room with the likes of me?"
            yojimbo "Sir, you would deny me a fight when I ask, and when I am relaxing you want to stir the pot!"
            pc "I will apologize, you seem new to this land-"
            yojimbo "that is because I am sir, I come at the behest of the Great Emperor, in search of creating a bridge to the Western Lands."
            pc "That would be us right?"
            yojimbo "Yes! The Emperor saw in a dream, a dream that foretold of a great kingdom that rose in the west, one that will become a force to be reckoned with."
            pc "And where is this future kingdom to be staked? There is are two great kingdoms to the left and the right of you."
            yojimbo "And therefore"
            n "He said with rising glee"
            yojimbo "This is where that new kingdom will lie!"
            pc ".....here? In this keep?"
            yojimbo "I do not know that word, is that the name of this kingdom?"
            n "Captain Eos gave a grunt that was as close to laughter that man has ever conjured."
            n "He had been waiting slightly outside the room, and took a few steps in"
            captain_eos "You know to a loyal soldier or guard captain, even, that might sound like the embers of treason are brewing."
            n "The Captain raised you; more with waps and tackles than with hugs and kisses, but he has raised you nonetheless, and you caught yourself smirking at the idea"
            n "The Notion-"
            n "That this would be the man to end your bloodline over a misunderstanding of treason."

        "What were you thinking causing such a ruckus with a naked weapon?":
            pc "What were you thinking causing such a ruckus with a naked weapon?"
            yojimbo "Apologies! I am unaware of things work around here, but, I know people. And people will always respond to a man with a naked blade."
            n "The man smirked, as if he had said something quite clever."
            yojimbo "That aside, thank you for the rest room, I was running low on provisions, and I appreciate having a safe place to restock."

        "Are you a spy? Who are you working for?":
            pc "Are you a spy? Who are you working for?"
            n "The man made the most token of efforts to hide his amusement before laughing"
            yojimbo "HAAAAHAAA"
            yojimbo "I apologize, but the Emperor has much bigger things to oversee than a petty conflict between two nations that where the mud used to build is still wet."
            pc "Oh? Are you referring to the war between our two kingdoms? Is the scale truly so insignificant to you?"

label the_masked_merchant:

    n "A masked merchant walks into a bar. He says 'Ow'"

label the_albenoraian_collector:
    
    n "A sharp knock echoes through the keep, crisp and authoritative. One of your guards steps in a moment later, clearing his throat."
    g "My lord, a royal tax official has arrived. Says he brings revised collections orders from the capital-"
    n "Before the guard could finish you interupted his report with an audible sigh. These men always arrive uninvited, and never with good news."
    pc "Send him in."
    n "A tall man enters the chamber, dressed not in the finery of a nobleman, but in the layered silks and chain-threaded vestments of a King's agent. His boots are polished, his ledger thick, and his eyes already scanning your hall with quiet judgment."
    tax_collector "Lord Edgar, I presume. I am Ser Jorlen, royal assessor in service of Bardhyl II, King of Albenora."
    pc "I’ve received no notice of new assessments."
    tax_collector "And yet, here I stand. With revised requisitions due to the wartime burdens the Crown bears. Drilonis, as it happens, has been marked for re-evaluation."
    pc "Re-evaluation?"
    tax_collector "Yes, my lord. It appears this hold has benefitted from an increase in trade — caravans rerouting to avoid the troubled highways. A blessing, in the eyes of the Crown... and a taxable one."
    n "He sets the thick ledger down and opens it, flipping to a ribbon-marked page with casual finality."
    tax_collector "By decree of the Treasury, your hold is to remit twofold the standard tribute for the season. Effective immediately."
    pc "Twofold? That's nearly our entire grain reserve."
    tax_collector "Of course, the Crown need not account for every silver. There are... discretionary routes, in the interest of efficiency. And mutual understanding."
    n "The implication hangs in the air like the smell of damp iron. A bribe — offered without being named. If you pay him, your tribute may 'adjust'. If not, you may find yourself under deeper scrutiny."

    menu:
        "Challenge the demand openly":
            pc "Threefold? You would have me starve the village and sell off my steel? Show me the seal — or take this to the King yourself."
            n "The man narrows his eyes slightly. Not offended, but calculating. He snaps the ledger shut."
            tax_collector "Very well, my lord. But do remember — not all favors come with second chances."
            # $ set the result of the event flag to "refused"  

        "Give the man what he wants":
            pc "Surely a man of your station has more pressing matters than counting every last coin owed the Crown?"
            n "Ser Jorlen does not answer. His hand stills over the ledger, fingers lingering on the parchment like a spider deciding where to weave."
            pc "And I imagine a few coins gone astray would trouble no one — provided they found their way into the right hands."
            tax_collector "Tact is a virtue in these trying times, my lord. One hundred silvers. Off the record. No ink, no seal."
            n "You nod once. A servant is summoned; the purse is passed with the quiet weight of understanding. The ledger closes without further comment."
            #$ treasury -= 100  # or whatever currency you use
            tax_collector "Prudent rule, Lord Edgar. I'll see to it that the assessment reflects your... discernment."
            # $ set the result of the event flag to "bribed"

        "Intimidate Ser Jorlen":
            pc "You speak boldly for a man with no guards, no writ, and his back to my blade hall."
            n "He holds his palm in your direction, barely giving you a look."
            tax_collector "Save it. I travel with an envoy of royal knights, even if you succeed this shortsighted affair, the next one will come with an order of execution. That is, if you think you can take on a Royal Knight."
            n "A man in massive armor appeared seemingly out of nowhere with the slightest of movements. You look at the sword and armor and see the material is more than adequate to stop you, let alone the skill the man must have."
            pc "Apologies, ser. I was making an observation, nothing more."
            tax_collector "Quite. I also observed an additional 50 silver on the ledger, thank you for bringing it to my attention."
            tax_collector "It is only fortunate that this observation is beneath the notice of the King."
            n "Unbenownst to the members of this conversation, another person who was also in the habit of observing, had decided it was a good time to leave. "