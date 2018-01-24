# coding=UTF-8
import slackclient, time, random

slack_bot_name = 'un-poohpeer'
puper_member_id = 'U4LEYSZB6'
slack_bot_secret = 'xoxb-304697651878-9SXyyoRRw0Dpx9TneHQWYOGs'
slack_bot_id = 'U8YLHK5RU'
schultz_id = 'U4KPC46Q1'
# delay in seconds before checking for new events
SOCKET_DELAY = 1

# initialize slack client
slack_bot_client = slackclient.SlackClient(slack_bot_secret)
# check if everything is alright
print(slack_bot_name)
print(slack_bot_secret)
is_ok = slack_bot_client.api_call("users.list").get('ok')
print(is_ok)

# find the id of our slack bot
if(is_ok):
    for user in slack_bot_client.api_call("users.list").get('members'):
        if user.get('name') == slack_bot_name:
            print(user.get('id'))


# how the bot is mentioned on slack
def get_mention(user):
    return '<@{user}>'.format(user=user)

puper_mention = get_mention(puper_member_id)
slack_bot_mention = get_mention(slack_bot_id)
schultz_mention = get_mention(schultz_id)

def is_for_me(event):
    """Know if the message is dedicated to me"""
    # check if not my own event
    type = event.get('type')
    if type and type == 'message' and not (event.get('user') == slack_bot_id):
        # in case it is a private message return true
        if is_private(event):
            return True
        # in case it is not a private message check mention
        text = event.get('text')
        channel = event.get('channel')
        # if slack_bot_mention in text.strip().split():
        return True


def say_hi(user_mention):
    """Say Hi to a user by formatting their mention"""
    response_template = random.choice(['Sup, {mention}...',
                                       'Yo!',
                                       'Hola {mention}',
                                       'Bonjour!'])
    return response_template.format(mention=user_mention)


def say_bye(user_mention):
    """Say Goodbye to a user"""
    response_template = random.choice(['See you later, alligator...',
                                       'adios amigo',
                                       'Bye {mention}!',
                                       'Au revoir!'])
    return response_template.format(mention=user_mention)


def do_the_unpoohpeer(user_mention):
    response_template = random.choice(['Не пизди!',
                                       'Харэ пиздеть!',
                                       'Нахуя так делать?',
                                       'Нубля!'])
    return response_template.format(mention=user_mention)


def is_hi(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['hello', 'bonjour', 'hey', 'hi', 'sup', 'morning', 'hola', 'ohai', 'yo'])


def is_bye(message):
    tokens = [word.lower() for word in message.strip().split()]
    return any(g in tokens
               for g in ['bye', 'goodbye', 'revoir', 'adios', 'later', 'cya'])


def is_puper(user):
    return get_mention(user) == puper_mention


def handle_message(message, user, channel):
    if is_hi(message):
        user_mention = get_mention(user)
        post_message(message=say_hi(user_mention), channel=channel)
    elif is_bye(message):
        user_mention = get_mention(user)
        post_message(message=say_bye(user_mention), channel=channel)
    elif is_puper(user):
        print "Attention, Poohpeer is speaking..."
        user_mention = get_mention(user)
        post_message(message=do_the_unpoohpeer(user_mention), channel=channel)


def post_message(message, channel):
    slack_bot_client.api_call('chat.postMessage', channel=channel,
                          text=message, as_user=True)


def run():
    if slack_bot_client.rtm_connect():
        print('[.] Un-poohpeer is here...')
        while True:
            event_list = slack_bot_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    print(event)
                    if is_for_me(event):
                        handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(SOCKET_DELAY)
    else:
        print('[!] Connection to Slack failed.')


def is_private(event):
    """Checks if private slack channel"""
    return event.get('channel').startswith('D')


if __name__=='__main__':
    run()