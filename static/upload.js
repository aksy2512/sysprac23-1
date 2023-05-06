

var finput, fList, contentDiv, dddisp, submitBtn;
window.addEventListener('load', function(e) {
    finput = document.getElementById('formFile');
    fList = document.getElementById('uploadedFiles');
    contentDiv = document.getElementById('uploadContainer');
    dddisp = document.getElementById('dragDropDisplay');
    submitBtn = document.getElementById('submitBtn');
    finput.addEventListener('change', fileAddedHandler);
    contentDiv.ondragover = (event) => {
        event.preventDefault();
    }
    contentDiv.ondragenter = function(event) {
        event.preventDefault();
        _dragDropCount++;
        dddisp.classList.remove('d-none');
    }
    contentDiv.ondragleave = function(event) {
        _dragDropCount--;
        if (_dragDropCount <= 0)
            dddisp.classList.add('d-none');
    }
    contentDiv.ondrop = function(event) {
        console.log('d', event.dataTransfer.files);
        finput.files = event.dataTransfer.files;
        event.preventDefault();
        _dragDropCount = 0;
        dddisp.classList.add('d-none');
        fileAddedHandler();
    }
})
const _maxFileMegaBytes = 200;
var _dragDropCount = 0;


function fListRowHTML(file) {
    let uid = uuidv4();
    let targettypes = getTargets(file.type);
    let options = targettypes.map(x => `<option value="${x}">${x}</option>`).join('');
    let content = new DocumentFragment();
    let parentr = document.createElement('tr');
    parentr.innerHTML =  `
    <input type="file" class="d-none" name="file_${uid}" disabled/>
    <td>${file.name}</td>
    <td>
        <div class="btn-group">
            <span class="btn btn-warning"><i class="bi bi-${svgid(file.type)}"></i></span>
            <span class="btn btn-warning"><i class="bi bi-arrow-right"></i></span>
            <span class="btn btn-warning">
                <select name="target_${uid}" class="custom-select fixed-input">
                    ${options}
                </select>
            </span>
        </div>
    </td>
    <td>
    <span class="btn btn-danger delbtn"><i class="bi bi-trash3-fill"></i></span></td>
    `;
    content.append(parentr);
    let fi = content.querySelector(`input[name="file_${uid}"]`);
    let datr = new DataTransfer();
    datr.items.add(file);
    fi.files = datr.files;
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
    <td><span class="btn btn-danger delbtn"><i class="bi bi-trash3-fill"></i></span></td>
    `;
    content.append(parentr);
    return content;
}

function svgid(mimetype) {
    switch (mimetype) {
        case 'image/bmp' : return 'filetype-bmp';
        case 'image/gif' : return 'filetype-gif';
        case 'image/jpeg' : return 'filetype-jpg';
        case 'image/png' : return 'filetype-png';
        case 'image/tiff' : return 'filetype-tiff';
        case 'application/pdf' : return 'filetype-pdf';
        case 'audio/mpeg' : return 'filetype-mp3';
        case 'audio/wav' : return 'filetype-wav';
        case 'text/html' : return 'filetype-html';
        case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' : return 'filetype-docx';
        case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' : return 'filetype-xlsx';
        default : return 'file-earmark-richtext';
    }
}

function getTargets(mimetype) {
    if (mimetype.slice(0,5) === 'image' && mimetype !== 'image/svg+xml') 
        return ['JPG', 'PNG', 'GIF', 'BMP', 'TIFF', 'ICO', 'ICNS', 'WEBP', 'TGA', 'EPS', 'PDF'];
    else if (mimetype === 'application/pdf') 
        return ['DOCX', 'JPG', 'PNG', 'GIF', 'BMP', 'TIFF', 'ICO', 'ICNS', 'WEBP', 'TGA', 'EPS'];
    else if (mimetype === 'audio/mpeg') return ['WAV', 'PDF'];
    else if (mimetype === 'audio/wav') return ['MP3', 'PDF'];
    else if (mimetype === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') return ['PDF'];
    else if (mimetype === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') return ['CSV', 'TSV'];
    else return [];
}

function uuidv4() {
    // https://stackoverflow.com/a/2117523
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
        (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

function allText(string) {
    for (let i=0; i<string.length; i++) {
        let cc = string.codePointAt(i);
        if (! (cc >= 0x20 && cc < 0x7f ||
               cc >= 0x08 && cc < 0x0e ||
               cc === 0 || cc === 0x1b))
        return false;
    }
    return true;
}

function inspectFile(content, giventype) {
    if (content.slice(0,4) === '\xFF\xD8\xFF\xDB' || 
        content.slice(0,4) === '\xFF\xD8\xFF\xE0' || 
        content.slice(0,4) === '\xFF\xD8\xFF\xE1' || 
        content.slice(0,4) === '\xFF\xD8\xFF\xE2' || 
        content.slice(0,4) === '\xFF\xD8\xFF\xEE') {
        return "image/jpeg";
    } else if (content.slice(0,2) === 'BM') {
        return "image/bmp";
    } else if (content.slice(0,6) === 'GIF87a' || 
               content.slice(0,6) === 'GIF89a') {
        return "image/gif";
    } else if (content.slice(0,4) === '\x00\x00\x01\x00') {
        return "image/vnd.microsoft.icon";
    } else if (content.slice(0,8) === '\x89\x50\x4E\x47\x0D\x0A\x1A\x0A') {
        return "image/png";
    } else if (content.slice(0,4) === '\x49\x49\x2A\x00' || 
               content.slice(0,4) === '\x4D\x4D\x00\x2A') {
        return "image/tiff";
    } else if (content.slice(0,4)  === 'RIFF' && 
               content.slice(8,12) === 'WEBP') {
        return "image/webp";
    } else if (content.slice(0,5) === '%PDF-') {
        return "application/pdf";
    } else if (content.slice(0,2) === '\xFF\xFB' ||
               content.slice(0,2) === '\xFF\xF3' ||
               content.slice(0,2) === '\xFF\xF2' ||
               content.slice(0,3) === 'ID3' ) {
        return "audio/mpeg";
    } else if (content.slice(0,4)  === 'RIFF' && 
               content.slice(8,12) === 'WAVE') {
        return "audio/wav";
    } else {
        return giventype;
    } 
}

function fileAddedHandler(loadevent) {
    console.log("aaaaaa");
    var rows = new DocumentFragment();
    Array.prototype.forEach.call(finput.files, function(file) {
        if (file.size > _maxFileMegaBytes*1024*1024) {
            rows.appendChild(fListRowHTMLerr(file, "File Size Too Large"));
        } else {
            var reader = new FileReader();
            reader.onloadend = () => { 
                let type = inspectFile(reader.result, file.type);
                if (getTargets(type).length === 0)
                    rows.appendChild(fListRowHTMLerr(file, "Unsupported / Corrupted Format"));
                else
                    rows.appendChild(fListRowHTML(file));
            }
            reader.readAsBinaryString(file.slice(0,20));
        }
    })
    window.setTimeout(function(e) {
        for (let dbn of rows.querySelectorAll('.delbtn')) {
            dbn.onclick = (event) => {event.target.closest('tr').remove()}
        }
        fList.appendChild(rows);
        if (finput.files.length > 0)
            submitBtn.classList.remove('d-none');
        else 
            submitBtn.classList.add('d-none');
    }, 10);
}


