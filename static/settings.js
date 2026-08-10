let socketio = io()
let username = document.querySelector("#username").textContent
socketio.on("connect",()=>{
    console.log("connected!!")
})
let AccType = document.querySelector("#AccType")

AccType.addEventListener("change",(e)=>{
    socketio.emit("changeAccountType",{"username":username,"accType":e.target.value})
})