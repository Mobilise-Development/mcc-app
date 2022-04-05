import ask_sdk_core.utils as ask_utils

from base import Base


class ListGroupIntentRequestHandler(Base):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ListGroupIntent")(handler_input)

    def handle(self, handler_input):
        available_groups = self.get_available_groups()
        speak_output = f"There are currently {len(available_groups)} groups available, here are the available groups: "
        if len(available_groups) == 0:
            speak_output = "There are currently no available groups."
        for group in available_groups:
            speak_output = speak_output + group + ", "
        
        return (
                handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
    
class ListCategoryGroupIntentRequestHandler(Base):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ListCategoryGroupIntent")(handler_input)
        
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        category = slots["category"].value
        available_groups = self.get_available_groups(category)

        speak_output = f"There are currently {len(available_groups)} {category} groups available, here are the available groups: "
        for group in available_groups:
            speak_output = speak_output + group + ', '
        
        return (
                handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
