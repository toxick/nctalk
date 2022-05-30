from typing import Union

from nextcloud import NextCloud

from nctalk.api import NextCloudTalkAPI
from nctalk.exceptions import NextCloudTalkNotCapable


class Chat(object):
    """Represents a NextCloud Chat Object."""

    def __init__(self, token: str, chat_api: 'ChatAPI'):
        self.token = token
        self.api = chat_api

    def __repr__(self):
        return f'{self.__class__.__name__}({self.__dict__})'

    def __str__(self):
        return f'Chat({self.token})'

    def receive_messages(
            self,
            last_known_message: int,
            last_common_read: int,
            look_into_future: bool = False,
            limit: int = 100,
            timeout: int = 30,
            set_read_marker: bool = True,
            include_last_known: bool = False):
        return self.api.query(
            method='GET',
            sub=f'/chat/{self.token}',
            data={
                'lookIntoFuture': 1 if look_into_future else 0,
                'limit': limit,
                'lastKnownMessageId': last_known_message,
                'lastCommonReadId': last_common_read,
                'timeout': timeout,
                'setReadMaker': 1 if set_read_marker else 0,
                'includeLastKnown': 1 if include_last_known else 0
            },
            include_headers=['X-Chat-Last-Given', 'X-Chat-Last-Common-Read']
        )

    def send(
            self,
            message: str,
            reply_to: int = 0,
            display_name: Union[str, None] = None,
            reference_id: Union[str, None] = None,
            silent: bool = False):
        """Send a text message to a conversation"""
        return self.api.query(
            method='POST',
            sub=f'/chat/{self.token}',
            data={
                "message": message,
                "replyTo": reply_to,
                "displayName": display_name,
                "referenceId": reference_id,
                "silent": silent
            }
        )


class ChatAPI(NextCloudTalkAPI):
    """Interface to the Conversations API.

    https://nextcloud-talk.readthedocs.io/en/latest/chat/
    """

    def __init__(self, client: NextCloud):
        """Initialize the Conversation API."""
        self.client = client
        if 'chat-v2' in self.client.capabilities:  # type: ignore
            self.api_endpoint = '/ocs/v2.php/apps/spreed/api/v1'
        else:
            raise NextCloudTalkNotCapable('Unable to determine chat endpoint.')

        super().__init__(client, api_endpoint=self.api_endpoint)
