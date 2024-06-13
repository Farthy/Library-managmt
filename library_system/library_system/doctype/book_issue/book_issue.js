// Copyright (c) 2024, Farthy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Book Issue', {
    refresh: function(frm) {
        if (frm.doc.extended) {
            frm.add_custom_button('Apply Penalty and Blacklist', () => {
                frappe.call({
                    method: "library_system.services.rest.apply_penalty_and_blacklist",
                    args: {
                        docname: frm.doc.name
                    },
                    callback: function() {
                        frm.reload_doc();
                    }
                });
            });
        }

        

    },
    validate: function(frm) {
        frappe.call({
            method: "library_system.services.rest.is_book_available",
            args: {
                docname: frm.doc.book
            },
            callback: function(response) {
                if (response.message === 'available') {
                    frappe.msgprint('Book is available');
                    frappe.validated = true;
                } else {
                    frappe.msgprint('Book is not available');
                    frappe.validated = false;
                }
            }
        })
    },
    onload: function(frm) {
        frappe.call({
            method: 'library_system.services.rest.enabled',
        });
    }
});
