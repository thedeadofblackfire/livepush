var isMSIE = /*@cc_on!@*/0;
var LivePush = new function() {
    this.channels = [];
    this.handlers = [];
    
    this.reconnect_delays = [1000, 2500, 5000, 10000, 30000, 60000];
    
    this.options = {
        // verbose?
        log: false,
        user: null,
        clientIdCookieName: "Push-ClientID",
    };

    this.connect = function(server, apikey, channels, options) {
        this.server = "http://" + server + "/connect";
        this.apikey = apikey;
        this.channels = channels;
        this.reconnect_tries = 0;        

        // merge options
        for (var attr in options) {
            this.options[attr] = options[attr];
        }
     
        if (!this.options.user) {
            this.options.user = this.readCookie(this.options.clientIdCookieName) || this.generateClientId();
        }
     
        this.user = this.options.user;

        this.makeConnection();
        
        // add stats
        this.log("User " + this.user + " Browser " + navigator.userAgent + " on " + navigator.platform + " platform");

        var that = this;
    };

    this.listen = function(handler) {
        this.log("New handler has been registered.");
        this.handlers.push(handler);
    };

    this.makeConnection = function() {
        var that = this;

        // make a connection
        this.socket = new SockJS(this.server, undefined, 
            {'debug': this.options.log});

        this.socket.onopen = function() {
            that.log("Connection has been estabilished.");

            // reset retries counter
            that.reconnect_tries = 0;

            // connect and subscribe to channels
            that.socket.send("CONNECT " + that.user + ":" + that.apikey);

            if (that.channels.length)
                that.socket.send("SUBSCRIBE " + that.channels.join(":"));
        }

        this.socket.onmessage = function(e) {
            that.log("Message has been received", e.data);

            try {
                // try to parse the message as json
                var json_data = JSON.parse(e.data);
                e.data = json_data;
            }
            catch(e) {
                // not json, leave it as is
            }

            for (var i = 0; i < that.handlers.length; i++) {
                that.handlers[i](e.data);
            }
        }

        this.socket.onclose = function(e) {
            that.log("Connection has been lost.");

            if (e.code == 9000 || e.code == 9001 || e.code == 9002) {
                // received "key not good" close message
                that.log("Reconnect supressed because of:", e);
                return;
            }

            var delay = that.reconnect_delays[that.reconnect_tries]
                || that.reconnect_delays[that.reconnect_delays.length - 1];

            that.log("Reconnecting in", delay, "ms...");
            that.reconnect_tries++;

            setTimeout(function() {
                that.makeConnection();
            }, delay);
        }
    };

    this.log = function(msg) {
        if (this.options.log
                && "console" in window && "log" in window.console) {

            if (arguments.length == 1) {
                console.log(arguments[0]);
            }
            else {
                if (isMSIE) {
                    var log = Function.prototype.bind.call(console.log, console);
                    log.apply(console, Array.prototype.slice.call(arguments));
                } else {
                    console.log.apply(console, Array.prototype.slice.call(arguments));
                }
            }
        }
    };
    
    /* extra feature for random user id using cookie */
    this.generateClientId = function () {
        var id = this.guid();               
        this.createCookie(this.options.clientIdCookieName, id, 6);        
        return id;
    };

    this.S4 = function () { return (((1+Math.random())*0x10000)|0).toString(16).substring(1); };    
    
    this.guid = function () { return (this.S4()+this.S4()+this.S4()+this.S4()+this.S4()); };
    
    this.createCookie = function (name, value, hours) {
        var expires = "";
        if (hours) {
            var date = new Date();
            date.setTime(date.getTime() + (hours * 60 * 60 * 1000));
            expires = "; expires=" + date.toGMTString();
        }
        document.cookie = name + "=" + value + expires + "; path=/";
        // console.log(document.cookie);
    };

    this.readCookie = function (name) {
        var nameEQ = name + "=";
        var ca = document.cookie.split(';');
        for (var i = 0; i < ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0) == ' ')
                c = c.substring(1, c.length);

            if (c.indexOf(nameEQ) == 0)
                return c.substring(nameEQ.length,c.length);
        }
        return null;
    };

    this.eraseCookie = function (name) {
        this.createCookie(name, "", -1);
    };
    
}