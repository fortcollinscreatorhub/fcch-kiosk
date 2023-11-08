// Copyright 2023 Stephen Warren <swarren@wwwdotorg.org>
// SPDX-License-Identifier: MIT

function postSimpleApi(url) {
    // FIXME: Use XHR in order to flash errors
    fetch(
        url,
        {
            method: "POST",
            body: "{}",
            headers: {
                "Content-type": "application/json; charset=UTF-8"
            }
        }
    );
}

function doLoad() {
    textArea = document.getElementById("txtUrls");
    textArea.textContent = "Loading..."
    xhr = new XMLHttpRequest();
    xhr.open("GET", "/api/urls-file");
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
            js = JSON.parse(xhr.responseText)
            textArea.textContent = js["content"];
        } else {
            // FIXME: Flash this
            console.log("Load Error: ${xhr.status}");
        }
    };
    xhr.send("");
}

function onLoadBody() {
    doLoad();
}

function onClickNext() {
    postSimpleApi("/api/next-url");
}

function onClickPrev() {
    postSimpleApi("/api/prev-url");
}

function onClickLoad() {
    doLoad();
}

function onClickSave() {
    textArea = document.getElementById("txtUrls");
    urls = textArea.value;
    xhr = new XMLHttpRequest();
    xhr.open("POST", "/api/urls-file");
    xhr.setRequestHeader("Content-Type", "text/plain; charset=UTF-8")
    xhr.onload = () => {
        if (xhr.readyState == 4 && xhr.status == 200) {
        } else {
            // FIXME: Flash this
            console.log("Save Error: ${xhr.status}");
        }
    };
    xhr.send(urls);
}

function onClickDebugOn() {
    postSimpleApi("/api/debug-on");
}

function onClickDebugOff() {
    postSimpleApi("/api/debug-off");
}
