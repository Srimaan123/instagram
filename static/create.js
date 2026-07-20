let socket = io();

socket.on("connect",()=>{
	console.log("connected!!")
})

let password = document.querySelector(".password")
let username = document.querySelector(".username")
let btn = document.querySelector("button")
let is_valid_pass = false
let is_valid_username = false
password.addEventListener("input",(e)=>{
	if(e.target.value.length < 1){
		password.classList.add("border-gray-200")
		password.classList.remove("border-red-400")
		is_valid_pass = false
	}
	else if(e.target.value.length < 8){
		password.classList.add("border-red-400")
		password.classList.remove("border-gray-200")
		is_valid_pass = false

	}else{
		password.classList.add("border-gray-200")
		password.classList.remove("border-red-400")
		is_valid_pass = true
	}
})
let specials = [
    '@', '!', '#', '$', '%', '&', '*', '(', ')', '-', 
    '+', '=', '[', ']', '{', '}', ';', ':', ',', '.', '/', 
    '?', '\\', '|', '`', '~', '^', '<', '>', '"', "'",' '
];

username.addEventListener("input",(e)=>{
	let is_valid = true
	for(let i=0;i<specials.length;i++){
		if(e.target.value.includes(specials[i])){
			is_valid=false
		}
	}
	if(is_valid == true){
		username.classList.add("border-gray-200")
		username.classList.remove("border-red-400")
		is_valid_username = true
	}else{
		username.classList.add("border-red-400")
		username.classList.remove("border-gray-200")
		is_valid_username = false
	}
})

btn.addEventListener("click",()=>{
	socket.emit("add_account",{"username": username.value,"password": password.value,"mobile_number": document.querySelector(".mobile_number").value})
})

socket.on("user_added",(data)=>{
	alert("user added"+data.username)
})
socket.on("user_already_exists",(data)=>{
	alert("username is alerady taken")
})