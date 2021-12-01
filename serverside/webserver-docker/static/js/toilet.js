const statusElement = document.querySelector("#status");

client = new Paho.Client(location.hostname, 8883, "webClient-" + uuidv4());

client.onConnectionLost = onConnectionLost;
client.onMessageArrived = onMessageArrived;

client.connect({onSuccess: onConnect, reconnect: true});

function onConnectionLost(response){
    if(response.errorCode !== 0){
        console.log("MQTT connection lost: " + response.errorMessage);
    }
}

function onConnect() {
    console.log("Connected to MQTT");

    client.subscribe("dk/ivy/occupancy/toilet");
}

function onMessageArrived(message){
    const payload = JSON.parse(message.payloadString);
    const occupied = payload.occupied;

    if(occupied) {
        statusElement.innerHTML = "Active";
        statusElement.style.color = "green";
    } else {
        statusElement.innerHTML = "Inactive";
        statusElement.style.color = "red";
    }
}