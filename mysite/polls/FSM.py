# FSM: Finite State Machine
############################################################################################################################################################
#FSM_TRANS_TABLE：改进建议状态转换表
#    source：源状态
#    trigger：触发条件，对应一个按钮
#    dest：经按钮触发后的目的状态
#    trans_action：转换后的一些动作，目前有：
#        assign_to:将问题指派给某个字段对应的处理人，已经支持
#        send_mail_to:给某人发送邮件，尚不支持
#        set_fields:给某些字段设置给定值，已经支持


trans_action_1 = {'assign_to':'改进建议评审人',    'send_mail_to':'XX字段' }
trans_action_2 = {'assign_to':'改进建议实施人',    'send_mail_to':'XX字段' }
trans_action_3 = {'assign_to':'创建人(只读)',      'send_mail_to':'XX字段' }
trans_action_4 = {}
trans_action_5 = {'assign_to':'改进建议评审人',    'send_mail_to':'XX字段' }
trans_action_6 = {}
trans_action_7 = {'assign_to':'改进建议实施人',    'send_mail_to':'XX字段' }

FSM_TRANS_TABLE = [
    {'source': '提交建议',			'trigger': '提交评审',	 		'dest': '改进建议价值评审',	'trans_condition':{},   'trans_action':trans_action_1}, #The source state of first line will be regard an init_state 
    {'source': '改进建议价值评审',	'trigger': '指定实施人', 	 	'dest': '改进建议实施',		'trans_condition':{},   'trans_action':trans_action_2}, #the value of assign_to here should be
    {'source': '改进建议价值评审',	'trigger': '评审不通过', 		'dest': '提交建议',	        'trans_condition':{},   'trans_action':trans_action_3},
	{'source': '改进建议实施',		'trigger': '更新进展',			'dest': '改进建议实施',		'trans_condition':{},   'trans_action':trans_action_4},
	{'source': '改进建议实施',		'trigger': '实施结果提交评审', 	'dest': '实施结果评审',		'trans_condition':{},   'trans_action':trans_action_5},
	{'source': '实施结果评审',		'trigger': '落地关闭', 			'dest': '关闭',		'trans_condition':{},   'trans_action':trans_action_6},
	{'source': '实施结果评审',		'trigger': '评审不通过',		'dest': '改进建议实施',		'trans_condition':{},   'trans_action':trans_action_7}]
############################################################################################################################################################
#FSM_TRANS_TABLE_DEVICECARD: 设备档案的状态转换表
device_card_trans_action_occupy = {'assign_to':'anyone',    'send_mail_to':'XX字段',    'set_fields':{'当前使用状态':'使用中'},
                             'set_field_nonconstant':{'设备使用人':'get_current_user'}
                             }

device_card_trans_action_free = {'assign_to':'anyone',    'send_mail_to':'XX字段',    'set_fields':{'当前使用状态':'未被占用', '设备使用人':'无'}}
device_trans_condition_update = {'当前使用状态':{'op':'!=','value':'使用中'}}
device_trans_condition_occupied = {'当前使用状态':{'op':'!=','value':'使用中'}}
device_trans_condition_freed = {'当前使用状态':{'op':'==','value':'使用中'}}
FSM_TRANS_TABLE_DEVICECARD = [
    {'source': '设备档案',		'trigger': '占用设备',		'dest': '设备档案',		'trans_condition':device_trans_condition_occupied,   'trans_action':device_card_trans_action_occupy},
    {'source': '设备档案',		'trigger': '释放设备',		'dest': '设备档案',		'trans_condition':device_trans_condition_freed,   'trans_action':device_card_trans_action_free},
    {'source': '设备档案',		'trigger': '更新信息',		'dest': '设备档案',		'trans_condition':device_trans_condition_update,   'trans_action':{}}
]
############################################################################################################################################################
#上市保障问题跟踪
issue_track_action_1 = {'assign_to':'维护代表'}
issue_track_action_2 = {'assign_to':'维护处理人'}
issue_track_action_3 = {'assign_to':'改进提取SE'}
FSM_TRANS_ISSUE_TRACK = [
    {'source': '维护人员处理',		'trigger': '更新进展',		'dest': '维护人员处理',		'trans_condition':{},   'trans_action':{'assign_to':'创建人(只读)'}},
    {'source': '维护人员处理',		'trigger': '提交审核',		'dest': '维护代表审核',		'trans_condition':{},   'trans_action':issue_track_action_1},
    {'source': '维护代表审核',		'trigger': '打回补充信息',	'dest': '维护人员处理',		'trans_condition':{},   'trans_action':issue_track_action_2},
    {'source': '维护代表审核',		'trigger': '转SE分析改进',	'dest': 'SE分析改进',		'trans_condition':{},   'trans_action':issue_track_action_3},
    {'source': 'SE分析改进',		'trigger': '问题关闭',	    'dest': '关闭',		    'trans_condition':{},   'trans_action':{}}
]

