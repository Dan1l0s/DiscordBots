import disnake
from disnake.ext import commands
import asyncio
import aiosqlite

import configs.private_config as private_config
import configs.public_config as public_config
import helpers.helpers as helpers
from helpers.embedder import Embed


class AdminBot():
    music_instances = None
    log_bot = None

    def __init__(self, name, token, logger):
        self.bot = commands.InteractionBot(intents=disnake.Intents.all(
        ), activity=disnake.Activity(name="with the subordinates", type=disnake.ActivityType.playing))
        self.name = name
        self.token = token
        self.file_logger = logger
        self.embedder = Embed()
        self.music_instances = []

        @self.bot.event
        async def on_voice_state_update(member, before: disnake.VoiceState, after: disnake.VoiceState):

            if await self.temp_channels(member, before, after):
                return

            if await self.unmute_clients(member, after):
                return

        @self.bot.event
        async def on_ready():
            self.file_logger.enabled(self.bot)
            print(f"{self.name} is logged as {self.bot.user}")
            self.bot.loop.create_task(self.scan_timer())

        @self.bot.event
        async def on_disconnect():
            print(f"{self.name} has disconnected from Discord")
            self.file_logger.lost_connection(self.bot)

        @self.bot.event
        async def on_connect():
            print(f"{self.name} has connected to Discord")
            # self.file_logger.lost_connection(self.bot)

        @self.bot.event
        async def on_message(message):
            if not message.guild:
                if message.author.id in private_config.admin_ids[list(private_config.admin_ids.keys())[0]]:
                    await message.reply("Your attention is an honor for me, my master.")
                return

            await self.check_message_content(message)
            await self.check_mentions(message)

        @ self.bot.slash_command(description="Allows admin to fix voice channels' bitrate")
        async def bitrate(inter):
            if await self.check_dm(inter):
                return

            if not helpers.is_admin(inter.author):
                return await inter.send("Unauthorized access, you are not the Supreme Being!")

            await inter.send("Processing...")

            await helpers.set_bitrate(inter.guild)

            bitrate = public_config.bitrate_values[inter.guild.premium_tier] // 1000

            await inter.edit_original_response(f'Bitrate was set to {bitrate}kbps!')
            await asyncio.sleep(5)
            await inter.delete_original_response()

        @ self.bot.slash_command(description="Clears voice channel (authorized use only)")
        async def purge(inter):
            if await self.check_dm(inter):
                return
            if inter.author.id != inter.guild.owner_id:
                return await inter.send("Unauthorized access, you are not the Greatest Supreme Being!")
            tasks = []
            for member in inter.author.voice.channel.members:
                if member != inter.author and member.id not in private_config.bot_ids.values():
                    tasks.append(member.move_to(None))
            await asyncio.gather(*tasks)

            await inter.send("Done!")
            await asyncio.sleep(5)
            await inter.delete_original_response()

        @ self.bot.slash_command(description="Clears custom amount of messages")
        async def clear(inter: disnake.AppCmdInter, amount: int):
            if await self.check_dm(inter):
                return
            if not helpers.is_admin(inter.author):
                return await inter.send(f"Unathorized attempt to clear messages!")

            await inter.channel.purge(limit=amount)
            await inter.send(f"Cleared {amount} messages")
            await asyncio.sleep(5)
            return await inter.delete_original_response()

        @ self.bot.slash_command(description="Recreates database")
        async def fill_ranks(inter: disnake.AppCmdInter):
            if await self.check_dm(inter):
                return
            if not inter.author.id in private_config.supreme_beings_ids[inter.guild.id]:
                return await inter.send(f"Unathorized attempt to recreate database!")

            await self.fill_ranks_data()

            await inter.send(f"Done!")
            await asyncio.sleep(5)
            return await inter.delete_original_response()

        @ self.bot.slash_command(description="Resets database")
        async def reset_db(inter: disnake.AppCmdInter):
            if await self.check_dm(inter):
                return
            if not inter.author.id in private_config.supreme_beings_ids[inter.guild.id]:
                return await inter.send(f"Unathorized attempt to recreate database!")

            db = await aiosqlite.connect('bot_database.db')

            await db.execute('''DROP TABLE IF EXISTS users_xp_data''')

            await db.close()

            await self.fill_ranks_data()

            await inter.send(f"Done!")
            await asyncio.sleep(5)
            return await inter.delete_original_response()

        # @ self.bot.slash_command(description="Reviews list of commands")
        # async def help(inter: disnake.AppCmdInter):
        #     await inter.response.defer()
        #     await inter.send(embed=disnake.Embed(color=0, description=self.help()))

    def add_music_instance(self, bot):
        self.music_instances.append(bot)

    def set_log_bot(self, bot):
        self.log_bot = bot

    async def run(self):
        await self.bot.start(self.token)

