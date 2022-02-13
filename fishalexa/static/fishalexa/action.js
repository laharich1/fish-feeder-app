"use strict"

function feed() {
    let request = new XMLHttpRequest()
    request.onreadystatechange = function() {
        if (request.readyState != 4) return
    }

    request.open("POST", "/feed", true);
    request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    request.send("&csrfmiddlewaretoken="+getCSRFToken());
}

function lightSwitch() {
    let itemTextElement = document.getElementById("id_light")
    let state   = itemTextElement.innerHTML
    let request = new XMLHttpRequest()
    request.onreadystatechange = function() {
        if (request.readyState != 4) return
    }
    console.log(state)
    if (state == "Light On") {
       itemTextElement.innerHTML = "Light Off"
       request.open("POST", "/light-on", true);
       request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
       request.send("currentState="+state+"&csrfmiddlewaretoken="+getCSRFToken());

    }
    else if (state == "Light Off") {
       itemTextElement.innerHTML = "Light On"
       request.open("POST", "/light-off", true);
       request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
       request.send("currentState="+state+"&csrfmiddlewaretoken="+getCSRFToken());
    }

}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}
