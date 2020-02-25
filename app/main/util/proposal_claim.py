from enum import Enum, unique

@unique
class ProposalClaimStatus(Enum):
    # 100 申领中
    # 200 申领通过
    # 300 申领不通过
    # 400 撤销申领

    claiming = 100
    passed = 200
    fail = 300
    cancel = 400