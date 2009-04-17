// input is the yellow input area, a textarea in disguise
helene.input = function() {
	this.className = 'hlInput';
	this.wrap = 'off';
	this.line = 1;
	this.length = 0;
	this.height = 1;
	this.minWidth = 0;
	this.grow = function(evt) {
		var cols = helene.util.tabs.charPosToColumn(this.value.length, this.value);
		var newwidth = (cols*this.editor.canvas.letterWidth)+1;
		if (newwidth>this.minWidth) {
			this.style.width = newwidth+'px';
			// FIXME: there should be another way to get the canvas to scroll to
			// the cursor position
			var pos = this.getPos();
			this.setPos(pos.line, pos.column, true);
		}
		evt = helene.event.get(evt);
		return helene.event.cancel(evt);			
	}

/*
	this.growHeight = function(n) {
		var pos = this.getPos();
		if (n>0) {
			var maxlength = this.editor.canvas.content.length - pos.line;
			if (n>maxlength) {
				n = maxlength;
			}
			// grow on bottom
			for (i=1; i<=n; i++) {
				var nextLine = this.editor.canvas.content.getLine(pos.line+i).getContent();
				this.value += '\n'+nexLine;
			}
			this.height+=n;
			// FIXME: get offset of last line, use that for height calculation
			this.style.height=(0.5+this.height)+'em';
		} else {
			// FIXME: save cursor position
			var maxlength = pos.line + n;
			if (maxlength - n <= 0) {
				n = 0 - maxlength;
			}
			// grow on top
			for (i=-1; i>=n; i--) {
				var prevLine = this.editor.canvas.content.getLine(pos.line+i).getContent();
				this.value = prevLine + '\n' + this.value;
			}
			this.height+=(-n);
			this.style.height=(0.5+this.height)+'em';
			// FIXME: reposition input, set cursor to original position
		}
	}

	this.shrinkHeight = function(n) {
		
	}
	
	this.resetHeight = function() {
		this.height=1;
	//	this.style.height = '1.5em';
	}
*/	
	this.init = function(editor) {
		this.editor = editor;
		this.style.fontFamily = this.editor.canvas.style.fontFamily;
		this.style.fontSize = this.editor.canvas.style.fontSize;
		this.style.color = this.editor.canvas.style.color;
		helene.event.attach(this, 'keydown', helene.keyboard.onKeyDown);
		helene.event.attach(this, 'keyup', helene.keyboard.onKeyUp);
		helene.event.attach(this, 'keypress', helene.keyboard.onKeyPress);
//			FIXME: growing shouldn't be done on scroll, but whenever the current
//			line grows larger than maxLineLength
//			also whenever the longest line shrinks, the reverse should be done
//			but never shrink the input line shorter than this.minWidth
		helene.event.attach(this, 'scroll', this.grow);
	}
	this.reset = function() {
		this.line = 1;
		this.style.top = '0px'; // CCI HERE IS THE PROBLEM (only for the first part, where does this get crappy?)
		this.value = this.editor.canvas.content.getLine(this.line).getContent();
		this.length = this.editor.canvas.content.getLine(this.line).getLength();
		var temp = parseInt(this.editor.canvas.content.getLine(this.line).offsetHeight);
		if (temp) {
			this.style.height = (temp)+'px'; // sets the height of the highlight... now just need the offset!
		}
		// calculating offsetWidth of the content doesn't work, since IE hasn't rendered it yet
		// so use the letterWidth and the maxLength instead.
		this.minWidth = this.editor.source.offsetWidth-(this.editor.canvas.borderWidth*2)-56;
		var maxWidth = this.editor.canvas.content.maxLineLength*this.editor.canvas.letterWidth;
		if (this.minWidth && maxWidth) {
			if (this.minWidth>maxWidth) {
				maxWidth = this.minWidth;
			} else {
				maxWidth+= 1; // make some room for the cursor in IE, there's a horizontal scrollbar anyway
			}
			this.style.width = maxWidth+'px';
		}
		this.show();
		this.focus();
		this.editor.canvas.scrollLeft = '0px';
	}
	this.hide = function() {
		this.style.visibility = 'hidden'; //display = 'none';
	}
	this.show = function() {
		this.style.visibility = 'visible'; //display = 'block';
	}
	this.apply = function() {
		if (this.isDirty()) {
			this.editor.canvas.content.setLine(this.line, this.value);
		}
	}
	this.isDirty = function() {
		return (this.editor.canvas.content.getLine(this.line).getContent()!=this.value);
	}
	this.getPos = function() {
		var input = this;
		function getCharacter() {
			// don't set the focus to the input line here, or the screen
			// will 'dance' around. Its not needed anyway.
			if (document.selection) {
				var cursor = document.selection.createRange();
				var fullRange = cursor.duplicate();
				fullRange.moveToElementText(input);
				cursor.setEndPoint('StartToStart', fullRange);
				var character = cursor.text.length;
			} else {
				var selection = window.getSelection();
				if (selection.anchorNode) {
					var character = input.selectionEnd;
				}
			}
			return character+1;
		}
		var character = getCharacter();
		var column = helene.util.tabs.charPosToColumn(character, this.value);
		return new helene.position(this.line, column, character);
	}
	this.setPos = function(line, column, skipTabs) {
		var editor = this.editor;
		var input = this;
		var result = true;
		function gotoCharacter(character) {
			if (document.selection) {
				var range = input.createTextRange();
				range.moveStart('character', character-1);
				range.collapse(true);
				range.select();
			} else {
				input.focus();
				input.setSelectionRange(character-1, character-1);
			}
		}
		function gotoLine(lineNo) {
			var result = true;
			input.apply();
			if (lineNo<1) {
				lineNo = 1;
				result = false;
			} else if (lineNo>editor.canvas.content.length) {
				lineNo = editor.canvas.content.length;
				result = false;
			}
			input.hide(); //input.style.visibility = 'hidden';
			var newPos = editor.canvas.content.getLine(lineNo).offsetTop;
			input.style.top = (newPos-2)+'px'; // FIXED CCI 4-15-09
			input.value = editor.canvas.content.getLine(lineNo).getContent();
			if (newPos<editor.canvas.scrollTop) {
				editor.canvas.scrollTop = newPos;
			} else if (newPos>(editor.canvas.scrollTop+editor.canvas.offsetHeight-input.offsetHeight)) {
				editor.canvas.scrollTop = newPos-(editor.canvas.offsetHeight)+input.offsetHeight;
			}
			input.line = lineNo;
			input.length = editor.canvas.content.getLine(lineNo).getLength();
			input.show(); //input.style.visibility = 'visible';
			return result;
		}
		gotoLine(line);
		if (column<1) {
			column = 1;
			result = false;
		} else {
			var length = this.editor.canvas.content.getLine(this.line).getLength();
			if (column>length) {
				column = length+1;
			}
			result = false;
		}
		this.column = helene.util.tabs.getRealColumn(column, this.value, skipTabs);
		this.character = helene.util.tabs.columnToCharPos(this.column, this.value);
		gotoCharacter(this.character);
		if (this.column<10) {
			this.editor.canvas.scrollLeft = '0px';
		}
		window.status = 'row: '+this.line+'   col: '+this.column;
		return result;
	}
	this.getTokenLeft = function() {
		if (document.selection) {
			var range = document.selection.createRange();
			range.moveStart('character', -1);
			var token = range.text;
		} else if (this.selectionStart) {
			var token = this.value.substr(this.selectionStart-1, 1);
		}
		return token;
	}
	this.getTokenRight = function() {
		if (document.selection) {
			var range = document.selection.createRange();
			range.moveEnd('character', 1);
			var token = range.text;
		} else {
			var token = this.value.substr(this.selectionStart, 1);
		}
		return token;
	}
	this.moveLeft = function() {
		var token = this.getTokenLeft();
		if (token) {
			if (token =='\t') {
				this.setPos(this.line, this.column-1);
				var pos = this.getPos();
			} else {
				if (document.selection) {
					var cursor = document.selection.createRange();
					cursor.moveStart('character', -1);
					cursor.moveEnd('character', -1);
					cursor.select();
				} else {
					this.setSelectionRange(this.selectionStart-1, this.selectionStart-1);
				}
				this.column--;
				this.character--;
				var pos = new helene.position(this.line, this.column, this.character);
			}
			window.status = 'row: '+this.line+'   col: '+this.column;
		} else {
			var pos = false;
		}
		return pos;
	}
	this.moveRight = function() {
		var token = this.getTokenRight();
		if (token) {
			if (token=='\t') {
				this.setPos(this.line, this.column+1, true);
				var pos = this.getPos();
			} else {
				if (document.selection) {
					var cursor = document.selection.createRange();
					cursor.moveStart('character', 1);
					// cursor.moveEnd('character', 1);
					cursor.select();
				} else {
					this.setSelectionRange(this.selectionStart+1, this.selectionStart+1);
				}
				this.column++;
				this.character++;
				var pos = new helene.position(this.line, this.column, this.character);
			}
			window.status = 'row: '+this.line+'   col: '+this.column;
		} else {
			var pos = false;
		}
		return pos;
	}
}