# *_______LevelingSystem____________________________________________________________________________________________________________________________________________________________________________________________

    def get_roles_from_exp(self, voice_xp, text_xp, ranks):
        ans = []
        prev_rank = self.get_prev_rank(voice_xp, text_xp, ranks)
        curr_rank_flag = False
        for voice_xp_req, text_xp_req, rank_id, remove_flag in ranks:
            if voice_xp >= voice_xp_req and text_xp >= text_xp_req:
                if remove_flag and not curr_rank_flag:
                    ans.append(rank_id)
                    curr_rank_flag = True
                elif not remove_flag:
                    ans.append(rank_id)
        return ans, prev_rank

    def get_prev_rank(self, voice_xp, text_xp, ranks):
        curr_rank_flag = False
        for voice_xp_req, text_xp_req, rank_id, remove_flag in ranks:
            if voice_xp >= voice_xp_req and text_xp >= text_xp_req and remove_flag:
                if not curr_rank_flag:
                    curr_rank_flag = True
                else:
                    return rank_id
        return None

    async def scan_timer(self):
        while not self.bot.is_closed():
            asyncio.create_task(self.scan_channels())
            await asyncio.sleep(60)

    async def scan_channels(self):
        tasks = []
        db = await aiosqlite.connect('bot_database.db')
        await db.execute('CREATE TABLE IF NOT EXISTS users_xp_data (guild_id TEXT, user_id TEXT, voice_xp INTEGER, text_xp INTEGER)')
        cursor = await db.cursor()
        for guild in self.bot.guilds:
            await cursor.execute('''SELECT voice_xp, text_xp, rank_id, remove_flag FROM ranks_data WHERE guild_id = ? ORDER BY voice_xp DESC''', (str(guild.id),))
            ranks = await cursor.fetchall()

            for channel in guild.voice_channels:
                if helpers.get_members_count(channel.members) > 1:
                    for member in channel.members:
                        if member.bot:
                            continue
                        await cursor.execute('''SELECT voice_xp, text_xp FROM users_xp_data WHERE user_id = ? AND guild_id = ?''', (str(member.id), str(guild.id),))
                        xp = await cursor.fetchone()
                        if xp:
                            voice_xp = xp[0] + 1
                            text_xp = xp[1]
                            await cursor.execute('''UPDATE users_xp_data SET voice_xp = ?
                                            WHERE user_id = ? AND guild_id = ?''', (voice_xp, str(member.id), str(guild.id), ))
                        else:
                            voice_xp = 1
                            text_xp = 0
                            await cursor.execute('''INSERT INTO users_xp_data (guild_id, user_id, voice_xp, text_xp) 
                            VALUES (?, ?, ?, ?)''', (str(guild.id), str(member.id), voice_xp, text_xp, ))

                        await db.commit()

                        if not ranks:
                            continue

                        new_ranks, old_rank = self.get_roles_from_exp(
                            voice_xp, text_xp, ranks)

                        new_roles = []
                        for rank_id in new_ranks:
                            rank = guild.get_role(int(rank_id))
                            if rank and rank not in member.roles:
                                new_roles.append(rank)
                        if len(new_roles) > 0:
                            tasks.append(member.add_roles(*new_roles))
                        old_role = None
                        if old_rank:
                            old_role = guild.get_role(int(old_rank))
                            if old_role and old_role in member.roles:
                                tasks.append(member.remove_roles(old_role))
                            else:
                                old_role = None

        await db.close()
        await asyncio.gather(*tasks)

    async def fill_ranks_data(self):
        db = await aiosqlite.connect('bot_database.db')

        await db.execute('''DROP TABLE IF EXISTS ranks_data''')

        await db.execute('''CREATE TABLE IF NOT EXISTS ranks_data (guild_id TEXT, 
                            voice_xp INTEGER, text_xp INTEGER,
                            rank_id TEXT, remove_flag INTEGER)''')

        cursor = await db.cursor()

        for guild, ranks in private_config.REQUIRED_EXP.items():
            for rank in ranks:
                await cursor.execute('''INSERT INTO ranks_data (guild_id, voice_xp, text_xp, rank_id, remove_flag) 
                                        VALUES (?, ?, ?, ?, ?)''', (str(guild), rank[0], rank[1], rank[2], rank[3]))

        await db.commit()
        await db.close()


# *_______OnVoiceStateUpdate_________________________________________________________________________________________________________________________________________________________________________________________


    async def temp_channels(self, member, before: disnake.VoiceState, after: disnake.VoiceState):
        ff = False
        if after.channel and after.channel.name == public_config.temporary_channels_settings['channel_name']:
            await helpers.create_private(member)
            ff = True
        if before.channel and "'s private" in before.channel.name and len(before.channel.members) == 0:
            await before.channel.delete()
            ff = True
        return ff

    async def unmute_clients(self, member, after: disnake.VoiceState):
        ff = False
        if after.channel:
            ff = await helpers.unmute_bots(member)
            ff = ff or (await helpers.unmute_admin(member))
        return ff

# *_______OnMessage_________________________________________________________________________________________________________________________________________________________________________________________

    async def check_message_content(self, message):
        if "discord.gg" in message.content.lower():
            try:
                await message.delete()
                await message.author.send(
                    f"Do NOT try to invite anyone to another servers {public_config.emojis['banned']}")
            except:
                pass
            return True
        return False

    async def check_mentions(self, message):
        if len(message.role_mentions) > 0 or len(message.mentions) > 0:
            client = message.guild.me
            if helpers.is_mentioned(client, message):
                if helpers.is_admin(message.author):
                    if "ping" in message.content.lower() or "пинг" in message.content.lower():
                        return await message.reply(f"Yes, my master. My ping is {round(self.bot.latency*1000)} ms")
                    else:
                        return await message.reply("At your service, my master.")
                else:
                    try:
                        await message.author.timeout(duration=10, reason="Ping by lower life form")
                    except:
                        pass
                    return await message.reply(f"How dare you tag me? Know your place, trash")

# *______SlashCommands______________________________________________________________________________________________________________________________________________________________________________________

    # def help(self):
        # ans = "Type /play to order a song (use URL from YT or just type the song's name)\n"
        # ans += "Type /stop to stop playback\n"
        # return ans

    async def check_dm(self, inter):
        if not inter.guild:
            if inter.author.id in private_config.admin_ids[list(private_config.admin_ids.keys())[0]]:
                await inter.send(f"{public_config.dm_error_admin}")
            else:
                await inter.send(f"{public_config.dm_error}")
            return True
        return False
