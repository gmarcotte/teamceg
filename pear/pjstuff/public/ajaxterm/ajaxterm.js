ajaxterm={};
ajaxterm.Terminal_ctor=function(id,width,height,ssh,user,update_url,key,term_id) {
  window.isDriver=true;
	var ie=0;
	if(window.ActiveXObject)
		ie=1;
	//var sid=term_id; // 
	window.sid=term_id;
  window.width = width;
  window.height = height;
  window.ssh = ssh;
  window.user = user;
  window.update_url = update_url;
  window.key = key;
  //window.query0suf="&w="+width+"&h="+height+"&ssh="+ssh+"&user="+user+"&key="+key;
  window.query0="s="+window.sid+"&w="+window.width+"&h="+window.height+"&ssh="+window.ssh+"&user="+window.user+"&key="+window.key;
  //var query0="s="+window.sid+"&w="+width+"&h="+height+"&ssh="+ssh+"&user="+user+"&key="+key;
	window.query1=window.query0+"&c=1&k=";
  //var query1=window.query0+"&c=1&k=";
	var buf="";
	var timeout;
	var error_timeout;
	var keybuf=[];
	var sending=0;
	var rmax=1;

	var div=document.getElementById(id);
	var dstat=document.createElement('pre');
	var sled=document.createElement('span');
	var opt_get=document.createElement('a');
	var opt_color=document.createElement('a');
	var opt_paste=document.createElement('a');
	var sdebug=document.createElement('span');
	var dterm=document.createElement('div');

	// these might not actually work cci
	/*function setSID(s) {
		sid = s;
		query0="s="+sid+"&w="+width+"&h="+height+"&ssh="+ssh+"&user="+user+"&key="+key;
		query1=query0+"&c=1&k=";
		
	}
	function set_driver(s) {
		isdriver = s;
		alert(isdriver);
	}*/
	//
	
	function debug(s) {
		sdebug.innerHTML=s;
	}
	function error() {
		sled.className='off';
		debug("Connection lost timeout ts:"+((new Date).getTime()));
	}
	function opt_add(opt,name) {
		opt.className='off';
		opt.innerHTML=' '+name+' ';
		dstat.appendChild(opt);
		dstat.appendChild(document.createTextNode(' '));
	}
	function do_get(event) {
		opt_get.className=(opt_get.className=='off')?'on':'off';
		debug('GET '+opt_get.className);
	}
	function do_color(event) {
		var o=opt_color.className=(opt_color.className=='off')?'on':'off';
		if(o=='on')
			query1=window.query0+"&c=1&k=";
		else
			query1=window.query0+"&k=";
		debug('Color '+opt_color.className);
	}
	function mozilla_clipboard() {
		 // mozilla sucks
		try {
			netscape.security.PrivilegeManager.enablePrivilege("UniversalXPConnect");
		} catch (err) {
			debug('Access denied, <a href="http://kb.mozillazine.org/Granting_JavaScript_access_to_the_clipboard" target="_blank">more info</a>');
			return undefined;
		}
		var clip = Components.classes["@mozilla.org/widget/clipboard;1"].createInstance(Components.interfaces.nsIClipboard);
		var trans = Components.classes["@mozilla.org/widget/transferable;1"].createInstance(Components.interfaces.nsITransferable);
		if (!clip || !trans) {
			return undefined;
		}
		trans.addDataFlavor("text/unicode");
		clip.getData(trans,clip.kGlobalClipboard);
		var str=new Object();
		var strLength=new Object();
		try {
			trans.getTransferData("text/unicode",str,strLength);
		} catch(err) {
			return "";
		}
		if (str) {
			str=str.value.QueryInterface(Components.interfaces.nsISupportsString);
		}
		if (str) {
			return str.data.substring(0,strLength.value / 2);
		} else {
			return "";
		}
	}
	function do_paste(event) {
		var p=undefined;
		if (window.clipboardData) {
			p=window.clipboardData.getData("Text");
		} else if(window.netscape) {
			p=mozilla_clipboard();
		}
		if (p) {
			debug('Pasted');
			queue(encodeURIComponent(p));
		} else {
		}
	}
	function update() {
//		debug("ts: "+((new Date).getTime())+" rmax:"+rmax);
		if(sending==0) {
			sending=1;
			sled.className='on';
			var r=new XMLHttpRequest();
			var send="";
			while(keybuf.length>0) {
				send+=keybuf.pop();
			}
			var query=query1+send;
      //alert(query);
			if(opt_get.className=='on') {
				r.open("GET",update_url+"u?"+query,true);
				if(ie) {
					r.setRequestHeader("If-Modified-Since", "Sat, 1 Jan 2000 00:00:00 GMT");
				}
			} else {
				r.open("POST",update_url+"u",true);
			}
			r.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
			r.onreadystatechange = function () {
//				debug("xhr:"+((new Date).getTime())+" state:"+r.readyState+" status:"+r.status+" statusText:"+r.statusText);
				if (r.readyState==4) {
					if(r.status==200) {
						window.clearTimeout(error_timeout);
						de=r.responseXML.documentElement;
						if(de.tagName=="pre") {
							if(ie) {
								Sarissa.updateContentFromNode(de, dterm);
							} else {
								Sarissa.updateContentFromNode(de, dterm);
//								old=div.firstChild;
//								div.replaceChild(de,old);
							}
							rmax=100;
						} else {
							rmax*=2;
							if(rmax>2000)
								rmax=2000;
						}
						sending=0;
						sled.className='off';
						timeout=window.setTimeout(update,rmax);
					} else {
						debug("Connection error status:"+r.status);
					}
				}
			}
			error_timeout=window.setTimeout(error,5000);
			if(opt_get.className=='on') {
				r.send(null);
			} else {
				r.send(query);
			}
		}
	}
	function queue(s) {
		keybuf.unshift(s);
		if(sending==0) {
			window.clearTimeout(timeout);
			timeout=window.setTimeout(update,1);
		}
	}

	function keypress(ev) {
    // this is necessary to make sure that we don't steal from chat
    var focusElement = document.activeElement;
    if (focusElement.id == "MYchatID") {
      return true;
    }
		//alert(query1);
    
		if (window.isDriver.toString() == 'false') {
			//alert("Passenger, not sending keypress");
			return true;
		}
		
    if (!ev) var ev=window.event;
		var kc;
		var k="";
		if (ev.keyCode)
			kc=ev.keyCode;
		if (ev.which)
			kc=ev.which;

    if (ev.altKey) { // was formerly if
			if (kc>=65 && kc<=90)
				kc+=32;
			if (kc>=97 && kc<=122) {
				k=String.fromCharCode(27)+String.fromCharCode(kc);
			}
		} else if (ev.ctrlKey) {
			if (kc>=65 && kc<=90) k=String.fromCharCode(kc-64); // Ctrl-A..Z
			else if (kc>=97 && kc<=122) k=String.fromCharCode(kc-96); // Ctrl-A..Z
			else if (kc==54)  k=String.fromCharCode(30); // Ctrl-^
			else if (kc==109) k=String.fromCharCode(31); // Ctrl-_
			else if (kc==219) k=String.fromCharCode(27); // Ctrl-[
			else if (kc==220) k=String.fromCharCode(28); // Ctrl-\
			else if (kc==221) k=String.fromCharCode(29); // Ctrl-]
			else if (kc==219) k=String.fromCharCode(29); // Ctrl-]
			else if (kc==219) k=String.fromCharCode(0);  // Ctrl-@
		} else if (ev.which==0) {
			if (kc==9) k=String.fromCharCode(9);  // Tab
			else if (kc==8) k=String.fromCharCode(127);  // Backspace
			else if (kc==27) k=String.fromCharCode(27); // Escape
      else {
				if (kc==33) k="[5~";        // PgUp
				else if (kc==34) k="[6~";   // PgDn
				else if (kc==35) k="[4~";   // End
				else if (kc==36) k="[1~";   // Home
				else if (kc==37) k="[D";    // Left
				else if (kc==38) k="[A";    // Up
				else if (kc==39) k="[C";    // Right
				else if (kc==40) k="[B";    // Down
				else if (kc==45) k="[2~";   // Ins
				else if (kc==46) k="[3~";   // Del
				else if (kc==112) k="[[A";  // F1
				else if (kc==113) k="[[B";  // F2
				else if (kc==114) k="[[C";  // F3
				else if (kc==115) k="[[D";  // F4
				else if (kc==116) k="[[E";  // F5
				else if (kc==117) k="[17~"; // F6
				else if (kc==118) k="[18~"; // F7
				else if (kc==119) k="[19~"; // F8
				else if (kc==120) k="[20~"; // F9
				else if (kc==121) k="[21~"; // F10
				else if (kc==122) k="[23~"; // F11
				else if (kc==123) k="[24~"; // F12
				if (k.length) {
					k=String.fromCharCode(27)+k;
				}
			}
		} else {
			if (kc==8)
				k=String.fromCharCode(127);  // Backspace
			else
				k=String.fromCharCode(kc);
		}
		if(k.length) {
//			queue(encodeURIComponent(k));
			if(k=="+") {
				queue("%2B");
			} else {
				queue(escape(k));
			}
		}
		ev.cancelBubble=true;
		if (ev.stopPropagation) ev.stopPropagation();
		if (ev.preventDefault)  ev.preventDefault();
		return false;
	}
	function keydown(ev) {
    // handle when this tries to steal from chat
    var focusElement = document.activeElement;
    if (focusElement.id == "MYchatID") {
      return true;
    }
		if (window.isDriver.toString() == 'false') {
			//alert("Passenger, not sending keypress");
			return true;
		}
    // need to deal with non-ajaxterm calls... maybe here?
		if (!ev) var ev=window.event;
    // safari hack for dealing with non-printing keys
    // that are handled as modifiers
    if (!window.netscape) {
      if (ev.charCode == 63232) ev.keyCode=37;
      else if (ev.charCode == 63233) ev.keyCode=38;
      else if (ev.charCode == 63234) ev.keyCode=39;
      else if (ev.charCode == 63235) ev.keyCode=40;
      ev.which=0;
      return keypress(ev);
    }
		if (ie) {
//			s="kd keyCode="+ev.keyCode+" which="+ev.which+" shiftKey="+ev.shiftKey+" ctrlKey="+ev.ctrlKey+" altKey="+ev.altKey;
//			debug(s);
			o={9:1,8:1,27:1,33:1,34:1,35:1,36:1,37:1,38:1,39:1,40:1,45:1,46:1,112:1,
			113:1,114:1,115:1,116:1,117:1,118:1,119:1,120:1,121:1,122:1,123:1};
			if (o[ev.keyCode] || ev.ctrlKey || ev.altKey) {
				ev.which=0;
				return keypress(ev);
			}
		}
	}
	function init() {
		sled.appendChild(document.createTextNode('\xb7'));
		sled.className='off';
		dstat.appendChild(sled);
		dstat.appendChild(document.createTextNode(' '));
		opt_add(opt_color,'Colors');
		opt_color.className='on';
		opt_add(opt_get,'GET');
		opt_add(opt_paste,'Paste');
		dstat.appendChild(sdebug);
		dstat.className='stat';
		div.appendChild(dstat);
		div.appendChild(dterm);
		if(opt_color.addEventListener) {
			opt_get.addEventListener('click',do_get,true);
			opt_color.addEventListener('click',do_color,true);
			opt_paste.addEventListener('click',do_paste,true);
		} else {
			opt_get.attachEvent("onclick", do_get);
			opt_color.attachEvent("onclick", do_color);
			opt_paste.attachEvent("onclick", do_paste);
		}
		this.onkeypress=keypress; 
    this.onkeydown=keydown;
    // if we are the real terminal, set the update normally
    timeout=window.setTimeout(update,100);
		if (key.toString() == term_id.toString()) {
			window.isDriver = true;
		}
		else {
			window.isDriver = false;
		}
		return ajaxterm; // maybe this will let us keep the object in scope?
	}
	init();
}
ajaxterm.Terminal=function(id,width,height,ssh,user,update_url,key,term_id) {
	return new this.Terminal_ctor(id,width,height,ssh,user,update_url,key,term_id);
}
/*ajaxterm.setSID=function(s) {
	alert("here"); alert(window.sid);
	window.sid=s;
	alert(window.sid);
}*/
