# FSM: Finite State Machine
trans_action_1 = {'assign_to':'改进建议评审人',    'send_mail_to':'XX字段' }
trans_action_2 = {'assign_to':'改进建议实施人',    'send_mail_to':'XX字段' }
trans_action_3 = {'assign_to':'创建人(只读)',      'send_mail_to':'XX字段' }
trans_action_4 = {}
trans_action_5 = {'assign_to':'改进建议评审人',    'send_mail_to':'XX字段' }
trans_action_6 = {}
trans_action_7 = {'assign_to':'改进建议实施人',    'send_mail_to':'XX字段' }

FSM_TRANS_TABLE = [
    {'source': '提交建议',			'trigger': '提交评审',	 		'dest': '改进建议价值评审',	'trans_action':trans_action_1}, #The source state of first line will be regard an init_state 
    {'source': '改进建议价值评审',	'trigger': '评审通过', 	 		'dest': '改进建议实施',		'trans_action':trans_action_2}, #the value of assign_to here should be
    {'source': '改进建议价值评审',	'trigger': '评审不通过', 		'dest': '提交建议',	        'trans_action':trans_action_3},
	{'source': '改进建议实施',		'trigger': '更新进展',			'dest': '改进建议实施',		'trans_action':trans_action_4},
	{'source': '改进建议实施',		'trigger': '实施结果提交评审', 	'dest': '实施结果评审',		'trans_action':trans_action_5},
	{'source': '实施结果评审',		'trigger': '评审通过', 			'dest': '改进建议落地',		'trans_action':trans_action_6},
	{'source': '实施结果评审',		'trigger': '评审不通过',		'dest': '改进建议实施',		'trans_action':trans_action_7}]

FSM_TRANS_TABLE_DEVICECARD = [
    {'source': '设备档案',		'trigger': '更新使用档案',		'dest': '设备档案',		'trans_action':{}}
]
TRANS_TABLE_DICT = {
    'improvement':FSM_TRANS_TABLE,
    'device_card':FSM_TRANS_TABLE_DEVICECARD
}

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
    def __init__(self, prj_name):
       self.G_STATE_LIST = []
       GENERIC_TRANS_TABLE = TRANS_TABLE_DICT[prj_name]
       for trans in GENERIC_TRANS_TABLE:
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
    def FSM_get_trans_action(self, prj_name, srcstate, trigger):
        GENERIC_TRANS_TABLE = TRANS_TABLE_DICT[prj_name]
        for trans in GENERIC_TRANS_TABLE:
            if trans['source'] == srcstate and trans['trigger'] == trigger:
                return trans['trans_action'] 
    

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
