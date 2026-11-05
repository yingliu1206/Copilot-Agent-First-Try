from collections.abc import Callable
from typing import Any

from basic_agent import get_genai_response

Action = dict[str, Any]


class Agent:
    """Choose and execute one of the actions provided to the agent."""

    def __init__(self, actions: list[Action]):
        if not actions:
            raise ValueError("An agent must have at least one action.")

        self.actions = actions
        self.actions_by_name = {}
        for action in actions:
            required_keys = {
                "action_name",
                "action_description",
                "action_function",
                "requires_permission",
            }
            missing_keys = required_keys - action.keys()
            if missing_keys:
                raise ValueError(
                    f"Action is missing required keys: {', '.join(sorted(missing_keys))}"
                )
            if action["action_name"] in self.actions_by_name:
                raise ValueError(f"Duplicate action name: {action['action_name']}")
            self.actions_by_name[action["action_name"]] = action

    def get_developer_prompt(self) -> str:
        action_descriptions = "\n".join(
            f"- {action['action_name']}: {action['action_description']}"
            for action in self.actions
        )
        return (
            "You are an assistant that chooses exactly one action based on the "
            "user's input.\n"
            f"Available actions:\n{action_descriptions}\n\n"
            "Respond only with the action name. Do not include any explanations."
        )

    def decide(self, user_prompt: str) -> str:
        decision = get_genai_response(
            dev_prompt=self.get_developer_prompt(),
            user_prompt=user_prompt,
        ).strip()
        if decision not in self.actions_by_name:
            raise ValueError(f"Agent returned an unknown action: {decision!r}")
        return decision

    def execute(self, action_name: str, input_data: Any) -> Any:
        try:
            action = self.actions_by_name[action_name]
        except KeyError as error:
            raise ValueError(f"Unknown action: {action_name!r}") from error

        if action["requires_permission"]:
            approval = input(
                f"Approve action '{action_name}' "
                f"({action['action_description']})? [y/N]: "
            )
            if approval.strip().lower() not in {"y", "yes"}:
                print(f"Action '{action_name}' was not approved.")
                return None

        action_function: Callable[[Any], Any] = action["action_function"]
        return action_function(input_data)

    def run(self, user_prompt: str, input_data: Any) -> Any:
        decision = self.decide(user_prompt)
        return self.execute(decision, input_data)


def get_email_prompt(email_data: dict[str, str]) -> str:
    return f"""Here is the email data:
From: {email_data['from']}
Sender Description: {email_data['sender_description']}
Subject: {email_data['subject']}
Text: {email_data['text']}

Based on this information, choose one of the available actions."""


def respond_to_email(email_data: dict[str, str]) -> None:
    response_text = "Thank you for your email. I will get back to you shortly."
    print(f"Responding to {email_data['from']} with: {response_text}")


def add_label(email_data: dict[str, str]) -> None:
    print(f"Adding the Important label to email from {email_data['from']}.")


def do_nothing(email_data: dict[str, str]) -> None:
    print("No action taken.")


def describe_sender(email_address: str) -> str:
    if email_address.endswith("@trusted.com"):
        return "The sender is from a trusted domain."
    if email_address.endswith("@spam.com"):
        return "The sender is from a known spam domain."
    return "The sender's domain is unknown."


EMAIL_ACTIONS: list[Action] = [
    {
        "action_name": "respond_to_email",
        "action_description": "Send a reply when the email is important and needs a response.",
        "action_function": respond_to_email,
        "requires_permission": True,
    },
    {
        "action_name": "add_label",
        "action_description": "Apply the Important label when the email matters but needs no reply.",
        "action_function": add_label,
        "requires_permission": False,
    },
    {
        "action_name": "do_nothing",
        "action_description": "Take no action when the email is not important.",
        "action_function": do_nothing,
        "requires_permission": False,
    },
]

email_agent = Agent(EMAIL_ACTIONS)


def make_decision(input_data: dict[str, str]) -> str:
    return email_agent.decide(get_email_prompt(input_data))


def execute_decision(decision: str, input_data: dict[str, str]) -> Any:
    return email_agent.execute(decision, input_data)


if __name__ == "__main__":
    while True:
        from_email = input("Enter the sender's email address: ")
        additional_info = describe_sender(from_email)
        subject = input("Enter the subject of the email: ")
        email_text = input("Enter the text of the email: ")

        email_data = {
            "from": from_email,
            "subject": subject,
            "text": email_text,
            "sender_description": additional_info,
        }

        email_agent.run(get_email_prompt(email_data), email_data)
