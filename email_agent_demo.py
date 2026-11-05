"""Demonstrate configuring the reusable Agent framework for email handling."""

from email_agent import (
    Agent,
    add_label,
    describe_sender,
    do_nothing,
    get_email_prompt,
    respond_to_email,
)

EMAIL_ACTIONS = [
    {
        "action_name": "respond_to_email",
        "action_description": "Reply when the email is important and needs a response.",
        "action_function": respond_to_email,
        "requires_permission": True,
    },
    {
        "action_name": "add_label",
        "action_description": "Label important email that does not need a reply.",
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


def main() -> None:
    while True:
        from_email = input("Enter the sender's email address: ")
        subject = input("Enter the subject of the email: ")
        email_text = input("Enter the text of the email: ")

        email_data = {
            "from": from_email,
            "subject": subject,
            "text": email_text,
            "sender_description": describe_sender(from_email),
        }

        email_agent.run(get_email_prompt(email_data), email_data)


if __name__ == "__main__":
    main()
