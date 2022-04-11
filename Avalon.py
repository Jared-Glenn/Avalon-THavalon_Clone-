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

    }
