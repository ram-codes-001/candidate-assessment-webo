/* ============================================================
   CTMS Custom JavaScript
   ============================================================ */

/* ------------------------------------------------------------
   SweetAlert2 Reason Modals
   ------------------------------------------------------------ */

/**
 * Show a reason modal before submitting an edit form.
 * BUG Cat-H: reason enforced by JS only — backend does NOT validate.
 */
function showEditReasonModal(formId) {
    Swal.fire({
        title: 'Reason for Edit',
        text: 'Please provide a reason for modifying this record.',
        input: 'textarea',
        inputPlaceholder: 'Enter reason...',
        showCancelButton: true,
        confirmButtonText: 'Confirm Edit',
        confirmButtonColor: '#007bff',
        preConfirm: (reason) => {
            if (!reason || reason.trim() === '') {
                Swal.showValidationMessage('Reason is required');
            }
            return reason;
        }
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('edit_reason').value = result.value;
            document.getElementById(formId).submit();
        }
    });
}

/**
 * Show a reason modal before submitting a delete form.
 */
function showDeleteReasonModal(formId) {
    Swal.fire({
        title: 'Confirm Deletion',
        text: 'This action cannot be undone. Please state the reason for deletion.',
        input: 'textarea',
        inputPlaceholder: 'Enter reason...',
        showCancelButton: true,
        confirmButtonText: 'Confirm Delete',
        confirmButtonColor: '#dc3545',
        preConfirm: (reason) => {
            if (!reason || reason.trim() === '') {
                Swal.showValidationMessage('Reason is required');
            }
            return reason;
        }
    }).then((result) => {
        if (result.isConfirmed) {
            const form = document.getElementById(formId);
            const reasonInput = form.querySelector('[name="delete_reason"]');
            if (reasonInput) reasonInput.value = result.value;
            form.submit();
        }
    });
}

/* ------------------------------------------------------------
   Initialise plugins on DOM ready
   ------------------------------------------------------------ */
document.addEventListener('DOMContentLoaded', function () {

    /* Flatpickr — date pickers */
    flatpickr('.flatpickr-input', {
        dateFormat: 'Y-m-d',
        allowInput: true,
    });

    /* Select2 — enhanced dropdowns */
    if (typeof $.fn.select2 !== 'undefined') {
        $('.select2').select2({
            theme: 'default',
            width: '100%',
        });
    }

    /* --------------------------------------------------------
       Protocol Deviation — show/hide deviation_notes
       -------------------------------------------------------- */
    var deviationCheckbox = document.getElementById('id_protocol_deviation');
    var deviationNotesRow = document.getElementById('deviation_notes_row');

    function toggleDeviationNotes() {
        if (!deviationCheckbox || !deviationNotesRow) return;
        deviationNotesRow.style.display = deviationCheckbox.checked ? '' : 'none';
    }

    if (deviationCheckbox) {
        toggleDeviationNotes(); // set initial state
        deviationCheckbox.addEventListener('change', toggleDeviationNotes);
    }

    /* --------------------------------------------------------
       SAE — show/hide sae_report_number
       -------------------------------------------------------- */
    var isSeaCheckbox = document.getElementById('id_is_sae');
    var saeReportRow = document.getElementById('sae_report_number_row');

    function toggleSaeReport() {
        if (!isSeaCheckbox || !saeReportRow) return;
        saeReportRow.style.display = isSeaCheckbox.checked ? '' : 'none';
    }

    if (isSeaCheckbox) {
        toggleSaeReport(); // set initial state
        isSeaCheckbox.addEventListener('change', toggleSaeReport);
    }

    /* --------------------------------------------------------
       Toastr configuration
       -------------------------------------------------------- */
    if (typeof toastr !== 'undefined') {
        toastr.options = {
            closeButton: true,
            progressBar: true,
            positionClass: 'toast-top-right',
            timeOut: 4000,
            extendedTimeOut: 1000,
        };
    }

});
