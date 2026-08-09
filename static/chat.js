let socketio = io();
let main = document.querySelector(".main")
let content = document.querySelector(".content")

socketio.on("connect", () => {
    console.log("connected!!")

})
socketio.emit("join-room", {
    sender_id: document.querySelector("#sender-id").textContent,
    receiver_id: document.querySelector("#receiver-id").textContent
})

socketio.on("joined_room", (data) => {
    let room_id = document.querySelector("#room_id")
    room_id.textContent = data.room
})

let sendBtn = document.querySelector(".sendBtn")
let input = document.querySelector("#input")
sendBtn.addEventListener("click", () => {
    socketio.emit("send_message", {
        sender: document.querySelector("#sender").textContent,
        receiver: document.querySelector("#receiver").textContent,
        "message": document.querySelector("#input").value,
        "room_id": document.querySelector("#room_id").textContent
    })
})

function add_message(text, sender) {
    let div = document.createElement("div")
    let p = document.createElement("p")
    if (document.querySelector("#sender").textContent == sender) {
        div.setAttribute("class", "bg-[var(--chat-bubble)] rounded-full p-2 w-6/12 self-end")
        p.setAttribute("class", "text-white font-[500]")
    }
    else {
        div.setAttribute("class", "bg-gray-200 rounded-full p-2 w-6/12 self-end")
        p.setAttribute("class", "text-white font-[500] ")
    }
    p.textContent = text
    div.append(p)
    content.append(div)
}

socketio.on("receive_message", (data) => {
    add_message(data.message, data.sender)
})