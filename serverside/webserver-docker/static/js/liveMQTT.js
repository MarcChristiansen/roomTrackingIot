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

    client.subscribe("dk/ivy/occupancy/living");
    client.subscribe("dk/ivy/occupancy/toilet");
}

function onMessageArrived(message){
    const payload = JSON.parse(message.payloadString);
    const occupied = payload.occupied;
    const topic = message.topic;
    const room = topic.split("/").at(-1);

    switch(room){
        case "living":
            setLiving(occupied);
            break;
        case "toilet":
            setToilet(occupied);
            break;
    }
}