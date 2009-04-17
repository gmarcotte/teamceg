// content is the numbered list that contains the html-ized content of the source textarea
helene.content = function() {
	this.className = 'hlContent';
	this.maxLineLength = 0;
	this.length = 0;
	this.init = function(editor) {
		// now read the content from the source, and insert it into
		// the document
		this.editor = editor;
		this.setContent('');
		helene.event.attach(this, 'mousedown', helene.mouse.onMouseDown);
		helene.event.attach(this, 'mouseup', helene.mouse.onMouseUp);
	}
	this.setContent = function(sourceText) {
		this.clearContent();
		this.editor.canvas.input.hide();
		sourceArray = sourceText.replace(/\r/, '').split('\n');
		var line = null;
		this.maxLineLength = 0;;
		for (var i = 0; i<sourceArray.length; i++) {
			line = helene.util.createElement('editorLine');
			line.init(this.editor);
			line.setContent(sourceArray[i]);
			this.appendChild(line);			
			if (this.maxLineLength<line.length) {
				this.maxLineLength = line.length;
			}
		}
		this.length = sourceArray.length;
		this.editor.canvas.input.reset();
	}
	this.clearContent = function() {
		for (var i = this.childNodes.length-1; i>=0; i--) {
			this.removeChild(this.childNodes[i]);
		}
		this.maxLineLength = 0;
		this.length = 0;
	}
	this.getContent = function() {
		this.editor.canvas.input.apply();
		var content = '';
		if (this.length) {
			for (var i = 1; i<this.length; i++) {
				content+=this.getLine(i).getContent()+'\n';
			}
			content+=this.getLine(this.length).getContent();
		}
		return content;
	}
	this.getLine = function(number) {
		return this.childNodes[number-1];
	}
	this.setLine = function(number, value) {
		return this.childNodes[number-1].setContent(value);
	}
	this.appendLine = function(number, value) {
		var line = helene.util.createElement('editorLine');
		line.init(this.editor);
		line.setContent(value);
		if (number>=this.length) {
			this.appendChild(line);
		} else { 
			var nextLine = this.getLine(number+1);
			this.insertBefore(line, nextLine);
		}
		this.length++;
	}
	this.removeLine = function(number) {
		this.removeChild(this.childNodes[number-1]);
		this.length--;
	}
	this.getLetterWidth = function() {
		// calculate letter width 
		var textNode = document.createTextNode('M');
		var spanLocator = document.createElement('span');
		spanLocator.style.backgroundColor = 'red';	
		spanLocator.appendChild(textNode);
		var listItem = helene.util.createElement('editorLine');
		listItem.appendChild(spanLocator);
		this.appendChild(listItem);
		var letterWidth = spanLocator.offsetWidth;
		this.removeChild(listItem);
		return letterWidth;
	}
}

