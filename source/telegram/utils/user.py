class User:
    def __init__(self, chat_id, message_id=-1, player_id=-1, liked=None, playlists=None, language=None):
        self.chat_id = chat_id
        self.player_id = player_id
        self.message_id = message_id
        self.liked = self.unpack_liked(liked)
        self.language = language
        self.playlists = self.unpack_playlists(playlists)

    @staticmethod
    def unpack_playlists(data):
        if not data:
            return {}
        response = {}
        for pl in data.split(';;'):
            name = pl.split('::')[0]
            traks = pl.split('::')[1].split(',,')
            response[name] = traks
        return response

    @staticmethod
    def unpack_liked(data):
        if not data:
            return []
        return data.split(',,')

    def pack_liked(self):
        return ' '.join(self.liked)

    def pack_playlists(self):
        return ';;'.join([f'{key}::{",,".join(elem)}'for key, elem in self.playlists.items()])
