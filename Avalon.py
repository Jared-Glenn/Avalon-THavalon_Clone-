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
        'Merlin' : 'You know which people have Evil roles, but not who has any specific role.\nYou are a valid Assassination target.',
        'Percival' : 'You know which people have the Merlin and Morgana roles, but not who has each.',
        'Lancelot' : 'You may play Reversal cards while on missions.\nYou appear Evil to Merlin.',
        'Arthur' : 'You know which Good roles are in the game, but not who has any given role.\nIf two missions have Failed, and less than two missions have Succeeded, you may declare as Arthur.\nAfter declaring, your vote on team proposals is counted twice, but you are unable to be on mission teams until the 5th mission.\nAfter declaring, you are immune to any effect that can forcibly change your vote.',
        'Titania' : 'You appear as Evil to all players with Evil roles (except Colgrevance).',
        'Nimue' : 'You know which Good and Evil roles are in the game, but not who has any given role.\nYou are a valid Assassination target.',
        'Galahad' : 'After two quests have failed, you can declare as Galahad.\nAfter declaring, all other players must close their eyes and hold their fists in front of them.\nYou can name two Good roles (such as Merlin, Arthur, or Lancelot), one at a time.\nIf one of the players is that role, they must raise their thumb to indicate who they are.\nAfter this phase, play resumes normally.',
        'Guinevere' : 'You know two \"rumors\" about other players, but nothing about their roles.\nThese rumors give you a glimpse at somebody else\'s character information, telling you who they know something about,\nbut not what roles they are.\nFor instance, you if you heard a rumor about Player A seeing Player B,\nit might mean Player A is Merlin seeing an Evil player, or it might mean they are both Evil and can see each other.',

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
def get_role_information(my_player,players):
    return {
        'Tristan' : ['{} is Iseult.'.format(player.name) for player in players if player.role == 'Iseult'],
        'Iseult' : ['{} is Tristan.'.format(player.name) for player in players if player.role == 'Tristan'],
        'Merlin' : ['{} is Evil'.format(player.name) for player in players if (player.team == 'Evil' and player.role != 'Mordred') or player.role == 'Lancelot'],
        'Percival' : ['{} is Merlin or Morgana.'.format(player.name) for player in players if player.role == 'Merlin' or player.role == 'Morgana'],
        'Lancelot' : [],
        'Arthur' : ['{}'.format(player.role) for player in players if player.team == 'Good' and player.role != 'Arthur'],
        'Titania' : [],
        'Nimue' : ['{}'.format(player.role) for player in players if player.role != 'Nimue'],
        'Galahad' : [],
        'Guinevere' : [get_rumors(my_player, players)],

        'Mordred' : ['{} is Evil.'.format(player.name) for player in players if (player.team == 'Evil' and player != my_player and player.role != 'Colgrevance') or player.role == 'Titania'],
        'Morgana' : ['{} is Evil.'.format(player.name) for player in players if (player.team == 'Evil' and player != my_player and player.role != 'Colgrevance') or player.role == 'Titania'],
        'Maelagant' : ['{} is Evil.'.format(player.name) for player in players if (player.team == 'Evil' and player != my_player and player.role != 'Colgrevance') or player.role == 'Titania'],
        'Agravaine' : ['{} is Evil.'.format(player.name) for player in players if (player.team == 'Evil' and player != my_player and player.role != 'Colgrevance') or player.role == 'Titania'],
        'Colgrevance' : ['{} is {}.'.format(player.name, player.role) for player in players if player.team == 'Evil' and player != my_player],
    }.get(my_player.role,[])

