let content = document.querySelector(".content")
let socketio = io()

socketio.on("connect",()=>{
    console.log("connected successfully")
})

let following = document.querySelector(".following")
if (following.innerHTML == ""){
    following.stye.display = 'none'
}