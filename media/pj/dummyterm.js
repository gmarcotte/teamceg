/*
 dummyterm.js
 
 C Ilvento
 This is a significant re-write of ajaxterm.js (open source from Ajaxterm)
 which creates a dummy terminal whose body text can be set but that cannot
 directly communicate with another server. 
 */
dummyterm={};
dummyterm.Terminal_ctor=function(id,width,height) {
  var ie=0;
	if(window.ActiveXObject)
		ie=1;
	var sid=""+Math.round(Math.random()*1000000000);
	var query0="s="+sid+"&w="+width+"&h="+height;
	var query1=query0+"&c=1&k=";
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
			query1=query0+"&c=1&k=";
		else
			query1=query0+"&k=";
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
    /* THIS FUNCTION INTENTIONALLY LEFT BLANK*/
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
	}
	init();
  /*
   THIS IS ABSOLUTELY ESSENTIAL! DO NOT DELETE THIS LINE!
   In the original ajaxterm.js, nothing was actually returned here,
   so we had no way of holding onto the terminal object. By returning
   the dterm, we can communicate with the dummy terminal to set it's
   body contents through Sarissa.
   */
  return dterm;
}

/*Added by C Ilvento*/
/*This sets the body text of the dummy console.
 The dt passed in MUST be what was returned from dummyterm.Terminal(),
 and the de must be passed from ajaxterm.js from within a separate update.*/
dummyterm.setdummytext=function(dt, de) {
  Sarissa.updateContentFromNode(de, dt);
}

dummyterm.Terminal=function(id,width,height) {
	return new this.Terminal_ctor(id,width,height);
}



