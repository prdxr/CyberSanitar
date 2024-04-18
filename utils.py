from discord.ext import commands

from settings import ADMIN_ROLE_ID, MODERATOR_ROLE_ID


def check_admin():
    def predicate(ctx):
        return commands.check_any(commands.is_owner(), commands.has_role(ADMIN_ROLE_ID))
    print(predicate(None))
    return commands.check(predicate)


def check_mod():
    def predicate(ctx):
        return commands.check_any(commands.is_owner(),
                                  commands.has_role(ADMIN_ROLE_ID),
                                  commands.has_role(MODERATOR_ROLE_ID))
    return commands.check(predicate)