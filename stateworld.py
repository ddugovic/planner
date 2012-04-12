import tworld as tw

class StateWorld:
    def __init__(self):
        #TODO hardcoded 32 board size
        #default is Floor
        self.top = [[tw.Empty]*32 for x in range(32)]
        self.bottom = [[tw.Empty]*32 for x in range(32)]
        self.tick = 0
#for these we always know, don't need to track
#         self.keys = [0]*4
#         self.boots = [false]*4
#         self.chips = 0
    
    #update our state based on the things we can see
    #TODO hardcoded vision size
    def update(self):
        vision=4 #from chip in all direction
        self.tick += 1
    
    #return if our plan will still work
    def validate(self, plan):
        #TODO actually validate this
        return len(plan)>0
    
    def write_pddl(self, out):
        """produce the pddle for the board in it's current state"""
        print >> out, """(define (problem p01-%d-cc)
          (:domain chips-challenge)
          """ % self.tick
        max_num = tw.chips_needed() + 5
        produce_objects( out, max_num)
        self.produce_init( out, max_num)
        self.produce_goal( out)
        print >> out, ")"

    def produce_init( self, out, max_num ):
        """Produce intial state"""
        print >> out, """(:init"""
        print >> out, "(chips-left n%d)" % tw.chips_needed()
        print >> out, "(switched-walls-open n0)" 
        print >> out, "(has-keys red n%d)" % tw.get_keys()[0] 
        print >> out, "(has-keys blue n%d)" % tw.get_keys()[1]
        print >> out, "(has-keys yellow n%d)" % tw.get_keys()[2]
        print >> out, "(has-keys green n%d)" % tw.get_keys()[3]
        if tw.get_boots()[0]: # ICE
            print >> out, "(has-boots ice)"
        if tw.get_boots()[1]: # SUCTION
            print >> out, "(has-boots slide)"
        if tw.get_boots()[2]: # FIRE
            print >> out, "(has-boots fire)"
        if tw.get_boots()[3]: # WATER
            print >> out, "(has-boots water)"
        produce_succesors(out, max_num) 
        self.produce_predicates( out, 32, 32)
        print >> out, ")"

        
    def produce_predicates( self, out, x_max, y_max ):
        ''' produce locations'''
        for i in range( x_max ):
            for j in range( y_max ):
                ################
                # TODO: improve this logic to be more readable
                # and maintinable
                #################
                
                treat_as_floor = (tw.Empty, tw.Exit, tw.HintButton, tw.Wall_North, tw.Wall_South, 
                                tw.Wall_East, tw.Wall_West, tw.Wall_Southeast)
                top, bot = tw.get_tile(i,j)
                
                produce_simple_conversions(out, top, i, j)
                
                if top in treat_as_floor:
                    print >> out, "(floor pos-%d-%d)" % (i,j)
                elif top in (tw.HiddenWall_Perm, tw.HiddenWall_Temp, 
                             tw.BlueWall_Real, tw.BlueWall_Fake):
                    print >> out, "(floor pos-%d-%d)" % (i,j)
                elif top == tw.Socket:
                    print >> out, "(socket pos-%d-%d)" % (i,j)
                elif top in (tw.Chip_North, tw.Chip_West, tw.Chip_South, tw.Chip_East):
                    print >> out, "(at pos-%d-%d)" % (i,j)
                    if top == tw.Chip_East:
                        chip_dir = "dir-east"
                    elif top == tw.Chip_West:
                        chip_dir = "dir-west"
                    elif top == tw.Chip_South:
                        chip_dir = "dir-south"
                    elif top == tw.Chip_North:
                        chip_dir = "dir-north"
    
                    if bot in treat_as_floor:
                        print >> out, "(floor pos-%d-%d)" % (i,j)
                    elif bot == tw.Wall:
                        print >> out, "(wall pos-%d-%d)" % (i,j)
                    elif bot == tw.Ice:
                        print >> out, "(ice pos-%d-%d)" % (i,j)
                        print >> out, "(chip-state slipping)"
                        print >> out, "(slipping-dir %s)" % chip_dir
                    elif bot == tw.SwitchWall_Open:
                        print >> out, "(switch-wall-open pos-%d-%d)" % (i,j)
                    elif bot == tw.SwitchWall_Closed:
                        print >> out, "(switch-wall-closed pos-%d-%d)" % (i,j)
                    elif bot == tw.Button_Green:
                        print >> out, "(green-button pos-%d-%d)" % (i,j)
                    elif bot in (tw.Slide_North, tw.Slide_South, tw.Slide_East, tw.Slide_West):
                        print >> out, "(force-floor pos-%d-%d)" % (i,j)
                        print >> out, "(chip-state sliding)" #note not slipping
                        if bot == tw.Slide_North:
                            print >> out, "(slide-dir pos-%d-%d dir-north)" % (i,j)
                        elif bot == tw.Slide_South:
                            print >> out, "(slide-dir pos-%d-%d dir-south)" % (i,j)
                        elif bot == tw.Slide_East:
                            print >> out, "(slide-dir pos-%d-%d dir-east)" % (i,j)
                        elif bot == tw.Slide_West:
                            print >> out, "(slide-dir pos-%d-%d dir-west)" % (i,j)
                elif top in (tw.Slide_North, tw.Slide_South, tw.Slide_East, tw.Slide_West):
                    print >> out, "(force-floor pos-%d-%d)" % (i,j)
                    if top == tw.Slide_North:
                        print >> out, "(slide-dir pos-%d-%d dir-north)" % (i,j)
                    elif top == tw.Slide_South:
                        print >> out, "(slide-dir pos-%d-%d dir-south)" % (i,j)
                    elif top == tw.Slide_East:
                        print >> out, "(slide-dir pos-%d-%d dir-east)" % (i,j)
                    elif top == tw.Slide_West:
                        print >> out, "(slide-dir pos-%d-%d dir-west)" % (i,j)
                elif top == tw.Gravel:
                    print >> out, "(floor pos-%d-%d)" % (i, j)
                    print >> out, "(gravel pos-%d-%d)" % (i, j)
                elif top in (tw.IceWall_Northeast, tw.IceWall_Northwest, tw.IceWall_Southeast, tw.IceWall_Southwest):
                    print >> out, "(ice-wall pos-%d-%d)" % (i,j)
                    if top == tw.IceWall_Northeast: # Open North and East
                        # slip in going south slip out going east
                        print >> out, "(ice-wall-dir pos-%d-%d dir-south dir-east)" % (i,j)
                        print >> out, "(ice-wall-dir pos-%d-%d dir-west dir-north)" % (i,j)
                    elif top == tw.IceWall_Northwest: # Open North and West
                        print >> out, "(ice-wall-dir pos-%d-%d dir-south dir-west)" % (i,j)
                        print >> out, "(ice-wall-dir pos-%d-%d dir-east dir-north)" % (i,j)
                    elif top == tw.IceWall_Southeast: # Open South and East
                        print >> out, "(ice-wall-dir pos-%d-%d dir-north dir-east)" % (i,j)
                        print >> out, "(ice-wall-dir pos-%d-%d dir-west dir-south)" % (i,j)
                    elif top == tw.IceWall_Southwest: # Open South and West
                        print >> out, "(ice-wall-dir pos-%d-%d dir-north dir-west)" % (i,j)
                        print >> out, "(ice-wall-dir pos-%d-%d dir-east dir-south)" % (i,j)
                elif top == tw.SwitchWall_Open or bot == tw.SwitchWall_Open:
                    print >> out, "(switch-wall-open pos-%d-%d)" % (i,j)
                elif top == tw.SwitchWall_Closed or bot == tw.SwitchWall_Closed:
                    print >> out, "(switch-wall-closed pos-%d-%d)" % (i,j)
                elif top == tw.Button_Green or bot == tw.Button_Green:
                    print >> out, "(green-button pos-%d-%d)" % (i,j)
                # set up movement
                if i != 0 and can_move_east_west(tw.get_tile(i-1,j),tw.get_tile(i,j)) :
                    print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-east)" % (i-1,j, i,j)
                    print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-west)" % (i,j, i-1,j)
                if j != 0 and can_move_north_south(tw.get_tile(i,j-1), tw.get_tile(i,j) ):
                    print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-south)" % (i,j-1, i,j)
                    print >> out, "(MOVE-DIR pos-%d-%d pos-%d-%d dir-north)" % (i,j, i,j-1)
        
        
    def produce_goal( self, out ):
        ''' product locations'''
        print >> out, "(:goal "
        for i in range( 32 ):
            for j in range( 32 ):
                top, bot = tw.get_tile(i,j)
                if top == tw.Exit :
                    print >> out, "(at pos-%d-%d)" % (i,j)
        print >> out, ")"

