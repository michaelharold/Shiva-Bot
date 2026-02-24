from rasa_sdk import Action, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from typing import Dict, Text, Any
import requests


class ValidateLeaveForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_leave_form"

    def validate_employee_id(
        self, value: Text, dispatcher: CollectingDispatcher,
        tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        if value.isdigit():
            return {"employee_id": value}
        else:
            dispatcher.utter_message(text="Employee ID must be numeric.")
            return {"employee_id": None}

    def validate_leave_type(
        self, value: Text, dispatcher: CollectingDispatcher,
        tracker, domain: Dict[Text, Any]
    ) -> Dict[Text, Any]:

        valid_types = ["casual", "sick", "earned"]

        if value.lower() in valid_types:
            return {"leave_type": value.lower()}
        else:
            dispatcher.utter_message(
                text="Leave type must be casual, sick, or earned."
            )
            return {"leave_type": None}


class ActionSubmitLeaveForm(Action):

    def name(self) -> Text:
        return "action_submit_leave_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker, domain):

        employee_id = tracker.get_slot("employee_id")
        leave_type = tracker.get_slot("leave_type")

        response = requests.get(
            f"http://localhost:5000/api/leave/{employee_id}/{leave_type}"
        )
        data = response.json()

        dispatcher.utter_message(
            text=f"You have {data['balance']} {leave_type} leaves remaining."
        )

        return [
            SlotSet("employee_id", None),
            SlotSet("leave_type", None)
        ]


class ActionPayroll(Action):

    def name(self) -> Text:
        return "action_payroll"

    def run(self, dispatcher, tracker, domain):

        employee_id = tracker.get_slot("employee_id")

        if not employee_id:
            dispatcher.utter_message(text="Please provide your employee ID.")
            return []

        response = requests.get(
            f"http://localhost:5000/api/payroll/{employee_id}"
        )
        data = response.json()

        dispatcher.utter_message(
            text=f"Your salary is {data['salary']} and bonus is {data['bonus']}."
        )

        return [SlotSet("employee_id", None)]


class ActionBenefits(Action):

    def name(self) -> Text:
        return "action_benefits"

    def run(self, dispatcher, tracker, domain):

        response = requests.get(
            "http://localhost:5000/api/benefits"
        )
        data = response.json()

        message = "\n".join([f"{k}: {v}" for k, v in data.items()])
        dispatcher.utter_message(text=f"Company Benefits:\n{message}")

        return []