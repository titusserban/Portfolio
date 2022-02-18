const csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value 
const alertBox = document.getElementById('alert-box')

const handleAlerts = (type, msg) => {
    alertBox.innerHTML = `
        <div class="alert alert-${type}" role="alert">
            ${msg}
        </div>
    `
}

// Disable autodiscover to avoid any errors
Dropzone.autoDiscover = false
const myDropzone = new Dropzone('#my-dropzone', {
    url: '/datascience/upload_file/',
    init: function() {
        this.on('sending', function(file, xhr, formData){
            // console.log('sending')
            formData.append('csrfmiddlewaretoken', csrf)
        })
        this.on('success', function(file, response){
            // console.log(response.ex)
            if(response.csv_exists) {
                handleAlerts('danger', 'File already exists')
            } else {
                handleAlerts('success', 'Your file has been uploaded')
            }
        })
    },
    maxFiles: 1,
    maxFilesize: 3, // mb
    acceptedFiles: '.csv'
})