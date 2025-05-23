# Copyright (c) 2025, sushant and contributors
# For license information, please see license.txt

# # import frappe
import requests
import frappe
from frappe.model.document import Document
from frappe.utils import now, today


class ExportIndiaAPISetting(Document):
	pass

@frappe.whitelist()
def fetch_exportindia_data():
	
	settings = frappe.get_single("ExportIndia API Setting")
	if not settings:
		frappe.log_error("ExportIndia API Setting doctype not found", "ExportIndia Integration")
		return
	
	if settings.enabled:
		k = settings.key
		email = settings.email_id
		date_from = today()

		url = f"https://members.exportersindia.com/api-inquiry-detail.php?k={k}&email={email}&date_from={date_from}"

		try:
			response = requests.get(url)
			response.raise_for_status()
			data = response.json()
			print(url,data)

			if isinstance(data, list):
				for record in data:
					inq_id = record.get("inq_id")
					if not frappe.db.exists("ExportIndia Lead", {"inq_id": inq_id}):
						doc = frappe.new_doc("ExportIndia Lead")
						doc.inq_id = inq_id
						doc.exportindia_data = record
						doc.status = "Queued"
						doc.created_on = now()
						doc.insert()
					else:
						print(f"Duplicate entry found for Inq_id: {inq_id}")
			else:
				frappe.log_error("Unexpected data format from ExportIndia API", "ExportIndia Integration")
		except requests.exceptions.RequestException as e:
			frappe.log_error("Unexpected data format from ExportIndia API", "ExportIndia Integration")
		except Exception as e:
			frappe.log_error("ExportIndia API Setting doctype not found", "ExportIndia Integration")

# import frappe
# import requests
# from frappe.utils import today, now

# @frappe.whitelist()
# def fetch_exportindia_data():
#     settings = frappe.get_single("ExportIndia API Setting")
    
#     if not settings:
#         frappe.log_error(message="ExportIndia API Setting doctype not found", title="ExportIndia Integration")
#         return
    
#     if settings.enabled:
#         k = settings.key
#         email = settings.email_id
#         date_from = today()

#         url = f"https://members.exportersindia.com/api-inquiry-detail.php?k={k}&email={email}&date_from={date_from}"

#         try:
#             response = requests.get(url)
#             response.raise_for_status()
#             data = response.json()
#             print(url, data)

#             if isinstance(data, list):
#                 for record in data:
#                     inq_id = record.get("inq_id")
#                     if not frappe.db.exists("ExportIndia Lead", {"inq_id": inq_id}):
#                         doc = frappe.new_doc("ExportIndia Lead")
#                         doc.inq_id = inq_id
#                         doc.exportindia_data = record
#                         doc.status = "Queued"
#                         doc.created_on = now()
#                         doc.insert()
#                     else:
#                         print(f"Duplicate entry found for Inq_id: {inq_id}")
#             else:
#                 frappe.log_error(
#                     message=f"Unexpected data format received from ExportIndia API: {data}",
#                     title="ExportIndia Integration"
#                 )

#         except requests.exceptions.RequestException as e:
#             frappe.log_error(
#                 message=frappe.get_traceback(),
#                 title="ExportIndia API Request Error"
#             )
#         except Exception as e:
#             frappe.log_error(
#                 message=frappe.get_traceback(),
#                 title="ExportIndia API Unexpected Error"
#             )
