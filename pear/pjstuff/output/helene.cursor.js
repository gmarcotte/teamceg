// cursor is the virtual cursor which keeps track of where the cursor should be
// it also has all the cursor handling methods (left, right, up, down, etc)
helene.cursor = function(editor) {
	this.editor=editor;
	this.column=1;
	this.line=1;
	this.uptodate=false;

	this.getRealPos=function() {
		return this.editor.canvas.input.getPos();
	}

	this.getPos=function() {
		if (!this.uptodate) {
			return this.editor.canvas.input.getPos();
		} else {
			return new helene.position(this.line, this.column, 0);
		}
	}

	this.setPos=function(line, column, skipTabs) {
		var result=this.editor.canvas.input.setPos(line, column, skipTabs);
		// this.editor.canvas.input.resetHeight();
		this.line=this.editor.canvas.input.line;
		this.column=column;
		this.uptodate=true;
		return result;
	}

	this.setRealPos=function(line, column, skipTabs) {
		var result=this.setPos(line, column, skipTabs);
		// this.editor.canvas.input.resetHeight();
		this.column=this.editor.canvas.input.column;
		return result;
	}
	
	this.down=function() {
		var pos=this.getPos();
		return this.setPos(pos.line+1, pos.column);
	}

	this.up=function() {
		var pos=this.getPos();
		return this.setPos(pos.line-1, pos.column);
	}

	this.left=function() {
		var pos=this.editor.canvas.input.moveLeft();
		if (pos) {
			this.column=pos.column;
			if (this.column<10) {
				this.editor.canvas.scrollLeft=0;
			} else if (helene.config.isMoz) {
				var xPos=this.column*this.editor.canvas.letterWidth+44-this.editor.canvas.letterWidth;
				var currX=this.editor.canvas.scrollLeft;
				if (currX>xPos) {
					this.editor.canvas.scrollLeft=xPos;
				}
			}
		} else {
			var line=this.editor.canvas.content.getLine(this.line-1);
			if (line) {
				this.setRealPos(this.line-1, line.getLength()+1);
				if (helene.config.isMoz) {
					var xPos=this.column*this.editor.canvas.letterWidth;
					var currX=this.editor.canvas.scrollLeft+this.editor.canvas.canvasWidth-44;
					if (currX<xPos) {
						this.editor.canvas.scrollLeft=(xPos-(this.editor.canvas.canvasWidth-44));
					}
				}
			}			
		}
	}

	this.right=function() {
		var pos=this.editor.canvas.input.moveRight();
		if (pos) {
			this.column=pos.column;
			if (helene.config.isMoz) {
				var xPos=this.column*this.editor.canvas.letterWidth;
				var currX=this.editor.canvas.scrollLeft+this.editor.canvas.canvasWidth-44;
				if (currX<xPos) {
					this.editor.canvas.scrollLeft=(xPos-(this.editor.canvas.canvasWidth-44));
				}
			}
		} else {
			var line=this.editor.canvas.content.getLine(this.line+1);
			if (line) {
				this.setRealPos(this.line+1, 1);
				this.editor.canvas.scrollLeft=0;
			}			
		}
	}

	this.home=function() {
		this.editor.canvas.scrollLeft=0;
		return this.setRealPos(this.line, 1);
	}

	this.end=function() {
		var result=this.setRealPos(this.line, this.editor.canvas.content.getLine(this.line).length+1);
		if (helene.config.isMoz) {
			var xPos=this.column*this.editor.canvas.letterWidth;
			var currX=this.editor.canvas.scrollLeft+this.editor.canvas.canvasWidth-44;
			if (currX<xPos) {
				this.editor.canvas.scrollLeft=(xPos-(this.editor.canvas.canvasWidth-44));
			}
		}
		return result;
	}

	this.top=function() {
		return this.setRealPos(1,1);
	}

	this.bottom=function() {
		var line=this.editor.canvas.content.getLine(this.editor.canvas.content.length);
		return this.setRealPos(this.editor.canvas.content.length, line.length+1);
	}

	this.pageUp=function() {
		var pos=this.getPos();
		return this.setPos(pos.line-helene.options.pageSize, pos.column);
	}

	this.pageDown=function() {
		var pos=this.getPos();
		return this.setPos(pos.line+helene.options.pageSize, pos.column);
	}

	this.wordRight=function() {
	}

	this.wordLeft=function() {
	}

}
