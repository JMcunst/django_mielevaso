from django.db import models


class GuildwarHistory(models.Model):
    atk_user_name = models.CharField(max_length=50)
    atk_hero1 = models.CharField(max_length=30)
    atk_hero2 = models.CharField(max_length=30)
    atk_hero3 = models.CharField(max_length=30)
    atk_hero1_death = models.BooleanField()
    atk_hero2_death = models.BooleanField()
    atk_hero3_death = models.BooleanField()
    atk_hero1_etc = models.TextField()
    atk_hero2_etc = models.TextField()
    atk_hero3_etc = models.TextField()
    def_user_name = models.CharField(max_length=30)
    def_hero1 = models.CharField(max_length=30)
    def_hero2 = models.CharField(max_length=30)
    def_hero3 = models.CharField(max_length=30)
    def_hero1_death = models.BooleanField()
    def_hero2_death = models.BooleanField()
    def_hero3_death = models.BooleanField()
    def_hero1_etc = models.TextField()
    def_hero2_etc = models.TextField()
    def_hero3_etc = models.TextField()
    is_atk_victory = models.BooleanField()
    is_def_victory = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    atk_guild_name = models.CharField(max_length=30)
    atk_guild_rank = models.IntegerField()
    def_guild_name = models.CharField(max_length=30)
    def_guild_rank = models.IntegerField()
    season_name = models.CharField(max_length=30)
    is_public = models.BooleanField()

    def __str__(self):
        return f"{self.atk_user_name} vs {self.def_user_name}"

    def get_atk_heroes(self):
        return [self.atk_hero1, self.atk_hero2, self.atk_hero3]

    def get_def_heroes(self):
        return [self.def_hero1, self.def_hero2, self.def_hero3]

    def get_atk_deaths(self):
        return [
            self.atk_hero1_death,
            self.atk_hero2_death,
            self.atk_hero3_death,
        ]

    def get_def_deaths(self):
        return [
            self.def_hero1_death,
            self.def_hero2_death,
            self.def_hero3_death,
        ]

    def get_atk_etc(self):
        return [self.atk_hero1_etc, self.atk_hero2_etc, self.atk_hero3_etc]

    def get_def_etc(self):
        return [self.def_hero1_etc, self.def_hero2_etc, self.def_hero3_etc]

    def is_atk_win(self):
        return self.is_atk_victory

    def is_def_win(self):
        return self.is_def_victory

