document.addEventListener('DOMContentLoaded', function() {
  
  //Script: Files

  document.getElementById('file-upload').addEventListener('change', function() {

    var fullPath = this.value;
    var fileName = fullPath.split('\\').pop();

    // Display the selected file name (optional)
    
    document.getElementById('selected-file').innerHTML = fileName;
  
  });
  
}); 