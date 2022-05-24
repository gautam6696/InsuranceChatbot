from google.cloud import dialogflow
import json
from google.oauth2 import service_account

project_id = 'nova-dskj'

with open('C:/Users/Gautam/Downloads/insur-arcw-f8ac168f2276.json') as source:
    info = json.load(source)

storage_credentials = service_account.Credentials.from_service_account_info(info)
session_client = dialogflow.SessionsClient(credentials=storage_credentials)
def detect_intent_texts(project_id, session_id, text, language_code="en-US"):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    

    session = session_client.session_path(project_id, session_id)
    #print("Session path: {}\n".format(session))


    text_input = dialogflow.TextInput(text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    intent_name = response.query_result.intent.display_name

    #richresponses = response.query_result.fulfillment_messages
    return response
    # return response.query_result.fulfillment_messages,intent_name
        
        # for message in richresponses:
        #     if message.text:
        #         print("Not welcome ", message.text.text[0])


def welcome_text(project_id = "nova-dskj", session_id= "1234"):

    session = session_client.session_path(project_id, session_id)
    event_input = dialogflow.EventInput(name='WELCOME', language_code='en-US')
    query_input = dialogflow.QueryInput(event=event_input)
    response = session_client.detect_intent(session=session, query_input=query_input)
    richresponses = response.query_result.fulfillment_messages
    # return 0
    
    
    # for message in richresponses:
    #     print("This is ", message.text.text[0])
    return response.query_result.fulfillment_messages

    
    
# detect_intent_texts("insurchatbot","1234","Hello","en-US")
# project_id = "insurchatbot"
# welcome_text()
# detect_intent_texts("insurchatbot","1234","Ram","en-US")