def produce_objects( out, max_num ):
    print >> out, """(:objects
    dir-east - direction
    dir-north - direction
    dir-south - direction
    dir-west - direction
    red - color
    blue - color
    yellow - color
    green - color
    water - type
    fire - type
    ice - type
    slide - type
    """
    produce_numbers( out, max_num )
    produce_locations( out, 32, 32 )
    print >> out, ")"

def produce_numbers( out, num ):
    for n in range( num + 1):
        print >> out, "n%d - number" % n

def produce_locations( out, x_max, y_max ):
    ''' product locations'''
    for i in range( x_max ):
        for j in range( y_max ):
            print >> out, "pos-%d-%d - location" % (i,j )

def produce_succesors(out, num ):
    ''' Procude the successor prediciates up to num'''
    for n in range( num ):
        print >> out, "(successor n%d n%d)" % (n, n+1)

def can_move_east_west( (w_top, w_bot), (e_top, e_bot) ):
    """ if movement east to west is possible"""
    if both_walls( (w_top, w_bot), (e_top, e_bot) ):
        return False
    # west does not have a blocking tile
    # IceWall_Southwest is open to the south and west
    if  set((w_top, w_bot)).isdisjoint( (tw.Wall_East, tw.IceWall_Southwest, tw.IceWall_Northwest, tw.Wall_Southeast) ) and \
        set( (e_top, e_bot)).isdisjoint( (tw.Wall_West, tw.IceWall_Southeast, tw.IceWall_Northeast) ):
        return True
    else:
        return False

