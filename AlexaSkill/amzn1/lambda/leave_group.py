import ask_sdk_core.utils as ask_utils
import requests

from base import Base


class LeaveGroupIntentRequestHandler(Base):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("LeaveGroupIntent")(handler_input)

    def handle(self, handler_input):
        req_envelope = handler_input.request_envelope

        if not (req_envelope.context.system.user.permissions and
                req_envelope.context.system.user.permissions.consent_token):
            return self.check_permissions(handler_input)

        current_attendee = self.get_attendee(handler_input)
        slots = handler_input.request_envelope.request.intent.slots
        group_name = slots["group_name"].value.replace(" ", "")
        group = self.get_group(group_name.title())
        term = group.get("current_term")
        speak_output = "You are not in this group."

        r = requests.get(f"{self.url}/groups/term/{term}/")
        term_object = r.json()
        attendees = term_object["attendees"]

        if current_attendee.get("uuid") in attendees:
            attendees.remove(current_attendee["uuid"])
            payload = {"group": term_object["group"], "attendees": attendees, "join_url": term_object["join_url"]}
            requests.put(f"{self.url}/groups/term/{term}/", payload)
            speak_output = f"you have left {group['name']} {group['provider']}"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
