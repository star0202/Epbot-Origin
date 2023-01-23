from discord import SlashCommandGroup

fishing_group = SlashCommandGroup("낚시터", "낚시터 관련 명령어")
land_group = fishing_group.create_subgroup("시설", "시설 관련 명령어")
theme_group = SlashCommandGroup("낚시카드", "낚시카드 테마 관련 명령어")
