# Copyright (c) 2025, sushant and contributors
# For license information, please see license.txt

# import frappe
import json
import frappe
from frappe.model.document import Document


class ExportIndiaLead(Document):
	pass

@frappe.whitelist()
def fetch_exportindia_data(exportindia_lead_name):
	print("success")
	try:
		exportindia_lead = frappe.get_doc("ExportIndia Lead", exportindia_lead_name)
	except frappe.DoesNotExistError:
		frappe.throw(f"ExportIndia Lead {exportindia_lead_name} does not exist.")

	settings = frappe.get_single("ExportIndia API Setting")
	exportindia_lead_data = exportindia_lead.exportindia_data
	if not exportindia_lead_data:
		frappe.throw("No data found in exportindia_data.")
	
	try:
		exportindia_lead_data = json.loads(exportindia_lead_data)
	except json.JSONDecodeError:
		frappe.throw("Invalid JSON format in exportindia_lead_data")

	
	lead_name = exportindia_lead_data.get("name") 
	phone = exportindia_lead_data.get("mobile")
	email = exportindia_lead_data.get("email")  
	# company_name = exportindia_lead_data.get("sender_co")  
	# subject = exportindia_lead_data.get("subject") 
	# message = exportindia_lead_data.get("message") 
	# inquiry_type = exportindia_lead_data.get("inquiry_type")  
	sender_city = exportindia_lead_data.get("city")  
	sender_state = exportindia_lead_data.get("state")  
	sender_country = exportindia_lead_data.get("country") 
	inqid= exportindia_lead_data.get("inq_id")

	if frappe.db.exists("Lead", {"custom_inq_id": inqid}):
		frappe.msgprint(f"Lead with ID {inqid} already exists.")
		return
	
	lead = frappe.new_doc("Lead")
	lead.lead_name = lead_name or "Unknown Lead"
	lead.email_id = email
	lead.phone = phone
	# lead.company_name = company_name
	# lead.job_title = subject
	# lead.notes = message
	lead.source = settings.source
	lead.city = sender_city
	lead.state = sender_state
	lead.custom_inq_id = inqid
	
	# lead.inquiry_type = inquiry_type
	lead.insert(ignore_permissions=True)
	frappe.db.commit()

	exportindia_lead.db_set("lead", lead.name)
	exportindia_lead.db_set("status", "Completed")
	frappe.msgprint(f"Lead {lead.name} created successfully.")

@frappe.whitelist()	
def process_exportindia_leads():
    """Processes all ExportIndia Lead entries that are not completed."""
    leads_to_process = frappe.get_all(
		        "ExportIndia Lead",
        filters={"status": ["!=", "Completed"]},
        fields=["name", "exportindia_data"]
    )
	
    settings = frappe.get_single("ExportIndia API Setting")
    for lead in leads_to_process:
        exportindia_lead_name = lead.get("name")
        exportindia_lead_data = lead.get("exportindia_data")

        try:
            if not exportindia_lead_data:
                frappe.db.set_value("ExportIndia Lead", exportindia_lead_name, "status", "No Data")
                frappe.msgprint(f"No data found for ExportIndia Lead {exportindia_lead_name}")
                continue
            print("###########Before Return")
            exportindia_lead_data = json.loads(exportindia_lead_data)
            lead_name = exportindia_lead_data.get("name") 
            phone = exportindia_lead_data.get("mobile")
            email = exportindia_lead_data.get("email") 
            sender_city = exportindia_lead_data.get("city")  
            sender_state = exportindia_lead_data.get("state") 
            sender_country = exportindia_lead_data.get("country")
            inqid= exportindia_lead_data.get("inq_id")
            # subject = exportindia_lead_data.get("subject")
            # message = exportindia_lead_data.get("message")
            # inquiry_type = exportindia_lead_data.get("inquiry_type")
			

            if frappe.db.exists("Lead", {"custom_inq_id": inqid}):
                  frappe.msgprint(f"Lead with ID {inqid} already exists.")
                  return

            lead = frappe.new_doc("Lead")
            lead.lead_name = lead_name or "Unknown Lead"
            lead.email_id = email
            lead.phone = phone
            # lead.company_name = company_name
            # 	# lead.job_title = subject
            # 	# lead.notes = message
            lead.source = settings.source
            lead.city = sender_city
            lead.state = sender_state
            lead.custom_inq_id = inqid
            lead.insert(ignore_permissions=True)
            # print(lead)
            frappe.db.set_value("ExportIndia Lead", exportindia_lead_name, "output", lead.name)
            frappe.db.set_value("ExportIndia Lead", exportindia_lead_name, "status", "Completed")
            frappe.msgprint(f"Lead {lead.name} created successfully for ExportIndia Lead {exportindia_lead_name}.")

        except json.JSONDecodeError:
            frappe.db.set_value("ExportIndia Lead", exportindia_lead_name, "status", "Failed")
            frappe.msgprint(f"Invalid JSON format for ExportIndia Lead {exportindia_lead_name}")
            print("lead#######################FailJSON")

        except Exception as e:
            frappe.db.set_value("ExportIndia Lead", exportindia_lead_name, "status", "Failed")
            print("Failed Exception@@@@@@@@@@#######################FailJSON")
           

