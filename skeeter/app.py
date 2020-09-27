"""
Gossip collect bot

Usage:
  skeeter [--config <config-path>] [--limit <messages-per-channel>] [--minutes <time-to-oldest>]

Options:
  --config <config-path>                path to configs for gossip channels [default: config/default.yaml]
  --limit <messages-per-channel>        number of messages to pull per channel [default: 25]
  --minutes <time-to-oldest>            minutes into the past to filter messages by [default: 30]
"""

import yaml
from pydash import py_
from docopt import docopt
from skeeter.bot import Bot
from skeeter.utils import past_timestamp


def main():
    args = docopt(__doc__)

    myBot = Bot()

    config = yaml.safe_load(open(args["--config"]))
    for destination, gossip in config.items():

        print(f":: Writing to destination: {destination}")

        channels = py_.filter(
            myBot.list_channels(), lambda channel: channel["name"] in gossip["sources"]
        )

        for channel in channels:

            print(f':: Parsing messages from source: {channel["name"]}')

            messages = myBot.list_messages(
                channel=channel["id"], limit=int(args["--limit"])
            )
            replies = myBot.collect_replies(
                channel=channel["id"],
                messages=messages,
                oldest=past_timestamp(minutes=int(args["--minutes"])),
            )

            print(f":: Found {len(replies)} messages")

            for message in replies:
                if any(word in message["text"] for word in gossip["words"]):

                    print(f':: Matching message with text: {message["text"]}')
                    print(
                        f':: Writing from source: {channel["name"]} to destination: {destination}'
                    )

                    message_link = myBot.create_link(
                        channel=channel["id"], message_ts=message["ts"]
                    )

                    myBot.post_message(
                        channel_name=destination, text=message_link, unfurl_links=True
                    )
