let search = document.querySelector(".search")
let container = document.querySelector(".accounts")
let username = document.querySelector("#username").textContent
let accounts = document.querySelectorAll(".account")

let socketio = io()

socketio.on("connect", () => {
    console.log("connected")
})

search.addEventListener("input", (e) => {
    let text = e.target.value
    if (text == "") {
        accounts.forEach(account => { account.style.display = 'flex' })
    } else {
        accounts.forEach(account => { account.style.display = 'none' })
        socketio.emit("search_account", { "text": text, "username": username })
    }

})
socketio.on("search_account_result", (data) => {
    console.log(data)
    for (let i = 0; i < data.users.length; i++) {
        const element = data.users[i];
        let account = document.querySelector(`#${element}`)
        console.log(account)
        account.style.display = "flex"
    }
})

let iframe = document.querySelector(".iframe-holder")
if (document.documentElement.clientWidth < 800) {
    iframe.style.display = 'none';
    document.querySelector(".screen").classList.add("w-full")
    document.querySelector(".screen").classList.remove("w-5/12")

}

accounts.forEach(account => {

    account.addEventListener("click", () => {
        account.querySelector(".new_badge").style.display = 'none'
        if (document.documentElement.clientWidth > 800) {
            let iframe = document.querySelector(".iframe-holder")
            iframe.style.display = 'flex'
            let iframe1 = document.querySelector(".iframe")
            iframe1.setAttribute("src", `/chat/${username}-${account.querySelector(".name").textContent}`)
        }
        
        else {
            window.location.href = `/chat/${username}-${account.querySelector(".name").textContent}`
        }

    })


})

window.addEventListener("DOMContentLoaded",()=>{
    console.log("asd")
    socketio.emit("check_new_messages",{"username": username})
})

socketio.on("new_messages_arrived",(data)=>{
    
    let senders = data.senders
    senders.forEach(sender=>{
        let account = document.querySelector(`#${sender}`)
        let newBadge = document.querySelector(".new_badge")
        newBadge.style.display = 'flex'

    })
})