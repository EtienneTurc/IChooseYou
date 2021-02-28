import ast


def assert_label_is_correct(label):
    positional_args, named_args = get_args_in_label(label)
    print(positional_args)
    print(named_args)

    count = 0
    for arg in positional_args:
        value = int(arg[1:])
        count += value
        if value < 1:
            # TODO throw error instead
            return False

    n = len(positional_args)
    if count == n * (n + 1) / 2:
        return True
    return False


def get_args_in_label(label):
    label_list = label.split(" ")
    positional_args = []
    named_args = []
    for word in label_list:
        if word[0] == "$" and word[1:].isdigit():
            positional_args.append(word)
        elif word[0] == "$":
            named_args.append(word)

    return positional_args, named_args


def get_as_string(options, name):
    return (" ").join(options[name])


def get_as_bool(options, name):
    return bool(options[name])


def get_as_list(options, name):
    return ast.literal_eval(get_as_string(options, name))
