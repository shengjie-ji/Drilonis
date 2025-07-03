# globals.rpy

default daily_action_points = 2
default daily_expended_points = 0
default current_visitor = None
default visitor_decision = None
default visitor_dialogue = ""

define n = Character("Narrator")                   

#default persistent.gs = GameStateManager()

init -98 python:
    def inspect_items(items):
        if not items:
            return "No items presented."
    
        lines = []
        for item, amount in items.items():
            lines.append(f"•\t{amount} {item}")
        return "\n".join(lines)


    if not hasattr(store, "completed_events"):
    	store.completed_events = set()

    