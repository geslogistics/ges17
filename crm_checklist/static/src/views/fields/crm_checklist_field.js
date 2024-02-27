/** @odoo-module */

import { Component } from "@odoo/owl";
import { CRMChecklist } from "@crm_checklist/components/crm_checklist/crm_checklist";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";
import { x2ManyCommands } from "@web/core/orm_service";


export class CRMChecklistField extends Component {
    static template = "crm_checklist.CRMChecklistField";
    static components = { CRMChecklist };
    static props = { ...standardFieldProps };
    /*
    * The method to prepare props for the component CRMChecklist
    */
    checkListProps() {
        return {
            checkPoints: this.list.records.map((record) => record.data.id),
            teamId: this._convertFormData(this.props.record.data.team_id),
            stageId: this._convertFormData(this.props.record.data.stage_id),
            onToggleApprove: this.onToggleApprove.bind(this),
            readonly: this.props.readonly,
        }
    }
    /*
    * Getter for the list
    */
    get list() {
        return this.props.record.data[this.props.name];
    }
    /*
    * The method to add (approve) a checkpoint
    */
    async addRecord(recordId) {
        await this.replaceWith([...this.list.currentIds, ...[recordId]]);
    }
    /*
    * The method to remove (disapprove) a checkpoint
    * IMPORTANT: we need [[6, 0, [ids]]] in write to make the checkpoints work
    */
    async removeRecord(recordId) {
        const currentIds = [...this.list.currentIds];
        const index = currentIds.indexOf(recordId);
        if (index != -1) {
            currentIds.splice(index, 1);
        };
        return this.replaceWith(currentIds);
    }
    /*
    * This is the method to apply the 6 command that is needed to the write method
    */
    async replaceWith(currentIds) {
        return this.list.model.mutex.exec(async () => {
            await this.list._replaceWith(currentIds, { reload: true });
            await this.list._onUpdate();
        });
    }
    /*
    * The method to add/remove new record
    */
    async onToggleApprove(checkPointId, alreadyApproved) {
        if (alreadyApproved) {
            await this.removeRecord(checkPointId);
        }
        else {
            await this.addRecord(checkPointId);
        };
    }
    /*
    * The method to convert form data to real ids
    */
    _convertFormData(fieldValue) {
        return fieldValue && fieldValue.length != 0 ? fieldValue[0] : false;
    }
};

export const cRMChecklistField = {
    component: CRMChecklistField,
    supportedTypes: ["many2many"],
    relatedFields: [ { name: "id", type: "integer" } ],
};

registry.category("fields").add("crm_checklist", cRMChecklistField);
