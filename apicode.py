from google.cloud import dialogflow
session_client = dialogflow.SessionsClient()


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))



    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))

def welcome_text():
    project_id = "insurchatbot"
    session_id = "1234"

    session = session_client.session_path(project_id, session_id)
    event_input = dialogflow.EventInput(name='WELCOME', language_code='en-US')
    query_input = dialogflow.QueryInput(event=event_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    print(response.query_result)
    
#detect_intent_texts("insurchatbot","1234",["Hello"],"en-US")
welcome_text()
detect_intent_texts("insurchatbot","1234",["Ram"],"en-US")