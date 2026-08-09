let socketio = io();
let main = document.querySelector(".main")

socketio.on("connect", () => {
    console.log("connected!!")

})

socketio.emit("join-room", {
    sender_id: document.querySelector("#sender").textContent,
    receiver_id: document.querySelector("#receiver").textContent
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
        room_id: document.querySelector("#room_id").textContent,
        sender: document.querySelector("#username").textContent,
        receiver: document.querySelector("#receiver").textContent,
        "message": document.querySelector(".input").value
    })
})