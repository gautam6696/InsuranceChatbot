// const container = document.querySelector('.chatbox_header')

ngrokurl = "http://127.0.0.1:5000"
// const style ={
//     top: 0,
//     left: 0,
//     width: '100%',
//     height: '100%',
//     position: 'fixed',
//     background: '#000'
// }

// const fireworks = new Fireworks(container, { intensity: 20 })
// console.log(fireworks)
//fireworks.start()

// fireworks.start()

// setTimeout( function(){fireworks.stop()},4000)
// fireworks.setOptions({ intensity: 1})

// after initialization you can change the fireworks parameters
// fireworks.setOptions({ delay: { min: 10, max: 15 }})

class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            //chipsbutton: document.querySelector('.chips_items')

        }

        //this.sendchips = this.sendchips.bind(this);
        this.state = false;
        this.messages = [];
        this.executed = false;
        this.chips = [];
        //var that = this;
        // this.exec = true;

    }

    display() {
        const { openButton, chatBox, sendButton } = this.args;

        openButton.addEventListener('click', () => this.toggleState(chatBox))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        //chipsbutton.addEventListener('click', () => this.onchipclick()) 

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({ key }) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;


        if (!this.executed) {
            fetch(ngrokurl + '/welcome', {
                method: 'POST',
                body: JSON.stringify({ message: "Welcome" }),
                mode: 'cors',
                headers: {
                    'Content-Type': 'application/json'
                },
            })
                .then(r => r.json())
                .then(r => {

                    // Object.values(r).forEach(value => {
                    // let msg2 = { name: "Nova", message: value};
                    // this.messages.push(msg2);
                    // this.updateChatText(chatbox)
                    // }
                    // );
                    Object.keys(r).forEach(key => {
                        if (key.includes("answer")) {

                            let msg2 = { name: "Nova", message: r[key] }
                            this.messages.push(msg2);
                            this.updateChatText(chatbox)

                        }
                    })

                })
            //console.log("Test")
            this.executed = true
        }

        // show or hides the box
        if (this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    

    onSendButton(chatbox) {
        this.chips = [];
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        // console.log(this.chipsbutton.innerHTML)
        // var chipvalue = chatbot.querySelector() 
        // console.log(chatbot.innerHTML)

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
        this.updateChatText(chatbox)
        textField.value = ''

        fetch(ngrokurl + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(r => r.json())
            .then(r => {

                Object.keys(r).forEach(key => {
                    
                    if (key.includes("answer")) {

                        let msg2 = { name: "Nova", message: r[key] }
                        this.messages.push(msg2);
                        //this.updateChatText(chatbox)

                    }
                    else {
                        let msg3 = { name: "Chips", message: r[key] }
                        this.chips.push(msg3);
                        //this.updateChatText(chatbox)
                    }
                    
                    

                }

                
                )
                this.updateChatText(chatbox);

                // Object.values(r).forEach(value => {
                // // console.log("Value")
                // // console.log("This is" + value);

                // let msg2 = { name: "Nova", message: value};
                // this.messages.push(msg2);
                // this.updateChatText(chatbox)
                // }
                // );
                textField.value = ''

            }).catch((error) => {
                console.error('Error:', error);
                this.updateChatText(chatbox)
                textField.value = ''
            });
    }



    // onchipclick(valuesr)
    // {
    //     console.log(valuesr)
    // }


    updateChatText(chatbox) {

        // onchipclick(valuesr)
        // {
        //     console.log(valuesr)
        // }
        var i = 0;
        var html = '';

        if (this.chips) {


            html += '<div class="chips_container">'
            this.chips.slice().forEach(function (item) {

                //divs = document.createElement("div");
                //divs.className = 'chips_container'
                html += '<button id="suggest' + i + '" class = "chips_items" type="button">' + item.message + '</button>';
                i = i + 1;



            })
            html += '</div>'
        };

        this.messages.slice().reverse().forEach(function (item, index) {
            if (item.name === "Nova") {
                if (item.message.includes("fit")) {

                    // fireworks.start()
                    // setTimeout( function(){fireworks.stop()}, 4000)

                    // This is being called twice. I dont know why so be careful
                    html += '<div class="messages__item specialmessages__item--operator">' + item.message + '</div>'
                    var chatheader = chatbox.querySelector('.chatbox__star--header')
                    //chatheader.style.transition = "all 2s";
                    chatheader.innerHTML = '<img class= Star src="../static/images/Twinklingstar.gif " alt="Star"> </img>'

                }
                else if (item.message.includes("has generally") || item.message.includes("need analysis")) {

                    html += '<div class="messages__item specialmessages__item--operator">' + item.message + '</div>'

                }

                else {

                    html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'

                }
            }
            else {

                if (item.message.includes("do not consume")) {
                    // this.exec = false;
                    //console.log("This is working"+ item.message)
                    html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
                    var chatheader = chatbox.querySelector('.chatbox__star--header2')
                    chatheader.innerHTML = '<img class= Star src="../static/images/Twinklingstar.gif " alt="Star2"> </img>'
                    // console.log(chatheader.innerHTML)
                }
                else {
                    html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
                }
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');


        //chatmessage.innerHTML = divs;
        chatmessage.innerHTML = html;
        // console.log("Hielekelfel");
        this.sendchips(chatbox);

        // var button1 = document.getElementById("suggest1");
        // if(button1){

        //     button1.onclick = function()
        //     {
        //         return button1.innerHTML; 
        //     };
        // }

        // button1 = docunetmgethd ajdn;
        // button1.addEventListener("click", 
        // );
    }

    sendchips(chatbox) {
        //this.sendchips.onclick = this.sendchips.bind(this);

        //this.messages = this.messages
        // onClick={(e) => this.handleClick(e)};

        var total_chips = document.getElementsByClassName('chips_items');
        //console.log(total_chips);

        if (total_chips.length > 0) {
            // extramsg = []
            //let msg2 = { name: "User", message: "This works how?" };
            //this.messages.push(msg2);
            //this.extraUpdateChatText(chatbox);

            //console.log(total_chips.length)
            //var total_chips = this.chips;
            for (var k = 0; k < total_chips.length; k++) {
                let single_chip = total_chips[k];
                console.log(single_chip.innerHTML)
                single_chip.addEventListener('click', () => {

                    this.onExtraSendButton(chatbox,single_chip.innerHTML);

                    // let msg2 = { name: "User", message: single_chip.innerHTML };
                    // this.messages.push(msg2);
                    // this.extraUpdateChatText(chatbox);

                    //console.log(single_chip.innerHTML);
                });

            }

        }
        // var button1 = document.getElementById("suggest1");
        // button1.onclick = function()
        // {
        //     return button1.innerHTML;
        // }


    }


    extraUpdateChatText(chatbox) {

        var html = '';

        this.messages.slice().reverse().forEach(function (item, index) {
            if (item.name === "Nova") {

                    html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'

            }
            else {
               
                    html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
    
            }
        });

        const chatmessage = chatbox.querySelector('.chatbox__messages');

        chatmessage.innerHTML = html;
    }

    onExtraSendButton(chatbox,textvalue) {
        this.chips = [];
        var textField = chatbox.querySelector('input');
        let text1 = textvalue
        if (text1 === "") {
            return;
        }

        // console.log(this.chipsbutton.innerHTML)
        // var chipvalue = chatbot.querySelector() 
        // console.log(chatbot.innerHTML)

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
        this.updateChatText(chatbox)
        textField.value = ''

        fetch(ngrokurl + '/predict', {
            method: 'POST',
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(r => r.json())
            .then(r => {

                Object.keys(r).forEach(key => {
                    
                    if (key.includes("answer")) {

                        let msg2 = { name: "Nova", message: r[key] }
                        this.messages.push(msg2);
                        //this.updateChatText(chatbox)

                    }
                    else {
                        let msg3 = { name: "Chips", message: r[key] }
                        this.chips.push(msg3);
                        //this.updateChatText(chatbox)
                    }
                    
                    

                }

                
                )
                this.updateChatText(chatbox);

                // Object.values(r).forEach(value => {
                // // console.log("Value")
                // // console.log("This is" + value);

                // let msg2 = { name: "Nova", message: value};
                // this.messages.push(msg2);
                // this.updateChatText(chatbox)
                // }
                // );
                textField.value = ''

            }).catch((error) => {
                console.error('Error:', error);
                this.updateChatText(chatbox)
                textField.value = ''
            });
    }

}


const chatbox = new Chatbox();
chatbox.display();
