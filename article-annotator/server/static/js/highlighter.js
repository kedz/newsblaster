var prevElement = null;
var prevBrush = null;
var previouslyAnnotatedElements = [];
var selectedBrush = "";
var brushes = []

var Base64={_keyStr:"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=",encode:function(e){var t="";var n,r,i,s,o,u,a;var f=0;e=Base64._utf8_encode(e);while(f<e.length){n=e.charCodeAt(f++);r=e.charCodeAt(f++);i=e.charCodeAt(f++);s=n>>2;o=(n&3)<<4|r>>4;u=(r&15)<<2|i>>6;a=i&63;if(isNaN(r)){u=a=64}else if(isNaN(i)){a=64}t=t+this._keyStr.charAt(s)+this._keyStr.charAt(o)+this._keyStr.charAt(u)+this._keyStr.charAt(a)}return t},decode:function(e){var t="";var n,r,i;var s,o,u,a;var f=0;e=e.replace(/[^A-Za-z0-9\+\/\=]/g,"");while(f<e.length){s=this._keyStr.indexOf(e.charAt(f++));o=this._keyStr.indexOf(e.charAt(f++));u=this._keyStr.indexOf(e.charAt(f++));a=this._keyStr.indexOf(e.charAt(f++));n=s<<2|o>>4;r=(o&15)<<4|u>>2;i=(u&3)<<6|a;t=t+String.fromCharCode(n);if(u!=64){t=t+String.fromCharCode(r)}if(a!=64){t=t+String.fromCharCode(i)}}t=Base64._utf8_decode(t);return t},_utf8_encode:function(e){e=e.replace(/\r\n/g,"\n");var t="";for(var n=0;n<e.length;n++){var r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r)}else if(r>127&&r<2048){t+=String.fromCharCode(r>>6|192);t+=String.fromCharCode(r&63|128)}else{t+=String.fromCharCode(r>>12|224);t+=String.fromCharCode(r>>6&63|128);t+=String.fromCharCode(r&63|128)}}return t},_utf8_decode:function(e){var t="";var n=0;var r=c1=c2=0;while(n<e.length){r=e.charCodeAt(n);if(r<128){t+=String.fromCharCode(r);n++}else if(r>191&&r<224){c2=e.charCodeAt(n+1);t+=String.fromCharCode((r&31)<<6|c2&63);n+=2}else{c2=e.charCodeAt(n+1);c3=e.charCodeAt(n+2);t+=String.fromCharCode((r&15)<<12|(c2&63)<<6|c3&63);n+=3}}return t}}

// When mousing over elements in the toolbar, highlight them with their respective colors
document.getElementById("palatte").addEventListener('mousemove',
    function(e){
        var elem = e.target || e.srcElement;
        if (prevBrush!= null) {
            prevBrush.classList.remove("annotated_" + prevBrush.innerHTML);
        }
        if (elem.innerHTML.indexOf('\n') < 1){
          var brush = elem.innerHTML;
          elem.classList.add("annotated_" + brush)
          prevBrush = elem;
        }
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

        previouslyAnnotatedElements.push(elem);

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

// Remove scripts + disable links
function sanitizeHTML(data){

    var strVal = data; //obviously, this line can be omitted - just assign your string to the name strVal or put your string var in the pattern.exec call below 
    var pattern = /<body[^>]*>((.|[\n\r])*)<\/body>/im
    var array_matches = pattern.exec(strVal);

    data = array_matches[1]

    data = data.replace(/<script[^>]*>/gi, ' <!-- ');
    data = data.replace(/<\/script>/gi, ' --> ');

    // Change all a's to a-disabled.
    data = data.replace(/<a[^>]*>/gi, '<a-disabled> ');
    data = data.replace(/<\/a>/gi, '</a-disabled>');

    return data;
}

function undo(){
  if(!(typeof previouslyAnnotatedElements[previouslyAnnotatedElements.length - 1] === 'undefined')){
    element = previouslyAnnotatedElements.pop();
    element.className="";
    element("annotation", "")
  };
}

function stripScripts(s) {
    console.log("Stripping javascript");

    var div = document.createElement('div');
    div.innerHTML = s;
    var scripts = div.getElementsByTagName('script');
    var i = scripts.length;
    while (i--) {
        console.log(scripts[i]);
        scripts[i].parentNode.removeChild(scripts[i]);
    }
    return div.innerHTML;
  }

function stripCSS(s) {
    console.log("Stripping CSS");

    var div = document.createElement('div');
    div.innerHTML = s;
    var css = div.getElementsByTagName('links');
    var i = css.length;
    while (i--) {
        console.log(scripts[i]);
        css[i].parentNode.removeChild(css[i]);
    }
    return div.innerHTML;
}

// Save Resulting HTML
function saveHTML(){
	var html = $('#htmlContent').clone();
    var htmlString = html.html();

  var cleanHTML = stripScripts(htmlString);

  var filename = $('#path').html();
  var end_idx = filename.indexOf(".html");
  filename = filename.substring(0,end_idx)

  data = {
    content: htmlString,
    filename: filename
  }

  console.log(data)

  var success = function(data){
    console.log("Success!")
    window.location=data
  }

  $.ajax({
    type: "POST",
    url: "http://localhost:5000/save/",
    data: data,
    success: success,
    dataType: "html"
  });
}

// Save Resulting HTML
function skip(){

  var filename = $('#path').html();
  var end_idx = filename.indexOf(".html");
  filename = filename.substring(0,end_idx)

  data = {
    filename: filename
  }

  var success = function(data){
    console.log("Success!")
    window.location=data
  }

  $.ajax({
    type: "POST",
    url: "http://localhost:5000/skip/",
    data: data,
    success: success,
    dataType: "html"
  });
}

// Manually remove all stylesheets
function removeStylesheets(){
    var css_links = $('#htmlContent link[rel=stylesheet]');
    console.log("CSS Links", css_links);
    css_links.remove();
}
