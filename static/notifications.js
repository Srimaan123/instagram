let content = document.querySelector(".content")
let socketio = io()

socketio.on("connect",()=>{
    console.log("connected successfully")
})

let following = document.querySelector(".following")
if (following.innerHTML == ""){
    following.stye.display = 'none'
}
let acceptBtns = document.querySelectorAll(".accept")
console.log(acceptBtns)
acceptBtns.forEach(btn => {
    btn.addEventListener("click",()=>{
        let parent = (btn.parentElement).parentElement
        let user = parent.querySelector(".name").textContent
        socketio.emit("accept_request",{"accepted_by":document.querySelector("#username").textContent,accepted_to:user})
    })
});
socketio.on("reload",()=>{
    window.location.reload()
})