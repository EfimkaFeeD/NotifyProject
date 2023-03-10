import sqlalchemy
from telegram.utils.connect_creater import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'
    chat_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    player_id = sqlalchemy.Column(sqlalchemy.Integer, default=-1)
    message_id = sqlalchemy.Column(sqlalchemy.Integer, default=-1)
    liked = sqlalchemy.Column(sqlalchemy.String, default='')
    language = sqlalchemy.Column(sqlalchemy.String, default='')
    playlists = sqlalchemy.Column(sqlalchemy.String, default='')

    def get_playlists(self):
        if not self.playlists:
            return {}
        response = {}
        for pl in self.playlists.split(';;'):
            name = pl.split('::')[0]
            traks = pl.split('::')[1].split(',,')
            response[name] = traks
        return response

    def get_liked(self):
        if not self.liked:
            return []
        return self.liked.split(',,')

    def pack_liked(self):
        return ' '.join(self.liked)

    def pack_playlists(self):
        return ';;'.join([f'{key}::{",,".join(elem)}'for key, elem in self.playlists.items()])
