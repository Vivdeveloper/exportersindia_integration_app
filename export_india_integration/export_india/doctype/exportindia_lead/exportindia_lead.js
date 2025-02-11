// Copyright (c) 2025, sushant and contributors
// For license information, please see license.txt

frappe.ui.form.on("ExportIndia Lead", {
	refresh: function (frm) {
        if (!frm.doc.lead) {
            frm.add_custom_button(__('Create Lead'), function() {
                frappe.call({
                    method: 'export_india_integration.export_india.doctype.exportindia_lead.exportindia_lead.fetch_exportindia_data',
                    args: {
                        exportindia_lead_name: frm.doc.name
                    },
                    callback: function(response) {
                        if (response.message) {
                            frappe.msgprint(response.message);
                            frm.reload_doc();
                        }
                    }
                });
            });
        } else {
            frm.add_custom_button(__('View Lead'), function() {
                frappe.set_route('Form', 'Lead', frm.doc.lead);
            });
        }
    }
});
