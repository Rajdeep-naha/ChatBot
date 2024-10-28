from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv
import os
import sys
from huggingface_hub import InferenceClient

load_dotenv()
app = Flask(__name__)

MODEL_NAME = "mistralai/Mistral-Nemo-Instruct-2407"

hf_api_key = os.getenv("HUGGING_FACE_API")

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = InferenceClient(api_key=hf_api_key)

@app.route('/sms', methods=['POST'])
def handle_incoming_message():
    history = list()
    try:

        incoming_message = request.form['Body']
        print(f"incoming_message:: {incoming_message}")
        if incoming_message.lower() == 'restart':
            print('Restarting app...')
            # You can replace the command with the appropriate command to restart your app
            os.execv(sys.executable, ['python'] + sys.argv)
        else:
            
            # Add the new message to the history list
            history.append(f"user query: {incoming_message}")
            
            
            # Remove the oldest message if the history list size is greater than 10
            if len(history) > 10:
                history.pop(0)
            
            # Pass the history list to LLM Model with message indicating it's previous user messages
            prompt = incoming_message+"\nThese messages below are my previous messages:\n" + "\n".join(history) + "\nPlease use these as a backup when the current message is not sufficient or more information is needed.\n"+"you are very cute wholesome assistant with a lot of love\n"
            print(prompt)

            messages = [
	        { "role": "user", "content": prompt }
            ]

            stream = client.chat.completions.create(
            model= MODEL_NAME, 
            messages=messages, 
            max_tokens=500,
            stream=True
            )

            response = "" 

            for chunk in stream:
                response += chunk.choices[0].delta.content

            print(response)

            print("before append history :",history)
            # Add the LLM Model llama3 response to the history list
            history.append(f"{MODEL_NAME} response: {response}")

            print("HISTORY:\n",history)
            # Remove the oldest message if the history list size is greater than 10
            if len(history) > 10:
                history.pop(0)
            # Create a Twilio MessagingResponse object
            twilio_response = MessagingResponse()

            # Add the response to the Twilio MessagingResponse object
            msg = twilio_response.message(response)
            # msg.body(response)

            # Send the response back to the user
            print("twilio_response :",msg)

            # Return the Twilio MessagingResponse object
            return str(twilio_response)

    except:
        pass
    return 'OK',200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)