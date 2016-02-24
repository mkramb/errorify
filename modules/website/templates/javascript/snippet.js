(function (win, doc, key) {
	win.errorify = { data:[key], log: function(){ this.data.push(arguments) } }, win.onerror = function () { win.errorify.data.push(arguments); };
    var a = doc.createElement("script"); a.type = "text/javascript"; a.src="{{ PROJECT_URL }}/core.js"; a.async = !0; 
    var b = doc.getElementsByTagName("script")[0]; b.parentNode.insertBefore(a, b); 
})(window, document, "NWIzM2U3Y2MtZTk3Zi0xMWUxLWFkMjYtN2NkMWMzZTJhMDg3");
