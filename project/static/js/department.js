function setupDepartment() {
	document.getElementById("editDeptName").value = department

	document.getElementById("editDeptConfirmButton").addEventListener("click", () => {
		let body = {
			name: document.querySelector("#editDeptName").value
		}
		console.log(body)
		sendRequest("PUT", endpoints['departments_api'] + department, body)
                    .then(data => {
                    	for (let span of document.querySelectorAll('.department-name'))
                    		span.innerHTML = data.name
						console.info('Department data updated')
						showInfoMessage('Department data updated')
                    })
	})

	document.getElementById("deleteDeptConfirmButton").addEventListener("click", () => {
		sendRequest("DELETE", endpoints["departments_api"] + department).then(() => {
		    window.location.replace(endpoints['index'])
			console.info('Department removed')
			showInfoMessage('Department removed')
		})
	})
}