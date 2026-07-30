let content = document.querySelector(".content")
let socketio = io()

socketio.on("connect",()=>{
    console.log("connected successfully")
})
socketio.on("notifications",(data)=>{
    if(data.follow_requests){
        followBox = document.createElement("div")
        followBox.setAttribute("class","border-2 border-gray-200 rounded-xl w-full p-2")
        content.append(followBox)
    }
})