import discord
import os


def hasRole(ctx, role):
    for r in ctx.message.author.roles:
        if role == r.name:
            return True
    return False


def hasManagerRole(ctx):
    return hasRole(ctx, os.environ['MANAGER_ROLE'])
