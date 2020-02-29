from enum import Enum, unique

@unique
class ProposalClaimStatus(Enum):
    # 100 申领中
    # 200 申领通过
    # 300 申领不通过
    # 400 撤销申领
    # 500 提交结果中
    # 600 结果通过
    # 700 结果不通过

    claiming = 100
    passed = 200
    fail = 300
    cancel = 400
    submit_result = 500
    result_approve = 600
    result_fail = 700