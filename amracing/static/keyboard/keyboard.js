//Based on PIN Pad Login Screen in JavaScript by dcode - https://codepen.io/dcode-software/pen/orXrXQ

class NumKeyboard {
    constructor ({el, fetchEndpoint, maxNumbers = 6}) {
        this.el = {
            main: el,
            numPad: el.querySelector(".pin-login__numpad"),
            textDisplay: el.querySelector(".pin-login__text"),
            
        };

        this.fetchEndpoint = fetchEndpoint;
        this.maxNumbers = maxNumbers;
        this.value = "";
        this.timestamp = "";
        this.first_digit = 0;

        this._generatePad();
    }

    _generatePad() {
        const padLayout = [
            "1", "2", "3",
            "4", "5", "6",
            "7", "8", "9",
            "\u2B05", "0", "\u2714"
        ];

        padLayout.forEach(key => {
            const insertBreak = key.search(/[369]/) !== -1;
            const keyEl = document.createElement("div");

            keyEl.classList.add("pin-login__key");
            keyEl.textContent = key;
            keyEl.addEventListener("click", () => { this._handleKeyPress(key) });
            this.el.numPad.appendChild(keyEl);

            if (insertBreak) {
                this.el.numPad.appendChild(document.createElement("br"));
            }
        });
        this.first_digit = true;
        this.el.textDisplay.value = "";

        this.el.textDisplay.addEventListener("keypress", (key) => { this._handleKeyboard(key) });
        
        if (document.getElementById("js-data").dataset.results == 0) {
            alert('This race has no start recorded\nRegister "000" to record start time')
        }
    }

    _handleKeyboard(kkey) {
        this._updateValueText();
        
        var keyCode = kkey.code;
        if (keyCode.substring(0,5) == "Digit") {
            if (this.first_digit == true) {
                var t = new Date(Date.now());
                this.timestamp = t;
                this.first_digit = false;            }
        } else if (keyCode == 'Enter') {
            this.value = this.el.textDisplay.value;
            this._recordTime();

        } else if (keyCode == 'Backspace') {this.el.textDisplay.classList.remove("pin-login__text--error");}
        else {
            this.el.textDisplay.classList.add("pin-login__text--error");
        }
    }

    _handleKeyPress(key) {
        switch (key) {
            case "\u2B05": //backspace
                this.el.textDisplay.value = this.el.textDisplay.value.substring(0, this.el.textDisplay.value.length - 1);
                break;
            case "\u2714": //confirm
                this.value = this.el.textDisplay.value;
                this._recordTime();
                break;
            default:

                if (this.el.textDisplay.value.length < this.maxNumbers && !isNaN(key)) {
                    this.el.textDisplay.value += key;

                    if (this.first_digit == true) {
                        var t = new Date(Date.now());
                        this.timestamp = t;
                        this.first_digit = false;
                    }
                }
                break;
        }
        this._updateValueText();
    }

    _updateValueText() {
        this.el.textDisplay.classList.remove("pin-login__text--error");
        this.el.textDisplay.classList.remove("pin-login__text--ok");

    }

    _recordTime() {
        if (this.value.length > 0) {
            fetch(this.fetchEndpoint, {
                method: "post",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": document.querySelector("input[name='csrfmiddlewaretoken']").value,

                },
                body: JSON.stringify({
                    "race_id": race_id,
                    "race_number": this.value,
                    "time":this.timestamp,
                })
            }).then(response => {
                if (response.status === 200) {
                    this.el.textDisplay.classList.add("pin-login__text--ok");
                    this.el.textDisplay.value = "";
                    this.first_digit = true;
                } else {
                    this.el.textDisplay.classList.add("pin-login__text--error");
                }
            })
        }
    }
}

race_id = document.getElementById("js-data").dataset.raceId;

new NumKeyboard({
    el: document.getElementById("mainPinLogin"),
    fetchEndpoint: `/results/new`,
});
