import pymongo
from bson.objectid import ObjectId
from pymodm import MongoModel, fields

from server.service.error.type.bad_request_error import BadRequestError
from server.service.error.type.missing_element_error import MissingElementError


# Now let's define some Models.
class Command(MongoModel):
    name = fields.CharField(required=True)
    channel_id = fields.CharField(required=True)
    label = fields.CharField(blank=True)
    description = fields.CharField(blank=True)
    pick_list = fields.ListField()
    only_users_in_pick_list = fields.BooleanField()
    self_exclude = fields.BooleanField()
    only_active_users = fields.BooleanField()
    weight_list = fields.ListField()
    strategy = fields.CharField()
    created_by_user_id = fields.CharField(required=True)
    updated_by_user_id = fields.CharField(required=True)

    @staticmethod
    def find_one_by_name_and_chanel(name: str, channel_id: int, catch=True):
        if not catch:
            return Command.objects.get({"name": name, "channel_id": channel_id})

        try:
            return Command.objects.get({"name": name, "channel_id": channel_id})
        except Command.DoesNotExist:
            raise MissingElementError(f"Command {name} does not exist.")

    @staticmethod
    def find_all_in_chanel(channel_id: int):
        return list(
            Command.objects.raw({"channel_id": channel_id}).aggregate(
                {"$sort": {"name": pymongo.ASCENDING}}
            )
        )

    @staticmethod
    def find_by_id(id: int):
        return Command.objects.get({"_id": ObjectId(id)})

    @staticmethod
    def create(
        *,
        name,
        channel_id,
        label,
        description,
        pick_list,
        only_users_in_pick_list,
        self_exclude,
        only_active_users,
        weight_list,
        strategy,
        created_by_user_id,
    ):
        try:
            Command.find_one_by_name_and_chanel(name, channel_id, catch=False)
            raise BadRequestError(f"Command {name} already exists.")
        except Command.DoesNotExist:
            Command(
                name,
                channel_id,
                label,
                description,
                pick_list,
                only_users_in_pick_list,
                self_exclude,
                only_active_users,
                weight_list,
                strategy,
                created_by_user_id,
                updated_by_user_id=created_by_user_id,
            ).save()

    @staticmethod
    def update(name, channel_id, updated_by_user_id, new_values):
        new_values["updated_by_user_id"] = updated_by_user_id
        return Command.objects.raw({"name": name, "channel_id": channel_id}).update(
            {"$set": new_values}
        )

    @staticmethod
    def delete_command(command):
        return command.delete()
