"""Classes representing Rich Objects for sharing."""


from nctalk.exceptions import NextCloudTalkException


class NextCloudTalkRichObject(object):
    """Base Class for Rich Objects."""

    id = None
    name = None
    object_type = None

    def __init__(self, data: dict):
        if 'id' not in data or 'name' not in data:
            raise NextCloudTalkException(f'{__class__.__name__} requires `id` and `name`.')
        self.__dict__.update(data)

    def metadata(self):
        """Return metadata array."""
        return {'id': self.id, 'name': self.name}


class AddressBook(NextCloudTalkRichObject):

    object_type = 'addressbook'


class AddressBookContact(NextCloudTalkRichObject):

    object_type = 'addressbook-contact'


class Announcement(NextCloudTalkRichObject):

    object_type = 'announcement'


class Calendar(NextCloudTalkRichObject):

    object_type = 'calendar'


class CalendarEvent(NextCloudTalkRichObject):

    object_type = 'calendar-event'


class Call(NextCloudTalkRichObject):

    object_type = 'call'
    call_type = None

    def __init__(self, data: dict):
        if 'call_type' not in data:
            raise NextCloudTalkException(f'\'call_type\' required for {__class__.__name__}')
        super().__init__(data)

    def metadata(self):
        return {
            'id': self.id,
            'name': self.name,
            'call-type': self.call_type
        }


class Circle(NextCloudTalkRichObject):

    object_type = 'circle'


class DeckBoard(NextCloudTalkRichObject):

    object_type = 'deck-board'


class DeckCard(NextCloudTalkRichObject):

    object_type = 'deck-card'


class Email(NextCloudTalkRichObject):

    object_type = 'email'


class File(NextCloudTalkRichObject):

    object_type = 'file'


class Form(NextCloudTalkRichObject):

    object_type = 'forms-form'


class GeoLocation(NextCloudTalkRichObject):

    object_type = 'geo-location'
    latitude = None
    longitude = None

    def __init__(self, name: str, latitude: str, longitude: str):
        data = {
            'id': f'geo:{latitude},{longitude}',
            'name': name,
            'longitude': longitude,
            'latitude': latitude}
        super().__init__(data)

    def __str__(self):
        return f'{__class__.__name__}'\
               f'(latitude={self.latitude}, longitude={self.longitude})'

    def metadata(self):
        return {
            'id': f'geo:{self.latitude},{self.longitude}',
            'name': self.name,
            'latitude': self.latitude,
            'longitude': self.longitude,
        }


class TalkAttachment(NextCloudTalkRichObject):

    object_type = 'talk-attachment'


class User(NextCloudTalkRichObject):

    object_type = 'user'


class UserGroup(NextCloudTalkRichObject):

    object_type = 'user-group'