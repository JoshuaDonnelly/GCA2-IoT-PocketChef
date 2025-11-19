let aliveSecond = 0;
let heartBeatRate = 5000;
let pubnub;
let appChannel = "johns-pi";

function time() {
  let d = new Date();
  let currentSecond = d.getTime();
  if (currentSecond - aliveSecond > heartBeatRate + 1000) {
    document.getElementById("connection_id").innerHTML = "DEAD";
  } else {
    document.getElementById("connection_id").innerHTML = "ALIVE";
  }
  setTimeout("time()", 1000);
}

function keepAlive() {
  fetch("/keep_alive")
    .then((response) => {
      if (response.ok) {
        let date = new Date();
        aliveSecond = date.getTime();
        return response.json();
      }
      throw new Error("Server offline");
    })
    .catch((error) => console.log(error));
  setTimeout("keepAlive", heartBeatRate);
}

function handleClick(cb) {
  if (cb.checked) {
    value = "on";
  } else {
    value = "off";
  }
  publishMessage({ buzzer: value });
}

const setupPubNub = () => {
  pubnub = new pubnub({
    publishKey: "your_publish_key",
    subscribeKey: "your_subscribe_key",
    userId: "johns_laptop",
  });

  //create a channel
  const channel = pubnub.channel(appChannel);
  //create a subscription
  const subscription = channel.subscription();

  pubnub.addListener({
    status: (s) => {
      console.log("Status", s.category);
    },
  });

  subscription.onMessage = (messageEvent) => {
    handleMessage(messageEvent.message);
  };
  subscription.subscribe();
};
