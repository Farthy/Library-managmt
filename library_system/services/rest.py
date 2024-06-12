# import frappe
# @frappe.whitelist()
# def get_available_book():
#     available_issues = frappe.get_all('Book Issue', filters={'status': 'available'}, fields=['book_name','member','status'])
#     return available_issues
# @frappe.whitelist()
# def blacklist_user_method(member, book_issue_name):
#     book_issue = frappe.get_doc("Book Issue", book_issue_name)
#     current_date = frappe.utils.nowdate()
#     if book_issue.return_date < current_date:
#         blacklist_user(member)
#         return "User blacklisted successfully"
#     else:
#         return "Return date not exceeded"
    
# @f@frappe.whitelist() rappe.whitelist()  
# def blacklist_user(member):
#     frappe.db.set_value("Book_Issue", member, "Blacklisted", 1)

# @frappe.whitelist()
# def fine_calculation():
#     book_issue = frappe.get_doc("Book Issue")
#     current_date = frappe.utils.nowdate()
#     fine_days = current_date - book_issue.return_date
#     return fine_days * 15
# library_management/library_management/doctype/book_issue/book_issue.py
# library_management/library_management/doctype/book_issue/book_issue.
import frappe
from frappe.model.document import Document
from frappe.utils import add_days, today
from datetime import datetime, timedelta
import datetime as dt

@frappe.whitelist(allow_guest=True)
def enabled():
    today = datetime.today().strftime('%Y-%m-%d')
    
    doc = frappe.get_list("Book Issue", filters={
        'return_date': ('<', today)
    }, fields=['name','return_date']) 
    for entry in doc:
        if entry.get('return_date'):
            frappe.db.set_value("Book Issue", entry['name'], "extended", 1)
        else:
            frappe.db.set_value("Book Issue", entry['name'], "extended", 0)

    frappe.db.commit()

    return "Enabled field updated successfully"
enabled()

@frappe.whitelist(allow_guest=True)
def apply_penalty_and_blacklist(docname):
    book_issue = frappe.get_doc("Book Issue", docname)
    penalty_amount_list = frappe.db.get_list("Library settings", fields=["penalty_amount"])
    penalty_amount = penalty_amount_list[0].get("penalty_amount")
    return_date = book_issue.return_date + timedelta(days=1)
    today_date = dt.datetime.strptime(frappe.utils.today(), "%Y-%m-%d").date()
    days_overdue = (today_date - return_date).days if today_date > return_date else 0

    
    if days_overdue > 0:
        penalty = days_overdue * penalty_amount
    
        member = frappe.get_doc("LIbrary Member", book_issue.library_member)
        frappe.db.set_value("LIbrary Member", member.name, "blacklisted", 1)
        frappe.db.set_value("LIbrary Member", member.name, "penalty", penalty)

        frappe.db.commit()
        return member

    