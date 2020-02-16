from app.main import db
from app.main.model import User, ProposalZone, Proposal, Currency, Category, ProposalLog
from app.main.service.util import save_changes
from app.main.service import proposal_service


class addInitLog:
    def run():
        create_proposal_log = proposal_service.create_proposal_log

        all_proposals = Proposal.query.all()
        for proposal in all_proposals:
            print(proposal.id, proposal.title, proposal.logs.count())
            if (proposal.logs.count() == 0):
                # add proposal log, create
                create_proposal_log(proposal_id=proposal.id,
                                    event_key='create',
                                    op_user_id=proposal.creator_id,
                                    creator_id=proposal.creator_id,
                                    op_time=proposal.created)

                print('新增创建日志')
