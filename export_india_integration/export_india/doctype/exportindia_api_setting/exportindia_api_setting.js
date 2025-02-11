// Copyright (c) 2025, sushant and contributors
// For license information, please see license.txt

frappe.ui.form.on("ExportIndia API Setting", {
	refresh: function (frm) {
        // Add a custom button
        frm.add_custom_button(__('Fetch Data'), function () {
            // Call the server-side method
            frappe.call({
                method: 'export_india_integration.export_india.doctype.exportindia_api_setting.exportindia_api_setting.fetch_exportindia_data',
                callback: function (r) {
                    if (r.message) {
                        frappe.msgprint(__('Fetched Date: {0}', [r.message]));
                    }
                }
            });
        });
    }
});