def can_move_north_south( n_tile, s_tile ):
    """ if movement north to south is possible n_tile and s_tile are (top, bot) tuples"""
    if both_walls( n_tile, s_tile ):
        return False
    # IceWall_Northeast is open to the north and east
    if  set( n_tile).isdisjoint( (tw.Wall_South, tw.IceWall_Northeast, tw.IceWall_Northwest, tw.Wall_Southeast) ) and \
        set( s_tile).isdisjoint( (tw.Wall_North, tw.IceWall_Southeast, tw.IceWall_Southwest) ):
        return True
    else:
        return False

def both_walls( (a_top, a_bot), (b_top, b_bot) ):
    """ if both a and b are walls movement between is impossible"""
    return (a_top == tw.Wall or a_bot == tw.Wall ) and \
           (b_bot == tw.Wall or b_bot == tw.Wall )

def produce_simple_conversions( out, top, i, j ):
    '''convert tiles that are simply converted to a feature at a location'''
    #TODO for efficiency these dictionaries should not be created every call
    #TODO this is only simple conversion for top, what about bottom?
    converts={
        tw.ICChip:'chip',
        tw.Wall: 'wall',
        tw.Water: 'water',
        tw.Fire: 'fire',
        tw.Ice: 'ice',
        tw.PopupWall: 'popup-wall',
        tw.Dirt: 'dirt',
        tw.Burglar: 'thief',
        tw.Block_Static: 'block',
        tw.Bomb: 'bomb'
    }
    if top in converts:
        pddl_label = converts[top]
        print >> out, "(%s pos-%d-%d)" % (pddl_label, i, j)

    typed_converts={
        tw.Key_Red: ('key', 'red'),
        tw.Key_Blue: ('key', 'blue'),
        tw.Key_Yellow: ('key', 'yellow'),
        tw.Key_Green: ('key', 'green'),
        tw.Door_Red: ('door', 'red'),
        tw.Door_Blue: ('door', 'blue'),
        tw.Door_Yellow: ('door', 'yellow'),
        tw.Door_Green: ('door', 'green'),
        tw.Boots_Water: ('boots', 'water'),
        tw.Boots_Fire: ('boots', 'fire'),
        tw.Boots_Ice: ('boots', 'ice'),
        tw.Boots_Slide: ('boots', 'slide')
    }
        
    if top in typed_converts:
        (pddl_label, val) = typed_converts[top]
        print >> out, "(%s pos-%d-%d %s)" % (pddl_label, i, j, val)