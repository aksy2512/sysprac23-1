function ajax_call(userId){
    const xhr = new XMLHttpRequest();
    const url = `http://127.0.0.1:5000/status/${userId}`
    xhr.open('GET', url, true)
    xhr.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            console.log(this.responseText);
        }
    }
    xhr.send()
}