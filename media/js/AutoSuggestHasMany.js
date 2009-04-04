function remove_assign_id(object_name, id) {
	el = $('id_' + object_name + 's');
	array = el.value.split(',');
	
	// Remove elements
	if (array.indexOf(id.toString()) >= 0) {
		array.remove(id.toString());
		$(object_name + '_' + id.toString()).remove();
	}

	el.value = array.join(',');
}

function autosuggest_options(url, object_name) {
	return {
		script:url,
		varname:"q",
		json:true,
		shownoresults:true,
		maxresults:6,
		callback: function (obj) {
			el = $('id_' + object_name + 's');
			array = el.value.split(',');
			
			if (array.indexOf(obj.id) == -1) {
				// Display object name
				new_el = new Element('li', 
									{'id': object_name + '_' + obj.id, 
									 'styles': {'color': 'green'}});
				new_el.setHTML(obj.value + ' <a href="#" onclick="remove_assign_id(\'' + object_name + '\',\'' + obj.id + '\'); return false;">[Remove]</a>');
				new_el.injectTop($('id_' + object_name + 's_list'));	
			}
			
			// Add object ID to input
			if (array[0] == '') {
				el.value = obj.id;
			}
			else {
				array.include(obj.id);
				el.value = array.join(',');
			}
			
			// Clear input
			input = $('id_' + object_name + 's_input');
			input.value = "";
		}		
	}
}

window.addEvent('domready', function() {
	$$('input.vModelHasManyWidget').each(function(el_input){
		object_name = el_input.getProperty('name');
		object_name = object_name.substring(0, object_name.lastIndexOf('s_input'));
		url = el_input.getProperty('src');
		
		new bsn.AutoSuggest('id_' + object_name + 's_input', autosuggest_options(url, object_name));
	});
});