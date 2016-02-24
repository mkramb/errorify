var callback = (typeof errorify !== "undefined") ? window.errorify.callback : null;
var data = (typeof errorify !== "undefined") ? window.errorify.data : [];

window.errorify = {

	data: [],
		
    log: function(ex, resourceId, position, url) {

		var data = {
		    client : {
		        cookieEnabled : navigator.cookieEnabled,
		        language : navigator.language,
		        url : (typeof position === 'undefined') ? window.location.toString() : url
		    },
		    position : (typeof position !== 'undefined') ? position : [],
		    stacktrace : this.compute(ex)
		};
    	
        this.send(data, resourceId);
    	
    },
    
    track: function() {

    	window.setInterval(function() {
    		var data = window.errorify.data;
    		
    		if (data.length > 0 && data.shift) {
    			var values = data.shift();
    			var message = values[0].split(':', 2);
    			
    			window.errorify.log({
            		'name' : message[0],
            		'message' : message[1],
            		'stack' : null
        		}, null, [values[2]], values[1]);
    		}
    	}, 1000);

    },

    compute: function(ex) {
    	
        if (!ex.stack && !ex.message) {
            return ex;
        }

        var stack = [];

        if (ex.stack) {
            var chrome_re = /((?:file|http):.*?):(\d+)(?::(\d+))/i,
            	gecko_re = /@((?:file|http).*?):(\d+)\s*$/i;

            var lines = ex.stack.split("\n"), 
            	parts, element;

            for ( var i = 0, j = lines.length; i < j; ++i) {
                if (parts = chrome_re.exec(lines[i])) {
                    element = {
                        'url' : parts[1],
                        'line' : +parts[2],
                        'column' : parts[3] ? +parts[3] : null
                    };
                } else if ((parts = gecko_re.exec(lines[i]))) {
                    element = {
                        'url' : parts[1],
                        'line' : +parts[2]
                    };
                } else {
                    continue;
                }

                stack.push(element);
            }

            if (!stack.length) {
                return null;
            }
        }

        return {
            'name' : ex.name,
            'message' : ex.message,
            'stack' : stack
        };
        
    },
    
	send: function(data, resourceId) {
		
        if (typeof this.key === 'undefined') {
            throw new Error('errorify: no api key provided');
        }
		
        var url = "{{ PROJECT_URL }}{% url app_api_log %}?key=" + this.key, 
        	script = document.createElement("script");

        if (resourceId) {
        	url += "&resourceId=" + resourceId;
        }
        
        url += "&payload=";
        
        data = (typeof JSON !== 'undefined' && typeof JSON.stringify === 'function') ?
    		JSON.stringify(data) : this.serializer.stringify(data);

        script.setAttribute('src', url + encodeURIComponent(data));
        document.getElementsByTagName('head')[0].appendChild(script);

        if (typeof this.callback === "function") {
            this.callback();
        }
        
	},
    
    serializer: {

        gap : null,
        indent : null,
        repr : null,
        escapable : /[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,

        stringify : function(value, replacer, space) {
            var i;

            this.gap = '';
            this.indent = '';

            if (typeof space === 'number') {
                for (i = 0; i < space; i += 1) {
                    this.indent += ' ';
                }
            } else if (typeof space === 'string') {
                this.indent = space;
            }

            this.rep = replacer;

            if (replacer && typeof replacer !== 'function' && (typeof replacer !== 'object' || typeof replacer.length !== 'number')) {
                throw new Error('JSON.stringify');
            }

            return this.str('', {
                '' : value
            });
        },

        str : function(key, holder) {
            var i, k, v, length, mind = this.gap, partial, value = holder[key];

            if (value && typeof value === 'object'
                    && typeof value.toJSON === 'function') {
                value = value.toJSON(key);
            }

            if (typeof this.rep === 'function') {
                value = this.rep.call(holder, key, value);
            }

            switch (typeof value) {
                case 'string':
                    return this.quote(value);
                case 'number':
                    return isFinite(value) ? String(value) : 'null';
                case 'boolean':
                case 'null':
                    return String(value);
                case 'object':
                    if (!value) {
                        return 'null';
                    }

                    this.gap += this.indent;
                    partial = [];

                    if (Object.prototype.toString.apply(value) === '[object Array]') {
                        length = value.length;

                        for (i = 0; i < length; i += 1) {
                            partial[i] = this.str(i, value) || 'null';
                        }

                        v = partial.length === 0 ? '[]' : this.gap ?
                            '[\n' + this.gap + partial.join(',\n' + this.gap) + '\n' + mind + ']' :
                            '[' + partial.join(',') + ']';

                        this.gap = mind;
                        return v;
                    }

                    if (this.rep && typeof this.rep === 'object') {
                        length = this.rep.length;
                        
                        for (i = 0; i < length; i += 1) {
                            if (typeof this.rep[i] === 'string') {
                                k = this.rep[i];
                                v = this.str(k, value);
                                if (v) {
                                    partial.push(this.quote(k)
                                            + (this.gap ? ': ' : ':') + v);
                                }
                            }
                        }
                    }
                    else {
                        for (k in value) {
                            if (Object.prototype.hasOwnProperty.call(value, k)) {
                                v = this.str(k, value);
                                if (v) {
                                    partial.push(this.quote(k)
                                            + (this.gap ? ': ' : ':') + v);
                                }
                            }
                        }
                    }

                    v = partial.length === 0 ? '{}' : this.gap ? 
                        '{\n' + this.gap + partial.join(',\n' + this.gap) + '\n' + mind + '}' :
                        '{' + partial.join(',') + '}';

                    this.gap = mind;
                    return v;
            }
        },

        quote : function(string) {
            this.escapable.lastIndex = 0;

            return this.escapable.test(string) ? '"' + string.replace(this.escapable, function(a) {
                var c = meta[a];

                return typeof c === 'string' ?
                    c : '\\u' + ('0000' + a.charCodeAt(0).toString(16)).slice(-4);
            }) + '"' : '"' + string + '"';
        }

    }
	
}

if (data.length > 0 && data.shift) {
	errorify.key =  data.shift();
}

if (callback) {
	errorify.callback = callback;
}

errorify.track();