def get_rumors(my_player, players):
    rumors = []

    # Generate rumors about Merlin
    merlin_player = None
    is_Merlin = 0
    for player in players:
        if player.role == 'Merlin':
            merlin_player = player.name
            is_Merlin = 1
    if is_Merlin == 1:
        for player in players:
            if (player.team == 'Evil' and player.role != 'Mordred') or player.role == "Lancelot":
                player_of_evil = player.name
                rumors.append('{} sees {}'.format(merlin_player, player_of_evil))

    # Generate rumors about Percival
    percival_player = None
    is_Percival = 0
    for player in players:
        if player.role == 'Percival':
            percival_player = player.name
            is_Percival = 1
    if is_Percival == 1:
        for player in players:
            if player.role == 'Merlin' or player.role == 'Morgana':
                seer = player.name
                rumors.append('{} sees {}'.format(percival_player, seer))

    # Generate rumor about the Lovers
    tristan_player = None
    iseult_player = None
    is_Lovers = 0
    for player in players:
        if player.role == 'Tristan':
            tristan_player = player.name
            is_Lovers += 1
        elif player.role == 'Iseult':
            iseult_player = player.name
            is_Lovers += 1
    if is_Lovers == 2:
        rumors.append('{} sees {}'.format(tristan_player, iseult_player))
        rumors.append('{} sees {}'.format(iseult_player, tristan_player))

    # Generate rumor about Evil players
    for player in players:
        if player.team == 'Evil' and player.role != 'Mordred':
            for player_two in players:
                if (player_two.team == 'Evil' and player_two.role != 'Mordred' and player_two.role != 'Colgrevance' and player_two != player) or (player_two.role == 'Titania' and player_two != player):
                    rumors.append('{} sees {}'.format(player.name, player_two.name))

    print(rumors)
    return random.choice(rumors)


# Oberoning Merlin (save for later)
#if player_of_role.get('Merlin'):
#    merlin_player = '{}'.format(player.name) for player in players if player.role == 'Merlin'
#    nonevil_list = []
#    for player in players:
#        if player.team != 'Evil' and player.role != "Lancelot" and player.role != "Merlin:
#            nonevil_list.append(player.name)
#    random_nonevil = random.sample(nonevil_list,1)[0]
#    rumors['merlin_rumor'] = [merlin_player + ' sees {}'.format(player.name) for player in players if (player.team == 'Evil' and player.role != 'Mordred') or player.role == 'Lancelot' or player.name == random_nonevil]


class Player():
    # Players have the following traits
    # name: the name of the player as fed into system arguments
    # role: the role the player possesses
    # team: whether the player is on good or evil's team
    # type: information or ability
    # seen: a list of what they will see
    # modifier: the random modifier this player has [NOT CURRENTLY UTILIZED]
    def __init__(self, name):
        self.name = name
        self.role = None
        self.team = None
        self.modifier = None
        self.info = []
        self.is_assassin = False

    def set_role(self, role):
        self.role = role

    def set_team(self, team):
        self.team = team

    def add_info(self, info):
        self.info += info

    def erase_info(self, info):
        self.info = []

    def generate_info(self, players):
        pass

