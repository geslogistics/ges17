/** @odoo-module */

import { CRMChecklist } from "@crm_checklist/components/crm_checklist/crm_checklist";
import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { useService } from "@web/core/utils/hooks";
import { useX2ManyCrud } from "@web/views/fields/relational_utils";


export class CRMChecklistField extends Component {
    /*
    * Overwrite to add own actions and services
    */
    setup() {
        const { saveRecord, removeRecord } = useX2ManyCrud( () => this.list, true);
        this.saveRecord = saveRecord;
        this.removeRecord = removeRecord;
    }
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
        return this.props.value;
    }
    /*
    * The method to add/remove new record
    */
    async onToggleApprove(checkPointId, alreadyApproved) {
        if (alreadyApproved) {
            const record = this.getRecordById(checkPointId);
            if (record) { await this.removeRecord(record) };
        }
        else { await this.saveRecord([checkPointId]) }
    }
    /*
    * The method to find a record by id
    */
    getRecordById(recordId) {
        const recordList = this.list.records.filter(rec => rec.data.id == recordId);
        if (recordList.length != 0) { return recordList[0] }
        return false
    }
    /*
    * The method to convert form data to real ids
    */
    _convertFormData(fieldValue) {
        return fieldValue && fieldValue.length != 0 ? fieldValue[0] : false
    }
}

CRMChecklistField.template = "crm_checklist.CRMChecklistField";
CRMChecklistField.components = { CRMChecklist };
CRMChecklistField.props = { ...standardFieldProps };
CRMChecklistField.supportedTypes = ["many2many"];
CRMChecklistField.isSet = (value) => value.count > 0;

registry.category("fields").add("crm_checklist", CRMChecklistField);
