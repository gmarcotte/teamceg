// editor is the core helene editor object
helene.editor = function(source) {
	var editor=this;
	this.source=source;
	this.canvas=helene.util.createElement('editorCanvas');
	// make sure the editor elements are in the document flow
	// before initializing them, so the browser will render them
	// and width/height of elements can be calculated
	this.source.parentNode.insertBefore(this.canvas, this.source);
	this.canvas.init(this);
	// load the content of the textarea
	this.canvas.content.setContent(this.source.value); 
	this.cursor=new helene.cursor(this);
	this.selection=new helene.selection(this);
	this.buffers={
		undo:new Array(),
		redo:new Array()
	}

	// editor methods
	this.save=function() {
		this.source.value=this.canvas.content.getContent();
	}
	this.doCleanState=function() {
		// do some cleaning up, clear up selections, etc.
		this.cursor.uptodate=false;
		return true;
	}
	this.insertTab=function() {
		var line = this.canvas.input.value;
		var pos = this.cursor.getRealPos();
    // CCI FIXED 4-16-09
    // do this 4 times to get a 4-space tab, etc.
    for (i = 0; i < helene.options.tabSize; i++) 
      line = line.substr(0,pos.character-1) + " " + line.substr(pos.character-1);
		this.canvas.input.value = line;
		this.cursor.setRealPos(pos.line, pos.column+helene.options.tabSize, true);
		return true;
	}
	this.insertLinebreak=function() {
		var pos=this.cursor.getRealPos();
		var head=this.canvas.input.value.substr(0, pos.character-1);
		var tail=this.canvas.input.value.substr(pos.character-1);
		var re = /([\t ]+)/;
		var match = re.exec(head);
		var newCursor = 1;
		if( helene.options.autoIndent && match ) {
			tail = match[1] + tail;
			if (match[1].length >= helene.options.tabSize-1)
        newCursor = helene.util.tabs.charPosToColumn(match[1].length+1, tail);
      else
        newCursor = helene.util.tabs.charPosToColumn(match[1].length, tail);
		}
		this.canvas.input.value=head;
		this.canvas.input.apply();
		this.canvas.content.appendLine(pos.line, tail);
		this.cursor.setPos(pos.line+1, newCursor);
	}
  // CCI FIXED 4-16-09
  // main problem was in setting the cursor position.
	this.doBackspace=function() {
    var line = this.canvas.input.value;
		var pos = this.cursor.getRealPos();
		if (pos.character>1) {
			line = line.substr(0, pos.character-2) + line.substr(pos.character-1);
			// first set the cursor to the new location, so it skips over tabs
			this.cursor.setRealPos(pos.line, pos.column-1);
			// then remember the cursor position
			pos=this.cursor.getPos();
			this.canvas.input.value=line;
			// now set the cursor back
			this.cursor.setRealPos(pos.line, pos.column);
		} else if (pos.line>1) {
			var prevLine=this.canvas.content.getLine(pos.line-1);
			this.cursor.setPos(pos.line-1, prevLine.length+1);
			// remove line only after the input has moved, otherwise the input will apply changes to the wrong line
			this.canvas.content.removeLine(pos.line);
			this.canvas.input.value+=line;
			// now set the cursor again, so its moved back from the end of the input
      var offset = this.canvas.input.value.length - line.length + 1;
			this.cursor.setPos(pos.line-1, offset);
		}		
	}
  
	this.doDelete=function() {
		var line = this.canvas.input.value;
		var pos = this.cursor.getRealPos();
		if (pos.character<=line.length) {
			// just remove a character
			line = line.substr(0, pos.character-1) + line.substr(pos.character);
			this.canvas.input.value=line;
			this.cursor.setPos(pos.line, pos.column);
		} 
    // fixed undefined over line break bug
    // CCI 4-23-09
    else if (pos.line<this.canvas.content.length) {
			// delete removes linebreak
      this.cursor.setPos(pos.line+1, 0);
			nextLine=this.canvas.input.value;
      this.cursor.setPos(pos.line,pos.column)
			this.canvas.input.value+=nextLine;
			this.canvas.content.removeLine(pos.line+1);
			this.cursor.setPos(pos.line, pos.column);				
		}
	}
	this.paste=function() {
	}
	this.copy=function() {
		var flashcopier = 'flashcopier';
		var text2copy = this.selection.getText();
		if(!document.getElementById(flashcopier)) {
			var divholder = document.createElement('div');
			divholder.id = flashcopier;
			this.canvas.appendChild(divholder);
		}
		document.getElementById(flashcopier).innerHTML = '';
		var divinfo = '<embed src="_clipboard.swf" FlashVars="clipboard='+escape(text2copy)+'" width="0" height="0" type="application/x-shockwave-flash"></embed>';
		document.getElementById(flashcopier).innerHTML = divinfo;
	}
	this.cut=function() {
	}
	this.undo=function() {
		if (this.canvas.input.isDirty()) {
			var redoElement={type:helene.config.undo.CHANGE_TEXT, text:this.canvas.content.getLine(this.cursor.line).source, newText:this.canvas.input.value, pos:this.cursor.getRealPos()}
			this.buffers.redo.push(redoElement); 
			this.canvas.input.value=this.canvas.content.getLine(this.cursor.line).source;
		} else if (this.buffers.undo.length) {
			var el=this.buffers.undo.pop();
			if (el) {
				switch(el.type) {
					case helene.config.undo.CHANGE_TEXT:
						this.canvas.input.value=el.text;
						this.cursor.setRealPos(el.pos.line, el.pos.column);
						this.buffers.redo.push({type:helene.config.undo.CHANGE_TEXT, text:el.newText, newText:el.text, pos:el.pos}); 
					break;
					case helene.config.undo.APPEND_LINE:
						this.canvas.content.removeLine(el.line);
						this.cursor.setRealPos(el.pos.line, el.pos.column);
						this.buffers.redo.push({type:helene.config.undo.DELETE_LINE, text:el.text, pos:el.pos});
					break;
					case helene.config.undo.DELETE_LINE:
						this.canvas.content.appendLine(el.pos.line-1, el.text);
						this.cursor.setRealPos(el.pos.line, el.pos.column);
						this.buffers.redo.push({type:helene.config.undo.APPEND_LINE, text:el.text, pos:el.pos});
					break;
					default:
					break;
				}
			}
		}
	}
	this.redo=function() {
		if (this.buffers.redo.length) {
			var el=this.buffers.redo.pop();
			if (el) {
				switch(el.type) {
					case helene.config.undo.CHANGE_TEXT:
						this.canvas.input.value=el.text;
						this.cursor.setRealPos(el.pos.line, el.pos.column);
						this.buffers.undo.push({type:helene.config.undo.CHANGE_TEXT, text:el.newText, newText:el.text, pos:el.pos}); 
					break;
					case helene.config.undo.APPEND_LINE:
						this.canvas.content.removeLine(el.line);
						this.cursor.setRealPos(el.pos.line, el.pos.column);
						this.buffers.undo.push({type:helene.config.undo.DELETE_LINE, text:el.text, pos:el.pos});
					break;
					case helene.config.undo.DELETE_LINE:
						this.canvas.content.appendLine(el.pos.line-1, el.text);
						this.cursor.setRealPos(el.pos.line, el.pos.column);
						this.buffers.undo.push({type:helene.config.undo.APPEND_LINE, text:el.text, pos:el.pos});
					break;
					default:
					break;
				}
			}
		}
	}
	this.keyboard=helene.keyboard.binding[helene.keyboard.behaviour](this);
	// now add onsubmit handler
	if (this.source.form) {
		helene.event.attach(this.source.form, 'submit', function() { editor.save(); });
	}
}
