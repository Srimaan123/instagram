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
    let wrap = document.createElement("div")
    if (document.querySelector("#sender").textContent == sender) {
        div.setAttribute("class", "bg-[var(--chat-bubble)] rounded-tr-xl rounded-tl-full rounded-br-full rounded-bl-full p-2 w-6/12 self-end")
        p.setAttribute("class", "text-white font-[500]")
        wrap.setAttribute("class","flex justify-end")
    }
    else {
        div.setAttribute("class", "bg-gray-200 rounded-tl-xl rounded-tr-full rounded-br-full rounded-bl-full p-2 w-6/12")
        p.setAttribute("class", "text-black font-[500] ")
        wrap.setAttribute("class","flex")
    }
    p.textContent = text
    div.append(p)
    wrap.append(div)
    content.append(wrap)
}

socketio.on("receive_message", (data) => {
    add_message(data.message, data.sender)
})