import requests
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_model.ui import AskForPermissionsConsentCard


class Base(AbstractRequestHandler):
    def __init__(self):
        self.permissions = ["alexa::profile:email:read", "alexa::profile:name:read"]
        self.url = "http://18.133.92.248/api"
        super().__init__()

    def get_available_groups(self, category=None):
        available_groups = []

        if category:
            r = requests.get(f"{self.url}/groups/management/", params={"category": category.upper()})
        else:
            r = requests.get(f"{self.url}/groups/management/")

        data = r.json()

        for group in data:
            if group['active']:
                available_groups.append(f"{group['name']}{group['provider']}")
        return available_groups

    def check_permissions(self, handler_input):
        response_builder = handler_input.response_builder
        response_builder.speak(
            "I need to send your name and email address to the group admin, please give me permission on the Alexa app.")
        response_builder.set_card(
            AskForPermissionsConsentCard(permissions=self.permissions))
        return response_builder.response

    def get_attendee(self, handler_input):
        req_envelope = handler_input.request_envelope
        response_builder = handler_input.response_builder

        if not (req_envelope.context.system.user.permissions and
                req_envelope.context.system.user.permissions.consent_token):
            self.check_permissions(handler_input)

        context = handler_input.request_envelope.context
        accesstoken = str(context.system.api_access_token)
        email_endpoint = f"{context.system.api_endpoint}/v2/accounts/~current/settings/Profile.email"
        name_endpoint = f"{context.system.api_endpoint}/v2/accounts/~current/settings/Profile.name"
        api_access_token = "Bearer " + accesstoken
        headers = {"Authorization": api_access_token}
        email_r = requests.get(email_endpoint, headers=headers)
        name_r = requests.get(name_endpoint, headers=headers)
        email = email_r.json()
        full_name = name_r.json()

        try:
            r = requests.get(f"{self.url}/attendee/", params={"email": email})
            data = r.json()
            attendee = data[0]
        except IndexError:
            self.create_attendee(email, full_name)
            r = requests.get(f"{self.url}/attendee/", params={"email": email})
            data = r.json()
            attendee = data[0]
        # data = r.json()
        # for attendee in data:
        #     if email == attendee["email"]:
        #         return attendee
        print("ATTENDEE", attendee)
        return attendee

    def create_attendee(self, email, full_name):
        attendee_object = {"full_name": full_name, "email": email, "alexa_id": "1234"}
        r = requests.post(f"{self.url}/attendee/", attendee_object)

    def get_group(self, group):
        r = requests.get(f"{self.url}/groups/management/{group}/")
        return r.json()
