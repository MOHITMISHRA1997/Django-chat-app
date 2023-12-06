$(document).ready(function(){
    $('#action_menu_btn').click(function(){
        $('.action_menu').toggle();
    });
        });





// showing online/offline inside the chatbox
user = document.getElementById('online_status').innerText


if(user == 'True'){

    var new_el = document.createElement('p')
    new_el.innerText = 'Online'
    document.getElementById('receiver_id').appendChild(new_el)

}
else{
    const on_off_icon = document.getElementById('status_icon')
    on_off_icon.classList.add("offline")
    var new_el = document.createElement('p')
    new_el.innerText = 'Offline'
    document.getElementById('receiver_id').appendChild(new_el)
  
}



// sending Images/files To the server 
document.getElementById('fileInput').addEventListener('change', handleFileSelect, false);

function handleFileSelect(event) {
    var files = event.target.files;
    // Handle the selected files (e.g., upload to server, display preview, etc.)
    // You can use XMLHttpRequest, fetch API, or other methods to upload files to the server.
}

// Optionally, you can add a click event listener to the paperclip icon to trigger the file input.
document.querySelector('.attach_btn').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});


