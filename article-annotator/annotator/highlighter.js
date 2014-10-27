var prevElement = null;
var prevBrush = null;
var selectedBrush = "";
var selectedBrushElement = "";
var brushes = []

var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},decode:function(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(f<e.length){s=this._keyStr.indexOf(e.charAt(f++));o=this._keyStr.indexOf(e.charAt(f++));u=this._keyStr.indexOf(e.charAt(f++));a=this._keyStr.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}t=Base64._utf8_decode(t);return t},_utf8_encode:function(e){e=e.replace(/\r\n/g,"\n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t},_utf8_decode:function(e){var t="";var n=0;var r=c1=c2=0;while(n<e.length){r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r);n++}else if(r>191&&r<224){c2=e.charCodeAt(n+1);t+=String.fromCharCode((r&31)<<6|c2&63);n+=2}else{c2=e.charCodeAt(n+1);c3=e.charCodeAt(n+2);t+=String.fromCharCode((r&15)<<12|(c2&63)<<6|c3&63);n+=3}}return t}}

// Initialize toolbar
$(document).ready(function() {  
    var stickyNavTop = $('.nav').offset().top;  
      
    var stickyNav = function(){                 
        $('.nav').addClass('sticky'); 
    };  
      
    stickyNav();  
      
    $(window).scroll(function() {  
        stickyNav();  
    });  
});  

// When mousing over elements in the toolbar, highlight them with their respective colors
document.getElementById("palatte").addEventListener('mousemove',
    function(e){
        var elem = e.target || e.srcElement;
        if (prevBrush!= null) {
            prevBrush.classList.remove("annotated_" + prevBrush.innerHTML);
        }
        var brush = elem.innerHTML;
        elem.classList.add("annotated_" + brush)
        prevBrush = elem;
    },true);

// When mousing over elements in the htmlContent, highlight them
document.getElementById("htmlContent").addEventListener('mousemove',
    function(e){
        var elem = e.target || e.srcElement;
        if (prevElement!= null) {prevElement.classList.remove("mouseOn");}
        elem.classList.add("mouseOn");
        prevElement = elem;
    },true);

// Applying annotation to DOM element
document.getElementById("htmlContent").addEventListener('click',
	function(e){
        var elem = e.target || e.srcElement;
        elem.className = ""
        elem.setAttribute("annotation", selectedBrush);
        elem.classList.add("annotated_" + selectedBrush)
        console.log("Element", elem);
    },true);

// Clicking a new brush changes the selectedBrush
document.getElementById("palatte").addEventListener('click',
	function(e){
        var elem = e.target || e.srcElement;
        selectedBrush = elem.innerHTML;
        console.log("selectedBrush", selectedBrush);
        $('#selectedBrushText').html("Selected Brush: " + selectedBrush);
    },true);

// Save Resulting HTML
function saveHTML(){
	var html = $('html').clone();
	var htmlString = html.html();

	var datauri = "data:text/html;charset=utf-8;base64," + Base64.encode(htmlString);
	$("#toolbar").append("<a href='" + datauri + "'>Save</a>");
}

function removeStylesheets(){
    var css_links = $('#htmlContent link[rel=stylesheet]');
    console.log("CSS Links", css_links);
    css_links.remove();
}

$.get('http://localhost:8000/testEbola.html')
 .success(function(data) {
     $('#htmlContent').html(data);
 });