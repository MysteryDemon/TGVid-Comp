import datetime
import motor.motor_asyncio
from config import Config
from .utils import send_log

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.users

    def new_user(self, id):
        return dict(
            id=int(id),
            join_date=datetime.date.today().isoformat(),
            caption=None,
            thumbnail=None,
            ffmpegcode=None,
            metadata=""" -map 0 -c:s copy -c:a copy -c:v copy -metadata title="Powered By:- @Kdramaland" -metadata author="@Snowball_Official" -metadata:s:s title="Subtitled By :- @Kdramaland" -metadata:s:a title="By :- @Kdramaland" -metadata:s:v title="By:- @Snowball_Official" """,
            ban_status=dict(
                is_banned=False,
                ban_duration=0,
                banned_on=datetime.date.max.isoformat(),
                ban_reason=''
            )
        )

    async def set_caption(self, user_id, caption):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('caption', None)
    

    async def set_thumbnail(self, user_id, thumbnail):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'thumbnail': thumbnail}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('thumbnail', None)
    

    async def set_ffmpegcode(self, user_id, ffmpegcode):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'ffmpegcode': ffmpegcode}})

    async def get_ffmpegcode(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('ffmpegcode', None)
    

    async def set_metadata(self, user_id, metadata):
        await self.col.update_one({'id': int(user_id)}, {'$set': {'metadata': metadata}})

    async def get_metadata(self, id):
        user = await self.col.find_one({'id': int(id)})
        return user.get('metadata', None)

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)
            await send_log(b, u)

    async def is_user_exist(self, id):
        user = await self.col.find_one({'id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})

    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})

    async def ban_user(self, user_id, ban_duration, ban_reason):
        ban_status = dict(
            is_banned=True,
            ban_duration=ban_duration,
            banned_on=datetime.date.today().isoformat(),
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_duration=0,
            banned_on=datetime.date.max.isoformat(),
            ban_reason=''
        )
        user = await self.col.find_one({'id': int(id)})
        return user.get('ban_status', default)

    async def get_all_banned_users(self):
        banned_users = self.col.find({'ban_status.is_banned': True})
        return banned_users


db = Database(Config.DB_URL, Config.DB_NAME)