function setupDepartment() {
	document.getElementById("editDeptName").value = department

	document.getElementById("editDeptConfirmButton").addEventListener("click", () => {
		let body = {
			name: document.querySelector("#editDepartment").value
		}
		sendRequest("PUT", endpoints['departments_api'] + department, body)
                    .then(data => {
                    	for (let span of document.querySelectorAll('.department-name'))
                    		span.innerHTML = data.name
                    })
	})

	document.getElementById("deleteDeptConfirmButton").addEventListener("click", () => {
		sendRequest("DELETE", endpoints["departments_api"] + department).then(() => {
		    window.location.replace(endpoints['index']);
		})
	})
}