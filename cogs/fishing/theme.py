# 필수 임포트
import os

import discord
from discord.ext import commands

# 부가 임포트
from cogs.fishing import theme_group as _theme_group
from classes.user import User
from constants import Constants
from utils import logger


class ThemeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    theme_group = _theme_group

    """
    @theme_group.command(name="설정", description="낚시카드의 테마를 선택하세요!")
    async def theme(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        ep_user = await User.fetch(ctx.author)
        view = ThemeSelectView(ep_user)
        await ctx.respond(content="골라바", view=view)

    @theme_group.command(name="미리보기", description="낚시카드의 테마를 미리 경헙해보세요")
    async def preview(
        self,
        ctx: discord.ApplicationContext,
        theme_id: Option(str, "미리보기할 테마 아이디를 입력해 주세요.") = None,
        rarity: Option(int, "미리보기할 테마 희귀도(0~4)를 입력해 주세요.") = 1,
    ):
        if not theme_id:
            theme = (await User.fetch(ctx.author.id)).theme
        else:
            theme = theme_id

        if rarity < -1 or rarity > 5:
            return await ctx.respond("그런 희귀도는 업서!")

        dummy_user = ExampleUser(theme)
        dummy_user.theme = theme
        fish = await (await Room.fetch(ctx.channel)).randfish()
        fish.owner = dummy_user
        fish.rarity = rarity

        from .game import get_fishcard_image_file_from_url

        await ctx.respond(f"```json\n{json.dumps(fish.card_data)}\n```")
    """


def setup(bot):
    logger.info(f"{os.path.abspath(__file__)} 로드 완료")
    bot.add_cog(ThemeCog(bot))


class ThemeSelect(discord.ui.Select):
    def __init__(self, ep_user: User):
        options = []
        for i in Constants.THEMES:
            icon = "✅" if i["id"] in ep_user.themes else "❌"
            label = i["name"]
            if i["id"] == ep_user.theme:
                label += " (사용 중)"

            label = i["name"] + " (미보유)" if i["id"] not in ep_user.themes else label
            options.append(
                discord.SelectOption(
                    label=label, description=i["description"], emoji=icon
                )
            )

        super().__init__(
            placeholder="바꿀 테마를 선택하세요.",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if "(미보유)" in self.values[0]:
            return await interaction.response.edit_message(
                content="미보유 테마야!", view=None
            )
        if "(사용 중)" in self.values[0]:
            return await interaction.response.edit_message(
                content="이미 이 테마를 사용하고 있어!", view=None
            )
        if self.values[0] not in [i["name"] for i in Constants.THEMES]:
            return await interaction.response.edit_message(content="으앙 오류", view=None)
        theme_id = list(
            filter(lambda e: e["name"] == self.values[0], Constants.THEMES)
        )[0]["id"]
        ep_user = await User.fetch(interaction.user)
        print(ep_user.theme)
        print(ep_user.themes)
        ep_user.theme = theme_id
        print(ep_user.theme)
        print(ep_user.themes)
        return await interaction.response.edit_message(
            content=f"테마를 `{self.values[0]}`으로 바꿨어!", view=None
        )


class ThemeSelectView(discord.ui.View):
    def __init__(self, ep_user: User):
        super().__init__()
        s = ThemeSelect(ep_user)
        self.add_item(s)


class ExampleUser:
    def __init__(self, theme):
        self.theme = theme

    id = 123456789
    name = "유저 이름"


class ExampleRoom:
    id = 123456789
    owner_id = 123456789
    name = "낚시터 이름"
    fee = 5
    maintenance = 5
    bonus = 5


class ExampleFish:
    id = 123
    name = "물고기"
    rarity = 1
    eng_name = "Fish"
    length = 12345
    average_cost = 654321
    average_length = 54321
    _cost = 123456

    def fee(self, user, room):
        if room.owner_id == user.id:
            return 0
        else:
            return -1 * int(self.cost() * (room.fee / 100))

    def maintenance(self, room):
        return -1 * int(self.cost() * (room.maintenance / 100))

    def bonus(self):
        # 보너스는 상관없이 5%라 가정
        return int(self.cost() * 0.05)

    def cost(self):
        return self._cost