def get_player_info(player_names):
    num_players = len(player_names)
    if len(player_names) != num_players:
        print('ERROR: Duplicate player names.')
        exit(1)

    # create player objects
    players = []
    for i in range(0, len(player_names)):
        player = Player(player_names[i])
        players.append(player)

    # number of good and evil roles
    if num_players < 7:
        num_evil = 2
    elif num_players < 9:
        num_evil = 3
    else:
        num_evil = 4
    num_good = num_players - num_evil

    # establish available roles
    good_roles = ['Merlin', 'Percival', 'Guinevere', 'Tristan', 'Iseult', 'Lancelot', 'Galahad']
    #'Tristan', 'Iseult'
    evil_roles = ['Mordred', 'Morgana', 'Maelagant']

    # additional roles for player-count
    # 5 only
    if num_players < 6:
        good_roles.append('Nimue')

    # 7 plus
    if num_players > 6:
        good_roles.append('Arthur')
        good_roles.append('Titania')

    # 8 plus
    if num_players > 7:
        evil_roles.append('Agravaine')

    # 10 only
    if num_players == 10:
        evil_roles.append('Colgrevance')

    '''
    cide for testing role interaction
    if num players == 2:
        good_roles = ['Merlin']
        evil_roles = ['Maeve']
        num_good = 1
        num_evil = 1
    '''
    good_roles_in_game = random.sample(good_roles, num_good)
    evil_roles_in_game = random.sample(evil_roles, num_evil)

    # lone lovers are rerolled
    # 50% chance to reroll one lone lover
    # 50% chance to reroll another role into a lover
    if sum(gr in ['Tristan','Iseult'] for gr in good_roles_in_game) == 1 and num_good > 1:
        if 'Tristan' in good_roles_in_game:
            good_roles_in_game.remove('Tristan')
        if 'Iseult' in good_roles_in_game:
            good_roles_in_game.remove('Iseult')

        if random.choice([True, False]):
            # replacing the lone lover
             available_roles = set(good_roles)-set(good_roles_in_game)-set(['Tristan','Iseult'])
            # DecrecationWarning issue. Found solution at https://stackoverflow.com/questions/70426576/get-random-number-from-set-deprecation
             good_roles_in_game.append(random.sample([available_roles],k=1)[0])
        else:
            # upgradng to pair of lovers
            rerolled = random.choice(good_roles_in_game)
            good_roles_in_game.remove(rerolled)
            good_roles_in_game.append('Tristan')
            good_roles_in_game.append('Iseult')

    # roles after validation
    #print(good_roles_in_game)
    #print(evil_roles_in_game)

    # role assignment
    random.shuffle(players)

    good_players = players[:num_good]
    evil_players = players[num_good:]

    player_of_role = dict()

    for gp in good_players:
        new_role = good_roles_in_game.pop()
        gp.set_role(new_role)
        gp.set_team('Good')
        player_of_role[new_role] = gp

    # if there is at least one evil, first evil player becomes assassin
    if len(evil_players) > 0:
        evil_players[0].is_assassin = True

    for ep in evil_players:
        new_role = evil_roles_in_game.pop()
        ep.set_role(new_role)
        ep.set_team('Evil')
        player_of_role[new_role] = ep

    for p in players:
        p.add_info(get_role_information(p,players))
        random.shuffle(p.info)
        # print(p.name,p.role,p.team,p.info)

    # Informing Evil about Colgrevance
    for ep in evil_players:
        if ep.role != 'Colgrevance' and player_of_role.get('Colgrevance'):
            ep.add_info(['Colgrevance lurks in the shadows. (There is another Evil that you do not see.)'])
        if ep.role != 'Colgrevance' and player_of_role.get('Titania'):
            ep.add_info(['Titania has infiltrated your ranks. (One of the people you see is not Evil.)'])
        if ep.is_assassin:
            ep.add_info(['You are the Assassin.'])

    # delete and recreate game directory
    if os.path.isdir("game"):
        shutil.rmtree("game")
    os.mkdir("game")

    bar= '----------------------------------------\n'
    for player in players:
        player.string= bar+'You are '+player.role+' ['+player.team+']\n'+bar+get_role_description(player.role)+'\n'+bar+'\n'.join(player.info)+'\n'+bar
        player_file = "game/{}".format(player.name)
        with open(player_file,"w") as file:
            file.write(player.string)

    first_player = random.sample(players,1)[0]
    with open("game/start", "w") as file:
        file.write("The player proposing the first mission is {}.".format(first_player.name))
        #file.write("\n" + second_mission_starter + " is the starting player of the 2nd round.\n")

    with open("game/DoNotOpen", "w") as file:
        file.write("Player -> Role\n\n GOOD TEAM:\n")
        for gp in good_players:
            file.write("{} -> {}\n".format(gp.name, gp.role))
        file.write("\nEVIL TEAM:\n")
        for ep in evil_players:
            file.write("{} -> {}\n".format(ep.name,ep.role))

if __name__ == "__main__":
    if not (6 <= len(sys.argv) <= 11):
        print("Invalid number of players")
        exit(1)

    players = sys.argv[1:]
    num_players = len(players)
    players = set(players) # use as a set to avoid duplicate players
    players = list(players) # convert to list
    random.shuffle(players) # ensure random order, though set should already do that
    if len(players) != num_players:
        print("No duplicate player names")
        exit(1)

    get_player_info(players)
