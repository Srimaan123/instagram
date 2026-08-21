let socketio = io()
let username = document.querySelector("#username").textContent
let changeDiv = document.querySelector(".change-div")
let profilepic = document.querySelector('.profilepic')
socketio.on("connect",()=>{
    console.log("connected!!")
})
let AccType = document.querySelector("#AccType")

AccType.addEventListener("change",(e)=>{
    socketio.emit("changeAccountType",{"username":username,"accType":e.target.value})
})
profilepic.addEventListener('click',(e)=>{
    changeDiv.style.display = 'flex'
    e.stopPropagation()
})
window.addEventListener('click',(e)=>{
    if(e.target != changeDiv){
        changeDiv.style.display = 'none'
    }
})