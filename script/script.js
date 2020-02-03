function symbol(){
	document.getElementById('ans').addEventListener('keyup', e => {
		console.log('Caret at: ', e.target.selectionStart)
	})
}