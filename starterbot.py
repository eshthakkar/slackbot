import os
from slackclient import SlackClient
import time

# Starter bot's id as an environment variable
BOT_ID = os.environ.get('BOT_ID')

AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# Instantiate slack client with our token
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))




def parse_slack_output(slack_rtm_output):

    output_list = slack_rtm_output

    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                return output['text'].split(AT_BOT)[1].strip().lower(), output['channel']

    return None, None 


def handle_command(command, channel):
    print "Hi"

    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
                "* command with numbers, delimited by spaces."

    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure.... Help me do something for you!"  

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)              


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 

    if slack_client.rtm_connect():
        print "starterbot connected and running!"

        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print "Connection failed. Invalid slack token or bot ID!" 
