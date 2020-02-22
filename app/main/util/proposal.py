from enum import Enum, unique

@unique
class ProposalStatus(Enum):
    # 100 待投票: 创建后第一个状态,此时还未上链
    # 200 立项投票中: 上链成功, 在规定投票时间内进行链上投票 -> 300, 400
    # 300 申领中: 如果投票通过, 提案状态自动改变(投票结束时达成条件) -> 500
    # 400 投票未通过: 在规定投票时内, 没有达成通过条件, 状态自动改变 end
    # 以下是 status=300 后才会有的状态
    # 500 进行中: 由(专区)管理员修改到此状态 -> 600, 800
    # 600 验收中: 由(专区)管理员修改到此状态，此时需要进行多签投票,决定提案是否验收 -> 700, 800
    # 700 已完成: 如果投票通过, 提案状态自动改变(投票结束时达成条件) end 
    # 800 失败: 验收投票不通过, 提案状态自动改变(投票结束时达成条件); 也可能是申领人放弃 end
    wait_to_vote = 100
    set_up_voting = 200
    claiming = 300
    set_up_vote_fail = 400
    under_way = 500
    checking = 600
    success = 700
    fail = 800

@unique
class ProposalLogEvent(Enum):

    # 提案基础信息
    create = 1 # 创建提案
    update_info = 2 # 更新提案信息
    update_status = 3 # 更新提案状态

    # 进度更新
    # TODO: 只有admin, creator, claim pass 的人可以发布更新
    update_progress = 4 # 更新项目进度

    # 提案链上投票
    onchain_success = 5 # 提案上链成功
    onchain_fail = 6 # 提案上链失败
    vote = 7 # 给提案投票
    vote_result = 8 # 投票结果产生
    
    # 提案申领
    proposal_claim_claiming = 9 # 提案申领
    proposal_claim_cancel = 10 # 取消提案申领
    proposal_claim_passed = 11 # 提案申领审核通过
    proposal_claim_fail = 12 # 提案申领审核失败
