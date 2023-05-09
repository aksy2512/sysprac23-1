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
            console.log(this.responseText);
            fileStatusList = this.responseText;
        }else{
            return undefined;
        }
    }
    xhr.send();
    return JSON.parse(fileStatusList);
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
        console.log(fileStatus);
        let flag = false;
        for(let i=0;i<fileStatus.length;i++){
            if(fileStatus[i]?.status === "Pending"){
                flag = true;
                break;
            }
        }
        fileAddedHandler(fileStatus);
        // break;
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
        cont = cont + `<td><span class="btn btn-danger downloadbtn"><i class="bi bi-trash3-fill"></i></span></td>`;
    }else{
        cont = cont + `<td><span> -- </span></td>`
    }
    parentr.innerHTML = cont;
    content.append(parentr);
    // let fi = content.querySelector(`input[name="file_${uid}"]`);
    // let datr = new DataTransfer();
    // datr.items.add(file);
    // fi.files = datr.files;
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

    // Array.prototype.forEach.call(finput.files, function(file) {
    //     if (file.size > _maxFileMegaBytes*1024*1024) {
    //         rows.appendChild(fListRowHTMLerr(file, "File Corrupted"));
    //     } else {
    //         var reader = new FileReader();
    //         reader.onloadend = () => { 
    //             let type = inspectFile(reader.result, file.type);
    //             if (getTargets(type).length === 0)
    //                 rows.appendChild(fListRowHTMLerr(file, "Unsupported / Corrupted Format"));
    //             else
    //                 rows.appendChild(fListRowHTML(file, type));
    //         }
    //         reader.readAsBinaryString(file.slice(0,20));
    //     }
    // })
    for (let downloadbtn of rows.querySelectorAll('.downloadbtn')) {
        downloadbtn.onclick = (event) => {event.target.closest('tr').remove()}
    }
    fList.appendChild(rows);
}
