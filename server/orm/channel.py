from pymodm import MongoModel, fields


# Now let's define some Models.
class Channel(MongoModel):
    channel_id = fields.CharField(required=True)
    found_xmas_easter_egg = fields.BooleanField(default=False)

    @staticmethod
    def find_one_by_channel_id(channel_id: int):
        try:
            return Channel.objects.get({"channel_id": channel_id})
        except:  # noqa E722
            return Channel(channel_id=channel_id, found_xmas_easter_egg=False)

    @staticmethod
    def upsert(*, channel_id, found_xmas_easter_egg=False):
        return Channel.objects.raw({"channel_id": channel_id}).update(
            {"$set": {"found_xmas_easter_egg": found_xmas_easter_egg}}, upsert=True
        )
