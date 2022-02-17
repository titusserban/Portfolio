const reportBtnContainer = document.getElementById("report-btn-container");
const reportBtn = document.getElementById("report-btn");
const img = document.getElementById("img")
const modalBody = document.getElementById("modal-body")
const reportName = document.getElementById("id_name")
const author = document.getElementById("id_author")
const reportRemarks = document.getElementById("id_remarks")
const csrf = document.getElementsByName("csrfmiddlewaretoken")[0].value
const reportForm = document.getElementById("report-form")
const alertBox = document.getElementById("alert-box")


const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
        `
}


if (img) {
    reportBtnContainer.classList.remove("not-visible");
}


reportBtn.addEventListener("click", () => {
    // set a boostrap class of 100% width
    img.setAttribute("class", "w-100");
    // append the image at the beginning of the form
    modalBody.prepend(img);

    reportForm.addEventListener("submit", (e) => {
        // we prevent the form submission 
        e.preventDefault() 
        // form data instantiating 
        const formData = new FormData();
        formData.append("csrfmiddlewaretoken", csrf);
        formData.append("name", reportName.value);
        formData.append("remarks", reportRemarks.value);
        formData.append("author", author.value);
        formData.append("image", img.src);

        // AJAX
        $.ajax ({
            type: "POST",
            url: "/datascience/create_report_view/",
            data: formData,
            success: function(response) {
                handleAlerts("success", "The report has been created.")
            },
            error: function(error) {
                handleAlerts("danger", "Error... Something went wrong...")
            },
            processData: false,
            contentType: false,
        })
    })
})


