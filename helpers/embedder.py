import disnake
import datetime

import configs.private_config as private_config
import configs.public_config as public_config

import helpers.helpers as helpers


class Embed:
    def songs(self, client, data, text):
        info = data
        if "entries" in info:
            info = info["entries"][0]
        embed = disnake.Embed(
            title=info['title'],
            url=info['webpage_url'],
            description=text,
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["songs"]),
            timestamp=datetime.datetime.now())
        duration = helpers.get_duration(info)

        embed.set_author(name=info['uploader'])
        embed.set_thumbnail(
            url=f"https://img.youtube.com/vi/{info['id']}/0.jpg")
        embed.add_field(name="*Duration*",
                        value=duration, inline=True)
        embed.add_field(name="*Requested by*",
                        value=client.display_name, inline=True)
        embed.add_field(name="*Channel*",
                        value=client.voice.channel.name, inline=True)
        return embed

    def radio(self, data):
        embed = disnake.Embed(
            title=data['name'],
            description="Playing from ANISON.FM",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["songs"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=data['source'])
        embed.add_field(name="*Duration*",
                        value=helpers.get_duration(data),
                        inline=True)
        embed.add_field(name="*Channel*",
                        value=data['channel'].name, inline=True)
        return embed

# --------------------- Entry Actions --------------------------------

    def entry_channel_create(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} created channel {entry.user.guild.get_channel(entry.target.id).mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        for attr in dir(entry.after):
            if attr in public_config.channel_create:
                embed.add_field(name=f"**{helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.after, attr)}", inline=False)
        if hasattr(entry.after, 'overwrites'):
            overwrites = []
            for role in entry.after.overwrites:
                if f"{role[1].pair()[0]}" == "<Permissions value=1024>":
                    overwrites += [f"User : {role[0].mention}"] if f"{type(role[0])}" == "<class 'disnake.member.Member'>" else [
                        f"Role : {role[0].mention}"]
            overwrites = '\n'.join(overwrites)
            embed.add_field(name=f"**Viewing Permissions:**",
                            value=overwrites, inline=False)
        if hasattr(entry.after, 'available_tags'):
            tags = []
            for tag in entry.after.available_tags:
                tags += [tag.name]
            tags = '\n'.join(tags)
            embed.add_field(name=f"**Available tags:**",
                            value=tags, inline=False)
        return embed

    def entry_channel_update(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} updated channel {entry.user.guild.get_channel(entry.target.id).mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        for attr in dir(entry.after):
            if attr in public_config.channel_update:
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name=f"**Old {helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.before, attr)}", inline=True)
                embed.add_field(name=f"**New {helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.after, attr)}", inline=True)

        if hasattr(entry.after, 'nsfw'):
            if entry.before.nsfw:
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name="**Old NSFW settings:**",
                                value="NSFW", inline=True)
                embed.add_field(name="**New NSFW settings:**",
                                value=":sob: Not NSFW", inline=True)
            else:
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name="**Old NSFW settings:**",
                                value="Not NSFW", inline=True)
                embed.add_field(name="**New NSFW settings:**",
                                value=":smiling_imp: NSFW", inline=True)

        if hasattr(entry.after, 'available_tags'):
            tags = []
            for tag in entry.before.available_tags:
                if tag not in entry.after.available_tags:
                    tags += [f"{public_config.emojis['false']} {tag.name}"]
            for tag in entry.after.available_tags:
                if tag not in entry.before.available_tags:
                    tags += [f"{public_config.emojis['true']} {tag.name}"]
            tags = '\n'.join(tags)
            embed.add_field(name="**Tag Updates**", value=tags, inline=False)

        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_channel_delete(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} deleted channel `{entry.before.name}`**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_thread_create(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has created thread {entry.target.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        for attr in dir(entry.after):
            if attr in public_config.threads:
                embed.add_field(name=f"**{helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.after, attr)}", inline=False)
        if hasattr(entry.after, 'applied_tags'):
            tags = []
            for tag in entry.after.applied_tags:
                tags += [tag.name]
            tags = '\n'.join(tags)
            embed.add_field(name=f"**Applied tags:**",
                            value=tags, inline=False)
        return embed

    def entry_thread_update(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has updated thread {entry.target.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        for attr in dir(entry.after):
            if attr in public_config.threads:
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name=f"**Old {helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.before, attr)}", inline=True)
                embed.add_field(name=f"**New {helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.after, attr)}", inline=True)
        if hasattr(entry.after, 'applied_tags'):
            tags = []
            for tag in entry.before.applied_tags:
                if tag not in entry.after.applied_tags:
                    tags += [f"{public_config.emojis['false']} {tag.name}"]
            for tag in entry.after.applied_tags:
                if tag not in entry.before.applied_tags:
                    tags += [f"{public_config.emojis['true']} {tag.name}"]
            tags = '\n'.join(tags)
            embed.add_field(name="**Tag Updates**", value=tags, inline=False)
        return embed

    def entry_thread_delete(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} deleted thread `{entry.before.name}`**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_kick(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} kicked member {entry.target.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.add_field(name="**REASON:**", value=f'{entry.reason}')
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_ban(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} banned member {entry.target.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.add_field(name="**REASON:**", value=f'{entry.reason}')
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_unban(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} unbanned user {entry.target.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_member_move(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} moved a user to {entry.user.guild.get_channel(entry.extra.channel.id).mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_member_update(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} updated user {entry.target.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        if hasattr(entry.before, "nick"):
            if entry.before.nick is not None:
                embed.add_field(name="**Old Nickname:**",
                                value=f'`{entry.before.nick}`')
            if entry.after.nick is not None:
                embed.add_field(name="**New Nickname:**",
                                value=f'`{entry.after.nick}`')
        if hasattr(entry.after, "timeout"):
            if entry.after.timeout is not None:
                embed.add_field(name="**Timeout expiration date:**",
                                value=entry.after.timeout.strftime("%d/%m %H:%M:%S"))
            else:
                embed.add_field(name="**Timeout:**",
                                value="Timeout has been removed")
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_member_role_update(self, entry):
        x = entry.after.roles
        z = entry.before.roles
        embed = disnake.Embed(
            description=f"**{entry.user.mention} updated user {entry.target.mention}'s roles**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        for y in range(len(x)):
            embed.add_field(name=f"Role added:", value=x[y].name)
        for y in range(len(z)):
            embed.add_field(name=f"Role removed:", value=z[y].name)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_member_disconnect(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} disconnected {entry.extra.count} user(s) from a voice channel**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_role_create(self, entry):
        embed = disnake.Embed(
            description=f'**A new role has been added to the Guild by {entry.user.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        if hasattr(entry.after, "name"):
            embed.add_field(name="**Role name:**", value=entry.after.name)
        return embed

    def entry_role_update(self, entry):
        embed = disnake.Embed(
            description=f'**The role {entry.target.mention} has been updated by {entry.user.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        if hasattr(entry.after, "name"):
            embed.add_field(name="**New Role name:**", value=entry.after.name)
        if hasattr(entry.after, "icon"):
            embed.set_thumbnail(url=entry.after.icon.url)
        if hasattr(entry.after, "colour"):
            embed.add_field(
                name="**Role Color:**", value=f'Red : {entry.after.colour.r}\nGreen : {entry.after.colour.g}\nBlue : {entry.after.colour.b}')
        # PERMISSIONS
        if hasattr(entry.after, "permissions"):
            perms = []
            for attr in dir(entry.after.permissions):
                if attr in public_config.permissions_list:
                    if (getattr(entry.before.permissions, attr) != getattr(entry.after.permissions, attr)):
                        perms += [f"{public_config.emojis['true']} {helpers.parse_key(attr)}"] if getattr(
                            entry.before.permissions, attr) == False else [f"{public_config.emojis['false']} {helpers.parse_key(attr)}"]
            perms = '\n'.join(perms)
            embed.add_field(name="**CHANGED PERMISSIONS:**",
                            value=perms, inline=False)
        return embed

    def entry_role_delete(self, entry):
        embed = disnake.Embed(
            description=f'**A role has been deleted by {entry.user.mention} from the guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        for attr in dir(entry.before):
            if attr in public_config.role_delete:
                embed.add_field(name=f"**{helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.before, attr)}", inline=False)
        return embed

    def entry_guild_update(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has updated the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        for attr in dir(entry.before):
            if attr in public_config.guild_update:
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name=f"**Old {helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.before, attr)}", inline=True)
                embed.add_field(name=f"**New {helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.after, attr)}", inline=True)
        return embed

    def entry_member_prune(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has pruned members from the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        embed.add_field(name="**Members Removed:**",
                        value=entry.extra.members_removed, inline=False)
        embed.add_field(name="**Prune size:**",
                        value=entry.extra.delete_members_days, inline=False)
        return embed

    def entry_invite_create(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has created an invite to the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        if hasattr(entry.after, 'channel'):
            embed.add_field(name="**Channel:**",
                            value=entry.after.channel.mention, inline=False)
        for attr in dir(entry.after):
            if attr in public_config.invites:
                embed.add_field(name=f"**{helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.after, attr)}", inline=False)
        return embed

    def entry_invite_update(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has updated an invite to the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_invite_delete(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has deleted an invite to the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        if hasattr(entry.before, 'channel'):
            embed.add_field(name="**Channel:**",
                            value=entry.after.channel.mention, inline=False)
        for attr in dir(entry.before):
            if attr in public_config.invites:
                embed.add_field(name=f"**{helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.before, attr)}", inline=False)
        return embed

    def entry_emoji_create(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has added an emoji to the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        embed.add_field(name="**Emoji:**",
                        value=entry.after.name, inline=False)
        return embed

    def entry_emoji_update(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has updated an emoji in the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        embed.add_field(name="**Old Emoji Name:**",
                        value=entry.before.name, inline=False)
        embed.add_field(name="**New Emoji Name:**",
                        value=entry.after.name, inline=False)

        return embed

    def entry_emoji_delete(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has removed an emoji from the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        embed.add_field(name="**Emoji:**",
                        value=entry.before.name, inline=False)
        return embed

    def entry_sticker_create(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has added a sticker to the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        for attr in dir(entry.before):
            if attr in public_config.sticker_ent:
                embed.add_field(name=f"**{helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.before, attr)}", inline=False)
        return embed

    def entry_sticker_update(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has updated a sticker in the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        for attr in dir(entry.before):
            if attr in public_config.sticker_ent:
                embed.add_field(name=f"**{helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.before, attr)}", inline=False)
        return embed

    def entry_sticker_create(self, entry):
        embed = disnake.Embed(
            description=f'**{entry.user.mention} has deleted a sticker from the Guild**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        for attr in dir(entry.before):
            if attr in public_config.sticker_ent:
                embed.add_field(name=f"**{helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.before, attr)}", inline=False)
        return embed

    def entry_message_delete(self, entry):
        embed = disnake.Embed(
            description=f"**{(f'<@{entry.target.id}>',entry.target.mention)[hasattr(entry.target, 'mention')]}'s messages have been deleted by moderator {entry.user.mention}**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        embed.add_field(name="**Channel from which the messages were deleted**",
                        value=entry.extra.channel.mention, inline=False)
        embed.add_field(name="**Amount of deleted messages**",
                        value=entry.extra.count, inline=False)
        return embed

    def entry_message_bulk_delete(self, entry):
        embed = disnake.Embed(
            description=f"**{entry.user.mention} has deleted {entry.extra['count']} message(s) from {entry.target.mention}**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["message"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_message_pin(self, entry):
        embed = disnake.Embed(
            description=f"**{entry.user.mention} has pinned {entry.target.mention}'s message in {entry.extra.channel.mention}**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["message"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_message_unpin(self, entry):
        embed = disnake.Embed(
            description=f"**{entry.user.mention} has unpinned {entry.target.mention}'s message from {entry.extra.channel.mention}**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["message"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed

    def entry_guild_scheduled_event_create(self, entry):
        embed = disnake.Embed(
            description=f"**{entry.user.mention} has created a scheduled guild event**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        if hasattr(entry.after, 'channel'):
            embed.add_field(name="**Channel**",
                            value=f"{entry.after.channel.mention}")
        for attr in dir(entry.after):
            if attr in public_config.guild_scheduled_event:
                embed.add_field(name=f"**{helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.after, attr)}", inline=False)
        if hasattr(entry.after, 'image'):
            embed.set_thumbnail(url=entry.after.image.url)
        return embed

    def entry_guild_scheduled_event_update(self, entry):
        embed = disnake.Embed(
            description=f"**{entry.user.mention} has updated a scheduled guild event**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        if hasattr(entry.after, 'channel'):
            embed.add_field(name="", value="", inline=False)
            embed.add_field(name="**Old Channel**",
                            value=f"{entry.before.channel.mention}", inline=True)
            embed.add_field(name="**New Channel**",
                            value=f"{entry.after.channel.mention}", inline=True)
        for attr in dir(entry.before):
            if attr in public_config.guild_scheduled_event:
                embed.add_field(name="", value="", inline=False)
                embed.add_field(name=f"**Old {helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.before, attr)}", inline=True)
                embed.add_field(name=f"**New {helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.after, attr)}", inline=True)
        if hasattr(entry.after, 'image'):
            embed.set_thumbnail(url=entry.after.image.url)
        return embed

    def entry_guild_scheduled_event_delete(self, entry):
        embed = disnake.Embed(
            description=f"**{entry.user.mention} has deleted a scheduled guild event**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        if hasattr(entry.before, 'channel'):
            embed.add_field(name="**Channel**",
                            value=f"{entry.before.channel.mention}")
        for attr in dir(entry.before):
            if attr in public_config.guild_scheduled_event:
                embed.add_field(name=f"**{helpers.parse_key(attr)}**",
                                value=f"{getattr(entry.before, attr)}", inline=False)
        if hasattr(entry.before, 'image'):
            embed.set_thumbnail(url=entry.after.before.url)
        return embed

    def entry_bot_add(self, entry):
        embed = disnake.Embed(
            description=f"**{entry.user.mention} has added a BOT - {entry.target.mention} - to the GUILD**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=entry.user.name,
                         icon_url=entry.user.display_avatar.url)
        embed.set_footer(text=f'{entry.user.guild.name}')
        return embed


# --------------------- CHANNEL SWITCHING --------------------------------

    def switched(self, member, before, after):
        embed = disnake.Embed(
            description=f'**{member.mention} switched from {before.channel.mention} to {after.channel.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["voice_update"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        return embed

    def connected(self, member, after):
        embed = disnake.Embed(
            description=f"**{member.mention} joined voice channel {after.channel.mention}**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["voice_update"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        return embed

    def disconnected(self, member, before):
        embed = disnake.Embed(
            description=f'**{member.mention} left voice channel {before.channel.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["voice_update"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        return embed

    def afk(self, member, after):
        embed = disnake.Embed(
            description=f'**{member.mention} has gone AFK in {after.channel.mention}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["voice_update"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        return embed

# --------------------- USER ACTIONS --------------------------------

    def welcome_message(self, member, user):
        embed = disnake.Embed(
            description=f'**{user.mention}, welcome to {helpers.get_guild_name(member.guild)}!**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["welcome_message"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        embed.add_field(name="**⏲ Age of account:**", value=f'`{member.created_at.strftime("%d/%m/%Y %H:%M")}`\n**{helpers.get_welcome_time(member.created_at)}**',
                        inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        return embed

    def profile_upd(self, before, after):
        embed = disnake.Embed(
            description=f'**{after.mention} has updated their profile**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=after.name, icon_url=after.display_avatar.url)
        embed.set_footer(text=f'{after.guild.name}')
        embed.set_thumbnail(url=after.display_avatar.url)
        for attr in dir(before):
            if attr in public_config.member_update and getattr(before, attr) != getattr(after, attr):
                embed.add_field(name="", value="", inline=False)
                embed.add_field(
                    name=f"**Old {helpers.parse_key(attr)}**", value=f"{getattr(before, attr)}", inline=True)
                embed.add_field(
                    name=f"**New {helpers.parse_key(attr)}**", value=f"{getattr(after, attr)}", inline=True)
        return embed

    def member_remove(self, payload):
        embed = disnake.Embed(
            description=f'**:no_entry_sign: {payload.user.mention} has left the server**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["ban_leave"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=payload.user.name,
                         icon_url=payload.user.display_avatar.url)
        embed.set_footer(text=f'{payload.user.guild.name}')
        embed.set_thumbnail(url=payload.user.display_avatar.url)
        return embed

    def member_join(self, member):
        embed = disnake.Embed(
            description=f'**:white_check_mark: {member.mention} has joined the server**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["welcome_message"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        embed.add_field(name="**⏲ Age of account:**", value=f'`{member.created_at.strftime("%d/%m/%Y %H:%M")}`\n**{helpers.get_welcome_time(member.created_at)}**',
                        inline=True)
        embed.set_thumbnail(url=member.display_avatar.url)
        return embed

    def ban(self, guild, user):
        embed = disnake.Embed(
            description=f'**{public_config.emojis["cat_ban"]} {user.mention} has been banned from {guild.name}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["ban_leave"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        embed.set_footer(text=f'{guild.name}')
        embed.set_thumbnail(url=user.display_avatar.url)
        return embed

    def unban(self, guild, user):
        embed = disnake.Embed(
            description=f'**:ballot_box_with_check: {user.mention} has been unbanned from {guild.name}**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["other_action"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)
        embed.set_footer(text=f'{guild.name}')
        embed.set_thumbnail(url=user.display_avatar.url)
        return embed

    def get_status(self, member):
        embed = disnake.Embed(
            description=f"**{member.mention}'s status: {member.status}**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        if member.activity is not None:
            for acts in member.activities:
                # embed.add_field(name = acts.name, value = acts.type)
                if f"{type(acts)}" == "<class 'disnake.activity.Spotify'>":
                    embed.add_field(name="**Listening to spotify:**",
                                    value=f'{acts.artists[0]} - "{acts.title}"\n Track url : {acts.track_url}', inline=False)
                    embed.set_thumbnail(url=f"{acts.album_cover_url}")
                elif f"{type(acts)}" != "<class 'NoneType'>":
                    x = f'{acts.type}'[13:]
                    embed.add_field(
                        name=f"**{x}**", value=f"{acts.name}", inline=False)
        return embed

    def activity_update(self, member, old_user_status, new_user_status):
        embed = disnake.Embed(
            description=f"**{member.mention}'s has updated their status/activities**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["member_action"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        if old_user_status.status != new_user_status.status:
            embed.add_field(name="", value="", inline=False)
            embed.add_field(
                name="**Old Status**", value=f'```{helpers.parse_key(old_user_status.status)}```', inline=True)
            embed.add_field(name="**Current Status**",
                            value=f'```{helpers.parse_key(new_user_status.status)}```', inline=True)
        if old_user_status.activities != new_user_status.activities and old_user_status.activities:
            fin = []
            for acts in old_user_status.activities:
                if acts not in new_user_status.activities:
                    fin += [f'{acts.actname}']
            fin = '\n'.join(fin)
            embed.add_field(name="**Finished Activities :**",
                            value=f"```{fin}```", inline=False)
        if member.activity is not None:
            embed.add_field(name="**Current Activities : **",
                            value="", inline=False)
            for acts in member.activities:
                # embed.add_field(name = acts.name, value = acts.type)
                if f"{type(acts)}" == "<class 'disnake.activity.Spotify'>":
                    embed.add_field(name="**Listening to spotify:**",
                                    value=f'```{acts.artists[0]} - "{acts.title}"```Track url : {acts.track_url}', inline=False)
                    embed.set_thumbnail(url=f"{acts.album_cover_url}")
                elif f"{type(acts)}" != "<class 'NoneType'>":
                    x = f'{acts.type}'[13:]
                    embed.add_field(
                        name=f"**{x}**", value=f"```{acts.name}```", inline=False)
        return embed

# --------------------- MESSAGES --------------------------------

    def message_edit(self, before, after):
        embed = disnake.Embed(
            description=f'**:pencil2:{before.author.mention} has edited a message in {before.channel.mention}. [Jump to message]({before.jump_url})**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["message"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=before.author.name,
                         icon_url=before.author.display_avatar.url)
        embed.set_footer(text=f'{before.guild.name}')
        embed.add_field(name="** Before: **",
                        value=f'```{before.content}```', inline=False)
        embed.add_field(name="** After: **",
                        value=f'```{after.content}```', inline=False)
        return embed

    def message_pin(self, before, after):
        embed = disnake.Embed(
            description=f'**:pushpin:A Message has been pinned in {before.channel.mention}. [Jump to message]({before.jump_url})**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["message"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=before.guild.name,
                         icon_url=before.guild.icon.url)
        embed.set_footer(text=f'{before.guild.name}')
        embed.add_field(name="** Message Author: **",
                        value=f'{before.author.mention}', inline=False)
        embed.add_field(name="** Message Content: **",
                        value=f'```{after.content}```\n', inline=False)
        return embed

    def message_unpin(self, before, after):
        embed = disnake.Embed(
            description=f'**:pushpin:A Message has been unpinned in {before.channel.mention}. [Jump to message]({before.jump_url})**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["message"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=before.guild.name,
                         icon_url=before.guild.icon.url)
        embed.set_footer(text=f'{before.guild.name}')
        embed.add_field(name="** Message Author: **",
                        value=f'{before.author.mention}\n', inline=False)
        embed.add_field(name="** Message Content: **",
                        value=f'```{after.content}```\n', inline=False)
        return embed

    def message_delete(self, message):
        embed = disnake.Embed(
            description=f'**:wastebasket: A Message sent by {message.author.mention} has been deleted in {message.channel.mention}.**',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["message"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=message.author,
                         icon_url=message.author.display_avatar.url)
        embed.set_footer(text=f'{message.channel.guild.name}')
        embed.add_field(name="** Message Content: **",
                        value=f'```{message.content}```\n', inline=False)
        return embed

# --------------------- VOICE STATES --------------------------------

    def mute(self, member, after):
        embed = disnake.Embed(
            description=f"**{member.mention}'s voice state has been updated**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["voice_update"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        if after.mute:
            embed.add_field(name=f":microphone2:** Server Mute**", value="Yes")
        else:
            embed.add_field(name=f":microphone2:** Server Mute**", value="No")
        return embed

    def deaf(self, member, after):
        embed = disnake.Embed(
            description=f"**{member.mention}'s voice state has been updated**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["voice_update"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        if after.deaf:
            embed.add_field(name=f":mute:** Server Deafen**", value="Yes")
        else:
            embed.add_field(name=f":mute:** Server Deafen**", value="No")
        return embed

    def self_mute(self, member, after):
        embed = disnake.Embed(
            description=f"**{member.mention} updated their voice state**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["voice_update"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        if after.self_mute:
            embed.add_field(name=f":microphone2:** Muted**", value="Yes")
        else:
            embed.add_field(name=f":microphone2:** Muted**", value="No")
        return embed

    def self_deaf(self, member, after):
        embed = disnake.Embed(
            description=f"**{member.mention} updated their voice state**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["voice_update"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        if after.self_deaf:
            embed.add_field(name=f":mute:** Deafened**", value="Yes")
        else:
            embed.add_field(name=f":mute:** Deafened**", value="No")
        return embed

    def self_stream(self, member, after):
        embed = disnake.Embed(
            description=f"**{member.mention} updated their stream status**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["voice_update"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        if after.self_stream:
            embed.add_field(name=f":tv:** Stream enabled**", value="Yes")
        else:
            embed.add_field(name=f":tv:** Stream enabled**", value="No")
        return embed

    def self_video(self, member, after):
        embed = disnake.Embed(
            description=f"**{member.mention} updated their video status**",
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["voice_update"]),
            timestamp=datetime.datetime.now())
        embed.set_author(name=member.name, icon_url=member.display_avatar.url)
        embed.set_footer(text=f'{member.guild.name}')
        if after.self_video:
            embed.add_field(
                name=f":video_camera:** Video enabled**", value="Yes")
        else:
            embed.add_field(
                name=f":video_camera:** Video enabled**", value="No")
        return embed

    def role_notification(self, guild, roles_list):
        embed = disnake.Embed(
            description=f'**You got a new role!** {public_config.emojis["yay"]}' if len(roles_list) == 1 else f'**You got new roles!** {public_config.emojis["yay"]}',
            color=disnake.Colour.from_rgb(
                *public_config.embed_colors["welcome_message"]),
            timestamp=datetime.datetime.now()
        )
        embed.set_author(name=guild.name,
                         icon_url=guild.icon.url)

        roles = []
        for role in roles_list:
            roles.append(role.name)

        roles = '\n* '.join(roles)
        embed.add_field(name="", value=f"* {roles}", inline=False)
        return embed
