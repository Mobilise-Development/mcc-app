import ask_sdk_core.utils as ask_utils

from base import Base


class MyGroupsIntentRequestHandler(Base):
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("MyGroupsIntent")(handler_input)

    def handle(self, handler_input):
        req_envelope = handler_input.request_envelope

        if not (req_envelope.context.system.user.permissions and
                req_envelope.context.system.user.permissions.consent_token):
            return self.check_permissions(handler_input)

        speak_output = "You are not currently a part of any groups. You can ask me what groups are available."
        attendee = self.get_attendee(handler_input)
        groups_list = attendee.get('groups_list')

        if groups_list:
            speak_output = f"You are currently in {len(groups_list)} groups, they are: "
            for group in groups_list:
                speak_output = speak_output + group + ', '

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