############################################################################################################################################################
#捷安特自行车维护
FSM_TRANS_GINAT_MAINTAIN_TRACK = [
    {'source': '创建保养预约单',	'trigger': '提交预约单',	'dest': '等待保养',		'trans_condition':{},   'trans_action':{'assign_to':{'constant':'tanluzhe7'}}},
    {'source': '等待保养',		'trigger': '完成保养',	        'dest': '关闭',		        'trans_condition':{},   'trans_action':{}}
]
############################################################################################################################################################
#OAK_ESS早期支持策略_订单支持
FSM_TRANS_ESS_ORDER_SUPPORT = [
    {'source': '打开',	'trigger': '更新进展',	'dest': '打开', 'trans_condition':{},   'trans_action':{}},
    {'source': '打开',	'trigger': '关闭',	'dest': '关闭', 'trans_condition':{},   'trans_action':{}}
]

############################################################################################################################################################
#定义各个项目对应的状态转换表
TRANS_TABLE_DICT = {
    'improvement':FSM_TRANS_TABLE,
    'device_card':FSM_TRANS_TABLE_DEVICECARD,
    'issue_track':FSM_TRANS_ISSUE_TRACK,
    'giant_maintain':FSM_TRANS_GINAT_MAINTAIN_TRACK,
    'ESS_OrderSupport':FSM_TRANS_ESS_ORDER_SUPPORT,
    'ESS_SupplySpport':FSM_TRANS_ESS_ORDER_SUPPORT,
    'ESS_CustomerIssue':FSM_TRANS_ESS_ORDER_SUPPORT,
    'ESS_MasterBranchSync':FSM_TRANS_ESS_ORDER_SUPPORT,
    'ESS_LeftBugSolve':FSM_TRANS_ESS_ORDER_SUPPORT
}
############################################################################################################################################################
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

def find_trans_by_state(state_list, srcstate, desstate, trigger):
    for cur_state in state_list:
        for trigger_tmp in cur_state.trans:
            if cur_state.name == srcstate and cur_state.trans[trigger_tmp]['dest'] == desstate and trigger in cur_state.trans:
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
           have_trans = find_trans_by_state(self.G_STATE_LIST, trans['source'], trans['dest'], trans['trigger'])
           if have_trans == False:
               statecase.trans[trans['trigger']] = {'dest':trans['dest'], 'condition':trans['trans_condition']}# replace trans['dest'] with {'dest':trans['dest'], 'condition':trans['condition']}
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
    for cur_trans in FSM_TRANS_TABLE: #test
        result_dict = get_triger_and_desstate(G_STATE_LIST, cur_trans['source'])
        for dict_elmt in result_dict:
            print("srcstate is %s, trigger is %s, des state is %s"%(cur_trans['source'], dict_elmt, result_dict[dict_elmt]))

    for cur_trans in FSM_TRANS_TABLE: #test
        trigger = get_triger_and_desstate(G_STATE_LIST, cur_trans['source'])
        for trigger_elmt in trigger:
            desstate = get_destination_state(G_STATE_LIST, cur_trans['source'], trigger_elmt)
            print("srcstate is %s, trigger is %s, des state is %s"%(cur_trans['source'], trigger_elmt, desstate))
#test_cases()

#functions for export
