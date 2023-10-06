// Register custome Btn/Field for UploadField
document.querySelector('.register-file-input').addEventListener('change', function (e) {
    var fileName = e.target.files[0].name;
    var maxLength = 20; // maximum number of characters to extract

    // truncate file name (preferably in the middle)
    var truncated = fileName;
    if (fileName.length > maxLength) {
        // truncate string in the middle
        truncated = fileName.substr(0, maxLength / 2) + '...' + fileName.substr(fileName.length - maxLength / 2, fileName.length);
    }

    // set truncated text content as custom file label
    var fileLabel = document.querySelector('.register-file-label');
    fileLabel.textContent = truncated;
});