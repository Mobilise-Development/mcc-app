import ask_sdk_core.utils as ask_utils
import requests

from base import Base


class JoinGroupIntentRequestHandler(Base):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("JoinGroupIntent")(handler_input)

    def handle(self, handler_input):
        req_envelope = handler_input.request_envelope

        if not (req_envelope.context.system.user.permissions and
                req_envelope.context.system.user.permissions.consent_token):
            return self.check_permissions(handler_input)

        attendee = self.get_attendee(handler_input)
        slots = handler_input.request_envelope.request.intent.slots
        group_name = slots["group_name"].value
        format_group_name = group_name.replace(" ", "")
        available_groups = self.get_available_groups()
        group = self.get_group(format_group_name.title())
        group_title = f"{group['name']}{group['provider']}"
        speak_output = f"Sorry, {group_name} does not exist {group['name']}"

        if group_title in available_groups:
            if self.check_permissions(handler_input):
                attendee = self.get_attendee(handler_input)

            name = group.get('name')
            provider = group.get('provider')
            current_term = group["current_term"]
            requests.post(f"{self.url}/access/", {"proposer": attendee["uuid"], "term": current_term})
            speak_output = f"I have sent a request for you to join the {name} {provider} group"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
