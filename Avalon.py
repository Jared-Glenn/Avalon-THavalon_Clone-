import copy
import os
import random
import shutil
import sys

# get_role_descriptions - this is called when information files are generated.
def get_role_description(role):
    return {
        'Tristan' : 'The person you see is also Good and is aware that you are Good.\nYou and Iseult are collectively a valid Assassination target.',
        'Iseult' : 'The person you see is also Good and is aware that you are Good.\nYou and Tristan are collectively a valid Assassination target.',
        'Merlin' : 'You know which people have Evil roles, but not who has any specific role.\nYou are a valid Assassination target.'
        'Percival' : 'You know which people have the Merlin and Morgana roles, but not who has each.',
        'Lancelot' : 'You may play Reversal cards while on missions.\nYou appear Evil to Merlin.',
        'Arthur' : 'You know which Good roles are in the game, but not who has any given role.\nIf two missions have Failed, and less than two missions have Succeeded, you may declare as Arthur.\nAfter declaring, your vote on team proposals is counted twice, but you are unable to be on mission teams until the 5th mission.\nAfter declaring, you are immune to any effect that can forcibly change your vote.',
        'Titania' : 'You appear as Evil to all players with Evil roles (except Colgrevance).',
        'Nimue' : 'You know which Good and Evil roles are in the game, but not who has any given role.\You are a valid Assassination target.',

        'Mordred' : 'You are hidden from all Good roles that could reveal that information.\nLike other Evil characters, you know who else is Evil (except Colgrevance).',
        'Morgana' : 'You appear like Merlin to Percival.\nLike other Evil characters, you know who else is Evil (except Colgrevance).',
        'Maelagant' : 'You may play Reversal cards while on missions.\nLike other Evil characters, you know who else is Evil (except Colgrevance).',
        'Agravaine' : 'You must play Fail cards while on missions.\nIf you are on a mission that Succeeds, you may declare as Agravaine to cause it to Fail instead.\nLike other Evil characters, you know who else is Evil (except Colgrevance).',
        'Colgrevance' : 'You know not only who else is Evil, but what role each other Evil player possesses.\nEvil players know that there is a Colgrevance, but do not know that it is you or even that you are Evil.',
}.get(role,'ERROR: No description available.')

# get_role_information: this is called to populate information files
# blank roles:
# - Lancelot: no information
# - Arthur: no information
# - Guinevere: too complicated to generate here
# - Colgrevance: name, role (evil has an update later to inform them about the presence of Colgrevance)
def get_role_information(myplayer,players):
    return {
        'Tristan' : ['{} is Iseult.'.format(player.name) for player in players if player.role is 'Iseult'],
        'Iseult' : ['{} is Tristan.'.format(player.name) for player in players if player.role is 'Tristan'],
        'Merlin' : ['{} is Evil'.format(player.name) for player in players if (player.team is 'Evil' and player.role is not 'Mordred') or player.role is 'Lancelot'],
        'Percival' : ['{} is Merlin or Morgana.'.format(player.name) for player in players if player.role is 'Merlin' or player.role is 'Morgana'],
        'Lancelot' : [],
        'Arthur' : ['{}'.format(player.name) for player in players if player.team is 'Good' and player.role is not 'Arthur'],
        'Titania' : [],
        'Nimue' : ['{}'.format(player.name) for player in players if player.role is not 'Nimue']

        'Mordred' : ['{} is Evil.'.format(player.name) for player in players if (player.team is 'Evil' and player is not my_player and player.role is not 'Colgrevance') or player.role is 'Titania'],
        'Morgana' : ['{} is Evil.'.format(player.name) for player in players if (player.team is 'Evil' and player is not my_player and player.role is not 'Colgrevance') or player.role is 'Titania'],
        'Maelagant' : ['{} is Evil.'.format(player.name) for player in players if (player.team is 'Evil' and player is not my_player and player.role is not 'Colgrevance') or player.role is 'Titania'],
        'Agravaine' : ['{} is Evil.'.format(player.name) for player in players if (player.team is 'Evil' and player is not my_player and player.role is not 'Colgrevance') or player.role is 'Titania'],
        'Colgrevance' : ['{} is {}.'.format(player.name, player.role) for player in players if player.team is 'Evil' and player is not my_player],
    }.get(my_player.role[])

class Player():
    # Players have the following traits
    # name: the name of the player as fed into system arguments
    # role: the role the player possesses
    # team: whether the player is on good or evil's team
    # type: information or ability
    # seen: a list of what they will see
    # modifier: the random modifier this player has [NOT CURRENTLY UTILIZED]
    def _init_(self, name)
        self.name = name
        self.role = None
        self.team = None
        self.modifier = None
        self.info = []
        self.is.assassin = False

    def set_role(self, role):
        self.role = role

    def set_team(self, team):
        self.team = team

    def add_info(self, info):
        self.info += info

    def generate_info(self, players):
        pass

    def get_player_info(player_names):
    }
