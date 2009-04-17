// keyboard contains all keyboard handling code, including key bindings for different editor behaviours
helene.keyboard = {
	behaviour:'default',
	binding:{
		'default':function(editor) {
			return {
				'default':	function() { editor.doCleanState(); return true; },
				'40':		function() { editor.cursor.down(); return false; },
				's40':		function() { editor.selection.down(); return false; },
				'38':		function() { editor.cursor.up(); return false; },
				's38':		function() { editor.selection.up(); return false; },
				'37':		function() { editor.cursor.left(); return false; },
				's37':		function() { editor.selection.left(); return false; },
				'39':		function() { editor.cursor.right(); return false; },
				's39':		function() { editor.selection.right(); return false; },
				'8':		function() { editor.doBackspace(); return false; },
				'46':		function() { editor.doDelete(); return false; },
				'13':		function() { editor.insertLinebreak(); return false; },
				'34':		function() { editor.cursor.pageDown(); return false; },
				's34':		function() { editor.selection.pageDown(); return false; },
				'33':		function() { editor.cursor.pageUp(); return false; },
				's33':		function() { editor.selection.pageUp(); return false; },
				'35':		function() { editor.cursor.end(); return false; },
				's35':		function() { editor.selection.end(); return false; },
				'c35':		function() { editor.cursor.bottom(); return false; },
				'cs35':		function() { editor.selection.bottom(); return false; },
				'36':		function() { editor.cursor.home(); return false; },
				's36':		function() { editor.selection.home(); return false; },
				'c36':		function() { editor.cursor.top(); return false; },
				'cs36':		function() { editor.selection.top(); return false; },
				'9':		function() { editor.insertTab(); return false; },
				'c86':		function() { editor.paste(); return true; },
				'c67':		function() { editor.copy(); return false; },
				'c88':		function() { editor.cut(); return false; },
				'c90':		function() { editor.undo(); return false; },
				'c89':		function() { editor.redo(); return false; },
				'cs90':		function() { editor.redo(); return false; },
				's16':		function() { return true; },
				'c17':		function() { return true; },
				'a18':		function() { return true; },
				'cs16':		function() { return true; },
				'cs17':		function() { return true; },
				'as16':		function() { return true; },
				'as18':		function() { return true; },
				'ac18':		function() { return true; },
				'ac17':		function() { return true; }
			}
		},
		'joe':function(editor) {
			return helene.keyboard.binding.merge(
				helene.keyboard.binding['default'](editor),
				{
					'c65':		function() { editor.cursor.home(); return false; },
					'c69':		function() { editor.cursor.end(); return false; },
					'c88':		function() { editor.cursor.wordRight(); return false; },
					'c90':		function() { editor.cursor.wordLeft(); return false; },
					'c75':		function() {
									editor.keyboard=helene.keyboard.binding['joeCtrlK'](editor);
									return false;
								},
					'cs189':	function() { editor.undo(); return false; },
					'cs109':	function() { editor.undo(); return false; },
					'cs54':		function() { editor.redo(); return false; }
				}
			);
		return false; },
		'joeCtrlK':function(editor) {
			return helene.keyboard.binding.merge(
				helene.keyboard.binding['default'](editor),
				{
					'85':		function() { editor.cursor.top(); editor.keyboard['default'](); return false; },
					'86':		function() { editor.cursor.bottom(); editor.keyboard['default'](); return false; },
					'default':	function() {
									editor.keyboard=helene.keyboard.binding['joe'](editor);
									return false;
								}
				}
			);
		}
	},
	getCharCode:function(evt) {
			return (evt.charCode ? evt.charCode : ((evt.keyCode) ? evt.keyCode : evt.which));
	},
	onKeyUp:function(evt) {
	},
	onKeyDown:function(evt) {
		var charCode;
		var charString = '';
		var keyResult;

		evt = helene.event.get(evt);
		if( evt ) {
			// Get the key pressed
			charCode = helene.keyboard.getCharCode(evt);

			// Create the encoded character string
			charString = charCode;

			if( evt.shiftKey ) {
				charString = 's' + charString;
			}
			if( evt.ctrlKey ) {
				charString = 'c' + charString;
			}
			if( evt.altKey ) {
				charString = 'a' + charString;
			}
//			window.status = '{'+charString+'}';
			if( this.editor.keyboard[charString] ) {
				window.status = '{'+charString+': found}';
				keyResult = this.editor.keyboard[charString](evt);
			} else {
				window.status = '{'+charString+': default}';
				keyResult = this.editor.keyboard["default"](evt);
			}

			if( ! keyResult ) {
				helene.event.cancel(evt);
				this.editor.cancelKey = true; // Mozilla can only cancel it on onKeyPress, so remember to do that
			}
			return keyResult;
		}
	},
	onKeyPress:function(evt) {
		if (helene.config.isMoz && this.editor.cancelKey) {
			this.editor.cancelKey=false;
			return helene.event.cancel(evt);
		} else {
			return helene.event.pass(evt);
		}
	}
}
