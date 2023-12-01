/** @odoo-module */

import { Domain } from "@web/core/domain";
import { Component, useState, onWillStart, onWillUpdateProps } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";


export class CRMChecklist extends Component {
    /*
    * The method to set up initial values
    */
    setup() {
        this.orm = useService("orm");
        this.state = useState({ allCheckPoints: null });
        onWillStart(async () => {
            await this.onCalculateCheckPoints(this.props);
        });
        onWillUpdateProps(async (nextProps) => {
            await this.onCalculateCheckPoints(nextProps);
        });
    }
    /*
    * The method to calculate checkpoints available for the current stage and team
    */
    async onCalculateCheckPoints(props) {
        const allCheckPoints = await this.orm.searchRead(
            "crm.check.list",
            this._getCheckPointsDomain(props),
            ["name", "description"]
        );
        Object.assign(this.state, { allCheckPoints: allCheckPoints});
    }
    /*
    * The method to approve/disapprove the checkpoint
    */
    async onToggleApprove(checkPointId, alreadyApproved=false) {
        if (this.props.readonly) { return };
        const saved = await this.orm.call("crm.check.list", "action_check_cheklist_rights", [[checkPointId]]);
        if (saved) { await this.props.onToggleApprove(checkPointId, alreadyApproved) };
    }
    /*
    * The method to construct the domain for available check points
    */
    _getCheckPointsDomain(props) {
        const teamDomain = Domain.or([ [["team_ids", "=", false]], [["team_ids", "=", props.teamId]] ]);
        const stageDomain = [ ["crm_stage_st_id", "=", props.stageId] ];
        return Domain.and([teamDomain, stageDomain]).toList()
    }
}

CRMChecklist.template = "crm_checklist.CRMChecklist";
CRMChecklist.props = {
    checkPoints: { type: Array },
    teamId: { type: Number },
    stageId: { type: Number },
    onToggleApprove: { type: Function },
    readonly: { type: Boolean },
};

