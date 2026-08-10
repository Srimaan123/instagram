let socketio = io()
socketio.on('connect', () => {
    console.log(1)
})
let sugglist = document.querySelector(".sugglist")
let search = document.querySelector(".search")
let clear = document.querySelector(".clear")
clear.addEventListener("click", () => {
    search.value = ""
})

search.addEventListener("input", (e) => {
    sugglist.innerHTML = ""
    if (e.target.value != "") {
        socketio.emit("search", { "text": e.target.value, "username": document.querySelector("#username").textContent })
    }
})

socketio.on("search_result", (data) => {

    for (let i = 0; i < data.users.length; i++) {
        const element = data.users[i];
        console.log(element)
        let account = document.createElement("div")
        account.setAttribute("class", "flex gap-2 relative")
        account.setAttribute("id", element)
        let profilepic = document.createElement("img")
        profilepic.setAttribute("class", "w-12 h-12 rounded-full bg-green-200")
        let h1 = document.createElement("h1")
        h1.setAttribute("class", "text-[16px] text-black font-['inter'] font-bold pt-1")
        h1.textContent = element
        let followbtn = document.createElement("button")
        if (data.is_followed == 'True') {
            followbtn.textContent = 'following'
            followbtn.setAttribute("class", " text-black font-md bg-[var(--bg-color)] border-2 border-gray-200 rounded-xl p-2 inline-block absolute right-0")
        }
        else if (data.is_requested[i] == 'True') {
            followbtn.textContent = 'requested'
            followbtn.setAttribute("class", " text-black font-md bg-[var(--bg-color)] border-2 border-gray-200 rounded-xl p-2 inline-block absolute right-0")
        } else {
            followbtn.textContent = 'follow'
            followbtn.setAttribute("class", " text-white font-md bg-[var(--insta-blue)] rounded-xl p-2 inline-block absolute right-0")
        }
        followbtn.addEventListener("click", () => {
            if (data.is_requested[i] == 'False') {
                socketio.emit("request", { requested_by: document.querySelector("#username").textContent, requested_to: element })
                data.is_requested[i] = 'True'
            }
            else {
                socketio.emit("delete_request", { requested_by: document.querySelector("#username").textContent, requested_to: element })
                data.is_requested[i] = 'False'
            }
            console.log("hiii")
        })

        account.append(profilepic, h1, followbtn)
        sugglist.append(account)
    }
})

socketio.on("requested", (data) => {
    console.log("hello")
    followbtn = document.querySelector(`#${data.requested_to}`).querySelector("button")
    followbtn.textContent = 'requested'
    followbtn.setAttribute("class", " text-black font-md bg-[var(--bg-color)] border-2 border-gray-200 rounded-xl p-2 inline-block absolute right-0")
})
socketio.on("followed", (data) => {
    console.log("hello")
    followbtn = document.querySelector(`#${data.requested_to}`).querySelector("button")
    followbtn.textContent = 'following'
    followbtn.setAttribute("class", " text-black font-md bg-[var(--bg-color)] border-2 border-gray-200 rounded-xl p-2 inline-block absolute right-0")
})
socketio.on("unfollowed", (data) => {
    followbtn = document.querySelector(`#${data.unfollowed_to}`).querySelector("button")
    followbtn.textContent = 'follow'
    followbtn.setAttribute("class", " text-white font-md bg-[var(--insta-blue)] rounded-xl p-2 inline-block absolute right-0")
})