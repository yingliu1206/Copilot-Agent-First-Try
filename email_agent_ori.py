from basic_agent import get_genai_response


def get_dev_prompt():
    return """
            You are an email classification agent.
            You will receive email data from the user. Based on that data, you will choose exactly one of these actions:
            - respond_to_email: If the email is important and requires a response, choose this action.
            - add_label: If the email is important but does not require a response, choose this action
            - do_nothing: If the email is not important, choose this action.

            Respond only with the action name. Do not include any explanations.
            """


def get_user_prompt(email_data):
    return f"""
            Here is the email data:
            From: {email_data['from']}
            Sender Description: {email_data['sender_description']}
            Subject: {email_data['subject']}
            Text: {email_data['text']}

            Based on this information, choose one of the actions specified in the developer prompt.
            """


# Brain
def make_decision(input_data):
    response = get_genai_response(
        dev_prompt=get_dev_prompt(),
        user_prompt=get_user_prompt(input_data)
    )

    return response.strip()  # Return the action name as a string, stripped of whitespace.

    # from_email = input_data['from']
    # subject = input_data['subject']
    # email_text = input_data['text']
    
    # if 'big sale' in email_text.lower():
    #     return "respond_to_email"
    # elif 'urgent' in subject.lower():
    #     return "add_label"
    # elif from_email.endswith('@spam.com'):
    #     return "do_nothing"


# Tools
def respond_to_email(response_text):
    print(f'Responding to email with: {response_text}')


def add_label(label):
    print(f'Adding label: {label}')


# Additional Knowledge
def describe_sender(email_address):
    if email_address.endswith('@trusted.com'):
        return "The sender is from a trusted domain."
    elif email_address.endswith('@spam.com'):
        return "The sender is from a known spam domain."
    else:
        return "The sender's domain is unknown."


# Plumbing
def execute_decision(decision):
    if decision == "respond_to_email":
        respond_to_email("Thank you for your email. I will get back to you shortly.")
    elif decision == "add_label":
        add_label("Important")
    elif decision == "do_nothing":
        print("No action taken.")
    else:
        print("Unknown decision.")


if __name__ == "__main__":
    while True:
        from_email = input('Enter the sender\'s email address: ')
        additional_info = describe_sender(from_email)
        subject = input('Enter the subject of the email: ')
        email_text = input('Enter the text of the email: ')

        email_data = {
            'from': from_email,
            'subject': subject,
            'text': email_text,
            'sender_description': additional_info
        }
        
        decision = make_decision(email_data)
        execute_decision(decision)
