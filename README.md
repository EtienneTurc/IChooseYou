# I choose you

<img src="https://github.com/EtienneTurc/IChooseYou/blob/master/assets/I_choose_you_banner_centered.png" alt="I choose you banner"/>

Making the right decision is hard, even more when relationships are involved. *I choose you* takes that burden off by transforming the power of randomness into fairness. It enables users to randomly pick any user directly in Slack. It can be used to pick a colleague to select the lunch place, a reviewer for your pr, an animator for your scrum rituals and much more.

The core features of *I choose you* are:
- Free to use without limits
- Customizable use
- Easy to use
- Can pick multiple users at once
- Multiple random strategies
- Integration with slack workflows

So hop on and [get started](#getting-started) !

## Contents

- [I choose you](#i-choose-you)
  - [Contents](#contents)
  - [Installing *I choose you* in Slack](#installing-i-choose-you-in-slack)
  - [Getting Started](#getting-started)
    - [Quick start to create a command](#quick-start-to-create-a-command)
    - [Quick start to run a command](#quick-start-to-run-a-command)
  - [Advanced](#advanced)
    - [Creating a command](#creating-a-command)
    - [Updating a command](#updating-a-command)
    - [Using a random strategy](#using-a-random-strategy)
    - [Running a command](#running-a-command)
    - [Resubmitting a command](#resubmitting-a-command)
    - [Deleting a pick message](#deleting-a-pick-message)
    - [Deleting a command](#deleting-a-command)
    - [Setting up workflows](#setting-up-workflows)
    - [Running an instant command](#running-an-instant-command)
  - [Contributing](#contributing)
    - [Opening an issue](#opening-an-issue)
    - [Local installation](#local-installation)
    - [Opening a pull request](#opening-a-pull-request)

## Installing *I choose you* in Slack

To install in slack, go to [this link](https://slack.com/oauth/v2/authorize?client_id=1796066292534.1788071729511&scope=channels:read,chat:write,commands,groups:read,incoming-webhook,users:read,workflow.steps:execute,chat:write.public&user_scope=) then choose the workspace and the channel you want *I choose you* to be installed on.

**Note**: *I choose you* can be used in all the public channels, so it does not really matter which channel you pick. However, to be at its fullest potential for private ones, it requires to add it to channel (```/invite @I choose you```).

You should now be prompted to grant *I choose you* permission. It requests permissions to:
- Use slash command to run *I choose you*
- Publish messages in channels to communicate
- Access public data concerning channels to propose channels in which to run *I choose you*
- Listing people in channel so it can only pick active users if requested

After accepting the permission, *I choose you* should now be installed in your Slack ! Well done ! You can type ```/ichu``` in any channel to verify that it is working.

You can now go to the [getting started](#getting-started) section to learn how to use it.

## Getting Started

This section will walk you through creating and using your first ever ```ichu``` command. If you are looking to a more in depth guide, go to the [advanced section](#advanced).

### Quick start to create a command

Typing ```/ichu``` in any channel will open a modal presenting two options:
- Creating a new command
- Running an instant command

<img src="https://github.com/EtienneTurc/IChooseYou/blob/master/assets/documentation/create_command.gif" alt="Create command gif"/>

In this guide, we will focus on creating a command. If you wish to learn more about running an instant command, go to the [running an instant command section](#running-an-instant-command).

But first, what the hell is a command ? A command is simply a configuration to select a random user for a given task. Bear in mind that a command is specific to a channel.

So now let's create our first command by clicking on the ```create``` button. You should now see a form with those fields:
- **Channel**: Channel in which the command exists. Note that that command can only be used in that channel. Of course, you can later on create the same command in an other channel. (Global commands is a feature that is still in development).
- **Name**: Name of the command. It is used to easily run the command.
- **Description of the command**: Extra information describing the purpose of the command.
- **Label**: Extra text to add when running the command. The message that will be issued after running a command will always be:
    ```
    Hey ! <Name of the user that ran the command> choose <User the has been picked> <extra text of the command filled in the label field>
    ```
- **Pick list**: List of users to pick from. Unfortunately, slack does not propose a select all button... (A custom solution is on its way).
- **Other fields**: We will ignore them for now. If you wish to learn more about those you can go to the [creating a command section](#creating-a-command).

After filling those fields, you can click on the ```submit``` button to create you first ever command ! Well done !

**Note**: If you only wish to run the command once (and never again), check out the [running an instant command section](#running-an-instant-command).

### Quick start to run a command

<img src="https://github.com/EtienneTurc/IChooseYou/blob/master/assets/documentation/run_command.gif" alt="Run command gif"/>

We can now go the channel that we defined our command in (i.e in this example ```documentation```) and again type ```/ichu```. You should now see the same modal as the last time at the exception of a new row corresponding to your brand new command. By clicking on the launch button, it should now open an other form with fields that we will ignore for now (if you wish to learn more about those you can go to the [running a commmand section](#running-a-command)).

By clicking on the submit button, *I choose you* should should have sent a pick message on the channel. In our case, the message was:
```
Hey ! Etienne choose John Doe to do a code review
```

**Note**: It can be pretty tedious to go through these steps just to run a command. Thankfully, there is a faster way, by simply typing ```/ichu <name of my command>``` (in the channel in which you created your command). In our case, typing ```/ichu code-review``` will lead to the same result as above. If you wish to learn more about it, check out the [running an instant command section](#running-an-instant-command).

TADA ! You now know the fundamentals about *I choose you* ! There is still plenty more to discover. Check it out in the [advanced section](#advanced).

## Advanced

This section will go in depth about all the features of *I choose you*.

### Creating a command

Creating a new command can be done by following two different processes:
- via the modal system by typing ```/ichu``` then clicking on the ```create``` button. (*Recommended*)
- via the command line by typing ```/ichu create <name of the command>```.

Both processes can be used to create any command; the only difference lies in the fact that using a modal is easier but slower (if you know what you are doing with the cli).

To create a new command, those are the fields to fill in:
| Field                | Short (cli) | Long (cli)          | Description                                                                                                                                                                                                                                                                                                                                    |
| -------------------- | ----------- | ------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Channel (*required*) | ∅           | ∅                   | Channel in which the command exists. Note that that command can only be used in that channel. Of course, you can later on create the same command in an other channel. This option does not exists for command line because it uses the channel in which *I choose you* is called. (Global commands is a feature that is still in development) |
| Name (*required*)    | ∅           | ∅                   | Name of the command. It is used to easily run the command.                                                                                                                                                                                                                                                                                     |
| Description          | -d          | --description       | Extra information describing the purpose of the command.                                                                                                                                                                                                                                                                                       |
| Label                | -l          | --label             | Extra text to add when running the command. The message that will be issued after running a command will always be: ```Hey ! <Name of the user that ran the command> choose <User the has been picked> <extra text of the command filled in the label field>                                                                              ```  |
| Pick list            | -p          | --pick-list         | List of users to pick from. Unfortunately, slack does not propose a select all button... (A custom solution is on its way).                                                                                                                                                                                                                    |
| Strategy             | -s          | --strategy          | Strategy to use. Valid values are ```uniform```, ```smooth``` and ```round_robin```. More about each strategy in the [using a random strategy section].(#using-a-random-strategy)                                                                                                                                                              |
| Self exclude         | -s          | --self-exclude      | Whether the user that triggers the command should be excluded of the pick list or not. For instance, if you are looking for someone to review what you have done, it is pretty convenient not to pick yourself. By default, the user that triggers the command is included in the pick.                                                        |
| Only active users    | -o          | --only-active-users | Whether to pick only active users, i.e users that appears active on Slack. Warning: It is discouraged to use that feature in order to exclude users that are in holidays, as users that are taking a short break may not be picked.                                                                                                            |

**Example:**

<img src="https://github.com/EtienneTurc/IChooseYou/blob/master/assets/documentation/create_command.gif" alt="Create command gif"/>

The same result can be obtained with:
```
/ichu create -d Select a reviewer for pull requests -l to do a code review -p @user1 @user2 @user3
```

### Updating a command

Updating a new command can be done by following two different processes:
- via the modal system by typing ```/ichu```, then clicking on the dotted button of the command to update, and finally on the ```update``` button. (*Recommended*)
- via the command line directly ```/ichu update <name of the command>```.

Both processes can be used to update any command; the only difference lies in the fact that using a modal is easier but slower (if you know what you are doing with the cli).

The same options as for creating a command are available when updating a command. Check them out in the [creating a command section](#creating-a-command).

The command line interface have two additional optional options to help updating the pick list:
  | Field                 | Short (cli) | Long (cli)              | Description                                          |
  | --------------------- | ----------- | ----------------------- | ---------------------------------------------------- |
  | Add to pick list      | -a          | --add-to-pick-list      | Users to add to the already existing pick list.      |
  | Remove from pick list | -r          | --remove-from-pick-list | Users to remove from the already existing pick list. |

Note: The command line interface does not support changing channel.

**Example:**

<img src="https://github.com/EtienneTurc/IChooseYou/blob/master/assets/documentation/update_command.gif" alt="Update command gif"/>

The same result can be obtained with:
```
/ichu update code-review -r @user
```

### Using a random strategy

*I choose you* support 3 different random strategies.
  | Strategy    | Description                                                                                                                                                                                                                                                                                                                                                      |
  | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | Uniform     | **Pure random**. When using this strategy every user has the same probability. This strategy is really standard although not recommended because a user can be picked multiple times in a row which does not seem fair (even if it is in the long run).                                                                                                          |
  | Smooth      | **Random with memory**. When using this strategy users that have been picked a long time ago are more likely to be pick. This strategy seems fair because it is the perfect balance between uncertainty and variety. This strategy is recommended for most cases.                                                                                                |
  | Round robin | **Deterministic randomness**. When using this strategy, all the users are picked in order but the order is random (i.e the order is not alphabetical and always different). This strategy is often use to ensure that everyone will be picked once before picking a user twice. This strategy is pretty situational because the outcome can be easily predicted. |

<!-- You can check out by yourself each strategy by inspecting the randomness. More on that in the [inspecting strategy randomness section](#inspecting-strategy-randomness). -->

### Running a command

Creating a command can be done by following two different processes:
- via the modal system by typing ```/ichu``` then clicking on the ``launch`` button. (*Recommended*)
- via the command line by typing ```/ichu <name of the command>```.

Both processes can be used to run any command; the only difference lies in the fact that using a modal is easier but slower (if you know what you are doing with the cli).

To run a command, those are the fields to fill in:
| Field                     | Short (cli) | Long (cli)                  | Description                                                                                                                                                                                |
| ------------------------- | ----------- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Additional text           | ∅           | ∅                           | Additional text that will be added at the end of the pick message (after the label). For the command line, all the text that lies after the options will be considered as additional text. |
| Number of users to select | -n          | --number-of-items-to-select | Number of users to select. It must be greater or equal than 1 and lower.                                                                                                                   |

**Example:**

<img src="https://github.com/EtienneTurc/IChooseYou/blob/master/assets/documentation/run_command.gif" alt="Run command gif"/>

The same result can be obtained with:
```
/ichu code-review https://github.com/EtienneTurc/IChooseYou/pull
```

### Resubmitting a command

After running a command, it may happened that the output is not satisfying. In that case, clicking on the ```resubmit``` button (visible only by the user that triggered the command) will resubmit the same command with the same options. The ```update & resubmit``` button opens a modal with the previous options that can be easily changed.

**Note**: If you are using the smooth or the round robin strategy, it will not discard the previous pick from their memory.

### Deleting a pick message

After running a command, it may happened that the output is not satisfying. Hopefully, *I choose you* provides a way to delete the message even if you are not admin of the slack workspace.

Click on the 3 dotted point on the pick message and then click on the shortcut ```Delete message``` provided by *I choose you*. It may not directly appear in the list the first, so you may have to look for it.

**Note**: Only the user that triggered the pick can delete the associated pick message with this method.

**Example:**

<img src="https://github.com/EtienneTurc/IChooseYou/blob/master/assets/documentation/delete_pick_message.gif" alt="Delete pick message gif"/>

### Deleting a command

Deleting a command can be done by following two different processes:
- via the modal system by typing ```/ichu```, then clicking on the dotted button of the command to update, and finally on the ```delete``` button. (*Recommended*)
- via the command line by typing ```/ichu delete <name of the command>```.

Both processes can be used to delete any command; the only difference lies in the fact that using a modal is easier but slower (if you know what you are doing with the cli).


### Setting up workflows

*I choose you* can be integrated with Slack workflows. When building a Slack workflow, you can run an *I choose you* command using the ```Run command``` workflow step provided by *I choose you*.

The form asks for those fields:

| Field           | Description                                                                                                                                                                                                                                                                                                                                                                                    |
| --------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Channel         | Channel in which the command will be run.                                                                                                                                                                                                                                                                                                                                                      |
| Slash command   | Slash command to execute. It is the same as running a command with the cli. For more information on that topic, check out the [running a command section](#running-a-command).                                                                                                                                                                                                                 |
| Send to slack ? | Whether *I choose you* should send the pick message in the selected channel. It can be used to add other steps with the response of the command. If so, the following step will be able to access the variable ```selected item n°i``` which is the i*th* user selected by the command and the variable ```selection message``` which is the message that would have been sent to the channel. |

**Example:**

<img src="https://github.com/EtienneTurc/IChooseYou/blob/master/assets/documentation/workflow.gif" alt="Workflow gif"/>

<!-- ### Inspecting strategy randomness

*I choose you* allows you to get a quick glance at the randomness of a command. To do so, invoke the randomness command followed by the name of the command you wish to inspect:
```
/ichu randomness <name of the command to inspect>
```
 -->

### Running an instant command

An instant command is simply a command that will only be used once and thus it will not be saved and have fewer options to run it as fast as possible. It can be run by following two different processes:
- via the modal system by typing ```/ichu``` then clicking on the ``run`` button on the second row. (*Recommended*)
- via the command line by typing ```/ichu instant```.

Both processes can be used to run any command; the only difference lies in the fact that using a modal is easier but slower (if you know what you are doing with the cli).

To run an instant command, those are the fields to fill in:
| Field                     | Short (cli) | Long (cli)                  | Description                                                                                                                                                                                                                                                |
| ------------------------- | ----------- | --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Channel (*required*)      | ∅           | ∅                           | Channel in which the pick message will be sent. This option does not exists for command line because it uses the channel in which *I choose you* is called.                                                                                                |
| Label                     | -l          | --label                     | Extra text to add when running the command. The message that will be issued after running the command will be: ```Hey ! <Name of the user that ran the command> choose <User the has been picked> <extra text of the command filled in the label field>``` |
| Pick list                 | -p          | --pick-list                 | List of users to pick from. Unfortunately, slack does not propose a select all button... (A custom solution is on its way).                                                                                                                                |
| Number of users to select | -n          | --number-of-items-to-select | Number of users to select. It must be greater or equal than 1 and lower.                                                                                                                                                                                   |
| Only active users         | -o          | --only-active-users         | Whether to pick only active users, i.e users that appears active on Slack. Warning: It is discouraged to use that feature in order to exclude users that are in holidays because users taking a short break may not be picked.                             |

**Example:**

<img src="https://github.com/EtienneTurc/IChooseYou/blob/master/assets/documentation/instant_command.gif" alt="Instant command gif"/>

The same result can be obtained with:
```
/ichu instant -l to review https://github.com/EtienneTurc/IChooseYou/pull -p @user1 @user2 @user3
```

## Contributing

Looking for a way to donate to *I choose you* ? Check out the patreon page [https://www.patreon.com/I_choose_you](https://www.patreon.com/I_choose_you) !

Looking for a way to give feedback or report a bug ? Feel free to open an issue by following the [opening an issue section](#opening-an-issue) !

Looking for a way to get into *I choose you* code ? Check out the [local installation section](#local-installation) and the [opening a pull request section](#opening-a-pull-request) !

### Opening an issue

Coming soon

### Local installation

Coming soon

### Opening a pull request

Coming soon

