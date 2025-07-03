label run_visitor_dialogue:
    python:

        default_event = "Inspection"
        for event, lines in current_visitor.dialogue_lines.items():
            if event == 'Inspection':
                current_character_event = current_visitor.name + "-" + current_visitor.event 
                # TODO: Check against global set 
                completed_events.add()
                for line in lines:
                    store.visitor_dialogue = line
                    renpy.pause(3.0)
        store.visitor_dialogue = ""


    return

label tutorial:

    n "Ahh, here comes the first visitor"
    jump day_loop

label day_loop:

    if daily_expended_points >= daily_action_points:
        jump day_end

    $ current_visitor = fur_merchant
    $ visitor_dialogue = ""

    show screen visitor_screening(current_visitor)
    call run_visitor_dialogue
    hide screen visitor_screening

    call screen visitor_screening(current_visitor)

    if visitor_decision:
        n "Correct Choice"
    else:
        n "Wrong decision"

    $ daily_expended_points += 1
    jump day_loop

screen visitor_screening(visitor):
    tag documents

    frame:
        xalign 0.5
        yalign 0.25
        vbox:
            spacing 15
            text "Name: [visitor.name]"
            text "[inspect_items(visitor.inventory)]" #style "monospaced"
            text "What's your call?"

            hbox:
                spacing 30
                textbutton "Approve" action [SetVariable("visitor_decision", True), Return()]
                textbutton "Deny" action [SetVariable("visitor_decision", False), Return()]
                textbutton "Apprehend" action [SetVariable("visitor_decision", False), Return()]  

    # Bottom-style dialogue display
    frame:
        style "say_window"
        xalign 0.5
        yalign 0.70
        xfill True
        yminimum 150

        text "[visitor_dialogue]" style "say_dialogue" xalign 0.5 yalign 1.0

label day_end:
    n "The day has ended; thank you for playing"
    return
