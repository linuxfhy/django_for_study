# FSM: Finite State Machine
FSM_TRANS_TABLE = [
    {'trigger': 'to_shuijiao', 'source': 'chifan', 'dest': 'shuijiao' }, #The source state of first line will be regard an init_state 
    {'trigger': 'to_dadoudou', 'source': 'chifan', 'dest': 'dadoudou' },
    {'trigger': 'to_dadoudou', 'source': 'shuijiao', 'dest': 'dadoudou'},
    {'trigger': 'to_chifan', 'source': 'dadoudou', 'dest': 'chifan'}]

class FsmStateTrans(object):
    def __init__(self, srcstate, desstate, trigger):
        self.srcstate = srcstate
        self.desstate = desstate
        self.trigger = trigger

class FsmState(object):
    def __init__(self, name):
        self.name = name
        self.trans = {}

def find_state_by_name(state_list, name):
    #print('enter find_state_by_name')
    for cur_state in state_list:
        #print('found stae %s'%cur_state.name)
        if cur_state.name == name:
            return cur_state
    #print('can not find stae %s'%name)
    return None

def find_trans_by_state(state_list, srcstate, desstate):
    for cur_state in state_list:
        for trigger in cur_state.trans:
            if cur_state.name == srcstate and cur_state.trans[trigger] == desstate:
                return True
    return False

def get_source_state(state_list):
    src_list = []
    for cur_state in state_list:
        src_list.append(cur_state.name)
    return src_list

def get_triger_and_desstate(state_list, srcstate):
    for cur_state in state_list:
        if cur_state.name == srcstate:
            return cur_state.trans
    return None

def get_destination_state(state_list, srcstate, trigger):
    for cur_state in state_list:
        if cur_state.name == srcstate:
            return cur_state.trans[trigger]
    return None


#Code for init
class WorkFlowFSM(object):
    def __init__(self):
       self.G_STATE_LIST = []
       for trans in FSM_TRANS_TABLE:
           statecase = find_state_by_name(self.G_STATE_LIST, trans['source'])
           if statecase == None:
               statecase = FsmState(trans['source'])
               self.G_STATE_LIST.append(statecase)
           have_trans = find_trans_by_state(self.G_STATE_LIST, trans['source'], trans['dest'])
           if have_trans == False:
               statecase.trans[trans['trigger']] = trans['dest']
    def FSM_get_init_state(self):
        return self.G_STATE_LIST[0].name

    def FSM_get_source_state(self):
        src_list = []
        for cur_state in self.G_STATE_LIST:
            src_list.append(cur_state.name)
        return src_list
    def FSM_get_triger_and_desstate(self, srcstate):
        for cur_state in self.G_STATE_LIST:
            if cur_state.name == srcstate:
                return cur_state.trans
        return None
    def FSM_get_trigger(self, srcstate):
        for cur_state in self.G_STATE_LIST:
            if cur_state.name == srcstate:
                trigger_list = []
                for elmt in cur_state.trans:
                   trigger_list.append(elmt)
                return trigger_list
        return None
    

#CODE FOR TEST:
def test_cases():
    for cur_trans in FSM_TRANS_TABLE:
        result_dict = get_triger_and_desstate(G_STATE_LIST, cur_trans['source'])
        for dict_elmt in result_dict:
            print("srcstate is %s, trigger is %s, des state is %s"%(cur_trans['source'], dict_elmt, result_dict[dict_elmt]))

    for cur_trans in FSM_TRANS_TABLE:
        trigger = get_triger_and_desstate(G_STATE_LIST, cur_trans['source'])
        for trigger_elmt in trigger:
            desstate = get_destination_state(G_STATE_LIST, cur_trans['source'], trigger_elmt)
            print("srcstate is %s, trigger is %s, des state is %s"%(cur_trans['source'], trigger_elmt, desstate))
#test_cases()

#functions for export
