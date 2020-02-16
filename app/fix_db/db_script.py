from app.main import db
from app.main.model import User, ProposalZone, Proposal, Currency, Category, ProposalLog
from app.main.service.util import save_changes
from app.main.service import proposal_service


class DbScript:
    def add_init_create_log():
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

    def set_all_proposal_status_none():

        all_proposals = Proposal.query.all()
        for proposal in all_proposals:
            print(proposal.id, proposal.title, proposal.status)
            proposal.status = None
            db.session.commit()
            print('修改状态成功')

    def del_logs_update_status_double():
        all_proposal_logs = ProposalLog.query.all()
        for proposal_log in all_proposal_logs:
            if (proposal_log.event_key == 'update_status'):
                if (proposal_log.to_value == None):
                    print(proposal_log.id, proposal_log.proposal_id,
                          proposal_log.event_key, proposal_log.to_value,
                          proposal_log.op_user_id)

                    # delete
                    db.session.delete(proposal_log)
                    db.session.commit()
                    print('delete success')