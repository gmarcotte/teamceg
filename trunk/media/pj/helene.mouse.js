// mouse contains all the mouse handling code, including position calculation
helene.mouse = {

	getTarget:function(evt) {
		return (evt.target) ? evt.target : evt.srcElement;
	},

	getPos:function(evt) {
		var target=helene.mouse.getTarget(evt);
		// get click position
		if (evt.pageX) {
			var offsetX=evt.pageX - ((target.offsetLeft) ? target.offsetLeft : target.left);
			var offsetY=evt.pageY - ((target.offsetTop) ? target.offsetTop : target.top);
		} else if (evt.clientX || evt.clientY) {
			var offsetX = evt.clientX - ((target.offsetLeft) ? target.offsetLeft : 0);
			var offsetY = evt.clientY - ((target.offsetTop) ? target.offsetTop : 0);
		}
		// since we only have the page coordinates, calculate the offset of the editor
		// on the page
		var offsetParent=target.offsetParent;
		while (offsetParent) {
			offsetX-=offsetParent.offsetLeft;
			offsetY-=offsetParent.offsetTop;
			if (offsetParent.tagName=='BODY') {
				break;
			}
			offsetParent=offsetParent.offsetParent;
		}
		// add the offset from the canvas scrollbars (and an offset of half the letterwidth for easier mouse positioning)
		offsetX+=target.editor.canvas.scrollLeft + Math.floor(target.editor.canvas.letterWidth/2);
		offsetY+=target.editor.canvas.scrollTop;
		// calculate the lineNo and column
		var x=1;
		var y=1;
		switch(target.tagName) {
			case 'TEXTAREA':
				y=target.line;
				x=Math.round(offsetX/target.editor.canvas.letterWidth);
			break;
			case 'DIV':
				target=target.content;
			// FALLTHROUGH					
			case 'OL':
				// clicked outside LI element, so first find the correct list item
				y=0;
				var temp=target.firstChild;
				while (temp && temp.offsetTop<offsetY) {
					temp=temp.nextSibling;
					y++;
				}
				x=Math.round(offsetX/target.editor.canvas.letterWidth);
			break;
			case 'LI':
				y=1;
				var temp=target;
				while (temp=temp.previousSibling) {
					y++;
				}
				x=Math.round(offsetX/target.editor.canvas.letterWidth);
			break;
		}
		return new helene.position(y, x, 0);
	},

  // CCI TODO: the cancel call seems to be a little bit sketchy
	onMouseDown:function(evt) {
		evt=helene.event.get(evt);
		return helene.event.cancel(evt);
	},

	onMouseUp:function(evt) {
		evt=helene.event.get(evt);
		var pos=helene.mouse.getPos(evt);
		this.editor.cursor.setRealPos(pos.line, pos.column, pos.character);
		return helene.event.cancel(evt);
	}
}
