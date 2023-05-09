const urlParams = new URLSearchParams(window.location.search);
const user_uuid = urlParams.get('user_uuid');
console.log(user_uuid);

function ajax_call(){
    let fileStatusList;
    const xhr = new XMLHttpRequest();
    const url = `http://localhost:5000/status/${user_uuid}`;
    xhr.open('GET', url, false);

    xhr.onreadystatechange = function () {
        if(this.readyState == 4 && this.status == 200){
            fileStatusList = this.responseText;
        }else{
            return undefined;
        }
    }
    xhr.send();
    return JSON.parse(fileStatusList);
}

function downloadFile(url, filename) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.responseType = 'blob';
    xhr.onload = function(){
        if (xhr.status === 200){
            var blob = new Blob([xhr.response], {type: 'application/octet-stream'});
            var url = URL.createObjectURL(blob);
            var link = document.createElement('a');
            link.href = url;
            link.download = filename;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }
    };
    xhr.send();
}

var fList, contentDiv;
window.addEventListener('load', function(e){
    // capturing the required DOM elements
    fList = document.getElementById('convertedFiles');
    contentDiv = document.getElementById('downloadContainer');
    if(!user_uuid){
        // user_uuid is not present
        // redirecting to home page
        window.location.replace("http://localhost:5000/")
    }
    while(true){
        // making ajax calls
        fileStatus = ajax_call();
        let flag = false;
        for(let i=0;i<fileStatus.length;i++){
            if(fileStatus[i]?.status === "Pending"){
                flag = true;
                break;
            }
        }
        fileAddedHandler(fileStatus);

        if(!flag){
            // All files are processed
            break;
        }
    }
});

function fListRowHTML(file){
    let content = new DocumentFragment();
    let parentr = document.createElement('tr');
    cont =  `
    <td>${file.name}</td>
    <td>${file.status}</td>
    `;
    if(file.status == 'Done'){
        cont = cont + `<td><span id=${file.file_id} class="btn btn-info downloadbtn" data-filename=${file.name}>Download</span></td>`;
    }else{
        cont = cont + `<td><span> -- </span></td>`
    }
    parentr.innerHTML = cont;
    content.append(parentr);
    return content;
}

function fListRowHTMLerr(file, err_msg) {
    let content = new DocumentFragment();
    let parentr = document.createElement('tr');
    parentr.classList.add('invalid-row');
    parentr.innerHTML = `
    <td>${file.name}</td>
    <td>
        <span class="text-danger">${err_msg}</span>
    </td>
    <td><span class="btn btn-danger downloadbtn">--</span></td>
    `;
    content.append(parentr);
    return content;
}

function fileAddedHandler(fileStatus){
    fList.innerHTML = null;
    var rows = new DocumentFragment();
    for(let i=0;i<fileStatus.length;i++){
        rows.appendChild(fListRowHTML(fileStatus[i]))
    }

    for (let downloadbtn of rows.querySelectorAll('.downloadbtn')) {
        downloadbtn.onclick = (event) => {
            id = event.target.id;
            filename = event.target.dataset.filename;
            downloadFile(`http://localhost:5000/download/${id}`, filename);
        }
    }
    fList.appendChild(rows);
}
