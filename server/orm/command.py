from pymodm import MongoModel, fields


# Now let's define some Models.
class Command(MongoModel):
    name = fields.CharField(required=True)
    channel_id = fields.CharField(required=True)
    label = fields.CharField()
    pick_list = fields.ListField()
    self_exclude = fields.BooleanField()

    @staticmethod
    def find_one_by_name_and_chanel(name, channel_id):
        return Command.objects.get({"name": name, "channel_id": channel_id})

    @staticmethod
    def find_all_in_chanel(channel_id):
        return list(Command.objects.raw({"channel_id": channel_id}))

    @staticmethod
    def create(name, channel_id, label, pick_list, self_exclude):
        try:
            Command.find_one_by_name_and_chanel(name, channel_id)
            raise Exception("Command already exists.")
        except Command.DoesNotExist:
            Command(name, channel_id, label, pick_list, self_exclude).save()

    @staticmethod
    def update(name, channel_id, new_values):
        return Command.objects.raw({"name": name, "channel_id": channel_id}).update(
            {"$set": new_values}
        )

    @staticmethod
    def delete_command(command):
        return command.delete()
