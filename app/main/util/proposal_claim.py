from enum import Enum, unique

@unique
class ProposalClaimStatus(Enum):
    # 100 申请中
    # 200 申请通过
    # 300 申请不通过
    # 400 撤销申请

    claiming = 100
    passed = 200
    fail = 300
    cancel = 400