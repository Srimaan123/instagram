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
    let room_id = document.createElement("p")
    room_id.style.display = 'none'
    room_id.setAttribute("id", "room_id")
    room_id.textContent = data.room_id
    main.append(room_id)
})

let sendBtn = document.querySelector(".sendBtn")
let input = document.querySelector("#input")
sendBtn.addEventListener("click", () => {
    socketio.emit("send_message", {
        sender: document.querySelector("#sender").textContent,
        receiver: document.querySelector("#receiver").textContent,
        "message": document.querySelector("#input").value,
        "room_id": document.querySelector("#room_id")
    })
})

function add_message(text, sender) {
    let div = document.createElement("div")
    let p = document.createElement("p")
    if (document.querySelector("#sender").textContent == sender) {
        div.setAttribute("class", "bg-[var(--chat-bubble)] rounded-full p-2")
        p.setAttribute("class", "text-white text-[500]")
    }
    else {
        div.setAttribute("class", "bg-gray-200 rounded-full p-2")
        p.setAttribute("class", "text-black text-[500]")
    }
    p.textContent = text
    div.append(p)
    content.append(div)
}

socketio.on("receive_message", (data) => {
    add_message(data.message, data.sender)
})