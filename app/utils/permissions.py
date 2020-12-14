import discord

def is_owner(ctx):
    """ Checks if the author is one of the owners """
    return ctx.author.id in owners

def hasRole(ctx):
    """ Checks if the author is one of the owners """
    print(ctx.author)
    return False
    """ if role in member.roles == 'o__o':
        return True
    else:
        return False """