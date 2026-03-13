function sendMessage(){

let input = document.getElementById("chat-input")
let message = input.value

fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({message:message})
})
.then(res=>res.json())
.then(data=>{

let box = document.getElementById("chatbox")

box.innerHTML += "<p><b>You:</b> "+message+"</p>"
box.innerHTML += "<p><b>Bot:</b> "+data.reply+"</p>"

input.value=""

})

}