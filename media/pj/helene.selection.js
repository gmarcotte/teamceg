// selection keeps track of a selection if it is available, and has all the cursor
// methods for cursor movement which changes the position/size of the selection
// this code needs a rewrite, the best way is to simply use the cursor/input textarea to also mark selections
// that way you can use the browsers textarea copy/paste functionality
// no need for flash objects or method calls marked unsafe (mozilla)


// CCI TODO: deal with the weirdnesses of selection and make them a bit more intuitive
// Also need to fix the apparent offset..

helene.selection = function(editor) {
	this.editor	= editor;
	
	// keep track of start and end position of selection
	this.start	= null;
	this.end	= null;

	this.unselect = function() {
		this.start	= null;
		this.end	= null;
		this.editor.canvas.removeChild(this.editor.canvas.selection);
		this.editor.canvas.selection = null;
	}
	
	this.select=function(start, end) {

		var editor = this.editor;
		
    // This is a total hack -- wtf were they thinking? needs to be fixed!
		function hlAddSelectLine(line, start, end) {
      // CCI TODO fix the weird offset error
			var tl = {
				x:line.offsetLeft+((start)*editor.canvas.letterWidth),
				y:line.offsetTop
			}
			var br = {
				x:line.offsetLeft+((end)*editor.canvas.letterWidth),
				y:line.offsetTop+line.offsetHeight
			}
			var line = document.createElement('DIV');
			line.style.position = 'absolute';
			line.className='hlSelection';
			line.style.top = (tl.y)+'px'; // CCI fixed
			line.style.left = tl.x+'px';
			line.style.height = (br.y - tl.y)+'px';
			line.style.width = (br.x - tl.x)+'px';
			return line;
		}
		
		// swap start and end if start > end
		if (start.largerThan(end)) {
			this.start = end;
			this.end = start;
		} else {
			this.start = start;
			this.end = end;
		}

    // if there are no selections, make a new one
		if (!this.editor.canvas.selection) {
			var selection = document.createElement('div');
			selection.style.position='absolute';
			selection.style.height='100%';
			selection.style.width='100%';
			selection.style.top='-1px';
			selection.style.left='0px';
			this.editor.canvas.appendChild(selection);
			this.editor.canvas.selection = selection;
		}
		
		// check to see if the current selection matches one of the start/end values
    // CCI TODO: we have already swapped the start and end values if they were switched,
    // so this might be wrong?
		if (this.editor.canvas.selection.start 
			&& this.editor.canvas.selection.start == this.start) {
			// start matches, so change only end
			var endLine = this.editor.canvas.content.getLine(this.end.line);
			if (this.end.line == this.start.line) {
				var startCol = this.start.column;
			} else {
				var startCol = 1;
			}
			if (this.editor.canvas.selection.end.line == this.end.line) {
				// just change last line a bit
				var hl = hlAddSelectLine(endLine, startCol, this.end.column);
				this.editor.canvas.selection.replaceChild(hl, this.editor.canvas.selection.lastChild);
			} else if (this.editor.canvas.selection.end.largerThan(this.end)) {
				// shrink
				while (this.editor.canvas.selection.lastChild.offsetTop>endLine.offsetTop) {
					this.editor.canvas.selection.removeChild(this.editor.canvas.selection.lastChild);
				}
				var hl = hlAddSelectLine(endLine, startCol, this.end.column);
				this.editor.canvas.selection.replaceChild(hl, this.editor.canvas.selection.lastChild);
			} else {
				// grow
				var prevEnd = this.editor.canvas.selection.end;
				var prevLastLine = this.editor.canvas.content.getLine(prevEnd.line);
				if (this.end.line = this.start.line) {
					startCol = this.start.column;
				} else {
					startCol = 1;
				}
				var hl = hlAddSelectLine(prevLastLine, startCol, prevLastLine.getLength()+1);
				this.editor.canvas.selection.replaceChild(hl, this.editor.canvas.selection.lastChild);
				var max = this.end.line - this.start.line - 1;
				var i = prevEnd.line - this.start.line;
				while (i<max) {
					var line = this.editor.canvas.content.getLine(this.start.line + i + 1);
					var highlight = hlAddSelectLine(line, 1, line.getLength()+1);
					this.editor.canvas.selection.appendChild(highlight);
					i++;
				}
				var highlight = hlAddSelectLine(endLine, 1, this.end.column);		
				this.editor.canvas.selection.appendChild(highlight);
			}
		} else if (this.editor.canvas.selection.end 
			&& this.editor.canvas.selection.end == this.end) {
			// end matches, so change only start
			var startLine = this.editor.canvas.content.getLine(this.start.line);
			if (this.start.line == this.end.line) {
				var endCol = this.end.column;
			} else {
				var endCol = startLine.getLength()+1;
			}
			if (this.editor.canvas.selection.start.line == this.start.line) {
				// just change first line a bit
				var hl = hlAddSelectLine(startLine, this.start.column, endCol);
				this.editor.canvas.selection.replaceChild(hl, this.editor.canvas.selection.firstChild);
			} else if (this.editor.canvas.selection.start.smallerThan(this.start)) {
				// shrink
				var newStartLine = this.editor.canvas.content.getLine(this.start.line);
				while (this.editor.canvas.selection.firstChild.offsetTop<newStartLine.offsetTop) {
					this.editor.canvas.selection.removeChild(this.editor.canvas.selection.firstChild);
				}
				var hl = hlAddSelectLine(startLine, this.start.column, endCol);
				this.editor.canvas.selection.replaceChild(hl, this.editor.canvas.selection.firstChild);
			} else {
				// grow
				var prevStart = this.editor.canvas.selection.start;
				var prevFirstLine = this.editor.canvas.content.getLine(prevStart.line);
				if (this.end.line = this.start.line) {
					endCol = this.end.column;
				} else {
					endCol = prevFirstLine.getLength()+1;
				}
				var hl = hlAddSelectLine(prevFirstLine, 1, endCol);
				this.editor.canvas.selection.replaceChild(hl, this.editor.canvas.selection.firstChild);
				var prevFirstChild = hl;
				var hl = hlAddSelectLine(startLine, this.start.column, startLine.getLength()+1);
				this.editor.canvas.selection.insertBefore(hl, prevFirstChild);
				var max = prevStart.line - this.start.line;
				var i = 1;
				while (i<max) {
					var line = this.editor.canvas.content.getLine(this.start.line + i);
					var hl = hlAddSelectLine(line, 1, line.getLength()+1);
					this.editor.canvas.selection.insertBefore(hl, prevFirstChild);
					i++;
				}
			}
		} else {
			// completely new
			// remove old selection
			this.editor.canvas.selection.innerHTML='';
			var startLine = this.editor.canvas.content.getLine(this.start.line);
			var endLine = this.editor.canvas.content.getLine(this.end.line);
			// draw from start to end
			if (this.start.line==this.end.line) {
				// single line
				var hl = hlAddSelectLine(startLine, this.start.column, this.end.column);
				this.editor.canvas.selection.appendChild(hl);
			} else {
				// top, middle and bottom div
				// top div and bottom div
				var hl = hlAddSelectLine(startLine, this.start.column, startLine.getLength()+1);
				this.editor.canvas.selection.appendChild(hl);
				var max = this.end.line - this.start.line;
				var i = 1;
				while (i<max) {
					var line = this.editor.canvas.content.getLine(this.start.line + i);
					var hl = hlAddSelectLine(line, 1, line.getLength()+1);
					this.editor.canvas.selection.appendChild(hl);
					i++;
				}
				var hl = hlAddSelectLine(endLine, 1, this.end.column);
				this.editor.canvas.selection.appendChild(hl);
			}
		}
		this.editor.canvas.selection.start = this.start;
		this.editor.canvas.selection.end = this.end;
	}
	
	this.getText=function() {
		if (this.editor.canvas.selection) {
			var text = '';
			var startLine = this.editor.canvas.content.getLine(this.start.line);
			var endLine = this.editor.canvas.content.getLine(this.end.line);
			if (this.start.line==this.end.line) {
				var text = startLine.getContent().substring(this.start.character-1, this.end.character-1);
			} else if ((this.end.line-this.start.line)==1) {
				var text = startLine.getContent().substring(this.start.character-1)+"\r\n";
				text += endLine.getContent().substring(0, this.end.character-1);
			} else {
				var text = startLine.getContent().substring(this.start.character-1)+"\r\n";
				var max = this.end.line - this.start.line - 1;
				var i =0;
				while (i<max) {
					var line = this.editor.canvas.content.getLine(this.start.line + i + 1);
					text += line.getContent()+"\r\n"
					i++;
				}
				text += endLine.getContent().substring(0, this.end.character-1);
			}
			return text;
		} else {
			return false;
		}
	}

  
  // added CCI 4-17-09
  // sets the listen select to the specified area.
  this.listenSelect=function(startline, startcol, endline, endcol) {
    var pos = this.editor.canvas.input.getPos();
    var start = pos;
    var end = pos;
    start.column = startcol;
    start.line = startline;
    end.column = endcol;
    end.line = endline;
    this.select(start,end);
  }
  
	this.moveEnd=function(end) {
	}

	this.moveStart=function(start) {
	}

	this.down=function() {
		//this.editor.canvas.input.growHeight(1);
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.down();
		var postPos=this.editor.canvas.input.getPos();

		// check if there is a selection, if not: start one
		if (!this.start) {
			this.select(prePos, postPos);
		} else {
			// if cursor is at the end of the selection, enlarge selection
			// if cursor is at the start of the selection, shrink selection
			if (this.end.compare(prePos)==0) {
				// grow
				this.select(this.start, postPos);
			} else {
				// shrink
				this.select(postPos, this.end);
			}
		}
	}

  // CCI
  this.doHighlight=function() {
    if (this.start) {
        //alert("ending selection")
        this.end = this.editor.canvas.input.getPos();
        this.select(this.start, this.end);
    }
    else {
      //alert("starting selection")
      this.start = this.editor.canvas.input.getPos();
    }
  }
  this.clearHighlight=function(){
    
    
  }
  this.startSelect=function() {
    //alert("starting selection")
    this.start = this.editor.canvas.input.getPos();
  }
  this.endSelect=function() {
    //alert("ending selection")
    if (this.start){
      this.end = this.editor.canvas.input.getPos();
      this.select(this.start, this.end);
    }
    
  }
  
  this.line=function() {
    alert("here")
    this.editor.cursor.down();
    var pos = this.editor.canvas.input.getPos();
    var s = pos;
    s.column = 0;
    var e = pos;
    e.column = 10;
    this.select(s, e);
  }
  // let's just make this highlight a whole line instead...CCI 4-17-09
	this.up=function() {
		this.editor.cursor.down();
    var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.up();
		var postPos=this.editor.canvas.input.getPos();
    // select the whole line
    // so position for selection needs to be the (line, 0)->(line, end)
    this.select(prePos, postPos);
		// check if there is a selection, if not: start one
		/*if (!this.start) {
			this.select(prePos, postPos);
		} else {
			// if cursor is at the start of the selection, enlarge selection
			// if cursor is at the end of the selection, shrink selection
			if (this.start.compare(prePos)==0) {
				//grow
				this.select(postPos, this.end);
			} else {
				// shrink
				this.select(this.start, postPos);
			}
		}*/
	}

  
	this.left=function() {
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.left();
		var postPos=this.editor.canvas.input.getPos();

		if (!this.start) {
			window.status='[]';
			this.select(postPos, prePos);
		} else {
			// if cursor is at the start of the selection, enlarge selection
			// if cursor is at the end of the selection, shrink selection
			if (this.start.compare(prePos)==0) {
				//grow
				this.select(postPos, this.end);
			} else {
				// shrink
				this.select(this.start, postPos);
			}
		}

	}

	this.right=function() {
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.right();
		var postPos=this.editor.canvas.input.getPos();
		// check if there is a selection, if not: start one
		if (!this.start) {
			this.select(prePos, postPos);
		} else {
			// if cursor is at the end of the selection, enlarge selection
			// if cursor is at the start of the selection, shrink selection
			if (this.end.compare(prePos)==0) {
				// grow
				this.select(this.start, postPos);
			} else {
				// shrink
				this.select(postPos, this.end);
			}
		}
	}

	this.home=function() {
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.home();
		var postPos=this.editor.canvas.input.getPos();
		// check if there is a selection, if not: start one
		if (!this.start) {
			this.start=postPos;
			this.end=prePos;
		}
		// if cursor is at the start of the selection, enlarge to home
		// if cursor is at the end:
		//   if selection is single line, set end point to start point, set start point to home
		//   else shrink selection to home
	}

	this.end=function() {
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.end();
		var postPos=this.editor.canvas.input.getPos();
		// check if there is a selection, if not: start one
		if (!this.start) {
			this.start=prePos;
			this.end=postPos;
		}
		// if cursor is at the end of the selection, enlarge to end
		// if cursor is at the start:
		//   if selection is single line, set start point to end point, set end point to end
		//   else shrink selection to end
	}

	this.top=function() {
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.top();
		var postPos=this.editor.canvas.input.getPos();
		// check if there is a selection, if not: start one
		if (!this.start) {
			this.start=postPos;
			this.end=prePos;
		}
		// if cursor is at the start of the selection, enlarge to top
		// else set end point to start point, set start point to top
	}

	this.bottom=function() {
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.bottom();
		var postPos=this.editor.canvas.input.getPos();
		// check if there is a selection, if not: start one
		if (!this.start) {
			this.start=prePos;
			this.end=postPos;
		}
		// if cursor is at the end of the selection, enlarge to bottom
		// else set start point to end point, set end point to bottom
	}

	this.pageUp=function() {
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.pageUp();
		var postPos=this.editor.canvas.input.getPos();
		// check if there is a selection, if not: start one
		if (!this.start) {
			this.start=postPos;
			this.end=prePos;
		}
	}

	this.pageDown=function() {
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.pageDown();
		var postPos=this.editor.canvas.input.getPos();
		// check if there is a selection, if not: start one
		if (!this.start) {
			this.start=prePos;
			this.end=postPos;
		}
	}

	this.wordRight=function() {
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.wordRight();
		var postPos=this.editor.canvas.input.getPos();
		// check if there is a selection, if not: start one
		if (!this.start) {
			this.start=prePos;
			this.end=postPos;
		}
	}

	this.wordLeft=function() {
		var prePos=this.editor.canvas.input.getPos();
		this.editor.cursor.wordLeft();
		var postPos=this.editor.canvas.input.getPos();
		// check if there is a selection, if not: start one
		if (!this.start) {
			this.start=postPos;
			this.end=prePos;
		}
	}
}
