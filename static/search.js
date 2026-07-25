let socketio = io()
socketio.on('connect',()=>{
    console.log(1)
})
let sugglist = document.querySelector(".sugglist")
let search = document.querySelector(".search")

search.addEventListener("input",(e)=>{
    sugglist.innerHTML = ""
    if (e.target.value != ""){
        socketio.emit("search",{"text": e.target.value,"uername": document.querySelector("#username").textContent})
    }
})

socketio.on("search_result",(data)=>{

    for (let i = 0; i < data.users.length; i++) {
        const element = data.users[i];
        
        let account = document.createElement("div")
        account.setAttribute("class","flex gap-1")
        let profilepic = document.createElement("img")
        profilepic.setAttribute("class","w-12 h-12 rounded-full bg-green-200")
        let h1 = document.createElement("h1")
        h1.setAttribute("class","text-[16px] text-black font-['fredoka'] font-md pt-1")
        h1.textContent = element
        let followbtn = document.createElement("button")
        if (data.is_requested == 'True'){
            followbtn.textContent = 'requested'
        }else{
            followbtn.textContent = 'follow'
        }
        
        account.append(profilepic,h1,followbtn)
        sugglist.append(account)
    }
})