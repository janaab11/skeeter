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
from skeeter.utils import past_timestamp, log_exceptions
from skeeter.logger import logger


@log_exceptions
def main():
    args = docopt(__doc__)

    config = yaml.safe_load(open(args["--config"]))

    for destination, gossip in config.items():

        logger.info(f":: Writing to destination: {destination}")

        myBot = Bot()

        channels = py_.filter(
            myBot.list_channels(), lambda channel: channel["name"] in gossip["sources"]
        )

        for channel in channels:

            logger.info(
                f':: Parsing {int(args["--limit"])} message heads from source: {channel["name"]}'
            )

            messages = myBot.list_messages(
                channel=channel["id"], limit=int(args["--limit"])
            )

            logger.info(f":: Collecting all replies")

            replies = myBot.collect_replies(
                channel=channel["id"],
                messages=messages,
                oldest=past_timestamp(minutes=int(args["--minutes"])),
            )

            logger.info(f":: Found {len(replies)} messages")

            post = False
            for message in replies:

                if any(word in message["text"] for word in gossip["words"]):

                    logger.info(f':: Matching message with text: {message["text"]}')

                    message_link = myBot.create_link(
                        channel=channel["id"], message_ts=message["ts"]
                    )

                    logger.info(
                        f':: Writing from source: {channel["name"]} to destination: {destination}'
                    )

                    myBot.post_message(
                        channel_name=destination, text=message_link, unfurl_links=True
                    )
                    post = True

            if not post:
                logger.info(f":: No matching messages")
