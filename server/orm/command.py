from pymodm import MongoModel, fields

from server.service.command.args import ArgError
from server.service.error.back_error import BackError


# Now let's define some Models.
class Command(MongoModel):
    name = fields.CharField(required=True)
    channel_id = fields.CharField(required=True)
    label = fields.CharField()
    pick_list = fields.ListField()
    self_exclude = fields.BooleanField()
    created_by_user_id = fields.CharField(required=True)
    updated_by_user_id = fields.CharField(required=True)

    @staticmethod
    def find_one_by_name_and_chanel(name, channel_id, catch=True):
        if not catch:
            return Command.objects.get({"name": name, "channel_id": channel_id})

        try:
            return Command.objects.get({"name": name, "channel_id": channel_id})
        except Command.DoesNotExist:
            raise ArgError(None, f"Command {name} does not exist.")

    @staticmethod
    def find_all_in_chanel(channel_id):
        return list(Command.objects.raw({"channel_id": channel_id}))

    @staticmethod
    def create(name, channel_id, label, pick_list, self_exclude, created_by_user_id):
        try:
            Command.find_one_by_name_and_chanel(name, channel_id, catch=False)
            raise BackError("Command already exists.", 400)
        except Command.DoesNotExist:
            Command(
                name,
                channel_id,
                label,
                pick_list,
                self_exclude,
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
