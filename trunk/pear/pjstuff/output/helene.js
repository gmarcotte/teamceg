/****************************************************************************************
	Helene 0.9
	Syntax Highlighting Textarea replacement with tab support and linenumbers
	Copyright (C) 2004 - 2005 Muze (http://www.muze.nl/)

	This library is free software; you can redistribute it and/or
	modify it under the terms of the GNU Lesser General Public
	License as published by the Free Software Foundation; either
	version 2.1 of the License, or (at your option) any later version.

	This library is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
	Lesser General Public License for more details.

	You should have received a copy of the GNU Lesser General Public
	License along with this library; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

	You can contact Muze through email at info@muze.nl, for snailmail use

		Muze
		Piet Heinstraat 13
		7511JE Enschede
		the Netherlands

	---------------------------------------------------------------------------------
	TODO:
	- replace tabs with spaces in input textarea, since IE has a fixed width of 64px
	  for tabs, instead of 8*letterWidth. And if we're doing that anyway, make tab
	  size configurable.
	- fix grow / add shrink for long inputlines
	- selections
	- undo/redo
	- copy/paste multiple lines
	- highlighting
	- fix onfocus stuff for textarea
	- create an option to let tabs switch between textarea's/helene's, and/or provide
	  an alternative key (shift-tab? ctrl-tab?)
	- allways show the linenumbers
	- fix onchange stuff for reloading


	Short API for Helene:
	---------------------------------------------------------------------------------	
	TEXTAREA.helene						instance of the helene editor
		.source			reference to the original textarea
		.keyboard		contains all current keyboard bindings

		.copy()	
		.cut()	
		.doBackspace()
		.doDelete()
		.insertLinebreak()
		.insertTab()
		.paste()
		.redo()
		.select()
		.undo()

	TEXTAREA.helene.canvas				DIV: contains the editor widget
		.editor			reference to the helene editor
		.letterWidth	
		.borderWidth

	TEXTAREA.helene.canvas.content		OL: contains the editor content (lines)
		.editor 		reference to the helene editor
		.maxLineLength
		.length

		.clearContent()
		.getLetterWidth()
		.getLine()
		.init()
		.setContent()
		.setLine()

	TEXTAREA.helene.canvas.content.line LI: contains a single line of content
		.editor			reference to the helene editor
		.length
		.source
		
		.init()
		.setContent()

	TEXTAREA.helene.canvas.input		TEXTAREA: the yellow input line
		.editor 		reference to the helene editor
		.line			current line
		.column			real column position, only valid immediately after setPos or getPos
		.character		character position, idem

		.apply()
		.getPos()
		.hide()
		.init()
		.isDirty()
		.reset()
		.setPos()
		.show()

	TEXTAREA.helene.cursor				cursor object to keep track of real and virtual
										position of the cursor and selections
		.editor 		reference to the helene editor

		.getPos()
		.getRealPos()		returns a position object of the real cursor location
		.up()
		.down()
		.left()
		.right()
		.home()
		.end()
		.top()
		.bottom()
		.pageUp()
		.pageDown()
		.setPos()			moves the cursor to the virtual position, the real one may differ (tabs)
		.setRealPos()		moves the cursor, and changes the virtual position to the real one
		.wordRight()
		.wordLeft()

	TEXTAREA.helene.selection
		.editor 		reference to the helene editor
		.start			start position
		.end			end position

		.select(start, end)
		.moveStart(start)
		.moveEnd(end)
		.clear()

	helene.position
		.line
		.column
		.character
		.compare()
***************************************************************************************************/

var helene={

	options:{
		css:'./helene.css',
		tabSize:4,
		pageSize:20,
		autoIndent:true
	},

	config:{
		isMoz:(window.navigator.product=='Gecko'),
		undo:{
			CHANGE_TEXT:1,
			APPEND_LINE:2,
			DELETE_LINE:3
		}
	},

	// load other javascripts
	load:function(url) {
		var dochead		= document.getElementsByTagName("head").item(0);
		var scriptOb	= document.createElement("script");
		scriptOb.setAttribute("type", "text/javascript");
		scriptOb.setAttribute("src", url);
		dochead.appendChild(scriptOb);
	},

	// event contains all the code necessary to make IE and Mozilla play nice with events
	event:{
		cache:[],
		get:function(evt) {
			if (!evt) {
				evt=window.event;
			}
			if (!evt.target) {
				evt.target=evt.srcElement;
			}
			return evt;
		},
		cancel:function(evt) {
			if (evt.returnValue) {
				evt.returnValue=false;
			} 
			if (evt.preventDefault) {
				evt.preventDefault();
			}
			evt.cancelBubble=true;
			if (evt.stopPropagation) {
				evt.stopPropagation();
			}
			return false;
		},
		pass:function(evt) {
			return true;
		},
		attach:function(ob, event, fp, useCapture) {
			function createHandlerFunction(obj, fn){
				// FIXME: remember handler function somewhere so we can unattach it on unload
				// perhaps remember all events per object, so you can also specifically unattach
				// events for a specific object
				var o = new Object;
				o.myObj = obj;
				o.calledFunc = fn;
				o.myFunc = function(e){ 
					var e = helene.event.get(e);
					return o.calledFunc.call(o.myObj, e);
				}
				return o.myFunc;
			}
			var handler=createHandlerFunction(ob, fp);
			helene.event.cache[helene.event.cache.length]={ event:event, object:ob, handler:handler };
			if (ob.addEventListener){
				ob.addEventListener(event, handler, useCapture);
				return true;
			} else if (ob.attachEvent){
				return ob.attachEvent("on"+event, handler);
			} else {
				//FIXME: don't do alerts like this
				alert("Handler could not be attached");
			}
		},
		clean:function() {
			var item=null;
			for (var i=helene.event.cache.length-1; i>=0; i--) {
				item=helene.event.cache[i];
				item.object['on'+item.event]=null;
				if (item.object.removeEventListener) {
					item.object.removeEventListener(item.event, item.handler, item.useCapture);
				} else if (item.object.detachEvent) {
					item.object.detachEvent("on" + item.event, item.handler);
				}
				helene.event.cache[i]=null;
			}
			item=null;
		}
	},
	
	// attach is the method that actually instantiates a new editor and attaches
	// it to the 'source' textarea
	attach:function(value) {
		value.helene=new helene.editor(value);
	},

	// this is the default helene initialization method, which
	// inserts the helene stylesheet and attaches helene editors
	// on each textarea with class 'helene' set.
	init:function() {
    alert("helene being called.");
		helene.util.createStyleSheet(helene.options.css);

		// attach helene to any textarea with class 'helene'
		var textareas=document.getElementsByTagName('TEXTAREA');
		var length=textareas.length;

		// this array is needed to prevent mozilla from silently 
		// changing the array while you add textareas to the 
		// document.
		var mozillasucks=new Array();
		for (var i=0; i<length; i++) {
			mozillasucks[i]=textareas[i];
		}
		for (var i=0; i<length; i++) {
			if (mozillasucks[i].className.match(/(.*helene.*)/)) {
				helene.attach(mozillasucks[i]);
			}
		}		
	}
}

helene.load('helene.util.js');
helene.load('helene.position.js');
helene.load('helene.keyboard.js');
helene.load('helene.mouse.js');
helene.load('helene.editor.js');
helene.load('helene.canvas.js');
helene.load('helene.input.js');
helene.load('helene.content.js');
helene.load('helene.line.js');
helene.load('helene.cursor.js');
helene.load('helene.selection.js');

helene.event.attach(window, 'load', helene.init);
helene.event.attach(window, 'unload', helene.event.clean);
