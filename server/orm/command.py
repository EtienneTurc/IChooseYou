from pymodm import MongoModel, fields


# Now let's define some Models.
class Command(MongoModel):
    # Use 'email' as the '_id' field in MongoDB.
    name = fields.CharField(primary_key=True, required=True)
    label = fields.CharField()
    pick_list = fields.ListField()
    self_exclude = fields.BooleanField()

    @staticmethod
    def find_one_by_name(name):
        return Command.objects.get({"_id": name})

    @staticmethod
    def create(name, label, pick_list, self_exclude):
        # alreadyCreated = self.find_one_by_name(name)
        # if alreadyCreated:
        Command(name, label, pick_list, self_exclude).save()
