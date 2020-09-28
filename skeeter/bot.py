import os
from pydash import py_
from slack import WebClient
from skeeter.utils import older_than_threshold, clean_url


class Bot:
    """ Instantiates a Bot object to handle Slack interactions."""

    def __init__(self, token=None):
        """
        When we instantiate a new bot object, we access the app
        credentials set earlier in our local development environment.
        """

        if not token:
            token = os.environ.get("SLACK_BOT_TOKEN")

        self.client = WebClient(token)

    def list_channels(self, limit=1000):
        """
        Lists all channels in the workspace.
        """

        return self.client.conversations_list(limit=limit, exclude_archived=1).data.get(
            "channels", None
        )

    def list_messages(self, channel, limit=1000):
        """
        Lists all messages in a channel.
        """

        return self.client.conversations_history(channel=channel, limit=limit).data.get(
            "messages", None
        )

    def list_replies(self, channel, ts, oldest=0):
        """
        Lists all replies to a message, including the message.

        :param oldest: controls the oldest ts to consider while filtering
        """

        replies = self.client.conversations_replies(
            channel=channel, ts=ts, oldest=oldest
        ).data.get("messages", None)

        # this is because `oldest` filter isn't applied to the head of the thread
        return py_.filter(
            replies,
            lambda reply: not older_than_threshold(reply["ts"], threshold=oldest),
        )

    def collect_replies(self, channel, messages, oldest=0):
        """
        Collect replies of a list of messages.
        """

        replies = [
            self.list_replies(channel=channel, ts=message["ts"], oldest=oldest)
            for message in messages
        ]
        return py_.flatten(replies)

    def post_message(self, channel_name, text, unfurl_links=True):
        """
        Posts message to channel.
        """

        channel = self.channel_name_to_id(channel_name)
        if not self.duplicate_exists(channel, text):
            _ = self.client.chat_postMessage(
                channel=channel, text=text, unfurl_links=unfurl_links
            )

    def duplicate_exists(self, channel, text):
        """
        Checks if message with duplicate text exists. Simple sanity check.
        """

        messages = self.list_messages(channel=channel)
        if any(message["text"] == text for message in messages):
            return True
        else:
            return False

    def channel_name_to_id(self, channel_name):
        """
        Return channel id for given channel name.
        """

        channels = self.list_channels()
        result = py_.find(channels, lambda channel: channel["name"] == channel_name)
        if result:
            return result["id"]
        else:
            raise ValueError(f"Channel {channel_name} not found")

    def create_link(self, channel, message_ts):
        """
        Returns permanent link to existing message.
        """

        response = self.client.chat_getPermalink(channel=channel, message_ts=message_ts)
        return clean_url(response.get("permalink", None))
